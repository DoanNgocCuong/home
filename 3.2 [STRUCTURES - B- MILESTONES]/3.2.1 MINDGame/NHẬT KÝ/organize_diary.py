import os
import re
import shutil

base_dirs = [
    r"d:\vip_DOCUMENTS_OBS\home\All\NHẬT KÝ\2025",
    r"d:\vip_DOCUMENTS_OBS\home\All\NHẬT KÝ\2026"
]

def organize_files(directory):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    print(f"Processing {directory}...")
    moved_count = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue

        # Match YYYY-MM-DD format
        match = re.match(r"^(\d{4})-(\d{2})-\d{2}", filename)
        if match:
            year, month = match.groups()
            
            target_folder = os.path.join(directory, month)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            
            new_path = os.path.join(target_folder, filename)
            # print(f"Moving {filename} to {month}/")
            shutil.move(file_path, new_path)
            moved_count += 1
            
    print(f"Moved {moved_count} files in {directory}.")

if __name__ == "__main__":
    for d in base_dirs:
        organize_files(d)
