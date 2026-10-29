import os
from PIL import Image, ImageDraw

out_dir = r"C:\Users\exbxda13\project2100\assets\pixel_parts"
os.makedirs(out_dir, exist_ok=True)

def create_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ============================================================
# DNF (Dungeon & Fighter) Master 16-Bit Arcade Palette
# ============================================================
# Skin
SKIN_HL   = (255, 235, 215, 255)
SKIN_BASE = (248, 202, 164, 255)
SKIN_SHD  = (212, 150, 110, 255)
SKIN_DEEP = (160,  95,  65, 255)

# Eyes
EYE_WHT   = (255, 255, 255, 255)
EYE_PUPIL = ( 30,  70, 140, 255) # Intense DNF Blue
EYE_DARK  = ( 15,  25,  50, 255)

# Hair Female (Blonde DNF Slayer/Fighter style)
HAIR_F_HL  = (255, 245, 160, 255)
HAIR_F_MID = (235, 195,  80, 255)
HAIR_F_SHD = (175, 130,  40, 255)
HAIR_F_DK  = ( 95,  65,  15, 255)

# Hair Male (Dark DNF Slayer style)
HAIR_M_HL  = ( 85,  80, 100, 255)
HAIR_M_MID = ( 48,  44,  60, 255)
HAIR_M_SHD = ( 28,  24,  38, 255)
HAIR_M_DK  = ( 14,  12,  20, 255)

# Ragged Short-Sleeve Shirt (누더기 반팔 티셔츠)
SHIRT_HL   = (242, 238, 228, 255)
SHIRT_MID  = (204, 198, 184, 255)
SHIRT_SHD  = (148, 140, 126, 255)
SHIRT_FRY  = (108, 100,  88, 255) # 올 풀린 실밥
SHIRT_OUT  = ( 55,  50,  42, 255)

# Ragged Denim Shorts (누더기 청 반바지)
DENIM_HL   = ( 85, 120, 160, 255)
DENIM_MID  = ( 52,  80, 115, 255)
DENIM_SHD  = ( 34,  55,  82, 255)
DENIM_FRY  = (125, 150, 185, 255) # 찢어진 데님 실밥
DENIM_OUT  = ( 18,  30,  48, 255)

# Bandages
BND_WHT = (245, 245, 245, 255)
BND_MID = (205, 205, 210, 255)
BND_SHD = (145, 145, 155, 255)

# Weapon (Starter Katana / Zanbato)
BLD_GLOW = (255, 255, 255, 255)
BLD_LGT  = (215, 230, 245, 255)
BLD_MID  = (150, 165, 185, 255)
BLD_DK   = ( 75,  85, 100, 255)
HILT_WD  = ( 60,  35,  20, 255)
GOLD_ACC = (240, 195,  40, 255)

# Universal DNF Pixel Outline
OUTLINE = (25, 20, 28, 255)

# ============================================================
# 1. HEAD FEMALE (44x40) - DNF Anime Pixel Head & Face
# ============================================================
def generate_head_female():
    im = create_canvas(44, 40)
    d = ImageDraw.Draw(im)

    # Ponytail extending back-left
    d.rectangle([2, 10, 10, 24], fill=HAIR_F_SHD, outline=OUTLINE)
    d.rectangle([4, 12, 11, 26], fill=HAIR_F_MID)
    d.rectangle([5, 14, 9, 20], fill=HAIR_F_HL)
    d.rectangle([1, 20, 7, 30], fill=HAIR_F_DK)
    # Red Cloth Ribbon / Headband knot
    d.rectangle([9, 12, 13, 16], fill=(220, 50, 50, 255), outline=OUTLINE)
    d.point((11, 14), fill=(255, 140, 140, 255))

    # Face Skin Base (Tapered anime chin)
    d.rectangle([14, 12, 32, 28], fill=SKIN_BASE)
    d.rectangle([16, 14, 30, 26], fill=SKIN_HL)
    # Jaw / Chin taper
    d.polygon([(16, 28), (30, 28), (26, 34), (20, 34)], fill=SKIN_SHD, outline=OUTLINE)
    d.rectangle([21, 33, 25, 34], fill=SKIN_BASE)

    # Eyes (Iconic DNF Anime Eye Shading)
    # Left eye
    d.rectangle([17, 19, 22, 25], fill=OUTLINE)
    d.rectangle([18, 20, 22, 24], fill=EYE_PUPIL)
    d.point((18, 20), fill=EYE_WHT) # Specular shine
    d.point((19, 21), fill=(100, 180, 255, 255)) # Iris light
    d.rectangle([17, 18, 23, 19], fill=OUTLINE) # Eyelash line
    # Right eye
    d.rectangle([25, 19, 30, 25], fill=OUTLINE)
    d.rectangle([25, 20, 29, 24], fill=EYE_PUPIL)
    d.point((26, 20), fill=EYE_WHT)
    d.point((27, 21), fill=(100, 180, 255, 255))
    d.rectangle([24, 18, 30, 19], fill=OUTLINE)

    # Eyebrows
    d.line([(17, 16), (22, 17)], fill=HAIR_F_DK, width=1)
    d.line([(25, 17), (30, 16)], fill=HAIR_F_DK, width=1)

    # Nose & Mouth
    d.point((23, 26), fill=SKIN_DEEP)
    d.line([(22, 29), (24, 29)], fill=SKIN_DEEP)

    # Hair Bangs & Front Strands (Framing Face)
    d.rectangle([13, 4, 33, 13], fill=HAIR_F_MID, outline=OUTLINE)
    d.rectangle([16, 3, 30, 8], fill=HAIR_F_HL)
    # Left bang tuft
    d.polygon([(13, 12), (16, 24), (12, 18)], fill=HAIR_F_MID, outline=OUTLINE)
    d.point((14, 18), fill=HAIR_F_SHD)
    # Center bang spikes
    d.polygon([(20, 11), (22, 17), (25, 11)], fill=HAIR_F_HL, outline=OUTLINE)
    d.point((22, 16), fill=HAIR_F_MID)
    # Right bang tuft
    d.polygon([(30, 12), (34, 18), (31, 24)], fill=HAIR_F_MID, outline=OUTLINE)
    d.point((32, 18), fill=HAIR_F_SHD)

    # Red Survivor Headband across forehead
    d.rectangle([14, 9, 32, 11], fill=(210, 45, 45, 255))
    d.line([(14, 9), (32, 9)], fill=(255, 110, 110, 255))

    im.save(os.path.join(out_dir, "head_female.png"))

# ============================================================
# 2. HEAD MALE (44x40) - DNF Slayer Style Spiky Hair Head
# ============================================================
def generate_head_male():
    im = create_canvas(44, 40)
    d = ImageDraw.Draw(im)

    # Face Skin
    d.rectangle([14, 12, 32, 28], fill=SKIN_BASE)
    d.rectangle([16, 14, 30, 26], fill=SKIN_HL)
    d.polygon([(16, 28), (30, 28), (26, 34), (20, 34)], fill=SKIN_SHD, outline=OUTLINE)

    # Sharp Anime Eyes
    d.rectangle([17, 20, 22, 24], fill=OUTLINE)
    d.rectangle([18, 20, 21, 23], fill=(40, 50, 70, 255))
    d.point((18, 20), fill=EYE_WHT)
    d.rectangle([25, 20, 30, 24], fill=OUTLINE)
    d.rectangle([26, 20, 29, 23], fill=(40, 50, 70, 255))
    d.point((26, 20), fill=EYE_WHT)

    # Fierce brows
    d.line([(16, 17), (22, 19)], fill=OUTLINE, width=1)
    d.line([(25, 19), (31, 17)], fill=OUTLINE, width=1)

    # Cheek Bandage
    d.rectangle([26, 25, 30, 27], fill=BND_WHT, outline=OUTLINE)
    d.point((28, 26), fill=(200, 120, 120, 255))

    # Mouth / Chin
    d.point((23, 26), fill=SKIN_DEEP)
    d.line([(21, 29), (25, 29)], fill=OUTLINE)

    # Spiky DNF Slayer Dark Hair
    d.rectangle([12, 3, 34, 14], fill=HAIR_M_MID, outline=OUTLINE)
    d.rectangle([15, 2, 31, 8], fill=HAIR_M_HL)
    # Wild spikes around edges
    d.polygon([(10, 6), (7, 14), (12, 18)], fill=HAIR_M_MID, outline=OUTLINE)
    d.polygon([(32, 6), (37, 14), (34, 18)], fill=HAIR_M_MID, outline=OUTLINE)
    d.polygon([(18, 12), (21, 18), (24, 12)], fill=HAIR_M_MID, outline=OUTLINE)
    d.polygon([(25, 12), (28, 17), (30, 12)], fill=HAIR_M_MID, outline=OUTLINE)

    im.save(os.path.join(out_dir, "head_male.png"))

# ============================================================
# 3. TORSO (36x42) - DNF Ragged Short-Sleeve (누더기 반팔)
# ============================================================
def generate_torso(female=True):
    im = create_canvas(36, 42)
    d = ImageDraw.Draw(im)

    # Exposed Neck / Collarbone
    d.rectangle([14, 2, 22, 9], fill=SKIN_BASE)
    d.rectangle([16, 4, 20, 8], fill=SKIN_HL)
    d.point((18, 9), fill=SKIN_SHD)

    # Main T-Shirt Body
    d.rectangle([8, 8, 28, 32], fill=SHIRT_MID, outline=SHIRT_OUT)
    d.rectangle([10, 10, 26, 28], fill=SHIRT_HL)

    # Open V-neck collar showing skin
    d.polygon([(14, 8), (22, 8), (18, 13)], fill=SKIN_BASE, outline=SHIRT_OUT)

    # Natural Cloth Folds / Shading lines (DNF Pixel wrinkles)
    d.line([(10, 18), (14, 21)], fill=SHIRT_SHD)
    d.line([(26, 18), (22, 21)], fill=SHIRT_SHD)
    d.line([(12, 25), (18, 27)], fill=SHIRT_SHD)

    # Ragged Torn Hem (밑단 뜯어짐 디테일 & 실밥)
    d.rectangle([8, 30, 28, 34], fill=SHIRT_SHD)
    # Jagged frayed edges
    for x in range(8, 29):
        if x % 3 == 0:
            d.point((x, 34), fill=SHIRT_FRY)
            d.point((x, 35), fill=SHIRT_OUT)
        elif x % 3 == 1:
            d.point((x, 33), fill=SHIRT_MID)

    # Survivor Waist Belt / Cord
    d.rectangle([8, 27, 28, 29], fill=(70, 45, 30, 255), outline=OUTLINE)
    d.rectangle([16, 27, 20, 29], fill=GOLD_ACC) # Belt buckle

    # Short Sleeves (Shoulder caps)
    d.polygon([(8, 8), (3, 14), (8, 17)], fill=SHIRT_MID, outline=SHIRT_OUT)
    d.polygon([(28, 8), (33, 14), (28, 17)], fill=SHIRT_MID, outline=SHIRT_OUT)

    fn = "torso_female.png" if female else "torso_male.png"
    im.save(os.path.join(out_dir, fn))

# ============================================================
# 4. RIGHT ARM + DNF KATANA (52x48)
# Pivot at shoulder: (10, 14)
# Bare skin arm wielding a gleaming DNF blade!
# ============================================================
def generate_arm_r_katana():
    im = create_canvas(52, 48)
    d = ImageDraw.Draw(im)

    # Ragged sleeve hem at shoulder
    d.rectangle([7, 8, 13, 13], fill=SHIRT_MID, outline=SHIRT_OUT)

    # Bare Skin Bicep
    d.rectangle([8, 13, 14, 21], fill=SKIN_BASE, outline=OUTLINE)
    d.rectangle([9, 14, 12, 19], fill=SKIN_HL)

    # Bare Forearm
    d.rectangle([9, 21, 15, 29], fill=SKIN_BASE, outline=OUTLINE)
    d.rectangle([10, 22, 13, 27], fill=SKIN_HL)

    # Hand gripping weapon hilt
    d.rectangle([11, 28, 16, 33], fill=SKIN_SHD, outline=OUTLINE)

    # DNF Katana (환도 / 낡은 생존용 검)
    # Hilt (손잡이)
    d.line([(13, 23), (15, 37)], fill=HILT_WD, width=2)
    d.rectangle([10, 31, 18, 33], fill=GOLD_ACC, outline=OUTLINE) # Tsuba/Guard

    # Blade (도신 - 대각선으로 쭉 뻗은 날렵한 은빛 도신)
    for i in range(28):
        bx = 18 + i
        by = 31 - int(i * 0.72)
        if 0 <= bx < 52 and 0 <= by < 48:
            d.point((bx, by - 1), fill=BLD_DK)   # 검등 (어두운 강철)
            d.point((bx, by),     fill=BLD_MID)  # 칼날 중심
            d.point((bx, by + 1), fill=BLD_LGT)  # 날카로운 은빛 칼날
            d.point((bx, by + 2), fill=OUTLINE)  # 하단 외곽선

    # Sharp Blade Tip & Gleam
    d.point((45, 11), fill=BLD_GLOW)
    d.point((46, 11), fill=BLD_GLOW)
    d.point((44, 12), fill=BLD_LGT)

    im.save(os.path.join(out_dir, "arm_r_katana.png"))

# ============================================================
# 5. LEFT ARM (28x38)
# Pivot at shoulder: (20, 8)
# Bare skin arm + White cloth bandage wrapped around wrist
# ============================================================
def generate_arm_l():
    im = create_canvas(28, 38)
    d = ImageDraw.Draw(im)

    # Ragged sleeve rim
    d.rectangle([16, 6, 22, 11], fill=SHIRT_MID, outline=SHIRT_OUT)

    # Bare Upper Arm
    d.rectangle([15, 11, 21, 19], fill=SKIN_BASE, outline=OUTLINE)
    d.rectangle([16, 12, 19, 17], fill=SKIN_HL)

    # Forearm
    d.rectangle([13, 19, 19, 25], fill=SKIN_BASE, outline=OUTLINE)

    # White Cloth Bandage wrap on wrist (DNF Fighter wrist wrap)
    d.rectangle([11, 24, 17, 30], fill=BND_WHT, outline=OUTLINE)
    d.line([(11, 26), (17, 26)], fill=BND_SHD)
    d.line([(11, 28), (17, 28)], fill=BND_MID)

    # Clenched Fist
    d.rectangle([9, 29, 15, 35], fill=SKIN_SHD, outline=OUTLINE)
    d.rectangle([10, 30, 13, 33], fill=SKIN_HL)

    im.save(os.path.join(out_dir, "arm_l.png"))

# ============================================================
# 6. LEGS (40x46) - DNF Ragged Shorts & Bare Legs (누더기 반바지)
# Pivot at hips: (20, 6)
# ============================================================
def generate_legs():
    im = create_canvas(40, 46)
    d = ImageDraw.Draw(im)

    # Hips / Pelvis Base
    d.rectangle([10, 2, 30, 8], fill=DENIM_SHD, outline=DENIM_OUT)

    # Left Short Leg (Frayed Denim)
    d.rectangle([8, 8, 19, 19], fill=DENIM_MID, outline=DENIM_OUT)
    d.rectangle([10, 10, 17, 17], fill=DENIM_HL)
    # Frayed threads hanging down
    d.point((9, 20), fill=DENIM_FRY)
    d.point((12, 21), fill=DENIM_FRY)
    d.point((15, 20), fill=DENIM_FRY)
    d.point((18, 21), fill=DENIM_FRY)

    # Right Short Leg (Frayed Denim)
    d.rectangle([21, 8, 32, 19], fill=DENIM_MID, outline=DENIM_OUT)
    d.rectangle([23, 10, 30, 17], fill=DENIM_HL)
    d.point((22, 20), fill=DENIM_FRY)
    d.point((25, 21), fill=DENIM_FRY)
    d.point((28, 20), fill=DENIM_FRY)
    d.point((31, 21), fill=DENIM_FRY)

    # Bare Skin Legs (Thigh to Knee)
    d.rectangle([10, 20, 17, 29], fill=SKIN_BASE, outline=OUTLINE)
    d.rectangle([11, 21, 15, 27], fill=SKIN_HL)
    d.rectangle([23, 20, 30, 29], fill=SKIN_BASE, outline=OUTLINE)
    d.rectangle([24, 21, 28, 27], fill=SKIN_HL)
    # Kneecap shadows
    d.point((13, 27), fill=SKIN_SHD)
    d.point((26, 27), fill=SKIN_SHD)

    # Right Leg Bandage wrap on Shin
    d.rectangle([23, 29, 30, 36], fill=BND_WHT, outline=OUTLINE)
    d.line([(23, 31), (30, 31)], fill=BND_SHD)
    d.line([(23, 34), (30, 34)], fill=BND_MID)

    # Left Bare Shin
    d.rectangle([10, 29, 17, 36], fill=SKIN_BASE, outline=OUTLINE)

    # Survivor Combat Boots
    d.polygon([(8, 36), (18, 36), (19, 43), (7, 43)], fill=(65, 45, 30, 255), outline=OUTLINE)
    d.rectangle([7, 42, 19, 44], fill=(35, 22, 15, 255)) # Sole
    d.polygon([(21, 35), (31, 35), (32, 43), (20, 43)], fill=(65, 45, 30, 255), outline=OUTLINE)
    d.rectangle([20, 42, 32, 44], fill=(35, 22, 15, 255))

    im.save(os.path.join(out_dir, "legs.png"))

# ============================================================
# 7. DNF CRESCENT SLASH VFX (64x64)
# ============================================================
def generate_slash_vfx():
    im = create_canvas(64, 64)
    d = ImageDraw.Draw(im)
    import math
    # Dynamic crescent slash arc
    for deg in range(25, 145):
        rad = math.radians(deg)
        r = 27
        cx = 26 + int(r * math.cos(rad))
        cy = 32 - int(r * math.sin(rad))
        d.line([(cx-1, cy), (cx+2, cy+2)], fill=(120, 220, 255, 255), width=2)
        d.point((cx, cy), fill=(255, 255, 255, 255))
    im.save(os.path.join(out_dir, "vfx_slash.png"))

if __name__ == "__main__":
    generate_head_female()
    generate_head_male()
    generate_torso(female=True)
    generate_torso(female=False)
    generate_arm_r_katana()
    generate_arm_l()
    generate_legs()
    generate_slash_vfx()
    print("DNF-Style Pixel Parts built successfully!")
