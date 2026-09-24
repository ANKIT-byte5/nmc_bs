import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# ==========================
# User Input: Processing Mode
# ==========================
choice = input("Do you want to process ALL matching files (A) or ONLY the latest match (L)? [A/L]: ").strip().lower()
process_all = True if choice == "a" else False

# ==========================
# Load Excel
# ==========================
df = pd.read_excel("WORK.xlsx")

# ==========================
# Config
# ==========================
font_path = "arial.ttf"
os.makedirs("output_images", exist_ok=True)

# ==========================
# Caches
# ==========================
folder_cache = {}
font_cache = {}

# ==========================
# Cached Font Loader
# ==========================
def get_font(size):
    if size not in font_cache:
        font_cache[size] = ImageFont.truetype(font_path, size)
    return font_cache[size]

# ==========================
# Main Loop
# ==========================
for row in df.itertuples(index=False):

    folder = str(row.folder_path)
    code = str(row.code)
    text = str(row.text)

    # ==========================
    # Cache folder listing
    # ==========================
    if folder not in folder_cache:
        try:
            folder_cache[folder] = os.listdir(folder)
        except FileNotFoundError:
            print(f"⚠️ Folder not found: {folder}")
            continue

    folder_files = folder_cache[folder]

    matched_files = [
        f for f in folder_files
        if f.startswith(code)
    ]

    if not matched_files:
        print(f"⚠️ No file found for code {code} in {folder}")
        continue

    # ==========================
    # Determine Files to Process
    # ==========================
    if process_all:
        files_to_process = matched_files
    else:
        # Get only the latest matching file
        latest_file = max(
            matched_files,
            key=lambda f: os.path.getmtime(os.path.join(folder, f))
        )
        files_to_process = [latest_file]

    # Process selected files for this code
    for file in files_to_process:
        img_path = os.path.join(folder, file)

        # ==========================
        # Open image
        # ==========================
        try:
            img = Image.open(img_path).convert("RGBA")
        except Exception as e:
            print(f"⚠️ Could not open {file}: {e}")
            continue

        W, H = img.size
        base = min(W, H)
        draw = ImageDraw.Draw(img)

        # ==========================
        # Initial font size
        # ==========================
        font_size = max(40, min(int(base * 0.06), 180))

        # ==========================
        # Auto-fit font
        # ==========================
        while font_size > 20:
            font = get_font(font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            if text_w <= W * 0.80:
                break
            font_size -= 2

        # Final dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # ==========================
        # Box sizing
        # ==========================
        padding_x = 40
        padding_y = 25

        box_w = text_w + (padding_x * 2)
        box_h = text_h + (padding_y * 2)

        # ==========================
        # Position
        # ==========================
        bottom_margin = max(20, int(H * 0.03))
        box_x = (W - box_w) // 2
        box_y = H - box_h - bottom_margin

        # ==========================
        # Transparent Overlay
        # ==========================
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        # Smooth rectangle radius (15% of box height instead of 50%)
        corner_radius = max(8, int(box_h * 0.15))

        overlay_draw.rounded_rectangle(
            [box_x, box_y, box_x + box_w, box_y + box_h],
            radius=corner_radius,
            fill=(255, 255, 255, 250),
            outline=(255, 255, 255, 80),
            width=2
        )

        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # ==========================
        # Center text
        # ==========================
        text_x = box_x + (box_w - text_w) // 2
        text_y = box_y + (box_h - text_h) // 2

        # Optional subtle shadow
        draw.text(
            (text_x + 2, text_y + 2),
            text,
            font=font,
            fill=(255, 255, 255, 120)
        )

        draw.text(
            (text_x, text_y),
            text,
            font=font,
            fill=(0, 0, 0, 255)
        )

        # ==========================
        # Save
        # ==========================
        file_name_without_ext = os.path.splitext(file)[0]
        out_path = os.path.join("output_images", f"{file_name_without_ext}.png")
        
        # Convert back to RGB to save as PNG properly without alpha issues in some viewers
        img.save(out_path)
        print(f"✅ Processed: {file_name_without_ext}")

print("✅ All images processed and saved in 'output_images' folder.")