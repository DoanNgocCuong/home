#!/usr/bin/env python3
"""
Script để quy hoạch lại thư mục nhật ký:
- Di chuyển daily notes từ All/NOTE/1. DailyNote/ sang All/NHẬT KÝ/{năm}/
- Di chuyển ảnh vào thư mục assets/{năm}/ và cập nhật đường dẫn trong markdown
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
import json

# Cấu hình đường dẫn
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR / "All" / "NOTE" / "1. DailyNote"
TARGET_DIR = BASE_DIR / "All" / "NHẬT KÝ"
ATTACHMENTS_DIR = BASE_DIR / "All" / "NOTE" / "1. DailyNote" / "attachments"
IMAGE_DIR = BASE_DIR / "All" / "NOTE" / "1. DailyNote" / "image"

# Pattern để tìm năm từ tên file hoặc đường dẫn
YEAR_PATTERN = re.compile(r'(\d{4})')

# Pattern để tìm link ảnh trong markdown
IMAGE_LINK_PATTERN = re.compile(
    r'!\[\[([^\]]+\.(?:png|jpg|jpeg|webp|gif))\]\]|'
    r'!\[([^\]]*)\]\(([^\)]+\.(?:png|jpg|jpeg|webp|gif))\)'
)


def extract_year_from_path(file_path: Path) -> str:
    """Trích xuất năm từ đường dẫn file"""
    # Tìm năm trong đường dẫn
    matches = YEAR_PATTERN.findall(str(file_path))
    if matches:
        # Lấy năm đầu tiên tìm thấy (thường là năm trong tên file)
        year = matches[0]
        # Kiểm tra năm hợp lệ (1900-2100)
        if 1900 <= int(year) <= 2100:
            return year
    
    # Nếu không tìm thấy trong đường dẫn, thử tìm trong tên file
    matches = YEAR_PATTERN.findall(file_path.name)
    if matches:
        year = matches[0]
        if 1900 <= int(year) <= 2100:
            return year
    
    return None


def find_image_files() -> Dict[str, Path]:
    """Tìm tất cả các file ảnh và map với tên file"""
    image_map = {}
    
    # Tìm trong thư mục attachments
    if ATTACHMENTS_DIR.exists():
        for img_file in ATTACHMENTS_DIR.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
                # Lưu cả tên file và đường dẫn đầy đủ
                image_map[img_file.name] = img_file
                # Lưu cả đường dẫn tương đối từ thư mục image
                if 'image' in str(img_file):
                    rel_path = img_file.relative_to(IMAGE_DIR.parent)
                    image_map[str(rel_path)] = img_file
    
    # Tìm trong thư mục image (bao gồm cả thư mục con)
    if IMAGE_DIR.exists():
        for img_file in IMAGE_DIR.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
                image_map[img_file.name] = img_file
                # Lưu cả đường dẫn tương đối
                rel_path = img_file.relative_to(IMAGE_DIR)
                image_map[str(rel_path)] = img_file
                # Lưu cả đường dẫn với prefix "image/"
                image_map[f"image/{rel_path}"] = img_file
    
    return image_map


def extract_year_from_image_name(image_name: str) -> str:
    """Trích xuất năm từ tên file ảnh (ví dụ: Pasted image 20251017000302.png)"""
    matches = YEAR_PATTERN.findall(image_name)
    if matches:
        year_str = matches[0]
        if len(year_str) == 4 and 1900 <= int(year_str) <= 2100:
            return year_str
    return None


def update_image_links(content: str, old_base_path: Path, new_base_path: Path, year: str) -> Tuple[str, List[Path]]:
    """Cập nhật đường dẫn ảnh trong nội dung markdown và trả về danh sách ảnh cần di chuyển"""
    images_to_move = []
    image_map = find_image_files()
    
    def replace_link(match):
        nonlocal images_to_move
        
        # Pattern 1: ![[image_name]] hoặc ![[image/image_name]]
        if match.group(1):
            image_path_str = match.group(1)
            # Xử lý đường dẫn có thư mục (ví dụ: image/Pasted image ...)
            if '/' in image_path_str:
                parts = image_path_str.split('/', 1)
                actual_image_name = parts[1]
            else:
                actual_image_name = image_path_str
            
            # Tìm file ảnh trong các thư mục
            image_found = None
            
            # Tìm theo tên chính xác
            if actual_image_name in image_map:
                image_found = image_map[actual_image_name]
            else:
                # Tìm theo tên không phân biệt hoa thường hoặc tìm trong thư mục con
                for img_name, img_path in image_map.items():
                    if img_name.lower() == actual_image_name.lower():
                        image_found = img_path
                        break
                    # Tìm trong thư mục con (ví dụ: 2025-09-17/1758062536900.png)
                    if img_path.parent.name == actual_image_name or img_path.name == actual_image_name:
                        image_found = img_path
                        break
            
            if image_found and image_found.exists():
                images_to_move.append(image_found)
                # Tạo đường dẫn mới: assets/{image_name} (ảnh nằm trong assets/ của năm đó)
                new_image_path = f"assets/{image_found.name}"
                return f"![[{new_image_path}]]"
            else:
                # Giữ nguyên nếu không tìm thấy
                print(f"  Canh bao: Khong tim thay anh: {actual_image_name}")
                return match.group(0)
        
        # Pattern 2: ![](path)
        elif match.group(3):
            image_path_str = match.group(3)
            # Xử lý đường dẫn tương đối
            if not image_path_str.startswith('http'):
                image_name = Path(image_path_str).name
                
                # Tìm file ảnh
                image_found = None
                if image_name in image_map:
                    image_found = image_map[image_name]
                else:
                    # Tìm không phân biệt hoa thường
                    for img_name, img_path in image_map.items():
                        if img_name.lower() == image_name.lower():
                            image_found = img_path
                            break
                
                if image_found and image_found.exists():
                    images_to_move.append(image_found)
                    # Tạo đường dẫn mới: assets/{image_name}
                    new_image_path = f"assets/{image_found.name}"
                    return f"![{match.group(2) or ''}]({new_image_path})"
            
            return match.group(0)
        
        return match.group(0)
    
    updated_content = IMAGE_LINK_PATTERN.sub(replace_link, content)
    return updated_content, list(set(images_to_move))


def move_file_with_git(file_path: Path, target_path: Path) -> bool:
    """Di chuyển file sử dụng git mv để giữ lịch sử"""
    try:
        # Tạo thư mục đích nếu chưa tồn tại
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Kiểm tra file có tồn tại không
        if not file_path.exists():
            print(f"  Canh bao: File khong ton tai: {file_path}")
            return False
        
        # Sử dụng git mv nếu file đã được track
        import subprocess
        result = subprocess.run(
            ['git', 'mv', str(file_path), str(target_path)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            return True
        else:
            # Nếu git mv thất bại (file chưa được track), dùng shutil
            if file_path.exists():
                shutil.move(str(file_path), str(target_path))
                return True
            return False
    except Exception as e:
        print(f"Loi khi di chuyen {file_path.name}: {e}")
        # Fallback: dùng shutil
        try:
            if file_path.exists():
                shutil.move(str(file_path), str(target_path))
                return True
        except:
            pass
        return False


def process_daily_notes():
    """Xử lý tất cả daily notes"""
    if not SOURCE_DIR.exists():
        print(f"Thư mục nguồn không tồn tại: {SOURCE_DIR}")
        return
    
    # Tạo thư mục đích
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    # Tìm tất cả file markdown
    markdown_files = list(SOURCE_DIR.rglob("*.md"))
    
    # Nhóm file theo năm
    files_by_year: Dict[str, List[Path]] = {}
    
    for md_file in markdown_files:
        year = extract_year_from_path(md_file)
        if year:
            if year not in files_by_year:
                files_by_year[year] = []
            files_by_year[year].append(md_file)
    
    # Xử lý từng năm
    for year, files in files_by_year.items():
        print(f"\nXu ly nam {year}: {len(files)} files")
        
        # Tạo thư mục đích cho năm
        year_target_dir = TARGET_DIR / year
        year_target_dir.mkdir(parents=True, exist_ok=True)
        
        # Tạo thư mục assets cho năm
        assets_dir = year_target_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Xử lý từng file
        for md_file in files:
            try:
                # Đọc nội dung
                content = md_file.read_text(encoding='utf-8')
                
                # Cập nhật đường dẫn ảnh
                updated_content, images_to_move = update_image_links(
                    content, md_file.parent, year_target_dir, year
                )
                
                # Di chuyển file markdown
                relative_path = md_file.relative_to(SOURCE_DIR)
                target_md_path = year_target_dir / relative_path.name
                
                # Nếu file đã được cập nhật, ghi lại
                if updated_content != content:
                    # Tạo file tạm với nội dung mới
                    temp_path = md_file.with_suffix('.tmp')
                    temp_path.write_text(updated_content, encoding='utf-8')
                    
                    # Di chuyển file tạm
                    move_file_with_git(temp_path, target_md_path)
                    
                    # Xóa file cũ nếu còn tồn tại
                    if md_file.exists():
                        md_file.unlink()
                else:
                    # Chỉ di chuyển file
                    move_file_with_git(md_file, target_md_path)
                
                # Di chuyển ảnh
                for image_path in images_to_move:
                    if image_path.exists():
                        target_image_path = assets_dir / image_path.name
                        move_file_with_git(image_path, target_image_path)
                
                print(f"  OK: {md_file.name}")
                
            except Exception as e:
                print(f"  LOI khi xu ly {md_file.name}: {e}")


if __name__ == "__main__":
    import sys
    # Set UTF-8 encoding for Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    print("Bat dau quy hoach lai thu muc nhat ky...")
    print(f"Nguon: {SOURCE_DIR}")
    print(f"Dich: {TARGET_DIR}")
    
    process_daily_notes()
    
    print("\nHoan thanh!")
