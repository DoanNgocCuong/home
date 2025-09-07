#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để hiển thị level của từng folder một cách rõ ràng
"""

import requests
import json

def show_folder_levels():
    """Hiển thị level của từng folder trong 3 folders đầu"""
    try:
        # Gọi API để lấy thông tin chi tiết
        response = requests.get('http://localhost:8000/api/domains/detailed')
        
        if response.status_code != 200:
            print(f"❌ Lỗi API: {response.status_code}")
            return
        
        data = response.json()
        
        if not data.get('success'):
            print("❌ API không trả về dữ liệu thành công")
            return
        
        domains = data.get('domains', {})
        
        print("=" * 80)
        print("📊 BẢNG LEVELS CỦA CÁC FOLDERS")
        print("=" * 80)
        
        folder_count = 0
        
        # Sắp xếp domains theo tên để hiển thị theo thứ tự
        sorted_domains = sorted(domains.items())
        
        for domain_name, domain_data in sorted_domains:
            folder_count += 1
            
            print(f"\n🗂️  FOLDER {folder_count}: {domain_name}")
            print(f"   📈 Level: {domain_data['level']}")
            print(f"   ⭐ XP: {domain_data['xp']:,}")
            print(f"   📄 Files: {domain_data['taskCount']}")
            print(f"   🔥 Streak: {domain_data['streakDays']} days")
            
            # Hiển thị subfolders nếu có
            subfolders = domain_data.get('subfolders', {})
            if subfolders:
                print(f"   📂 Subfolders ({len(subfolders)}):")
                
                # Sắp xếp subfolders theo level (cao → thấp)
                sorted_subfolders = sorted(
                    subfolders.items(), 
                    key=lambda x: x[1]['level'], 
                    reverse=True
                )
                
                for subfolder_name, subfolder_data in sorted_subfolders:
                    print(f"      └── 📁 {subfolder_name}")
                    print(f"          📈 Level: {subfolder_data['level']}")
                    print(f"          ⭐ XP: {subfolder_data['xp']:,}")
                    print(f"          📄 Files: {subfolder_data['taskCount']}")
            
            # Chỉ hiển thị 3 folders đầu theo yêu cầu
            if folder_count >= 3:
                break
        
        print("\n" + "=" * 80)
        print("🏆 TOP 3 HIGHEST LEVEL SUBFOLDERS:")
        print("=" * 80)
        
        # Thu thập tất cả subfolders từ tất cả domains
        all_subfolders = []
        for domain_name, domain_data in domains.items():
            subfolders = domain_data.get('subfolders', {})
            for subfolder_name, subfolder_data in subfolders.items():
                all_subfolders.append({
                    'name': subfolder_name,
                    'parent': domain_name,
                    'level': subfolder_data['level'],
                    'xp': subfolder_data['xp'],
                    'taskCount': subfolder_data['taskCount']
                })
        
        # Sắp xếp theo level cao nhất
        top_subfolders = sorted(all_subfolders, key=lambda x: x['level'], reverse=True)[:3]
        
        for i, subfolder in enumerate(top_subfolders, 1):
            print(f"\n🥇 #{i}: {subfolder['name']}")
            print(f"   📁 Parent: {subfolder['parent']}")
            print(f"   📈 Level: {subfolder['level']}")
            print(f"   ⭐ XP: {subfolder['xp']:,}")
            print(f"   📄 Files: {subfolder['taskCount']}")
        
        print("\n" + "=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối tới API. Hãy chạy backend server trước:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == '__main__':
    show_folder_levels()
