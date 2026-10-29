import os
import math
from PIL import Image, ImageDraw

out_dir = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
os.makedirs(out_dir, exist_ok=True)

# 120x120 canvas size for each frame
CANVAS_W = 120
CANVAS_H = 120

# DNF 16-Bit Arcade Palette
SKIN_HL   = (255, 235, 215, 255)
SKIN_BASE = (248, 202, 164, 255)
SKIN_SHD  = (212, 150, 110, 255)
SKIN_DK   = (160,  95,  65, 255)

EYE_WHT   = (255, 255, 255, 255)
EYE_BLU   = ( 30,  80, 160, 255)
EYE_DK    = ( 15,  25,  50, 255)

HAIR_F_HL  = (255, 245, 160, 255)
HAIR_F_MID = (235, 195,  80, 255)
HAIR_F_SHD = (175, 130,  40, 255)
HAIR_F_DK  = ( 95,  65,  15, 255)

HAIR_M_HL  = ( 85,  80, 100, 255)
HAIR_M_MID = ( 48,  44,  60, 255)
HAIR_M_SHD = ( 28,  24,  38, 255)
HAIR_M_DK  = ( 14,  12,  20, 255)

# Ragged Short-Sleeve (누더기 반팔 티셔츠)
SHIRT_HL   = (242, 238, 228, 255)
SHIRT_MID  = (204, 198, 184, 255)
SHIRT_SHD  = (148, 140, 126, 255)
SHIRT_FRY  = (108, 100,  88, 255)
SHIRT_OUT  = ( 55,  50,  42, 255)

# Ragged Denim Shorts (누더기 청 반바지)
DENIM_HL   = ( 85, 120, 160, 255)
DENIM_MID  = ( 52,  80, 115, 255)
DENIM_SHD  = ( 34,  55,  82, 255)
DENIM_FRY  = (125, 150, 185, 255)
DENIM_OUT  = ( 18,  30,  48, 255)

# Bandages & Leather
BND_WHT = (245, 245, 245, 255)
BND_MID = (205, 205, 210, 255)
BND_SHD = (145, 145, 155, 255)
BOOT_MID = ( 65,  45,  30, 255)
BOOT_DK  = ( 35,  22,  15, 255)

# Katana Blade
BLD_GLOW = (255, 255, 255, 255)
BLD_LGT  = (220, 235, 250, 255)
BLD_MID  = (150, 165, 185, 255)
BLD_DK   = ( 75,  85, 100, 255)
HILT_WD  = ( 60,  35,  20, 255)
GOLD_ACC = (240, 195,  40, 255)
SLASH_BLU = (120, 220, 255, 255)
SLASH_WHT = (255, 255, 255, 255)

OUTLINE = (25, 20, 28, 255)

def create_frame():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# -------------------------------------------------------------
# Base Drawer Helper Functions
# -------------------------------------------------------------
def draw_head(d, cx, cy, female=True, tilt=0):
    # cx, cy: center of face (around x=56, y=28)
    ox, oy = cx - 20, cy - 20
    
    # Hair Back
    if female:
        # Ponytail
        d.rectangle([ox + 2, oy + 8, ox + 10, oy + 26], fill=HAIR_F_SHD, outline=OUTLINE)
        d.rectangle([ox + 4, oy + 10, ox + 11, oy + 28], fill=HAIR_F_MID)
        d.rectangle([ox + 1, oy + 20, ox + 7, oy + 32], fill=HAIR_F_DK)
        # Ribbon knot
        d.rectangle([ox + 9, oy + 10, ox + 13, oy + 14], fill=(220, 50, 50, 255), outline=OUTLINE)
    else:
        # Spiky hair back
        d.polygon([(ox+4, oy+8), (ox+2, oy+18), (ox+8, oy+16)], fill=HAIR_M_SHD, outline=OUTLINE)
        d.polygon([(ox+32, oy+8), (ox+36, oy+18), (ox+30, oy+16)], fill=HAIR_M_SHD, outline=OUTLINE)

    # Face Skin Base
    d.rectangle([ox + 12, oy + 10, ox + 30, oy + 26], fill=SKIN_BASE)
    d.rectangle([ox + 14, oy + 12, ox + 28, oy + 24], fill=SKIN_HL)
    d.polygon([(ox+14, oy+26), (ox+28, oy+26), (ox+25, oy+32), (ox+17, oy+32)], fill=SKIN_SHD, outline=OUTLINE)

    # Eyes
    d.rectangle([ox + 16, oy + 17, ox + 20, oy + 23], fill=OUTLINE)
    d.rectangle([ox + 17, oy + 18, ox + 20, oy + 22], fill=EYE_BLU)
    d.point((ox + 17, oy + 18), fill=EYE_WHT)
    
    d.rectangle([ox + 23, oy + 17, ox + 27, oy + 23], fill=OUTLINE)
    d.rectangle([ox + 23, oy + 18, ox + 26, oy + 22], fill=EYE_BLU)
    d.point((ox + 24, oy + 18), fill=EYE_WHT)

    # Nose / Mouth
    d.point((ox + 21, oy + 25), fill=SKIN_DK)
    d.line([(ox + 20, oy + 28), (ox + 22, oy + 28)], fill=SKIN_DK)

    # Hair Front / Bangs
    h_mid = HAIR_F_MID if female else HAIR_M_MID
    h_hl  = HAIR_F_HL if female else HAIR_M_HL
    h_shd = HAIR_F_SHD if female else HAIR_M_SHD

    d.rectangle([ox + 11, oy + 2, ox + 31, oy + 11], fill=h_mid, outline=OUTLINE)
    d.rectangle([ox + 14, oy + 1, ox + 28, oy + 6], fill=h_hl)
    # Side strands
    d.polygon([(ox+11, oy+10), (ox+14, oy+22), (ox+10, oy+16)], fill=h_mid, outline=OUTLINE)
    d.polygon([(ox+28, oy+10), (ox+32, oy+16), (ox+29, oy+22)], fill=h_mid, outline=OUTLINE)
    # Center Bang spike
    d.polygon([(ox+18, oy+9), (ox+20, oy+15), (ox+23, oy+9)], fill=h_hl, outline=OUTLINE)

    # Headband (Female: Red, Male: Cheek bandage)
    if female:
        d.rectangle([ox + 12, oy + 7, ox + 30, oy + 9], fill=(210, 45, 45, 255))
    else:
        d.rectangle([ox + 24, oy + 24, ox + 28, oy + 26], fill=BND_WHT, outline=OUTLINE)

def draw_torso_ragged(d, cx, cy, tilt=0):
    # cx, cy: center of chest (around x=56, y=52)
    ox, oy = cx - 18, cy - 18
    # Neck
    d.rectangle([ox + 14, oy + 2, ox + 22, oy + 8], fill=SKIN_BASE)
    d.point((ox + 18, oy + 7), fill=SKIN_SHD)
    
    # Main T-Shirt
    d.rectangle([ox + 8, oy + 8, ox + 28, oy + 30], fill=SHIRT_MID, outline=SHIRT_OUT)
    d.rectangle([ox + 10, oy + 10, ox + 26, oy + 26], fill=SHIRT_HL)
    d.polygon([(ox+14, oy+8), (ox+22, oy+8), (ox+18, oy+13)], fill=SKIN_BASE, outline=SHIRT_OUT) # V-neck

    # Folds
    d.line([(ox+10, oy+17), (ox+14, oy+20)], fill=SHIRT_SHD)
    d.line([(ox+26, oy+17), (ox+22, oy+20)], fill=SHIRT_SHD)

    # Frayed Bottom Hem (누더기 실밥)
    d.rectangle([ox + 8, oy + 28, ox + 28, oy + 32], fill=SHIRT_SHD)
    for x in range(ox + 8, ox + 29, 3):
        d.point((x, oy + 32), fill=SHIRT_FRY)
        d.point((x, oy + 33), fill=SHIRT_OUT)

    # Belt / Waist cord
    d.rectangle([ox + 9, oy + 26, ox + 27, oy + 28], fill=(70, 45, 30, 255), outline=OUTLINE)
    d.rectangle([ox + 16, oy + 26, ox + 20, oy + 28], fill=GOLD_ACC)

    # Short Sleeves (Shoulder caps)
    d.polygon([(ox+8, oy+8), (ox+3, oy+14), (ox+8, oy+17)], fill=SHIRT_MID, outline=SHIRT_OUT)
    d.polygon([(ox+28, oy+8), (ox+33, oy+14), (ox+28, oy+17)], fill=SHIRT_MID, outline=SHIRT_OUT)

def draw_shorts_and_legs(d, cx, cy, leg_l_state=0, leg_r_state=0):
    # cx, cy: hips center (around x=56, y=72)
    ox, oy = cx - 20, cy - 8
    
    # Pelvis
    d.rectangle([ox + 10, oy + 2, ox + 30, oy + 8], fill=DENIM_SHD, outline=DENIM_OUT)

    # Left Leg (Character's left / back)
    lx = ox + 8 + leg_l_state * 4
    ly = oy + 8
    d.rectangle([lx, ly, lx + 11, ly + 11], fill=DENIM_MID, outline=DENIM_OUT)
    d.rectangle([lx + 2, ly + 2, lx + 9, ly + 9], fill=DENIM_HL)
    d.point((lx + 2, ly + 12), fill=DENIM_FRY)
    d.point((lx + 6, ly + 13), fill=DENIM_FRY)
    d.point((lx + 9, ly + 12), fill=DENIM_FRY)
    # Bare leg
    d.rectangle([lx + 2, ly + 12, lx + 9, ly + 22], fill=SKIN_BASE, outline=OUTLINE)
    d.point((lx + 5, ly + 18), fill=SKIN_SHD) # knee
    d.rectangle([lx + 2, ly + 22, lx + 9, ly + 29], fill=SKIN_BASE, outline=OUTLINE)
    # Boot
    d.polygon([(lx, ly+29), (lx+10, ly+29), (lx+11, ly+36), (lx-1, ly+36)], fill=BOOT_MID, outline=OUTLINE)
    d.rectangle([lx - 1, ly + 35, lx + 11, ly + 37], fill=BOOT_DK)

    # Right Leg (Character's right / front)
    rx = ox + 21 + leg_r_state * 4
    ry = oy + 8
    d.rectangle([rx, ry, rx + 11, ry + 11], fill=DENIM_MID, outline=DENIM_OUT)
    d.rectangle([rx + 2, ry + 2, rx + 9, ry + 9], fill=DENIM_HL)
    d.point((rx + 2, ry + 12), fill=DENIM_FRY)
    d.point((rx + 6, ry + 13), fill=DENIM_FRY)
    d.point((rx + 9, ry + 12), fill=DENIM_FRY)
    # Bare leg
    d.rectangle([rx + 2, ry + 12, rx + 9, ry + 22], fill=SKIN_BASE, outline=OUTLINE)
    d.point((rx + 5, ry + 18), fill=SKIN_SHD) # knee
    # Bandage wrap on right shin
    d.rectangle([rx + 2, ry + 22, rx + 9, ly + 29], fill=BND_WHT, outline=OUTLINE)
    d.line([(rx+2, ry+24), (rx+9, ry+24)], fill=BND_SHD)
    d.line([(rx+2, ry+27), (rx+9, ry+27)], fill=BND_MID)
    # Boot
    d.polygon([(rx, ry+29), (rx+10, ry+29), (rx+11, ry+36), (rx-1, ry+36)], fill=BOOT_MID, outline=OUTLINE)
    d.rectangle([rx - 1, ry + 35, rx + 11, ry + 37], fill=BOOT_DK)

def draw_arm_l(d, sx, sy, state=0):
    # sx, sy: shoulder joint
    d.rectangle([sx - 3, sy - 2, sx + 3, sy + 3], fill=SHIRT_MID, outline=SHIRT_OUT) # sleeve
    if state == 0: # down
        d.rectangle([sx - 2, sy + 3, sx + 4, sy + 11], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx - 3, sy + 11, sx + 3, sy + 18], fill=SKIN_BASE, outline=OUTLINE)
        # Bandage wrist
        d.rectangle([sx - 4, sy + 18, sx + 2, sy + 23], fill=BND_WHT, outline=OUTLINE)
        # Fist
        d.rectangle([sx - 5, sy + 23, sx + 1, sy + 28], fill=SKIN_SHD, outline=OUTLINE)
    elif state == 1: # back swing
        d.polygon([(sx, sy), (sx-8, sy+8), (sx-5, sy+14)], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx - 10, sy + 14, sx - 4, sy + 20], fill=BND_WHT, outline=OUTLINE)
        d.rectangle([sx - 12, sy + 20, sx - 6, sy + 25], fill=SKIN_SHD, outline=OUTLINE)
    elif state == 2: # forward guard
        d.polygon([(sx, sy), (sx+6, sy+8), (sx+4, sy+14)], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx + 2, sy + 14, sx + 8, sy + 19], fill=BND_WHT, outline=OUTLINE)
        d.rectangle([sx + 3, sy + 19, sx + 9, sy + 24], fill=SKIN_SHD, outline=OUTLINE)

def draw_arm_r_and_katana(d, sx, sy, pose='ready'):
    # sx, sy: shoulder joint (around x=68, y=48)
    d.rectangle([sx - 3, sy - 2, sx + 3, sy + 3], fill=SHIRT_MID, outline=SHIRT_OUT) # sleeve
    
    if pose == 'ready': # Holding blade angled forward
        d.rectangle([sx - 1, sy + 2, sx + 5, sy + 10], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx + 1, sy + 10, sx + 7, sy + 17], fill=SKIN_BASE, outline=OUTLINE)
        # Hand
        d.rectangle([sx + 3, sy + 16, sx + 8, sy + 21], fill=SKIN_SHD, outline=OUTLINE)
        # Hilt & Guard
        d.line([(sx + 5, sy + 12), (sx + 7, sy + 25)], fill=HILT_WD, width=2)
        d.rectangle([sx + 2, sy + 19, sx + 10, sy + 21], fill=GOLD_ACC, outline=OUTLINE)
        # Blade extending up-right
        for i in range(26):
            bx = sx + 8 + i
            by = sy + 19 - int(i * 0.7)
            d.point((bx, by - 1), fill=BLD_DK)
            d.point((bx, by), fill=BLD_MID)
            d.point((bx, by + 1), fill=BLD_LGT)
        d.point((sx + 34, sy), fill=BLD_GLOW)

    elif pose == 'windup': # Drawn way back over shoulder
        d.polygon([(sx, sy), (sx-4, sy-8), (sx-2, sy-14)], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx - 4, sy - 16, sx + 2, sy - 10], fill=SKIN_SHD, outline=OUTLINE) # Hand
        # Hilt pointing down-back
        d.line([(sx - 2, sy - 18), (sx, sy - 6)], fill=HILT_WD, width=2)
        d.rectangle([sx - 5, sy - 12, sx + 3, sy - 10], fill=GOLD_ACC, outline=OUTLINE)
        # Blade trailing back
        for i in range(28):
            bx = sx - 4 - i
            by = sy - 12 - int(i * 0.4)
            d.point((bx, by - 1), fill=BLD_DK)
            d.point((bx, by), fill=BLD_MID)
            d.point((bx, by + 1), fill=BLD_LGT)

    elif pose == 'slash': # Sweeping forward in full strike!
        d.polygon([(sx, sy), (sx+10, sy+4), (sx+18, sy+2)], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx + 16, sy, sx + 22, sy + 5], fill=SKIN_SHD, outline=OUTLINE) # Hand
        d.rectangle([sx + 21, sy - 2, sx + 23, sy + 6], fill=GOLD_ACC, outline=OUTLINE)
        # Flat horizontal slash blade
        for i in range(32):
            bx = sx + 23 + i
            by = sy + 2 + int(i * 0.15)
            d.point((bx, by - 1), fill=BLD_DK)
            d.point((bx, by), fill=BLD_MID)
            d.point((bx, by + 1), fill=BLD_GLOW)
        # Giant Crescent Slash Arc
        for deg in range(15, 145, 2):
            rad = math.radians(deg)
            r = 34
            cx = sx + 28 + int(r * math.cos(rad))
            cy = sy + 4 - int(r * math.sin(rad))
            d.line([(cx-1, cy), (cx+2, cy+2)], fill=SLASH_BLU, width=2)
            d.point((cx, cy), fill=SLASH_WHT)

    elif pose == 'upper_slash': # DNF Upper Slash leap!
        d.polygon([(sx, sy), (sx+4, sy-10), (sx+8, sy-16)], fill=SKIN_BASE, outline=OUTLINE)
        d.rectangle([sx + 6, sy - 18, sx + 12, sy - 13], fill=SKIN_SHD, outline=OUTLINE) # Hand
        d.rectangle([sx + 7, sy - 14, sx + 13, sy - 12], fill=GOLD_ACC, outline=OUTLINE)
        # Blade pointing straight to the sky!
        for i in range(32):
            bx = sx + 10 + int(i * 0.1)
            by = sy - 15 - i
            d.point((bx - 1, by), fill=BLD_DK)
            d.point((bx, by), fill=BLD_MID)
            d.point((bx + 1, by), fill=BLD_GLOW)
        # Vertical Geyser Slash Arc
        for deg in range(60, 180, 2):
            rad = math.radians(deg)
            r = 38
            cx = sx + 8 + int(r * math.cos(rad))
            cy = sy - 10 - int(r * math.sin(rad))
            d.line([(cx, cy-1), (cx+2, cy+2)], fill=SLASH_BLU, width=2)
            d.point((cx, cy), fill=SLASH_WHT)

# =============================================================
# Generate 4-Action Animation Sets
# =============================================================
def generate_all_animations(female=True):
    prefix = "female" if female else "male"
    
    # 1. IDLE (4 frames)
    for i in range(4):
        im = create_frame()
        d = ImageDraw.Draw(im)
        bob = -2 if i in [1, 2] else 0
        
        # Draw layers in natural depth:
        draw_arm_l(d, 46, 46 + bob, state=0)
        draw_shorts_and_legs(d, 56, 72, leg_l_state=0, leg_r_state=0)
        draw_torso_ragged(d, 56, 52 + bob)
        draw_head(d, 56, 28 + bob, female=female)
        draw_arm_r_and_katana(d, 66, 48 + bob, pose='ready')
        
        im.save(os.path.join(out_dir, f"{prefix}_idle_{i}.png"))

    # 2. RUN (6 frames)
    leg_cycles = [
        (-2, 2, 1, 'ready'),   # Frame 0: Left back, Right forward
        (-1, 1, 0, 'ready'),   # Frame 1: Plant
        (0, 0, 2, 'ready'),    # Frame 2: Passing
        (2, -2, 1, 'ready'),   # Frame 3: Left forward, Right back
        (1, -1, 0, 'ready'),   # Frame 4: Plant
        (0, 0, 2, 'ready')     # Frame 5: Passing
    ]
    for i, (ll, lr, arm_st, k_pose) in enumerate(leg_cycles):
        im = create_frame()
        d = ImageDraw.Draw(im)
        bob = -2 if i in [0, 3] else 0
        
        draw_arm_l(d, 46, 46 + bob, state=arm_st)
        draw_shorts_and_legs(d, 56, 72, leg_l_state=ll, leg_r_state=lr)
        draw_torso_ragged(d, 56, 52 + bob, tilt=4)
        draw_head(d, 58, 28 + bob, female=female)
        draw_arm_r_and_katana(d, 66, 48 + bob, pose=k_pose)
        
        im.save(os.path.join(out_dir, f"{prefix}_run_{i}.png"))

    # 3. ATTACK (4 frames: Windup -> Slash Impact -> Extension -> Recovery)
    attack_configs = [
        ('windup', -2, 2, 1, 0),       # 0: Windup back
        ('slash', 0, 4, 1, 8),         # 1: Slash Impact!
        ('ready', 0, 3, 2, 6),         # 2: Extension
        ('ready', 0, 1, 0, 0)          # 3: Recovery
    ]
    for i, (k_pose, ll, lr, arm_st, lunge_x) in enumerate(attack_configs):
        im = create_frame()
        d = ImageDraw.Draw(im)
        
        draw_arm_l(d, 46 + lunge_x, 46, state=arm_st)
        draw_shorts_and_legs(d, 56 + lunge_x, 72, leg_l_state=ll, leg_r_state=lr)
        draw_torso_ragged(d, 56 + lunge_x, 52)
        draw_head(d, 56 + lunge_x, 28, female=female)
        draw_arm_r_and_katana(d, 66 + lunge_x, 48, pose=k_pose)
        
        im.save(os.path.join(out_dir, f"{prefix}_attack_{i}.png"))

    # 4. SKILL (4 frames: Crouch -> Upper Slash Leap -> Apex -> Landing Slam)
    skill_configs = [
        ('windup', 0, 1, 1, 0, 4),          # 0: Low Crouch
        ('upper_slash', -1, 1, 2, 4, -14),  # 1: Exploding Upper Slash Leap!
        ('ready', 0, 0, 1, 6, -18),         # 2: Aerial Apex
        ('slash', 1, 2, 1, 4, 4)            # 3: Landing Ground Slam!
    ]
    for i, (k_pose, ll, lr, arm_st, lx, ly) in enumerate(skill_configs):
        im = create_frame()
        d = ImageDraw.Draw(im)
        
        draw_arm_l(d, 46 + lx, 46 + ly, state=arm_st)
        draw_shorts_and_legs(d, 56 + lx, 72 + (ly if ly > 0 else ly//2), leg_l_state=ll, leg_r_state=lr)
        draw_torso_ragged(d, 56 + lx, 52 + ly)
        draw_head(d, 56 + lx, 28 + ly, female=female)
        draw_arm_r_and_katana(d, 66 + lx, 48 + ly, pose=k_pose)
        
        im.save(os.path.join(out_dir, f"{prefix}_skill_{i}.png"))

if __name__ == "__main__":
    generate_all_animations(female=True)
    generate_all_animations(female=False)
    print("All DNF-Style frame-by-frame action sprites rendered successfully!")
