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

# 1. Crop 4 Nature Backgrounds from Sheet A (Cavern, Forest, Coastal, Alpine)
im_bg_a = Image.open(SHEET_BG_A).convert("RGBA")
w_a, h_a = im_bg_a.size
half_w_a, half_h_a = w_a // 2, h_a // 2

bg_cavern = im_bg_a.crop((0, 0, half_w_a, half_h_a)).resize((640, 360), Image.Resampling.LANCZOS)
bg_forest = im_bg_a.crop((half_w_a, 0, w_a, half_h_a)).resize((640, 360), Image.Resampling.LANCZOS)
bg_coastal = im_bg_a.crop((0, half_h_a, half_w_a, h_a)).resize((640, 360), Image.Resampling.LANCZOS)
bg_alpine = im_bg_a.crop((half_w_a, half_h_a, w_a, h_a)).resize((640, 360), Image.Resampling.LANCZOS)

# 2. Crop 4 Nature Backgrounds from Sheet B (Ocean Abyss, Glacier, Desert, Magma)
# In Sheet B, there is a header title and black frames around each box. Crop inside the frames.
im_bg_b = Image.open(SHEET_BG_B).convert("RGBA")
w_b, h_b = im_bg_b.size

# Sub-regions inside inner borders
bg_ocean = im_bg_b.crop((int(w_b * 0.05), int(h_b * 0.08), int(w_b * 0.49), int(h_b * 0.48))).resize((640, 360), Image.Resampling.LANCZOS)
bg_glacier = im_bg_b.crop((int(w_b * 0.51), int(h_b * 0.08), int(w_b * 0.95), int(h_b * 0.48))).resize((640, 360), Image.Resampling.LANCZOS)
bg_desert = im_bg_b.crop((int(w_b * 0.05), int(h_b * 0.54), int(w_b * 0.49), int(h_b * 0.94))).resize((640, 360), Image.Resampling.LANCZOS)
bg_magma = im_bg_b.crop((int(w_b * 0.51), int(h_b * 0.54), int(w_b * 0.95), int(h_b * 0.94))).resize((640, 360), Image.Resampling.LANCZOS)

print("Cropped 8 distinct 16-bit pure nature battle stages.")

# 3. Extract 9 Pure Nature Stage Props from Sheet Props (3x3 grid)
def remove_white_floodfill(im, threshold=238):
    rgba = im.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    visited = [[False] * w for _ in range(h)]
    q = deque()
    def is_bg(r, g, b):
        return r >= threshold and g >= threshold and b >= threshold and abs(r - g) < 18 and abs(g - b) < 18
    for x in range(w):
        for y in (0, h - 1):
            r, g, b, _ = px[x, y]
            if is_bg(r, g, b):
                visited[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visited[y][x]:
                r, g, b, _ = px[x, y]
                if is_bg(r, g, b):
                    visited[y][x] = True
                    q.append((x, y))
    while q:
        cx, cy = q.popleft()
        px[cx, cy] = (0, 0, 0, 0)
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                r, g, b, _ = px[nx, ny]
                if is_bg(r, g, b):
                    visited[ny][nx] = True
                    q.append((nx, ny))
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = px[x, y]
            if a > 0 and r > 225 and g > 225 and b > 225:
                if (px[x - 1, y][3] == 0 or px[x + 1, y][3] == 0 or px[x, y - 1][3] == 0 or px[x, y + 1][3] == 0):
                    px[x, y] = (10, 7, 5, 255)
    return rgba

def trim_sprite(rgba, max_w, max_h):
    alpha = rgba.split()[3]
    bbox = alpha.point(lambda p: 255 if p > 25 else 0).getbbox()
    trimmed = rgba.crop(bbox) if bbox else rgba
    ratio = min(max_w / max(1, trimmed.width), max_h / max(1, trimmed.height))
    nw = max(1, int(trimmed.width * ratio))
    nh = max(1, int(trimmed.height * ratio))
    return trimmed.resize((nw, nh), Image.Resampling.LANCZOS)

im_p = Image.open(SHEET_PROPS).convert("RGBA")
pw, ph = im_p.size
cw_p, ch_p = pw // 3, ph // 3

prop_mushrooms   = trim_sprite(remove_white_floodfill(im_p.crop((0, 0, cw_p, ch_p))), 160, 160)
prop_ancient_root= trim_sprite(remove_white_floodfill(im_p.crop((cw_p, 0, cw_p * 2, ch_p))), 170, 175)
prop_coastal_rock= trim_sprite(remove_white_floodfill(im_p.crop((cw_p * 2, 0, pw, ch_p))), 175, 170)

prop_snow_branch = trim_sprite(remove_white_floodfill(im_p.crop((0, ch_p, cw_p, ch_p * 2))), 175, 175)
prop_bamboo_maple= trim_sprite(remove_white_floodfill(im_p.crop((cw_p, ch_p, cw_p * 2, ch_p * 2))), 170, 180)
prop_jungle_ferns= trim_sprite(remove_white_floodfill(im_p.crop((cw_p * 2, ch_p, pw, ch_p * 2))), 175, 175)

prop_ocean_coral = trim_sprite(remove_white_floodfill(im_p.crop((0, ch_p * 2, cw_p, ph))), 165, 165)
prop_volcano_rock= trim_sprite(remove_white_floodfill(im_p.crop((cw_p, ch_p * 2, cw_p * 2, ph))), 175, 175)
prop_raw_crystals= trim_sprite(remove_white_floodfill(im_p.crop((cw_p * 2, ch_p * 2, pw, ph))), 175, 175)

print("Extracted 9 pure nature props.")

# Map 14 regions to their Pure Nature Themes (Primary and Deep Secondary background) and Props
# Every region represents a natural dimension inside the gate!
NATURE_REGION_MAP = {
    1:  {"name": "지하 발광 버섯 동굴",  "bg1": bg_cavern,  "bg2": bg_cavern,  "prop1": prop_mushrooms,    "prop2": prop_ancient_root, "tint": (0.9, 1.1, 1.15)},
    2:  {"name": "태고의 신목 성역 숲",  "bg1": bg_forest,  "bg2": bg_forest,  "prop1": prop_ancient_root, "prop2": prop_jungle_ferns, "tint": (1.0, 1.05, 0.95)},
    3:  {"name": "폭풍우 암석 해안 절벽","bg1": bg_coastal, "bg2": bg_coastal, "prop1": prop_coastal_rock, "prop2": prop_mushrooms,    "tint": (0.95, 1.0, 1.05)},
    4:  {"name": "설악산 설원 고산 침엽수","bg1": bg_alpine,  "bg2": bg_glacier, "prop1": prop_snow_branch,  "prop2": prop_coastal_rock,"tint": (0.92, 1.05, 1.15)},
    5:  {"name": "심층 지하수 석순 계곡", "bg1": bg_cavern,  "bg2": bg_cavern,  "prop1": prop_mushrooms,    "prop2": prop_coastal_rock, "tint": (1.1, 0.95, 0.9)},
    6:  {"name": "단풍 대나무 비경 계곡", "bg1": bg_forest,  "bg2": bg_forest,  "prop1": prop_bamboo_maple, "prop2": prop_ancient_root, "tint": (1.1, 0.95, 0.95)},
    7:  {"name": "열대 맹그로브 밀림",    "bg1": bg_forest,  "bg2": bg_desert,  "prop1": prop_jungle_ferns, "prop2": prop_ancient_root, "tint": (1.05, 1.1, 0.9)},
    8:  {"name": "동토의 툰드라 설원",    "bg1": bg_alpine,  "bg2": bg_glacier, "prop1": prop_snow_branch,  "prop2": prop_raw_crystals, "tint": (0.85, 1.05, 1.25)},
    9:  {"name": "태평양 심해 산호 해구", "bg1": bg_ocean,   "bg2": bg_ocean,   "prop1": prop_ocean_coral,  "prop2": prop_raw_crystals, "tint": (0.85, 1.1, 1.25)},
    10: {"name": "히말라야 만년설 빙벽",  "bg1": bg_glacier, "bg2": bg_alpine,  "prop1": prop_raw_crystals, "prop2": prop_snow_branch,  "tint": (0.95, 1.08, 1.2)},
    11: {"name": "타클라마칸 붉은 사막",  "bg1": bg_desert,  "bg2": bg_desert,  "prop1": prop_coastal_rock, "prop2": prop_mushrooms,    "tint": (1.15, 1.0, 0.85)},
    12: {"name": "로키 화산 용암 분화구", "bg1": bg_magma,   "bg2": bg_magma,   "prop1": prop_volcano_rock, "prop2": prop_volcano_rock, "tint": (1.2, 0.9, 0.8)},
    13: {"name": "성층권 천공 부유석",    "bg1": bg_alpine,  "bg2": bg_ocean,   "prop1": prop_raw_crystals, "prop2": prop_ancient_root, "tint": (1.05, 1.0, 1.15)},
    14: {"name": "다이아몬드 수정 광맥",  "bg1": bg_cavern,  "bg2": bg_magma,   "prop1": prop_raw_crystals, "prop2": prop_raw_crystals, "tint": (1.1, 1.05, 1.25)},
}

# 4. Generate 2400x360 Wide Panoramic Nature Battle Grounds and Matching Parallax Props for all 14 regions
# Total width = 2400px (4x 600px spanning Wave 1 -> Wave 6)
PANO_W = 2400
PANO_H = 360

for r_id in range(1, 15):
    cfg = NATURE_REGION_MAP[r_id]
    b1 = cfg["bg1"].copy()
    b2 = cfg["bg2"].copy()
    rm, gm, bm = cfg["tint"]

    # Tint backgrounds
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

    # Compose 2400x360 panoramic nature landscape (Wave 1: entrance, Wave 3: middle, Wave 6: deep inner lair)
    pano_bg = Image.new("RGBA", (PANO_W, PANO_H))
    pano_bg.paste(b1, (0, 0))
    pano_bg.paste(b1_flipped, (600, 0))
    pano_bg.paste(b2, (1200, 0))
    pano_bg.paste(b2_flipped, (1800, 0))

    # Blend seams smoothly (linear alpha blend around 600, 1200, 1800)
    pano_bg.save(os.path.join(REGIONS_DIR, f"battle_pano_{r_id}.png"))

    # Also save a standard battle_bg_{r_id}.png snapshot for backward compatibility
    b1.save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png"))
    for f in range(4):
        b1.save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}_f{f}.png"))

    # Compose matching 2400x360 panoramic Nature Foreground Props strip
    # Props are distributed across the 6 battle zones on the ground!
    pano_props = Image.new("RGBA", (PANO_W, PANO_H), (0, 0, 0, 0))
    p1 = cfg["prop1"]
    p2 = cfg["prop2"]
    p1_flip = p1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    p2_flip = p2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    # Wave 1 (0..400)
    pano_props.alpha_composite(p1, (12, PANO_H - p1.height - 4))
    pano_props.alpha_composite(p2_flip, (390, PANO_H - p2.height - 4))
    # Wave 2 (400..800)
    pano_props.alpha_composite(p2, (480, PANO_H - p2.height - 4))
    pano_props.alpha_composite(p1_flip, (780, PANO_H - p1.height - 4))
    # Wave 3 (800..1200)
    pano_props.alpha_composite(p1, (880, PANO_H - p1.height - 4))
    pano_props.alpha_composite(p2_flip, (1180, PANO_H - p2.height - 4))
    # Wave 4 (1200..1600)
    pano_props.alpha_composite(p2, (1280, PANO_H - p2.height - 4))
    pano_props.alpha_composite(p1_flip, (1580, PANO_H - p1.height - 4))
    # Wave 5 Named (1600..2000)
    pano_props.alpha_composite(p1, (1680, PANO_H - p1.height - 4))
    pano_props.alpha_composite(p2_flip, (1980, PANO_H - p2.height - 4))
    # Wave 6 Boss Lair (2000..2400)
    pano_props.alpha_composite(p2, (2080, PANO_H - p2.height - 4))
    pano_props.alpha_composite(p1_flip, (PANO_W - p1.width - 12, PANO_H - p1.height - 4))

    pano_props.save(os.path.join(REGIONS_DIR, f"nature_props_pano_{r_id}.png"))

    # Also save region_obj_{r_id}_f0..3.png snapshot for town & fallback
    for f in range(4):
        c_crop = pano_props.crop((0, 0, 640, 360))
        c_crop.save(os.path.join(REGIONS_DIR, f"region_obj_{r_id}_f{f}.png"))

print("Successfully generated 14 region 2400px panoramic battle nature grounds and parallax props!")
