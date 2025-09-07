# utils_folder_level.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    UTILITIES FOR FOLDER LEVEL SCANNING
================================================================================

MÔ TẢ:
    Module chứa các hàm tiện ích để scan và tính toán level cho các folder
    và subfolder trong hệ thống theo dõi tiến độ học tập.

CHỨC NĂNG CHÍNH:
    1. Scan folder đơn lẻ và tính toán XP/Level
    2. Scan folder với các subfolder chi tiết
    3. Ước tính số từ trong các loại file khác nhau
    4. Tính toán các metrics: XP, Level, Streak, etc.

TÁC GIẢ: Hệ thống theo dõi tiến độ học tập
NGÀY TẠO: 2024
PHIÊN BẢN: 1.0.0
================================================================================
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

# Import các hàm tính toán từ main module (sẽ được import khi cần)
def get_domain_color(domain_name: str) -> str:
    """
    Lấy màu sắc tương ứng cho domain dựa trên tên domain
    
    Args:
        domain_name (str): Tên của domain
        
    Returns:
        str: Mã màu hex tương ứng với domain
    """
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
    
    for key, color in DOMAIN_COLORS.items():
        if key in domain_name:
            return color
    return DOMAIN_COLORS['default']

def calculate_xp_from_articles(articles_count: int, total_words: int) -> int:
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
    """
    # Base XP: 100 XP per article
    base_xp = articles_count * 100
    
    # Bonus XP: 1 XP per 10 words
    word_bonus = total_words // 10
    
    return base_xp + word_bonus

def calculate_level_from_xp(xp: int) -> int:
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

def estimate_word_count(file_path: str, file_ext: str) -> int:
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

def calculate_streak_days(article_dates: List[datetime]) -> int:
    """
    Tính toán số ngày liên tiếp (không gián đoạn) có hoạt động viết bài
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
        
    Returns:
        int: Số ngày liên tiếp học tập (streak days)
    """
    if not article_dates:
        return 0
    
    # Chuyển datetime object thành date object và deduplicate
    article_date_set = {
        d.date() if isinstance(d, datetime) else d 
        for d in article_dates
    }
    
    if not article_date_set:
        return 0
    
    current_date = datetime.now().date()
    
    # Flexible mode: Nếu hôm nay chưa viết, bắt đầu từ ngày gần nhất có bài viết
    if current_date not in article_date_set:
        try:
            current_date = max(d for d in article_date_set if d <= current_date)
        except ValueError:
            return 0
    
    # Tính toán giới hạn thông minh
    min_date = min(article_date_set)
    max_possible_days = (current_date - min_date).days + 1
    max_days = min(365, max_possible_days)
    
    # Main counting loop
    streak = 0
    day_counter = 0
    
    while day_counter < max_days and current_date >= min_date:
        if current_date in article_date_set:
            streak += 1
            current_date = current_date - timedelta(days=1)
        else:
            break
        day_counter += 1
    
    return streak

def calculate_max_historical_streak(article_dates: List[datetime]) -> int:
    """
    Tìm chuỗi ngày liên tiếp dài nhất từng có trong toàn bộ lịch sử viết bài
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
        
    Returns:
        int: Streak tối đa trong lịch sử
    """
    if not article_dates:
        return 0
    
    # Convert và sort các ngày unique
    unique_dates = sorted({
        d.date() if isinstance(d, datetime) else d 
        for d in article_dates
    })
    
    if not unique_dates:
        return 0
    
    if len(unique_dates) == 1:
        return 1
    
    # Sliding window algorithm
    max_streak = current_streak = 1
    
    for i in range(1, len(unique_dates)):
        prev_date = unique_dates[i-1]
        curr_date = unique_dates[i]
        
        day_gap = (curr_date - prev_date).days
        
        if day_gap == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    
    return max_streak

def calculate_total_days(article_dates: List[datetime]) -> int:
    """
    Tính toán tổng số ngày học tập từ ngày đầu tiên đến hiện tại
    
    Args:
        article_dates (list): Danh sách các datetime object của ngày tạo bài viết
        
    Returns:
        int: Tổng số ngày từ ngày đầu tiên đến hiện tại
    """
    if not article_dates:
        return 0
    
    # Tìm ngày đầu tiên (xa nhất)
    first_date = min(article_dates).date()
    current_date = datetime.now().date()
    
    # Tính số ngày
    total_days = (current_date - first_date).days + 1  # +1 để bao gồm cả ngày đầu
    
    return max(1, total_days)  # Ít nhất là 1 ngày

def scan_single_folder(folder_path: str, supported_extensions: set) -> Optional[Dict[str, Any]]:
    """
    Scan một folder đơn lẻ và trả về thông tin XP/Level
    
    Args:
        folder_path (str): Đường dẫn đến folder cần scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        
    Returns:
        Dict[str, Any]: Thông tin folder bao gồm XP, level, etc. hoặc None nếu không tồn tại
    """
    if not os.path.exists(folder_path):
        return None
    
    folder_name = os.path.basename(folder_path)
    print(f"📁 SCAN DEBUG: Đang scan folder: {folder_name}")
    
    articles_count = 0
    total_words = 0
    article_dates = []
    last_activity = None
    
    # Duyệt qua tất cả file trong folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()
            
            if file_ext in supported_extensions:
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
        'name': folder_name,
        'xp': xp,
        'level': level,
        'color': get_domain_color(folder_name),
        'taskCount': articles_count,
        'streakDays': streak_days,
        'maxStreakDays': max_streak_days,
        'totalDays': total_days,
        'lastTaskDate': last_activity.isoformat() if last_activity else datetime.now().isoformat(),
        'totalWords': total_words,
        'lastActivity': last_activity.isoformat() if last_activity else None
    }

def scan_folder_with_subfolders(folder_path: str, supported_extensions: set) -> Optional[Dict[str, Any]]:
    """
    Scan folder và các subfolder của nó để hiển thị level từng folder riêng biệt
    
    Args:
        folder_path (str): Đường dẫn đến folder chính cần scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        
    Returns:
        Dict[str, Any]: Thông tin folder chính + subfolders hoặc None nếu không tồn tại
    """
    if not os.path.exists(folder_path):
        return None
    
    folder_name = os.path.basename(folder_path)
    print(f"📁 DETAILED SCAN: Đang scan {folder_name} với subfolders...")
    
    # Scan folder chính
    folder_data = scan_single_folder(folder_path, supported_extensions)
    if not folder_data:
        return None
    
    # Scan các subfolder
    subfolders = {}
    
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Chỉ scan các thư mục con, bỏ qua file
            if os.path.isdir(item_path):
                subfolder_data = scan_single_folder(item_path, supported_extensions)
                if subfolder_data:  # Luôn hiển thị cả khi chưa có file hợp lệ
                    subfolders[item] = {
                        'name': item,
                        'xp': subfolder_data['xp'],
                        'level': subfolder_data['level'],
                        'color': subfolder_data['color'],
                        'taskCount': subfolder_data['taskCount'],
                        'streakDays': subfolder_data['streakDays'],
                        'maxStreakDays': subfolder_data['maxStreakDays'],
                        'totalDays': subfolder_data['totalDays'],
                        'lastTaskDate': subfolder_data['lastTaskDate']
                    }
                    print(f"  📂 Subfolder: {item} - Level {subfolder_data['level']} - XP {subfolder_data['xp']} - {subfolder_data['taskCount']} files")
    except Exception as e:
        print(f"Lỗi khi scan subfolders của {folder_name}: {e}")
    
    # Thêm thông tin subfolders vào folder data
    folder_data['subfolders'] = subfolders
    folder_data['subfolderCount'] = len(subfolders)
    
    return folder_data

def get_top_subfolders_by_level(domains_data: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
    """
    Lấy danh sách top N subfolders có level cao nhất
    
    Args:
        domains_data (Dict): Dữ liệu domains từ scan_all_domains
        top_n (int): Số lượng top subfolders cần lấy
        
    Returns:
        List[Dict]: Danh sách top subfolders
    """
    all_subfolders = []
    
    for domain_name, domain_data in domains_data.items():
        subfolders = domain_data.get('subfolders', {})
        for subfolder_name, subfolder_data in subfolders.items():
            all_subfolders.append({
                'name': subfolder_name,
                'parent': domain_name,
                'level': subfolder_data['level'],
                'xp': subfolder_data['xp'],
                'taskCount': subfolder_data['taskCount'],
                'streakDays': subfolder_data['streakDays']
            })
    
    # Sắp xếp theo level cao nhất
    return sorted(all_subfolders, key=lambda x: x['level'], reverse=True)[:top_n]

def scan_folder_tree_recursive(folder_path: str, supported_extensions: set, max_depth: int = 3, current_depth: int = 0) -> Optional[Dict[str, Any]]:
    """
    Scan folder theo kiểu cây đệ quy để hiển thị tất cả các cấp
    
    Args:
        folder_path (str): Đường dẫn đến folder cần scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        max_depth (int): Độ sâu tối đa để scan (tránh vô hạn)
        current_depth (int): Độ sâu hiện tại
        
    Returns:
        Dict[str, Any]: Thông tin folder với tree structure hoặc None nếu không tồn tại
    """
    if not os.path.exists(folder_path) or current_depth > max_depth:
        return None
    
    folder_name = os.path.basename(folder_path)
    print(f"{'  ' * current_depth}📁 TREE SCAN: Đang scan {folder_name} (depth {current_depth})")
    
    # Scan files trong folder hiện tại
    articles_count = 0
    total_words = 0
    article_dates = []
    last_activity = None
    
    # Scan files (không recursive, chỉ trong folder hiện tại)
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            if os.path.isfile(file_path):
                file_ext = Path(file).suffix.lower()
                
                if file_ext in supported_extensions:
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
                        print(f"{'  ' * current_depth}❌ Lỗi khi đọc file {file}: {e}")
    except Exception as e:
        print(f"{'  ' * current_depth}❌ Lỗi khi scan folder {folder_name}: {e}")
    
    # Tính toán metrics cho folder hiện tại
    xp = calculate_xp_from_articles(articles_count, total_words)
    level = calculate_level_from_xp(xp)
    # Ghi nhận ngày hoạt động của các file TRỰC TIẾP trong folder hiện tại
    aggregated_dates = {
        (d.date() if isinstance(d, datetime) else d)
        for d in article_dates
    }
    
    # Scan subfolders (recursive)
    children = {}
    child_total_xp = 0
    child_total_articles = 0
    child_max_level = 0
    
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            if os.path.isdir(item_path):
                # Skip các folder ẩn hoặc system folders
                if item.startswith('.') or item.startswith('__'):
                    continue
                    
                child_data = scan_folder_tree_recursive(
                    item_path, 
                    supported_extensions, 
                    max_depth, 
                    current_depth + 1
                )
                
                # Luôn giữ child vào tree, kể cả khi chưa có file hợp lệ
                if child_data:
                    children[item] = child_data
                    # Aggregate totals including all descendants of the child
                    child_total_xp += child_data.get('totalXpWithChildren', child_data['xp'])
                    child_total_articles += child_data.get('totalArticlesWithChildren', child_data['taskCount'])
                    # Gom ngày hoạt động từ child (đã được child tổng hợp)
                    child_dates = child_data.get('_dates_set')
                    if child_dates:
                        aggregated_dates.update(child_dates)
                    child_max_level = max(child_max_level, child_data['level'])
                    
                    print(f"{'  ' * current_depth}  └── {item}: Level {child_data['level']}, XP {child_data['xp']}, Files {child_data['taskCount']}")
    except Exception as e:
        print(f"{'  ' * current_depth}❌ Lỗi khi scan subfolders của {folder_name}: {e}")
    
    # TÍNH STREAK/GLOBAL-DAYS CHO TOÀN BỘ CÂY CỦA FOLDER NÀY
    # - Streak của folder = streak của TỔNG hợp tất cả ngày hoạt động của chính folder + mọi folder con
    if aggregated_dates:
        streak_days = calculate_streak_days(list(aggregated_dates))
        max_streak_days = calculate_max_historical_streak(list(aggregated_dates))
        first_date = min(aggregated_dates)
        total_days = (datetime.now().date() - first_date).days + 1
    else:
        streak_days = 0
        max_streak_days = 0
        total_days = 0

    # Tính total metrics (bao gồm cả children)
    total_xp_with_children = xp + child_total_xp
    total_articles_with_children = articles_count + child_total_articles
    max_level_in_tree = max(level, child_max_level)
    
    folder_data = {
        'name': folder_name,
        'path': folder_path,
        'depth': current_depth,
        
        # Metrics của folder hiện tại (chỉ files trong folder này)
        'xp': xp,
        'level': level,
        'taskCount': articles_count,
        'streakDays': streak_days,
        'maxStreakDays': max_streak_days,
        'totalDays': total_days,
        'lastTaskDate': last_activity.isoformat() if last_activity else datetime.now().isoformat(),
        'totalWords': total_words,
        
        # Metrics tổng hợp (bao gồm children)
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
    }
    # LƯU Ý: _dates_set là internal để truyền ngược lên cha khi tính streak tổng hợp.
    # Khi trả JSON ra API Tree, khóa này sẽ bị loại bỏ ở build_complete_folder_tree.
    folder_data['_dates_set'] = aggregated_dates
    
    return folder_data

def build_complete_folder_tree(base_path: str, supported_extensions: set, specific_folders: List[str] = None) -> Dict[str, Any]:
    """
    Build complete folder tree cho tất cả các folders
    
    Args:
        base_path (str): Đường dẫn base để scan
        supported_extensions (set): Set các file extensions được hỗ trợ
        specific_folders (List[str]): Danh sách các folder cụ thể cần scan
        
    Returns:
        Dict[str, Any]: Complete tree structure
    """
    if not os.path.exists(base_path):
        return {}
    
    tree_data = {}
    
    print(f"🌳 BUILDING COMPLETE TREE từ: {base_path}")
    
    # Scan tất cả items trong base path
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        
        if os.path.isdir(item_path):
            # Nếu có specific_folders, chỉ scan những folder đó
            if specific_folders and item not in specific_folders:
                continue
            
            print(f"\n🌿 Scanning root folder: {item}")
            folder_tree = scan_folder_tree_recursive(item_path, supported_extensions, max_depth=4)
            
            if folder_tree:
                # Loại bỏ khóa nội bộ _dates_set khỏi toàn bộ cây trước khi trả kết quả
                def strip_internal(node: Dict[str, Any]):
                    node.pop('_dates_set', None)
                    for child in node.get('children', {}).values():
                        strip_internal(child)
                strip_internal(folder_tree)
                tree_data[item] = folder_tree
    
    return tree_data

def format_tree_display(tree_data: Dict[str, Any], show_stats: bool = True) -> str:
    """
    Format tree data thành string để hiển thị dạng ASCII tree
    
    Args:
        tree_data (Dict): Tree data từ build_complete_folder_tree
        show_stats (bool): Có hiển thị stats không
        
    Returns:
        str: Formatted tree string
    """
    def format_folder_line(folder_data: Dict[str, Any], prefix: str = "", is_last: bool = True) -> str:
        """Format một dòng cho folder"""
        connector = "└── " if is_last else "├── "
        name = folder_data['name']
        
        if show_stats:
            level = folder_data['level']
            xp = folder_data['xp']
            task_count = folder_data['taskCount']
            
            # Nếu có children, hiển thị tổng stats
            if folder_data['hasChildren']:
                total_xp = folder_data['totalXpWithChildren']
                total_articles = folder_data['totalArticlesWithChildren']
                max_level = folder_data['maxLevelInTree']
                stats = f"(Level {level}→{max_level}, XP {xp}→{total_xp:,}, Files {task_count}→{total_articles})"
            else:
                stats = f"(Level {level}, XP {xp:,}, Files {task_count})"
                
            line = f"{prefix}{connector}📁 {name} {stats}"
        else:
            line = f"{prefix}{connector}📁 {name}"
        
        return line
    
    def format_tree_recursive(folder_data: Dict[str, Any], prefix: str = "", is_last: bool = True) -> List[str]:
        """Recursive function để format tree"""
        lines = []
        
        # Add current folder line
        lines.append(format_folder_line(folder_data, prefix, is_last))
        
        # Add children
        children = folder_data.get('children', {})
        if children:
            child_prefix = prefix + ("    " if is_last else "│   ")
            child_items = list(children.items())
            
            for i, (child_name, child_data) in enumerate(child_items):
                is_last_child = i == len(child_items) - 1
                child_lines = format_tree_recursive(child_data, child_prefix, is_last_child)
                lines.extend(child_lines)
        
        return lines
    
    # Build complete tree display
    all_lines = []
    root_items = list(tree_data.items())
    
    for i, (root_name, root_data) in enumerate(root_items):
        is_last_root = i == len(root_items) - 1
        root_lines = format_tree_recursive(root_data, "", is_last_root)
        all_lines.extend(root_lines)
        
        # Add separator between root folders
        if not is_last_root:
            all_lines.append("")
    
    return "\n".join(all_lines)
