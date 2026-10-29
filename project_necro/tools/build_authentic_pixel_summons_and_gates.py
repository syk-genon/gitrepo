# -*- coding: utf-8 -*-
import os, sys, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"D:\workspace\GEMINI\project_necro"
SUMMONS_DIR = os.path.join(BASE_DIR, "assets", "summons")
GATES_DIR = os.path.join(BASE_DIR, "assets", "ui", "gates")
SRC_MONSTERS = r"D:\workspace\GEMINI\project2100\assets\monsters"
os.makedirs(SUMMONS_DIR, exist_ok=True)
os.makedirs(GATES_DIR, exist_ok=True)


def pixelate_sprite(src_img, grid_res=56, colors=24, tint=None):
    im = src_img.convert("RGBA")
    alpha = im.split()[3]
    bbox = alpha.point(lambda p: 255 if p > 30 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)

    if tint:
        rm, gm, bm = tint
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a > 0:
                    px[x, y] = (
                        max(0, min(255, int(r * rm))),
                        max(0, min(255, int(g * gm))),
                        max(0, min(255, int(b * bm))),
                        a,
                    )

    r, g, b, a = im.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageEnhance.Color(rgb).enhance(1.25)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.18)

    inner = grid_res - 6
    ratio = min(inner / max(1, im.width), inner / max(1, im.height))
    nw = max(1, int(im.width * ratio))
    nh = max(1, int(im.height * ratio))

    s_rgb = rgb.resize((nw, nh), Image.Resampling.LANCZOS)
    s_a = a.resize((nw, nh), Image.Resampling.LANCZOS).point(lambda p: 255 if p > 90 else 0)

    quant = s_rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGBA")
    quant.putalpha(s_a)

    canvas = Image.new("RGBA", (grid_res, grid_res), (0, 0, 0, 0))
    canvas.alpha_composite(quant, ((grid_res - nw) // 2, (grid_res - nh) // 2))

    # 1px dark outline at grid_res -> 2px at 2x
    ga = canvas.split()[3]
    dil = ga.filter(ImageFilter.MaxFilter(3))
    out = Image.new("RGBA", (grid_res, grid_res), (0, 0, 0, 0))
    opx = out.load()
    spx = canvas.load()
    dpx = dil.load()
    for y in range(grid_res):
        for x in range(grid_res):
            if spx[x, y][3] > 128:
                opx[x, y] = spx[x, y]
            elif dpx[x, y] > 128:
                opx[x, y] = (10, 7, 5, 255)

    return out.resize((grid_res * 2, grid_res * 2), Image.Resampling.NEAREST)


# 1. Build 7 Authentic 16-bit Pixel Summon Units
SUMMON_SOURCES = [
    ("minion_skeleton_warrior.png", "m_2_3.png", (0.85, 1.25, 1.10), 56),
    ("minion_skeleton_archer.png", "m_7_3.png", (0.80, 1.30, 1.05), 56),
    ("minion_skeleton_mage.png", "m_5_named.png", (0.95, 0.85, 1.35), 56),
    ("minion_death_knight.png", "m_7_boss.png", (0.85, 0.85, 1.35), 68),
    ("minion_frost_dragon.png", "m_10_boss.png", (0.90, 1.15, 1.35), 76),
    ("minion_shadow_clone.png", "m_3_named.png", (0.80, 0.75, 1.35), 56),
    ("minion_holy_guardian.png", "m_10_4.png", (1.35, 1.25, 0.75), 60),
]

for fn, src_m, tint, g_res in SUMMON_SOURCES:
    im = Image.open(os.path.join(SRC_MONSTERS, src_m)).convert("RGBA")
    if src_m == "m_7_boss.png":
        w, h = im.size
        im = im.crop((0, 0, w, int(h * 0.90)))
    sp = pixelate_sprite(im, grid_res=g_res, colors=28, tint=tint)
    out_p = os.path.join(SUMMONS_DIR, fn)
    sp.save(out_p)
    print(f"Summon {fn}: {os.path.getsize(out_p):,} B")


# 2. Build 6 Authentic 16-bit Pixel Art Dungeon Gates (drawn directly on 64x72 pixel grid with brick-by-brick masonry, wood planks, rivets & swirling pixel portal, then upscaled 2x NEAREST)
GATE_PALETTES = {
    "gate_iron.png": {
        "stone_dark": (48, 52, 62, 255),
        "stone_mid": (88, 96, 110, 255),
        "stone_hi": (142, 152, 168, 255),
        "door_dark": (46, 32, 22, 255),
        "door_mid": (78, 52, 34, 255),
        "portal_1": (0, 145, 105, 255),
        "portal_2": (0, 235, 165, 255),
        "portal_3": (175, 255, 225, 255),
        "gem": (0, 255, 170, 255),
    },
    "gate_bronze.png": {
        "stone_dark": (78, 44, 22, 255),
        "stone_mid": (145, 86, 42, 255),
        "stone_hi": (215, 142, 78, 255),
        "door_dark": (52, 34, 20, 255),
        "door_mid": (92, 60, 34, 255),
        "portal_1": (20, 135, 115, 255),
        "portal_2": (60, 225, 175, 255),
        "portal_3": (195, 255, 230, 255),
        "gem": (255, 185, 70, 255),
    },
    "gate_silver.png": {
        "stone_dark": (68, 84, 108, 255),
        "stone_mid": (138, 162, 192, 255),
        "stone_hi": (218, 235, 252, 255),
        "door_dark": (38, 52, 74, 255),
        "door_mid": (68, 92, 126, 255),
        "portal_1": (0, 120, 195, 255),
        "portal_2": (0, 215, 255, 255),
        "portal_3": (200, 250, 255, 255),
        "gem": (0, 240, 255, 255),
    },
    "gate_gold.png": {
        "stone_dark": (112, 72, 12, 255),
        "stone_mid": (198, 142, 24, 255),
        "stone_hi": (255, 225, 88, 255),
        "door_dark": (68, 42, 12, 255),
        "door_mid": (122, 78, 22, 255),
        "portal_1": (195, 95, 0, 255),
        "portal_2": (255, 185, 0, 255),
        "portal_3": (255, 248, 175, 255),
        "gem": (255, 215, 0, 255),
    },
    "gate_platinum.png": {
        "stone_dark": (58, 72, 112, 255),
        "stone_mid": (118, 148, 205, 255),
        "stone_hi": (210, 232, 255, 255),
        "door_dark": (42, 32, 72, 255),
        "door_mid": (78, 58, 128, 255),
        "portal_1": (105, 25, 185, 255),
        "portal_2": (185, 75, 255, 255),
        "portal_3": (240, 195, 255, 255),
        "gem": (200, 80, 255, 255),
    },
    "gate_diamond.png": {
        "stone_dark": (48, 82, 138, 255),
        "stone_mid": (105, 188, 238, 255),
        "stone_hi": (225, 252, 255, 255),
        "door_dark": (72, 22, 52, 255),
        "door_mid": (138, 38, 88, 255),
        "portal_1": (185, 18, 88, 255),
        "portal_2": (255, 42, 125, 255),
        "portal_3": (255, 215, 240, 255),
        "gem": (255, 42, 109, 255),
    },
}


def build_pixel_gate(fn, pal):
    GW, GH = 64, 72
    im = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    px = im.load()
    OL = (10, 7, 5, 255)

    cx, cy = 32, 38

    # 1. Stepped stone pedestal base (y=60..69)
    for y in range(60, 65):
        for x in range(8, 56):
            if y == 60 or y == 64 or x == 8 or x == 55 or (x + (y // 2) * 5) % 8 == 0:
                px[x, y] = OL
            elif y == 61:
                px[x, y] = pal["stone_hi"]
            else:
                px[x, y] = pal["stone_mid"]
    for y in range(65, 70):
        for x in range(4, 60):
            if y == 65 or y == 69 or x == 4 or x == 59 or (x + 3) % 9 == 0:
                px[x, y] = OL
            elif y == 66:
                px[x, y] = pal["stone_hi"]
            else:
                px[x, y] = pal["stone_dark"]

    # 2. Archway & Pillars + Inner Swirling Pixel Portal
    for y in range(10, 60):
        for x in range(10, 54):
            # Arch equation for top (y < 30)
            dx = x - cx
            dy = y - 30
            in_outer = False
            in_inner = False
            if y >= 28:
                in_outer = (11 <= x <= 52)
                in_inner = (18 <= x <= 45)
            else:
                dist = math.sqrt(dx * dx + (dy * 1.15) ** 2)
                in_outer = dist <= 21.5
                in_inner = dist <= 14.0

            if in_inner:
                # Pixel vortex inside gate
                r_dist = math.sqrt(dx * dx + ((y - 38) * 0.85) ** 2)
                ang = math.atan2(y - 38, dx)
                swirl = int((r_dist * 0.9 + ang * 2.5) * 2) % 3
                if r_dist < 3.2:
                    px[x, y] = pal["portal_3"]
                elif swirl == 0:
                    px[x, y] = pal["portal_3"] if (x + y) % 2 == 0 else pal["portal_2"]
                elif swirl == 1:
                    px[x, y] = pal["portal_2"]
                else:
                    px[x, y] = pal["portal_1"]
            elif in_outer:
                # Brick masonry pattern on arch and pillars
                brick_row = y // 4
                brick_col = (x + (brick_row % 2) * 3) // 6
                is_mortar = (y % 4 == 0) or ((x + (brick_row % 2) * 3) % 6 == 0)
                if is_mortar:
                    px[x, y] = pal["stone_dark"]
                elif (y % 4 == 1) or (x < cx and (x % 6 == 1)):
                    px[x, y] = pal["stone_hi"]
                else:
                    px[x, y] = pal["stone_mid"]

    # 3. Heavy Wooden/Iron Dungeon Doors slightly ajar on left & right of portal (x=18..24 and x=39..45, y=28..59)
    for y in range(28, 60):
        for x in list(range(18, 25)) + list(range(39, 46)):
            if x in (18, 24, 39, 45) or y == 28 or y == 59:
                px[x, y] = OL
            elif y in (34, 44, 53):
                # Iron hinge bands & rivets
                px[x, y] = pal["stone_hi"] if x % 2 == 0 else pal["stone_mid"]
            else:
                px[x, y] = pal["door_mid"] if (x % 2 == 0) else pal["door_dark"]

    # 4. Keystone Gem Crest at top of arch (cx=32, y=6..16)
    for y in range(5, 17):
        for x in range(26, 39):
            md = abs(x - cx) + abs(y - 11)
            if md == 6:
                px[x, y] = OL
            elif md == 5:
                px[x, y] = pal["stone_hi"]
            elif md <= 4:
                px[x, y] = pal["portal_3"] if md <= 1 else pal["gem"]

    # 5. Crisp outer black pixel outline
    a = im.split()[3]
    dil = a.filter(ImageFilter.MaxFilter(3))
    out = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    opx = out.load()
    dpx = dil.load()
    for y in range(GH):
        for x in range(GW):
            if px[x, y][3] > 128:
                opx[x, y] = px[x, y]
            elif dpx[x, y] > 128:
                opx[x, y] = OL

    # Upscale 2.5x with NEAREST -> 160x180
    final_gate = out.resize((160, 180), Image.Resampling.NEAREST)
    out_path = os.path.join(GATES_DIR, fn)
    final_gate.save(out_path)
    return os.path.getsize(out_path)


for fn, pal in GATE_PALETTES.items():
    sz = build_pixel_gate(fn, pal)
    print(f"Gate {fn}: {sz:,} B")
