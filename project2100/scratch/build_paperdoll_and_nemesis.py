import os
import math
from PIL import Image, ImageDraw

hero_dir = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
weapons_dir = os.path.join(hero_dir, "weapons")
armors_dir = os.path.join(hero_dir, "armors")
os.makedirs(weapons_dir, exist_ok=True)
os.makedirs(armors_dir, exist_ok=True)

CANVAS_W = 120
CANVAS_H = 120

# DNF / 16-bit Palettes
OUTLINE = (20, 16, 25, 255)

# Skin
SKIN_BASE = (248, 202, 164, 255)
SKIN_HL   = (255, 235, 215, 255)
SKIN_SHD  = (212, 150, 110, 255)
SKIN_DK   = (160,  95,  65, 255)

# Nemesis Colors
NEM_SKIN_BASE = (180, 185, 210, 255) # Ashen pale
NEM_SKIN_SHD  = (130, 135, 165, 255)
NEM_ARMOR_DK  = ( 22,  18,  30, 255)
NEM_ARMOR_MID = ( 45,  35,  60, 255)
NEM_ARMOR_HL  = ( 85,  70, 115, 255)
NEM_GLOW_RED  = (255,  35,  80, 255)
NEM_GLOW_PUR  = (180,  50, 255, 255)
NEM_SLASH_PUR = (220,  80, 255, 255)

def create_frame():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# =============================================================
# 1. NEMESIS CHARACTER GENERATION
# =============================================================

def draw_nemesis_head(d, cx, cy, female=True):
    ox, oy = cx - 20, cy - 20
    # Demonic Horns / Spikes
    d.polygon([(ox+10, oy+6), (ox+4, oy-6), (ox+14, oy+2)], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.polygon([(ox+30, oy+6), (ox+36, oy-6), (ox+26, oy+2)], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.point((ox+5, oy-4), fill=NEM_GLOW_RED)
    d.point((ox+35, oy-4), fill=NEM_GLOW_RED)

    # Hair (Wild Jet Black with Crimson Tips)
    d.rectangle([ox + 9, oy + 2, ox + 31, oy + 12], fill=NEM_ARMOR_MID, outline=OUTLINE)
    d.polygon([(ox+8, oy+10), (ox+4, oy+24), (ox+10, oy+16)], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.point((ox+5, oy+22), fill=NEM_GLOW_RED)
    d.polygon([(ox+30, oy+10), (ox+35, oy+24), (ox+29, oy+16)], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.point((ox+34, oy+22), fill=NEM_GLOW_RED)

    # Face Skin
    d.rectangle([ox + 12, oy + 10, ox + 30, oy + 26], fill=NEM_SKIN_BASE)
    d.polygon([(ox+14, oy+26), (ox+28, oy+26), (ox+25, oy+32), (ox+17, oy+32)], fill=NEM_SKIN_SHD, outline=OUTLINE)

    # Glowing Red / Void Eyes
    d.rectangle([ox + 16, oy + 17, ox + 20, oy + 22], fill=NEM_GLOW_RED)
    d.point((ox + 17, oy + 18), fill=(255, 255, 255, 255))
    d.rectangle([ox + 23, oy + 17, ox + 27, oy + 22], fill=NEM_GLOW_RED)
    d.point((ox + 24, oy + 18), fill=(255, 255, 255, 255))

    # Mouth line & sinister marking
    d.line([(ox + 19, oy + 28), (ox + 23, oy + 28)], fill=OUTLINE)
    d.line([(ox + 18, oy + 20), (ox + 18, oy + 24)], fill=NEM_GLOW_PUR)
    d.line([(ox + 24, oy + 20), (ox + 24, oy + 24)], fill=NEM_GLOW_PUR)

def draw_nemesis_torso(d, cx, cy):
    ox, oy = cx - 18, cy - 18
    # Heavy biomechanical carapace
    d.rectangle([ox + 8, oy + 8, ox + 28, oy + 30], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.rectangle([ox + 11, oy + 10, ox + 25, oy + 26], fill=NEM_ARMOR_MID)
    # Glowing Core
    d.rectangle([ox + 16, oy + 15, ox + 20, oy + 20], fill=NEM_GLOW_RED, outline=NEM_GLOW_PUR)
    d.point((ox + 18, oy + 17), fill=(255, 255, 255, 255))
    # Shoulder spikes
    d.polygon([(ox+8, oy+8), (ox+1, oy+2), (ox+6, oy+14)], fill=NEM_ARMOR_HL, outline=OUTLINE)
    d.polygon([(ox+28, oy+8), (ox+35, oy+2), (ox+30, oy+14)], fill=NEM_ARMOR_HL, outline=OUTLINE)
    # Waist belt
    d.rectangle([ox + 9, oy + 27, ox + 27, oy + 29], fill=NEM_GLOW_PUR)

def draw_nemesis_legs(d, cx, cy, leg_l_state=0, leg_r_state=0):
    ox, oy = cx - 20, cy - 8
    # Left Leg
    lx = ox + 8 + leg_l_state * 4
    ly = oy + 8
    d.rectangle([lx, ly, lx + 11, ly + 26], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.rectangle([lx + 2, ly + 2, lx + 9, ly + 14], fill=NEM_ARMOR_MID)
    d.line([(lx+3, ly+14), (lx+8, ly+14)], fill=NEM_GLOW_RED)
    d.rectangle([lx - 1, ly + 26, lx + 11, ly + 37], fill=NEM_ARMOR_HL, outline=OUTLINE)

    # Right Leg
    rx = ox + 21 + leg_r_state * 4
    ry = oy + 8
    d.rectangle([rx, ry, rx + 11, ry + 26], fill=NEM_ARMOR_DK, outline=OUTLINE)
    d.rectangle([rx + 2, ry + 2, rx + 9, ry + 14], fill=NEM_ARMOR_MID)
    d.line([(rx+3, ry+14), (rx+8, ry+14)], fill=NEM_GLOW_RED)
    d.rectangle([rx - 1, ry + 26, rx + 11, ry + 37], fill=NEM_ARMOR_HL, outline=OUTLINE)

def draw_nemesis_arm_l(d, sx, sy, state=0):
    d.rectangle([sx - 4, sy - 2, sx + 4, sy + 4], fill=NEM_ARMOR_DK, outline=OUTLINE)
    if state == 0:
        d.rectangle([sx - 3, sy + 4, sx + 4, sy + 18], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.point((sx, sy + 12), fill=NEM_GLOW_RED)
        d.rectangle([sx - 5, sy + 18, sx + 2, sy + 27], fill=NEM_ARMOR_HL, outline=OUTLINE)
    elif state == 1:
        d.polygon([(sx, sy), (sx-8, sy+8), (sx-4, sy+16)], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.rectangle([sx - 11, sy + 16, sx - 4, sy + 24], fill=NEM_ARMOR_HL, outline=OUTLINE)
    elif state == 2:
        d.polygon([(sx, sy), (sx+6, sy+8), (sx+4, sy+16)], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.rectangle([sx + 3, sy + 16, sx + 9, sy + 24], fill=NEM_ARMOR_HL, outline=OUTLINE)

def draw_nemesis_weapon(d, sx, sy, pose='ready'):
    # Nemesis Void Cleaver (검붉은 공허의 대검)
    d.rectangle([sx - 4, sy - 2, sx + 4, sy + 4], fill=NEM_ARMOR_DK, outline=OUTLINE)
    if pose == 'ready':
        d.rectangle([sx - 2, sy + 4, sx + 6, sy + 16], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.rectangle([sx + 2, sy + 16, sx + 8, sy + 22], fill=NEM_ARMOR_HL, outline=OUTLINE)
        # Giant Cleaver Blade extending up-right
        for i in range(30):
            bx = sx + 8 + i
            by = sy + 20 - int(i * 0.7)
            d.line([(bx, by-3), (bx, by+3)], fill=NEM_ARMOR_DK)
            d.point((bx, by), fill=NEM_GLOW_RED)
            d.point((bx, by-1), fill=NEM_GLOW_PUR)
        d.point((sx + 38, sy), fill=(255, 255, 255, 255))
    elif pose == 'windup':
        d.polygon([(sx, sy), (sx-4, sy-8), (sx-2, sy-14)], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.rectangle([sx - 4, sy - 16, sx + 3, sy - 9], fill=NEM_ARMOR_HL, outline=OUTLINE)
        for i in range(32):
            bx = sx - 4 - i
            by = sy - 12 - int(i * 0.4)
            d.line([(bx, by-3), (bx, by+3)], fill=NEM_ARMOR_DK)
            d.point((bx, by), fill=NEM_GLOW_RED)
    elif pose == 'slash':
        d.polygon([(sx, sy), (sx+10, sy+4), (sx+18, sy+2)], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.rectangle([sx + 16, sy, sx + 22, sy + 6], fill=NEM_ARMOR_HL, outline=OUTLINE)
        for i in range(34):
            bx = sx + 23 + i
            by = sy + 2 + int(i * 0.15)
            d.line([(bx, by-3), (bx, by+3)], fill=NEM_ARMOR_DK)
            d.point((bx, by), fill=NEM_GLOW_RED)
        # Giant Nemesis Void Slash Arc
        for deg in range(15, 150, 2):
            rad = math.radians(deg)
            r = 38
            cx = sx + 28 + int(r * math.cos(rad))
            cy = sy + 4 - int(r * math.sin(rad))
            d.line([(cx-2, cy-1), (cx+3, cy+3)], fill=NEM_SLASH_PUR, width=3)
            d.line([(cx-1, cy), (cx+1, cy+1)], fill=NEM_GLOW_RED, width=2)
            d.point((cx, cy), fill=(255, 255, 255, 255))
    elif pose == 'upper_slash':
        d.polygon([(sx, sy), (sx+4, sy-10), (sx+8, sy-16)], fill=NEM_ARMOR_MID, outline=OUTLINE)
        d.rectangle([sx + 6, sy - 18, sx + 13, sy - 12], fill=NEM_ARMOR_HL, outline=OUTLINE)
        for i in range(34):
            bx = sx + 10 + int(i * 0.1)
            by = sy - 15 - i
            d.line([(bx-3, by), (bx+3, by)], fill=NEM_ARMOR_DK)
            d.point((bx, by), fill=NEM_GLOW_RED)
        for deg in range(50, 180, 2):
            rad = math.radians(deg)
            r = 44
            cx = sx + 8 + int(r * math.cos(rad))
            cy = sy - 10 - int(r * math.sin(rad))
            d.line([(cx-2, cy-2), (cx+3, cy+3)], fill=NEM_SLASH_PUR, width=3)
            d.line([(cx-1, cy), (cx+1, cy)], fill=NEM_GLOW_RED, width=2)

def generate_nemesis_animations(female=True):
    prefix = f"{'female' if female else 'male'}_nemesis"
    # Idle
    for i in range(4):
        im = create_frame()
        d = ImageDraw.Draw(im)
        bob = -2 if i in [1, 2] else 0
        draw_nemesis_arm_l(d, 46, 46 + bob, state=0)
        draw_nemesis_legs(d, 56, 72, leg_l_state=0, leg_r_state=0)
        draw_nemesis_torso(d, 56, 52 + bob)
        draw_nemesis_head(d, 56, 28 + bob, female=female)
        draw_nemesis_weapon(d, 66, 48 + bob, pose='ready')
        im.save(os.path.join(hero_dir, f"{prefix}_idle_{i}.png"))

    # Run
    leg_cycles = [
        (-2, 2, 1, 'ready'),
        (-1, 1, 0, 'ready'),
        (0, 0, 2, 'ready'),
        (2, -2, 1, 'ready'),
        (1, -1, 0, 'ready'),
        (0, 0, 2, 'ready')
    ]
    for i, (ll, lr, arm_st, k_pose) in enumerate(leg_cycles):
        im = create_frame()
        d = ImageDraw.Draw(im)
        bob = -2 if i in [0, 3] else 0
        draw_nemesis_arm_l(d, 46, 46 + bob, state=arm_st)
        draw_nemesis_legs(d, 56, 72, leg_l_state=ll, leg_r_state=lr)
        draw_nemesis_torso(d, 56, 52 + bob)
        draw_nemesis_head(d, 58, 28 + bob, female=female)
        draw_nemesis_weapon(d, 66, 48 + bob, pose=k_pose)
        im.save(os.path.join(hero_dir, f"{prefix}_run_{i}.png"))

    # Attack
    attack_configs = [
        ('windup', -2, 2, 1, 0),
        ('slash', 0, 4, 1, 8),
        ('ready', 0, 3, 2, 6),
        ('ready', 0, 1, 0, 0)
    ]
    for i, (k_pose, ll, lr, arm_st, lunge_x) in enumerate(attack_configs):
        im = create_frame()
        d = ImageDraw.Draw(im)
        draw_nemesis_arm_l(d, 46 + lunge_x, 46, state=arm_st)
        draw_nemesis_legs(d, 56 + lunge_x, 72, leg_l_state=ll, leg_r_state=lr)
        draw_nemesis_torso(d, 56 + lunge_x, 52)
        draw_nemesis_head(d, 56 + lunge_x, 28, female=female)
        draw_nemesis_weapon(d, 66 + lunge_x, 48, pose=k_pose)
        im.save(os.path.join(hero_dir, f"{prefix}_attack_{i}.png"))

    # Skill
    skill_configs = [
        ('windup', 0, 1, 1, 0, 4),
        ('upper_slash', -1, 1, 2, 4, -14),
        ('ready', 0, 0, 1, 6, -18),
        ('slash', 1, 2, 1, 4, 4)
    ]
    for i, (k_pose, ll, lr, arm_st, lx, ly) in enumerate(skill_configs):
        im = create_frame()
        d = ImageDraw.Draw(im)
        draw_nemesis_arm_l(d, 46 + lx, 46 + ly, state=arm_st)
        draw_nemesis_legs(d, 56 + lx, 72 + (ly if ly > 0 else ly//2), leg_l_state=ll, leg_r_state=lr)
        draw_nemesis_torso(d, 56 + lx, 52 + ly)
        draw_nemesis_head(d, 56 + lx, 28 + ly, female=female)
        draw_nemesis_weapon(d, 66 + lx, 48 + ly, pose=k_pose)
        im.save(os.path.join(hero_dir, f"{prefix}_skill_{i}.png"))

# =============================================================
# 2. WEAPON OVERLAY GENERATION (5 Types)
# =============================================================
WEAPONS = {
    "katana": {
        "color_blade": (220, 235, 250, 255),
        "color_edge": (255, 255, 255, 255),
        "color_dark": (80, 90, 105, 255),
        "color_hilt": (70, 35, 20, 255),
        "color_guard": (240, 195, 40, 255),
        "slash_color": (120, 220, 255, 255),
        "type": "sword"
    },
    "axe": {
        "color_blade": (195, 200, 210, 255),
        "color_edge": (250, 250, 255, 255),
        "color_dark": (90, 80, 70, 255),
        "color_hilt": (110, 50, 25, 255),
        "color_guard": (200, 120, 40, 255),
        "slash_color": (255, 140, 40, 255),
        "type": "axe"
    },
    "crystal_sword": {
        "color_blade": (60, 240, 255, 255),
        "color_edge": (220, 255, 255, 255),
        "color_dark": (140, 40, 230, 255),
        "color_hilt": (40, 20, 60, 255),
        "color_guard": (255, 60, 180, 255),
        "slash_color": (0, 255, 230, 255),
        "type": "sword"
    },
    "heavy_cannon": {
        "color_blade": (80, 95, 115, 255),
        "color_edge": (160, 185, 210, 255),
        "color_dark": (35, 45, 55, 255),
        "color_hilt": (50, 50, 55, 255),
        "color_guard": (230, 170, 50, 255),
        "slash_color": (255, 220, 80, 255),
        "type": "gun"
    },
    "lava_launcher": {
        "color_blade": (160, 50, 30, 255),
        "color_edge": (255, 140, 30, 255),
        "color_dark": (50, 20, 20, 255),
        "color_hilt": (70, 30, 20, 255),
        "color_guard": (255, 80, 20, 255),
        "slash_color": (255, 60, 20, 255),
        "type": "gun"
    }
}

def draw_weapon_instance(d, sx, sy, w_key, pose='ready'):
    w = WEAPONS[w_key]
    wtype = w["type"]
    b_col = w["color_blade"]
    e_col = w["color_edge"]
    d_col = w["color_dark"]
    g_col = w["color_guard"]
    s_col = w["slash_color"]

    if wtype in ["sword", "axe"]:
        if pose == 'ready':
            # Hilt & Guard
            d.line([(sx + 5, sy + 12), (sx + 7, sy + 25)], fill=w["color_hilt"], width=2)
            d.rectangle([sx + 2, sy + 19, sx + 10, sy + 21], fill=g_col, outline=OUTLINE)
            if wtype == "sword":
                for i in range(26):
                    bx = sx + 8 + i
                    by = sy + 19 - int(i * 0.7)
                    d.point((bx, by - 1), fill=d_col)
                    d.point((bx, by), fill=b_col)
                    d.point((bx, by + 1), fill=e_col)
            else: # Axe
                for i in range(22):
                    bx = sx + 8 + i
                    by = sy + 19 - int(i * 0.7)
                    d.point((bx, by), fill=w["color_hilt"])
                # Axe Head
                ax, ay = sx + 22, sy + 9
                d.polygon([(ax-4, ay-8), (ax+8, ay-6), (ax+12, ay+4), (ax, ay+8)], fill=b_col, outline=OUTLINE)
                d.line([(ax+8, ay-6), (ax+12, ay+4)], fill=e_col, width=2)

        elif pose == 'windup':
            d.line([(sx - 2, sy - 18), (sx, sy - 6)], fill=w["color_hilt"], width=2)
            d.rectangle([sx - 5, sy - 12, sx + 3, sy - 10], fill=g_col, outline=OUTLINE)
            if wtype == "sword":
                for i in range(28):
                    bx = sx - 4 - i
                    by = sy - 12 - int(i * 0.4)
                    d.point((bx, by - 1), fill=d_col)
                    d.point((bx, by), fill=b_col)
                    d.point((bx, by + 1), fill=e_col)
            else:
                for i in range(22):
                    bx = sx - 4 - i
                    by = sy - 12 - int(i * 0.4)
                    d.point((bx, by), fill=w["color_hilt"])
                ax, ay = sx - 22, sy - 18
                d.polygon([(ax-8, ay-6), (ax+4, ay-8), (ax, ay+8), (ax-10, ay+2)], fill=b_col, outline=OUTLINE)

        elif pose == 'slash':
            d.rectangle([sx + 21, sy - 2, sx + 23, sy + 6], fill=g_col, outline=OUTLINE)
            if wtype == "sword":
                for i in range(32):
                    bx = sx + 23 + i
                    by = sy + 2 + int(i * 0.15)
                    d.point((bx, by - 1), fill=d_col)
                    d.point((bx, by), fill=b_col)
                    d.point((bx, by + 1), fill=e_col)
            else:
                for i in range(26):
                    bx = sx + 23 + i
                    by = sy + 2 + int(i * 0.15)
                    d.point((bx, by), fill=w["color_hilt"])
                ax, ay = sx + 44, sy + 4
                d.polygon([(ax-2, ay-10), (ax+10, ay-8), (ax+12, ay+8), (ax-2, ay+8)], fill=b_col, outline=OUTLINE)
            # Slash Arc
            for deg in range(15, 145, 2):
                rad = math.radians(deg)
                r = 35
                cx = sx + 28 + int(r * math.cos(rad))
                cy = sy + 4 - int(r * math.sin(rad))
                d.line([(cx-1, cy), (cx+2, cy+2)], fill=s_col, width=2)
                d.point((cx, cy), fill=(255, 255, 255, 255))

        elif pose == 'upper_slash':
            d.rectangle([sx + 7, sy - 14, sx + 13, sy - 12], fill=g_col, outline=OUTLINE)
            if wtype == "sword":
                for i in range(32):
                    bx = sx + 10 + int(i * 0.1)
                    by = sy - 15 - i
                    d.point((bx - 1, by), fill=d_col)
                    d.point((bx, by), fill=b_col)
                    d.point((bx + 1, by), fill=e_col)
            else:
                for i in range(24):
                    bx = sx + 10 + int(i * 0.1)
                    by = sy - 15 - i
                    d.point((bx, by), fill=w["color_hilt"])
                ax, ay = sx + 10, sy - 35
                d.polygon([(ax-8, ay-4), (ax+8, ay-4), (ax+10, ay+8), (ax-10, ay+8)], fill=b_col, outline=OUTLINE)
            # Vertical Slash Arc
            for deg in range(60, 180, 2):
                rad = math.radians(deg)
                r = 38
                cx = sx + 8 + int(r * math.cos(rad))
                cy = sy - 10 - int(r * math.sin(rad))
                d.line([(cx, cy-1), (cx+2, cy+2)], fill=s_col, width=2)
                d.point((cx, cy), fill=(255, 255, 255, 255))

    elif wtype == "gun":
        # Chunky Heavy Weapon
        if pose in ['ready', 'windup']:
            d.rectangle([sx + 8, sy + 10, sx + 32, sy + 22], fill=b_col, outline=OUTLINE)
            d.rectangle([sx + 12, sy + 12, sx + 28, sy + 18], fill=e_col)
            d.rectangle([sx + 30, sy + 8, sx + 35, sy + 24], fill=d_col, outline=OUTLINE) # Muzzle
        elif pose in ['slash', 'upper_slash']: # Firing blast!
            d.rectangle([sx + 10, sy + 6, sx + 36, sy + 18], fill=b_col, outline=OUTLINE)
            d.rectangle([sx + 34, sy + 4, sx + 39, sy + 20], fill=d_col, outline=OUTLINE)
            # Muzzle flash burst
            d.polygon([(sx+38, sy+12), (sx+48, sy+2), (sx+58, sy+12), (sx+48, sy+22)], fill=s_col)
            d.polygon([(sx+40, sy+12), (sx+46, sy+6), (sx+52, sy+12), (sx+46, sy+18)], fill=(255, 255, 255, 255))

def generate_all_weapons():
    for w_key in WEAPONS:
        # Idle (4 frames)
        for i in range(4):
            im = create_frame()
            d = ImageDraw.Draw(im)
            bob = -2 if i in [1, 2] else 0
            draw_weapon_instance(d, 66, 48 + bob, w_key, pose='ready')
            im.save(os.path.join(weapons_dir, f"{w_key}_idle_{i}.png"))

        # Run (6 frames)
        for i in range(6):
            im = create_frame()
            d = ImageDraw.Draw(im)
            bob = -2 if i in [0, 3] else 0
            draw_weapon_instance(d, 66, 48 + bob, w_key, pose='ready')
            im.save(os.path.join(weapons_dir, f"{w_key}_run_{i}.png"))

        # Attack (4 frames)
        attack_poses = ['windup', 'slash', 'ready', 'ready']
        lunges = [0, 8, 6, 0]
        for i, (pose, lx) in enumerate(zip(attack_poses, lunges)):
            im = create_frame()
            d = ImageDraw.Draw(im)
            draw_weapon_instance(d, 66 + lx, 48, w_key, pose=pose)
            im.save(os.path.join(weapons_dir, f"{w_key}_attack_{i}.png"))

        # Skill (4 frames)
        skill_poses = ['windup', 'upper_slash', 'ready', 'slash']
        lx_ly = [(0, 4), (4, -14), (6, -18), (4, 4)]
        for i, (pose, (lx, ly)) in enumerate(zip(skill_poses, lx_ly)):
            im = create_frame()
            d = ImageDraw.Draw(im)
            draw_weapon_instance(d, 66 + lx, 48 + ly, w_key, pose=pose)
            im.save(os.path.join(weapons_dir, f"{w_key}_skill_{i}.png"))

# =============================================================
# 3. ARMOR OVERLAYS (5 Types)
# =============================================================
ARMORS = {
    "military": { # Joseon Military Uniform
        "color_main": (35, 55, 95, 255),
        "color_hl": (55, 85, 140, 255),
        "color_trim": (195, 40, 40, 255),
        "color_gold": (235, 190, 40, 255)
    },
    "leather": { # Lead Shielded Leather Trench
        "color_main": (85, 55, 35, 255),
        "color_hl": (120, 80, 50, 255),
        "color_trim": (50, 32, 20, 255),
        "color_gold": (180, 180, 190, 255)
    },
    "nano_carbon": { # High-tech Carbon Exoskeleton
        "color_main": (40, 44, 52, 255),
        "color_hl": (70, 78, 92, 255),
        "color_trim": (0, 240, 255, 255), # Neon cyan lines
        "color_gold": (0, 255, 200, 255)
    },
    "hardlight": { # Neutron Hardlight Barrier
        "color_main": (60, 180, 255, 200),
        "color_hl": (180, 240, 255, 240),
        "color_trim": (255, 255, 255, 255),
        "color_gold": (0, 140, 255, 255)
    },
    "yeti_fur": { # Bigfoot Yeti Fur Coat
        "color_main": (210, 215, 220, 255),
        "color_hl": (250, 250, 255, 255),
        "color_trim": (140, 145, 155, 255),
        "color_gold": (90, 70, 55, 255)
    }
}

def draw_armor_overlay(d, cx, cy, arm_key, tilt=0):
    a = ARMORS[arm_key]
    ox, oy = cx - 18, cy - 18
    # Main Chest Armor
    d.rectangle([ox + 7, oy + 8, ox + 29, oy + 30], fill=a["color_main"], outline=OUTLINE)
    d.rectangle([ox + 10, oy + 10, ox + 26, oy + 26], fill=a["color_hl"])
    # Trims / Plates
    d.line([(ox + 7, oy + 18), (ox + 29, oy + 18)], fill=a["color_trim"], width=2)
    d.rectangle([ox + 16, oy + 16, ox + 20, oy + 20], fill=a["color_gold"])
    # Pauldrons (Shoulder Guards)
    d.polygon([(ox+7, oy+6), (ox+1, oy+14), (ox+7, oy+16)], fill=a["color_trim"], outline=OUTLINE)
    d.polygon([(ox+29, oy+6), (ox+35, oy+14), (ox+29, oy+16)], fill=a["color_trim"], outline=OUTLINE)

def generate_all_armors():
    for arm_key in ARMORS:
        # Idle (4 frames)
        for i in range(4):
            im = create_frame()
            d = ImageDraw.Draw(im)
            bob = -2 if i in [1, 2] else 0
            draw_armor_overlay(d, 56, 52 + bob, arm_key)
            im.save(os.path.join(armors_dir, f"{arm_key}_idle_{i}.png"))

        # Run (6 frames)
        for i in range(6):
            im = create_frame()
            d = ImageDraw.Draw(im)
            bob = -2 if i in [0, 3] else 0
            draw_armor_overlay(d, 56, 52 + bob, arm_key)
            im.save(os.path.join(armors_dir, f"{arm_key}_run_{i}.png"))

        # Attack (4 frames)
        lunges = [0, 8, 6, 0]
        for i, lx in enumerate(lunges):
            im = create_frame()
            d = ImageDraw.Draw(im)
            draw_armor_overlay(d, 56 + lx, 52, arm_key)
            im.save(os.path.join(armors_dir, f"{arm_key}_attack_{i}.png"))

        # Skill (4 frames)
        lx_ly = [(0, 4), (4, -14), (6, -18), (4, 4)]
        for i, (lx, ly) in enumerate(lx_ly):
            im = create_frame()
            d = ImageDraw.Draw(im)
            draw_armor_overlay(d, 56 + lx, 52 + ly, arm_key)
            im.save(os.path.join(armors_dir, f"{arm_key}_skill_{i}.png"))

if __name__ == "__main__":
    print("1. Rendering Nemesis full sprite action sets (female & male)...")
    generate_nemesis_animations(female=True)
    generate_nemesis_animations(female=False)
    print("2. Rendering 5 Modular Weapon Action sets...")
    generate_all_weapons()
    print("3. Rendering 5 Modular Armor Overlay sets...")
    generate_all_armors()
    print("Done! All paperdoll equipment & Nemesis action sets rendered cleanly!")
