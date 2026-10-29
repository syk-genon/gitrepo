import os
import math
from PIL import Image, ImageDraw

vfx_dir = r"C:\Users\exbxda13\project2100\assets\pixel_vfx"
os.makedirs(vfx_dir, exist_ok=True)

# 1. VFX Slash Arc (80x80)
im_slash = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
d = ImageDraw.Draw(im_slash)
# Giant Crescent Wave
for deg in range(10, 160, 2):
    rad = math.radians(deg)
    r = 32
    cx = 40 + int(r * math.cos(rad))
    cy = 40 - int(r * math.sin(rad))
    d.line([(cx-2, cy-1), (cx+3, cy+3)], fill=(0, 240, 255, 230), width=3)
    d.line([(cx-1, cy), (cx+1, cy+1)], fill=(255, 255, 255, 255), width=2)
# Trailing kinetic sparks
for i in range(12):
    sx = 25 + (i * 3)
    sy = 30 + (i * 2)
    d.point((sx, sy), fill=(180, 255, 255, 255))
im_slash.save(os.path.join(vfx_dir, "vfx_slash_arc.png"))

# 2. VFX Axe Spin (64x64)
im_axe = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
d = ImageDraw.Draw(im_axe)
# Whirling circle of orange/yellow wind
for deg in range(0, 360, 10):
    rad = math.radians(deg)
    r = 24
    cx = 32 + int(r * math.cos(rad))
    cy = 32 + int(r * math.sin(rad))
    d.line([(cx-1, cy), (cx+2, cy+1)], fill=(255, 140, 30, 180), width=2)
# Heavy steel double-bladed axe in center
d.line([(18, 18), (46, 46)], fill=(120, 60, 30, 255), width=3) # Handle
# Blades
d.polygon([(16, 20), (12, 10), (24, 14), (20, 24)], fill=(200, 210, 225, 255), outline=(30, 35, 45, 255))
d.polygon([(44, 48), (48, 58), (36, 54), (40, 44)], fill=(200, 210, 225, 255), outline=(30, 35, 45, 255))
# Glowing blade tips
d.point((12, 10), fill=(255, 255, 255, 255))
d.point((48, 58), fill=(255, 255, 255, 255))
im_axe.save(os.path.join(vfx_dir, "vfx_axe_spin.png"))

# 3. VFX Laser Bolt (64x32)
im_laser = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(im_laser)
# Horizontal high-tech plasma bolt
d.line([(8, 16), (56, 16)], fill=(255, 255, 255, 255), width=3)
d.line([(4, 16), (58, 16)], fill=(0, 240, 255, 200), width=6)
d.line([(2, 16), (62, 16)], fill=(180, 40, 255, 120), width=10)
# Arrow head tip
d.polygon([(54, 8), (62, 16), (54, 24)], fill=(255, 255, 255, 255))
im_laser.save(os.path.join(vfx_dir, "vfx_laser_bolt.png"))

# 4. VFX Hit Impact Burst (64x64)
im_hit = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
d = ImageDraw.Draw(im_hit)
# 16-Bit Arcade 8-pointed star burst
cx, cy = 32, 32
# Core diamond
d.polygon([(cx-8, cy), (cx, cy-8), (cx+8, cy), (cx, cy+8)], fill=(255, 255, 255, 255))
# 4 Cardinal rays
d.polygon([(cx-2, cy-6), (cx, cy-28), (cx+2, cy-6)], fill=(255, 240, 60, 255))
d.polygon([(cx-2, cy+6), (cx, cy+28), (cx+2, cy+6)], fill=(255, 240, 60, 255))
d.polygon([(cx-6, cy-2), (cx-28, cy), (cx-6, cy+2)], fill=(255, 240, 60, 255))
d.polygon([(cx+6, cy-2), (cx+28, cy), (cx+6, cy+2)], fill=(255, 240, 60, 255))
# 4 Diagonal sparks
d.line([(cx-18, cy-18), (cx+18, cy+18)], fill=(255, 100, 30, 255), width=2)
d.line([(cx+18, cy-18), (cx-18, cy+18)], fill=(255, 100, 30, 255), width=2)
im_hit.save(os.path.join(vfx_dir, "vfx_hit_burst.png"))

# 5. VFX Nemesis Demonic Slash (80x80)
im_nem_vfx = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
d = ImageDraw.Draw(im_nem_vfx)
for deg in range(15, 160, 2):
    rad = math.radians(deg)
    r = 34
    cx = 40 + int(r * math.cos(rad))
    cy = 40 - int(r * math.sin(rad))
    d.line([(cx-3, cy-2), (cx+4, cy+4)], fill=(160, 20, 220, 230), width=4)
    d.line([(cx-1, cy), (cx+2, cy+2)], fill=(255, 30, 80, 255), width=2)
    d.point((cx, cy), fill=(255, 255, 255, 255))
im_nem_vfx.save(os.path.join(vfx_dir, "vfx_nemesis_burst.png"))

print("All 16-bit arcade VFX sprites rendered successfully!")
