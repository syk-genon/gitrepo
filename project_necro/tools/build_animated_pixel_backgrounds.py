# -*- coding: utf-8 -*-
import os, sys, math
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

REGIONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\ui\regions"
os.makedirs(REGIONS_DIR, exist_ok=True)

OL = (10, 7, 5, 255)
GW, GH = 160, 90

# 4-Frame Sway Offsets: F0(0: 기본 위치) -> F1(+1: 오른쪽 살짝 휨) -> F2(+2: 최대 휨) -> F3(+1: 돌아오는 중간 단계)
SWAY_OFFSETS = [0, 1, 2, 1]


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
    y_cur = 0
    for y_end, col in bands:
        for y in range(y_cur, min(GH, y_end)):
            for x in range(GW):
                px[x, y] = col
        y_cur = y_end


def build_clouds_strip(r_id, cloud_col=(245, 250, 255, 255), shade_col=(195, 215, 235, 255)):
    """Builds a tileable horizontal pixel cloud layer (GW x GH, upscaled 4x to 640x360) for infinite 1px scrolling."""
    im = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    px = im.load()
    clouds = [(26, 12, 13), (78, 18, 10), (132, 11, 15)]
    for cx, cy, cw in clouds:
        # Outline pass
        for dy in range(-5, 5):
            for dx in range(-cw - 1, cw + 2):
                if (dx * dx) / ((cw + 1) ** 2) + (dy * dy) / 18.0 <= 1.0:
                    x = (cx + dx) % GW
                    y = cy + dy
                    if 0 <= y < GH:
                        px[x, y] = OL
        # Fill pass
        for dy in range(-4, 4):
            for dx in range(-cw, cw + 1):
                if (dx * dx) / (cw * cw + 1) + (dy * dy) / 13.0 <= 1.0:
                    x = (cx + dx) % GW
                    y = cy + dy
                    if 0 <= y < GH:
                        px[x, y] = shade_col if dy >= 2 else cloud_col
    return im.resize((640, 360), Image.Resampling.NEAREST)


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


def draw_pixel_tree_sway(px, tx, ty_ground, r_crown, sway_dx=0, trunk_col=(110, 62, 32, 255), leaf_dark=(22, 95, 28, 255), leaf_mid=(48, 165, 42, 255), leaf_hi=(115, 225, 65, 255)):
    tw = max(2, r_crown // 3)
    th = int(r_crown * 1.2)
    for y in range(ty_ground - th, ty_ground + 1):
        for x in range(tx - tw, tx + tw + 1):
            if 0 <= x < GW and 0 <= y < GH:
                if x == tx - tw or x == tx + tw:
                    px[x, y] = OL
                else:
                    px[x, y] = trunk_col

    cy = ty_ground - th - r_crown // 2
    # Lower canopy sways by sway_dx, upper crown sways by sway_dx (or +1 on max bend)
    top_dx = sway_dx + (1 if sway_dx == 2 else 0)
    blobs = [
        (sway_dx, 0, r_crown),
        (-r_crown // 2 + sway_dx, 2, int(r_crown * 0.78)),
        (r_crown // 2 + sway_dx, 2, int(r_crown * 0.78)),
        (top_dx, -r_crown // 2, int(r_crown * 0.75)),
    ]
    for bx, by, br in blobs:
        for dy in range(-br - 1, br + 2):
            for dx in range(-br - 1, br + 2):
                if dx * dx + dy * dy <= (br + 1) ** 2:
                    x, y = tx + bx + dx, cy + by + dy
                    if 0 <= x < GW and 0 <= y < GH:
                        px[x, y] = OL
    for bx, by, br in blobs:
        for dy in range(-br, br + 1):
            for dx in range(-br, br + 1):
                if dx * dx + dy * dy <= br * br:
                    x, y = tx + bx + dx, cy + by + dy
                    if 0 <= x < GW and 0 <= y < GH:
                        if dy < -br * 0.25 and (x - sway_dx + y) % 2 == 0:
                            px[x, y] = leaf_hi
                        elif dy > br * 0.35:
                            px[x, y] = leaf_dark
                        else:
                            px[x, y] = leaf_mid


def draw_swaying_grass_blades(px, y_base, sway_dx, col_hi, col_mid):
    """Draws retro World 1-1 style grass tufts along the road borders that bend right with sway_dx."""
    for gx in range(6, GW - 6, 11):
        for blade in (-2, 0, 2):
            bx = gx + blade
            for h_step in range(1, 5):
                bend = (sway_dx * h_step) // 3
                x = bx + bend
                y = y_base - h_step
                if 0 <= x < GW and 0 <= y < GH:
                    px[x, y] = col_hi if h_step >= 3 else col_mid
                    if x - 1 >= 0 and px[x - 1, y] != col_hi:
                        px[x - 1, y] = OL


def draw_ground_road(px, y_grass, y_road_top, y_road_bot, grass_top, grass_dark, road_main, road_pebble, sway_dx=0):
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

    # Foreground swaying grass tufts along road bottom & top
    draw_swaying_grass_blades(px, y_road_top, sway_dx, grass_top, grass_dark)
    draw_swaying_grass_blades(px, GH - 1, sway_dx, grass_top, grass_dark)


def draw_house_or_building(px, hx, hy_ground, w, h, roof_h, wall_col, wall_brick, roof_col, roof_hi, sign_col=(225, 165, 70, 255), sway_dx=0):
    y_top = hy_ground - h
    # Chimney with animated smoke puff
    ch_x = hx + w - 16
    draw_pixel_rect_outlined(px, ch_x, y_top - roof_h - 4, ch_x + 6, y_top - roof_h + 2, wall_col, wall_brick)
    smoke_x = ch_x + 3 + sway_dx * 2
    smoke_y = y_top - roof_h - 7 - (sway_dx % 2)
    draw_pixel_rect_outlined(px, smoke_x, smoke_y, smoke_x + 4, smoke_y + 3, (220, 228, 238, 255))

    for y in range(y_top, hy_ground):
        for x in range(hx, hx + w):
            if 0 <= x < GW and 0 <= y < GH:
                if x == hx or x == hx + w - 1 or y == y_top or y == hy_ground - 1:
                    px[x, y] = OL
                elif (y - y_top) % 4 == 0 or ((x + ((y - y_top) // 4) * 3) % 6 == 0):
                    px[x, y] = wall_brick
                else:
                    px[x, y] = wall_col

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

    dx0 = hx + w // 2 - 5
    dx1 = hx + w // 2 + 5
    dy0 = hy_ground - 14
    draw_pixel_rect_outlined(px, dx0, dy0, dx1, hy_ground - 1, (125, 72, 32, 255), (165, 102, 48, 255), (78, 42, 18, 255))
    draw_pixel_rect_outlined(px, dx0 - 2, dy0 - 7, dx1 + 2, dy0 - 2, sign_col, (255, 215, 115, 255))


def draw_crates_and_signpost(px, gx, gy):
    draw_pixel_rect_outlined(px, gx, gy - 9, gx + 9, gy, (155, 92, 38, 255), (198, 128, 58, 255), (98, 54, 20, 255))
    draw_pixel_rect_outlined(px, gx + 10, gy - 7, gx + 18, gy, (142, 82, 32, 255), (185, 118, 52, 255), (88, 48, 18, 255))
    sx = 78
    draw_pixel_rect_outlined(px, sx, gy - 16, sx + 3, gy, (112, 64, 28, 255))
    draw_pixel_rect_outlined(px, sx - 6, gy - 15, sx + 9, gy - 9, (175, 108, 44, 255), (218, 148, 72, 255))


from build_authentic_pixel_backgrounds import THEMES


def build_town_frame(r_id, cfg, frame_idx):
    sway_dx = SWAY_OFFSETS[frame_idx % 4]
    im = Image.new("RGBA", (GW, GH), (0, 0, 0, 255))
    px = im.load()

    draw_sky_bands(px, cfg["sky"])
    m_main, m_shade, snow = cfg["mtn"]
    draw_mountain(px, 94, 22, 62, 0.85, m_main, m_shade, snow_cap=snow)
    draw_mountain(px, 124, 15, 62, 0.92, m_main, m_shade, snow_cap=snow)

    g_top, g_dark = cfg["grass"]
    for y in range(46, 65):
        for x in range(GW):
            hill_y = 48 + int(math.sin(x * 0.06 + r_id) * 3)
            if y == hill_y:
                px[x, y] = OL
            elif y > hill_y:
                px[x, y] = g_top

    td, tm, th = cfg["tree"]
    draw_pixel_tree_sway(px, 64, 62, 11, sway_dx=sway_dx, leaf_dark=td, leaf_mid=tm, leaf_hi=th)
    draw_pixel_tree_sway(px, 118, 62, 12, sway_dx=sway_dx, leaf_dark=td, leaf_mid=tm, leaf_hi=th)

    w_col, w_brk = cfg["wall"]
    r_col, r_hi = cfg["roof"]
    draw_house_or_building(px, 4, 64, 52, 28, 14, w_col, w_brk, r_col, r_hi, sway_dx=sway_dx)

    rd_main, rd_peb = cfg["road"]
    draw_ground_road(px, 61, 64, 82, g_top, g_dark, rd_main, rd_peb, sway_dx=sway_dx)
    draw_crates_and_signpost(px, 12, 66)

    return im.resize((640, 360), Image.Resampling.NEAREST)


def build_battle_frame(r_id, cfg, frame_idx):
    sway_dx = SWAY_OFFSETS[frame_idx % 4]
    im = Image.new("RGBA", (GW, GH), (0, 0, 0, 255))
    px = im.load()

    draw_sky_bands(px, cfg["battle_sky"])
    m_main, m_shade, snow = cfg["mtn"]
    draw_mountain(px, 46, 20, 62, 0.9, m_main, m_shade, snow_cap=snow)
    draw_mountain(px, 98, 16, 62, 0.95, m_main, m_shade, snow_cap=snow)
    draw_mountain(px, 138, 22, 62, 0.85, m_main, m_shade, snow_cap=snow)

    prop = cfg["battle_prop"]
    w_col, w_brk = cfg["wall"]
    r_col, r_hi = cfg["roof"]
    if prop in ("subway_pillars", "bunker_walls", "mothership_pillars", "gold_pillars"):
        for px_x in range(18, 150, 36):
            draw_pixel_rect_outlined(px, px_x, 18, px_x + 10, 63, w_col, r_hi, w_brk)
            draw_pixel_rect_outlined(px, px_x - 2, 16, px_x + 12, 21, r_col, r_hi)
            # Flickering torch/beacon on pillars per frame
            beacon_col = (255, 225, 60, 255) if frame_idx % 2 == 0 else (255, 110, 30, 255)
            draw_pixel_rect_outlined(px, px_x + 2, 24 - (frame_idx % 2), px_x + 7, 29, beacon_col)
    elif prop in ("silver_altar", "torii_shrine", "diamond_throne"):
        for px_x in [36, 114]:
            draw_pixel_rect_outlined(px, px_x, 22, px_x + 8, 63, r_col, r_hi, w_brk)
        draw_pixel_rect_outlined(px, 28, 18, 130, 24, r_col, r_hi, w_brk)
    elif prop == "dragon_bones":
        for rx in range(28, 136, 26):
            draw_pixel_rect_outlined(px, rx, 26, rx + 6, 63, (235, 242, 250, 255), (255, 255, 255, 255), (158, 175, 195, 255))
    elif prop == "volcano_lava":
        lava_hi = (255, 225, 60, 255) if frame_idx % 2 == 0 else (255, 145, 30, 255)
        draw_pixel_rect_outlined(px, 0, 56 + (frame_idx % 2), GW - 1, 63, (255, 85, 20, 255), lava_hi, (178, 32, 10, 255))

    td, tm, th = cfg["tree"]
    draw_pixel_tree_sway(px, 20, 63, 10, sway_dx=sway_dx, leaf_dark=td, leaf_mid=tm, leaf_hi=th)
    draw_pixel_tree_sway(px, 142, 63, 11, sway_dx=sway_dx, leaf_dark=td, leaf_mid=tm, leaf_hi=th)

    g_top, g_dark = cfg["grass"]
    rd_main, rd_peb = cfg["road"]
    draw_ground_road(px, 60, 63, 82, g_top, g_dark, rd_main, rd_peb, sway_dx=sway_dx)

    return im.resize((640, 360), Image.Resampling.NEAREST)


if __name__ == "__main__":
    # Generate tileable cloud layer
    cloud_strip = build_clouds_strip(1)
    cloud_strip.save(os.path.join(REGIONS_DIR, "clouds_strip.png"))

    for r_id, cfg in THEMES.items():
        for f_idx in range(4):
            t_img = build_town_frame(r_id, cfg, f_idx)
            t_img.save(os.path.join(REGIONS_DIR, f"town_bg_{r_id}_f{f_idx}.png"))
            if f_idx == 0:
                t_img.save(os.path.join(REGIONS_DIR, f"town_bg_{r_id}.png"))

            b_img = build_battle_frame(r_id, cfg, f_idx)
            b_img.save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}_f{f_idx}.png"))
            if f_idx == 0:
                b_img.save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png"))

        print(f"Region {r_id:02d}: generated 4-frame swaying town_bg_{r_id}_f0..3.png & battle_bg_{r_id}_f0..3.png")
