#!/usr/bin/env python3
"""
Script để sửa lại đường dẫn ảnh trong các file markdown
Từ: ![[assets/2025/image.png]]
Thành: ![[assets/image.png]]
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIARY_DIR = BASE_DIR / "All" / "NHẬT KÝ"

# Pattern để tìm link ảnh có đường dẫn sai
WRONG_PATTERN = re.compile(r'!\[\[assets/(\d{4})/([^\]]+)\]\]')
CORRECT_PATTERN = r'![[assets/\2]]'


def fix_image_paths():
    """Sửa lại đường dẫn ảnh trong tất cả file markdown"""
    markdown_files = list(DIARY_DIR.rglob("*.md"))
    
    fixed_count = 0
    
    for md_file in markdown_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            original_content = content
            
            # Thay thế đường dẫn sai
            content = WRONG_PATTERN.sub(CORRECT_PATTERN, content)
            
            if content != original_content:
                md_file.write_text(content, encoding='utf-8')
                fixed_count += 1
                print(f"Fixed: {md_file.name}")
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
    
    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    fix_image_paths()
