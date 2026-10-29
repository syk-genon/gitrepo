# -*- coding: utf-8 -*-
import os, sys
from collections import deque
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

ARTIFACT_DIR = r"C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f"
NECRO_DIR = r"D:\workspace\GEMINI\project_necro"
GATES_DIR = os.path.join(NECRO_DIR, "assets", "ui", "gates")
REGIONS_DIR = os.path.join(NECRO_DIR, "assets", "ui", "regions")
SUMMONS_DIR = os.path.join(NECRO_DIR, "assets", "summons")

os.makedirs(GATES_DIR, exist_ok=True)
os.makedirs(REGIONS_DIR, exist_ok=True)
os.makedirs(SUMMONS_DIR, exist_ok=True)

GATES_SHEET = os.path.join(ARTIFACT_DIR, "pixel_art_dungeon_portal_gates_1793168262406.jpg")
TREES_SHEET = os.path.join(ARTIFACT_DIR, "retro_pixel_art_spritesheet_1793168250006.jpg")
CLOUDS_SHEET = os.path.join(ARTIFACT_DIR, "pixel_art_clouds_foliage_sprites_1793168237178.jpg")


def remove_white_bg_floodfill(im, threshold=236):
    """
    Removes exterior solid white background (#FFFFFF) using corner/edge BFS floodfill
    so bright interior portal highlights or cloud centers are 100% preserved!
    """
    rgba = im.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    visited = [[False] * w for _ in range(h)]
    q = deque()

    def is_bg_white(r, g, b):
        return r >= threshold and g >= threshold and b >= threshold and abs(r - g) < 18 and abs(g - b) < 18

    # Seed from all 4 borders
    for x in range(w):
        for y in (0, h - 1):
            r, g, b, a = px[x, y]
            if is_bg_white(r, g, b):
                visited[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visited[y][x]:
                r, g, b, a = px[x, y]
                if is_bg_white(r, g, b):
                    visited[y][x] = True
                    q.append((x, y))

    while q:
        cx, cy = q.popleft()
        px[cx, cy] = (0, 0, 0, 0)
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                r, g, b, a = px[nx, ny]
                if is_bg_white(r, g, b):
                    visited[ny][nx] = True
                    q.append((nx, ny))

    # Clean 1px white fringe next to transparent pixels
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = px[x, y]
            if a > 0 and r > 220 and g > 220 and b > 220:
                if (
                    px[x - 1, y][3] == 0
                    or px[x + 1, y][3] == 0
                    or px[x, y - 1][3] == 0
                    or px[x, y + 1][3] == 0
                ):
                    px[x, y] = (10, 7, 5, 255)

    return rgba


def trim_and_pad(rgba, canvas_w=240, canvas_h=240, pad=8, align_bottom=True):
    alpha = rgba.split()[3]
    bbox = alpha.point(lambda p: 255 if p > 20 else 0).getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    tw = canvas_w - pad * 2
    th = canvas_h - pad * 2
    ratio = min(tw / max(1, rgba.width), th / max(1, rgba.height))
    nw = max(1, int(rgba.width * ratio))
    nh = max(1, int(rgba.height * ratio))
    resized = rgba.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    ox = (canvas_w - nw) // 2
    oy = (canvas_h - pad - nh) if align_bottom else (canvas_h - nh) // 2
    canvas.alpha_composite(resized, (ox, oy))
    return canvas


# =====================================================================
# 1. Extract 6 AI-Generated 16-Bit Pixel Art Gates (3x2 grid)
# =====================================================================
gates_im = Image.open(GATES_SHEET).convert("RGBA")
gw, gh = gates_im.size
col_w = gw // 3
row_h = gh // 2

gate_specs = [
    ("gate_iron.png", 0, 0),
    ("gate_bronze.png", 1, 0),
    ("gate_silver.png", 2, 0),
    ("gate_gold.png", 0, 1),
    ("gate_platinum.png", 1, 1),
    ("gate_diamond.png", 2, 1),
]

for fname, cx, cy in gate_specs:
    cell = gates_im.crop((cx * col_w, cy * row_h, (cx + 1) * col_w, (cy + 1) * row_h))
    clean_cell = remove_white_bg_floodfill(cell, threshold=232)
    final_gate = trim_and_pad(clean_cell, 240, 240, pad=6, align_bottom=True)
    final_gate.save(os.path.join(GATES_DIR, fname))
print("1. Extracted 6 AI-generated 16-bit pixel art gates -> assets/ui/gates/gate_*.png")


# =====================================================================
# 2. Extract AI-Generated 16-Bit Pixel Art Clouds -> clouds_strip.png
# =====================================================================
clouds_im = Image.open(CLOUDS_SHEET).convert("RGBA")
cw, ch = clouds_im.size
# Upper half has 4 fluffy pixel-art clouds
upper_clouds = remove_white_bg_floodfill(clouds_im.crop((0, 0, cw, int(ch * 0.48))), threshold=236)

# Resize upper_clouds onto a seamless 640x130 strip
cloud_strip = Image.new("RGBA", (640, 130), (0, 0, 0, 0))
resized_clouds = upper_clouds.resize((620, 120), Image.Resampling.LANCZOS)
cloud_strip.alpha_composite(resized_clouds, (10, 5))
cloud_strip.save(os.path.join(REGIONS_DIR, "clouds_strip.png"))
print("2. Built AI-generated 16-bit pixel art cloud strip -> assets/ui/regions/clouds_strip.png")


# =====================================================================
# 3. Build 4-Frame Swaying AI Pixel-Art Trees, Lanterns, Bushes & Grass Layer
#    (foliage_overlay_f0.png ~ foliage_overlay_f3.png)
# =====================================================================
trees_im = Image.open(TREES_SHEET).convert("RGBA")
tw_s, th_s = trees_im.size
clean_trees_sheet = remove_white_bg_floodfill(trees_im, threshold=235)

# Extract Left Tree (top-left), Right Tree (top-right), Flower Bush (mid-left-2), Grass Tuft (mid-right)
tree_left = trim_and_pad(clean_trees_sheet.crop((0, 0, int(tw_s * 0.48), int(th_s * 0.50))), 170, 175, pad=2, align_bottom=True)
tree_right = trim_and_pad(clean_trees_sheet.crop((int(tw_s * 0.52), 0, tw_s, int(th_s * 0.50))), 170, 175, pad=2, align_bottom=True)
bush_round = trim_and_pad(clean_trees_sheet.crop((0, int(th_s * 0.50), int(tw_s * 0.27), int(th_s * 0.72))), 64, 52, pad=2, align_bottom=True)
bush_flower = trim_and_pad(clean_trees_sheet.crop((int(tw_s * 0.27), int(th_s * 0.50), int(tw_s * 0.50), int(th_s * 0.72))), 64, 52, pad=2, align_bottom=True)
grass_1 = trim_and_pad(clean_trees_sheet.crop((int(tw_s * 0.50), int(th_s * 0.50), int(tw_s * 0.74), int(th_s * 0.72))), 54, 48, pad=2, align_bottom=True)
grass_2 = trim_and_pad(clean_trees_sheet.crop((int(tw_s * 0.74), int(th_s * 0.50), tw_s, int(th_s * 0.72))), 50, 46, pad=2, align_bottom=True)


def shear_top_of_sprite(sprite, max_dx_px, max_dy_px=0, anchor_bottom_ratio=0.72):
    """
    Applies classic retro pixel wind-shear to a tree/bush/grass sprite:
    - The trunk/roots at the bottom (y >= anchor_bottom_ratio * H) stay 100% anchored on the ground!
    - The upper canopy/leaves/lanterns/grass tips bend smoothly in whole pixel steps (max_dx_px).
    """
    w, h = sprite.size
    src = sprite.load()
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dst = out.load()
    anchor_y = int(h * anchor_bottom_ratio)

    for y in range(h):
        if y >= anchor_y:
            dx = 0
            dy = 0
        else:
            t = (anchor_y - y) / max(1.0, float(anchor_y))
            dx = int(round(max_dx_px * t))
            dy = int(round(max_dy_px * (t ** 1.3)))
        for x in range(w):
            c = src[x, y]
            if c[3] > 0:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    dst[nx, ny] = c
    return out


# 4-frame retro wind cycle:
# Frame 0: 기본 위치 (0px)
# Frame 1: 오른쪽 살짝 휨 (+2px)
# Frame 2: 최대 휨 (+4px, +1px)
# Frame 3: 돌아오는 중간 단계 (+2px)
SWAY_CYCLE = [(0, 0), (2, 0), (4, 1), (2, 0)]

for f_idx, (dx_tree, dy_tree) in enumerate(SWAY_CYCLE):
    canvas = Image.new("RGBA", (640, 360), (0, 0, 0, 0))

    # Warped left & right village trees on the far edges framing the scene
    t_l = shear_top_of_sprite(tree_left, dx_tree, dy_tree, anchor_bottom_ratio=0.62)
    t_r = shear_top_of_sprite(tree_right, dx_tree, dy_tree, anchor_bottom_ratio=0.62)
    canvas.alpha_composite(t_l, (-28, 152))
    canvas.alpha_composite(t_r, (640 - 142, 152))

    # Warped foreground bushes & flower tufts & grass blades along bottom corners
    b_round = shear_top_of_sprite(bush_round, max(0, dx_tree - 1), 0, anchor_bottom_ratio=0.75)
    b_flw = shear_top_of_sprite(bush_flower, max(0, dx_tree - 1), 0, anchor_bottom_ratio=0.75)
    g1 = shear_top_of_sprite(grass_1, dx_tree, 0, anchor_bottom_ratio=0.80)
    g2 = shear_top_of_sprite(grass_2, dx_tree, 0, anchor_bottom_ratio=0.80)

    canvas.alpha_composite(b_round, (68, 304))
    canvas.alpha_composite(b_flw, (118, 308))
    canvas.alpha_composite(g1, (168, 312))
    canvas.alpha_composite(g2, (430, 314))
    canvas.alpha_composite(b_flw, (468, 308))
    canvas.alpha_composite(g1, (520, 312))

    canvas.save(os.path.join(REGIONS_DIR, f"foliage_overlay_f{f_idx}.png"))

print("3. Built 4-frame AI pixel-art swaying trees, lanterns, flower bushes & grass -> foliage_overlay_f0..3.png")


# =====================================================================
# 4. Rebuild 14 Region 4-Frame Backgrounds at Full 640x360 High Detail
#    (No 320x180 downsampling blur!)
# =====================================================================
MASTER_TOWN_1 = Image.open(os.path.join(ARTIFACT_DIR, "town_bg_1_1793147727296.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.LANCZOS)
MASTER_TOWN_2 = Image.open(os.path.join(ARTIFACT_DIR, "town_bg_2_1793147728821.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.LANCZOS)
MASTER_TOWN_3 = Image.open(os.path.join(ARTIFACT_DIR, "town_bg_3_1793168250006.jpg" if os.path.exists(os.path.join(ARTIFACT_DIR, "town_bg_3_1793168250006.jpg")) else os.path.join(ARTIFACT_DIR, "town_bg_3_1793147731093.jpg"))).convert("RGBA").resize((640, 360), Image.Resampling.LANCZOS)

MASTER_BATTLE_1 = Image.open(os.path.join(ARTIFACT_DIR, "battle_bg_1_1793147708706.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.LANCZOS)
MASTER_BATTLE_2 = Image.open(os.path.join(ARTIFACT_DIR, "battle_bg_2_1793147709966.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.LANCZOS)
MASTER_BATTLE_3 = Image.open(os.path.join(ARTIFACT_DIR, "battle_bg_3_1793147711700.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.LANCZOS)


def clamp(v):
    return max(0, min(255, int(v)))


def build_highres_4frame_bg(base_img, r_mod=1.0, g_mod=1.0, b_mod=1.0, r_add=0, g_add=0, b_add=0, flip_x=False):
    work = base_img.copy()
    if flip_x:
        work = work.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    W, H = 640, 360
    spx = work.load()
    for y in range(H):
        for x in range(W):
            r, g, b, a = spx[x, y]
            spx[x, y] = (
                clamp(r * r_mod + r_add),
                clamp(g * g_mod + g_add),
                clamp(b * b_mod + b_add),
                255,
            )

    # Identify foliage / lantern / flame pixels at full 640x360 resolution
    mask = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            r, g, b, _ = spx[x, y]
            if (g > r + 14 and g > b + 10 and g > 40) or (r > 210 and g > 110 and b < 70 and y > H * 0.2):
                mask[y][x] = True

    sway_px = [0, 2, 4, 2]
    frames = []
    for dx in sway_px:
        if dx == 0:
            frames.append(work.copy())
            continue
        fim = work.copy()
        fpx = fim.load()
        for y in range(2, H - 2):
            for x in range(W - 1, dx, -1):
                if mask[y][x - dx]:
                    fpx[x, y] = spx[x - dx, y]
        frames.append(fim)
    return frames


REGION_CONFIGS = {
    1:  (MASTER_TOWN_3, MASTER_BATTLE_3, 1.00, 1.00, 1.00, 0, 0, 0, False),
    2:  (MASTER_TOWN_1, MASTER_BATTLE_1, 0.92, 1.05, 1.18, 0, 8, 20, False),
    3:  (MASTER_TOWN_2, MASTER_BATTLE_2, 1.08, 0.98, 0.88, 10, 0, -5, False),
    4:  (MASTER_TOWN_1, MASTER_BATTLE_1, 0.88, 1.12, 1.28, 15, 22, 38, True),
    5:  (MASTER_TOWN_2, MASTER_BATTLE_2, 1.05, 0.95, 0.82, 8, 0, -10, True),
    6:  (MASTER_TOWN_3, MASTER_BATTLE_3, 1.15, 0.88, 1.12, 18, -8, 15, False),
    7:  (MASTER_TOWN_2, MASTER_BATTLE_3, 1.22, 1.05, 0.82, 22, 10, -10, True),
    8:  (MASTER_TOWN_1, MASTER_BATTLE_1, 0.78, 1.08, 1.28, -8, 12, 32, False),
    9:  (MASTER_TOWN_3, MASTER_BATTLE_1, 0.72, 1.15, 1.32, -12, 18, 38, True),
    10: (MASTER_TOWN_1, MASTER_BATTLE_1, 0.95, 1.08, 1.25, 12, 18, 32, True),
    11: (MASTER_TOWN_3, MASTER_BATTLE_2, 1.22, 1.08, 0.78, 28, 12, -20, False),
    12: (MASTER_TOWN_2, MASTER_BATTLE_2, 1.32, 0.82, 0.72, 35, -10, -18, True),
    13: (MASTER_TOWN_3, MASTER_BATTLE_3, 1.18, 1.12, 0.88, 20, 15, 0, False),
    14: (MASTER_TOWN_3, MASTER_BATTLE_2, 1.18, 0.85, 1.32, 20, -8, 35, False),
}

for r_id, (t_m, b_m, rm, gm, bm, ra, ga, ba, flip) in REGION_CONFIGS.items():
    tf = build_highres_4frame_bg(t_m, rm, gm, bm, ra, ga, ba, flip)
    bf = build_highres_4frame_bg(b_m, rm, gm, bm, ra, ga, ba, flip)
    for f_idx in range(4):
        tf[f_idx].save(os.path.join(REGIONS_DIR, f"town_bg_{r_id}_f{f_idx}.png"))
        bf[f_idx].save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}_f{f_idx}.png"))
    tf[0].save(os.path.join(REGIONS_DIR, f"town_bg_{r_id}.png"))
    bf[0].save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png"))

print("4. Rebuilt all 14 regions x 4 frames at full 640x360 crisp resolution.")
