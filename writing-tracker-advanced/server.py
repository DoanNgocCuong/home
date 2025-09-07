#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Writing Tracker Server
Tích hợp với Python script để scan bài viết thực tế
"""

import os
import json
import csv
from datetime import datetime
import re
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# Cấu hình
SUPPORTED_EXTENSIONS = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf'}
DEFAULT_SCAN_PATH = r"D:\vip_DOCUMENTS_OBS\home"

class ArticleScanner:
    def __init__(self):
        self.scan_results = []
        self.is_scanning = False
        self.last_scan_time = None

    def scan_folder(self, folder_path, include_subfolders=True):
        """Scan thư mục và trả về danh sách bài viết"""
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Thư mục không tồn tại: {folder_path}")
        
        self.is_scanning = True
        articles_data = []
        
        try:
            if include_subfolders:
                # Duyệt qua tất cả file trong thư mục (bao gồm cả thư mục con)
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        article_info = self._analyze_file(file_path, folder_path)
                        if article_info:
                            articles_data.append(article_info)
            else:
                # Chỉ scan thư mục hiện tại
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        article_info = self._analyze_file(file_path, folder_path)
                        if article_info:
                            articles_data.append(article_info)
            
            # Sắp xếp theo ngày tạo
            articles_data.sort(key=lambda x: x['date'], reverse=True)
            
            self.scan_results = articles_data
            self.last_scan_time = datetime.now()
            
            return articles_data
            
        finally:
            self.is_scanning = False

    def _analyze_file(self, file_path, base_path):
        """Phân tích một file và trả về thông tin bài viết"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext not in SUPPORTED_EXTENSIONS:
                return None
            
            # Lấy thông tin file
            stat_info = os.stat(file_path)
            
            # Ngày tạo file (hoặc ngày sửa đổi)
            creation_time = datetime.fromtimestamp(stat_info.st_ctime)
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            
            # Tên file (bỏ extension)
            title = Path(file_path).stem
            
            # Ước tính số từ
            word_count = self._estimate_word_count(file_path, file_ext)
            
            # Đoán danh mục từ đường dẫn hoặc tên file
            category = self._guess_category(file_path, title)
            
            # Kích thước file (KB)
            file_size = round(stat_info.st_size / 1024, 2)
            
            # Đường dẫn tương đối
            relative_path = os.path.relpath(file_path, base_path)
            
            # Thư mục chứa file
            folder = os.path.dirname(relative_path) or "Root"
            
            article_info = {
                'id': len(self.scan_results) + 1,
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
            
            return article_info
            
        except Exception as e:
            print(f"Lỗi khi phân tích file {file_path}: {e}")
            return None

    def _estimate_word_count(self, file_path, file_ext):
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

    def _guess_category(self, file_path, title):
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

# Khởi tạo scanner
scanner = ArticleScanner()

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/scan', methods=['POST'])
def scan_articles():
    """API endpoint để scan bài viết"""
    try:
        data = request.get_json()
        folder_path = data.get('folder_path', DEFAULT_SCAN_PATH)
        include_subfolders = data.get('include_subfolders', True)
        
        if scanner.is_scanning:
            return jsonify({
                'success': False,
                'message': 'Đang quét, vui lòng đợi...',
                'is_scanning': True
            }), 202
        
        # Chạy scan trong thread riêng để không block
        def scan_thread():
            try:
                articles = scanner.scan_folder(folder_path, include_subfolders)
                print(f"Scan hoàn thành: {len(articles)} bài viết")
            except Exception as e:
                print(f"Lỗi khi scan: {e}")
        
        thread = threading.Thread(target=scan_thread)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Bắt đầu quét bài viết...',
            'is_scanning': True
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_scan_status():
    """Lấy trạng thái scan"""
    return jsonify({
        'is_scanning': scanner.is_scanning,
        'last_scan_time': scanner.last_scan_time.isoformat() if scanner.last_scan_time else None,
        'article_count': len(scanner.scan_results)
    })

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Lấy danh sách bài viết"""
    return jsonify({
        'success': True,
        'articles': scanner.scan_results,
        'count': len(scanner.scan_results),
        'last_scan': scanner.last_scan_time.isoformat() if scanner.last_scan_time else None
    })

@app.route('/api/export/<format>', methods=['GET'])
def export_articles(format):
    """Xuất dữ liệu ra file"""
    try:
        if format == 'csv':
            # Tạo CSV
            output = []
            if scanner.scan_results:
                output.append(','.join(scanner.scan_results[0].keys()))
                for article in scanner.scan_results:
                    row = [str(article[key]) for key in article.keys()]
                    output.append(','.join(f'"{item}"' for item in row))
            
            return '\n'.join(output), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename=articles-{datetime.now().strftime("%Y%m%d")}.csv'
            }
        
        elif format == 'json':
            return jsonify({
                'articles': scanner.scan_results,
                'export_date': datetime.now().isoformat(),
                'count': len(scanner.scan_results)
            })
        
        else:
            return jsonify({'error': 'Format không hỗ trợ'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Lấy thống kê"""
    try:
        articles = scanner.scan_results
        
        if not articles:
            return jsonify({
                'total_articles': 0,
                'current_streak': 0,
                'longest_streak': 0,
                'this_week': 0,
                'total_folders': 0,
                'categories': {},
                'monthly_data': []
            })
        
        # Tính streak
        current_streak = calculate_current_streak(articles)
        longest_streak = calculate_longest_streak(articles)
        
        # Tính tuần này
        this_week = calculate_this_week(articles)
        
        # Tính thư mục
        total_folders = len(set(article['folder'] for article in articles))
        
        # Tính categories
        categories = {}
        for article in articles:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        # Tính dữ liệu theo tháng
        monthly_data = get_monthly_data(articles)
        
        return jsonify({
            'total_articles': len(articles),
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'this_week': this_week,
            'total_folders': total_folders,
            'categories': categories,
            'monthly_data': monthly_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_current_streak(articles):
    """Tính streak hiện tại"""
    if not articles:
        return 0
    
    # Sắp xếp theo ngày giảm dần
    sorted_dates = sorted([datetime.strptime(article['date'], '%Y-%m-%d') for article in articles], reverse=True)
    
    streak = 0
    current_date = datetime.now().date()
    
    for article_date in sorted_dates:
        if article_date.date() == current_date:
            streak += 1
            current_date = current_date.replace(day=current_date.day - 1)
        elif article_date.date() < current_date:
            break
    
    return streak

def calculate_longest_streak(articles):
    """Tính streak dài nhất"""
    if not articles:
        return 0
    
    # Sắp xếp theo ngày tăng dần
    sorted_dates = sorted([datetime.strptime(article['date'], '%Y-%m-%d') for article in articles])
    
    max_streak = 0
    current_streak = 1
    
    for i in range(1, len(sorted_dates)):
        prev_date = sorted_dates[i-1].date()
        current_date = sorted_dates[i].date()
        
        if (current_date - prev_date).days == 1:
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1
    
    return max(max_streak, current_streak)

def calculate_this_week(articles):
    """Tính số bài viết tuần này"""
    now = datetime.now()
    start_of_week = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_week.replace(day=start_of_week.day - start_of_week.weekday())
    
    count = 0
    for article in articles:
        article_date = datetime.strptime(article['date'], '%Y-%m-%d')
        if article_date >= start_of_week:
            count += 1
    
    return count

def get_monthly_data(articles):
    """Lấy dữ liệu theo tháng"""
    monthly_data = {}
    
    for article in articles:
        date = datetime.strptime(article['date'], '%Y-%m-%d')
        month_key = date.strftime('%Y-%m')
        monthly_data[month_key] = monthly_data.get(month_key, 0) + 1
    
    # Sắp xếp theo tháng
    sorted_months = sorted(monthly_data.items())
    
    return [{'month': month, 'count': count} for month, count in sorted_months]

if __name__ == '__main__':
    print("🚀 Starting Advanced Writing Tracker Server...")
    print(f"📁 Default scan path: {DEFAULT_SCAN_PATH}")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API endpoints:")
    print("  - POST /api/scan - Scan articles")
    print("  - GET /api/status - Get scan status")
    print("  - GET /api/articles - Get articles list")
    print("  - GET /api/stats - Get statistics")
    print("  - GET /api/export/csv - Export CSV")
    print("  - GET /api/export/json - Export JSON")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
