# -*- coding: utf-8 -*-
"""
Precision Anatomical Segmentation & Skeletal Animation Test for Male & Female Heroes
Verifies zero ghost limbs, zero torso-chop, and natural limb swinging.
"""
import os, math
from PIL import Image, ImageDraw

OUT_HERO = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
CANVAS_W = 120
CANVAS_H = 120

def load_master_and_flip(path, target_h=90):
    im = Image.open(path).convert("RGBA")
    im_flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    mw, mh = im_flipped.size
    target_w = int(mw * (target_h / mh))
    base = im_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    alpha = base.split()[3].point(lambda p: 255 if p > 70 else 0)
    rgb = base.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    return rgb

def segment_male(master):
    """
    Male master is 56x90 (facing right).
    Exact anatomy:
    - Head: y = 0..29
    - Foreground Arm (f_arm, screen-left): x = 16..24, y = 30..60, pivot = (21, 34)
    - Background Arm (b_arm, screen-right): synthesized/extracted from sleeve x = 34..40, y = 31..55, pivot = (36, 34)
    - Torso (shirt + belt + pelvis): x = 21..39, y = 28..60 (with f_arm skin at x<=23, y>=38 removed)
    - Foreground Leg (l_leg, screen-left): x = 14..28, y = 58..90, pivot = (23, 60)
    - Background Leg (r_leg, screen-right): x = 29..47, y = 58..90, pivot = (35, 60)
    """
    w, h = master.size
    pix = master.load()

    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    b_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # 1. Head (y = 0..29)
    head.paste(master.crop((0, 0, w, 29)), (0, 0))

    # 2. Foreground Arm (x = 16..24, y = 30..60)
    f_arm_pix = f_arm.load()
    for y in range(30, 60):
        for x in range(16, 25):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            # At y >= 48, x >= 23 is part of belt/jeans on torso, except fist at y=53..59, x=17..23
            if y >= 48 and x >= 24:
                continue
            if 38 <= y <= 47 and x >= 23 and (r > 200 and g > 195 and b > 175):
                # White shirt body belongs to torso
                continue
            f_arm_pix[x, y] = (r, g, b, a)

    # 3. Torso (y = 28..60, excluding f_arm pixels so no ghost arm remains!)
    torso_pix = torso.load()
    for y in range(28, 61):
        for x in range(20, 39):
            if f_arm_pix[x, y][3] > 0 and y >= 36:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            # Exclude right-edge background arm skin pixels at x >= 36, y >= 38
            if x >= 36 and 38 <= y <= 48 and (r > 160 and g < 150):
                continue
            torso_pix[x, y] = (r, g, b, a)

    # Fill the left side seam of torso (x = 22..24, y = 36..58) where f_arm used to cover it
    for y in range(36, 48):
        if torso_pix[25, y][3] > 0:
            torso_pix[24, y] = torso_pix[25, y]
            torso_pix[23, y] = (160, 150, 138, 255) # shirt shadow outline
    for y in range(48, 52):
        torso_pix[23, y] = (75, 42, 26, 255) # belt
        torso_pix[22, y] = (26, 20, 32, 255)
    for y in range(52, 60):
        torso_pix[23, y] = (46, 68, 98, 255) # jeans
        torso_pix[22, y] = (26, 20, 32, 255)

    # 4. Background Arm (b_arm, screen-right, behind torso, pivot = (35, 34))
    bd = ImageDraw.Draw(b_arm)
    # Sleeve
    bd.rectangle([33, 31, 38, 38], fill=(165, 155, 142, 255), outline=(26, 20, 32, 255))
    # Forearm (shaded skin)
    bd.rectangle([34, 38, 38, 50], fill=(205, 138, 102, 255), outline=(26, 20, 32, 255))
    # Wristband
    bd.rectangle([34, 49, 39, 52], fill=(75, 42, 26, 255))
    # Fist
    bd.rectangle([34, 52, 39, 57], fill=(195, 128, 92, 255), outline=(26, 20, 32, 255))

    # 5. Legs (y = 58..90)
    l_leg.paste(master.crop((14, 58, 29, h)), (14, 58))
    r_leg.paste(master.crop((29, 58, 48, h)), (29, 58))

    pivots = {
        "head": (28, 27),
        "torso": (29, 45),
        "f_arm": (21, 34),
        "b_arm": (36, 34),
        "l_leg": (23, 60),
        "r_leg": (35, 60),
        "hand_local": (21, 56), # resting fist center on f_arm
    }
    return head, torso, f_arm, b_arm, l_leg, r_leg, pivots

def segment_female(master):
    """
    Female master is 47x90 (facing right).
    Exact anatomy:
    - Head + Ponytail: y = 0..24 (plus ponytail at x = 5..13, y = 4..35)
    - Foreground Arm (f_arm, screen-left): x = 8..15, y = 26..52, pivot = (13, 29)
    - Background Arm (b_arm, screen-right): x = 26..31, y = 27..52, pivot = (27, 29)
    - Torso (shirt y=24..40, shorts pelvis y=40..51): x = 13..28, y = 24..51
    - Foreground Leg (l_leg, screen-left): x = 12..21, y = 49..88, pivot = (16, 51)
    - Background Leg (r_leg, screen-right): x = 21..31, y = 49..88, pivot = (25, 51)
    """
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
    l_leg_pix = l_leg.load()
    r_leg_pix = r_leg.load()

    # 1. Head (y = 0..24, plus ponytail at x <= 12, y = 24..35)
    for y in range(0, 36):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            if y < 24:
                head_pix[x, y] = (r, g, b, a)
            elif x <= 11 and (r > 160 and g > 90 and b < 110):
                # Golden ponytail hair pixels
                head_pix[x, y] = (r, g, b, a)

    # 2. Foreground Arm (x = 8..15, y = 26..52)
    for y in range(26, 53):
        for x in range(8, 16):
            if head_pix[x, y][3] > 0:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            # Exclude denim shorts at y >= 40, x >= 12
            if y >= 40 and x >= 12 and (b > r or (r < 110 and g < 110)):
                continue
            # Exclude inner white shirt at y <= 39, x >= 15
            if y <= 39 and x >= 15:
                continue
            f_arm_pix[x, y] = (r, g, b, a)

    # 3. Torso (x = 12..28, y = 24..51, excluding f_arm and head)
    for y in range(24, 52):
        for x in range(12, 28):
            if head_pix[x, y][3] > 0 or f_arm_pix[x, y][3] > 0:
                continue
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            torso_pix[x, y] = (r, g, b, a)

    # Cleanly fill torso left edge behind f_arm (x = 14..15, y = 28..39)
    for y in range(28, 40):
        if torso_pix[16, y][3] > 0:
            torso_pix[15, y] = torso_pix[16, y]
            torso_pix[14, y] = (180, 170, 155, 255)

    # 4. Background Arm (b_arm, screen-right, pivot = (27, 29))
    bd = ImageDraw.Draw(b_arm)
    bd.rectangle([25, 26, 29, 33], fill=(215, 205, 190, 255), outline=(90, 70, 60, 255))
    bd.rectangle([26, 33, 29, 45], fill=(235, 185, 155, 255), outline=(120, 85, 65, 255))
    bd.rectangle([26, 44, 30, 47], fill=(230, 230, 235, 255)) # white wristband
    bd.rectangle([26, 47, 30, 51], fill=(235, 185, 155, 255), outline=(120, 85, 65, 255))

    # 5. Legs (y = 50..88, filtering out ground shadow)
    for y in range(50, h):
        for x in range(11, 32):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            # Remove pale ground shadow around feet (y >= 84 and very bright/greyish)
            if y >= 84 and r > 220 and g > 220 and b > 210:
                continue
            if x <= 20:
                l_leg_pix[x, y] = (r, g, b, a)
            else:
                r_leg_pix[x, y] = (r, g, b, a)

    pivots = {
        "head": (21, 22),
        "torso": (21, 38),
        "f_arm": (13, 29),
        "b_arm": (27, 29),
        "l_leg": (16, 51),
        "r_leg": (25, 51),
        "hand_local": (11, 49),
    }
    return head, torso, f_arm, b_arm, l_leg, r_leg, pivots

def rotate_limb(img, pivot, swing_right_deg):
    """
    swing_right_deg > 0 swings a downward-hanging limb FORWARD (to the right, counter-clockwise in PIL).
    swing_right_deg < 0 swings a downward-hanging limb BACKWARD (to the left, clockwise in PIL).
    """
    if swing_right_deg == 0:
        return img
    return img.rotate(swing_right_deg, resample=Image.Resampling.NEAREST, center=pivot)

def rotate_body(img, pivot, lean_right_deg):
    """
    lean_right_deg > 0 tilts the upper body/head FORWARD (to the right, clockwise in PIL).
    """
    if lean_right_deg == 0:
        return img
    return img.rotate(-lean_right_deg, resample=Image.Resampling.NEAREST, center=pivot)

def test_render():
    for female in [False, True]:
        prefix = "female" if female else "male"
        master = load_master_and_flip(f"assets/pixel_hero/master_{prefix}_clean.png", target_h=90)
        mw, mh = master.size
        bx = (CANVAS_W - mw) // 2
        by = CANVAS_H - mh - 2

        if female:
            head, torso, f_arm, b_arm, l_leg, r_leg, piv = segment_female(master)
        else:
            head, torso, f_arm, b_arm, l_leg, r_leg, piv = segment_male(master)

        def compose(dx=0, dy=0, head_lean=0, torso_lean=0,
                    fa_swing=0, ba_swing=0, ll_swing=0, rl_swing=0,
                    ll_dy=0, rl_dy=0):
            cv = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
            ox, oy = bx + dx, by + dy

            # 1. Background Arm (behind torso)
            r_ba = rotate_limb(b_arm, piv["b_arm"], ba_swing)
            cv.paste(r_ba, (ox, oy), r_ba)

            # 2. Background Leg (r_leg)
            r_rl = rotate_limb(r_leg, piv["r_leg"], rl_swing)
            cv.paste(r_rl, (ox, oy + rl_dy), r_rl)

            # 3. Foreground Leg (l_leg)
            r_ll = rotate_limb(l_leg, piv["l_leg"], ll_swing)
            cv.paste(r_ll, (ox, oy + ll_dy), r_ll)

            # 4. Torso
            r_t = rotate_body(torso, piv["torso"], torso_lean)
            cv.paste(r_t, (ox, oy), r_t)

            # 5. Head
            r_h = rotate_body(head, piv["head"], head_lean)
            cv.paste(r_h, (ox, oy), r_h)

            # 6. Foreground Arm (in front of torso)
            r_fa = rotate_limb(f_arm, piv["f_arm"], fa_swing)
            cv.paste(r_fa, (ox, oy), r_fa)

            return cv

        # Create a contact sheet of IDLE(4), RUN(6), ATTACK(4), SKILL(4)
        sheet = Image.new("RGBA", (CANVAS_W * 6, CANVAS_H * 4), (15, 20, 30, 255))

        # Row 0: IDLE (4f)
        idle_cfgs = [
            dict(dx=0, dy=0, fa_swing=0, ba_swing=0),
            dict(dx=0, dy=-1, fa_swing=4, ba_swing=-4),
            dict(dx=0, dy=-2, fa_swing=7, ba_swing=-7),
            dict(dx=0, dy=-1, fa_swing=4, ba_swing=-4),
        ]
        for i, c in enumerate(idle_cfgs):
            sheet.paste(compose(**c), (i * CANVAS_W, 0))

        # Row 1: RUN (6f - true limb crossing!)
        run_cfgs = [
            dict(dx=2, dy=1, head_lean=4, torso_lean=6, fa_swing=28, ba_swing=-24, ll_swing=-22, rl_swing=22),
            dict(dx=3, dy=2, head_lean=5, torso_lean=8, fa_swing=14, ba_swing=-12, ll_swing=-10, rl_swing=12, ll_dy=-1),
            dict(dx=2, dy=-3, head_lean=3, torso_lean=5, fa_swing=-4, ba_swing=4, ll_swing=4, rl_swing=-4, ll_dy=-2, rl_dy=-2),
            dict(dx=2, dy=1, head_lean=4, torso_lean=6, fa_swing=-22, ba_swing=28, ll_swing=22, rl_swing=-22),
            dict(dx=3, dy=2, head_lean=5, torso_lean=8, fa_swing=-10, ba_swing=14, ll_swing=12, rl_swing=-10, rl_dy=-1),
            dict(dx=2, dy=-3, head_lean=3, torso_lean=5, fa_swing=4, ba_swing=-4, ll_swing=-4, rl_swing=4, ll_dy=-2, rl_dy=-2),
        ]
        for i, c in enumerate(run_cfgs):
            sheet.paste(compose(**c), (i * CANVAS_W, CANVAS_H))

        # Row 2: ATTACK (4f - windup -> forward slash -> followthrough -> guard)
        atk_cfgs = [
            dict(dx=-4, dy=1, head_lean=-5, torso_lean=-8, fa_swing=-38, ba_swing=20, ll_swing=-12, rl_swing=14),
            dict(dx=8, dy=0, head_lean=6, torso_lean=10, fa_swing=68, ba_swing=-25, ll_swing=-18, rl_swing=22),
            dict(dx=10, dy=0, head_lean=5, torso_lean=8, fa_swing=52, ba_swing=-18, ll_swing=-14, rl_swing=18),
            dict(dx=2, dy=0, head_lean=2, torso_lean=3, fa_swing=12, ba_swing=-6, ll_swing=-4, rl_swing=4),
        ]
        for i, c in enumerate(atk_cfgs):
            sheet.paste(compose(**c), (i * CANVAS_W, CANVAS_H * 2))

        # Row 3: SKILL (4f - crouch charge -> aerial upper burst -> mid-air climax -> slam landing)
        # Note: dx, dy applies to ALL parts including legs, so the body is NEVER severed!
        skill_cfgs = [
            dict(dx=-1, dy=4, head_lean=4, torso_lean=6, fa_swing=-28, ba_swing=-15, ll_swing=-10, rl_swing=12, ll_dy=-3, rl_dy=-3),
            dict(dx=5, dy=-14, head_lean=-4, torso_lean=-4, fa_swing=105, ba_swing=-30, ll_swing=-16, rl_swing=18, ll_dy=-2, rl_dy=-1),
            dict(dx=7, dy=-17, head_lean=4, torso_lean=6, fa_swing=78, ba_swing=-20, ll_swing=-20, rl_swing=22, ll_dy=-2, rl_dy=-2),
            dict(dx=4, dy=3, head_lean=6, torso_lean=8, fa_swing=32, ba_swing=-15, ll_swing=-12, rl_swing=16, ll_dy=-2, rl_dy=-2),
        ]
        for i, c in enumerate(skill_cfgs):
            sheet.paste(compose(**c), (i * CANVAS_W, CANVAS_H * 3))

        sheet.save(f"scratch/test_sheet_{prefix}.png")
        print(f"Saved scratch/test_sheet_{prefix}.png")

if __name__ == "__main__":
    test_render()
