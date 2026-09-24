import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# Load Excel file (columns: folder_path, code, text)
df = pd.read_excel("WORK.xlsx")

# Font setup
font_path = "arial.ttf"

# Output folder
os.makedirs("output_images", exist_ok=True)

for idx, row in df.iterrows():

    folder = row['folder_path']
    code = str(row['code'])
    text = str(row['text'])

    # Find matching files
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

    W, H = img.size
    base = min(W, H)

    draw = ImageDraw.Draw(img)

    # ==========================
    # Dynamic starting font size
    # ==========================

    font_size = max(40, min(int(base * 0.06), 180))

    # ==========================
    # Auto-fit font
    # ==========================

    while font_size > 20:

        font = ImageFont.truetype(font_path, font_size)

        bbox = draw.textbbox((0, 0), text, font=font)

        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Prevent text from becoming too wide
        if text_w <= W * 0.80:
            break

        font_size -= 2

    # ==========================
    # Rectangle size from text
    # ==========================

    padding_x = max(20, int(text_w * 0.08))
    padding_y = max(10, int(text_h * 0.35))

    box_w = text_w + (padding_x * 2)
    box_h = text_h + (padding_y * 2)

    # ==========================
    # Positioning
    # ==========================

    bottom_margin = max(20, int(H * 0.03))

    box_x = (W - box_w) // 2
    box_y = H - box_h - bottom_margin

    # ==========================
    # Transparent rectangle overlay
    # ==========================

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    overlay_draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
		radius=int(box_h * 0.25),
        fill=(255, 255, 255, 80)  # Transparency
    )

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # ==========================
    # Center text in rectangle
    # ==========================

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