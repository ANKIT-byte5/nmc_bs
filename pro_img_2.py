import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# Load Excel file (columns: 'folder_path', 'code', 'text')
df = pd.read_excel("WORK.xlsx")

# Font setup
font_path = "arial.ttf"
font_size = 40
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

    for file in matched_files:
        img_path = os.path.join(folder, file)

        # Open image
        img = Image.open(img_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # Get image size
        W, H = img.size

        # Calculate text size
        # Calculate text size (new Pillow versions)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]


        # Coordinates for centered box
        box_w, box_h = text_w + 40, text_h + 40
        box_x, box_y = (W - box_w) // 2, (H - box_h) // 2

        # Draw rectangle (semi-transparent background)
        draw.rectangle(
            [box_x, box_y, box_x + box_w, box_y + box_h],
            fill=(0, 0, 0, 150)
        )

        # Draw text centered
        text_x = (W - text_w) // 2
        text_y = (H - text_h) // 2
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

        # Save output
        out_path = os.path.join("output_images", f"output_{idx}_{file}.png")
        img.save(out_path)

print("✅ All images processed and saved in 'output_images' folder.")
