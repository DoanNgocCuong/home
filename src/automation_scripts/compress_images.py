import os
import re
from pathlib import Path
from PIL import Image

# ================= CẤU HÌNH VÀ THIẾT LẬP =================
# Thư mục chứa ghi chú và ảnh
WORKING_DIR = Path(r"d:\VIP\working")

# Dung lượng tối thiểu của ảnh PNG (tính bằng MB) để script quét và nén
SIZE_THRESHOLD_MB = 1.0

# Chất lượng của ảnh WebP (từ 0 đến 100). 95 là rất tốt và gần như không khác bản gốc
QUALITY = 95

# NẾU TRUE: Script sẽ XÓA vĩnh viễn file PNG gốc sau khi đã nén thành công sang WebP.
# NẾU FALSE: Script vẫn giữ nguyên file PNG bên cạnh file WebP (bạn có thể tự xóa bằng tay).
DELETE_ORIGINAL = True
# =========================================================

def compress_images():
    print(f"[*] Đang quét thư mục: {WORKING_DIR}")
    
    # 1. Quét tìm tất cả các file PNG
    png_files = list(WORKING_DIR.rglob("*.png"))
    large_pngs = [f for f in png_files if f.stat().st_size > SIZE_THRESHOLD_MB * 1024 * 1024]
    
    if not large_pngs:
        print("[!] Không tìm thấy ảnh PNG nào quá lớn để nén.")
        return

    print(f"[*] Tìm thấy {len(large_pngs)} ảnh PNG nặng trên {SIZE_THRESHOLD_MB}MB.")
    
    # Dictionary lưu trữ tên file cũ -> tên file mới để replace trong markdown
    converted_files = {} 
    
    # 2. Xử lý nén ảnh PNG sang WebP
    for png_path in large_pngs:
        webp_path = png_path.with_suffix(".webp")
        size_mb = png_path.stat().st_size / (1024*1024)
        
        print(f"    - Đang nén: {png_path.name} ({size_mb:.2f} MB)")
        try:
            # Mở file và nén
            with Image.open(png_path) as img:
                img.save(webp_path, "webp", quality=QUALITY)
            
            # Lưu lại tên file để bước sau tiến hành replace trong markdown
            converted_files[png_path.name] = webp_path.name
            
            # Xóa file PNG gốc nếu thành công và cho phép xóa
            if DELETE_ORIGINAL and webp_path.exists():
                png_path.unlink()
        except Exception as e:
            print(f"[ERROR] Lỗi không thể nén {png_path.name}: {e}")

    # 3. Cập nhật lại các liên kết ảnh trong file Markdown
    if converted_files:
        print("\n[*] Đang tìm và cập nhật liên kết ảnh trong các file Markdown...")
        md_files = list(WORKING_DIR.rglob("*.md"))
        updated_count = 0
        
        for md_path in md_files:
            try:
                # Đọc nội dung file Markdown
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Biến đổi các link hình ảnh
                for old_name, new_name in converted_files.items():
                    # Xử lý trường hợp có thể Obsidian encode dấu cách thành %20
                    old_name_encoded = old_name.replace(" ", "%20")
                    new_name_encoded = new_name.replace(" ", "%20")
                    
                    # Thay thế đường dẫn chuẩn (vd: ![[Pasted image ...png]])
                    content = content.replace(old_name, new_name)
                    # Thay thế cả đường dẫn mã hóa URL (vd: ![alt](Pasted%20image%...png))
                    content = content.replace(old_name_encoded, new_name_encoded)
                
                # Nếu nội dung thay đổi, ghi đè lại file
                if content != original_content:
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_count += 1
                    print(f"    - Đã cập nhật xong file: {md_path.name}")
            except Exception as e:
                print(f"[ERROR] Lỗi khi đọc/ghi file Markdown {md_path.name}: {e}")
                
        print(f"\n[DONE] Hoàn tất! Đã nén ảnh và cập nhật lại {updated_count} bài viết Markdown.")

if __name__ == "__main__":
    compress_images()
