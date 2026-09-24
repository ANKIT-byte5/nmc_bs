import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# Load Excel file (columns: 'folder_path', 'code', 'text')
df = pd.read_excel("WORK.xlsx")

# Font setup
font_path = "arial.ttf"

# Output folder
os.makedirs("output_images", exist_ok=True)

for idx, row in df.iterrows():
    folder = row['folder_path']
    code = str(row['code'])
    text = str(row['text'])

    # Find matching files in folder
    matched_files = [
        f for f in os.listdir(folder)
        if f.startswith(code)
    ]

    if not matched_files:
        print(f"⚠️ No file found for code {code} in {folder}")
        continue

    # Pick latest file
    matched_files.sort(
        key=lambda f: os.path.getmtime(os.path.join(folder, f)),
        reverse=True
    )

    file = matched_files[0]
    img_path = os.path.join(folder, file)

    # Open image
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Image size
    W, H = img.size

    # ==========================
    # Dynamic scaling section
    # ==========================

    base = min(W, H)

    # Font size scales with image
    font_size = max(40, min(int(base * 0.06), 180))

    # Box size scales with image
    box_w = int(W * 0.70)

    box_h = max(80, min(int(base * 0.10), 250))

    # Bottom margin scales too
    bottom_margin = max(20, int(H * 0.03))

    # Position (bottom center)
    box_x = (W - box_w) // 2
    box_y = H - box_h - bottom_margin

    # ==========================
    # Auto-fit font
    # ==========================

    while font_size > 20:
        font = ImageFont.truetype(font_path, font_size)

        bbox = draw.textbbox((0, 0), text, font=font)

        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Leave small padding inside box
        if text_w <= box_w * 0.90 and text_h <= box_h * 0.85:
            break

        font_size -= 2

    # Draw rectangle
    draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        fill=(255, 255, 255, 200)
    )

    # Recalculate final text size
    bbox = draw.textbbox((0, 0), text, font=font)

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Center text in box
    text_x = box_x + (box_w - text_w) // 2
    text_y = box_y + (box_h - text_h) // 2

    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=(0, 0, 0, 255)
    )

    # Save output
    out_path = os.path.join(
        "output_images",
        f"output_{idx}_{file}.png"
    )

    img.save(out_path)

print("✅ All images processed and saved in 'output_images' folder.")