#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để hiển thị cấu trúc cây thư mục với tất cả các cấp
"""

import requests
import json

def show_tree_structure():
    """Hiển thị cấu trúc cây thư mục cho tất cả các cấp"""
    try:
        print("🌳 ĐANG LẤY CẤU TRÚC CÂY THƯ MỤC...")
        print("=" * 80)
        
        # Gọi API để lấy tree display
        response = requests.get('http://localhost:8000/api/domains/tree/display')
        
        if response.status_code != 200:
            print(f"❌ Lỗi API: {response.status_code}")
            return
        
        data = response.json()
        
        if not data.get('success'):
            print("❌ API không trả về dữ liệu thành công")
            return
        
        # Hiển thị ASCII tree
        tree_display = data.get('tree_display', '')
        if tree_display:
            print("📂 CẤU TRÚC CÂY THƯ MỤC:")
            print("-" * 80)
            print(tree_display)
            print("-" * 80)
        
        # Hiển thị thống kê tổng quan
        tree_data = data.get('tree_data', {})
        scan_path = data.get('scan_path', '')
        last_scan = data.get('last_scan', '')
        
        print(f"\n📊 THỐNG KÊ TỔNG QUAN:")
        print(f"📁 Đường dẫn scan: {scan_path}")
        print(f"🔍 Số folder gốc: {len(tree_data)}")
        print(f"🕐 Thời gian scan: {last_scan}")
        
        # Thống kê chi tiết cho từng root folder
        for root_name, root_data in tree_data.items():
            print(f"\n🗂️  ROOT FOLDER: {root_name}")
            print(f"   📈 Level: {root_data['level']} → Max: {root_data['maxLevelInTree']}")
            print(f"   ⭐ XP: {root_data['xp']:,} → Total: {root_data['totalXpWithChildren']:,}")
            print(f"   📄 Files: {root_data['taskCount']} → Total: {root_data['totalArticlesWithChildren']}")
            print(f"   📂 Subfolders: {root_data['childrenCount']}")
            print(f"   🔥 Streak: {root_data['streakDays']} days")
            
            if root_data['hasChildren']:
                print(f"   └── Chi tiết subfolders:")
                show_children_stats(root_data['children'], depth=1)
        
        print("\n" + "=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối tới API. Hãy chạy backend server trước:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def show_children_stats(children: dict, depth: int = 0, max_depth: int = 3):
    """Hiển thị thống kê chi tiết cho children"""
    if depth > max_depth:
        return
    
    indent = "       " + "  " * depth
    
    # Sắp xếp theo level (cao → thấp)
    sorted_children = sorted(
        children.items(), 
        key=lambda x: x[1]['level'], 
        reverse=True
    )
    
    for child_name, child_data in sorted_children:
        print(f"{indent}📁 {child_name}: Level {child_data['level']}, XP {child_data['xp']:,}, Files {child_data['taskCount']}")
        
        # Nếu có children, hiển thị tiếp (recursive)
        if child_data.get('hasChildren') and depth < max_depth:
            show_children_stats(child_data.get('children', {}), depth + 1, max_depth)

def show_simple_tree():
    """Hiển thị tree structure đơn giản (chỉ tên folder)"""
    try:
        print("\n🌿 CẤU TRÚC CÂY ĐơN GIẢN:")
        print("=" * 50)
        
        # Gọi API để lấy tree data
        response = requests.get('http://localhost:8000/api/domains/tree')
        
        if response.status_code == 200:
            data = response.json()
            tree_data = data.get('tree', {})
            
            for root_name, root_data in tree_data.items():
                print(f"📁 {root_name}")
                show_simple_children(root_data.get('children', {}), depth=1)
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Lỗi khi hiển thị simple tree: {e}")

def show_simple_children(children: dict, depth: int = 0, max_depth: int = 4):
    """Hiển thị children đơn giản"""
    if depth > max_depth:
        return
    
    indent = "  " * depth
    connector = "├── " if depth > 0 else ""
    
    for child_name, child_data in children.items():
        print(f"{indent}{connector}📁 {child_name}")
        
        # Nếu có children, hiển thị tiếp (recursive)
        if child_data.get('hasChildren'):
            show_simple_children(child_data.get('children', {}), depth + 1, max_depth)

if __name__ == '__main__':
    print("🌳 DOMAIN PROGRESS TRACKER - TREE STRUCTURE VIEWER")
    print("=" * 80)
    
    show_tree_structure()
    show_simple_tree()
