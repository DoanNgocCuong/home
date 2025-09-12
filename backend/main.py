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
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import re

# Import utilities từ module riêng
from utils_folder_level import (
    get_domain_color,
    calculate_xp_from_articles,
    calculate_level_from_xp,
    estimate_word_count,
    calculate_streak_days,
    calculate_max_historical_streak,
    calculate_total_days,
    scan_single_folder,
    scan_folder_with_subfolders,
    get_top_subfolders_by_level,
    build_complete_folder_tree,
    format_tree_display
)
from utils_streak import (
    calculate_github_like_streak,
    build_contribution_calendar,
)

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
from pathlib import Path
import os

# Sử dụng pathlib để xử lý đường dẫn linh hoạt
BASE_DIR = Path(__file__).parent
DATA_SCIENCE_PATH = BASE_DIR / "data"  # /app/data trong Docker
CKP_PATH = BASE_DIR / "ckp"  # /app/ckp trong Docker  
NOTES_PATH = BASE_DIR / "notes"  # /app/notes trong Docker

# Fallback cho development (khi chạy local)
if not DATA_SCIENCE_PATH.exists():
    # Đường dẫn development
    DATA_SCIENCE_PATH = Path(r"D:\vip_DOCUMENTS_OBS\home\All")
    CKP_PATH = Path(r"D:\vip_DOCUMENTS_OBS\home\0_CKP")
    NOTES_PATH = Path(r"D:\vip_DOCUMENTS_OBS\home\NOTE")

SUPPORTED_EXTENSIONS = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf'}

# Pydantic Models
class DomainData(BaseModel):
    xp: int
    level: int
    color: str
    taskCount: int
    streakDays: int
    maxStreakDays: int
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

# Domain colors và utility functions đã được chuyển sang utils_folder_level.py

# Các utility functions đã được chuyển sang utils_folder_level.py


# scan_domain_folder function đã được thay thế bằng scan_single_folder trong utils_folder_level.py

# scan_domain_with_subfolders function đã được chuyển sang utils_folder_level.py

def scan_all_domains():
    """Scan tất cả domain folders bao gồm các thư mục cụ thể trong All"""
    domains = {}
    
    if not DATA_SCIENCE_PATH.exists():
        return domains
    
    # Danh sách các thư mục cụ thể cần scan
    specific_folders = [
        "0. NHẤT HƯỚNG",
        "DATA_SCIENCE_AND_AI", 
        "NOTE"
    ]
    
    # Tìm tất cả domain folders và specific folders
    for item in DATA_SCIENCE_PATH.iterdir():
        item_path = item
        
        # Scan các domain folders (giữ logic cũ)
        if item_path.is_dir() and item.name.startswith('Domain'):
            domain_data = scan_single_folder(item_path, SUPPORTED_EXTENSIONS)
            if domain_data:
                domains[domain_data['name']] = {
                    'xp': domain_data['xp'],
                    'level': domain_data['level'],
                    'color': domain_data['color'],
                    'taskCount': domain_data['taskCount'],
                    'streakDays': domain_data['streakDays'],
                    'maxStreakDays': domain_data['maxStreakDays'],
                    'totalDays': domain_data['totalDays'],
                    'lastTaskDate': domain_data['lastTaskDate']
                }
        
        # Scan các specific folders trong All directory với detailed scanning
        elif item_path.is_dir() and item.name in specific_folders:
            domain_data = scan_folder_with_subfolders(item_path, SUPPORTED_EXTENSIONS)
            if domain_data:
                domains[domain_data['name']] = {
                    'xp': domain_data['xp'],
                    'level': domain_data['level'],
                    'color': domain_data['color'],
                    'taskCount': domain_data['taskCount'],
                    'streakDays': domain_data['streakDays'],
                    'maxStreakDays': domain_data['maxStreakDays'],
                    'totalDays': domain_data['totalDays'],
                    'lastTaskDate': domain_data['lastTaskDate'],
                    'subfolders': domain_data.get('subfolders', {}),
                    'subfolderCount': domain_data.get('subfolderCount', 0)
                }

                # Also surface subfolders as top-level domains for UI visibility
                for sub_name, sub_data in domain_data.get('subfolders', {}).items():
                    # Avoid key collision; keep child original name if unique
                    child_key = sub_name if sub_name not in domains else f"{domain_data['name']} / {sub_name}"
                    domains[child_key] = {
                        'xp': sub_data['xp'],
                        'level': sub_data['level'],
                        'color': sub_data['color'],
                        'taskCount': sub_data['taskCount'],
                        'streakDays': sub_data['streakDays'],
                        'maxStreakDays': sub_data['maxStreakDays'],
                        'totalDays': sub_data['totalDays'],
                        'lastTaskDate': sub_data['lastTaskDate']
                    }
    
    return domains

def _collect_all_contribution_dates() -> List[datetime]:
    """Thu thập tất cả ngày đóng góp (thời gian tạo file) trên toàn hệ thống.
    Chỉ tính các file có phần mở rộng được hỗ trợ, trong các thư mục như scan_all_domains().
    """
    contribution_dates: List[datetime] = []
    if not DATA_SCIENCE_PATH.exists():
        return contribution_dates

    specific_folders = [
        "0. NHẤT HƯỚNG",
        "DATA_SCIENCE_AND_AI", 
        "NOTE"
    ]

    for item in DATA_SCIENCE_PATH.iterdir():
        item_path = item

        if not item_path.is_dir():
            continue

        # Chỉ lấy các folder Domain* hoặc specific_folders
        if not (item.name.startswith('Domain') or item.name in specific_folders):
            continue

        for root, dirs, files in os.walk(item_path):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in SUPPORTED_EXTENSIONS:
                    try:
                        stat_info = os.stat(os.path.join(root, file))
                        contribution_dates.append(datetime.fromtimestamp(stat_info.st_ctime))
                    except Exception:
                        continue
    return contribution_dates

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
            "stats": "/api/domains/stats",
            "detailed": "/api/domains/detailed",
            "tree": "/api/domains/tree",
            "tree_display": "/api/domains/tree/display"
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

@app.get("/api/domains/detailed")
async def get_detailed_domains():
    """API endpoint để lấy thông tin chi tiết các domain bao gồm subfolder levels"""
    try:
        domains = scan_all_domains()
        
        # Tạo response chi tiết với subfolder information
        detailed_response = {
            'success': True,
            'domains': {},
            'count': len(domains),
            'last_scan': datetime.now().isoformat()
        }
        
        for domain_name, domain_data in domains.items():
            detailed_response['domains'][domain_name] = {
                'xp': domain_data['xp'],
                'level': domain_data['level'],
                'color': domain_data['color'],
                'taskCount': domain_data['taskCount'],
                'streakDays': domain_data['streakDays'],
                'maxStreakDays': domain_data['maxStreakDays'],
                'totalDays': domain_data['totalDays'],
                'lastTaskDate': domain_data['lastTaskDate'],
                'subfolders': domain_data.get('subfolders', {}),
                'subfolderCount': domain_data.get('subfolderCount', 0)
            }
        
        return detailed_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New: Global streak and contribution calendar endpoints
@app.get("/api/streak/global")
async def get_global_streak():
    try:
        dates = _collect_all_contribution_dates()
        result = calculate_github_like_streak(dates, require_today=True)
        return { 'success': True, 'streak': result }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/streak/calendar")
async def get_contribution_calendar(days: int = 365):
    try:
        dates = _collect_all_contribution_dates()
        calendar = build_contribution_calendar(dates, days=days)
        return { 'success': True, 'days': days, 'calendar': calendar }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/domains/tree")
async def get_folder_tree():
    """API endpoint để lấy cấu trúc cây thư mục đầy đủ cho tất cả các cấp"""
    try:
        # Danh sách các thư mục cụ thể cần scan
        specific_folders = [
            "0. NHẤT HƯỚNG",
            "DATA_SCIENCE_AND_AI", 
            "NOTE"
        ]
        
        # Build complete tree structure
        tree_data = build_complete_folder_tree(
            DATA_SCIENCE_PATH, 
            SUPPORTED_EXTENSIONS, 
            specific_folders
        )
        
        # Tạo response với tree structure
        tree_response = {
            'success': True,
            'tree': tree_data,
            'count': len(tree_data),
            'last_scan': datetime.now().isoformat(),
            'scan_path': str(DATA_SCIENCE_PATH),
            'supported_extensions': list(SUPPORTED_EXTENSIONS)
        }
        
        return tree_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/domains/tree/display")
async def get_folder_tree_display():
    """API endpoint để lấy hiển thị ASCII tree của cấu trúc thư mục"""
    try:
        # Danh sách các thư mục cụ thể cần scan
        specific_folders = [
            "0. NHẤT HƯỚNG",
            "DATA_SCIENCE_AND_AI", 
            "NOTE"
        ]
        
        # Build complete tree structure
        tree_data = build_complete_folder_tree(
            DATA_SCIENCE_PATH, 
            SUPPORTED_EXTENSIONS, 
            specific_folders
        )
        
        # Format tree display
        tree_display = format_tree_display(tree_data, show_stats=True)
        
        # Tạo response với formatted tree
        display_response = {
            'success': True,
            'tree_display': tree_display,
            'tree_data': tree_data,
            'count': len(tree_data),
            'last_scan': datetime.now().isoformat(),
            'scan_path': str(DATA_SCIENCE_PATH)
        }
        
        return display_response
        
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
