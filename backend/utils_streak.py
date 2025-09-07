#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                            UTILS STREAK - STREAK CALCULATION UTILITIES
================================================================================

MÔ TẢ:
    Module chứa các hàm tính toán streak (chuỗi ngày liên tiếp) cho hệ thống 
    theo dõi tiến độ học tập. Được tách riêng từ main.py để dễ bảo trì và tái sử dụng.

CHỨC NĂNG CHÍNH:
    1. calculate_streak_days(): Tính streak hiện tại (từ gần nhất về quá khứ)
    2. calculate_max_historical_streak(): Tìm streak dài nhất trong lịch sử
    3. calculate_total_days(): Tính tổng số ngày từ ngày đầu tiên đến hiện tại

TÁC GIẢ: Domain Progress Tracker Team
NGÀY TẠO: 2024
PHIÊN BẢN: 1.0.0
================================================================================
"""

from datetime import datetime, timedelta
from typing import List, Union


def calculate_streak_days(article_dates: List[Union[datetime, str]]) -> int:
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


def calculate_max_historical_streak(article_dates: List[Union[datetime, str]]) -> int:
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


def calculate_total_days(article_dates: List[Union[datetime, str]]) -> int:
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
