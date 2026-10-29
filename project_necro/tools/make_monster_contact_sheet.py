# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC_DIR = r"D:\workspace\GEMINI\project2100\assets\monsters"
OUT_DIR = r"D:\workspace\GEMINI\project_necro\tools"

files = sorted([f for f in os.listdir(SRC_DIR) if f.endswith(".png")])
cols = 12
rows = (len(files) + cols - 1) // cols
cw, ch = 120, 140
sheet = Image.new("RGBA", (cols * cw, rows * ch), (20, 20, 25, 255))
draw = ImageDraw.Draw(sheet)

for idx, fn in enumerate(files):
    c = idx % cols
    r = idx // cols
    im = Image.open(os.path.join(SRC_DIR, fn)).convert("RGBA")
    im.thumbnail((100, 100), Image.Resampling.LANCZOS)
    x = c * cw + (cw - im.width) // 2
    y = r * ch + 22
    sheet.alpha_composite(im, (x, y))
    draw.text((c * cw + 6, r * ch + 4), fn.replace(".png", ""), fill=(255, 220, 0, 255))

out_path = os.path.join(OUT_DIR, "contact_sheet_84_monsters.png")
sheet.save(out_path)
print("Saved contact sheet:", out_path)
