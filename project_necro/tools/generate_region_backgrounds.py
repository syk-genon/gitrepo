# -*- coding: utf-8 -*-
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

REGIONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\ui\regions"
os.makedirs(REGIONS_DIR, exist_ok=True)

BASE_TOWNS = {
    1: Image.open(os.path.join(REGIONS_DIR, "town_bg_1.png")).convert("RGBA"),
    2: Image.open(os.path.join(REGIONS_DIR, "town_bg_2.png")).convert("RGBA"),
    3: Image.open(os.path.join(REGIONS_DIR, "town_bg_3.png")).convert("RGBA"),
}
BASE_BATTLES = {
    1: Image.open(os.path.join(REGIONS_DIR, "battle_bg_1.png")).convert("RGBA"),
    2: Image.open(os.path.join(REGIONS_DIR, "battle_bg_2.png")).convert("RGBA"),
    3: Image.open(os.path.join(REGIONS_DIR, "battle_bg_3.png")).convert("RGBA"),
}


def clamp(v):
    return max(0, min(255, int(v)))


def tint_and_grade(img, r_mul, g_mul, b_mul, r_add=0, g_add=0, b_add=0, contrast=1.08, flip_x=False):
    work = img.copy()
    if flip_x:
        work = work.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    work = ImageEnhance.Contrast(work).enhance(contrast)
    # Resize down to pixel-art resolution (320x180) to grade fast, then upscale to 640x360 with NEAREST for crisp retro pixel art
    small = work.resize((320, 180), Image.Resampling.NEAREST)
    px = small.load()
    for y in range(180):
        for x in range(320):
            r, g, b, a = px[x, y]
            nr = clamp(r * r_mul + r_add)
            ng = clamp(g * g_mul + g_add)
            nb = clamp(b * b_mul + b_add)
            px[x, y] = (nr, ng, nb, a)
    return small


def draw_pixel_decorations(small_img, region_id, is_battle):
    d = ImageDraw.Draw(small_img)
    w, h = small_img.size  # 320 x 180
    random.seed(region_id * 100 + (1 if is_battle else 0))

    if region_id == 1:
        # Seoul Subway Labyrinth & Euljiro Forge: toxic green/emerald runes & subway iron beams
        for x in range(20, w, 60):
            d.rectangle([x, 0, x + 6, 42], fill=(28, 36, 34, 230), outline=(10, 12, 12, 255))
        for _ in range(18):
            rx, ry = random.randint(10, w - 10), random.randint(20, h - 25)
            d.rectangle([rx, ry, rx + 2, ry + 2], fill=(0, 255, 170, 210))
    elif region_id == 2:
        # Bukhansan Silver Gate Sanctuary: silver-blue sacred pillars & floating silver runes
        for x in [45, 160, 275]:
            d.polygon([(x, 12), (x + 8, 26), (x, 40), (x - 8, 26)], fill=(180, 240, 255, 220), outline=(20, 45, 70, 255))
        for _ in range(24):
            rx, ry = random.randint(8, w - 8), random.randint(10, h - 20)
            d.rectangle([rx, ry, rx + 2, ry + 2], fill=(160, 235, 255, 220))
    elif region_id == 3:
        # Incheon Port Harbor Night & Black Market: amber crane lights & sea fog
        d.rectangle([0, h - 28, w, h], fill=(12, 32, 48, 160))
        for x in range(18, w, 48):
            d.ellipse([x - 4, 18, x + 4, 26], fill=(255, 190, 60, 240))
    elif region_id == 4:
        # Seoraksan Daecheongbong Snow Peak: blizzard snow & cyan sword aura peaks
        for _ in range(45):
            rx, ry = random.randint(4, w - 4), random.randint(4, h - 10)
            d.rectangle([rx, ry, rx + 2, ry + 2], fill=(235, 250, 255, 240))
        if is_battle:
            for sx in [70, 160, 250]:
                d.line([(sx, 15), (sx - 12, 135)], fill=(0, 240, 255, 180), width=2)
    elif region_id == 5:
        # DMZ & Pyongyang 50m Underground Bunker: hazard stripes & red emergency beacons
        for x in range(0, w, 24):
            d.polygon([(x, 0), (x + 12, 0), (x + 4, 10), (x - 8, 10)], fill=(230, 170, 20, 235))
        for x in [55, 160, 265]:
            d.ellipse([x - 5, 14, x + 5, 24], fill=(255, 40, 60, 240))
    elif region_id == 6:
        # Tokyo Onmyoji Main Shrine: crimson torii & purple shikigami talismans
        for _ in range(14):
            rx, ry = random.randint(20, w - 20), random.randint(15, h - 40)
            d.rectangle([rx, ry, rx + 5, ry + 9], fill=(245, 230, 190, 230), outline=(180, 30, 60, 255))
    elif region_id == 7:
        # Macau VIP Casino Night: neon gold & magenta casino lights
        for x in range(16, w - 16, 28):
            col = (255, 210, 0, 245) if (x // 28) % 2 == 0 else (255, 42, 109, 245)
            d.rectangle([x, 12, x + 6, 18], fill=col)
    elif region_id == 8:
        # Vladivostok Subsea Fortress: deep abyssal cyan & ice pipes
        for y in [22, 48]:
            d.line([(0, y), (w, y)], fill=(60, 140, 180, 190), width=3)
        for _ in range(25):
            rx, ry = random.randint(10, w - 10), random.randint(15, h - 20)
            d.ellipse([rx, ry, rx + 4, ry + 4], outline=(140, 240, 255, 200))
    elif region_id == 9:
        # Pacific Abyssal Trench Gate: bioluminescent jellyfish/spores & deep water beams
        for x in [60, 140, 230]:
            d.polygon([(x, 0), (x + 25, 0), (x + 55, h), (x - 10, h)], fill=(0, 220, 200, 38))
        for _ in range(28):
            rx, ry = random.randint(8, w - 8), random.randint(10, h - 15)
            d.rectangle([rx, ry, rx + 3, ry + 3], fill=(0, 255, 210, 230))
    elif region_id == 10:
        # Himalaya Ancient Dragon Graveyard: giant dragon ribcage silhouettes & frost souls
        if is_battle:
            for i in range(4):
                bx = 45 + i * 70
                d.arc([bx - 30, 20, bx + 40, 160], start=190, end=350, fill=(210, 225, 240, 215), width=4)
        for _ in range(30):
            rx, ry = random.randint(5, w - 5), random.randint(10, h - 20)
            d.rectangle([rx, ry, rx + 2, ry + 2], fill=(120, 220, 255, 235))
    elif region_id == 11:
        # Siberia & Taklamakan Glass Desert: golden sandstorm & scorching sun/mirage
        d.ellipse([240, 16, 284, 60], fill=(255, 210, 90, 220), outline=(255, 120, 30, 240))
        for _ in range(35):
            rx, ry = random.randint(5, w - 5), random.randint(20, h - 15)
            d.line([(rx, ry), (rx + 8, ry + 2)], fill=(255, 215, 120, 190), width=1)
    elif region_id == 12:
        # Rhine River & Rocky Mountains Magma: volcanic ash, lava cracks & crimson sky
        d.rectangle([0, h - 18, w, h], fill=(220, 55, 15, 165))
        for _ in range(32):
            rx, ry = random.randint(8, w - 8), random.randint(12, h - 12)
            d.rectangle([rx, ry, rx + 3, ry + 3], fill=(255, 120, 20, 240))
    elif region_id == 13:
        # Stratosphere Gold Gate Mothership: golden alien energy grid & orbital beams
        for x in range(30, w, 65):
            d.line([(x, 0), (x, h)], fill=(255, 215, 0, 75), width=2)
        for y in range(25, h, 45):
            d.line([(0, y), (w, y)], fill=(0, 240, 255, 65), width=1)
    elif region_id == 14:
        # 2070 Stratosphere Diamond Gate Throne: cosmic prism stars & dimensional rift lightning
        for _ in range(40):
            rx, ry = random.randint(6, w - 6), random.randint(6, h - 16)
            col = (255, 42, 109, 240) if random.random() < 0.5 else (0, 240, 255, 240)
            d.rectangle([rx, ry, rx + 2, ry + 2], fill=col)
        d.polygon([(160, 8), (176, 36), (160, 64), (144, 36)], fill=(255, 230, 250, 210), outline=(255, 42, 109, 255))

    return small_img.resize((640, 360), Image.Resampling.NEAREST)


REGION_THEMES = {
    1:  {"base": 1, "r": 0.85, "g": 1.15, "b": 0.95, "ra": 0,   "ga": 18,  "ba": 10,  "flip": False},
    2:  {"base": 2, "r": 0.82, "g": 1.05, "b": 1.32, "ra": 5,   "ga": 15,  "ba": 35,  "flip": False},
    3:  {"base": 3, "r": 1.15, "g": 0.98, "b": 0.82, "ra": 18,  "ga": 8,   "ba": -5,  "flip": False},
    4:  {"base": 1, "r": 0.88, "g": 1.18, "b": 1.42, "ra": 25,  "ga": 35,  "ba": 55,  "flip": True},
    5:  {"base": 2, "r": 1.12, "g": 0.92, "b": 0.78, "ra": 15,  "ga": 5,   "ba": -10, "flip": True},
    6:  {"base": 3, "r": 1.25, "g": 0.78, "b": 1.15, "ra": 25,  "ga": -10, "ba": 20,  "flip": True},
    7:  {"base": 2, "r": 1.32, "g": 1.05, "b": 0.75, "ra": 30,  "ga": 12,  "ba": -10, "flip": False},
    8:  {"base": 1, "r": 0.72, "g": 1.08, "b": 1.35, "ra": -10, "ga": 15,  "ba": 40,  "flip": False},
    9:  {"base": 3, "r": 0.65, "g": 1.15, "b": 1.38, "ra": -15, "ga": 20,  "ba": 45,  "flip": False},
    10: {"base": 1, "r": 0.95, "g": 1.08, "b": 1.30, "ra": 15,  "ga": 20,  "ba": 40,  "flip": True},
    11: {"base": 2, "r": 1.38, "g": 1.12, "b": 0.68, "ra": 38,  "ga": 18,  "ba": -25, "flip": True},
    12: {"base": 3, "r": 1.45, "g": 0.75, "b": 0.65, "ra": 45,  "ga": -12, "ba": -20, "flip": True},
    13: {"base": 3, "r": 1.28, "g": 1.18, "b": 0.85, "ra": 28,  "ga": 22,  "ba": 0,   "flip": False},
    14: {"base": 2, "r": 1.25, "g": 0.82, "b": 1.42, "ra": 25,  "ga": -5,  "ba": 45,  "flip": False},
}

if __name__ == "__main__":
    for r_id, cfg in REGION_THEMES.items():
        # Keep original 1,2,3 or enrich all 1..14 so every region has town_bg_{r_id}.png and battle_bg_{r_id}.png
        t_base = BASE_TOWNS[cfg["base"]]
        b_base = BASE_BATTLES[cfg["base"]]

        if r_id > 3:
            t_small = tint_and_grade(t_base, cfg["r"], cfg["g"], cfg["b"], cfg["ra"], cfg["ga"], cfg["ba"], flip_x=cfg["flip"])
            t_out = draw_pixel_decorations(t_small, r_id, is_battle=False)
            t_path = os.path.join(REGIONS_DIR, f"town_bg_{r_id}.png")
            t_out.save(t_path)

            b_small = tint_and_grade(b_base, cfg["r"], cfg["g"], cfg["b"], cfg["ra"], cfg["ga"], cfg["ba"], flip_x=cfg["flip"])
            b_out = draw_pixel_decorations(b_small, r_id, is_battle=True)
            b_path = os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png")
            b_out.save(b_path)
            print(f"Region {r_id:02d}: generated town_bg_{r_id}.png ({os.path.getsize(t_path):,} B) & battle_bg_{r_id}.png ({os.path.getsize(b_path):,} B)")
        else:
            print(f"Region {r_id:02d}: using master town_bg_{r_id}.png & battle_bg_{r_id}.png")
