import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# Load Excel file (columns: 'folder_path', 'code', 'text')
df = pd.read_excel("WORK.xlsx")

# Font setup
font_path = "arial.ttf"
font_size = 80
font = ImageFont.truetype(font_path, font_size)

# Output folder
os.makedirs("output_images", exist_ok=True)

for idx, row in df.iterrows():
    folder = row['folder_path']
    code = str(row['code'])
    text = str(row['text'])

    # Find matching files in folder
    matched_files = [f for f in os.listdir(folder) if f.startswith(code)]
    
    if not matched_files:
        print(f"⚠️ No file found for code {code} in {folder}")
        continue

    # Pick the latest file (by modification time)
    matched_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    file = matched_files[0]

    img_path = os.path.join(folder, file)

    # Open image
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Get image size
    W, H = img.size

    # Fixed box size (uniform across all images)
    box_w, box_h = 900, 140  

    # Position options:
    # Bottom-center
    box_x = (W - box_w) // 2
    box_y = H - box_h - 40   # 40px margin from bottom

    # Left-center (alternative)
    # box_x = 40
    # box_y = (H - box_h) // 2

    # Draw rectangle (white background)
    draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        fill=(255, 255, 255, 255)
    )

    # Calculate text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Center text inside box
    text_x = box_x + (box_w - text_w) // 2
    text_y = box_y + (box_h - text_h) // 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 255))

    # Save output
    out_path = os.path.join("output_images", f"output_{idx}_{file}.png")
    img.save(out_path)

print("✅ All images processed and saved in 'output_images' folder.")
