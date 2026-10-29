# -*- coding: utf-8 -*-
import os, sys, math, random
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

REGIONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\ui\regions"
os.makedirs(REGIONS_DIR, exist_ok=True)

OL = (10, 7, 5, 255)
GW, GH = 160, 90


def draw_pixel_rect_outlined(px, x0, y0, x1, y1, fill, hi=None, dark=None):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    for y in range(max(0, y0), min(GH, y1 + 1)):
        for x in range(max(0, x0), min(GW, x1 + 1)):
            if x == x0 or x == x1 or y == y0 or y == y1:
                px[x, y] = OL
            elif hi and (y == y0 + 1 or x == x0 + 1):
                px[x, y] = hi
            elif dark and (y == y1 - 1 or x == x1 - 1):
                px[x, y] = dark
            else:
                px[x, y] = fill


def draw_sky_bands(px, bands):
    # bands: list of (y_end, color)
    y_cur = 0
    for y_end, col in bands:
        for y in range(y_cur, min(GH, y_end)):
            for x in range(GW):
                px[x, y] = col
        y_cur = y_end


def draw_pixel_cloud(px, cx, cy, w, col=(245, 250, 255, 255), shade=(195, 215, 235, 255)):
    for dy in range(-4, 4):
        for dx in range(-w, w + 1):
            if (dx * dx) / (w * w + 1) + (dy * dy) / 14.0 <= 1.0:
                x, y = cx + dx, cy + dy
                if 0 <= x < GW and 0 <= y < GH:
                    px[x, y] = shade if dy >= 2 else col


def draw_mountain(px, peak_x, peak_y, base_y, slope, col_main, col_shade, snow_cap=True):
    for y in range(peak_y, min(GH, base_y)):
        half_w = int((y - peak_y) * slope)
        for x in range(max(0, peak_x - half_w), min(GW, peak_x + half_w + 1)):
            if x == peak_x - half_w or x == peak_x + half_w:
                px[x, y] = OL
            elif snow_cap and (y - peak_y) < (base_y - peak_y) * 0.32 - abs(x - peak_x) * 0.25:
                px[x, y] = (245, 250, 255, 255) if x <= peak_x else (200, 220, 240, 255)
            else:
                px[x, y] = col_main if x <= peak_x else col_shade


def draw_pixel_tree(px, tx, ty_ground, r_crown, trunk_col=(110, 62, 32, 255), leaf_dark=(22, 95, 28, 255), leaf_mid=(48, 165, 42, 255), leaf_hi=(115, 225, 65, 255)):
    # Trunk with black outline
    tw = max(2, r_crown // 3)
    th = int(r_crown * 1.2)
    for y in range(ty_ground - th, ty_ground + 1):
        for x in range(tx - tw, tx + tw + 1):
            if 0 <= x < GW and 0 <= y < GH:
                if x == tx - tw or x == tx + tw:
                    px[x, y] = OL
                else:
                    px[x, y] = trunk_col

    # Leafy clusters with black outline
    cy = ty_ground - th - r_crown // 2
    blobs = [(0, 0, r_crown), (-r_crown // 2, 2, int(r_crown * 0.75)), (r_crown // 2, 2, int(r_crown * 0.75)), (0, -r_crown // 2, int(r_crown * 0.75))]
    # First pass: black outline
    for bx, by, br in blobs:
        for dy in range(-br - 1, br + 2):
            for dx in range(-br - 1, br + 2):
                if dx * dx + dy * dy <= (br + 1) ** 2:
                    x, y = tx + bx + dx, cy + by + dy
                    if 0 <= x < GW and 0 <= y < GH:
                        px[x, y] = OL
    # Second pass: leaf shading
    for bx, by, br in blobs:
        for dy in range(-br, br + 1):
            for dx in range(-br, br + 1):
                if dx * dx + dy * dy <= br * br:
                    x, y = tx + bx + dx, cy + by + dy
                    if 0 <= x < GW and 0 <= y < GH:
                        if dy < -br * 0.25 and (x + y) % 2 == 0:
                            px[x, y] = leaf_hi
                        elif dy > br * 0.35:
                            px[x, y] = leaf_dark
                        else:
                            px[x, y] = leaf_mid


def draw_ground_road(px, y_grass, y_road_top, y_road_bot, grass_top, grass_dark, road_main, road_pebble):
    for y in range(y_grass, GH):
        for x in range(GW):
            if y == y_grass or y == y_road_top or y == y_road_bot:
                px[x, y] = OL
            elif y < y_road_top:
                px[x, y] = grass_top if (x + y) % 3 != 0 else grass_dark
            elif y < y_road_bot:
                px[x, y] = road_pebble if ((x * 7 + y * 13) % 29 == 0) else road_main
            else:
                px[x, y] = grass_dark if (x + y) % 2 == 0 else grass_top


def draw_house_or_building(px, hx, hy_ground, w, h, roof_h, wall_col, wall_brick, roof_col, roof_hi, sign_col=(225, 165, 70, 255)):
    y_top = hy_ground - h
    # Stone brick wall
    for y in range(y_top, hy_ground):
        for x in range(hx, hx + w):
            if 0 <= x < GW and 0 <= y < GH:
                if x == hx or x == hx + w - 1 or y == y_top or y == hy_ground - 1:
                    px[x, y] = OL
                elif (y - y_top) % 4 == 0 or ((x + ((y - y_top) // 4) * 3) % 6 == 0):
                    px[x, y] = wall_brick
                else:
                    px[x, y] = wall_col

    # Pitched tiled roof with black outline
    for dy in range(roof_h + 1):
        y = y_top - roof_h + dy
        pad = int((roof_h - dy) * 0.8)
        rx0 = hx - 3 + pad
        rx1 = hx + w + 2 - pad
        for x in range(rx0, rx1 + 1):
            if 0 <= x < GW and 0 <= y < GH:
                if x == rx0 or x == rx1 or dy == 0 or dy == roof_h:
                    px[x, y] = OL
                elif dy % 3 == 0:
                    px[x, y] = roof_hi
                else:
                    px[x, y] = roof_col

    # Wooden Door & Signboard
    dx0 = hx + w // 2 - 5
    dx1 = hx + w // 2 + 5
    dy0 = hy_ground - 14
    draw_pixel_rect_outlined(px, dx0, dy0, dx1, hy_ground - 1, (125, 72, 32, 255), (165, 102, 48, 255), (78, 42, 18, 255))
    # Signboard above door
    draw_pixel_rect_outlined(px, dx0 - 2, dy0 - 7, dx1 + 2, dy0 - 2, sign_col, (255, 215, 115, 255))


def draw_crates_and_signpost(px, gx, gy):
    # Wooden crates with black outline
    draw_pixel_rect_outlined(px, gx, gy - 9, gx + 9, gy, (155, 92, 38, 255), (198, 128, 58, 255), (98, 54, 20, 255))
    draw_pixel_rect_outlined(px, gx + 10, gy - 7, gx + 18, gy, (142, 82, 32, 255), (185, 118, 52, 255), (88, 48, 18, 255))
    # Wooden signpost in middle
    sx = 78
    draw_pixel_rect_outlined(px, sx, gy - 16, sx + 3, gy, (112, 64, 28, 255))
    draw_pixel_rect_outlined(px, sx - 6, gy - 15, sx + 9, gy - 9, (175, 108, 44, 255), (218, 148, 72, 255))


# 14 Distinct Themes for the 16-bit Side-Scrolling Pixel Art Engine
THEMES = {
    1: {  # 서울 지하철 미궁 & 을지로 대장간 [철문]
        "sky": [(22, (28, 36, 52, 255)), (45, (42, 58, 78, 255)), (65, (64, 88, 108, 255))],
        "mtn": ((110, 78, 92, 255), (68, 52, 68, 255), False),
        "grass": ((42, 148, 88, 255), (24, 96, 56, 255)),
        "road": ((142, 118, 96, 255), (98, 78, 62, 255)),
        "wall": ((138, 146, 158, 255), (88, 96, 108, 255)),
        "roof": ((188, 42, 48, 255), (235, 78, 72, 255)),
        "tree": ((28, 118, 68, 255), (52, 178, 102, 255), (112, 238, 158, 255)),
        "battle_sky": [(24, (18, 24, 32, 255)), (48, (28, 44, 48, 255)), (66, (38, 68, 62, 255))],
        "battle_prop": "subway_pillars",
    },
    2: {  # 북한산 비밀 성역 & 은문 [은문]
        "sky": [(22, (72, 168, 245, 255)), (45, (112, 198, 255, 255)), (65, (168, 228, 255, 255))],
        "mtn": ((148, 168, 198, 255), (98, 118, 152, 255), True),
        "grass": ((64, 195, 68, 255), (38, 138, 42, 255)),
        "road": ((205, 156, 104, 255), (158, 112, 68, 255)),
        "wall": ((168, 178, 192, 255), (112, 122, 138, 255)),
        "roof": ((52, 118, 198, 255), (96, 168, 242, 255)),
        "tree": ((24, 112, 48, 255), (54, 178, 68, 255), (128, 235, 92, 255)),
        "battle_sky": [(24, (32, 68, 118, 255)), (48, (54, 108, 168, 255)), (66, (88, 152, 212, 255))],
        "battle_prop": "silver_altar",
    },
    3: {  # 인천항 제4부두 암시장 [동문]
        "sky": [(22, (38, 52, 88, 255)), (45, (68, 84, 128, 255)), (65, (118, 112, 148, 255))],
        "mtn": ((92, 104, 128, 255), (58, 68, 88, 255), False),
        "grass": ((68, 138, 92, 255), (42, 92, 62, 255)),
        "road": ((168, 138, 102, 255), (122, 96, 68, 255)),
        "wall": ((178, 112, 64, 255), (122, 72, 38, 255)),
        "roof": ((198, 88, 38, 255), (242, 138, 62, 255)),
        "tree": ((38, 98, 48, 255), (72, 152, 68, 255), (138, 208, 92, 255)),
        "battle_sky": [(24, (24, 38, 68, 255)), (48, (42, 68, 104, 255)), (66, (68, 102, 138, 255))],
        "battle_prop": "harbor_cranes",
    },
    4: {  # 설악산 대청봉 설원 [은문]
        "sky": [(22, (88, 188, 255, 255)), (45, (138, 215, 255, 255)), (65, (195, 238, 255, 255))],
        "mtn": ((188, 212, 238, 255), (128, 158, 196, 255), True),
        "grass": ((215, 238, 255, 255), (168, 202, 235, 255)),
        "road": ((178, 196, 218, 255), (132, 154, 182, 255)),
        "wall": ((158, 172, 188, 255), (108, 122, 142, 255)),
        "roof": ((68, 148, 218, 255), (128, 202, 255, 255)),
        "tree": ((48, 128, 148, 255), (92, 184, 208, 255), (215, 248, 255, 255)),
        "battle_sky": [(24, (58, 138, 218, 255)), (48, (98, 178, 242, 255)), (66, (158, 218, 255, 255))],
        "battle_prop": "ice_peaks",
    },
    5: {  # DMZ 휴전선 & 평양 지하벙커 [동문]
        "sky": [(22, (58, 64, 52, 255)), (45, (88, 96, 76, 255)), (65, (124, 132, 104, 255))],
        "mtn": ((108, 98, 82, 255), (72, 64, 52, 255), False),
        "grass": ((92, 148, 58, 255), (58, 102, 34, 255)),
        "road": ((158, 138, 108, 255), (112, 96, 72, 255)),
        "wall": ((118, 124, 112, 255), (78, 84, 74, 255)),
        "roof": ((148, 88, 42, 255), (198, 128, 64, 255)),
        "tree": ((42, 88, 32, 255), (78, 138, 52, 255), (132, 188, 78, 255)),
        "battle_sky": [(24, (38, 36, 32, 255)), (48, (58, 54, 48, 255)), (66, (82, 76, 66, 255))],
        "battle_prop": "bunker_walls",
    },
    6: {  # 양재동 & 도쿄 음양사 본가 [은문]
        "sky": [(22, (68, 38, 98, 255)), (45, (112, 58, 138, 255)), (65, (168, 88, 162, 255))],
        "mtn": ((118, 78, 128, 255), (78, 48, 92, 255), True),
        "grass": ((58, 158, 88, 255), (34, 104, 56, 255)),
        "road": ((192, 148, 118, 255), (142, 104, 78, 255)),
        "wall": ((215, 202, 188, 255), (158, 142, 128, 255)),
        "roof": ((198, 32, 58, 255), (248, 78, 98, 255)),
        "tree": ((138, 38, 88, 255), (212, 78, 138, 255), (255, 158, 198, 255)),
        "battle_sky": [(24, (48, 24, 72, 255)), (48, (82, 38, 108, 255)), (66, (128, 58, 138, 255))],
        "battle_prop": "torii_shrine",
    },
    7: {  # 마카오 불야성 VIP 카지노 [금문]
        "sky": [(22, (48, 24, 68, 255)), (45, (92, 42, 98, 255)), (65, (158, 78, 108, 255))],
        "mtn": ((138, 98, 68, 255), (92, 62, 42, 255), False),
        "grass": ((78, 168, 68, 255), (48, 112, 42, 255)),
        "road": ((218, 178, 108, 255), (168, 128, 68, 255)),
        "wall": ((218, 168, 68, 255), (158, 112, 38, 255)),
        "roof": ((218, 42, 68, 255), (255, 198, 58, 255)),
        "tree": ((38, 118, 52, 255), (78, 178, 78, 255), (248, 215, 78, 255)),
        "battle_sky": [(24, (58, 22, 48, 255)), (48, (108, 42, 68, 255)), (66, (168, 82, 68, 255))],
        "battle_prop": "gold_pillars",
    },
    8: {  # 블라디보스토크 해저 기지 [금문]
        "sky": [(22, (28, 78, 138, 255)), (45, (48, 118, 182, 255)), (65, (82, 162, 218, 255))],
        "mtn": ((118, 168, 208, 255), (78, 122, 162, 255), True),
        "grass": ((158, 218, 242, 255), (108, 168, 202, 255)),
        "road": ((138, 168, 192, 255), (96, 124, 148, 255)),
        "wall": ((128, 152, 178, 255), (84, 104, 128, 255)),
        "roof": ((208, 148, 42, 255), (248, 198, 78, 255)),
        "tree": ((32, 98, 118, 255), (64, 158, 182, 255), (168, 238, 255, 255)),
        "battle_sky": [(24, (18, 58, 108, 255)), (48, (32, 92, 152, 255)), (66, (58, 132, 192, 255))],
        "battle_prop": "ice_pipes",
    },
    9: {  # 태평양 미지의 해연 게이트 [플래티넘문]
        "sky": [(22, (14, 48, 98, 255)), (45, (24, 88, 148, 255)), (65, (38, 138, 188, 255))],
        "mtn": ((48, 118, 158, 255), (28, 78, 112, 255), False),
        "grass": ((38, 168, 148, 255), (22, 112, 98, 255)),
        "road": ((168, 158, 122, 255), (124, 114, 82, 255)),
        "wall": ((98, 148, 178, 255), (62, 102, 128, 255)),
        "roof": ((138, 68, 208, 255), (188, 118, 248, 255)),
        "tree": ((18, 118, 112, 255), (38, 188, 172, 255), (118, 252, 228, 255)),
        "battle_sky": [(24, (10, 36, 78, 255)), (48, (18, 68, 122, 255)), (66, (28, 108, 162, 255))],
        "battle_prop": "coral_spires",
    },
    10: {  # 히말라야 고룡 묘지 [플래티넘문]
        "sky": [(22, (58, 118, 208, 255)), (45, (98, 158, 238, 255)), (65, (158, 208, 252, 255))],
        "mtn": ((205, 222, 245, 255), (148, 172, 208, 255), True),
        "grass": ((198, 228, 248, 255), (148, 184, 218, 255)),
        "road": ((168, 178, 198, 255), (122, 132, 154, 255)),
        "wall": ((188, 198, 215, 255), (132, 144, 165, 255)),
        "roof": ((128, 68, 198, 255), (178, 118, 242, 255)),
        "tree": ((58, 118, 158, 255), (108, 178, 218, 255), (225, 248, 255, 255)),
        "battle_sky": [(24, (42, 88, 168, 255)), (48, (72, 128, 208, 255)), (66, (118, 178, 238, 255))],
        "battle_prop": "dragon_bones",
    },
    11: {  # 시베리아 & 타클라마칸 사막 [금문]
        "sky": [(22, (98, 178, 245, 255)), (45, (168, 212, 248, 255)), (65, (238, 218, 168, 255))],
        "mtn": ((218, 168, 98, 255), (168, 118, 58, 255), False),
        "grass": ((198, 178, 82, 255), (152, 132, 52, 255)),
        "road": ((235, 195, 118, 255), (188, 148, 78, 255)),
        "wall": ((218, 182, 122, 255), (168, 132, 78, 255)),
        "roof": ((218, 128, 32, 255), (255, 188, 68, 255)),
        "tree": ((58, 128, 42, 255), (98, 178, 62, 255), (168, 228, 88, 255)),
        "battle_sky": [(24, (188, 118, 52, 255)), (48, (228, 162, 78, 255)), (66, (248, 202, 118, 255))],
        "battle_prop": "pyramids",
    },
    12: {  # 독일 라인강 & 북미 로키산맥 화산 [플래티넘문]
        "sky": [(22, (88, 28, 28, 255)), (45, (148, 52, 32, 255)), (65, (208, 92, 38, 255))],
        "mtn": ((118, 58, 48, 255), (72, 34, 28, 255), False),
        "grass": ((118, 78, 48, 255), (78, 48, 28, 255)),
        "road": ((148, 98, 68, 255), (98, 62, 42, 255)),
        "wall": ((118, 98, 92, 255), (78, 62, 58, 255)),
        "roof": ((198, 58, 28, 255), (248, 118, 42, 255)),
        "tree": ((98, 38, 24, 255), (168, 68, 32, 255), (248, 148, 48, 255)),
        "battle_sky": [(24, (68, 18, 18, 255)), (48, (128, 38, 24, 255)), (66, (188, 78, 28, 255))],
        "battle_prop": "volcano_lava",
    },
    13: {  # 태평양 성층권 금문 모함 [금문]
        "sky": [(22, (24, 32, 68, 255)), (45, (42, 62, 118, 255)), (65, (72, 108, 178, 255))],
        "mtn": ((168, 148, 78, 255), (118, 98, 48, 255), False),
        "grass": ((68, 168, 148, 255), (42, 118, 102, 255)),
        "road": ((188, 168, 112, 255), (138, 118, 72, 255)),
        "wall": ((198, 168, 78, 255), (142, 118, 48, 255)),
        "roof": ((218, 168, 32, 255), (255, 222, 88, 255)),
        "tree": ((38, 128, 118, 255), (72, 198, 178, 255), (158, 248, 228, 255)),
        "battle_sky": [(24, (18, 24, 52, 255)), (48, (32, 48, 96, 255)), (66, (58, 88, 148, 255))],
        "battle_prop": "mothership_pillars",
    },
    14: {  # 2070 성층권 다이아몬드문 [다이아몬드문]
        "sky": [(22, (48, 18, 68, 255)), (45, (88, 32, 118, 255)), (65, (148, 52, 158, 255))],
        "mtn": ((138, 188, 238, 255), (88, 128, 188, 255), True),
        "grass": ((88, 198, 178, 255), (52, 138, 128, 255)),
        "road": ((208, 168, 198, 255), (158, 118, 148, 255)),
        "wall": ((168, 212, 242, 255), (112, 158, 198, 255)),
        "roof": ((228, 42, 108, 255), (255, 118, 178, 255)),
        "tree": ((118, 38, 128, 255), (188, 78, 198, 255), (255, 168, 238, 255)),
        "battle_sky": [(24, (36, 12, 54, 255)), (48, (72, 24, 98, 255)), (66, (128, 42, 138, 255))],
        "battle_prop": "diamond_throne",
    },
}


def build_town_bg(r_id, cfg):
    im = Image.new("RGBA", (GW, GH), (0, 0, 0, 255))
    px = im.load()

    # 1. Sky bands + pixel clouds
    draw_sky_bands(px, cfg["sky"])
    draw_pixel_cloud(px, 108, 14, 14)
    draw_pixel_cloud(px, 142, 19, 10)

    # 2. Distant pixelated mountains (like World 1-1 reference)
    m_main, m_shade, snow = cfg["mtn"]
    draw_mountain(px, 94, 22, 62, 0.85, m_main, m_shade, snow_cap=snow)
    draw_mountain(px, 124, 15, 62, 0.92, m_main, m_shade, snow_cap=snow)

    # 3. Rolling green/biome hills in midground (y=46..64)
    g_top, g_dark = cfg["grass"]
    for y in range(46, 65):
        for x in range(GW):
            hill_y = 48 + int(math.sin(x * 0.06 + r_id) * 3)
            if y == hill_y:
                px[x, y] = OL
            elif y > hill_y:
                px[x, y] = g_top

    # 4. Background pixel trees with bold black outlines
    td, tm, th = cfg["tree"]
    draw_pixel_tree(px, 64, 62, 11, leaf_dark=td, leaf_mid=tm, leaf_hi=th)
    draw_pixel_tree(px, 118, 62, 12, leaf_dark=td, leaf_mid=tm, leaf_hi=th)

    # 5. Left side-view pixel house/outpost (just like the red-roofed stone house in World 1-1!)
    w_col, w_brk = cfg["wall"]
    r_col, r_hi = cfg["roof"]
    draw_house_or_building(px, 4, 64, 52, 28, 14, w_col, w_brk, r_col, r_hi)

    # 6. Dirt road & foreground grass tufts (y=62..90)
    rd_main, rd_peb = cfg["road"]
    draw_ground_road(px, 61, 64, 82, g_top, g_dark, rd_main, rd_peb)

    # 7. Wooden crates & signpost on the road edge
    draw_crates_and_signpost(px, 12, 66)

    # Upscale 4x NEAREST NEIGHBOR -> 640x360 crisp retro pixel art
    return im.resize((640, 360), Image.Resampling.NEAREST)


def build_battle_bg(r_id, cfg):
    im = Image.new("RGBA", (GW, GH), (0, 0, 0, 255))
    px = im.load()

    # 1. Battle sky bands + clouds/stars
    draw_sky_bands(px, cfg["battle_sky"])
    draw_pixel_cloud(px, 48, 14, 12)
    draw_pixel_cloud(px, 118, 16, 15)

    # 2. Distant mountains / dungeon backdrop
    m_main, m_shade, snow = cfg["mtn"]
    draw_mountain(px, 46, 20, 62, 0.9, m_main, m_shade, snow_cap=snow)
    draw_mountain(px, 98, 16, 62, 0.95, m_main, m_shade, snow_cap=snow)
    draw_mountain(px, 138, 22, 62, 0.85, m_main, m_shade, snow_cap=snow)

    # 3. Region-specific side-scrolling dungeon landmarks with bold black outlines
    prop = cfg["battle_prop"]
    w_col, w_brk = cfg["wall"]
    r_col, r_hi = cfg["roof"]
    if prop in ("subway_pillars", "bunker_walls", "mothership_pillars", "gold_pillars"):
        for px_x in range(18, 150, 36):
            draw_pixel_rect_outlined(px, px_x, 18, px_x + 10, 63, w_col, r_hi, w_brk)
            draw_pixel_rect_outlined(px, px_x - 2, 16, px_x + 12, 21, r_col, r_hi)
    elif prop in ("silver_altar", "torii_shrine", "diamond_throne"):
        # Grand archway / torii / crystal pillars in background
        for px_x in [36, 114]:
            draw_pixel_rect_outlined(px, px_x, 22, px_x + 8, 63, r_col, r_hi, w_brk)
        draw_pixel_rect_outlined(px, 28, 18, 130, 24, r_col, r_hi, w_brk)
    elif prop == "dragon_bones":
        # Giant pixel dragon ribcage arches
        for rx in range(28, 136, 26):
            draw_pixel_rect_outlined(px, rx, 26, rx + 6, 63, (235, 242, 250, 255), (255, 255, 255, 255), (158, 175, 195, 255))
    elif prop == "volcano_lava":
        # Glowing lava river in midground
        draw_pixel_rect_outlined(px, 0, 56, GW - 1, 63, (255, 95, 20, 255), (255, 210, 50, 255), (178, 32, 10, 255))

    # 4. Left & right trees / biome rocks framing the combat road
    td, tm, th = cfg["tree"]
    draw_pixel_tree(px, 20, 63, 10, leaf_dark=td, leaf_mid=tm, leaf_hi=th)
    draw_pixel_tree(px, 142, 63, 11, leaf_dark=td, leaf_mid=tm, leaf_hi=th)

    # 5. Flat horizontal side-scrolling combat road (y=63..82) where Hero (left) & Monster (right) stand!
    g_top, g_dark = cfg["grass"]
    rd_main, rd_peb = cfg["road"]
    draw_ground_road(px, 60, 63, 82, g_top, g_dark, rd_main, rd_peb)

    return im.resize((640, 360), Image.Resampling.NEAREST)


if __name__ == "__main__":
    for r_id, cfg in THEMES.items():
        t_img = build_town_bg(r_id, cfg)
        t_path = os.path.join(REGIONS_DIR, f"town_bg_{r_id}.png")
        t_img.save(t_path)

        b_img = build_battle_bg(r_id, cfg)
        b_path = os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png")
        b_img.save(b_path)
        print(f"Region {r_id:02d}: generated 16-bit side-scrolling town_bg_{r_id}.png & battle_bg_{r_id}.png")
