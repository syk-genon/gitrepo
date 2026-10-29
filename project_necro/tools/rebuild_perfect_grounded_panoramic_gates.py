# -*- coding: utf-8 -*-
import os, sys
from collections import deque
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

ARTIFACT_DIR = r"C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f"
REGIONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\ui\regions"
os.makedirs(REGIONS_DIR, exist_ok=True)

SHEET_BG_A = os.path.join(ARTIFACT_DIR, "retro_nature_battle_backgrounds_2x2_1793171611199.jpg")
SHEET_BG_B = os.path.join(ARTIFACT_DIR, "retro_nature_battle_backgrounds_2x2_1793171659027.jpg")
SHEET_PROPS = os.path.join(ARTIFACT_DIR, "pixel_nature_props_3x3_1793171607052.jpg")

# 1. Clean Crop Sheet A (no borders)
im_a = Image.open(SHEET_BG_A).convert("RGBA")
wa, ha = im_a.size
hwa, hha = wa // 2, ha // 2
bg_cavern = im_a.crop((0, 0, hwa, hha)).resize((640, 360), Image.Resampling.LANCZOS)
bg_forest = im_a.crop((hwa, 0, wa, hha)).resize((640, 360), Image.Resampling.LANCZOS)
bg_coastal = im_a.crop((0, hha, hwa, ha)).resize((640, 360), Image.Resampling.LANCZOS)
bg_alpine = im_a.crop((hwa, hha, wa, ha)).resize((640, 360), Image.Resampling.LANCZOS)

# 2. Clean Border-Free Crop Sheet B (completely inside inner frame, 0 black lines, 0 text)
im_b = Image.open(SHEET_BG_B).convert("RGBA")
bg_ocean = im_b.crop((88, 79, 671, 386)).resize((640, 360), Image.Resampling.LANCZOS)
bg_glacier = im_b.crop((704, 79, 1287, 386)).resize((640, 360), Image.Resampling.LANCZOS)
bg_desert = im_b.crop((88, 443, 671, 732)).resize((640, 360), Image.Resampling.LANCZOS)
bg_magma = im_b.crop((704, 443, 1287, 732)).resize((640, 360), Image.Resampling.LANCZOS)

print("1. Cleanly extracted 8 border-free nature battle plates.")

# 3. Thorough Background Removal with BFS + Defringe on 9 Props
def clean_prop_thorough(cell):
    rgba = cell.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    visited = [[False] * w for _ in range(h)]
    q = deque()

    # Seed from all 4 borders for any off-white / light grey
    for x in range(w):
        for y in (0, h - 1):
            r, g, b, _ = px[x, y]
            if r > 208 and g > 208 and b > 208 and max(r, g, b) - min(r, g, b) < 32:
                visited[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visited[y][x]:
                r, g, b, _ = px[x, y]
                if r > 208 and g > 208 and b > 208 and max(r, g, b) - min(r, g, b) < 32:
                    visited[y][x] = True
                    q.append((x, y))

    while q:
        cx, cy = q.popleft()
        px[cx, cy] = (0, 0, 0, 0)
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                r, g, b, a = px[nx, ny]
                if a > 0 and r > 200 and g > 200 and b > 200 and max(r, g, b) - min(r, g, b) < 36:
                    visited[ny][nx] = True
                    q.append((nx, ny))

    # Defringe: any non-transparent pixel touching transparency that is light grayish/white
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r > 195 and g > 195 and b > 195 and max(r, g, b) - min(r, g, b) < 26:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    if 0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3] == 0:
                        px[x, y] = (0, 0, 0, 0)
                        break

    alpha = rgba.split()[3]
    bbox = alpha.getbbox()
    return rgba.crop(bbox) if bbox else rgba

def resize_prop(rgba, max_w, max_h):
    ratio = min(max_w / max(1, rgba.width), max_h / max(1, rgba.height))
    nw = max(1, int(rgba.width * ratio))
    nh = max(1, int(rgba.height * ratio))
    return rgba.resize((nw, nh), Image.Resampling.LANCZOS)

im_p = Image.open(SHEET_PROPS).convert("RGBA")
pw, ph = im_p.size
cw, ch = pw // 3, ph // 3

# Ground Props: (sitting firmly on the ground)
prop_mushrooms    = resize_prop(clean_prop_thorough(im_p.crop((0, 0, cw, ch))), 165, 160)
prop_ancient_root = resize_prop(clean_prop_thorough(im_p.crop((cw, 0, cw * 2, ch))), 175, 175)
prop_coastal_rock = resize_prop(clean_prop_thorough(im_p.crop((cw * 2, 0, pw, ch))), 180, 165)
prop_bamboo_maple = resize_prop(clean_prop_thorough(im_p.crop((cw, ch, cw * 2, ch * 2))), 170, 180)
prop_jungle_ferns = resize_prop(clean_prop_thorough(im_p.crop((cw * 2, ch, pw, ch * 2))), 175, 170)
prop_ocean_coral  = resize_prop(clean_prop_thorough(im_p.crop((0, ch * 2, cw, ph))), 165, 160)
prop_volcano_rock = resize_prop(clean_prop_thorough(im_p.crop((cw, ch * 2, cw * 2, ph))), 175, 170)
prop_raw_crystals = resize_prop(clean_prop_thorough(im_p.crop((cw * 2, ch * 2, pw, ph))), 175, 175)

# Canopy Props: (hanging from the top ceiling!)
prop_snow_branch  = resize_prop(clean_prop_thorough(im_p.crop((0, ch, cw, ch * 2))), 185, 175)

print("2. Thoroughly cleaned all props with zero white fringe.")

# 4. Define 14 Nature Regions with Ground Props and Canopy Props
NATURE_REGION_MAP = {
    1:  {"bg1": bg_cavern,  "bg2": bg_cavern,  "ground": prop_mushrooms,    "canopy": None,             "tint": (0.92, 1.10, 1.15)},
    2:  {"bg1": bg_forest,  "bg2": bg_forest,  "ground": prop_ancient_root, "canopy": None,             "tint": (1.00, 1.05, 0.95)},
    3:  {"bg1": bg_coastal, "bg2": bg_coastal, "ground": prop_coastal_rock, "canopy": None,             "tint": (0.95, 1.00, 1.05)},
    4:  {"bg1": bg_alpine,  "bg2": bg_glacier, "ground": prop_coastal_rock, "canopy": prop_snow_branch, "tint": (0.92, 1.05, 1.15)},
    5:  {"bg1": bg_cavern,  "bg2": bg_cavern,  "ground": prop_mushrooms,    "canopy": None,             "tint": (1.10, 0.95, 0.90)},
    6:  {"bg1": bg_forest,  "bg2": bg_forest,  "ground": prop_bamboo_maple, "canopy": None,             "tint": (1.10, 0.95, 0.95)},
    7:  {"bg1": bg_forest,  "bg2": bg_desert,  "ground": prop_jungle_ferns, "canopy": None,             "tint": (1.05, 1.10, 0.90)},
    8:  {"bg1": bg_alpine,  "bg2": bg_glacier, "ground": prop_raw_crystals, "canopy": prop_snow_branch, "tint": (0.85, 1.05, 1.25)},
    9:  {"bg1": bg_ocean,   "bg2": bg_ocean,   "ground": prop_ocean_coral,  "canopy": None,             "tint": (0.85, 1.10, 1.25)},
    10: {"bg1": bg_glacier, "bg2": bg_alpine,  "ground": prop_raw_crystals, "canopy": prop_snow_branch, "tint": (0.95, 1.08, 1.20)},
    11: {"bg1": bg_desert,  "bg2": bg_desert,  "ground": prop_coastal_rock, "canopy": None,             "tint": (1.15, 1.00, 0.85)},
    12: {"bg1": bg_magma,   "bg2": bg_magma,   "ground": prop_volcano_rock, "canopy": None,             "tint": (1.20, 0.90, 0.80)},
    13: {"bg1": bg_alpine,  "bg2": bg_ocean,   "ground": prop_raw_crystals, "canopy": None,             "tint": (1.05, 1.00, 1.15)},
    14: {"bg1": bg_cavern,  "bg2": bg_magma,   "ground": prop_raw_crystals, "canopy": None,             "tint": (1.10, 1.05, 1.25)},
}

PANO_W = 2400
PANO_H = 360

for r_id in range(1, 15):
    cfg = NATURE_REGION_MAP[r_id]
    b1 = cfg["bg1"].copy()
    b2 = cfg["bg2"].copy()
    rm, gm, bm = cfg["tint"]

    def apply_tint(im):
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                px[x, y] = (min(255, int(r * rm)), min(255, int(g * gm)), min(255, int(b * bm)), a)
        return im

    b1 = apply_tint(b1)
    b2 = apply_tint(b2)
    b1_flipped = b1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    b2_flipped = b2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    # Seamless horizontal panoramic nature background
    pano_bg = Image.new("RGBA", (PANO_W, PANO_H))
    pano_bg.paste(b1, (0, 0))
    pano_bg.paste(b1_flipped, (600, 0))
    pano_bg.paste(b2, (1200, 0))
    pano_bg.paste(b2_flipped, (1800, 0))
    pano_bg.save(os.path.join(REGIONS_DIR, f"battle_pano_{r_id}.png"))

    # Also update battle_bg_{r_id}.png snapshot
    b1.save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png"))
    for f in range(4):
        b1.save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}_f{f}.png"))

    # 5. Build Grounded Panoramic Props (firmly grounded at y = PANO_H - prop.height, ZERO floating!)
    pano_props = Image.new("RGBA", (PANO_W, PANO_H), (0, 0, 0, 0))
    g_prop = cfg["ground"]
    g_flip = g_prop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    canopy_prop = cfg["canopy"]

    # Place Ground Props firmly anchored on the floor across the 6 battle zones
    # Ground Y is anchored directly to the bottom (y = PANO_H - h) so rocks and roots never float!
    ground_xs = [16, 420, 820, 1220, 1640, 2060]
    for i, gx in enumerate(ground_xs):
        p_to_use = g_flip if i % 2 == 1 else g_prop
        gy = PANO_H - p_to_use.height  # Flush with bottom floor!
        pano_props.alpha_composite(p_to_use, (gx, gy))

    # Place Canopy Props hanging from the top ceiling (y = 0) if applicable!
    if canopy_prop:
        canopy_flip = canopy_prop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        canopy_xs = [0, 480, 960, 1440, 1920]
        for i, cx in enumerate(canopy_xs):
            c_to_use = canopy_flip if i % 2 == 1 else canopy_prop
            pano_props.alpha_composite(c_to_use, (cx, 0))  # Flush with ceiling!

    pano_props.save(os.path.join(REGIONS_DIR, f"nature_props_pano_{r_id}.png"))

    # Fallback snapshot
    for f in range(4):
        c_crop = pano_props.crop((0, 0, 640, 360))
        c_crop.save(os.path.join(REGIONS_DIR, f"region_obj_{r_id}_f{f}.png"))

print("3. Successfully rebuilt all 14 panoramic battle grounds and grounded props!")

# 6. Update display.html to remove lifting transform from ground objects
HTML_PATH = r"D:\workspace\GEMINI\project_necro\display.html"
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Replace propSmoothFloat with grounded subtle sway that stays anchored at the bottom
old_anim_def = """        @keyframes propSmoothFloat {
            0% { transform: translateY(0); }
            100% { transform: translateY(-3.5px); }
        }"""

new_anim_def = """        /* 지면 오브젝트가 붕 뜨지 않고 바닥에 고정된 채 자연스럽게 숨쉬는 모션 */
        @keyframes propGroundedBreath {
            0% { transform: scale(1.0) translateY(0); opacity: 0.95; }
            50% { transform: scale(1.006) translateY(0); opacity: 1; }
            100% { transform: scale(1.0) translateY(0); opacity: 0.95; }
        }"""

if old_anim_def in html:
    html = html.replace(old_anim_def, new_anim_def, 1)

html = html.replace("animation: propSmoothFloat 1.8s ease-in-out infinite alternate;", "animation: propGroundedBreath 2.6s ease-in-out infinite alternate; transform-origin: bottom center;")

# Update cache buster to v=6
html = html.replace("?v=5", "?v=6").replace("?v=4", "?v=6")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("4. Updated display.html: grounded breath animation applied, translateY lifting removed!")

# 7. Update display.js cache busters to ?v=6
JS_PATH = r"D:\workspace\GEMINI\project_necro\display.js"
with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()
js = js.replace("?v=5", "?v=6").replace("?v=4", "?v=6")
with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js)
print("5. Updated display.js with cache buster ?v=6.")
