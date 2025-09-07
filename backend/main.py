#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    DOMAIN PROGRESS TRACKER BACKEND - FASTAPI
================================================================================

MÔ TẢ TỔNG QUAN:
    Ứng dụng backend được xây dựng bằng FastAPI để theo dõi tiến độ học tập 
    thông qua hệ thống XP/Level giống như game. Hệ thống sẽ quét các thư mục 
    domain học tập và tính toán điểm kinh nghiệm (XP) dựa trên số lượng bài viết 
    và nội dung học tập.

CHỨC NĂNG CHÍNH:
    1. Quét và phân tích các thư mục domain học tập
    2. Tính toán XP và Level dựa trên số bài viết và từ ngữ
    3. Theo dõi streak days (số ngày liên tiếp học tập)
    4. Cung cấp API RESTful để frontend có thể truy cập dữ liệu
    5. Thống kê tổng quan về tiến độ học tập

CẤU TRÚC HỆ THỐNG:
    - Domain 1: Mathematical & Statistical Foundation (Màu Indigo)
    - Domain 2: Programming & Software Engineering (Màu Emerald)
    - Domain 3: Machine Learning Fundamentals (Màu Amber)
    - Domain 4: Deep Learning & Neural Networks (Màu Pink)
    - Domain 5: Data Engineering & Processing (Màu Blue)
    - Domain 6: Production Systems & MLOps (Màu Violet)
    - Domain 7: Cloud & Infrastructure (Màu Red)
    - Domain 8: Advanced AI Applications (Màu Teal)
    - Domain 9: Research & Innovation (Màu Orange)
    - Domain 10: Business & Entrepreneurship (Màu Lime)

CÔNG THỨC TÍNH XP:
    - Base XP: 100 điểm cho mỗi bài viết
    - Bonus XP: 1 điểm cho mỗi 10 từ trong nội dung
    - Tổng XP = (Số bài viết × 100) + (Tổng từ ÷ 10)

CÔNG THỨC TÍNH LEVEL:
    - Level 1: Cần 1000 XP
    - Level 2: Cần 1500 XP (1000 × 1.5)
    - Level 3: Cần 2250 XP (1500 × 1.5)
    - Level n: Cần 1000 × (1.5^(n-1)) XP

API ENDPOINTS:
    - GET /: Thông tin cơ bản về API
    - GET /api/domains: Lấy danh sách tất cả domains với XP/Level
    - POST /api/domains/refresh: Làm mới dữ liệu domains
    - GET /api/domains/stats: Lấy thống kê tổng quan

TÁC GIẢ: Hệ thống theo dõi tiến độ học tập
NGÀY TẠO: 2024
PHIÊN BẢN: 1.0.0
================================================================================
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import re

app = FastAPI(
    title="Domain Progress Tracker API",
    description="API để scan và tính toán XP/Level cho các domain học tập",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình
DATA_SCIENCE_PATH = r"D:\vip_DOCUMENTS_OBS\home\DATA SCIENCE AND AI"
SUPPORTED_EXTENSIONS = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf'}

# Pydantic Models
class DomainData(BaseModel):
    xp: int
    level: int
    color: str
    taskCount: int
    streakDays: int
    maxStreakDays: int
    totalDays: int
    lastTaskDate: str

class DomainsResponse(BaseModel):
    success: bool
    domains: Dict[str, DomainData]
    count: int
    last_scan: str

class StatsResponse(BaseModel):
    success: bool
    stats: Dict[str, Any]
    last_scan: str

class ErrorResponse(BaseModel):
    success: bool
    error: str

# Domain colors mapping
DOMAIN_COLORS = {
    'Domain 1': '#4F46E5',  # Indigo - Mathematical Foundation
    'Domain 2': '#10B981',  # Emerald - Programming & Software Engineering  
    'Domain 3': '#F59E0B',  # Amber - Machine Learning Fundamentals
    'Domain 4': '#EC4899',  # Pink - Deep Learning & Neural Networks
    'Domain 5': '#3B82F6',  # Blue - Data Engineering & Processing
    'Domain 6': '#8B5CF6',  # Violet - Production Systems & MLOps
    'Domain 7': '#EF4444',  # Red - Cloud & Infrastructure
    'Domain 8': '#14B8A6',  # Teal - Advanced AI Applications
    'Domain 9': '#F97316',  # Orange - Research & Innovation
    'Domain 10': '#84CC16', # Lime - Business & Entrepreneurship
    'default': '#6B7280'    # Gray
}

def get_domain_color(domain_name):
    """
    Lấy màu sắc tương ứng cho domain dựa trên tên domain
    
    Args:
        domain_name (str): Tên của domain (ví dụ: "Domain 1 Mathematical Foundation")
        
    Returns:
        str: Mã màu hex tương ứng với domain, mặc định là màu xám nếu không tìm thấy
        
    Ví dụ:
        get_domain_color("Domain 1 Mathematical") -> "#4F46E5" (Indigo)
        get_domain_color("Domain 2 Programming") -> "#10B981" (Emerald)
        get_domain_color("Unknown Domain") -> "#6B7280" (Gray)
    """
    for key, color in DOMAIN_COLORS.items():
        if key in domain_name:
            return color
    return DOMAIN_COLORS['default']

def calculate_xp_from_articles(articles_count, total_words):
    """
    Tính toán điểm kinh nghiệm (XP) dựa trên số lượng bài viết và tổng số từ
    
    Công thức tính XP:
    - Base XP: 100 điểm cho mỗi bài viết
    - Bonus XP: 1 điểm cho mỗi 10 từ trong nội dung
    - Tổng XP = Base XP + Bonus XP
    
    Args:
        articles_count (int): Số lượng bài viết/tài liệu trong domain
        total_words (int): Tổng số từ trong tất cả bài viết
        
    Returns:
        int: Tổng điểm XP được tính toán
        
    Ví dụ:
        calculate_xp_from_articles(5, 2500) -> 750 XP
        # Base: 5 × 100 = 500 XP
        # Bonus: 2500 ÷ 10 = 250 XP
        # Tổng: 500 + 250 = 750 XP
    """
    # Base XP: 100 XP per article
    base_xp = articles_count * 100
    
    # Bonus XP: 1 XP per 10 words
    word_bonus = total_words // 10
    
    return base_xp + word_bonus

def calculate_level_from_xp(xp):
    """
    Tính toán level dựa trên tổng điểm XP (hệ thống tương tự game)
    
    Công thức tính level:
    - Level 1: Cần 1000 XP
    - Level 2: Cần 1500 XP (1000 × 1.5)
    - Level 3: Cần 2250 XP (1500 × 1.5)
    - Level n: Cần 1000 × (1.5^(n-1)) XP
    
    Args:
        xp (int): Tổng điểm XP hiện tại
        
    Returns:
        int: Level tương ứng với số XP
        
    Ví dụ:
        calculate_level_from_xp(800) -> 0 (chưa đủ XP cho level 1)
        calculate_level_from_xp(1200) -> 1 (đủ XP cho level 1, còn 200 XP)
        calculate_level_from_xp(2500) -> 2 (đủ XP cho level 1 và 2)
    """
    level = 0
    required_xp = 1000  # Base XP required for level 1
    LEVEL_XP_MULTIPLIER = 1.5
    
    current_xp = xp
    while current_xp >= required_xp:
        level += 1
        current_xp -= required_xp
        required_xp = int(1000 * (LEVEL_XP_MULTIPLIER ** level))
    
    return level

def estimate_word_count(file_path, file_ext):
    """
    Ước tính số từ trong file dựa trên loại file và nội dung
    
    Hỗ trợ các loại file:
    - .txt, .md: Đếm từ trực tiếp từ nội dung text
    - .html: Loại bỏ HTML tags rồi đếm từ
    - Các loại khác: Ước tính dựa trên kích thước file
    
    Args:
        file_path (str): Đường dẫn đến file cần đếm từ
        file_ext (str): Phần mở rộng của file (ví dụ: '.md', '.txt')
        
    Returns:
        int: Số từ ước tính trong file
        
    Ví dụ:
        estimate_word_count("note.md", ".md") -> 150 (đếm từ thực tế)
        estimate_word_count("doc.docx", ".docx") -> 200 (ước tính từ kích thước)
    """
    try:
        if file_ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                words = len(content.split())
                return words
        elif file_ext == '.html':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                clean_text = re.sub(r'<[^>]+>', ' ', content)
                words = len(clean_text.split())
                return words
        else:
            # Ước tính dựa trên kích thước file
            file_size = os.path.getsize(file_path)
            estimated_words = file_size // 5
            return max(100, estimated_words)
    except:
        return 500  # Giá trị mặc định

def calculate_streak_days(article_dates):
    """
    ================================================================================
                            TÍNH TOÁN WRITING STREAK HIỆN TẠI
    ================================================================================
    
    MỤC ĐÍCH:
        Tính toán số ngày liên tiếp (không gián đoạn) có hoạt động viết bài,
        đếm từ ngày gần nhất có bài viết trở về quá khứ cho đến khi gặp khoảng trống.
    
    ĐỊNH NGHĨA STREAK:
        - Streak = Chuỗi ngày liên tiếp có bài viết
        - Liên tiếp = Không được thiếu ngày nào giữa chừng  
        - Dừng ngay khi gặp gap (ngày không có bài viết)
        - Flexible mode: Không bắt buộc phải viết hôm nay
    
    THUẬT TOÁN TỐI ƯU:
        1. 📊 DATA PROCESSING: Chuyển thành set để lookup O(1)
        2. 🎯 FLEXIBLE MODE: Tìm ngày gần nhất có bài viết làm điểm bắt đầu
        3. ⚡ DYNAMIC LIMIT: Tính toán giới hạn dựa trên dữ liệu thực tế
        4. 🔄 BACKWARD COUNTING: Đếm ngược từ điểm bắt đầu về quá khứ
        5. 🛑 STOP ON GAP: Dừng ngay khi gặp ngày đầu tiên không có bài viết
    
    PERFORMANCE:
        - Time Complexity: O(n + k) với n=số bài viết, k=streak length
        - Space Complexity: O(d) với d=số ngày unique
        - Optimizations: Set comprehension, generator expression, dynamic limits
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
                             Có thể chứa nhiều bài viết cùng ngày (sẽ được deduplicate)
        
    Returns:
        int: Số ngày liên tiếp học tập (streak days)
             - 0 nếu không có bài viết hoặc không có bài viết trước hôm nay
             - 1+ nếu có streak (bao gồm cả streak độc lập không kết thúc hôm nay)
        
    Ví dụ thực tế:
        Input: [2025-09-06, 2025-09-05, 2025-09-03, 2025-09-01]
        Hôm nay: 2025-09-07
        
        Quá trình:
        1. Hôm nay (07) không có bài viết → Bắt đầu từ 06
        2. Ngày 06: ✅ có → streak = 1
        3. Ngày 05: ✅ có → streak = 2  
        4. Ngày 04: ❌ không có → DỪNG
        
        Kết quả: streak = 2
    """
    # ============================================================================
    # BƯỚC 1: VALIDATION & INPUT PROCESSING
    # ============================================================================
    
    # Kiểm tra input rỗng - edge case cơ bản nhất
    if not article_dates:
        print("🔥 STREAK DEBUG: Không có article_dates")
        return 0
    
    # ✅ OPTIMIZATION: Set comprehension thay vì loop thủ công
    # - Chuyển datetime object thành date object (bỏ time component)
    # - Tự động deduplicate nhiều bài viết cùng ngày
    # - Time complexity: O(n) thay vì O(n log n) nếu dùng sort
    article_date_set = {
        d.date() if isinstance(d, datetime) else d 
        for d in article_dates
    }
    
    # Kiểm tra sau khi convert - có thể tất cả dates đều invalid
    if not article_date_set:
        print("🔥 STREAK DEBUG: Không có ngày hợp lệ")
        return 0
    
    # Debug info: So sánh số bài viết raw vs unique dates
    print(f"🔥 STREAK DEBUG: Số bài viết: {len(article_dates)}")
    print(f"📊 STREAK DEBUG: Unique dates: {len(article_date_set)} từ {len(article_dates)} articles")
    print(f"🔥 STREAK DEBUG: Ngày bài viết: {sorted(article_date_set, reverse=True)[:10]}")
    
    # ============================================================================
    # BƯỚC 2: FLEXIBLE MODE - TÌM ĐIỂM BẮT ĐẦU
    # ============================================================================
    
    current_date = datetime.now().date()
    print(f"🔥 STREAK DEBUG: Ngày hiện tại: {current_date}")
    
    # ✅ FLEXIBLE MODE: Không bắt buộc phải viết hôm nay
    # Nếu hôm nay chưa viết, bắt đầu từ ngày gần nhất có bài viết
    if current_date not in article_date_set:
        try:
            # ✅ OPTIMIZATION: Generator expression thay vì list comprehension
            # - Không tạo list trung gian, tiết kiệm memory
            # - max() với generator chỉ iterate một lần
            current_date = max(d for d in article_date_set if d <= current_date)
            print(f"🔥 STREAK DEBUG: Hôm nay chưa viết, bắt đầu từ: {current_date}")
        except ValueError:
            # Trường hợp tất cả bài viết đều trong tương lai
            print(f"🔥 STREAK DEBUG: Không có bài viết trước hôm nay → streak = 0")
            return 0
    
    # ============================================================================
    # BƯỚC 3: DYNAMIC LIMIT CALCULATION
    # ============================================================================
    
    # ✅ OPTIMIZATION: Tính toán giới hạn thông minh dựa trên dữ liệu
    # Thay vì fixed limit 365, chỉ check đến ngày đầu tiên có bài viết
    min_date = min(article_date_set)
    max_possible_days = (current_date - min_date).days + 1
    max_days = min(365, max_possible_days)  # Safety cap tại 365 ngày
    
    print(f"🔥 STREAK DEBUG: Dynamic limit: {max_days} ngày (từ {min_date} đến {current_date})")
    
    # ============================================================================
    # BƯỚC 4: BACKWARD COUNTING ALGORITHM
    # ============================================================================
    
    # Khởi tạo counters
    streak = 0          # Kết quả streak cuối cùng
    day_counter = 0     # Đếm số ngày đã check (để debug)
    
    # Main loop: Đếm ngược từ current_date về quá khứ
    while day_counter < max_days and current_date >= min_date:
        print(f"🔥 STREAK DEBUG: Kiểm tra ngày {day_counter + 1}: {current_date}")
        
        # ✅ CORE LOGIC: Set lookup O(1) complexity
        if current_date in article_date_set:
            # Có bài viết trong ngày này
            streak += 1
            print(f"🔥 STREAK DEBUG: ✅ Có bài viết ngày {current_date} → streak = {streak}")
            
            # Di chuyển về ngày trước đó để tiếp tục check
            current_date = current_date - timedelta(days=1)
        else:
            # ❌ CRITICAL: Gặp gap đầu tiên → Dừng streak ngay lập tức
            # Đây là điểm khác biệt quan trọng với thuật toán tính tổng số ngày
            print(f"🔥 STREAK DEBUG: ❌ Không có bài viết ngày {current_date} → DỪNG")
            break
        
        # Increment counter cho debugging và safety check
        day_counter += 1
    
    # ============================================================================
    # BƯỚC 5: RETURN RESULT
    # ============================================================================
    
    print(f"🔥 STREAK DEBUG: Kết quả cuối cùng: streak = {streak}")
    return streak

def calculate_max_historical_streak(article_dates):
    """
    ================================================================================
                        TÍNH TOÁN WRITING STREAK TỐI ĐA TRONG LỊCH SỬ
    ================================================================================
    
    MỤC ĐÍCH:
        Tìm chuỗi ngày liên tiếp dài nhất từng có trong toàn bộ lịch sử viết bài,
        không nhất thiết phải kết thúc ở thời điểm hiện tại. Đây là "kỷ lục" streak.
    
    KHÁC BIỆT VỚI CURRENT STREAK:
        - Current streak: Chỉ tính từ gần đây nhất về quá khứ, dừng khi gặp gap
        - Max historical: Quét toàn bộ timeline, tìm đoạn liên tiếp dài nhất
        
    THUẬT TOÁN SLIDING WINDOW:
        1. 📅 CHRONOLOGICAL SORT: Sắp xếp tất cả ngày theo thứ tự thời gian
        2. 🔄 SEQUENTIAL SCAN: Duyệt qua từng cặp ngày liên tiếp  
        3. 📏 CONSECUTIVE CHECK: Kiểm tra khoảng cách đúng 1 ngày
        4. 📈 DYNAMIC TRACKING: Update max ngay khi tìm thấy streak dài hơn
        5. 🔄 RESET ON GAP: Reset current streak khi gặp khoảng trống
    
    PERFORMANCE OPTIMIZATIONS:
        - Time Complexity: O(n log n) do sorting, O(n) cho scanning  
        - Space Complexity: O(d) với d=số ngày unique
        - Single-pass algorithm: Chỉ duyệt dữ liệu một lần sau khi sort
        - In-loop max update: Không cần lưu trữ tất cả streaks
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
                             Có thể chứa nhiều bài viết cùng ngày (sẽ được deduplicate)
        
    Returns:
        int: Streak tối đa trong lịch sử
             - 0 nếu không có bài viết
             - 1 nếu chỉ có 1 ngày hoặc không có ngày nào liên tiếp  
             - 2+ nếu có ít nhất 1 cặp ngày liên tiếp
        
    Ví dụ thực tế:
        Input: [2025-01-01, 2025-01-02, 2025-01-03, 2025-01-10, 2025-01-11]
        Timeline: 01→02→03 [gap] 10→11
        
        Quá trình:
        1. Sort: [01, 02, 03, 10, 11]
        2. 01→02: liên tiếp → current=2, max=2
        3. 02→03: liên tiếp → current=3, max=3  
        4. 03→10: gap 7 ngày → reset current=1
        5. 10→11: liên tiếp → current=2, max=3
        
        Kết quả: max_streak = 3 (từ ngày 01→03)
    """
    # ============================================================================
    # BƯỚC 1: VALIDATION & INPUT PROCESSING
    # ============================================================================
    
    # Kiểm tra input rỗng
    if not article_dates:
        print("🏆 MAX STREAK DEBUG: Không có article_dates")
        return 0
    
    # ✅ OPTIMIZATION: Combine convert + sort + deduplicate trong một operation
    # - Set comprehension để deduplicate O(n)
    # - Sorted để sắp xếp chronological O(n log n)  
    # - Chuyển datetime → date để normalize time component
    unique_dates = sorted({
        d.date() if isinstance(d, datetime) else d 
        for d in article_dates
    })
    
    # Kiểm tra sau khi processing
    if not unique_dates:
        print("🏆 MAX STREAK DEBUG: Không có ngày hợp lệ")
        return 0
    
    # ✅ EDGE CASE: Chỉ có 1 ngày duy nhất
    # Không thể tạo streak với 1 ngày, nhưng streak của 1 ngày = 1
    if len(unique_dates) == 1:
        print(f"🏆 MAX STREAK DEBUG: Chỉ có 1 ngày ({unique_dates[0]}) → max_streak = 1")
        return 1
    
    # Debug info: Hiển thị timeline overview
    print(f"🏆 MAX STREAK DEBUG: Tổng {len(unique_dates)} ngày có bài viết")
    print(f"🏆 MAX STREAK DEBUG: Timeline: {unique_dates[0]} → {unique_dates[-1]}")
    print(f"🏆 MAX STREAK DEBUG: Chi tiết: {unique_dates[:10]}{'...' if len(unique_dates) > 10 else ''}")
    
    # ============================================================================
    # BƯỚC 2: SLIDING WINDOW ALGORITHM
    # ============================================================================
    
    # ✅ OPTIMIZATION: Initialize với 1 thay vì 0
    # Vì ngày đầu tiên luôn là streak có độ dài 1
    max_streak = current_streak = 1
    
    # Duyệt qua tất cả cặp ngày liên tiếp trong timeline
    for i in range(1, len(unique_dates)):
        prev_date = unique_dates[i-1]   # Ngày trước đó
        curr_date = unique_dates[i]     # Ngày hiện tại
        
        # ✅ CORE LOGIC: Kiểm tra consecutive dates
        # Chỉ những ngày cách nhau đúng 1 ngày mới tính là liên tiếp
        day_gap = (curr_date - prev_date).days
        
        if day_gap == 1:
            # ✅ CONSECUTIVE: Ngày liên tiếp
            current_streak += 1
            
            # ✅ OPTIMIZATION: Update max_streak ngay trong loop
            # Thay vì đợi đến cuối loop, update ngay khi có streak mới
            max_streak = max(max_streak, current_streak)
            
            print(f"🏆 MAX STREAK DEBUG: {prev_date}→{curr_date} liên tiếp → current={current_streak}, max={max_streak}")
            
        else:
            # ❌ GAP DETECTED: Có khoảng trống
            print(f"🏆 MAX STREAK DEBUG: Gap {day_gap} ngày từ {prev_date}→{curr_date} → reset streak")
            
            # Reset current streak về 1 (ngày hiện tại bắt đầu streak mới)
            current_streak = 1
            # Lưu ý: Không cần update max_streak ở đây vì đã update trong loop trên
    
    # ============================================================================
    # BƯỚC 3: RETURN RESULT
    # ============================================================================
    
    print(f"🏆 MAX STREAK DEBUG: Kết quả cuối cùng: max_streak = {max_streak}")
    return max_streak

def calculate_total_days(article_dates):
    """
    Tính toán tổng số ngày học tập từ ngày đầu tiên đến hiện tại
    
    Thuật toán:
    1. Tìm ngày đầu tiên có bài viết (ngày xa nhất)
    2. Tính số ngày từ ngày đó đến hiện tại
    3. Trả về tổng số ngày
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
        
    Returns:
        int: Tổng số ngày từ ngày đầu tiên đến hiện tại
        
    Ví dụ:
        # Bài viết đầu tiên: 1/1/2024, hôm nay: 15/1/2024
        dates = [datetime(2024,1,1), datetime(2024,1,15)]
        calculate_total_days(dates) -> 14 ngày
    """
    if not article_dates:
        return 0
    
    # Tìm ngày đầu tiên (xa nhất)
    first_date = min(article_dates).date()
    current_date = datetime.now().date()
    
    # Tính số ngày
    total_days = (current_date - first_date).days + 1  # +1 để bao gồm cả ngày đầu
    
    return max(1, total_days)  # Ít nhất là 1 ngày

def scan_domain_folder(domain_path):
    """Scan một domain folder và trả về thông tin"""
    if not os.path.exists(domain_path):
        return None
    
    domain_name = os.path.basename(domain_path)
    print(f"📁 SCAN DEBUG: Đang scan domain: {domain_name}")
    articles_count = 0
    total_words = 0
    article_dates = []
    last_activity = None
    
    # Duyệt qua tất cả file trong domain
    for root, dirs, files in os.walk(domain_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()
            
            if file_ext in SUPPORTED_EXTENSIONS:
                try:
                    # Lấy thông tin file
                    stat_info = os.stat(file_path)
                    creation_time = datetime.fromtimestamp(stat_info.st_ctime)
                    
                    # Đếm từ
                    word_count = estimate_word_count(file_path, file_ext)
                    
                    articles_count += 1
                    total_words += word_count
                    article_dates.append(creation_time)
                    
                    print(f"📄 FILE DEBUG: {file} - Ngày tạo: {creation_time.date()} - Từ: {word_count}")
                    
                    if last_activity is None or creation_time > last_activity:
                        last_activity = creation_time
                        
                except Exception as e:
                    print(f"Lỗi khi đọc file {file}: {e}")
    
    # Tính toán metrics
    xp = calculate_xp_from_articles(articles_count, total_words)
    level = calculate_level_from_xp(xp)
    streak_days = calculate_streak_days(article_dates)
    max_streak_days = calculate_max_historical_streak(article_dates)
    total_days = calculate_total_days(article_dates)
    
    return {
        'name': domain_name,
        'xp': xp,
        'level': level,
        'color': get_domain_color(domain_name),
        'taskCount': articles_count,  # Số bài viết
        'streakDays': streak_days,
        'maxStreakDays': max_streak_days,
        'totalDays': total_days,
        'lastTaskDate': last_activity.isoformat() if last_activity else datetime.now().isoformat(),
        'totalWords': total_words,
        'lastActivity': last_activity.isoformat() if last_activity else None
    }

def scan_all_domains():
    """Scan tất cả domain folders"""
    domains = {}
    
    if not os.path.exists(DATA_SCIENCE_PATH):
        return domains
    
    # Tìm tất cả domain folders
    for item in os.listdir(DATA_SCIENCE_PATH):
        item_path = os.path.join(DATA_SCIENCE_PATH, item)
        
        if os.path.isdir(item_path) and item.startswith('Domain'):
            domain_data = scan_domain_folder(item_path)
            if domain_data:
                domains[domain_data['name']] = {
                    'xp': domain_data['xp'],
                    'level': domain_data['level'],
                    'color': domain_data['color'],
                    'taskCount': domain_data['taskCount'],
                    'streakDays': domain_data['streakDays'],
                    'maxStreakDays': domain_data['maxStreakDays'],
                    'totalDays': domain_data['totalDays'],
                    'lastTaskDate': domain_data['lastTaskDate']
                }
    
    return domains

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Domain Progress Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "domains": "/api/domains",
            "refresh": "/api/domains/refresh", 
            "stats": "/api/domains/stats"
        }
    }

@app.get("/api/domains", response_model=DomainsResponse)
async def get_domains():
    """API endpoint để lấy danh sách domains với XP/Level"""
    try:
        domains = scan_all_domains()
        
        return DomainsResponse(
            success=True,
            domains=domains,
            count=len(domains),
            last_scan=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/domains/refresh", response_model=DomainsResponse)
async def refresh_domains():
    """API endpoint để refresh domain data"""
    try:
        domains = scan_all_domains()
        
        return DomainsResponse(
            success=True,
            domains=domains,
            count=len(domains),
            last_scan=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/domains/stats", response_model=StatsResponse)
async def get_domain_stats():
    """API endpoint để lấy thống kê tổng quan"""
    try:
        domains = scan_all_domains()
        
        total_articles = sum(domain['taskCount'] for domain in domains.values())
        total_xp = sum(domain['xp'] for domain in domains.values())
        total_levels = sum(domain['level'] for domain in domains.values())
        
        # Domain có level cao nhất
        highest_level_domain = max(domains.items(), key=lambda x: x[1]['level']) if domains else None
        
        # Domain có nhiều bài viết nhất
        most_articles_domain = max(domains.items(), key=lambda x: x[1]['taskCount']) if domains else None
        
        return StatsResponse(
            success=True,
            stats={
                'total_domains': len(domains),
                'total_articles': total_articles,
                'total_xp': total_xp,
                'total_levels': total_levels,
                'average_level': total_levels / len(domains) if domains else 0,
                'highest_level_domain': highest_level_domain,
                'most_articles_domain': most_articles_domain
            },
            last_scan=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    
    print("🚀 Starting Domain Progress Tracker Server (FastAPI)...")
    print(f"📁 Scanning path: {DATA_SCIENCE_PATH}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📖 API endpoints:")
    print("  - GET /api/domains - Get all domains with XP/Level")
    print("  - POST /api/domains/refresh - Refresh domain data")
    print("  - GET /api/domains/stats - Get domain statistics")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
