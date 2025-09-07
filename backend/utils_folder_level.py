#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    UTILS FOLDER - FOLDER SCANNING AND PROCESSING MODULE
================================================================================

MÔ TẢ:
    Module chuyên xử lý scan folder, đọc file và tổng hợp dữ liệu cho hệ thống
    theo dõi tiến độ học tập. Được refactor từ utils_folder_level.py, loại bỏ
    duplicate code và tuân thủ Single Responsibility Principle.

CHỨC NĂNG CHÍNH:
    1. Scan folder đơn lẻ và tính toán metrics
    2. Scan folder với subfolders (recursive)
    3. Xây dựng tree structure cho hiển thị
    4. Ước tính word count từ các loại file
    5. Domain color mapping cho UI

DEPENDENCIES:
    - utils_xp_level: Cho tính toán XP và Level
    - utils_streak: Cho tính toán streak days

TÁC GIẢ: Domain Progress Tracker Team
NGÀY TẠO: 2025-09-07
PHIÊN BẢN: 2.0.0
================================================================================
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Set

# Import từ các module đã refactor
from utils_xp_level import (
    calculate_xp_from_articles,
    calculate_level_from_xp,
    get_level_info
)

from utils_streak import (
    calculate_streak_days,
    calculate_max_historical_streak,
    calculate_total_days
)


# ================================================================================
#                           CONFIGURATION CONSTANTS
# ================================================================================

# Domain color mapping cho UI
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
    '0. NHẤT HƯỚNG': '#FFD700',  # Gold - Special folder
    'DATA SCIENCE AND AI': '#00CED1',  # Dark Turquoise
    'default': '#6B7280'    # Gray - Default color
}

# File processing configuration
DEFAULT_WORDS_PER_FILE = 500  # Giá trị mặc định khi không đọc được file
MIN_WORDS_PER_FILE = 100      # Số từ tối thiểu estimate
BYTES_PER_WORD_ESTIMATE = 5   # Ước tính 5 bytes = 1 từ


# ================================================================================
#                           UI/DISPLAY FUNCTIONS
# ================================================================================

def get_domain_color(domain_name: str) -> str:
    """
    Lấy màu sắc tương ứng cho domain dựa trên tên domain.
    
    Args:
        domain_name (str): Tên của domain
        
    Returns:
        str: Mã màu hex tương ứng với domain
        
    Examples:
        >>> get_domain_color('Domain 1: Math')
        '#4F46E5'
        >>> get_domain_color('Unknown Domain')
        '#6B7280'
    """
    # Check exact match first
    if domain_name in DOMAIN_COLORS:
        return DOMAIN_COLORS[domain_name]
    
    # Check partial match
    for key, color in DOMAIN_COLORS.items():
        if key in domain_name or domain_name.startswith(key.split(':')[0]):
            return color
    
    return DOMAIN_COLORS['default']


# ================================================================================
#                           FILE PROCESSING FUNCTIONS
# ================================================================================

def estimate_word_count(file_path: str, file_ext: str) -> int:
    """
    Ước tính số từ trong file dựa trên loại file và nội dung.
    
    SUPPORTED FORMATS:
        - Text files (.txt, .md): Đếm từ trực tiếp
        - HTML files (.html): Strip tags rồi đếm từ
        - Other formats: Ước tính dựa trên file size
    
    Args:
        file_path (str): Đường dẫn đến file cần đếm từ
        file_ext (str): Phần mở rộng của file (ví dụ: '.md', '.txt')
        
    Returns:
        int: Số từ ước tính trong file
        
    Examples:
        >>> estimate_word_count('/path/to/file.md', '.md')
        1250
    """
    try:
        # Text-based files: Count words directly
        if file_ext in ['.txt', '.md', '.markdown']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Split by whitespace and filter empty strings
                words = len([w for w in content.split() if w])
                return max(words, MIN_WORDS_PER_FILE)
                
        # HTML files: Strip tags first
        elif file_ext in ['.html', '.htm']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Remove HTML tags
                clean_text = re.sub(r'<[^>]+>', ' ', content)
                # Remove extra whitespace
                clean_text = re.sub(r'\s+', ' ', clean_text)
                words = len([w for w in clean_text.split() if w])
                return max(words, MIN_WORDS_PER_FILE)
                
        # Document files: Estimate based on file size
        elif file_ext in ['.doc', '.docx', '.rtf', '.odt']:
            file_size = os.path.getsize(file_path)
            # Rough estimate: 1 word ≈ 5 bytes (after compression)
            estimated_words = file_size // BYTES_PER_WORD_ESTIMATE
            return max(estimated_words, MIN_WORDS_PER_FILE)
            
        else:
            # Default: Estimate based on file size
            file_size = os.path.getsize(file_path)
            estimated_words = file_size // (BYTES_PER_WORD_ESTIMATE * 2)  # More conservative
            return max(estimated_words, MIN_WORDS_PER_FILE)
            
    except Exception as e:
        print(f"⚠️ Error reading file {file_path}: {e}")
        return DEFAULT_WORDS_PER_FILE


# ================================================================================
#                           FOLDER SCANNING FUNCTIONS
# ================================================================================

def scan_single_folder(folder_path: str, supported_extensions: Set[str]) -> Optional[Dict[str, Any]]:
    """
    Scan một folder đơn lẻ và trả về thông tin metrics.
    
    PROCESS:
        1. Duyệt tất cả files trong folder (recursive)
        2. Lọc files theo supported extensions
        3. Thu thập creation dates và word counts
        4. Tính toán XP, Level, Streak metrics
    
    Args:
        folder_path (str): Đường dẫn đến folder cần scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        
    Returns:
        Dict[str, Any]: Thông tin folder bao gồm XP, level, streak, etc.
                       hoặc None nếu folder không tồn tại
    """
    if not os.path.exists(folder_path):
        return None
    
    folder_name = os.path.basename(folder_path)
    print(f"📁 Scanning folder: {folder_name}")
    
    # Initialize counters
    articles_count = 0
    total_words = 0
    article_dates = []
    last_activity = None
    
    # Scan all files in folder (recursive)
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                if file_ext in supported_extensions:
                    try:
                        # Get file creation time
                        stat_info = os.stat(file_path)
                        creation_time = datetime.fromtimestamp(stat_info.st_ctime)
                        
                        # Count words
                        word_count = estimate_word_count(file_path, file_ext)
                        
                        # Update counters
                        articles_count += 1
                        total_words += word_count
                        article_dates.append(creation_time)
                        
                        # Track last activity
                        if last_activity is None or creation_time > last_activity:
                            last_activity = creation_time
                            
                    except Exception as e:
                        print(f"  ⚠️ Error processing {file}: {e}")
                        
    except Exception as e:
        print(f"❌ Error scanning folder {folder_name}: {e}")
        return None
    
    # Calculate metrics using imported functions
    xp = calculate_xp_from_articles(articles_count, total_words)
    level = calculate_level_from_xp(xp)
    level_info = get_level_info(xp)
    
    # Calculate streak metrics
    streak_days = calculate_streak_days(article_dates) if article_dates else 0
    max_streak_days = calculate_max_historical_streak(article_dates) if article_dates else 0
    total_days = calculate_total_days(article_dates) if article_dates else 0
    
    return {
        'name': folder_name,
        'path': folder_path,
        'xp': xp,
        'level': level,
        'levelProgress': level_info['progress'],
        'xpForNextLevel': level_info['xp_for_next'],
        'xpRemaining': level_info['xp_remaining'],
        'color': get_domain_color(folder_name),
        'taskCount': articles_count,
        'streakDays': streak_days,
        'maxStreakDays': max_streak_days,
        'totalDays': total_days,
        'lastTaskDate': last_activity.isoformat() if last_activity else datetime.now().isoformat(),
        'totalWords': total_words,
        'lastActivity': last_activity.isoformat() if last_activity else None
    }


def scan_folder_with_subfolders(folder_path: str, supported_extensions: Set[str]) -> Optional[Dict[str, Any]]:
    """
    Scan folder và các subfolder level 1 của nó.
    
    Args:
        folder_path (str): Đường dẫn đến folder chính cần scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        
    Returns:
        Dict[str, Any]: Thông tin folder chính + subfolders
    """
    if not os.path.exists(folder_path):
        return None
    
    folder_name = os.path.basename(folder_path)
    print(f"📁 Detailed scan: {folder_name} with subfolders...")
    
    # Scan main folder
    folder_data = scan_single_folder(folder_path, supported_extensions)
    if not folder_data:
        return None
    
    # Scan subfolders (level 1 only)
    subfolders = {}
    
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Only scan directories, skip files and hidden folders
            if os.path.isdir(item_path) and not item.startswith('.'):
                subfolder_data = scan_single_folder(item_path, supported_extensions)
                
                if subfolder_data:
                    # Store minimal info for subfolders
                    subfolders[item] = {
                        'name': item,
                        'xp': subfolder_data['xp'],
                        'level': subfolder_data['level'],
                        'levelProgress': subfolder_data['levelProgress'],
                        'color': subfolder_data['color'],
                        'taskCount': subfolder_data['taskCount'],
                        'streakDays': subfolder_data['streakDays'],
                        'maxStreakDays': subfolder_data['maxStreakDays'],
                        'totalDays': subfolder_data['totalDays'],
                        'lastTaskDate': subfolder_data['lastTaskDate']
                    }
                    print(f"  📂 Subfolder: {item} - Level {subfolder_data['level']} ({subfolder_data['taskCount']} files)")
                    
    except Exception as e:
        print(f"⚠️ Error scanning subfolders of {folder_name}: {e}")
    
    # Add subfolder information to main folder data
    folder_data['subfolders'] = subfolders
    folder_data['subfolderCount'] = len(subfolders)
    
    return folder_data


def scan_folder_tree_recursive(
    folder_path: str, 
    supported_extensions: Set[str], 
    max_depth: int = 3, 
    current_depth: int = 0
) -> Optional[Dict[str, Any]]:
    """
    Scan folder theo kiểu cây đệ quy để hiển thị tất cả các cấp.
    
    ALGORITHM:
        1. Scan files trong folder hiện tại (không recursive)
        2. Tính metrics cho folder hiện tại
        3. Recursive scan các subfolders
        4. Aggregate metrics từ children
        5. Build tree structure
    
    Args:
        folder_path (str): Đường dẫn đến folder cần scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        max_depth (int): Độ sâu tối đa để scan (default: 3)
        current_depth (int): Độ sâu hiện tại trong recursion
        
    Returns:
        Dict[str, Any]: Tree structure với metrics ở mọi level
    """
    # Check depth limit and existence
    if not os.path.exists(folder_path) or current_depth > max_depth:
        return None
    
    folder_name = os.path.basename(folder_path)
    indent = '  ' * current_depth
    print(f"{indent}📁 Tree scan: {folder_name} (depth {current_depth})")
    
    # Initialize counters for current folder only
    articles_count = 0
    total_words = 0
    article_dates = []
    last_activity = None
    
    # Scan ONLY files in current folder (not recursive)
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            if os.path.isfile(file_path):
                file_ext = Path(file).suffix.lower()
                
                if file_ext in supported_extensions:
                    try:
                        # Get file stats
                        stat_info = os.stat(file_path)
                        creation_time = datetime.fromtimestamp(stat_info.st_ctime)
                        
                        # Count words
                        word_count = estimate_word_count(file_path, file_ext)
                        
                        # Update counters
                        articles_count += 1
                        total_words += word_count
                        article_dates.append(creation_time)
                        
                        # Track last activity
                        if last_activity is None or creation_time > last_activity:
                            last_activity = creation_time
                            
                    except Exception as e:
                        print(f"{indent}  ⚠️ Error reading {file}: {e}")
                        
    except Exception as e:
        print(f"{indent}❌ Error scanning folder {folder_name}: {e}")
    
    # Calculate metrics for current folder
    xp = calculate_xp_from_articles(articles_count, total_words)
    level = calculate_level_from_xp(xp)
    
    # Collect all dates for aggregated streak calculation
    aggregated_dates = set()
    if article_dates:
        aggregated_dates.update(
            d.date() if isinstance(d, datetime) else d
            for d in article_dates
        )
    
    # Scan subfolders recursively
    children = {}
    child_total_xp = 0
    child_total_articles = 0
    child_max_level = 0
    
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Skip files, hidden folders, and system folders
            if not os.path.isdir(item_path) or item.startswith('.') or item.startswith('__'):
                continue
            
            # Recursive scan
            child_data = scan_folder_tree_recursive(
                item_path,
                supported_extensions,
                max_depth,
                current_depth + 1
            )
            
            if child_data:
                children[item] = child_data
                
                # Aggregate metrics from children
                child_total_xp += child_data.get('totalXpWithChildren', child_data['xp'])
                child_total_articles += child_data.get('totalArticlesWithChildren', child_data['taskCount'])
                child_max_level = max(child_max_level, child_data.get('maxLevelInTree', child_data['level']))
                
                # Aggregate dates for streak calculation
                child_dates = child_data.get('_dates_set', set())
                if child_dates:
                    aggregated_dates.update(child_dates)
                
                print(f"{indent}  └── {item}: Level {child_data['level']} ({child_data['taskCount']} files)")
                
    except Exception as e:
        print(f"{indent}⚠️ Error scanning subfolders of {folder_name}: {e}")
    
    # Calculate aggregated streak metrics
    if aggregated_dates:
        aggregated_dates_list = list(aggregated_dates)
        streak_days = calculate_streak_days(aggregated_dates_list)
        max_streak_days = calculate_max_historical_streak(aggregated_dates_list)
        total_days = calculate_total_days(aggregated_dates_list)
    else:
        streak_days = max_streak_days = total_days = 0
    
    # Calculate total metrics (including children)
    total_xp_with_children = xp + child_total_xp
    total_articles_with_children = articles_count + child_total_articles
    max_level_in_tree = max(level, child_max_level)
    
    # Build folder data structure
    folder_data = {
        'name': folder_name,
        'path': folder_path,
        'depth': current_depth,
        
        # Metrics for current folder only
        'xp': xp,
        'level': level,
        'taskCount': articles_count,
        'streakDays': streak_days,
        'maxStreakDays': max_streak_days,
        'totalDays': total_days,
        'lastTaskDate': last_activity.isoformat() if last_activity else datetime.now().isoformat(),
        'totalWords': total_words,
        
        # Aggregated metrics (including children)
        'totalXpWithChildren': total_xp_with_children,
        'totalArticlesWithChildren': total_articles_with_children,
        'maxLevelInTree': max_level_in_tree,
        
        # Tree structure
        'children': children,
        'childrenCount': len(children),
        'hasChildren': len(children) > 0,
        
        # Display info
        'color': get_domain_color(folder_name),
        'isLeaf': len(children) == 0,
        
        # Internal: dates for parent aggregation (will be removed before API response)
        '_dates_set': aggregated_dates
    }
    
    return folder_data


# ================================================================================
#                           TREE BUILDING & DISPLAY FUNCTIONS
# ================================================================================

def build_complete_folder_tree(
    base_path: str, 
    supported_extensions: Set[str], 
    specific_folders: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Build complete folder tree cho tất cả các folders hoặc specific folders.
    
    Args:
        base_path (str): Đường dẫn base để scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        specific_folders (List[str], optional): Danh sách các folder cụ thể cần scan
        
    Returns:
        Dict[str, Any]: Complete tree structure
    """
    if not os.path.exists(base_path):
        print(f"❌ Base path không tồn tại: {base_path}")
        return {}
    
    tree_data = {}
    
    print(f"🌳 Building complete tree từ: {base_path}")
    
    # Scan all items in base path
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        
        if os.path.isdir(item_path):
            # Filter by specific folders if provided
            if specific_folders and item not in specific_folders:
                continue
            
            print(f"\n🌿 Scanning root folder: {item}")
            folder_tree = scan_folder_tree_recursive(item_path, supported_extensions, max_depth=4)
            
            if folder_tree:
                # Remove internal _dates_set before returning
                def strip_internal(node: Dict[str, Any]):
                    node.pop('_dates_set', None)
                    for child in node.get('children', {}).values():
                        strip_internal(child)
                
                strip_internal(folder_tree)
                tree_data[item] = folder_tree
    
    print(f"\n✅ Tree building completed: {len(tree_data)} root folders")
    return tree_data


def get_top_subfolders_by_level(domains_data: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
    """
    Lấy danh sách top N subfolders có level cao nhất từ domains data.
    
    Args:
        domains_data (Dict): Dữ liệu domains từ scan
        top_n (int): Số lượng top subfolders cần lấy (default: 3)
        
    Returns:
        List[Dict]: Danh sách top subfolders sorted by level
    """
    all_subfolders = []
    
    # Collect all subfolders from all domains
    for domain_name, domain_data in domains_data.items():
        subfolders = domain_data.get('subfolders', {})
        
        for subfolder_name, subfolder_data in subfolders.items():
            all_subfolders.append({
                'name': subfolder_name,
                'parent': domain_name,
                'level': subfolder_data['level'],
                'xp': subfolder_data['xp'],
                'taskCount': subfolder_data['taskCount'],
                'streakDays': subfolder_data['streakDays'],
                'color': subfolder_data.get('color', '#6B7280')
            })
    
    # Sort by level (descending) and return top N
    sorted_subfolders = sorted(all_subfolders, key=lambda x: x['level'], reverse=True)
    return sorted_subfolders[:top_n]


def format_tree_display(tree_data: Dict[str, Any], show_stats: bool = True) -> str:
    """
    Format tree data thành string để hiển thị dạng ASCII tree.
    
    Args:
        tree_data (Dict): Tree data từ build_complete_folder_tree
        show_stats (bool): Có hiển thị stats không (default: True)
        
    Returns:
        str: Formatted tree string for display
        
    Example output:
        📁 Domain 1 (Level 5, XP 5,230, Files 52)
        ├── 📁 Subfolder A (Level 2, XP 2,100, Files 21)
        └── 📁 Subfolder B (Level 3, XP 3,130, Files 31)
    """
    
    def format_folder_line(folder_data: Dict[str, Any], prefix: str = "", is_last: bool = True) -> str:
        """Format một dòng cho folder với proper indentation."""
        connector = "└── " if is_last else "├── "
        name = folder_data['name']
        
        if show_stats:
            level = folder_data['level']
            xp = folder_data['xp']
            task_count = folder_data['taskCount']
            
            # Show aggregated stats if has children
            if folder_data.get('hasChildren', False):
                total_xp = folder_data.get('totalXpWithChildren', xp)
                total_articles = folder_data.get('totalArticlesWithChildren', task_count)
                max_level = folder_data.get('maxLevelInTree', level)
                
                if total_xp != xp or total_articles != task_count:
                    stats = f"(L{level}→{max_level}, {xp:,}→{total_xp:,} XP, {task_count}→{total_articles} files)"
                else:
                    stats = f"(Level {level}, {xp:,} XP, {task_count} files)"
            else:
                stats = f"(Level {level}, {xp:,} XP, {task_count} files)"
                
            line = f"{prefix}{connector}📁 {name} {stats}"
        else:
            line = f"{prefix}{connector}📁 {name}"
        
        return line
    
    def format_tree_recursive(
        folder_data: Dict[str, Any], 
        prefix: str = "", 
        is_last: bool = True
    ) -> List[str]:
        """Recursive function để format tree với proper ASCII art."""
        lines = []
        
        # Add current folder line
        lines.append(format_folder_line(folder_data, prefix, is_last))
        
        # Process children if any
        children = folder_data.get('children', {})
        if children:
            # Prepare child prefix
            child_prefix = prefix + ("    " if is_last else "│   ")
            child_items = list(children.items())
            
            # Format each child
            for i, (child_name, child_data) in enumerate(child_items):
                is_last_child = (i == len(child_items) - 1)
                child_lines = format_tree_recursive(child_data, child_prefix, is_last_child)
                lines.extend(child_lines)
        
        return lines
    
    # Build complete tree display
    all_lines = []
    root_items = list(tree_data.items())
    
    for i, (root_name, root_data) in enumerate(root_items):
        is_last_root = (i == len(root_items) - 1)
        root_lines = format_tree_recursive(root_data, "", is_last_root)
        all_lines.extend(root_lines)
        
        # Add separator between root folders for readability
        if not is_last_root:
            all_lines.append("")
    
    return "\n".join(all_lines)


# ================================================================================
#                           MODULE TESTING
# ================================================================================

if __name__ == "__main__":
    """Test các functions chính của module."""
    
    print("=" * 80)
    print("TESTING UTILS_FOLDER MODULE")
    print("=" * 80)
    
    # Test configuration
    TEST_PATH = r"D:\vip_DOCUMENTS_OBS\home\All"
    TEST_EXTENSIONS = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf'}
    
    print(f"\n📁 Test path: {TEST_PATH}")
    print(f"📝 Supported extensions: {TEST_EXTENSIONS}")
    
    # Test 1: Domain color mapping
    print("\n🎨 Testing domain colors:")
    test_domains = ['Domain 1', 'Domain 5', '0. NHẤT HƯỚNG', 'Unknown']
    for domain in test_domains:
        color = get_domain_color(domain)
        print(f"  {domain}: {color}")
    
    # Test 2: Single folder scan (if path exists)
    if os.path.exists(TEST_PATH):
        print("\n📊 Testing single folder scan:")
        test_folders = os.listdir(TEST_PATH)[:2]  # Test first 2 folders
        
        for folder_name in test_folders:
            folder_path = os.path.join(TEST_PATH, folder_name)
            if os.path.isdir(folder_path):
                result = scan_single_folder(folder_path, TEST_EXTENSIONS)
                if result:
                    print(f"\n  {folder_name}:")
                    print(f"    Level: {result['level']}")
                    print(f"    XP: {result['xp']:,}")
                    print(f"    Files: {result['taskCount']}")
                    print(f"    Streak: {result['streakDays']} days")
    
    print("\n" + "=" * 80)
    print("✅ Module testing completed!")