import os
import shutil

# Pre-saved source folders
folders = {
    "1": r"W:\\",   # all
    "2": r"Y:\\",   # 4 no
    "3": r"X:\\",   # 5 no
}

# Ask user to choose source folder
print("Choose source folder:")
print("1 - all (W:\\)")
print("2 - 4 no (Y:\\)")
print("3 - 5 no (X:\\)")
choice_folder = input("Enter choice [1/2/3]: ").strip()

source_folder = folders.get(choice_folder, r"W:\\")  # default to W:\\ if invalid

# Destination and list file remain fixed
destination_folder = r"C:\Users\LENOVO\Desktop\ft"
list_file = r"C:\Users\LENOVO\Desktop\ft\BS.txt"  # Text file containing partial codes

# Ask user whether to copy all matches or just the first one
choice = input("Do you want to copy ALL matching files (A) or ONLY the first match (F)? [A/F]: ").strip().lower()
copy_all = True if choice == "a" else False

# Read partial codes from the text file (strip whitespace/newlines)
with open(list_file, "r") as f:
    partial_codes = [line.strip() for line in f if line.strip()]

# Loop through each partial code
for code in partial_codes:
    found = False
    # Walk through files in source folder
    for filename in os.listdir(source_folder):
        if filename.startswith(code):   # match only files beginning with code
            src_path = os.path.join(source_folder, filename)
            dst_path = os.path.join(destination_folder, filename)
            shutil.copy2(src_path, dst_path)  # copy with metadata
            found = True
            if not copy_all:
                break  # stop after first match if user chose "F"
    if not found:
        print(f"NOT FOUND: {code}")

print("Copy operation completed!")
