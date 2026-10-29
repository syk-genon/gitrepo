# -*- coding: utf-8 -*-
import os, sys
from collections import deque
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

ARTIFACT_DIR = r"C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f"
REGIONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\ui\regions"
os.makedirs(REGIONS_DIR, exist_ok=True)

SHEET_A = os.path.join(ARTIFACT_DIR, "environmental_stage_props_sheet_1793170148589.jpg")
SHEET_B = os.path.join(ARTIFACT_DIR, "biome_stage_props_spritesheet_1793170154616.jpg")
TREES_SHEET = os.path.join(ARTIFACT_DIR, "retro_pixel_art_spritesheet_1793168250006.jpg")


def remove_white_bg_floodfill(im, threshold=238):
    rgba = im.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    visited = [[False] * w for _ in range(h)]
    q = deque()

    def is_bg_white(r, g, b):
        return r >= threshold and g >= threshold and b >= threshold and abs(r - g) < 18 and abs(g - b) < 18

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

    # Clean 1px fringe
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = px[x, y]
            if a > 0 and r > 225 and g > 225 and b > 225:
                if (px[x - 1, y][3] == 0 or px[x + 1, y][3] == 0 or
                    px[x, y - 1][3] == 0 or px[x, y + 1][3] == 0):
                    px[x, y] = (10, 7, 5, 255)
    return rgba


def trim_tight(rgba):
    alpha = rgba.split()[3]
    bbox = alpha.point(lambda p: 255 if p > 25 else 0).getbbox()
    return rgba.crop(bbox) if bbox else rgba


def resize_sprite(rgba, max_w, max_h):
    trimmed = trim_tight(rgba)
    ratio = min(max_w / max(1, trimmed.width), max_h / max(1, trimmed.height))
    nw = max(1, int(trimmed.width * ratio))
    nh = max(1, int(trimmed.height * ratio))
    return trimmed.resize((nw, nh), Image.Resampling.LANCZOS)


print("Loading and extracting authentic 16-bit props...")
im_a = Image.open(SHEET_A).convert("RGBA")
aw, ah = im_a.size
col_a, row_a = aw // 3, ah // 2

prop_cheongsa = resize_sprite(remove_white_bg_floodfill(im_a.crop((0, 0, col_a, row_a))), 160, 200)
prop_crane = resize_sprite(remove_white_bg_floodfill(im_a.crop((col_a, 0, col_a * 2, row_a))), 180, 210)
prop_bunker = resize_sprite(remove_white_bg_floodfill(im_a.crop((col_a * 2, 0, aw, row_a))), 165, 210)
prop_torii = resize_sprite(remove_white_bg_floodfill(im_a.crop((0, row_a, col_a, ah))), 175, 205)
prop_dragon = resize_sprite(remove_white_bg_floodfill(im_a.crop((col_a, row_a, col_a * 2, ah))), 160, 210)
prop_braziers = resize_sprite(remove_white_bg_floodfill(im_a.crop((col_a * 2, row_a, aw, ah))), 170, 160)

im_b = Image.open(SHEET_B).convert("RGBA")
bw, bh = im_b.size
col_b, row_b = bw // 3, bh // 2

prop_snowpine = resize_sprite(remove_white_bg_floodfill(im_b.crop((0, 0, col_b, row_b))), 170, 205)
prop_kelp = resize_sprite(remove_white_bg_floodfill(im_b.crop((col_b, 0, col_b * 2, row_b))), 175, 200)
prop_dragon_ribs = resize_sprite(remove_white_bg_floodfill(im_b.crop((col_b * 2, 0, bw, row_b))), 185, 185)
prop_obelisk = resize_sprite(remove_white_bg_floodfill(im_b.crop((0, row_b, col_b, bh))), 160, 200)
prop_volcano = resize_sprite(remove_white_bg_floodfill(im_b.crop((col_b, row_b, col_b * 2, bh))), 175, 195)
prop_crystal_pylon = resize_sprite(remove_white_bg_floodfill(im_b.crop((col_b * 2, row_b, bw, bh))), 165, 210)

im_t = Image.open(TREES_SHEET).convert("RGBA")
tw, th = im_t.size
prop_sacred_tree = resize_sprite(remove_white_bg_floodfill(im_t.crop((0, 0, tw // 2, th // 2))), 170, 195)


def shear_prop(sprite, dx, dy=0, anchor_ratio=0.65):
    w, h = sprite.size
    src = sprite.load()
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dst = out.load()
    anchor_y = int(h * anchor_ratio)
    for y in range(h):
        if y >= anchor_y:
            cur_dx, cur_dy = 0, 0
        else:
            t = (anchor_y - y) / max(1.0, float(anchor_y))
            cur_dx = int(round(dx * t))
            cur_dy = int(round(dy * (t ** 1.3)))
        for x in range(w):
            c = src[x, y]
            if c[3] > 0:
                nx, ny = x + cur_dx, y + cur_dy
                if 0 <= nx < w and 0 <= ny < h:
                    dst[nx, ny] = c
    return out


def pulse_bright(sprite, mult=1.0):
    if abs(mult - 1.0) < 0.01:
        return sprite
    r, g, b, a = sprite.split()
    rgb = Image.merge("RGB", (r, g, b))
    enh = ImageEnhance.Brightness(rgb).enhance(mult)
    enh.putalpha(a)
    return enh


# Define prop layout & motion style for all 14 regions:
# Displacements are halved (maximum 1px shear) so objects never jerk abruptly!
REGION_PROPS = {
    1:  {"left": prop_cheongsa,     "right": prop_braziers,      "style": "sway",  "dx": 1, "dy": 0},
    2:  {"left": prop_sacred_tree,   "right": prop_braziers,      "style": "sway",  "dx": 1, "dy": 0},
    3:  {"left": prop_crane,         "right": prop_crane,        "style": "sway",  "dx": 1, "dy": 0},
    4:  {"left": prop_snowpine,      "right": prop_snowpine,     "style": "sway",  "dx": 1, "dy": 0},
    5:  {"left": prop_bunker,        "right": prop_bunker,       "style": "pulse", "dx": 0, "dy": 0},
    6:  {"left": prop_torii,         "right": prop_braziers,      "style": "sway",  "dx": 1, "dy": 0},
    7:  {"left": prop_dragon,        "right": prop_braziers,      "style": "sway",  "dx": 1, "dy": 0},
    8:  {"left": prop_snowpine,      "right": prop_braziers,      "style": "sway",  "dx": 1, "dy": 0},
    9:  {"left": prop_kelp,          "right": prop_kelp,         "style": "sway",  "dx": 1, "dy": 0},
    10: {"left": prop_dragon_ribs,   "right": prop_snowpine,     "style": "pulse", "dx": 1, "dy": 0},
    11: {"left": prop_obelisk,       "right": prop_obelisk,      "style": "pulse", "dx": 0, "dy": 0},
    12: {"left": prop_volcano,       "right": prop_volcano,      "style": "pulse", "dx": 1, "dy": 0},
    13: {"left": prop_crystal_pylon, "right": prop_crystal_pylon,"style": "float", "dx": 1, "dy": 1},
    14: {"left": prop_crystal_pylon, "right": prop_crystal_pylon,"style": "float", "dx": 1, "dy": 1},
}

# 4-frame animation cycle with halved, subtle transitions:
# Frame 0: 기본 위치
# Frame 1: 극미세 흔들림 (+0~1px)
# Frame 2: 최대 흔들림 (+1px)
# Frame 3: 복귀 중간 단계 (+0~1px)
CYCLES = {
    "sway":  [(0, 0, 1.0), (0, 0, 1.01), (1, 0, 1.03), (0, 0, 1.01)],
    "pulse": [(0, 0, 1.0), (0, 0, 1.05), (0, 0, 1.12), (0, 0, 1.05)],
    "float": [(0, 0, 1.0), (0, -1, 1.03), (1, -1, 1.06), (0, -1, 1.03)]
}

for r_id in range(1, 15):
    cfg = REGION_PROPS[r_id]
    l_prop = cfg["left"]
    r_prop = cfg["right"]
    style = cfg["style"]
    scale_dx = cfg["dx"]
    scale_dy = cfg["dy"]

    for f_idx, (dx_step, dy_step, bright) in enumerate(CYCLES[style]):
        canvas = Image.new("RGBA", (640, 360), (0, 0, 0, 0))

        # Halved pixel displacement (maximum 1px displacement!)
        c_dx = min(1, int(round(dx_step * scale_dx)))
        c_dy = min(1, int(round(dy_step * scale_dy)))

        # Process left prop
        cur_l = shear_prop(l_prop, c_dx, c_dy, anchor_ratio=0.72)
        cur_l = pulse_bright(cur_l, bright)

        # Process right prop (flipped horizontally for balanced framing)
        cur_r = r_prop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        cur_r = shear_prop(cur_r, -c_dx, c_dy, anchor_ratio=0.72)
        cur_r = pulse_bright(cur_r, bright)

        # Place left prop on ground corner
        lx = 4
        ly = 360 - cur_l.height - 4
        canvas.alpha_composite(cur_l, (lx, ly))

        # Place right prop on far ground corner
        rx = 640 - cur_r.width - 4
        ry = 360 - cur_r.height - 4
        canvas.alpha_composite(cur_r, (rx, ry))

        out_name = f"region_obj_{r_id}_f{f_idx}.png"
        canvas.save(os.path.join(REGIONS_DIR, out_name))

print("Successfully generated all 14 regions x 4 frames of authentic 16-bit environmental objects!")
