#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Writing Tracker - Article Scanner
Tích hợp với web app để scan bài viết thực tế
"""

import os
import json
import csv
from datetime import datetime
import re
from pathlib import Path
import sys

def analyze_article_folder(folder_path, output_format='json'):
    """
    Scan thư mục bài viết và tạo file dữ liệu
    
    Args:
        folder_path: Đường dẫn đến thư mục chứa bài viết
        output_format: 'csv' hoặc 'json'
    """
    
    # Các extension file được hỗ trợ
    supported_extensions = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf'}
    
    articles_data = []
    
    # Duyệt qua tất cả file trong thư mục (bao gồm cả thư mục con)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()
            
            if file_ext in supported_extensions:
                try:
                    # Lấy thông tin file
                    stat_info = os.stat(file_path)
                    
                    # Ngày tạo file (hoặc ngày sửa đổi)
                    creation_time = datetime.fromtimestamp(stat_info.st_ctime)
                    modified_time = datetime.fromtimestamp(stat_info.st_mtime)
                    
                    # Tên file (bỏ extension)
                    title = Path(file).stem
                    
                    # Ước tính số từ
                    word_count = estimate_word_count(file_path, file_ext)
                    
                    # Đoán danh mục từ đường dẫn hoặc tên file
                    category = guess_category(file_path, title)
                    
                    # Kích thước file (KB)
                    file_size = round(stat_info.st_size / 1024, 2)
                    
                    # Đường dẫn tương đối
                    relative_path = os.path.relpath(file_path, folder_path)
                    
                    # Thư mục chứa file
                    folder = os.path.dirname(relative_path) or "Root"
                    
                    article_info = {
                        'id': len(articles_data) + 1,
                        'title': title,
                        'filePath': file_path,
                        'relativePath': relative_path,
                        'category': category,
                        'date': creation_time.strftime('%Y-%m-%d'),
                        'modifiedDate': modified_time.strftime('%Y-%m-%d'),
                        'wordCount': word_count,
                        'fileSize': file_size,
                        'fileExtension': file_ext,
                        'folder': folder,
                        'createdAt': creation_time.isoformat()
                    }
                    
                    articles_data.append(article_info)
                    print(f"✅ Đã phân tích: {title}")
                    
                except Exception as e:
                    print(f"❌ Lỗi khi đọc file {file}: {e}")
    
    # Sắp xếp theo ngày tạo
    articles_data.sort(key=lambda x: x['date'], reverse=True)
    
    # Xuất dữ liệu
    if output_format.lower() == 'json':
        output_file = 'articles_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)
    else:
        output_file = 'articles_data.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if articles_data:
                writer = csv.DictWriter(f, fieldnames=articles_data[0].keys())
                writer.writeheader()
                writer.writerows(articles_data)
    
    print(f"\n🎉 Hoàn thành! Đã tạo file: {output_file}")
    print(f"📊 Tổng cộng: {len(articles_data)} bài viết")
    return output_file, articles_data

def estimate_word_count(file_path, file_ext):
    """Ước tính số từ trong file"""
    try:
        if file_ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Đếm từ (tách bằng khoảng trắng)
                words = len(content.split())
                return words
        elif file_ext == '.html':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Loại bỏ HTML tags và đếm từ
                clean_text = re.sub(r'<[^>]+>', ' ', content)
                words = len(clean_text.split())
                return words
        else:
            # Đối với các file khác, ước tính dựa trên kích thước
            file_size = os.path.getsize(file_path)
            # Ước tính ~5 ký tự/từ
            estimated_words = file_size // 5
            return max(100, estimated_words)  # Tối thiểu 100 từ
    except:
        return 500  # Giá trị mặc định

def guess_category(file_path, title):
    """Đoán danh mục từ đường dẫn hoặc tiêu đề"""
    path_lower = file_path.lower()
    title_lower = title.lower()
    
    categories = {
        'technical': ['tech', 'technology', 'ai', 'machine', 'programming', 'code', 'software', 'công nghệ', 'domain', 'ml', 'dl', 'nlp', 'rag', 'llm'],
        'business': ['business', 'marketing', 'finance', 'money', 'kinh doanh', 'tài chính', 'market', 'product'],
        'personal': ['life', 'lifestyle', 'living', 'đời sống', 'cuộc sống', 'personal', 'note', 'daily', 'reflection'],
        'education': ['education', 'learning', 'study', 'giáo dục', 'học tập', 'course', 'lesson', 'tutorial', 'guide'],
        'other': ['other', 'misc', 'khác', 'untitled']
    }
    
    full_text = f"{path_lower} {title_lower}"
    
    for category, keywords in categories.items():
        if any(keyword in full_text for keyword in keywords):
            return category
    
    return 'other'

def create_sample_usage():
    """Tạo ví dụ sử dụng"""
    print("=== ADVANCED WRITING TRACKER - ARTICLE SCANNER ===")
    print("1. Thay đổi đường dẫn thư mục bài viết của bạn")
    print("2. Chạy script để tạo file JSON")
    print("3. Import file JSON vào web tracker")
    print()
    
    # Ví dụ sử dụng
    folder_path = input("Nhập đường dẫn thư mục bài viết (Enter để dùng mặc định): ").strip()
    
    if not folder_path:
        folder_path = r"D:\vip_DOCUMENTS_OBS\home"  # Đường dẫn mặc định
        print(f"Sử dụng đường dẫn mặc định: {folder_path}")
    
    if os.path.exists(folder_path):
        print(f"\n📁 Đang scan thư mục: {folder_path}")
        output_file, articles = analyze_article_folder(folder_path, 'json')
        
        # Hiển thị thống kê
        print(f"\n📈 THỐNG KÊ:")
        print(f"- Tổng bài viết: {len(articles)}")
        
        categories = {}
        for article in articles:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("- Phân bố danh mục:")
        for cat, count in categories.items():
            print(f"  • {cat}: {count} bài")
            
        print(f"\n💾 File đã tạo: {output_file}")
        print("🔄 Bây giờ bạn có thể import file này vào web tracker!")
        
    else:
        print(f"❌ Thư mục không tồn tại: {folder_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Chạy với tham số command line
        folder_path = sys.argv[1]
        output_format = sys.argv[2] if len(sys.argv) > 2 else 'json'
        
        if os.path.exists(folder_path):
            print(f"📁 Scanning: {folder_path}")
            output_file, articles = analyze_article_folder(folder_path, output_format)
            print(f"✅ Completed: {len(articles)} articles found")
        else:
            print(f"❌ Folder not found: {folder_path}")
    else:
        # Chạy interactive mode
        create_sample_usage()
