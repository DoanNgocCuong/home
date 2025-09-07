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
from datetime import datetime
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
    Tính toán số ngày liên tiếp học tập (streak days) dựa trên ngày tạo bài viết
    
    Thuật toán:
    1. Sắp xếp danh sách ngày theo thứ tự giảm dần (mới nhất trước)
    2. Bắt đầu từ ngày hiện tại, kiểm tra xem có bài viết không
    3. Nếu có, tăng streak và chuyển sang ngày trước đó
    4. Tiếp tục cho đến khi không còn bài viết liên tiếp
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
        
    Returns:
        int: Số ngày liên tiếp học tập (streak days)
        
    Ví dụ:
        # Có bài viết hôm nay, hôm qua, và 3 ngày trước
        dates = [datetime(2024,1,15), datetime(2024,1,14), datetime(2024,1,12)]
        calculate_streak_days(dates) -> 2 (hôm nay + hôm qua)
    """
    if not article_dates:
        return 0
    
    # Sắp xếp ngày giảm dần
    sorted_dates = sorted(article_dates, reverse=True)
    
    streak = 0
    current_date = datetime.now().date()
    
    for article_date in sorted_dates:
        if article_date.date() == current_date:
            streak += 1
            current_date = current_date.replace(day=current_date.day - 1)
        elif article_date.date() < current_date:
            break
    
    return streak

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
                    
                    if last_activity is None or creation_time > last_activity:
                        last_activity = creation_time
                        
                except Exception as e:
                    print(f"Lỗi khi đọc file {file}: {e}")
    
    # Tính toán metrics
    xp = calculate_xp_from_articles(articles_count, total_words)
    level = calculate_level_from_xp(xp)
    streak_days = calculate_streak_days(article_dates)
    total_days = calculate_total_days(article_dates)
    
    return {
        'name': domain_name,
        'xp': xp,
        'level': level,
        'color': get_domain_color(domain_name),
        'taskCount': articles_count,  # Số bài viết
        'streakDays': streak_days,
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
