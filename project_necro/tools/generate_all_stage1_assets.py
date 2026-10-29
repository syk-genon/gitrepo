# -*- coding: utf-8 -*-
"""
GENERATE ALL STAGE 1 RETRO 16-BIT ASSETS
For 《목적을 잃지 않는 사령군주》 (PROJECT NECRO)
Strictly adheres to NECROMANCER_GAME_AI_BLUEPRINT.md [Section 8.2]:
- 2x supersampling (SS=2)
- draw_bezier_tube for organic curves, bones, horns, weapons & energy arcs
- apply_16bit_shading with directional bevel highlights & shadows
- add_fast_anime_outline (MaxFilter(5)) for 2px dark outer contour
- NO crude PIL geometric boxes or stick figures.
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = r"D:\workspace\GEMINI\project_necro"
SUMMONS_DIR = os.path.join(ROOT_DIR, "assets", "summons")
SKILLS_DIR = os.path.join(ROOT_DIR, "assets", "pixel_vfx", "skills")
ITEMS_SETS_DIR = os.path.join(ROOT_DIR, "assets", "ui", "items_sets")
ITEMS_UNIQUES_DIR = os.path.join(ROOT_DIR, "assets", "ui", "items_uniques")

for p in [SUMMONS_DIR, SKILLS_DIR, ITEMS_SETS_DIR, ITEMS_UNIQUES_DIR]:
    os.makedirs(p, exist_ok=True)

OUTLINE_COLOR = (20, 16, 26, 255)

def add_fast_anime_outline(im, outline_color=OUTLINE_COLOR, size=5):
    """C-accelerated 2px dark outline around RGBA sprite."""
    r, g, b, a = im.split()
    a_solid = a.point(lambda p: 255 if p > 125 else 0)
    im_solid = Image.merge("RGBA", (r, g, b, a_solid))
    dilated_a = a_solid.filter(ImageFilter.MaxFilter(size))
    outline_layer = Image.new("RGBA", im.size, outline_color)
    outline_layer.putalpha(dilated_a)
    return Image.alpha_composite(outline_layer, im_solid)

def apply_16bit_shading(im, preserve_glow=True):
    """Directional bevel highlight (1.24x) and shadow (0.72x) for authentic 16-bit depth."""
    w, h = im.size
    src = im.load()
    out = im.copy()
    dst = out.load()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = src[x, y]
            if a == 0 or (r < 35 and g < 30 and b < 40):
                continue
            if preserve_glow and r > 235 and g > 235 and b > 235:
                continue
            tl_empty = src[x - 1, y - 1][3] == 0
            br_empty = src[x + 1, y + 1][3] == 0
            if tl_empty and not br_empty:
                dst[x, y] = (min(255, int(r * 1.25) + 14), min(255, int(g * 1.25) + 14), min(255, int(b * 1.25) + 14), a)
            elif br_empty and not tl_empty:
                dst[x, y] = (int(r * 0.72), int(g * 0.72), int(b * 0.76), a)
    return out

def draw_bezier_tube(d, p0, p1, p2, p3, r_start, r_end, col_dark, col_main, col_hi, steps=32):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3)*p0[0] + 3*(mt**2)*t*p1[0] + 3*mt*(t**2)*p2[0] + (t**3)*p3[0]
        y = (mt**3)*p0[1] + 3*(mt**2)*t*p1[1] + 3*mt*(t**2)*p2[1] + (t**3)*p3[1]
        r = r_start + (r_end - r_start) * t
        pts.append((x, y, r))
    for x, y, r in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=col_dark)
    for x, y, r in pts:
        rm = max(1.0, r * 0.82)
        d.ellipse([x - rm, y - rm - r * 0.08, x + rm, y + rm - r * 0.08], fill=col_main)
    for x, y, r in pts[2:-2]:
        rh = max(0.8, r * 0.42)
        d.ellipse([x - rh, y - r * 0.55 - rh, x + rh, y - r * 0.55 + rh], fill=col_hi)

def draw_rune_star(d, cx, cy, r_outer, r_inner, color, points=5):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.pi / points * i - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=color)

print("Core generator primitives loaded successfully.")

# =========================================================================
# 1. 7대 소환수 (Minions Legion) HD 도트 생성기
# =========================================================================
def make_skeleton_warrior():
    SS = 2
    W, H = 100 * SS, 100 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 50 * SS, 52 * SS

    # 1. 망토/배경 음영
    draw_bezier_tube(d, (cx - 14*SS, cy - 8*SS), (cx - 24*SS, cy + 10*SS), (cx - 28*SS, cy + 24*SS), (cx - 22*SS, cy + 34*SS),
                     r_start=12*SS, r_end=16*SS, col_dark=(30, 22, 38, 255), col_main=(52, 38, 64, 255), col_hi=(80, 58, 98, 255))

    # 2. 다리뼈 & 발
    draw_bezier_tube(d, (cx - 8*SS, cy + 18*SS), (cx - 10*SS, cy + 26*SS), (cx - 10*SS, cy + 34*SS), (cx - 8*SS, cy + 40*SS),
                     r_start=5*SS, r_end=4*SS, col_dark=(130, 120, 105, 255), col_main=(210, 200, 185, 255), col_hi=(255, 250, 240, 255))
    draw_bezier_tube(d, (cx + 8*SS, cy + 18*SS), (cx + 10*SS, cy + 26*SS), (cx + 12*SS, cy + 34*SS), (cx + 14*SS, cy + 40*SS),
                     r_start=5*SS, r_end=4*SS, col_dark=(130, 120, 105, 255), col_main=(210, 200, 185, 255), col_hi=(255, 250, 240, 255))

    # 3. 흉곽 (Ribcage) & 척추
    draw_bezier_tube(d, (cx, cy - 6*SS), (cx, cy + 4*SS), (cx, cy + 12*SS), (cx, cy + 18*SS),
                     r_start=8*SS, r_end=7*SS, col_dark=(110, 100, 90, 255), col_main=(190, 180, 165, 255), col_hi=(245, 240, 230, 255))
    # 갈비뼈 3단
    for dy, r_len in [(-2*SS, 14*SS), (4*SS, 16*SS), (10*SS, 13*SS)]:
        draw_bezier_tube(d, (cx - r_len, cy + dy), (cx - r_len*0.6, cy + dy + 2*SS), (cx + r_len*0.6, cy + dy + 2*SS), (cx + r_len, cy + dy),
                         r_start=3*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(220, 210, 195, 255), col_hi=(255, 250, 240, 255))
    # 흉곽 내부 영혼석 (녹색 핵)
    d.ellipse([cx - 5*SS, cy + 2*SS, cx + 5*SS, cy + 10*SS], fill=(0, 255, 170, 220))
    d.ellipse([cx - 2*SS, cy + 4*SS, cx + 2*SS, cy + 8*SS], fill=(220, 255, 240, 255))

    # 4. 왼팔 & 낡은 놋쇠 룬 방패 (좌측)
    draw_bezier_tube(d, (cx - 12*SS, cy - 2*SS), (cx - 18*SS, cy + 6*SS), (cx - 24*SS, cy + 10*SS), (cx - 26*SS, cy + 14*SS),
                     r_start=4*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(205, 195, 180, 255), col_hi=(250, 245, 235, 255))
    # 방패 본체 (중후한 타원형 목판/놋쇠 방패)
    sh_x, sh_y = cx - 28*SS, cy + 12*SS
    d.ellipse([sh_x - 14*SS, sh_y - 20*SS, sh_x + 14*SS, sh_y + 20*SS], fill=(35, 26, 22, 255))
    d.ellipse([sh_x - 12*SS, sh_y - 18*SS, sh_x + 12*SS, sh_y + 18*SS], outline=(212, 163, 56, 255), width=3*SS)
    d.ellipse([sh_x - 7*SS, sh_y - 8*SS, sh_x + 7*SS, sh_y + 8*SS], fill=(70, 52, 42, 255), outline=(120, 90, 60, 255), width=2*SS)
    d.ellipse([sh_x - 4*SS, sh_y - 4*SS, sh_x + 4*SS, sh_y + 4*SS], fill=(0, 255, 170, 255)) # 방패 중앙 영혼보석

    # 5. 오른팔 & 룬 뼈검 (우측으로 치켜듦)
    draw_bezier_tube(d, (cx + 12*SS, cy - 2*SS), (cx + 18*SS, cy + 4*SS), (cx + 24*SS, cy + 8*SS), (cx + 28*SS, cy + 12*SS),
                     r_start=4*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(205, 195, 180, 255), col_hi=(250, 245, 235, 255))
    # 뼈검 칼날 (우상향 베지어 곡선)
    draw_bezier_tube(d, (cx + 26*SS, cy + 12*SS), (cx + 34*SS, cy + 2*SS), (cx + 40*SS, cy - 12*SS), (cx + 44*SS, cy - 28*SS),
                     r_start=6*SS, r_end=2*SS, col_dark=(140, 130, 115, 255), col_main=(230, 225, 210, 255), col_hi=(255, 255, 250, 255))
    # 칼날 영혼광 (에메랄드 룬 선)
    d.line([(cx + 28*SS, cy + 10*SS), (cx + 43*SS, cy - 26*SS)], fill=(0, 255, 170, 240), width=2*SS)

    # 6. 두개골 (Skull) & 녹색 영혼 불꽃 안광
    draw_bezier_tube(d, (cx - 2*SS, cy - 12*SS), (cx, cy - 20*SS), (cx, cy - 28*SS), (cx, cy - 32*SS),
                     r_start=13*SS, r_end=15*SS, col_dark=(140, 130, 115, 255), col_main=(230, 220, 205, 255), col_hi=(255, 255, 250, 255))
    # 턱뼈
    draw_bezier_tube(d, (cx - 6*SS, cy - 14*SS), (cx - 4*SS, cy - 10*SS), (cx + 4*SS, cy - 10*SS), (cx + 6*SS, cy - 14*SS),
                     r_start=4*SS, r_end=4*SS, col_dark=(120, 110, 95, 255), col_main=(190, 185, 170, 255), col_hi=(240, 235, 220, 255))
    # 눈구멍 및 영혼 불꽃
    for ex in [cx - 6*SS, cx + 5*SS]:
        d.ellipse([ex - 4*SS, cy - 24*SS, ex + 4*SS, cy - 17*SS], fill=(12, 10, 15, 255))
        d.ellipse([ex - 2*SS, cy - 23*SS, ex + 2*SS, cy - 18*SS], fill=(0, 255, 170, 255))
        d.point([(ex, cy - 21*SS)], fill=(255, 255, 255, 255))

    # 7. 철제 어깨 갑옷 (Pauldron)
    draw_bezier_tube(d, (cx - 16*SS, cy - 8*SS), (cx - 18*SS, cy - 4*SS), (cx - 14*SS, cy + 2*SS), (cx - 10*SS, cy + 2*SS),
                     r_start=7*SS, r_end=5*SS, col_dark=(40, 42, 50, 255), col_main=(90, 95, 110, 255), col_hi=(160, 170, 195, 255))
    draw_bezier_tube(d, (cx + 16*SS, cy - 8*SS), (cx + 18*SS, cy - 4*SS), (cx + 14*SS, cy + 2*SS), (cx + 10*SS, cy + 2*SS),
                     r_start=7*SS, r_end=5*SS, col_dark=(40, 42, 50, 255), col_main=(90, 95, 110, 255), col_hi=(160, 170, 195, 255))

    im = apply_16bit_shading(im)
    im = im.resize((100, 100), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_skeleton_warrior.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

def make_skeleton_archer():
    SS = 2
    W, H = 100 * SS, 100 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 48 * SS, 52 * SS

    # 1. 보라색 누더기 망토
    draw_bezier_tube(d, (cx - 12*SS, cy - 14*SS), (cx - 24*SS, cy + 4*SS), (cx - 26*SS, cy + 24*SS), (cx - 18*SS, cy + 38*SS),
                     r_start=14*SS, r_end=16*SS, col_dark=(45, 22, 60, 255), col_main=(82, 42, 108, 255), col_hi=(130, 72, 168, 255))

    # 2. 다리뼈
    draw_bezier_tube(d, (cx - 7*SS, cy + 18*SS), (cx - 9*SS, cy + 28*SS), (cx - 9*SS, cy + 36*SS), (cx - 7*SS, cy + 42*SS),
                     r_start=4*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(210, 200, 185, 255), col_hi=(255, 250, 240, 255))
    draw_bezier_tube(d, (cx + 7*SS, cy + 18*SS), (cx + 9*SS, cy + 28*SS), (cx + 11*SS, cy + 36*SS), (cx + 13*SS, cy + 42*SS),
                     r_start=4*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(210, 200, 185, 255), col_hi=(255, 250, 240, 255))

    # 3. 등에 멘 화살통 & 화살깃
    draw_bezier_tube(d, (cx - 14*SS, cy - 6*SS), (cx - 18*SS, cy + 4*SS), (cx - 20*SS, cy + 16*SS), (cx - 22*SS, cy + 26*SS),
                     r_start=6*SS, r_end=5*SS, col_dark=(60, 42, 28, 255), col_main=(120, 80, 50, 255), col_hi=(175, 125, 80, 255))
    # 깃털 3개
    for ox, oy in [(-18*SS, -12*SS), (-15*SS, -15*SS), (-12*SS, -11*SS)]:
        d.line([(cx + ox, cy + oy), (cx + ox - 4*SS, cy + oy - 8*SS)], fill=(0, 240, 255, 255), width=3*SS)

    # 4. 척추 & 흉곽
    draw_bezier_tube(d, (cx, cy - 6*SS), (cx, cy + 6*SS), (cx, cy + 14*SS), (cx, cy + 18*SS),
                     r_start=7*SS, r_end=6*SS, col_dark=(110, 100, 90, 255), col_main=(190, 180, 165, 255), col_hi=(245, 240, 230, 255))
    for dy, r_len in [(-1*SS, 12*SS), (5*SS, 14*SS), (11*SS, 11*SS)]:
        draw_bezier_tube(d, (cx - r_len, cy + dy), (cx - r_len*0.6, cy + dy + 2*SS), (cx + r_len*0.6, cy + dy + 2*SS), (cx + r_len, cy + dy),
                         r_start=3*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(220, 210, 195, 255), col_hi=(255, 250, 240, 255))

    # 5. 팔과 대형 뼈 활 (Bone Recurve Bow)
    # 활대 곡선 (우측 전방으로 호를 그림)
    draw_bezier_tube(d, (cx + 26*SS, cy - 32*SS), (cx + 42*SS, cy - 14*SS), (cx + 42*SS, cy + 14*SS), (cx + 26*SS, cy + 32*SS),
                     r_start=5*SS, r_end=5*SS, col_dark=(130, 120, 105, 255), col_main=(225, 215, 200, 255), col_hi=(255, 255, 245, 255))
    # 시위 (빛나는 시안 영혼 활시위)
    d.line([(cx + 26*SS, cy - 30*SS), (cx + 16*SS, cy), (cx + 26*SS, cy + 30*SS)], fill=(0, 240, 255, 240), width=2*SS)
    # 조준된 영혼 화살
    d.line([(cx + 14*SS, cy), (cx + 48*SS, cy)], fill=(0, 255, 255, 255), width=4*SS)
    d.polygon([(cx + 48*SS, cy - 4*SS), (cx + 56*SS, cy), (cx + 48*SS, cy + 4*SS)], fill=(220, 255, 255, 255))

    # 왼팔 (활대 지탱)
    draw_bezier_tube(d, (cx + 8*SS, cy - 2*SS), (cx + 18*SS, cy), (cx + 28*SS, cy), (cx + 36*SS, cy),
                     r_start=4*SS, r_end=3*SS, col_dark=(130, 120, 105, 255), col_main=(205, 195, 180, 255), col_hi=(250, 245, 235, 255))

    # 6. 두개골 & 보라색 두건 (Hood)
    draw_bezier_tube(d, (cx - 2*SS, cy - 12*SS), (cx, cy - 20*SS), (cx, cy - 28*SS), (cx, cy - 32*SS),
                     r_start=13*SS, r_end=15*SS, col_dark=(140, 130, 115, 255), col_main=(230, 220, 205, 255), col_hi=(255, 255, 250, 255))
    # 두건 덮개
    draw_bezier_tube(d, (cx - 16*SS, cy - 20*SS), (cx - 10*SS, cy - 38*SS), (cx + 10*SS, cy - 38*SS), (cx + 14*SS, cy - 22*SS),
                     r_start=9*SS, r_end=8*SS, col_dark=(45, 22, 60, 255), col_main=(90, 45, 118, 255), col_hi=(145, 80, 185, 255))
    # 눈구멍 및 시안 안광
    for ex in [cx - 5*SS, cx + 5*SS]:
        d.ellipse([ex - 4*SS, cy - 23*SS, ex + 4*SS, cy - 17*SS], fill=(12, 10, 15, 255))
        d.ellipse([ex - 2*SS, cy - 22*SS, ex + 2*SS, cy - 18*SS], fill=(0, 240, 255, 255))
        d.point([(ex, cy - 20*SS)], fill=(255, 255, 255, 255))

    im = apply_16bit_shading(im)
    im = im.resize((100, 100), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_skeleton_archer.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

def make_skeleton_mage():
    SS = 2
    W, H = 100 * SS, 100 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 46 * SS, 52 * SS

    # 1. 흑마도사 로브 (Robe) 하단 넓은 자락
    draw_bezier_tube(d, (cx, cy), (cx - 16*SS, cy + 18*SS), (cx - 24*SS, cy + 32*SS), (cx - 22*SS, cy + 42*SS),
                     r_start=12*SS, r_end=20*SS, col_dark=(20, 14, 30, 255), col_main=(44, 28, 62, 255), col_hi=(78, 48, 108, 255))
    draw_bezier_tube(d, (cx, cy), (cx + 12*SS, cy + 18*SS), (cx + 18*SS, cy + 32*SS), (cx + 16*SS, cy + 42*SS),
                     r_start=12*SS, r_end=18*SS, col_dark=(20, 14, 30, 255), col_main=(44, 28, 62, 255), col_hi=(78, 48, 108, 255))
    # 황금 두석 장식단
    d.arc([cx - 24*SS, cy + 34*SS, cx + 18*SS, cy + 44*SS], start=10, end=170, fill=(212, 163, 56, 255), width=3*SS)

    # 2. 리치 두개골 & 황금 서클릿 티아라
    draw_bezier_tube(d, (cx, cy - 14*SS), (cx, cy - 22*SS), (cx, cy - 28*SS), (cx, cy - 32*SS),
                     r_start=13*SS, r_end=15*SS, col_dark=(140, 130, 115, 255), col_main=(230, 220, 205, 255), col_hi=(255, 255, 250, 255))
    # 황금 티아라
    d.polygon([(cx - 16*SS, cy - 30*SS), (cx - 18*SS, cy - 42*SS), (cx - 8*SS, cy - 36*SS),
               (cx, cy - 46*SS), (cx + 8*SS, cy - 36*SS), (cx + 18*SS, cy - 42*SS), (cx + 16*SS, cy - 30*SS)],
              fill=(220, 175, 45, 255))
    d.ellipse([cx - 3*SS, cy - 39*SS, cx + 3*SS, cy - 33*SS], fill=(0, 255, 170, 255))

    # 안광 (녹색 영혼불)
    for ex in [cx - 6*SS, cx + 5*SS]:
        d.ellipse([ex - 4*SS, cy - 24*SS, ex + 4*SS, cy - 17*SS], fill=(12, 10, 15, 255))
        d.ellipse([ex - 2*SS, cy - 23*SS, ex + 2*SS, cy - 18*SS], fill=(0, 255, 170, 255))
        d.point([(ex, cy - 21*SS)], fill=(255, 255, 255, 255))

    # 3. 우측 대형 사령 지팡이 (Skull Staff)
    st_x = cx + 28*SS
    # 지팡이 자루
    draw_bezier_tube(d, (st_x, cy + 42*SS), (st_x, cy + 10*SS), (st_x, cy - 14*SS), (st_x, cy - 30*SS),
                     r_start=5*SS, r_end=4*SS, col_dark=(42, 28, 20, 255), col_main=(95, 65, 45, 255), col_hi=(155, 110, 75, 255))
    # 지팡이 꼭대기 미니 해골 머리
    draw_bezier_tube(d, (st_x, cy - 30*SS), (st_x, cy - 34*SS), (st_x, cy - 38*SS), (st_x, cy - 42*SS),
                     r_start=7*SS, r_end=8*SS, col_dark=(130, 120, 105, 255), col_main=(220, 215, 200, 255), col_hi=(255, 255, 245, 255))
    # 지팡이 상공 소용돌이치는 보라/청록 마력구
    d.ellipse([st_x - 12*SS, cy - 56*SS, st_x + 12*SS, cy - 32*SS], outline=(200, 80, 255, 200), width=3*SS)
    d.ellipse([st_x - 8*SS, cy - 52*SS, st_x + 8*SS, cy - 36*SS], fill=(0, 255, 170, 220))
    d.ellipse([st_x - 4*SS, cy - 48*SS, st_x + 4*SS, cy - 40*SS], fill=(255, 255, 255, 255))

    im = apply_16bit_shading(im)
    im = im.resize((100, 100), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_skeleton_mage.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

def make_death_knight():
    SS = 2
    W, H = 110 * SS, 110 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 52 * SS, 56 * SS

    # 1. 칠흑 망토 (Black Abyss Cloak)
    draw_bezier_tube(d, (cx - 16*SS, cy - 10*SS), (cx - 28*SS, cy + 12*SS), (cx - 32*SS, cy + 30*SS), (cx - 26*SS, cy + 44*SS),
                     r_start=15*SS, r_end=18*SS, col_dark=(15, 10, 20, 255), col_main=(35, 24, 45, 255), col_hi=(65, 45, 85, 255))

    # 2. 중장갑 판금 다리 (Heavy Armored Greaves)
    draw_bezier_tube(d, (cx - 9*SS, cy + 16*SS), (cx - 12*SS, cy + 28*SS), (cx - 12*SS, cy + 38*SS), (cx - 9*SS, cy + 46*SS),
                     r_start=7*SS, r_end=6*SS, col_dark=(25, 25, 32, 255), col_main=(55, 58, 70, 255), col_hi=(115, 120, 140, 255))
    draw_bezier_tube(d, (cx + 9*SS, cy + 16*SS), (cx + 12*SS, cy + 28*SS), (cx + 15*SS, cy + 38*SS), (cx + 18*SS, cy + 46*SS),
                     r_start=7*SS, r_end=6*SS, col_dark=(25, 25, 32, 255), col_main=(55, 58, 70, 255), col_hi=(115, 120, 140, 255))

    # 3. 흉갑 (Abyssal Breastplate with Crimson Runes)
    draw_bezier_tube(d, (cx, cy - 6*SS), (cx, cy + 4*SS), (cx, cy + 12*SS), (cx, cy + 18*SS),
                     r_start=14*SS, r_end=12*SS, col_dark=(22, 22, 28, 255), col_main=(50, 52, 65, 255), col_hi=(100, 105, 125, 255))
    # 진홍 룬 문양
    d.line([(cx - 6*SS, cy + 2*SS), (cx, cy + 10*SS), (cx + 6*SS, cy + 2*SS)], fill=(255, 40, 90, 255), width=3*SS)

    # 4. 거대 가시 견갑 (Spiked Pauldrons)
    draw_bezier_tube(d, (cx - 18*SS, cy - 8*SS), (cx - 24*SS, cy - 18*SS), (cx - 28*SS, cy - 24*SS), (cx - 22*SS, cy - 22*SS),
                     r_start=11*SS, r_end=5*SS, col_dark=(20, 20, 25, 255), col_main=(60, 62, 75, 255), col_hi=(130, 135, 155, 255))
    draw_bezier_tube(d, (cx + 18*SS, cy - 8*SS), (cx + 24*SS, cy - 18*SS), (cx + 28*SS, cy - 24*SS), (cx + 22*SS, cy - 22*SS),
                     r_start=11*SS, r_end=5*SS, col_dark=(20, 20, 25, 255), col_main=(60, 62, 75, 255), col_hi=(130, 135, 155, 255))

    # 5. 오른손 거대 흑염 대검 (Blackflame Greatsword)
    draw_bezier_tube(d, (cx + 22*SS, cy + 16*SS), (cx + 32*SS, cy + 4*SS), (cx + 40*SS, cy - 16*SS), (cx + 46*SS, cy - 38*SS),
                     r_start=10*SS, r_end=4*SS, col_dark=(18, 15, 22, 255), col_main=(45, 40, 52, 255), col_hi=(95, 85, 110, 255))
    # 칼날을 휘감은 흑염 & 진홍 불꽃
    d.line([(cx + 24*SS, cy + 14*SS), (cx + 45*SS, cy - 36*SS)], fill=(255, 20, 70, 255), width=4*SS)
    d.line([(cx + 26*SS, cy + 12*SS), (cx + 44*SS, cy - 34*SS)], fill=(255, 150, 50, 200), width=2*SS)

    # 6. 듀라한 흑철 뿔투구 (Horned Helm with Crimson Eye Slit)
    draw_bezier_tube(d, (cx, cy - 12*SS), (cx, cy - 20*SS), (cx, cy - 28*SS), (cx, cy - 32*SS),
                     r_start=14*SS, r_end=15*SS, col_dark=(20, 20, 26, 255), col_main=(52, 54, 68, 255), col_hi=(115, 120, 142, 255))
    # 좌우 굽은 뿔
    draw_bezier_tube(d, (cx - 12*SS, cy - 30*SS), (cx - 22*SS, cy - 36*SS), (cx - 26*SS, cy - 44*SS), (cx - 20*SS, cy - 48*SS),
                     r_start=6*SS, r_end=3*SS, col_dark=(35, 15, 25, 255), col_main=(90, 40, 60, 255), col_hi=(160, 75, 110, 255))
    draw_bezier_tube(d, (cx + 12*SS, cy - 30*SS), (cx + 22*SS, cy - 36*SS), (cx + 26*SS, cy - 44*SS), (cx + 20*SS, cy - 48*SS),
                     r_start=6*SS, r_end=3*SS, col_dark=(35, 15, 25, 255), col_main=(90, 40, 60, 255), col_hi=(160, 75, 110, 255))
    # 가로로 찢어진 진홍 안광 슬릿
    d.line([(cx - 9*SS, cy - 22*SS), (cx + 9*SS, cy - 22*SS)], fill=(255, 0, 60, 255), width=3*SS)
    d.line([(cx - 4*SS, cy - 22*SS), (cx + 4*SS, cy - 22*SS)], fill=(255, 220, 220, 255), width=2*SS)

    im = apply_16bit_shading(im)
    im = im.resize((110, 110), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_death_knight.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

def make_frost_dragon():
    SS = 2
    W, H = 140 * SS, 140 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 68 * SS, 70 * SS

    # 1. 빙룡의 거대한 얼음 날개 (Ice Wings with Crystalline Veins)
    # 좌측 날개
    pts_l = [(cx - 10*SS, cy - 10*SS), (cx - 40*SS, cy - 45*SS), (cx - 62*SS, cy - 38*SS), (cx - 48*SS, cy - 10*SS), (cx - 24*SS, cy + 4*SS)]
    d.polygon(pts_l, fill=(25, 85, 125, 220))
    draw_bezier_tube(d, (cx - 8*SS, cy - 8*SS), (cx - 36*SS, cy - 40*SS), (cx - 56*SS, cy - 36*SS), (cx - 62*SS, cy - 38*SS),
                     r_start=6*SS, r_end=3*SS, col_dark=(30, 110, 160, 255), col_main=(80, 200, 255, 255), col_hi=(220, 250, 255, 255))
    # 우측 날개
    pts_r = [(cx + 10*SS, cy - 10*SS), (cx + 40*SS, cy - 45*SS), (cx + 62*SS, cy - 38*SS), (cx + 48*SS, cy - 10*SS), (cx + 24*SS, cy + 4*SS)]
    d.polygon(pts_r, fill=(25, 85, 125, 220))
    draw_bezier_tube(d, (cx + 8*SS, cy - 8*SS), (cx + 36*SS, cy - 40*SS), (cx + 56*SS, cy - 36*SS), (cx + 62*SS, cy - 38*SS),
                     r_start=6*SS, r_end=3*SS, col_dark=(30, 110, 160, 255), col_main=(80, 200, 255, 255), col_hi=(220, 250, 255, 255))

    # 2. 꼬리뼈 (Curved Spine Tail)
    draw_bezier_tube(d, (cx, cy + 20*SS), (cx - 15*SS, cy + 34*SS), (cx - 25*SS, cy + 48*SS), (cx - 15*SS, cy + 58*SS),
                     r_start=7*SS, r_end=3*SS, col_dark=(40, 100, 140, 255), col_main=(120, 210, 250, 255), col_hi=(240, 255, 255, 255))

    # 3. 얼음 갈비뼈 & 시안 심장핵
    draw_bezier_tube(d, (cx, cy - 10*SS), (cx, cy + 4*SS), (cx, cy + 14*SS), (cx, cy + 22*SS),
                     r_start=12*SS, r_end=9*SS, col_dark=(35, 95, 135, 255), col_main=(100, 200, 245, 255), col_hi=(230, 250, 255, 255))
    d.ellipse([cx - 8*SS, cy - 2*SS, cx + 8*SS, cy + 12*SS], fill=(0, 240, 255, 240))
    d.ellipse([cx - 4*SS, cy + 1*SS, cx + 4*SS, cy + 8*SS], fill=(255, 255, 255, 255))

    # 4. 용의 두개골 & 빙룡 뿔
    draw_bezier_tube(d, (cx, cy - 14*SS), (cx + 4*SS, cy - 24*SS), (cx + 8*SS, cy - 32*SS), (cx + 12*SS, cy - 38*SS),
                     r_start=13*SS, r_end=15*SS, col_dark=(40, 110, 155, 255), col_main=(125, 215, 255, 255), col_hi=(240, 255, 255, 255))
    # 뾰족한 주둥이 (우향)
    d.polygon([(cx + 6*SS, cy - 42*SS), (cx + 28*SS, cy - 36*SS), (cx + 14*SS, cy - 30*SS)], fill=(180, 235, 255, 255))
    # 뒤로 뻗은 얼음 뿔
    draw_bezier_tube(d, (cx + 2*SS, cy - 36*SS), (cx - 14*SS, cy - 46*SS), (cx - 28*SS, cy - 54*SS), (cx - 36*SS, cy - 56*SS),
                     r_start=7*SS, r_end=2*SS, col_dark=(25, 80, 120, 255), col_main=(80, 195, 255, 255), col_hi=(230, 255, 255, 255))
    # 푸른 안광
    d.ellipse([cx + 10*SS, cy - 38*SS, cx + 16*SS, cy - 33*SS], fill=(0, 255, 240, 255))
    d.point([(cx + 13*SS, cy - 35*SS)], fill=(255, 255, 255, 255))

    im = apply_16bit_shading(im)
    im = im.resize((140, 140), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_frost_dragon.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

def make_shadow_clone():
    SS = 2
    W, H = 100 * SS, 100 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 50 * SS, 52 * SS

    # 1. 심연 그림자 연기 아우라 (Dark Violet Smoky Aura)
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        ox = int(22*SS * math.cos(rad))
        oy = int(22*SS * math.sin(rad))
        d.ellipse([cx + ox - 14*SS, cy + oy - 14*SS, cx + ox + 14*SS, cy + oy + 14*SS], fill=(60, 20, 85, 90))

    # 2. 그림자 닌자 몸체 & 다리
    draw_bezier_tube(d, (cx - 8*SS, cy + 14*SS), (cx - 10*SS, cy + 26*SS), (cx - 12*SS, cy + 34*SS), (cx - 8*SS, cy + 42*SS),
                     r_start=6*SS, r_end=5*SS, col_dark=(15, 10, 25, 255), col_main=(38, 20, 52, 255), col_hi=(85, 45, 115, 255))
    draw_bezier_tube(d, (cx + 8*SS, cy + 14*SS), (cx + 10*SS, cy + 26*SS), (cx + 14*SS, cy + 34*SS), (cx + 16*SS, cy + 42*SS),
                     r_start=6*SS, r_end=5*SS, col_dark=(15, 10, 25, 255), col_main=(38, 20, 52, 255), col_hi=(85, 45, 115, 255))
    draw_bezier_tube(d, (cx, cy - 6*SS), (cx, cy + 4*SS), (cx, cy + 10*SS), (cx, cy + 16*SS),
                     r_start=11*SS, r_end=9*SS, col_dark=(18, 12, 28, 255), col_main=(45, 25, 65, 255), col_hi=(98, 55, 135, 255))

    # 3. 쌍 단검 (Dual Shadow Daggers)
    # 왼손 역검
    draw_bezier_tube(d, (cx - 16*SS, cy + 8*SS), (cx - 24*SS, cy + 14*SS), (cx - 30*SS, cy + 22*SS), (cx - 34*SS, cy + 32*SS),
                     r_start=4*SS, r_end=2*SS, col_dark=(40, 20, 60, 255), col_main=(180, 50, 255, 255), col_hi=(240, 180, 255, 255))
    # 오른손 순검 (전방 조준)
    draw_bezier_tube(d, (cx + 16*SS, cy + 8*SS), (cx + 26*SS, cy + 4*SS), (cx + 36*SS, cy - 4*SS), (cx + 44*SS, cy - 14*SS),
                     r_start=4*SS, r_end=2*SS, col_dark=(40, 20, 60, 255), col_main=(180, 50, 255, 255), col_hi=(240, 180, 255, 255))

    # 4. 닌자 두건 & 붉은 눈 (Crimson Glowing Eyes)
    draw_bezier_tube(d, (cx, cy - 12*SS), (cx, cy - 18*SS), (cx, cy - 26*SS), (cx, cy - 30*SS),
                     r_start=13*SS, r_end=14*SS, col_dark=(15, 10, 22, 255), col_main=(42, 22, 60, 255), col_hi=(95, 50, 130, 255))
    # 붉은 안광 슬릿
    for ex in [cx - 6*SS, cx + 5*SS]:
        d.ellipse([ex - 4*SS, cy - 22*SS, ex + 4*SS, cy - 17*SS], fill=(255, 20, 80, 255))
        d.point([(ex, cy - 19*SS)], fill=(255, 220, 230, 255))

    im = apply_16bit_shading(im)
    im = im.resize((100, 100), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_shadow_clone.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

def make_holy_guardian():
    SS = 2
    W, H = 100 * SS, 100 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 50 * SS, 54 * SS

    # 1. 황금 천사 날개 (Golden Angel Wings)
    pts_l = [(cx - 8*SS, cy - 12*SS), (cx - 36*SS, cy - 34*SS), (cx - 44*SS, cy - 16*SS), (cx - 24*SS, cy + 10*SS)]
    d.polygon(pts_l, fill=(240, 210, 120, 230))
    pts_r = [(cx + 8*SS, cy - 12*SS), (cx + 36*SS, cy - 34*SS), (cx + 44*SS, cy - 16*SS), (cx + 24*SS, cy + 10*SS)]
    d.polygon(pts_r, fill=(240, 210, 120, 230))
    draw_bezier_tube(d, (cx - 6*SS, cy - 10*SS), (cx - 28*SS, cy - 30*SS), (cx - 40*SS, cy - 18*SS), (cx - 42*SS, cy - 14*SS),
                     r_start=5*SS, r_end=2*SS, col_dark=(180, 140, 40, 255), col_main=(255, 225, 90, 255), col_hi=(255, 255, 210, 255))
    draw_bezier_tube(d, (cx + 6*SS, cy - 10*SS), (cx + 28*SS, cy - 30*SS), (cx + 40*SS, cy - 18*SS), (cx + 42*SS, cy - 14*SS),
                     r_start=5*SS, r_end=2*SS, col_dark=(180, 140, 40, 255), col_main=(255, 225, 90, 255), col_hi=(255, 255, 210, 255))

    # 2. 백금 성기사 갑옷 (White-Gold Paladin Armor)
    draw_bezier_tube(d, (cx - 7*SS, cy + 16*SS), (cx - 9*SS, cy + 26*SS), (cx - 9*SS, cy + 34*SS), (cx - 7*SS, cy + 42*SS),
                     r_start=6*SS, r_end=5*SS, col_dark=(150, 150, 160, 255), col_main=(230, 230, 240, 255), col_hi=(255, 255, 255, 255))
    draw_bezier_tube(d, (cx + 7*SS, cy + 16*SS), (cx + 9*SS, cy + 26*SS), (cx + 11*SS, cy + 34*SS), (cx + 13*SS, cy + 42*SS),
                     r_start=6*SS, r_end=5*SS, col_dark=(150, 150, 160, 255), col_main=(230, 230, 240, 255), col_hi=(255, 255, 255, 255))
    draw_bezier_tube(d, (cx, cy - 6*SS), (cx, cy + 4*SS), (cx, cy + 10*SS), (cx, cy + 16*SS),
                     r_start=12*SS, r_end=10*SS, col_dark=(160, 160, 175, 255), col_main=(240, 240, 250, 255), col_hi=(255, 255, 255, 255))
    # 황금 십자가 문양
    d.line([(cx, cy + 2*SS), (cx, cy + 12*SS)], fill=(255, 208, 0, 255), width=3*SS)
    d.line([(cx - 5*SS, cy + 5*SS), (cx + 5*SS, cy + 5*SS)], fill=(255, 208, 0, 255), width=3*SS)

    # 3. 우측 황금 십자 석장 (Holy Cross Spear)
    sp_x = cx + 28*SS
    draw_bezier_tube(d, (sp_x, cy + 40*SS), (sp_x, cy + 10*SS), (sp_x, cy - 14*SS), (sp_x, cy - 36*SS),
                     r_start=4*SS, r_end=3*SS, col_dark=(160, 120, 30, 255), col_main=(235, 195, 60, 255), col_hi=(255, 250, 180, 255))
    d.polygon([(sp_x - 8*SS, cy - 36*SS), (sp_x, cy - 48*SS), (sp_x + 8*SS, cy - 36*SS)], fill=(255, 240, 120, 255))

    # 4. 성기사 투구 & 천사 헤일로 (Angel Halo)
    draw_bezier_tube(d, (cx, cy - 12*SS), (cx, cy - 18*SS), (cx, cy - 26*SS), (cx, cy - 30*SS),
                     r_start=12*SS, r_end=14*SS, col_dark=(150, 150, 165, 255), col_main=(230, 230, 245, 255), col_hi=(255, 255, 255, 255))
    # 황금 천사 헤일로 링
    d.ellipse([cx - 16*SS, cy - 46*SS, cx + 16*SS, cy - 38*SS], outline=(255, 215, 0, 255), width=3*SS)
    d.ellipse([cx - 14*SS, cy - 45*SS, cx + 14*SS, cy - 39*SS], outline=(255, 255, 200, 255), width=2*SS)

    im = apply_16bit_shading(im)
    im = im.resize((100, 100), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SUMMONS_DIR, "minion_holy_guardian.png")
    im.save(out_path, "PNG")
    print(f"[SAVED] {out_path} ({os.path.getsize(out_path)} bytes)")

# 실행: 7대 소환수 생성
print("--- Generating 7 Summon Minions ---")
make_skeleton_warrior()
make_skeleton_archer()
make_skeleton_mage()
make_death_knight()
make_frost_dragon()
make_shadow_clone()
make_holy_guardian()

# =========================================================================
# 2. 전 12개 직업 72종 전용 16비트 스킬 도트 VFX 생성기
# =========================================================================

SKILL_SPECS = [
    # Necromancer
    ("vfx_necro_1", "necro", "summon", (0, 255, 170), (20, 45, 35)),
    ("vfx_necro_2", "necro", "corpse_burst", (255, 40, 100), (45, 15, 25)),
    ("vfx_necro_3", "necro", "projectile", (230, 240, 230), (0, 255, 170)),
    ("vfx_necro_4", "necro", "barrier", (0, 255, 170), (30, 60, 50)),
    ("vfx_necro_5", "necro", "summon_elite", (160, 40, 255), (255, 30, 80)),
    ("vfx_necro_ult", "necro", "cataclysm", (0, 255, 220), (20, 20, 40)),

    # Guardian
    ("vfx_guard_1", "guard", "barrier", (0, 240, 255), (30, 80, 120)),
    ("vfx_guard_2", "guard", "bash", (0, 240, 255), (255, 215, 0)),
    ("vfx_guard_3", "guard", "slam", (212, 163, 56), (90, 65, 40)),
    ("vfx_guard_4", "guard", "barrier", (255, 215, 0), (0, 240, 255)),
    ("vfx_guard_5", "guard", "shout", (255, 200, 50), (255, 100, 30)),
    ("vfx_guard_ult", "guard", "cataclysm", (255, 220, 50), (0, 240, 255)),

    # Storm Wizard
    ("vfx_storm_1", "storm", "rune_grid", (200, 80, 255), (100, 40, 180)),
    ("vfx_storm_2", "storm", "chain_lightning", (180, 120, 255), (255, 255, 255)),
    ("vfx_storm_3", "storm", "meteor", (255, 100, 30), (255, 220, 50)),
    ("vfx_storm_4", "storm", "blink", (180, 80, 255), (0, 255, 255)),
    ("vfx_storm_5", "storm", "artillery", (255, 160, 40), (200, 60, 255)),
    ("vfx_storm_ult", "storm", "cataclysm", (200, 100, 255), (0, 240, 255)),

    # Sniper
    ("vfx_snip_1", "snip", "crosshair", (255, 60, 60), (255, 200, 50)),
    ("vfx_snip_2", "snip", "railgun", (255, 160, 30), (255, 255, 200)),
    ("vfx_snip_3", "snip", "explosive", (255, 90, 30), (200, 40, 20)),
    ("vfx_snip_4", "snip", "smoke", (100, 100, 110), (0, 255, 170)),
    ("vfx_snip_5", "snip", "headshot", (255, 20, 60), (255, 220, 0)),
    ("vfx_snip_ult", "snip", "cataclysm", (255, 50, 80), (255, 230, 100)),

    # Priest
    ("vfx_priest_1", "priest", "holy_burst", (255, 215, 0), (255, 255, 220)),
    ("vfx_priest_2", "priest", "holy_bolt", (255, 225, 60), (255, 255, 255)),
    ("vfx_priest_3", "priest", "holy_flame", (255, 180, 40), (255, 230, 120)),
    ("vfx_priest_4", "priest", "halo_shield", (255, 220, 80), (255, 255, 240)),
    ("vfx_priest_5", "priest", "heal_pillar", (255, 235, 100), (255, 255, 255)),
    ("vfx_priest_ult", "priest", "cataclysm", (255, 215, 0), (255, 255, 255)),

    # Assassin
    ("vfx_as_1", "as", "poison_stab", (160, 32, 240), (0, 255, 120)),
    ("vfx_as_2", "as", "shadow_step", (60, 20, 90), (180, 50, 255)),
    ("vfx_as_3", "as", "blade_dance", (220, 40, 160), (255, 20, 80)),
    ("vfx_as_4", "as", "shadow_clone", (120, 40, 180), (40, 15, 60)),
    ("vfx_as_5", "as", "corpse_burst", (255, 0, 80), (120, 20, 60)),
    ("vfx_as_ult", "as", "cataclysm", (180, 30, 220), (255, 20, 90)),

    # Sword Master
    ("vfx_sm_1", "sm", "sword_ki", (0, 230, 255), (0, 140, 255)),
    ("vfx_sm_2", "sm", "flash_slash", (255, 255, 255), (0, 220, 255)),
    ("vfx_sm_3", "sm", "slash_5combo", (0, 240, 255), (100, 255, 255)),
    ("vfx_sm_4", "sm", "parry", (255, 220, 50), (0, 240, 255)),
    ("vfx_sm_5", "sm", "blue_dragon", (0, 200, 255), (20, 80, 180)),
    ("vfx_sm_ult", "sm", "cataclysm", (0, 240, 255), (255, 255, 255)),

    # Death Knight
    ("vfx_dk_1", "dk", "blood_drain", (255, 20, 60), (120, 10, 30)),
    ("vfx_dk_2", "dk", "dark_slash", (120, 20, 140), (255, 30, 60)),
    ("vfx_dk_3", "dk", "death_grip", (40, 20, 50), (200, 40, 80)),
    ("vfx_dk_4", "dk", "undead_armor", (60, 30, 80), (180, 40, 90)),
    ("vfx_dk_5", "dk", "guillotine", (255, 30, 70), (60, 15, 25)),
    ("vfx_dk_ult", "dk", "cataclysm", (255, 20, 60), (60, 10, 30)),

    # Martial King
    ("vfx_mk_1", "mk", "iron_fist", (255, 180, 50), (180, 80, 20)),
    ("vfx_mk_2", "mk", "punch_shock", (255, 200, 70), (255, 255, 255)),
    ("vfx_mk_3", "mk", "punch_flurry", (255, 140, 30), (255, 220, 90)),
    ("vfx_mk_4", "mk", "inner_burst", (255, 190, 40), (255, 80, 30)),
    ("vfx_mk_5", "mk", "haoh_blast", (255, 160, 40), (255, 240, 120)),
    ("vfx_mk_ult", "mk", "cataclysm", (255, 180, 40), (255, 255, 200)),

    # Psionic Tactician
    ("vfx_psi_1", "psi", "grid_calc", (180, 80, 255), (80, 240, 255)),
    ("vfx_psi_2", "psi", "gravity_well", (80, 20, 120), (220, 60, 255)),
    ("vfx_psi_3", "psi", "talisman", (255, 60, 100), (255, 210, 40)),
    ("vfx_psi_4", "psi", "mind_hack", (200, 60, 255), (0, 255, 200)),
    ("vfx_psi_5", "psi", "drone_laser", (0, 255, 220), (180, 80, 255)),
    ("vfx_psi_ult", "psi", "cataclysm", (220, 60, 255), (0, 255, 255)),

    # Berserker
    ("vfx_ber_1", "ber", "rage_blood", (255, 30, 30), (120, 10, 10)),
    ("vfx_ber_2", "ber", "axe_whirl", (255, 60, 40), (255, 180, 50)),
    ("vfx_ber_3", "ber", "sand_storm", (210, 150, 60), (255, 60, 30)),
    ("vfx_ber_4", "ber", "immortal_aura", (255, 20, 40), (255, 140, 20)),
    ("vfx_ber_5", "ber", "giant_leap", (255, 80, 40), (140, 30, 20)),
    ("vfx_ber_ult", "ber", "cataclysm", (255, 30, 30), (255, 180, 40)),

    # Cryo Empress
    ("vfx_cryo_1", "cryo", "frost_aura", (0, 230, 255), (30, 100, 160)),
    ("vfx_cryo_2", "cryo", "ice_spears", (160, 240, 255), (0, 200, 255)),
    ("vfx_cryo_3", "cryo", "frost_nova", (0, 240, 255), (200, 250, 255)),
    ("vfx_cryo_4", "cryo", "ice_crystallize", (180, 240, 255), (40, 140, 200)),
    ("vfx_cryo_5", "cryo", "glacier_fall", (120, 220, 255), (20, 80, 140)),
    ("vfx_cryo_ult", "cryo", "cataclysm", (0, 245, 255), (255, 255, 255)),
]

def make_vfx_sprite(filename, category, archetype, col_primary, col_secondary):
    SS = 2
    W, H = 64 * SS, 64 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 32 * SS, 32 * SS

    c_pri = col_primary + (255,)
    c_sec = col_secondary + (255,)
    c_glow = (col_primary[0], col_primary[1], col_primary[2], 120)

    if archetype in ("summon", "summon_elite"):
        # 바닥 원근 마법진 링 + 솟구치는 룬 기둥
        d.ellipse([cx - 24*SS, cy + 6*SS, cx + 24*SS, cy + 26*SS], outline=c_pri, width=3*SS)
        d.ellipse([cx - 16*SS, cy + 10*SS, cx + 16*SS, cy + 22*SS], outline=c_sec, width=2*SS)
        draw_rune_star(d, cx, cy + 16*SS, 10*SS, 4*SS, c_pri, points=6)
        # 상공으로 솟아오르는 빛기둥 & 룬 불꽃
        for rx, ry in [(-12*SS, 4*SS), (0, -10*SS), (12*SS, 4*SS)]:
            draw_bezier_tube(d, (cx + rx, cy + 16*SS), (cx + rx*0.8, cy), (cx + rx*0.4, cy - 14*SS), (cx + rx*0.2, cy - 24*SS),
                             r_start=4*SS, r_end=1*SS, col_dark=col_secondary + (255,), col_main=col_primary + (255,), col_hi=(255, 255, 255, 255))

    elif archetype in ("corpse_burst", "holy_burst", "slam", "explosive"):
        # 폭발 중심 섬광 + 방사형 파편 튜브 8개
        d.ellipse([cx - 12*SS, cy - 12*SS, cx + 12*SS, cy + 12*SS], fill=(255, 255, 255, 255))
        d.ellipse([cx - 18*SS, cy - 18*SS, cx + 18*SS, cy + 18*SS], outline=c_pri, width=4*SS)
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            x1 = cx + int(14*SS * math.cos(rad))
            y1 = cy + int(14*SS * math.sin(rad))
            x2 = cx + int(28*SS * math.cos(rad))
            y2 = cy + int(28*SS * math.sin(rad))
            draw_bezier_tube(d, (x1, y1), ((x1+x2)//2, (y1+y2)//2), ((x1+x2)//2, (y1+y2)//2), (x2, y2),
                             r_start=4*SS, r_end=1*SS, col_dark=col_secondary + (255,), col_main=col_primary + (255,), col_hi=(255, 255, 255, 255))

    elif archetype in ("projectile", "railgun", "ice_spears", "holy_bolt", "drone_laser"):
        # 고속 투사체 빔/뼈창 (좌하->우상 또는 수평 궤적)
        draw_bezier_tube(d, (cx - 26*SS, cy + 18*SS), (cx - 10*SS, cy + 6*SS), (cx + 10*SS, cy - 6*SS), (cx + 26*SS, cy - 18*SS),
                         r_start=6*SS, r_end=2*SS, col_dark=col_secondary + (255,), col_main=col_primary + (255,), col_hi=(255, 255, 255, 255))
        # 탄두 스파크
        d.polygon([(cx + 24*SS, cy - 24*SS), (cx + 30*SS, cy - 18*SS), (cx + 24*SS, cy - 12*SS), (cx + 18*SS, cy - 18*SS)], fill=(255, 255, 255, 255))
        # 궤적 잔상
        d.line([(cx - 28*SS, cy + 24*SS), (cx - 12*SS, cy + 12*SS)], fill=c_pri, width=3*SS)

    elif archetype in ("flash_slash", "sword_ki", "dark_slash", "blade_dance", "axe_whirl", "slash_5combo"):
        # 거대 초승달 검기 아크 (Crescent Slash Arc)
        draw_bezier_tube(d, (cx - 22*SS, cy + 22*SS), (cx - 4*SS, cy - 22*SS), (cx + 20*SS, cy - 20*SS), (cx + 26*SS, cy + 16*SS),
                         r_start=7*SS, r_end=2*SS, col_dark=col_secondary + (255,), col_main=col_primary + (255,), col_hi=(255, 255, 255, 255))
        # 교차 베기 보조 호
        draw_bezier_tube(d, (cx - 18*SS, cy - 16*SS), (cx, cy), (cx + 16*SS, cy + 8*SS), (cx + 24*SS, cy + 20*SS),
                         r_start=4*SS, r_end=1*SS, col_dark=col_secondary + (255,), col_main=col_primary + (255,), col_hi=(255, 255, 255, 255))

    elif archetype in ("cataclysm", "meteor", "glacier_fall"):
        # 전장 초토화 궁극기 (하늘에서 꽂히는 거대 신검/빙창/운석 + 지면 대폭발)
        # 상공에서 떨어지는 거대 쐐기
        draw_bezier_tube(d, (cx, cy - 28*SS), (cx, cy - 10*SS), (cx, cy + 6*SS), (cx, cy + 18*SS),
                         r_start=11*SS, r_end=3*SS, col_dark=col_secondary + (255,), col_main=col_primary + (255,), col_hi=(255, 255, 255, 255))
        # 지면 충격파 링 2개
        d.ellipse([cx - 26*SS, cy + 10*SS, cx + 26*SS, cy + 28*SS], outline=c_pri, width=4*SS)
        d.ellipse([cx - 18*SS, cy + 14*SS, cx + 18*SS, cy + 24*SS], fill=(255, 255, 255, 220))
        # 파편 스파크
        for dx in [-18*SS, -10*SS, 10*SS, 18*SS]:
            d.line([(cx + dx, cy + 18*SS), (cx + dx*1.3, cy + 8*SS)], fill=c_pri, width=3*SS)

    else:
        # 범용 버프/아우라/충격파 (기본 베지어 링 & 룬)
        d.ellipse([cx - 20*SS, cy - 20*SS, cx + 20*SS, cy + 20*SS], outline=c_pri, width=4*SS)
        draw_rune_star(d, cx, cy, 14*SS, 6*SS, c_sec, points=5)
        d.ellipse([cx - 6*SS, cy - 6*SS, cx + 6*SS, cy + 6*SS], fill=(255, 255, 255, 255))

    im = apply_16bit_shading(im)
    im = im.resize((64, 64), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    out_path = os.path.join(SKILLS_DIR, f"{filename}.png")
    im.save(out_path, "PNG")

print("--- Generating 72 Dedicated Skill VFX Sprites ---")
for spec in SKILL_SPECS:
    make_vfx_sprite(spec[0], spec[1], spec[2], spec[3], spec[4])
print("Completed 72 skill VFX generation.")

# =========================================================================
# 3. 12대 직업 5부작 신화 세트 아이템 (60종) HD 아이콘 생성기
# =========================================================================

SET_CLASSES = [
    ("necro", "사령군주", (0, 255, 170), (45, 20, 60)),
    ("guardian", "아이기스", (0, 240, 255), (212, 163, 56)),
    ("storm_wizard", "마도왕", (200, 80, 255), (60, 20, 120)),
    ("sniper", "호크아이", (255, 140, 30), (40, 45, 55)),
    ("priest", "대성역", (255, 220, 40), (255, 255, 255)),
    ("assassin", "그림자군주", (180, 40, 240), (20, 10, 30)),
    ("sword_master", "청룡검왕", (0, 220, 255), (10, 50, 110)),
    ("death_knight", "아발론단두대", (255, 20, 70), (25, 15, 35)),
    ("martial_king", "곤륜무신", (255, 190, 50), (140, 40, 20)),
    ("psionic_tactician", "화성이단참모", (220, 70, 255), (30, 80, 140)),
    ("berserker", "중력광전사", (255, 35, 35), (80, 20, 20)),
    ("cryo_empress", "시베리아빙여제", (0, 240, 255), (220, 245, 255)),
]

def make_set_item_icon(class_id, part, col_theme, col_base):
    SS = 2
    W, H = 48 * SS, 48 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 24 * SS, 24 * SS

    # 배경 은은한 한지/암석 슬롯 (다크 라운드 스퀘어)
    d.rounded_rectangle([2*SS, 2*SS, (48-2)*SS, (48-2)*SS], radius=6*SS, fill=(16, 12, 10, 255), outline=(70, 50, 35, 255), width=2*SS)

    if part == "ring":
        # 황금/미스릴 반지 밴드 (도넛 링)
        d.ellipse([cx - 14*SS, cy - 10*SS, cx + 14*SS, cy + 14*SS], outline=col_base + (255,), width=5*SS)
        d.ellipse([cx - 14*SS, cy - 10*SS, cx + 14*SS, cy + 14*SS], outline=(255, 215, 60, 255), width=2*SS)
        # 상단 소켓 보석
        d.polygon([(cx, cy - 18*SS), (cx + 8*SS, cy - 10*SS), (cx, cy - 4*SS), (cx - 8*SS, cy - 10*SS)], fill=col_theme + (255,))
        d.polygon([(cx, cy - 16*SS), (cx + 4*SS, cy - 10*SS), (cx, cy - 6*SS), (cx - 4*SS, cy - 10*SS)], fill=(255, 255, 255, 255))

    elif part == "weapon":
        # 대각선 직업 무기 (검/지팡이/총/도끼/너클)
        draw_bezier_tube(d, (cx - 14*SS, cy + 16*SS), (cx - 4*SS, cy + 4*SS), (cx + 6*SS, cy - 6*SS), (cx + 16*SS, cy - 16*SS),
                         r_start=5*SS, r_end=2*SS, col_dark=col_base + (255,), col_main=col_theme + (255,), col_hi=(255, 255, 255, 255))
        # 힐트/가드
        d.line([(cx - 8*SS, cy + 6*SS), (cx + 2*SS, cy + 14*SS)], fill=(255, 215, 50, 255), width=3*SS)
        # 폼멜 보석
        d.ellipse([cx - 17*SS, cy + 13*SS, cx - 11*SS, cy + 19*SS], fill=col_theme + (255,))

    elif part == "armor":
        # 흉갑/두정갑/로브
        draw_bezier_tube(d, (cx, cy - 12*SS), (cx, cy - 2*SS), (cx, cy + 6*SS), (cx, cy + 14*SS),
                         r_start=11*SS, r_end=9*SS, col_dark=col_base + (255,), col_main=col_theme + (255,), col_hi=(255, 255, 255, 255))
        # 좌우 어깨 보호대
        draw_bezier_tube(d, (cx - 10*SS, cy - 12*SS), (cx - 16*SS, cy - 6*SS), (cx - 14*SS, cy + 2*SS), (cx - 8*SS, cy + 2*SS),
                         r_start=5*SS, r_end=4*SS, col_dark=col_base + (255,), col_main=(212, 163, 56, 255), col_hi=(255, 240, 180, 255))
        draw_bezier_tube(d, (cx + 10*SS, cy - 12*SS), (cx + 16*SS, cy - 6*SS), (cx + 14*SS, cy + 2*SS), (cx + 8*SS, cy + 2*SS),
                         r_start=5*SS, r_end=4*SS, col_dark=col_base + (255,), col_main=(212, 163, 56, 255), col_hi=(255, 240, 180, 255))

    elif part == "helmet":
        # 투구/왕관/서클릿/복면
        draw_bezier_tube(d, (cx, cy - 6*SS), (cx, cy - 12*SS), (cx, cy - 16*SS), (cx, cy - 18*SS),
                         r_start=12*SS, r_end=13*SS, col_dark=col_base + (255,), col_main=col_theme + (255,), col_hi=(255, 255, 255, 255))
        # 안광 슬릿
        d.line([(cx - 7*SS, cy - 8*SS), (cx + 7*SS, cy - 8*SS)], fill=(255, 255, 255, 255), width=2*SS)
        # 상단 뿔/크라운 장식
        d.polygon([(cx - 6*SS, cy - 16*SS), (cx, cy - 22*SS), (cx + 6*SS, cy - 16*SS)], fill=(255, 215, 60, 255))

    elif part == "core":
        # 신화 심장핵 (Pulsating Rune Core Orb)
        d.ellipse([cx - 12*SS, cy - 12*SS, cx + 12*SS, cy + 12*SS], fill=col_theme + (255,))
        d.ellipse([cx - 8*SS, cy - 8*SS, cx + 8*SS, cy + 8*SS], fill=(255, 255, 255, 240))
        # 외곽 회전 봉인 링 2개
        d.arc([cx - 16*SS, cy - 16*SS, cx + 16*SS, cy + 16*SS], start=30, end=150, fill=(255, 215, 50, 255), width=2*SS)
        d.arc([cx - 16*SS, cy - 16*SS, cx + 16*SS, cy + 16*SS], start=210, end=330, fill=(255, 215, 50, 255), width=2*SS)

    im = apply_16bit_shading(im)
    im = im.resize((48, 48), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=3)
    out_path = os.path.join(ITEMS_SETS_DIR, f"set_{class_id}_{part}.png")
    im.save(out_path, "PNG")

print("--- Generating 60 Mythic Set Item Icons ---")
for c_id, c_name, c_theme, c_base in SET_CLASSES:
    for part in ["ring", "weapon", "armor", "helmet", "core"]:
        make_set_item_icon(c_id, part, c_theme, c_base)
print("Completed 60 Mythic Set Item Icons.")


# =========================================================================
# 4. 빌드 체인저 고유(Unique) 아이템 36종 HD 아이콘 생성기
# =========================================================================

UNIQUE_SPECS = [
    (1, "hammer", (212, 163, 56), (90, 60, 40)),
    (2, "candy", (255, 80, 140), (255, 255, 255)),
    (3, "wood_sword", (0, 220, 255), (140, 90, 50)),
    (4, "black_grimoire", (160, 40, 240), (25, 15, 35)),
    (5, "frost_orb", (0, 240, 255), (180, 240, 255)),
    (6, "exoskeleton", (100, 110, 130), (40, 45, 55)),
    (7, "arthur_helm", (255, 20, 60), (30, 25, 40)),
    (8, "shuriken", (180, 60, 255), (50, 20, 80)),
    (9, "terminal", (0, 255, 200), (30, 40, 60)),
    (10, "lava_heart", (255, 60, 20), (120, 30, 10)),
    (11, "tentacle", (160, 50, 200), (40, 90, 140)),
    (12, "dragon_scale", (0, 230, 255), (20, 60, 120)),
    (13, "gold_ring", (255, 215, 0), (180, 130, 30)),
    (14, "pizza_box", (255, 140, 40), (200, 40, 30)),
    (15, "chicken_beer", (255, 180, 50), (120, 70, 30)),
    (16, "bulletproof_vest", (70, 80, 95), (35, 40, 45)),
    (17, "overheat_core", (255, 90, 30), (255, 220, 60)),
    (18, "target_laser", (255, 40, 40), (40, 40, 50)),
    (19, "holy_rosary", (255, 225, 80), (255, 255, 240)),
    (20, "mana_elixir", (0, 240, 255), (30, 80, 150)),
    (21, "s_certificate", (255, 215, 0), (240, 230, 210)),
    (22, "black_box", (40, 40, 50), (255, 200, 40)),
    (23, "arachne_carapace", (120, 220, 40), (30, 50, 20)),
    (24, "casino_dice", (255, 220, 0), (200, 30, 60)),
    (25, "lightning_spear", (255, 240, 80), (180, 100, 255)),
    (26, "greatsword_shard", (220, 220, 235), (140, 40, 40)),
    (27, "sand_hourglass", (230, 180, 90), (110, 70, 40)),
    (28, "jade_plaque", (100, 230, 160), (212, 163, 56)),
    (29, "infinity_orb", (190, 80, 255), (40, 160, 255)),
    (30, "gravity_controller", (80, 20, 120), (0, 255, 220)),
    (31, "world_breaker_mace", (255, 80, 30), (50, 30, 30)),
    (32, "void_cloak", (90, 30, 140), (20, 10, 30)),
    (33, "emperor_crown", (255, 215, 0), (200, 20, 60)),
    (34, "memory_crystal", (0, 255, 230), (160, 40, 255)),
    (35, "dimension_shard", (220, 245, 255), (140, 80, 255)),
    (36, "regression_pocketwatch", (255, 210, 50), (90, 60, 30)),
]

def make_unique_item_icon(item_id, item_type, col_pri, col_sec):
    SS = 2
    W, H = 48 * SS, 48 * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 24 * SS, 24 * SS

    # 한지 족자 배경 테두리
    d.rounded_rectangle([2*SS, 2*SS, (48-2)*SS, (48-2)*SS], radius=6*SS, fill=(18, 14, 12, 255), outline=(212, 163, 56, 255), width=2*SS)

    # 품목별 특화 형상
    if item_type in ("hammer", "wood_sword", "lightning_spear", "world_breaker_mace"):
        # 대각선 무기/도구
        draw_bezier_tube(d, (cx - 14*SS, cy + 14*SS), (cx - 4*SS, cy + 4*SS), (cx + 6*SS, cy - 6*SS), (cx + 16*SS, cy - 16*SS),
                         r_start=5*SS, r_end=3*SS, col_dark=col_sec + (255,), col_main=col_pri + (255,), col_hi=(255, 255, 255, 255))
        d.ellipse([cx + 10*SS, cy - 18*SS, cx + 18*SS, cy - 10*SS], fill=col_pri + (255,))

    elif item_type in ("frost_orb", "lava_heart", "infinity_orb", "overheat_core", "memory_crystal", "dimension_shard"):
        # 보주 / 결정 / 코어
        d.ellipse([cx - 12*SS, cy - 12*SS, cx + 12*SS, cy + 12*SS], fill=col_pri + (255,))
        d.ellipse([cx - 7*SS, cy - 7*SS, cx + 7*SS, cy + 7*SS], fill=(255, 255, 255, 220))
        draw_rune_star(d, cx, cy, 14*SS, 6*SS, col_sec + (255,), points=5)

    elif item_type in ("black_grimoire", "s_certificate", "terminal", "black_box"):
        # 고서/문서/단말기 (비스듬한 책/패널)
        d.rounded_rectangle([cx - 12*SS, cy - 14*SS, cx + 12*SS, cy + 14*SS], radius=3*SS, fill=col_sec + (255,), outline=col_pri + (255,), width=2*SS)
        d.line([(cx - 8*SS, cy - 6*SS), (cx + 8*SS, cy - 6*SS)], fill=col_pri + (255,), width=2*SS)
        d.line([(cx - 8*SS, cy), (cx + 8*SS, cy)], fill=(255, 255, 255, 220), width=2*SS)
        d.line([(cx - 8*SS, cy + 6*SS), (cx + 4*SS, cy + 6*SS)], fill=(255, 255, 255, 220), width=2*SS)

    elif item_type in ("gold_ring", "regression_pocketwatch", "holy_rosary", "sand_hourglass"):
        # 회중시계/반지/모래시계
        d.ellipse([cx - 13*SS, cy - 11*SS, cx + 13*SS, cy + 15*SS], outline=col_pri + (255,), width=4*SS)
        d.ellipse([cx - 9*SS, cy - 7*SS, cx + 9*SS, cy + 11*SS], fill=col_sec + (255,))
        d.line([(cx, cy + 2*SS), (cx + 4*SS, cy - 3*SS)], fill=(255, 255, 255, 255), width=2*SS)
        d.ellipse([cx - 3*SS, cy - 16*SS, cx + 3*SS, cy - 10*SS], fill=col_pri + (255,))

    elif item_type in ("arthur_helm", "emperor_crown", "exoskeleton", "bulletproof_vest", "arachne_carapace", "void_cloak"):
        # 방어구/투구/왕관
        draw_bezier_tube(d, (cx, cy - 8*SS), (cx, cy - 12*SS), (cx, cy - 14*SS), (cx, cy - 16*SS),
                         r_start=12*SS, r_end=13*SS, col_dark=col_sec + (255,), col_main=col_pri + (255,), col_hi=(255, 255, 255, 255))
        d.polygon([(cx - 10*SS, cy - 14*SS), (cx, cy - 20*SS), (cx + 10*SS, cy - 14*SS)], fill=(255, 215, 50, 255))
        d.line([(cx - 6*SS, cy - 6*SS), (cx + 6*SS, cy - 6*SS)], fill=(255, 255, 255, 255), width=2*SS)

    else:
        # 음식/주사위/수리검 등 기타 특수 유물
        d.ellipse([cx - 12*SS, cy - 12*SS, cx + 12*SS, cy + 12*SS], fill=col_pri + (255,), outline=col_sec + (255,), width=2*SS)
        d.ellipse([cx - 4*SS, cy - 4*SS, cx + 4*SS, cy + 4*SS], fill=(255, 255, 255, 255))

    im = apply_16bit_shading(im)
    im = im.resize((48, 48), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=3)
    out_path = os.path.join(ITEMS_UNIQUES_DIR, f"unique_{item_id}.png")
    im.save(out_path, "PNG")

print("--- Generating 36 Build-Changer Unique Item Icons ---")
for spec in UNIQUE_SPECS:
    make_unique_item_icon(spec[0], spec[1], spec[2], spec[3])
print("Completed 36 Unique Item Icons.")
print("=== ALL STAGE 1 ASSETS GENERATED SUCCESSFULLY! ===")
