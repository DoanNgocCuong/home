#!/usr/bin/env python3
"""
Script để tổ chức lại thư mục nhật ký theo tháng.
Di chuyển file markdown và ảnh vào thư mục tháng tương ứng.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Đường dẫn gốc - tự động tìm từ thư mục hiện tại hoặc từ __file__
if __file__:
    try:
        BASE_DIR = Path(__file__).parent / "2025"
    except:
        # Fallback: tìm từ thư mục hiện tại
        BASE_DIR = Path.cwd() / "All" / "NHẬT KÝ" / "2025"
else:
    BASE_DIR = Path.cwd() / "All" / "NHẬT KÝ" / "2025"

ASSETS_DIR = BASE_DIR / "assets"


def extract_month_from_filename(filename: str) -> Optional[str]:
    """
    Trích xuất tháng từ tên file.
    Format: YYYY-MM-DD hoặc YYYY-MM-DD - description
    """
    # Pattern: YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        return match.group(2)  # Trả về MM
    
    # Pattern: YYYYMMDD trong tên file ảnh
    match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if match:
        return match.group(2)  # Trả về MM
    
    return None


def extract_month_from_image_name(image_name: str) -> Optional[str]:
    """
    Trích xuất tháng từ tên file ảnh.
    Format: Pasted image YYYYMMDDHHMMSS.png
    """
    match = re.search(r'(\d{4})(\d{2})(\d{2})', image_name)
    if match:
        return match.group(2)  # Trả về MM
    return None


def find_image_references(md_file: Path) -> List[str]:
    """
    Tìm tất cả các tham chiếu ảnh trong file markdown.
    Trả về danh sách tên file ảnh.
    """
    image_refs = []
    
    if not md_file.exists():
        return image_refs
    
    content = md_file.read_text(encoding='utf-8')
    
    # Pattern 1: ![[assets/Pasted image ...]]
    pattern1 = r'!\[\[assets/([^\]]+)\]\]'
    matches1 = re.findall(pattern1, content)
    image_refs.extend(matches1)
    
    # Pattern 2: ![[Pasted image ...]]
    pattern2 = r'!\[\[([^\]]*Pasted image[^\]]+)\]\]'
    matches2 = re.findall(pattern2, content)
    image_refs.extend(matches2)
    
    # Pattern 3: ![](assets/...)
    pattern3 = r'!\[[^\]]*\]\(assets/([^\)]+)\)'
    matches3 = re.findall(pattern3, content)
    image_refs.extend(matches3)
    
    return image_refs


def update_image_paths(md_file: Path, old_assets_path: str, new_assets_path: str) -> bool:
    """
    Cập nhật đường dẫn ảnh trong file markdown.
    """
    if not md_file.exists():
        return False
    
    content = md_file.read_text(encoding='utf-8')
    original_content = content
    
    # Thay thế ![[assets/...]] thành ![[../assets/...]] hoặc ![[assets/...]]
    # Tùy vào vị trí file markdown so với assets
    content = re.sub(
        r'!\[\[assets/([^\]]+)\]\]',
        lambda m: f'![[{new_assets_path}/{m.group(1)}]]',
        content
    )
    
    # Thay thế ![](assets/...) thành ![](../assets/...) hoặc ![](assets/...)
    content = re.sub(
        r'!\[([^\]]*)\]\(assets/([^\)]+)\)',
        lambda m: f'![{m.group(1)}]({new_assets_path}/{m.group(2)})',
        content
    )
    
    if content != original_content:
        md_file.write_text(content, encoding='utf-8')
        return True
    
    return False


def organize_files():
    """
    Tổ chức lại file theo tháng.
    """
    # Tạo thư mục tháng
    month_dirs = {}
    for month in range(1, 13):
        month_str = f"{month:02d}"
        month_dir = BASE_DIR / month_str
        month_dir.mkdir(exist_ok=True)
        month_dirs[month_str] = month_dir
    
    # Tạo thư mục assets cho từng tháng
    month_assets_dirs = {}
    for month in range(1, 13):
        month_str = f"{month:02d}"
        assets_dir = BASE_DIR / month_str / "assets"
        assets_dir.mkdir(exist_ok=True)
        month_assets_dirs[month_str] = assets_dir
    
    # Map ảnh -> tháng (để biết ảnh nào thuộc tháng nào)
    image_to_month: Dict[str, str] = {}
    
    # Bước 1: Xử lý file markdown
    md_files = list(BASE_DIR.glob("*.md"))
    moved_files = []
    
    for md_file in md_files:
        month = extract_month_from_filename(md_file.name)
        if not month:
            print(f"⚠️  Không thể xác định tháng cho file: {md_file.name}")
            continue
        
        # Tìm các ảnh được tham chiếu trong file này
        image_refs = find_image_references(md_file)
        
        # Map ảnh -> tháng
        for img_ref in image_refs:
            img_name = os.path.basename(img_ref)
            image_to_month[img_name] = month
        
        # Di chuyển file markdown
        target_dir = month_dirs[month]
        target_file = target_dir / md_file.name
        
        if target_file.exists():
            print(f"⚠️  File đã tồn tại: {target_file}")
        else:
            shutil.move(str(md_file), str(target_file))
            moved_files.append((md_file, target_file))
            print(f"✅ Đã di chuyển: {md_file.name} -> {month}/")
    
    # Bước 2: Di chuyển ảnh vào thư mục tháng tương ứng
    if ASSETS_DIR.exists():
        image_files = list(ASSETS_DIR.glob("*.png")) + list(ASSETS_DIR.glob("*.jpg")) + \
                      list(ASSETS_DIR.glob("*.jpeg")) + list(ASSETS_DIR.glob("*.webp")) + \
                      list(ASSETS_DIR.glob("*.gif"))
        
        for img_file in image_files:
            # Thử xác định tháng từ tên file
            month = extract_month_from_image_name(img_file.name)
            
            # Nếu không tìm được từ tên file, thử tìm từ map
            if not month:
                month = image_to_month.get(img_file.name)
            
            if not month:
                print(f"⚠️  Không thể xác định tháng cho ảnh: {img_file.name}")
                # Di chuyển vào thư mục "unknown" hoặc giữ nguyên
                continue
            
            # Di chuyển ảnh
            target_assets_dir = month_assets_dirs[month]
            target_img_file = target_assets_dir / img_file.name
            
            if target_img_file.exists():
                print(f"⚠️  Ảnh đã tồn tại: {target_img_file}")
            else:
                shutil.move(str(img_file), str(target_img_file))
                print(f"✅ Đã di chuyển ảnh: {img_file.name} -> {month}/assets/")
    
    # Bước 3: Cập nhật đường dẫn ảnh trong các file markdown
    for old_path, new_path in moved_files:
        # Đường dẫn mới: assets/... (vì assets nằm cùng thư mục với markdown)
        new_assets_path = "assets"
        updated = update_image_paths(new_path, "assets", new_assets_path)
        if updated:
            print(f"✅ Đã cập nhật đường dẫn ảnh trong: {new_path.name}")
    
    # Xóa thư mục assets cũ nếu rỗng
    if ASSETS_DIR.exists():
        try:
            if not any(ASSETS_DIR.iterdir()):
                ASSETS_DIR.rmdir()
                print(f"✅ Đã xóa thư mục assets cũ (rỗng)")
        except OSError:
            pass
    
    print("\n✅ Hoàn thành tổ chức lại file theo tháng!")


if __name__ == "__main__":
    organize_files()
