#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Domain Progress Tracker Backend
Scan các domain folders và tính XP/Level như Tag system
"""

import os
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Cấu hình
DATA_SCIENCE_PATH = r"D:\vip_DOCUMENTS_OBS\home\DATA SCIENCE AND AI"
SUPPORTED_EXTENSIONS = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf'}

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
    """Lấy màu cho domain"""
    for key, color in DOMAIN_COLORS.items():
        if key in domain_name:
            return color
    return DOMAIN_COLORS['default']

def calculate_xp_from_articles(articles_count, total_words):
    """Tính XP dựa trên số bài viết và số từ"""
    # Base XP: 100 XP per article
    base_xp = articles_count * 100
    
    # Bonus XP: 1 XP per 10 words
    word_bonus = total_words // 10
    
    return base_xp + word_bonus

def calculate_level_from_xp(xp):
    """Tính level từ XP (giống như tag system)"""
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
    """Ước tính số từ trong file"""
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
    """Tính streak days dựa trên ngày viết bài"""
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
    
    return {
        'name': domain_name,
        'xp': xp,
        'level': level,
        'color': get_domain_color(domain_name),
        'taskCount': articles_count,  # Số bài viết
        'streakDays': streak_days,
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
                    'lastTaskDate': domain_data['lastTaskDate']
                }
    
    return domains

@app.route('/')
def index():
    """Serve static files"""
    return send_from_directory('.', 'index.html')

@app.route('/api/domains', methods=['GET'])
def get_domains():
    """API endpoint để lấy danh sách domains với XP/Level"""
    try:
        domains = scan_all_domains()
        
        return jsonify({
            'success': True,
            'domains': domains,
            'count': len(domains),
            'last_scan': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/domains/refresh', methods=['POST'])
def refresh_domains():
    """API endpoint để refresh domain data"""
    try:
        domains = scan_all_domains()
        
        return jsonify({
            'success': True,
            'message': 'Domains refreshed successfully',
            'domains': domains,
            'count': len(domains),
            'last_scan': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/domains/stats', methods=['GET'])
def get_domain_stats():
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
        
        return jsonify({
            'success': True,
            'stats': {
                'total_domains': len(domains),
                'total_articles': total_articles,
                'total_xp': total_xp,
                'total_levels': total_levels,
                'average_level': total_levels / len(domains) if domains else 0,
                'highest_level_domain': highest_level_domain,
                'most_articles_domain': most_articles_domain
            },
            'last_scan': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Domain Progress Tracker Server...")
    print(f"📁 Scanning path: {DATA_SCIENCE_PATH}")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API endpoints:")
    print("  - GET /api/domains - Get all domains with XP/Level")
    print("  - POST /api/domains/refresh - Refresh domain data")
    print("  - GET /api/domains/stats - Get domain statistics")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
