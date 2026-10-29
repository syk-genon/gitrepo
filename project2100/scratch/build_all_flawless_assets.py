# -*- coding: utf-8 -*-
"""
Master 240x240 High-Definition Character, Nemesis, Weapon, Armor & 13 Mutation Asset Builder
for PROJECT 2100:
- Anatomically segmented Male & Female Hero 4-Motion HD Sprites (36 files)
- Awakened Nemesis Male & Female 4-Motion HD Sprites with Abyssal Armor & Runeblade (36 files)
- 5 HD Shaded & Outlined Weapons locked to hand coordinates across all 18 frames (90 files)
- 10 HD Contour-Mapped + Pauldron/Chestplate Detailed Armors for Male & Female (180 files)
- 13 Multi-Layered HD Shaded & Outlined Mutation Parts locked to anatomical anchors (234 files)
Total: 576 240x240 HD Sprites
"""
import os, math, shutil
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERO_DIR = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
WEAPONS_DIR = os.path.join(HERO_DIR, "weapons")
ARMORS_DIR = os.path.join(HERO_DIR, "armors")
MUT_DIR = os.path.join(HERO_DIR, "mutations")

os.makedirs(HERO_DIR, exist_ok=True)
os.makedirs(WEAPONS_DIR, exist_ok=True)
os.makedirs(ARMORS_DIR, exist_ok=True)
os.makedirs(MUT_DIR, exist_ok=True)

SCALE = 2
BASE_W = 120
BASE_H = 120
CANVAS_W = BASE_W * SCALE  # 240
CANVAS_H = BASE_H * SCALE  # 240
OUTLINE = (20, 16, 26, 255)

MOTION_CONFIGS = {
    "idle": [
        dict(dx=0, dy=0, head_lean=0, torso_lean=0, fa_swing=0, ba_swing=0, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=0, dy=-1, head_lean=0, torso_lean=0, fa_swing=4, ba_swing=-4, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=0, dy=-2, head_lean=0, torso_lean=0, fa_swing=7, ba_swing=-7, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=0, dy=-1, head_lean=0, torso_lean=0, fa_swing=4, ba_swing=-4, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
    ],
    "run": [
        dict(dx=2, dy=1, head_lean=4, torso_lean=6, fa_swing=28, ba_swing=-24, ll_swing=-22, rl_swing=22, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=3, dy=2, head_lean=5, torso_lean=8, fa_swing=14, ba_swing=-12, ll_swing=-10, rl_swing=12, ll_dy=-1, rl_dy=0, vfx=None),
        dict(dx=2, dy=-3, head_lean=3, torso_lean=5, fa_swing=-4, ba_swing=4, ll_swing=4, rl_swing=-4, ll_dy=-2, rl_dy=-2, vfx=None),
        dict(dx=2, dy=1, head_lean=4, torso_lean=6, fa_swing=-22, ba_swing=28, ll_swing=22, rl_swing=-22, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=3, dy=2, head_lean=5, torso_lean=8, fa_swing=-10, ba_swing=14, ll_swing=12, rl_swing=-10, ll_dy=0, rl_dy=-1, vfx=None),
        dict(dx=2, dy=-3, head_lean=3, torso_lean=5, fa_swing=4, ba_swing=-4, ll_swing=-4, rl_swing=4, ll_dy=-2, rl_dy=-2, vfx=None),
    ],
    "attack": [
        dict(dx=-4, dy=1, head_lean=-5, torso_lean=-8, fa_swing=-38, ba_swing=20, ll_swing=-12, rl_swing=14, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=8, dy=0, head_lean=6, torso_lean=10, fa_swing=68, ba_swing=-25, ll_swing=-18, rl_swing=22, ll_dy=0, rl_dy=0, vfx="slash"),
        dict(dx=10, dy=0, head_lean=5, torso_lean=8, fa_swing=52, ba_swing=-18, ll_swing=-14, rl_swing=18, ll_dy=0, rl_dy=0, vfx="pierce"),
        dict(dx=2, dy=0, head_lean=2, torso_lean=3, fa_swing=12, ba_swing=-6, ll_swing=-4, rl_swing=4, ll_dy=0, rl_dy=0, vfx=None),
    ],
    "skill": [
        dict(dx=-1, dy=4, head_lean=4, torso_lean=6, fa_swing=-28, ba_swing=-15, ll_swing=-10, rl_swing=12, ll_dy=-3, rl_dy=-3, vfx="charge"),
        dict(dx=5, dy=-14, head_lean=-4, torso_lean=-4, fa_swing=105, ba_swing=-30, ll_swing=-16, rl_swing=18, ll_dy=-2, rl_dy=-1, vfx="upper"),
        dict(dx=7, dy=-17, head_lean=4, torso_lean=6, fa_swing=78, ba_swing=-20, ll_swing=-20, rl_swing=22, ll_dy=-2, rl_dy=-2, vfx="burst"),
        dict(dx=4, dy=3, head_lean=6, torso_lean=8, fa_swing=32, ba_swing=-15, ll_swing=-12, rl_swing=16, ll_dy=-2, rl_dy=-2, vfx="slam"),
    ]
}

def add_fast_anime_outline(im, outline_color=OUTLINE, size=5):
    """C-accelerated 2px bold dark outer contour outline around any RGBA sprite."""
    r, g, b, a = im.split()
    a_solid = a.point(lambda p: 255 if p > 125 else 0)
    im_solid = Image.merge("RGBA", (r, g, b, a_solid))
    dilated_a = a_solid.filter(ImageFilter.MaxFilter(size))
    outline_layer = Image.new("RGBA", im.size, outline_color)
    outline_layer.putalpha(dilated_a)
    return Image.alpha_composite(outline_layer, im_solid)

def apply_16bit_shading(im, preserve_glow=True):
    """Adds directional bevel highlight & shadow to drawn equipment/mutation layers."""
    w, h = im.size
    src = im.load()
    out = im.copy()
    dst = out.load()

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = src[x, y]
            if a == 0:
                continue
            if r < 40 and g < 35 and b < 45:
                continue
            if preserve_glow and r > 240 and g > 240 and b > 240:
                continue

            tl_empty = src[x - 1, y - 1][3] == 0 or (src[x - 1, y - 1][0] < 40 and src[x - 1, y - 1][1] < 35)
            br_empty = src[x + 1, y + 1][3] == 0 or (src[x + 1, y + 1][0] < 40 and src[x + 1, y + 1][1] < 35)

            if tl_empty and not br_empty:
                dst[x, y] = (min(255, int(r * 1.24) + 14), min(255, int(g * 1.24) + 14), min(255, int(b * 1.24) + 14), a)
            elif br_empty and not tl_empty:
                dst[x, y] = (int(r * 0.72), int(g * 0.72), int(b * 0.76), a)
    return out

def load_master_and_flip(path, target_h=90):
    im = Image.open(path).convert("RGBA")
    im_flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    mw, mh = im_flipped.size
    target_w = int(mw * (target_h / mh))
    base = im_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    r, g, b, a = base.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageEnhance.Color(rgb).enhance(1.22)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.15)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.35)
    alpha = a.point(lambda p: 255 if p > 110 else 0)
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out

def make_shaded_back_arm(f_arm, pivot_x, target_x, shift_y=0):
    w, h = f_arm.size
    b_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fpix = f_arm.load()
    bpix = b_arm.load()
    y_thresh = 41 * (h // 90)
    for y in range(h):
        for x in range(w):
            r, g, b, a = fpix[x, y]
            if a > 0:
                nx = target_x + (pivot_x - x)
                ny = y + shift_y
                if 0 <= nx < w and 0 <= ny < h:
                    shade = 0.94 if y <= y_thresh else 0.85
                    bpix[nx, ny] = (int(r * shade), int(g * shade), int(b * (shade + 0.02)), a)
    return b_arm

def segment_male(master):
    w, h = master.size
    pix = master.load()

    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    head.paste(master.crop((0, 0, w, 29)), (0, 0))

    f_arm_pix = f_arm.load()
    for y in range(30, 60):
        for x in range(16, 25):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if y >= 48 and x >= 24:
                continue
            if 38 <= y <= 47 and x >= 23 and (r > 200 and g > 195 and b > 175):
                continue
            f_arm_pix[x, y] = (r, g, b, a)

    torso_pix = torso.load()
    for y in range(28, 61):
        for x in range(20, 40):
            if f_arm_pix[x, y][3] > 0 and y >= 30:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if x >= 35 and 40 <= y <= 48 and (r > 170 and g < 155 and b < 130):
                continue
            torso_pix[x, y] = (r, g, b, a)

    # Seal left side of torso behind foreground arm with clean interior shirt/belt/shorts colors
    for y in range(31, 48):
        src_c = torso_pix[28, y] if torso_pix[28, y][3] > 0 else torso_pix[27, y]
        if src_c[3] > 0:
            for fill_x in range(21, 27):
                torso_pix[fill_x, y] = src_c
    for y in range(48, 52):
        for fill_x in range(22, 26):
            torso_pix[fill_x, y] = (75, 42, 26, 255)
    for y in range(52, 60):
        for fill_x in range(22, 26):
            torso_pix[fill_x, y] = (46, 68, 98, 255)

    b_arm = make_shaded_back_arm(f_arm, pivot_x=21, target_x=30, shift_y=0)

    l_leg.paste(master.crop((14, 58, 29, h)), (14, 58))
    ll_pix = l_leg.load()
    for y in range(58, 62):
        for x in range(14, 21):
            ll_pix[x, y] = (0, 0, 0, 0)

    r_leg.paste(master.crop((29, 58, 48, h)), (29, 58))

    pivots = {
        "head": (28, 27),
        "torso": (29, 45),
        "f_arm": (21, 34),
        "b_arm": (30, 34),
        "l_leg": (23, 60),
        "r_leg": (35, 60),
    }
    return head, torso, f_arm, b_arm, l_leg, r_leg, pivots

def segment_female(master):
    w, h = master.size
    pix = master.load()

    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    b_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    head_pix = head.load()
    torso_pix = torso.load()
    f_arm_pix = f_arm.load()
    b_arm_pix = b_arm.load()
    l_leg_pix = l_leg.load()
    r_leg_pix = r_leg.load()

    # 1. Head & Long Blonde Hair (include full ponytail + its warm brown shading at x <= 12, y <= 37)
    for y in range(0, 38):
        for x in range(0, w):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if y <= 25:
                head_pix[x, y] = (r, g, b, a)
            elif x <= 12 and b < 155:
                head_pix[x, y] = (r, g, b, a)

    # 2. Foreground arm (left side: x = 8..15, y = 26..53)
    for y in range(26, 53):
        for x in range(8, 16):
            if head_pix[x, y][3] > 0:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if y >= 40 and x >= 11 and (b > r or (r < 125 and g < 125)):
                continue
            if y <= 39 and x >= 15:
                continue
            if y >= 45 and r < 145 and g < 105 and b < 95:
                continue
            # Clean dark crease on sleeve so arm swings cleanly over white shirt
            if y <= 35 and (r < 200 or g < 190):
                r, g, b = 238, 232, 224
            f_arm_pix[x, y] = (r, g, b, a)

    # 3. Background arm (right side below sleeve: y = 34..53, x = 25..31)
    for y in range(34, 53):
        min_bx = 25 if y <= 39 else 26
        for x in range(min_bx, 32):
            if head_pix[x, y][3] > 0:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if y >= 39 and (b > r + 8 or (x == 26 and r < 140 and g < 140)):
                continue
            if y >= 47 and r < 115 and g < 75 and b < 65:
                continue
            b_arm_pix[x, y] = (r, g, b, a)

    # 4. Torso + Shirt + Shorts (x = 10..29, y = 24..52)
    for y in range(24, 52):
        for x in range(10, 29):
            if head_pix[x, y][3] > 0 or f_arm_pix[x, y][3] > 0 or b_arm_pix[x, y][3] > 0:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            torso_pix[x, y] = (r, g, b, a)

    # Seal torso all the way to the ponytail (x=10..18) so zero gap opens when f_arm swings forward!
    for y in range(26, 40):
        src_c = torso_pix[19, y] if torso_pix[19, y][3] > 0 else (242, 235, 225, 255)
        min_fill_x = 10 if y <= 36 else 13
        for fill_x in range(min_fill_x, 19):
            if head_pix[fill_x, y][3] == 0:
                torso_pix[fill_x, y] = src_c
    for y in range(40, 50):
        if torso_pix[18, y][3] > 0:
            torso_pix[17, y] = torso_pix[18, y]
            torso_pix[16, y] = torso_pix[18, y]
            torso_pix[15, y] = torso_pix[18, y]
            torso_pix[14, y] = (42, 58, 82, 255)

    # 5. Legs (y = 50..88)
    for y in range(50, 88):
        for x in range(11, 31):
            if b_arm_pix[x, y][3] > 0:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if y >= 84 and r > 215 and g > 215 and b > 205:
                continue
            if y <= 54 and x <= 13 and r < 100 and g < 65 and b < 55:
                continue
            if y <= 54 and x >= 27 and r < 115 and g < 75 and b < 65:
                continue
            if x <= 20:
                l_leg_pix[x, y] = (r, g, b, a)
            else:
                if y >= 86 and x <= 25:
                    continue
                r_leg_pix[x, y] = (r, g, b, a)

    pivots = {
        "head": (21, 22),
        "torso": (21, 38),
        "f_arm": (13, 29),
        "b_arm": (25, 29),
        "l_leg": (16, 51),
        "r_leg": (25, 51),
    }
    return head, torso, f_arm, b_arm, l_leg, r_leg, pivots

def build_hd_parts_from_master(path, female=False):
    m1 = load_master_and_flip(path, target_h=90)
    if female:
        head1, torso1, fa1, ba1, ll1, rl1, piv1 = segment_female(m1)
    else:
        head1, torso1, fa1, ba1, ll1, rl1, piv1 = segment_male(m1)

    w1, h1 = m1.size
    w2, h2 = w1 * SCALE, h1 * SCALE
    hi_master = load_master_and_flip(path, target_h=h2)
    hpix = hi_master.load()

    def upscale_part_hd(p1, is_torso=False):
        p2_fb = p1.resize((w2, h2), Image.Resampling.BILINEAR)
        p2_nr = p1.resize((w2, h2), Image.Resampling.NEAREST)
        fb_pix = p2_fb.load()
        nr_pix = p2_nr.load()
        out = Image.new("RGBA", (w2, h2), (0, 0, 0, 0))
        opix = out.load()
        seal_max_x = (19 if female else 27) * SCALE
        for y in range(h2):
            for x in range(w2):
                if nr_pix[x, y][3] > 120:
                    if is_torso and x < seal_max_x and (26 * SCALE <= y <= 59 * SCALE):
                        # Use clean sealed torso color instead of unsegmented hi_master (which has the idle arm crease)
                        opix[x, y] = (fb_pix[x, y][0], fb_pix[x, y][1], fb_pix[x, y][2], 255)
                    elif hpix[x, y][3] > 120:
                        nr_r, nr_g, nr_b, _ = nr_pix[x, y]
                        hr, hg, hb, _ = hpix[x, y]
                        if abs(nr_r - hr) + abs(nr_g - hg) + abs(nr_b - hb) < 75:
                            opix[x, y] = (hr, hg, hb, 255)
                        else:
                            opix[x, y] = (fb_pix[x, y][0], fb_pix[x, y][1], fb_pix[x, y][2], 255)
                    else:
                        opix[x, y] = (fb_pix[x, y][0], fb_pix[x, y][1], fb_pix[x, y][2], 255)
        return out

    head2 = upscale_part_hd(head1)
    torso2 = upscale_part_hd(torso1, is_torso=True)
    fa2 = upscale_part_hd(fa1)
    # Clean dark outline/crease pixels on fa2 sleeve & upper arm so rotating across white shirt leaves zero dark speckles
    fa2_pix = fa2.load()
    sleeve_cut_y = (35 if female else 40) * SCALE
    wrist_cut_y = (45 if female else 49) * SCALE
    for y in range(h2):
        for x in range(w2):
            r, g, b, a = fa2_pix[x, y]
            if a == 0:
                continue
            if y <= sleeve_cut_y:
                # Ensure entire sleeve is clean warm-white fabric with soft shading (no dark outline speckles)
                if r < 210 or g < 198:
                    fa2_pix[x, y] = (232, 224, 214, 255)
            elif y <= wrist_cut_y:
                # Upper bare forearm: soften any black outline pixels into natural warm skin shadow
                if r < 155 or g < 105:
                    fa2_pix[x, y] = (208, 152, 122, 255)

    ll2 = upscale_part_hd(ll1)
    rl2 = upscale_part_hd(rl1)
    if female:
        ba2 = upscale_part_hd(ba1)
    else:
        ba2 = make_shaded_back_arm(fa2, pivot_x=piv1["f_arm"][0] * SCALE, target_x=piv1["b_arm"][0] * SCALE, shift_y=0)

    piv2 = {k: (v[0] * SCALE, v[1] * SCALE) for k, v in piv1.items()}
    return hi_master, head2, torso2, fa2, ba2, ll2, rl2, piv2

def rotate_smooth_hd(img, pivot, deg):
    if deg == 0:
        return img
    # Dilate RGB into transparent neighbors before BICUBIC rotation so edges NEVER blend with black (0,0,0)!
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    dilated_rgb = rgb.filter(ImageFilter.MaxFilter(5))
    mask_solid = a.point(lambda p: 255 if p > 10 else 0)
    padded_rgb = Image.composite(rgb, dilated_rgb, mask_solid)
    padded_rgb2 = Image.composite(padded_rgb, padded_rgb.filter(ImageFilter.MaxFilter(5)), a.point(lambda p: 255 if p > 0 else 0))
    pr, pg, pb = padded_rgb2.split()
    rot_r = pr.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot)
    rot_g = pg.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot)
    rot_b = pb.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot)
    rot_a = a.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot).point(lambda p: 255 if p > 125 else 0)
    return Image.merge("RGBA", (rot_r, rot_g, rot_b, rot_a))

def rotate_limb(img, pivot, swing_right_deg):
    return rotate_smooth_hd(img, pivot, swing_right_deg)

def rotate_body(img, pivot, lean_right_deg):
    return rotate_smooth_hd(img, pivot, -lean_right_deg)

def get_hand_pos_and_angle(cfg):
    dx, dy = cfg["dx"], cfg["dy"]
    fa_swing = cfg["fa_swing"]
    sx = (53 + dx) * SCALE
    sy = (61 + dy) * SCALE
    rad = math.radians(fa_swing)
    hx = sx + int(21 * SCALE * math.sin(rad))
    hy = sy + int(21 * SCALE * math.cos(rad))
    blade_deg = fa_swing - 22
    return hx, hy, blade_deg

def make_nemesis_variant(hero_frame, torso_layer, f_arm_layer, b_arm_layer, hx, hy, fa_swing, vfx, cfg, is_female=False):
    w, h = hero_frame.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src = hero_frame.load()
    dst = out.load()

    dx2, dy2 = cfg["dx"] * SCALE, cfg["dy"] * SCALE

    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                continue
            if r < 35 and g < 30 and b < 42:
                dst[x, y] = OUTLINE
            elif y < 110 + dy2 and (b > r + 20 or (is_female and r > 180 and g < 140 and y > 78 + dy2)):
                # Eye iris -> Glowing Awakened Crimson Eyes
                dst[x, y] = (255, 25, 80, a)
            elif b > r + 8 and y > 110 + dy2:
                # Blue denim shorts -> Abyssal Obsidian Greaves (continuous shading)
                lum = (r + g + b) / 3.0
                dst[x, y] = (min(255, int(lum * 0.58) + 18), int(lum * 0.28), min(255, int(lum * 0.82) + 28), a)
            elif is_female and y < 120 + dy2 and (r > b + 45 and g > b + 20 and r > 145):
                # Female blonde hair -> Smooth Awakened Silver-Lavender Hair
                lum = (r + g + b) / 3.0
                dst[x, y] = (min(255, int(lum * 0.82) + 32), min(255, int(lum * 0.68) + 18), min(255, int(lum * 0.98) + 45), a)
            else:
                # Smooth continuous Dusk-Awakened skin & dark hair (zero hard threshold blotches!)
                nr = min(255, int(r * 0.86) + 14)
                ng = min(255, int(g * 0.78) + 6)
                nb = min(255, int(b * 0.94) + 28)
                dst[x, y] = (nr, ng, nb, a)

    # Composite Contour-Fitted Abyssal Obsidian-Crimson Battle Armor onto Nemesis!
    abyssal_armor = build_contour_armor_frame("abyssal", torso_layer, f_arm_layer, b_arm_layer, cfg, is_female=is_female)
    out.alpha_composite(abyssal_armor)

    # Add Ornate HD Abyssal Nemesis Runeblade
    w_cv = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    wd = ImageDraw.Draw(w_cv)
    gx, gy = 48, 96
    wd.rectangle([gx - 20, gy - 4, gx, gy + 4], fill=(42, 16, 58, 255), outline=OUTLINE)
    wd.polygon([(gx - 4, gy - 14), (gx + 6, gy - 6), (gx + 6, gy + 6), (gx - 4, gy + 14)],
               fill=(235, 25, 95, 255), outline=OUTLINE)
    wd.polygon([(gx + 4, gy - 6), (gx + 76, gy - 7), (gx + 92, gy), (gx + 76, gy + 7), (gx + 4, gy + 6)],
               fill=(185, 18, 78, 255), outline=OUTLINE)
    wd.polygon([(gx + 8, gy - 3), (gx + 72, gy - 3), (gx + 84, gy), (gx + 72, gy + 3), (gx + 8, gy + 3)],
               fill=(255, 85, 155, 255))
    wd.line([(gx + 8, gy), (gx + 84, gy)], fill=(255, 240, 250, 255), width=2)
    w_cv = add_fast_anime_outline(w_cv, outline_color=OUTLINE, size=5)
    rot_w = rotate_smooth_hd(w_cv, (gx, gy), fa_swing - 22)
    out.paste(rot_w, (hx - gx, hy - gy), rot_w)

    return out

def draw_cute_star(d, cx, cy, r_out, r_in, fill, outline=None):
    pts = []
    for i in range(8):
        ang = math.radians(i * 45 - 90)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=outline)

def draw_cute_heart(d, cx, cy, sz, fill, outline=None):
    r = sz * 0.55
    d.ellipse([cx - sz, cy - sz * 0.8, cx, cy + sz * 0.2], fill=fill, outline=outline)
    d.ellipse([cx, cy - sz * 0.8, cx + sz, cy + sz * 0.2], fill=fill, outline=outline)
    d.polygon([(cx - sz * 0.95, cy - sz * 0.1), (cx + sz * 0.95, cy - sz * 0.1), (cx, cy + sz * 1.05)], fill=fill)
    # Glossy bubble shine on heart
    d.ellipse([cx - sz * 0.65, cy - sz * 0.55, cx - sz * 0.25, cy - sz * 0.2], fill=(255, 255, 255, 235))

def draw_bezier_tube(d, p0, p1, p2, p3, r_start, r_end, col_dark, col_main, col_hi, steps=36):
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
        d.ellipse([x - rm, y - rm - r*0.08, x + rm, y + rm - r*0.08], fill=col_main)
    for x, y, r in pts[2:-2]:
        rh = max(0.8, r * 0.42)
        d.ellipse([x - rh, y - r*0.55 - rh, x + rh, y - r*0.55 + rh], fill=col_hi)

def draw_rotated_weapon(weapon_type, cfg):
    im = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    hx, hy, blade_deg = get_hand_pos_and_angle(cfg)
    vfx = cfg.get("vfx")

    # 2x Supersampled canvas for silky-smooth cute chibi weapon curves
    SS = 2
    w_ss = Image.new("RGBA", (192 * SS, 192 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(w_ss)
    gx, gy = 48 * SS, 96 * SS

    if weapon_type == "katana":
        # Cute Sakura-Gold Chibi Katana with Clover Guard & Tassel
        d.rounded_rectangle([gx - 44, gy - 9, gx + 2, gy + 9], radius=8, fill=(88, 36, 58, 255))
        for tx in range(gx - 36, gx - 4, 12):
            d.ellipse([tx - 4, gy - 6, tx + 4, gy + 6], fill=(255, 115, 165, 255))
        # Cute golden pommel cap & floating sakura tassel
        d.ellipse([gx - 48, gy - 10, gx - 36, gy + 10], fill=(255, 208, 65, 255))
        # Plump Golden Clover/Flower Guard (Tsuba)
        d.rounded_rectangle([gx - 6, gy - 24, gx + 10, gy + 24], radius=7, fill=(255, 205, 55, 255))
        d.ellipse([gx - 4, gy - 14, gx + 8, gy + 14], fill=(255, 240, 150, 255))
        # Chunky, curved cute anime blade
        d.polygon([
            (gx + 8, gy - 12), (gx + 145, gy - 16), (gx + 178, gy - 4),
            (gx + 156, gy + 12), (gx + 8, gy + 10)
        ], fill=(175, 202, 232, 255))
        d.polygon([
            (gx + 10, gy - 11), (gx + 144, gy - 14), (gx + 170, gy - 4),
            (gx + 148, gy + 2), (gx + 10, gy + 1)
        ], fill=(238, 248, 255, 255))
        # Glossy white anime shine & cute star sparkle near tip
        d.line([(gx + 16, gy - 6), (gx + 158, gy - 8)], fill=(255, 255, 255, 255), width=5)
        draw_cute_star(d, gx + 140, gy - 4, 10, 4, (255, 255, 255, 255))

    elif weapon_type == "axe":
        # Cute Chibi Winged Star-Battleaxe
        d.rounded_rectangle([gx - 40, gy - 8, gx + 128, gy + 8], radius=7, fill=(135, 82, 48, 255))
        d.line([(gx - 34, gy - 3), (gx + 120, gy - 3)], fill=(195, 132, 82, 255), width=4)
        d.ellipse([gx - 46, gy - 11, gx - 32, gy + 11], fill=(255, 205, 65, 255))
        # Plump, rounded crescent twin axe blades
        d.chord([gx + 40, gy - 62, gx + 132, gy + 20], start=190, end=350, fill=(135, 158, 190, 255))
        d.chord([gx + 40, gy - 20, gx + 132, gy + 62], start=10, end=170, fill=(118, 140, 172, 255))
        # Bright glossy bevels on curved blades
        d.arc([gx + 42, gy - 60, gx + 130, gy + 18], start=200, end=340, fill=(245, 252, 255, 255), width=8)
        d.arc([gx + 42, gy - 18, gx + 130, gy + 60], start=20, end=160, fill=(235, 245, 255, 255), width=8)
        # Cute golden star/heart center socket & chubby top spike
        d.polygon([(gx + 124, gy - 9), (gx + 152, gy), (gx + 124, gy + 9)], fill=(255, 210, 68, 255))
        d.rounded_rectangle([gx + 72, gy - 16, gx + 102, gy + 16], radius=8, fill=(245, 55, 95, 255))
        draw_cute_star(d, gx + 87, gy, 12, 5, (255, 235, 110, 255))

    elif weapon_type == "crystal_sword":
        # Cute Magical Star-Crystal Broadsword
        d.rounded_rectangle([gx - 40, gy - 8, gx + 4, gy + 8], radius=7, fill=(85, 98, 145, 255))
        d.ellipse([gx - 46, gy - 11, gx - 32, gy + 11], fill=(255, 215, 75, 255))
        # Chubby Crystal Blade (Pastel Aqua & Sakura Glow)
        d.polygon([
            (gx + 10, gy - 20), (gx + 142, gy - 20), (gx + 182, gy),
            (gx + 142, gy + 20), (gx + 10, gy + 20)
        ], fill=(38, 195, 255, 250))
        d.polygon([
            (gx + 16, gy - 12), (gx + 136, gy - 12), (gx + 168, gy),
            (gx + 136, gy + 12), (gx + 16, gy + 12)
        ], fill=(165, 248, 255, 255))
        d.line([(gx + 18, gy), (gx + 164, gy)], fill=(255, 255, 255, 255), width=6)
        # Cute Puffy Winged Guard & Heart Gem
        d.ellipse([gx - 8, gy - 32, gx + 20, gy - 4], fill=(255, 235, 120, 255))
        d.ellipse([gx - 8, gy + 4, gx + 20, gy + 32], fill=(255, 235, 120, 255))
        draw_cute_heart(d, gx + 8, gy, 11, (255, 85, 165, 255))
        draw_cute_star(d, gx + 125, gy - 6, 11, 4, (255, 255, 255, 255))

    elif weapon_type == "heavy_cannon":
        # Cute Chubby Capsule Star-Blaster
        d.rounded_rectangle([gx - 32, gy - 16, gx + 20, gy + 22], radius=10, fill=(65, 78, 102, 255))
        d.rounded_rectangle([gx + 4, gy - 26, gx + 138, gy + 18], radius=18, fill=(88, 108, 142, 255))
        d.rounded_rectangle([gx + 12, gy - 20, gx + 130, gy - 2], radius=10, fill=(195, 218, 248, 255))
        # Cute glowing cyan bubble windows along barrel
        for vx in [gx + 34, gx + 68, gx + 102]:
            d.ellipse([vx - 11, gy - 14, vx + 11, gy + 8], fill=(0, 242, 255, 255))
            d.ellipse([vx - 6, gy - 10, vx, gy - 4], fill=(255, 255, 255, 255))
        # Chubby rounded muzzle ring
        d.rounded_rectangle([gx + 126, gy - 30, gx + 152, gy + 22], radius=10, fill=(255, 205, 65, 255))
        if vfx in ["slash", "pierce", "upper", "burst", "slam"]:
            draw_cute_star(d, gx + 184, gy - 4, 34, 15, (255, 235, 75, 255))
            draw_cute_star(d, gx + 184, gy - 4, 20, 9, (255, 255, 255, 255))

    elif weapon_type == "lava_launcher":
        # Cute Chubby Magma-Dragon Bubble Cannon
        d.rounded_rectangle([gx - 34, gy - 24, gx + 136, gy + 20], radius=18, fill=(98, 46, 48, 255))
        d.rounded_rectangle([gx - 24, gy - 18, gx + 126, gy - 2], radius=10, fill=(148, 72, 68, 255))
        # Cute glowing round magma portholes
        for cx_pos in [gx + 22, gx + 60, gx + 98]:
            d.ellipse([cx_pos - 13, gy - 14, cx_pos + 13, gy + 12], fill=(255, 115, 28, 255))
            d.ellipse([cx_pos - 8, gy - 9, cx_pos + 6, gy + 5], fill=(255, 238, 95, 255))
            d.ellipse([cx_pos - 5, gy - 7, cx_pos - 1, gy - 3], fill=(255, 255, 255, 255))
        # Flared cute dragon-snout muzzle
        d.rounded_rectangle([gx + 126, gy - 30, gx + 158, gy + 26], radius=12, fill=(235, 95, 38, 255))
        d.rounded_rectangle([gx + 144, gy - 22, gx + 158, gy + 18], radius=6, fill=(255, 215, 70, 255))
        if vfx in ["slash", "pierce", "upper", "burst", "slam"]:
            d.ellipse([gx + 160, gy - 28, gx + 212, gy + 24], fill=(255, 105, 25, 255))
            d.ellipse([gx + 168, gy - 20, gx + 202, gy + 14], fill=(255, 238, 95, 255))

    w_cv = w_ss.resize((192, 192), Image.Resampling.LANCZOS)
    w_cv = add_fast_anime_outline(w_cv, size=5)
    rot_w = rotate_smooth_hd(w_cv, (48, 96), blade_deg)
    im.paste(rot_w, (hx - 48, hy - 96), rot_w)

    if weapon_type in ["katana", "axe", "crystal_sword"] and vfx in ["slash", "upper", "burst"]:
        sd = ImageDraw.Draw(im)
        color_main = (110, 240, 255, 240) if weapon_type != "axe" else (255, 135, 75, 240)
        for deg in range(-48, 62, 2):
            r_rad = math.radians(deg)
            rx = hx + 20 + int(52 * math.cos(r_rad))
            ry = hy - 12 - int(56 * math.sin(r_rad))
            sd.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=color_main)
            sd.point((rx, ry), fill=(255, 255, 255, 255))

    return im

def build_contour_armor_frame(armor_type, torso_layer, f_arm_layer, b_arm_layer, cfg, is_female=False):
    """
    HD 240x240 Contour-Mapped Armor + Rich Shoulder Pauldrons, Collar, Chestplate & Belt Details!
    """
    w, h = torso_layer.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tpix = torso_layer.load()
    fapix = f_arm_layer.load()
    bapix = b_arm_layer.load()
    dpix = out.load()

    PALETTES = {
        "military":    ((122, 154, 96),  (84, 112, 64),  (52, 70, 40),   (38, 44, 32),   (245, 200, 52)),
        "leather":     ((182, 115, 72),  (138, 80, 46),  (90, 48, 28),   (55, 32, 18),   (240, 195, 58)),
        "nano_carbon": ((84, 98, 126),   (48, 58, 78),   (26, 32, 46),   (0, 230, 255),  (0, 248, 255)),
        "hardlight":   ((185, 248, 255), (68, 200, 252), (28, 128, 198), (235, 252, 255),(0, 248, 255)),
        "yeti_fur":    ((252, 254, 255), (222, 236, 250),(175, 198, 226),(75, 108, 148), (125, 238, 255)),
        "abyssal":     ((92, 48, 138),   (58, 28, 92),   (34, 16, 56),   (145, 22, 78),  (255, 30, 95)),
    }
    hl, mid, shd, trim, acc = PALETTES[armor_type]

    dx2, dy2 = cfg["dx"] * SCALE, cfg["dy"] * SCALE
    waist_max_y = ((69 if is_female else 75) * SCALE) + dy2
    belt_min_y = ((66 if is_female else 72) * SCALE) + dy2
    neck_max_y = ((57 if is_female else 60) * SCALE) + dy2
    sleeve_max_y = ((68 if is_female else 72) * SCALE) + dy2
    cx = (128 if is_female else 121) + dx2
    cy = (124 if is_female else 126) + dy2

    for y in range(h):
        for x in range(w):
            fa_r, fa_g, fa_b, fa_a = fapix[x, y]
            is_fa_sleeve = False
            if fa_a > 0:
                # Warm-white sleeve has G >= 185, B >= 165, and R - G < 25 (whereas bare peach skin has G < 185 and R - G > 32)
                is_fa_sleeve = (fa_g >= 185 and fa_b >= 165 and (fa_r - fa_g) < 25 and y <= waist_max_y)
                if not is_fa_sleeve:
                    continue

            r, g, b, a = (fa_r, fa_g, fa_b, fa_a) if is_fa_sleeve else tpix[x, y]
            if a == 0:
                ba_r, ba_g, ba_b, ba_a = bapix[x, y]
                if ba_a > 0 and (ba_g >= 170 and ba_b >= 155 and (ba_r - ba_g) < 25 and y <= sleeve_max_y):
                    r, g, b, a = ba_r, ba_g, ba_b, ba_a
            if a == 0 or y > waist_max_y:
                continue

            if r > 175 and g > 105 and r > b + 28 and y < neck_max_y:
                continue

            if r < 42 and g < 38 and b < 48:
                dpix[x, y] = (r, g, b, a)
                continue

            lum = (r + g + b) / 3.0
            if belt_min_y <= y <= waist_max_y:
                if cx - 3 <= x <= cx + 4:
                    dpix[x, y] = (*acc, 255)
                else:
                    dpix[x, y] = (*trim, 255)
                continue

            if lum > 210:
                c = hl
            elif lum > 165:
                c = mid
            else:
                c = shd

            # Cute Anime Armor Collars, Badges & Chest Emblems
            dist_c = math.hypot(x - cx, y - (cy - 2))
            if armor_type == "nano_carbon":
                # Sleek cyber V-trim + cute glowing cyan diamond/heart core
                if dist_c <= 4.2:
                    c = (210, 255, 255) if dist_c <= 2.2 else acc
                elif y < cy and abs(abs(x - cx) - (cy - y) * 0.8) <= 1.2:
                    c = acc
            elif armor_type == "abyssal":
                if dist_c <= 4.5:
                    c = (255, 225, 240) if dist_c <= 2.2 else acc
                elif y < cy and abs(abs(x - cx) - (cy - y) * 0.8) <= 1.2:
                    c = acc
            elif armor_type == "hardlight":
                # Glowing crystal-star chest emblem & soft holo sheen
                if dist_c <= 5.0:
                    c = (255, 255, 255) if dist_c <= 2.8 else (160, 250, 255)
                elif (x + y) % 7 == 0:
                    c = hl
            elif armor_type == "leather":
                # Cute diagonal adventurer strap + golden chest buckle
                if dist_c <= 3.5:
                    c = acc
                elif abs((x - cx) - (y - cy) * 0.9) <= 2.2:
                    c = trim
            elif armor_type == "military":
                # Cute tactical jacket center zip + golden star badge on chest
                if math.hypot(x - (cx + 6), y - (cy - 3)) <= 2.8:
                    c = acc
                elif abs(x - cx) <= 1:
                    c = trim
            elif armor_type == "yeti_fur":
                # Fluffy white winter coat with sky-blue pom-pom collar & hem
                if y <= neck_max_y + 4 or y >= belt_min_y - 3:
                    c = (255, 255, 255) if (x + y) % 2 == 0 else acc
                elif math.hypot(x - cx, y - (neck_max_y + 5)) <= 3.5:
                    c = acc

            alpha_out = 225 if armor_type == "hardlight" else 255
            dpix[x, y] = (c[0], c[1], c[2], alpha_out)

    return out

def draw_mutation_frame(part_name, cfg, frame_idx, f_arm_layer=None):
    # 2x Supersampled canvas (480x480 -> 240x240 LANCZOS) for ultra-cute, rounded chibi-anime parts!
    SS = 2
    ss_im = Image.new("RGBA", (CANVAS_W * SS, CANVAS_H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(ss_im)
    dx, dy = cfg["dx"] * SCALE * SS, cfg["dy"] * SCALE * SS
    pulse = (frame_idx % 2) * 4 * SS

    if part_name == "horns":
        # Cute Chubby Curved Oni/Dragon Horns + Mini Golden Crown Gem
        cx, cy = 122 * SS + dx, 72 * SS + dy
        # Left chubby curved horn
        draw_bezier_tube(
            d,
            (cx - 18, cy + 8), (cx - 42, cy - 8), (cx - 56, cy - 30), (cx - 42, cy - 48),
            r_start=13, r_end=5,
            col_dark=(175, 25, 58, 255), col_main=(255, 68, 105, 255), col_hi=(255, 195, 210, 255)
        )
        # Right chubby curved horn
        draw_bezier_tube(
            d,
            (cx + 18, cy + 8), (cx + 42, cy - 8), (cx + 56, cy - 30), (cx + 42, cy - 48),
            r_start=13, r_end=5,
            col_dark=(175, 25, 58, 255), col_main=(255, 68, 105, 255), col_hi=(255, 195, 210, 255)
        )
        # Cute golden tiger/oni rings on horns
        d.arc([cx - 54, cy - 32, cx - 30, cy - 10], start=180, end=360, fill=(255, 220, 75, 255), width=6)
        d.arc([cx + 30, cy - 32, cx + 54, cy - 10], start=180, end=360, fill=(255, 220, 75, 255), width=6)
        # Cute little floating golden mini-crown / star gem in the center
        d.polygon([
            (cx - 14, cy + 4), (cx - 18, cy - 18), (cx - 7, cy - 10),
            (cx, cy - 26), (cx + 7, cy - 10), (cx + 18, cy - 18), (cx + 14, cy + 4)
        ], fill=(255, 215, 55, 255))
        d.ellipse([cx - 5, cy - 9, cx + 5, cy + 1], fill=(255, 55, 115, 255))
        d.ellipse([cx - 3, cy - 7, cx, cy - 4], fill=(255, 255, 255, 255))

    elif part_name == "visor":
        # Cute Cyber-Neko / Heart Hologram Goggles
        cx, cy = 122 * SS + dx, 92 * SS + dy
        # Cute little cat-ear / winglet side headphone on left temple
        d.polygon([(cx - 30, cy - 4), (cx - 42, cy - 26), (cx - 18, cy - 14)], fill=(255, 105, 180, 255))
        d.polygon([(cx - 28, cy - 6), (cx - 36, cy - 20), (cx - 20, cy - 12)], fill=(0, 245, 255, 255))
        d.ellipse([cx - 32, cy - 12, cx - 14, cy + 12], fill=(240, 248, 255, 255))
        # Rounded pill-shaped translucent holo-visor lens
        d.rounded_rectangle([cx - 20, cy - 12, cx + 34, gy_vis := cy + 11], radius=11, fill=(255, 45, 125, 230))
        d.rounded_rectangle([cx - 16, cy - 9, cx + 30, cy + 7], radius=8, fill=(255, 105, 180, 235))
        # Glossy anime diagonal lens shine & cute star HUD icon
        d.line([(cx - 10, cy - 5), (cx + 18, cy - 5)], fill=(255, 255, 255, 250), width=5)
        draw_cute_star(d, cx + 20, cy, 8, 3, (0, 255, 245, 255))

    elif part_name == "antennae":
        # Cute Bouncy Bobble-Heart / Star Pom-Pom Antennae
        cx, cy = 120 * SS + dx, 62 * SS + dy
        # Left & Right curved springy stalks
        draw_bezier_tube(
            d,
            (cx - 14, cy + 14), (cx - 26, cy - 18), (cx - 42, cy - 34), (cx - 52, cy - 46 - pulse),
            r_start=5, r_end=4,
            col_dark=(25, 165, 215, 255), col_main=(95, 245, 255, 255), col_hi=(255, 255, 255, 255)
        )
        draw_bezier_tube(
            d,
            (cx + 14, cy + 14), (cx + 26, cy - 18), (cx + 42, cy - 34), (cx + 52, cy - 46 - pulse),
            r_start=5, r_end=4,
            col_dark=(25, 165, 215, 255), col_main=(95, 245, 255, 255), col_hi=(255, 255, 255, 255)
        )
        # Plump glowing pastel yellow & pink pom-pom / heart-orb tips
        for ox_tip in [cx - 52, cx + 52]:
            oy_tip = cy - 48 - pulse
            d.ellipse([ox_tip - 16, oy_tip - 16, ox_tip + 16, oy_tip + 16], fill=(255, 195, 55, 255))
            d.ellipse([ox_tip - 13, oy_tip - 14, ox_tip + 13, oy_tip + 11], fill=(255, 242, 115, 255))
            # Cute pink cheek dot & white glossy bubble
            d.ellipse([ox_tip + 2, oy_tip, ox_tip + 9, oy_tip + 6], fill=(255, 115, 165, 255))
            d.ellipse([ox_tip - 9, oy_tip - 10, ox_tip - 2, oy_tip - 3], fill=(255, 255, 255, 255))

    elif part_name == "halo":
        # Cute Winged Angel Halo with Twinkling Stars
        cx, cy = 120 * SS + dx, 42 * SS + dy - (pulse // 2)
        # Cute puffy white angel winglets on left & right of the halo
        for side in [-1, 1]:
            wx = cx + side * 56
            d.ellipse([wx - 18, cy - 16, wx + 18, cy + 4], fill=(235, 248, 255, 255))
            d.ellipse([wx - 14, cy - 6, wx + 14, cy + 10], fill=(255, 255, 255, 255))
            d.ellipse([wx - 22 if side < 0 else wx - 6, cy - 22, wx + 6 if side < 0 else wx + 22, cy - 2], fill=(255, 255, 255, 255))
        # Plump golden-cyan glowing torus ring
        d.ellipse([cx - 52, cy - 14, cx + 52, cy + 14], outline=(255, 200, 55, 255), width=12)
        d.ellipse([cx - 52, cy - 14, cx + 52, cy + 14], outline=(255, 248, 150, 255), width=6)
        d.arc([cx - 48, cy - 12, cx + 48, cy + 12], start=200, end=340, fill=(255, 255, 255, 255), width=4)
        draw_cute_star(d, cx - 56, cy - 14, 10, 4, (120, 248, 255, 255))
        draw_cute_star(d, cx + 56, cy - 14, 10, 4, (120, 248, 255, 255))

    elif part_name == "wings":
        # Cute Plump Chibi Bat / Little Demon Wings with Heart Thumbs & Scalloped Webbing
        cx, cy = 114 * SS + dx, 126 * SS + dy
        flap = (frame_idx % 2) * 10
        for side in [-1, 1]:
            sx = cx + (12 * SS if side > 0 else 0)
            # Outer plump wing membrane (Berry-Purple)
            pts_outer = [
                (sx, cy - 6),
                (sx + side * 52, cy - 58 - flap),
                (sx + side * 108, cy - 44 - flap),
                (sx + side * 116, cy - 4 - flap // 2),
                (sx + side * 86, cy + 28),
                (sx + side * 46, cy + 22),
                (sx + side * 12, cy + 32),
            ]
            d.polygon(pts_outer, fill=(108, 38, 138, 255))
            # Inner pastel pink-magenta membrane
            pts_inner = [
                (sx + side * 8, cy - 2),
                (sx + side * 50, cy - 46 - flap),
                (sx + side * 96, cy - 34 - flap),
                (sx + side * 98, cy - 6 - flap // 2),
                (sx + side * 76, cy + 18),
                (sx + side * 42, cy + 14),
            ]
            d.polygon(pts_inner, fill=(245, 78, 152, 255))
            # Cute curved upper wing-arm tube
            draw_bezier_tube(
                d,
                (sx, cy - 4), (sx + side * 28, cy - 38 - flap),
                (sx + side * 58, cy - 56 - flap), (sx + side * 104, cy - 40 - flap),
                r_start=8, r_end=5,
                col_dark=(78, 24, 105, 255), col_main=(155, 62, 192, 255), col_hi=(235, 175, 255, 255),
                steps=24
            )
            # Cute little pink heart/claw thumb at top wing joint!
            draw_cute_heart(d, sx + side * 52, cy - 60 - flap, 10, (255, 115, 175, 255))
            # Glossy bubble shine on wing
            d.ellipse([sx + side * 62 - 6, cy - 26 - flap, sx + side * 62 + 6, cy - 16 - flap], fill=(255, 215, 238, 255))

    elif part_name == "fairy_wings":
        # Cute Sparkly Butterfly / Pixie Tear-Drop Wings
        cx, cy = 114 * SS + dx, 126 * SS + dy
        flare = (frame_idx % 2) * 8
        for side in [-1, 1]:
            sx = cx + (14 * SS if side > 0 else 0)
            # Lower plump sakura-pink petal
            draw_bezier_tube(
                d,
                (sx, cy + 8), (sx + side * 42, cy + 12),
                (sx + side * 82 + side * flare, cy + 42), (sx + side * 36, cy + 50),
                r_start=10, r_end=22,
                col_dark=(225, 95, 185, 235), col_main=(255, 165, 228, 240), col_hi=(255, 235, 250, 255),
                steps=24
            )
            # Upper plump pastel sky-blue & mint butterfly petal
            draw_bezier_tube(
                d,
                (sx, cy - 6), (sx + side * 56, cy - 58 - flare),
                (sx + side * 112 + side * flare, cy - 46 - flare), (sx + side * 72, cy - 6),
                r_start=12, r_end=28,
                col_dark=(45, 185, 245, 235), col_main=(135, 245, 255, 245), col_hi=(235, 255, 255, 255),
                steps=28
            )
            # Cute inner glowing dewdrop & twinkling star on each wing
            d.ellipse([sx + side * 74 - 10, cy - 36 - flare, sx + side * 74 + 10, cy - 18 - flare], fill=(255, 255, 255, 245))
            draw_cute_star(d, sx + side * 92, cy - 44 - flare, 11, 4, (255, 250, 140, 255))

    elif part_name == "shell":
        # Cute Plump Koopa / Emerald Tortoise Shell with Fluffy Cream Rim
        cx, cy = 100 * SS + dx, 132 * SS + dy
        # Emerald dome
        d.ellipse([cx - 42, cy - 46, cx + 26, cy + 50], fill=(38, 148, 112, 255))
        d.ellipse([cx - 36, cy - 40, cx + 18, cy + 42], fill=(72, 212, 158, 255))
        # Cute rounded hexagonal shell markings
        for py in [cy - 22, cy, cy + 22]:
            d.rounded_rectangle([cx - 28, py - 9, cx - 8, py + 9], radius=6, fill=(42, 162, 122, 255))
        # Glossy white bubble highlight on dome
        d.ellipse([cx - 30, cy - 30, cx - 16, cy - 12], fill=(215, 255, 238, 255))
        d.ellipse([cx - 26, cy - 26, cx - 20, cy - 18], fill=(255, 255, 255, 255))
        # Fluffy cream-white ruffled shell rim along the right/back edge
        for ry_rim in range(cy - 38, cy + 44, 14):
            d.ellipse([cx - 8, ry_rim - 10, cx + 14, ry_rim + 10], fill=(255, 248, 225, 255))

    elif part_name == "booster":
        # Cute Chubby Capsule Rocket Backpack with Star Badge & Puffy Cartoon Flame Clouds
        cx, cy = 94 * SS + dx, 126 * SS + dy
        flare = pulse + (16 if cfg.get("vfx") else 0)
        # Puffy cartoon flame clouds shooting out the bottom
        d.ellipse([cx - 28, cy + 24, cx + 8, cy + 64 + flare], fill=(255, 105, 45, 255))
        d.ellipse([cx - 22, cy + 26, cx + 2, cy + 52 + flare], fill=(255, 215, 65, 255))
        d.ellipse([cx - 18, cy + 26, cx - 2, cy + 40 + flare // 2], fill=(255, 255, 255, 255))
        # Cute rounded capsule rocket body (Enamel White & Pastel Blue)
        d.rounded_rectangle([cx - 30, cy - 34, cx + 12, cy + 26], radius=18, fill=(185, 215, 245, 255))
        d.rounded_rectangle([cx - 26, cy - 30, cx + 8, cy + 20], radius=14, fill=(242, 250, 255, 255))
        # Cute coral-red rocket nose-cap at top & thruster nozzle at bottom
        d.chord([cx - 30, cy - 36, cx + 12, cy - 6], start=180, end=360, fill=(255, 75, 115, 255))
        d.rounded_rectangle([cx - 24, cy + 20, cx + 4, cy + 30], radius=5, fill=(85, 102, 132, 255))
        # Cute round cyan porthole & golden star badge
        d.ellipse([cx - 20, cy - 12, cx - 2, cy + 6], fill=(0, 232, 255, 255))
        d.ellipse([cx - 16, cy - 9, cx - 9, cy - 2], fill=(255, 255, 255, 255))

    elif part_name == "crystals":
        # Cute Floating Pastel Star-Candy / Magic Crystal Cluster (Both Shoulders!)
        cx, cy = 120 * SS + dx, 124 * SS + dy
        crystal_specs = [
            (cx - 38, cy - 26, (cx - 68, cy - 54), (85, 248, 195, 255), (205, 255, 238, 255)),
            (cx - 44, cy + 2,  (cx - 76, cy - 8),  (115, 235, 255, 255), (225, 252, 255, 255)),
            (cx - 34, cy + 24, (cx - 60, cy + 34), (255, 145, 220, 255), (255, 225, 245, 255)),
            (cx + 38, cy - 26, (cx + 68, cy - 54), (85, 248, 195, 255), (205, 255, 238, 255)),
            (cx + 44, cy + 2,  (cx + 76, cy - 8),  (115, 235, 255, 255), (225, 252, 255, 255)),
            (cx + 34, cy + 24, (cx + 60, cy + 34), (255, 145, 220, 255), (255, 225, 245, 255)),
        ]
        for bx_c, by_c, (tx_c, ty_c), c_main, c_hi in crystal_specs:
            draw_bezier_tube(
                d,
                (bx_c, by_c), ((bx_c + tx_c) // 2, (by_c + ty_c) // 2 - 4),
                (tx_c, ty_c), (tx_c, ty_c),
                r_start=11, r_end=6,
                col_dark=(45, 165, 145, 255), col_main=c_main, col_hi=c_hi,
                steps=16
            )
        draw_cute_star(d, cx - 72, cy - 32, 10, 4, (255, 255, 190, 255))
        draw_cute_star(d, cx + 72, cy - 32, 10, 4, (255, 255, 190, 255))

    elif part_name == "spikes":
        # Cute Plump Dino/Dragon Shoulder Pauldrons with Rounded Chubby Horns
        lx, ly = 102 * SS + dx, 118 * SS + dy
        rx, ry = 136 * SS + dx, 118 * SS + dy
        for sx, sy, side in [(lx, ly, -1), (rx, ry, 1)]:
            # Plump coral-orange shoulder pad dome
            d.ellipse([sx - 20, sy - 14, sx + 20, sy + 16], fill=(245, 95, 55, 255))
            d.ellipse([sx - 16, sy - 12, sx + 16, sy + 10], fill=(255, 145, 75, 255))
            # Cute chubby golden horn sticking out
            draw_bezier_tube(
                d,
                (sx + side * 6, sy - 4), (sx + side * 20, sy - 18),
                (sx + side * 32, sy - 26), (sx + side * 36, sy - 30),
                r_start=9, r_end=4,
                col_dark=(225, 155, 25, 255), col_main=(255, 225, 65, 255), col_hi=(255, 255, 210, 255),
                steps=16
            )
            # Glossy bubble shine
            d.ellipse([sx - 6, sy - 8, sx + 4, sy - 1], fill=(255, 235, 195, 255))

    elif part_name == "core":
        # Cute Magical Winged Heart-Crystal Chest Brooch (Symmetric Left & Right Winglets!)
        cx, cy = 122 * SS + dx, 126 * SS + dy
        d.ellipse([cx - 34, cy - 12, cx - 6, cy + 4], fill=(255, 245, 190, 255))
        d.ellipse([cx - 28, cy - 2, cx - 6, cy + 10], fill=(255, 255, 255, 255))
        d.ellipse([cx + 6, cy - 12, cx + 34, cy + 4], fill=(255, 245, 190, 255))
        d.ellipse([cx + 6, cy - 2, cx + 28, cy + 10], fill=(255, 255, 255, 255))
        # Golden brooch frame & plump glowing cyan/pink heart gem
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 205, 55, 255))
        draw_cute_heart(d, cx, cy - 1, 11, (0, 242, 255, 255))

    elif part_name == "tail":
        # Cute Bouncy S-Curved Chibi Tail with Plump Heart Tip & Ribbon
        cx, cy = 100 * SS + dx, 156 * SS + dy
        wave = (frame_idx % 3 - 1) * 8
        p0 = (cx, cy)
        p1 = (cx - 38, cy + 26 + wave)
        p2 = (cx - 78, cy + 14 - wave)
        p3 = (cx - 106, cy - 28 + wave // 2)
        draw_bezier_tube(
            d, p0, p1, p2, p3,
            r_start=9, r_end=6,
            col_dark=(95, 38, 125, 255), col_main=(168, 78, 212, 255), col_hi=(235, 185, 255, 255),
            steps=40
        )
        # Cute plump berry-pink Heart Tip at the end of the tail!
        draw_cute_heart(d, p3[0] - 6, p3[1] - 6, 18, (255, 55, 125, 255))

    elif part_name == "claws":
        # Cute Oversized Chibi Cat/Beast Paw Gauntlet with Pink Paw-Pad & Chubby Claws
        hx, hy, _ = get_hand_pos_and_angle(cfg)
        c_ss = Image.new("RGBA", (128 * SS, 128 * SS), (0, 0, 0, 0))
        cd = ImageDraw.Draw(c_ss)
        gx, gy = 40 * SS, 64 * SS
        # Plump rounded cat-paw glove body
        cd.ellipse([gx - 22, gy - 22, gx + 22, gy + 22], fill=(255, 238, 245, 255))
        cd.ellipse([gx - 18, gy - 18, gx + 18, gy + 18], fill=(255, 250, 252, 255))
        # Cute pink main paw-pad + 3 toe beans!
        cd.ellipse([gx - 10, gy - 8, gx + 6, gy + 8], fill=(255, 105, 165, 255))
        for ty_bean in [-11, 0, 11]:
            cd.ellipse([gx + 6, gy + ty_bean - 5, gx + 16, gy + ty_bean + 5], fill=(255, 125, 180, 255))
            # Chubby, rounded glowing cyan/white crystal claw
            cd.polygon([
                (gx + 14, gy + ty_bean - 6),
                (gx + 52, gy + ty_bean),
                (gx + 14, gy + ty_bean + 6)
            ], fill=(115, 245, 255, 255))
            cd.line([(gx + 16, gy + ty_bean - 1), (gx + 44, gy + ty_bean)], fill=(255, 255, 255, 255), width=4)
        c_cv = c_ss.resize((128, 128), Image.Resampling.LANCZOS)
        c_cv = add_fast_anime_outline(c_cv, size=5)
        rot_c = rotate_smooth_hd(c_cv, (40, 64), cfg["fa_swing"] - 28)
        im = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        im.paste(rot_c, (hx - 40, hy - 64), rot_c)
        return im

    im = ss_im.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    im = add_fast_anime_outline(im, size=5)
    return im

def build_all():
    print("=== Building All 576 240x240 HD Hero, Nemesis, Weapon, Armor, and 13 Mutation Sprites ===")

    male_torso_layers = {}
    male_fa_layers = {}
    male_ba_layers = {}
    female_torso_layers = {}
    female_fa_layers = {}
    female_ba_layers = {}

    for female in [False, True]:
        prefix = "female" if female else "male"
        path = f"assets/pixel_hero/master_{prefix}_clean.png"
        hi_master, head, torso, f_arm, b_arm, l_leg, r_leg, piv = build_hd_parts_from_master(path, female=female)
        mw, mh = hi_master.size
        bx = (CANVAS_W - mw) // 2 + (10 if female else 0)
        by = CANVAS_H - mh - 4

        for motion, cfg_list in MOTION_CONFIGS.items():
            for f_idx, cfg in enumerate(cfg_list):
                cv = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
                ox, oy = bx + cfg["dx"] * SCALE, by + cfg["dy"] * SCALE

                r_ba = rotate_limb(b_arm, piv["b_arm"], cfg["ba_swing"])
                r_rl = rotate_limb(r_leg, piv["r_leg"], cfg["rl_swing"])
                r_ll = rotate_limb(l_leg, piv["l_leg"], cfg["ll_swing"])
                r_t = rotate_body(torso, piv["torso"], cfg["torso_lean"])
                r_h = rotate_body(head, piv["head"], cfg["head_lean"])
                r_fa = rotate_limb(f_arm, piv["f_arm"], cfg["fa_swing"])

                # If idle_0 (all angles 0), use unsegmented hi_master for 100% seamless body, else composite limbs
                if cfg["head_lean"] == 0 and cfg["torso_lean"] == 0 and cfg["fa_swing"] == 0 and cfg["ba_swing"] == 0 and cfg["ll_swing"] == 0 and cfg["rl_swing"] == 0:
                    cv.paste(hi_master, (ox, oy), hi_master)
                else:
                    cv.paste(r_ba, (ox, oy), r_ba)
                    cv.paste(r_rl, (ox, oy + cfg["rl_dy"] * SCALE), r_rl)
                    cv.paste(r_ll, (ox, oy + cfg["ll_dy"] * SCALE), r_ll)
                    cv.paste(r_t, (ox, oy), r_t)
                    cv.paste(r_h, (ox, oy), r_h)
                    cv.paste(r_fa, (ox, oy), r_fa)

                cv = add_fast_anime_outline(cv, size=5)

                t_cv = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
                t_cv.paste(r_t, (ox, oy), r_t)
                fa_cv = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
                fa_cv.paste(r_fa, (ox, oy), r_fa)
                ba_cv = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
                ba_cv.paste(r_ba, (ox, oy), r_ba)

                if not female:
                    male_torso_layers[(motion, f_idx)] = t_cv
                    male_fa_layers[(motion, f_idx)] = fa_cv
                    male_ba_layers[(motion, f_idx)] = ba_cv
                else:
                    female_torso_layers[(motion, f_idx)] = t_cv
                    female_fa_layers[(motion, f_idx)] = fa_cv
                    female_ba_layers[(motion, f_idx)] = ba_cv

                cv.save(os.path.join(HERO_DIR, f"{prefix}_{motion}_{f_idx}.png"))

                hx, hy, _ = get_hand_pos_and_angle(cfg)
                nem_cv = make_nemesis_variant(cv, t_cv, fa_cv, ba_cv, hx, hy, cfg["fa_swing"], cfg["vfx"], cfg, is_female=female)
                nem_cv.save(os.path.join(HERO_DIR, f"{prefix}_nemesis_{motion}_{f_idx}.png"))

    shutil.copy(os.path.join(HERO_DIR, "female_idle_0.png"), "assets/pixel_agents/agent_female_trainee_1.png")
    shutil.copy(os.path.join(HERO_DIR, "male_idle_0.png"), "assets/pixel_agents/agent_male_trainee_1.png")
    shutil.copy(os.path.join(HERO_DIR, "female_idle_0.png"), os.path.join(HERO_DIR, "preview_classic_female.png"))
    shutil.copy(os.path.join(HERO_DIR, "male_idle_0.png"), os.path.join(HERO_DIR, "preview_classic_male.png"))

    weapons = ["katana", "axe", "crystal_sword", "heavy_cannon", "lava_launcher"]
    for w_name in weapons:
        for motion, cfg_list in MOTION_CONFIGS.items():
            for f_idx, cfg in enumerate(cfg_list):
                w_im = draw_rotated_weapon(w_name, cfg)
                w_im.save(os.path.join(WEAPONS_DIR, f"{w_name}_{motion}_{f_idx}.png"))

    armors = ["military", "leather", "nano_carbon", "hardlight", "yeti_fur"]
    for a_name in armors:
        for motion, cfg_list in MOTION_CONFIGS.items():
            for f_idx, cfg in enumerate(cfg_list):
                a_im = build_contour_armor_frame(
                    a_name,
                    male_torso_layers[(motion, f_idx)],
                    male_fa_layers[(motion, f_idx)],
                    male_ba_layers[(motion, f_idx)],
                    cfg,
                    is_female=False
                )
                a_im.save(os.path.join(ARMORS_DIR, f"{a_name}_{motion}_{f_idx}.png"))

                fa_im = build_contour_armor_frame(
                    a_name,
                    female_torso_layers[(motion, f_idx)],
                    female_fa_layers[(motion, f_idx)],
                    female_ba_layers[(motion, f_idx)],
                    cfg,
                    is_female=True
                )
                fa_im.save(os.path.join(ARMORS_DIR, f"female_{a_name}_{motion}_{f_idx}.png"))

    parts = [
        "horns", "tail", "visor", "wings", "shell", "fairy_wings",
        "booster", "spikes", "antennae", "claws", "core", "crystals", "halo"
    ]
    for p_name in parts:
        for motion, cfg_list in MOTION_CONFIGS.items():
            for f_idx, cfg in enumerate(cfg_list):
                p_im = draw_mutation_frame(p_name, cfg, f_idx, male_fa_layers[(motion, f_idx)])
                p_im.save(os.path.join(MUT_DIR, f"{p_name}_{motion}_{f_idx}.png"))

    print("SUCCESS: All 576 240x240 HD Hero, Nemesis, Weapon, Armor, and Mutation sprites built!")

if __name__ == "__main__":
    build_all()
