#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    UTILS XP LEVEL - XP AND LEVEL CALCULATION MODULE
================================================================================

MÔ TẢ:
    Module chuyên xử lý tính toán điểm kinh nghiệm (XP) và cấp độ (Level)
    cho hệ thống theo dõi tiến độ học tập. Được tách riêng từ utils_folder_level.py
    để tuân thủ Single Responsibility Principle.

CHỨC NĂNG CHÍNH:
    1. calculate_xp_from_articles(): Tính XP từ số bài viết và số từ
    2. calculate_level_from_xp(): Chuyển đổi XP thành Level
    3. get_xp_for_next_level(): Tính XP cần thiết cho level tiếp theo
    4. get_level_progress(): Tính phần trăm tiến độ của level hiện tại
    5. get_level_info(): Lấy thông tin chi tiết về level

TÁC GIẢ: Domain Progress Tracker Team
NGÀY TẠO: 2025-09-07
PHIÊN BẢN: 2.0.0
================================================================================
"""

from typing import Dict, Tuple


# ================================================================================
#                           CONFIGURATION CONSTANTS
# ================================================================================

# XP Configuration
BASE_XP_PER_ARTICLE = 100    # Điểm XP cơ bản cho mỗi bài viết
WORDS_PER_XP = 10            # Số từ để đạt 1 XP bonus
MIN_WORD_BONUS = 0           # XP bonus tối thiểu từ word count
WORD_BONUS_NO_CAP = "NO CAP"  # Chế độ không giới hạn bonus theo từ
MAX_WORD_BONUS_PER_ARTICLE = WORD_BONUS_NO_CAP  # Dùng "NO CAP" để không giới hạn

# Level Configuration  
BASE_LEVEL_XP = 1000         # XP cần thiết cho Level 1
LEVEL_XP_MULTIPLIER = 1.5    # Hệ số nhân XP cho mỗi level
MAX_LEVEL = 100              # Level tối đa trong hệ thống


# ================================================================================
#                           CORE CALCULATION FUNCTIONS
# ================================================================================

def calculate_xp_from_articles(articles_count: int, total_words: int) -> int:
    """
    Tính toán điểm kinh nghiệm (XP) dựa trên số lượng bài viết và tổng số từ.
    
    CÔNG THỨC TÍNH XP:
        - Base XP: BASE_XP_PER_ARTICLE điểm cho mỗi bài viết
        - Word Bonus: 1 điểm cho mỗi WORDS_PER_XP từ
        - Tổng XP = Base XP + Word Bonus
    
    GIỚI HẠN:
        - Word bonus tối đa: MAX_WORD_BONUS_PER_ARTICLE × articles_count
        - "NO CAP" mode: đặt MAX_WORD_BONUS_PER_ARTICLE = "NO CAP" để bỏ giới hạn.
          Lý do: tự mô tả (self-documenting), giữ nguyên công thức cũ (words//10),
          và phù hợp vibe gamification. 
        - Đảm bảo không có negative XP
        - MAX_WORD_BONUS_PER_ARTICLE: giới hạn XP bonus từ từ vựng
          * "NO CAP" hoặc 0 = không giới hạn (tính đủ words//10)
          * > 0 = đặt trần XP/bài (vd: 200 = tối đa 200 XP/bài từ từ vựng)
    
    Args:
        articles_count (int): Số lượng bài viết/tài liệu
        total_words (int): Tổng số từ trong tất cả bài viết
        
    Returns:
        int: Tổng điểm XP được tính toán
        
    Examples:
        >>> calculate_xp_from_articles(5, 5000)
        1000  # 5×100 + 5000÷10 = 500 + 500
        
        >>> calculate_xp_from_articles(10, 1000)  
        1100  # 10×100 + 1000÷10 = 1000 + 100
    """
    # Validate inputs
    if articles_count < 0 or total_words < 0:
        return 0
    
    # Calculate base XP from article count
    base_xp = articles_count * BASE_XP_PER_ARTICLE
    
    # Calculate bonus XP from word count
    word_bonus = total_words // WORDS_PER_XP
    
    # Apply maximum word bonus limit if configured (skip when NO CAP)
    if MAX_WORD_BONUS_PER_ARTICLE != WORD_BONUS_NO_CAP and articles_count > 0:
        max_allowed_bonus = int(MAX_WORD_BONUS_PER_ARTICLE) * articles_count
        word_bonus = min(word_bonus, max_allowed_bonus)
    
    # Apply minimum word bonus
    word_bonus = max(word_bonus, MIN_WORD_BONUS)
    
    return base_xp + word_bonus


def calculate_level_from_xp(xp: int) -> int:
    """
    Tính toán level dựa trên tổng điểm XP (hệ thống tương tự game RPG).
    
    CÔNG THỨC LEVEL PROGRESSION:
        - Level 0: 0 XP (starting point)
        - Level 1: Cần BASE_LEVEL_XP (1000 XP)
        - Level 2: Cần BASE_LEVEL_XP × LEVEL_XP_MULTIPLIER (1500 XP)
        - Level 3: Cần BASE_LEVEL_XP × LEVEL_XP_MULTIPLIER² (2250 XP)
        - Level n: Cần BASE_LEVEL_XP × LEVEL_XP_MULTIPLIER^(n-1) XP
    
    THUẬT TOÁN:
        Dùng vòng lặp để trừ dần XP cần thiết cho mỗi level
        cho đến khi XP không đủ cho level tiếp theo.
    
    Args:
        xp (int): Tổng điểm XP hiện tại
        
    Returns:
        int: Level tương ứng với số XP (0 đến MAX_LEVEL)
        
    Examples:
        >>> calculate_level_from_xp(0)
        0
        >>> calculate_level_from_xp(1000)
        1
        >>> calculate_level_from_xp(2500)
        2  # 1000 + 1500 = 2500
    """
    # Validate input
    if xp < 0:
        return 0
    
    level = 0
    current_xp = xp
    required_xp = BASE_LEVEL_XP
    
    # Calculate level by subtracting required XP for each level
    while current_xp >= required_xp and level < MAX_LEVEL:
        level += 1
        current_xp -= required_xp
        # Calculate XP required for next level
        required_xp = int(BASE_LEVEL_XP * (LEVEL_XP_MULTIPLIER ** level))
    
    return level


def get_xp_for_next_level(current_xp: int) -> Tuple[int, int, int]:
    """
    Tính toán XP cần thiết để đạt level tiếp theo.
    
    Args:
        current_xp (int): Tổng XP hiện tại
        
    Returns:
        Tuple[int, int, int]: (XP đã có trong level hiện tại, 
                               XP cần cho level tiếp theo,
                               XP còn thiếu)
        
    Examples:
        >>> get_xp_for_next_level(1200)
        (200, 1500, 1300)  # Level 1, đã có 200/1500 XP cho level 2
    """
    if current_xp < 0:
        return 0, BASE_LEVEL_XP, BASE_LEVEL_XP
    
    level = calculate_level_from_xp(current_xp)
    
    # Calculate total XP needed to reach current level
    total_for_current = 0
    for i in range(level):
        total_for_current += int(BASE_LEVEL_XP * (LEVEL_XP_MULTIPLIER ** i))
    
    # XP in current level
    xp_in_current_level = current_xp - total_for_current
    
    # XP needed for next level
    if level >= MAX_LEVEL:
        return xp_in_current_level, 0, 0
    
    xp_for_next = int(BASE_LEVEL_XP * (LEVEL_XP_MULTIPLIER ** level))
    xp_remaining = xp_for_next - xp_in_current_level
    
    return xp_in_current_level, xp_for_next, xp_remaining


def get_level_progress(current_xp: int) -> float:
    """
    Tính phần trăm tiến độ hoàn thành của level hiện tại.
    
    Args:
        current_xp (int): Tổng XP hiện tại
        
    Returns:
        float: Phần trăm hoàn thành (0.0 - 100.0)
        
    Examples:
        >>> get_level_progress(1500)
        33.33  # Level 1, có 500/1500 XP cho level 2 = 33.33%
    """
    xp_in_level, xp_for_next, _ = get_xp_for_next_level(current_xp)
    
    if xp_for_next == 0:  # Max level reached
        return 100.0
    
    progress = (xp_in_level / xp_for_next) * 100
    return round(progress, 2)


def get_level_info(current_xp: int) -> Dict[str, any]:
    """
    Lấy thông tin chi tiết về level hiện tại và tiến độ.
    
    Args:
        current_xp (int): Tổng XP hiện tại
        
    Returns:
        Dict: Dictionary chứa thông tin chi tiết về level:
            - level: Level hiện tại
            - total_xp: Tổng XP
            - xp_in_level: XP trong level hiện tại
            - xp_for_next: XP cần cho level tiếp theo
            - xp_remaining: XP còn thiếu
            - progress: Phần trăm hoàn thành
            - next_level: Level tiếp theo
            
    Examples:
        >>> get_level_info(3000)
        {
            'level': 2,
            'total_xp': 3000,
            'xp_in_level': 500,
            'xp_for_next': 2250,
            'xp_remaining': 1750,
            'progress': 22.22,
            'next_level': 3
        }
    """
    level = calculate_level_from_xp(current_xp)
    xp_in_level, xp_for_next, xp_remaining = get_xp_for_next_level(current_xp)
    progress = get_level_progress(current_xp)
    
    return {
        'level': level,
        'total_xp': current_xp,
        'xp_in_level': xp_in_level,
        'xp_for_next': xp_for_next,
        'xp_remaining': xp_remaining,
        'progress': progress,
        'next_level': level + 1 if level < MAX_LEVEL else MAX_LEVEL,
        'is_max_level': level >= MAX_LEVEL
    }


def get_total_xp_for_level(target_level: int) -> int:
    """
    Tính tổng XP cần thiết để đạt được một level cụ thể.
    
    Args:
        target_level (int): Level mục tiêu
        
    Returns:
        int: Tổng XP cần thiết
        
    Examples:
        >>> get_total_xp_for_level(3)
        3750  # 1000 + 1500 + 2250
    """
    if target_level <= 0:
        return 0
    
    if target_level > MAX_LEVEL:
        target_level = MAX_LEVEL
    
    total_xp = 0
    for i in range(target_level):
        total_xp += int(BASE_LEVEL_XP * (LEVEL_XP_MULTIPLIER ** i))
    
    return total_xp


# ================================================================================
#                           UTILITY FUNCTIONS
# ================================================================================

def format_xp_display(xp: int) -> str:
    """
    Format XP để hiển thị đẹp hơn (với dấu phân cách hàng nghìn).
    
    Args:
        xp (int): Số XP cần format
        
    Returns:
        str: XP đã được format
        
    Examples:
        >>> format_xp_display(1500)
        '1,500 XP'
        >>> format_xp_display(1000000)
        '1,000,000 XP'
    """
    return f"{xp:,} XP"


def get_level_title(level: int) -> str:
    """
    Lấy title/rank tương ứng với level (gamification).
    
    Args:
        level (int): Level hiện tại
        
    Returns:
        str: Title tương ứng
    """
    titles = {
        0: "🌱 Beginner",
        1: "📚 Novice",
        2: "💡 Apprentice", 
        3: "⚡ Adept",
        5: "🔥 Expert",
        8: "⭐ Master",
        12: "💎 Grandmaster",
        16: "👑 Champion",
        20: "🏆 Legend",
        25: "🌟 Mythic",
        30: "🔮 Transcendent",
        40: "🌌 Celestial",
        50: "♾️ Infinite"
    }
    
    # Find appropriate title based on level
    for min_level in sorted(titles.keys(), reverse=True):
        if level >= min_level:
            return titles[min_level]
    
    return titles[0]


# ================================================================================
#                           MODULE TESTING
# ================================================================================

if __name__ == "__main__":
    """Test các functions chính của module."""
    
    print("=" * 80)
    print("TESTING UTILS_XP_LEVEL MODULE")
    print("=" * 80)
    
    # Test cases
    test_cases = [
        (0, 0),      # No articles
        (1, 100),    # 1 article, 100 words
        (5, 2500),   # 5 articles, 2500 words
        (10, 10000), # 10 articles, 10000 words
        (50, 50000), # 50 articles, 50000 words
    ]
    
    for articles, words in test_cases:
        xp = calculate_xp_from_articles(articles, words)
        level = calculate_level_from_xp(xp)
        progress = get_level_progress(xp)
        title = get_level_title(level)
        
        print(f"\n📊 Test Case: {articles} articles, {words:,} words")
        print(f"   XP: {format_xp_display(xp)}")
        print(f"   Level: {level} - {title}")
        print(f"   Progress: {progress}%")
        
        info = get_level_info(xp)
        if not info['is_max_level']:
            print(f"   Next Level: Need {info['xp_remaining']:,} more XP")
    
    print("\n" + "=" * 80)
    print("✅ Module testing completed!")