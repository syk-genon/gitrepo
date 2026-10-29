import os
from PIL import Image, ImageDraw

out_dir = r"C:\Users\exbxda13\project2100\assets\pixel_parts"
os.makedirs(out_dir, exist_ok=True)

def create_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# Colors Palette
SKIN_LIGHT = (255, 228, 205, 255)
SKIN_MID   = (250, 208, 175, 255)
SKIN_SHADE = (225, 175, 140, 255)
SKIN_BLUSH = (255, 180, 170, 255)

EYE_WHITE  = (255, 255, 255, 255)
EYE_BLUE   = (40, 130, 220, 255)
EYE_DARK   = (20, 40, 70, 255)
EYE_SHINE  = (255, 255, 255, 255)

HAIR_GOLD_LIGHT = (255, 240, 150, 255)
HAIR_GOLD_MID   = (240, 210, 100, 255)
HAIR_GOLD_SHADE = (200, 160, 60, 255)
HAIR_GOLD_DARK  = (150, 110, 40, 255)

HAIR_MALE_LIGHT = (70, 65, 80, 255)
HAIR_MALE_MID   = (45, 40, 55, 255)
HAIR_MALE_DARK  = (25, 20, 35, 255)

SHIRT_WHITE_LIGHT = (235, 230, 220, 255) # 누더기 아이보리 반팔
SHIRT_WHITE_MID   = (205, 198, 185, 255)
SHIRT_WHITE_SHADE = (165, 155, 140, 255)
SHIRT_TEAR        = (130, 120, 110, 255)

SHIRT_MALE_LIGHT = (90, 100, 95, 255) # 누더기 카키 반팔
SHIRT_MALE_MID   = (70, 80, 75, 255)
SHIRT_MALE_SHADE = (50, 60, 55, 255)

SHORTS_DENIM_LIGHT = (75, 105, 140, 255)
SHORTS_DENIM_MID   = (55, 80, 115, 255)
SHORTS_DENIM_SHADE = (40, 60, 90, 255)
SHORTS_DENIM_TEAR  = (140, 160, 190, 255) # 찢어진 실밥

BANDAGE_LIGHT = (230, 230, 225, 255)
BANDAGE_SHADE = (180, 180, 175, 255)

LEATHER_LIGHT = (130, 85, 55, 255)
LEATHER_MID   = (95, 60, 35, 255)
LEATHER_DARK  = (65, 38, 20, 255)

OUTLINE = (35, 25, 30, 255)

# ==========================================
# 1. FEMALE HEAD (44x40) - Cute Anime Survivor
# ==========================================
def generate_head_female():
    im = create_canvas(44, 40)
    d = ImageDraw.Draw(im)

    # Ponytail (Left/Behind)
    d.rectangle([4, 12, 10, 26], fill=HAIR_GOLD_SHADE)
    d.rectangle([6, 14, 12, 28], fill=HAIR_GOLD_MID)
    d.rectangle([2, 20, 8, 30], fill=HAIR_GOLD_DARK)
    # Hair Ribbon / Survivor Cloth Tie
    d.rectangle([9, 12, 13, 16], fill=(220, 70, 70, 255))
    d.point((11, 14), fill=(255, 150, 150, 255))

    # Face Base (Peach skin)
    d.rectangle([14, 12, 32, 32], fill=SKIN_MID)
    d.rectangle([16, 14, 30, 30], fill=SKIN_LIGHT)
    # Chin taper
    d.rectangle([18, 32, 28, 34], fill=SKIN_SHADE)
    d.rectangle([20, 34, 26, 35], fill=SKIN_MID)

    # Eyes (Big Anime Eyes)
    # Left eye
    d.rectangle([17, 20, 21, 26], fill=EYE_DARK)
    d.rectangle([18, 21, 21, 25], fill=EYE_BLUE)
    d.point((18, 21), fill=EYE_SHINE)
    d.point((19, 21), fill=EYE_WHITE)
    d.rectangle([16, 19, 22, 19], fill=OUTLINE) # Eyelash
    # Right eye
    d.rectangle([25, 20, 29, 26], fill=EYE_DARK)
    d.rectangle([25, 21, 28, 25], fill=EYE_BLUE)
    d.point((26, 21), fill=EYE_SHINE)
    d.point((27, 21), fill=EYE_WHITE)
    d.rectangle([24, 19, 30, 19], fill=OUTLINE) # Eyelash

    # Blush
    d.point((16, 26), fill=SKIN_BLUSH)
    d.point((29, 26), fill=SKIN_BLUSH)

    # Cute Mouth / Nose
    d.point((23, 27), fill=SKIN_SHADE) # nose
    d.rectangle([22, 30, 24, 30], fill=(200, 100, 110, 255)) # mouth

    # Bangs & Hair front
    d.rectangle([13, 4, 33, 15], fill=HAIR_GOLD_MID)
    d.rectangle([15, 2, 31, 8], fill=HAIR_GOLD_LIGHT) # top shine
    # Left bang strands
    d.rectangle([12, 12, 16, 24], fill=HAIR_GOLD_MID)
    d.rectangle([13, 14, 15, 26], fill=HAIR_GOLD_SHADE)
    # Center bangs
    d.rectangle([21, 10, 25, 17], fill=HAIR_GOLD_LIGHT)
    d.point((22, 18), fill=HAIR_GOLD_MID)
    d.point((24, 17), fill=HAIR_GOLD_MID)
    # Right bang strands
    d.rectangle([30, 12, 34, 24], fill=HAIR_GOLD_MID)
    d.rectangle([31, 14, 33, 26], fill=HAIR_GOLD_SHADE)

    # Survivor Headband / Bandage
    d.rectangle([14, 8, 32, 10], fill=BANDAGE_LIGHT)
    d.point((23, 9), fill=BANDAGE_SHADE)

    im.save(os.path.join(out_dir, "head_female.png"))

# ==========================================
# 2. MALE HEAD (44x40) - Handsome Anime Survivor
# ==========================================
def generate_head_male():
    im = create_canvas(44, 40)
    d = ImageDraw.Draw(im)

    # Face Base
    d.rectangle([14, 12, 32, 32], fill=SKIN_MID)
    d.rectangle([16, 14, 30, 30], fill=SKIN_LIGHT)
    d.rectangle([18, 32, 28, 35], fill=SKIN_MID)

    # Eyes (Sharp Anime Eyes)
    d.rectangle([17, 21, 21, 25], fill=EYE_DARK)
    d.point((18, 22), fill=EYE_SHINE)
    d.rectangle([16, 20, 22, 20], fill=OUTLINE) # Brow/lash
    d.rectangle([25, 21, 29, 25], fill=EYE_DARK)
    d.point((26, 22), fill=EYE_SHINE)
    d.rectangle([24, 20, 30, 20], fill=OUTLINE)

    # Cheek Bandage
    d.rectangle([27, 26, 31, 28], fill=BANDAGE_LIGHT)
    d.point((29, 27), fill=(200, 120, 120, 255))

    # Mouth / Nose
    d.point((23, 27), fill=SKIN_SHADE)
    d.rectangle([21, 30, 25, 30], fill=OUTLINE)

    # Messy Dark Hair
    d.rectangle([12, 4, 34, 14], fill=HAIR_MALE_MID)
    d.rectangle([14, 2, 32, 8], fill=HAIR_MALE_LIGHT) # top
    # Spiky tufts
    d.rectangle([10, 8, 14, 22], fill=HAIR_MALE_MID)
    d.point((9, 12), fill=HAIR_MALE_DARK)
    d.point((10, 16), fill=HAIR_MALE_DARK)
    d.rectangle([32, 8, 36, 22], fill=HAIR_MALE_MID)
    d.point((37, 12), fill=HAIR_MALE_DARK)
    # Forehead bangs
    d.rectangle([18, 12, 21, 18], fill=HAIR_MALE_MID)
    d.rectangle([24, 12, 27, 17], fill=HAIR_MALE_MID)

    im.save(os.path.join(out_dir, "head_male.png"))

# ==========================================
# 3. FEMALE TORSO (36x42) - Ragged Short-Sleeve
# ==========================================
def generate_torso_female():
    im = create_canvas(36, 42)
    d = ImageDraw.Draw(im)

    # Neck
    d.rectangle([14, 2, 22, 8], fill=SKIN_MID)
    d.rectangle([16, 4, 20, 8], fill=SKIN_LIGHT)

    # Ragged Short-Sleeve Shirt (Ivory / Off-White)
    d.rectangle([8, 8, 28, 32], fill=SHIRT_WHITE_MID)
    d.rectangle([10, 10, 26, 28], fill=SHIRT_WHITE_LIGHT)
    # V-Neck / Open collar showing collarbone
    d.rectangle([15, 8, 21, 12], fill=SKIN_LIGHT)
    d.point((18, 13), fill=SKIN_SHADE) # collarbone shadow

    # Frayed / ragged bottom hem with tears
    d.rectangle([8, 29, 28, 33], fill=SHIRT_WHITE_SHADE)
    # Torn zig-zag hem
    d.point((9, 34), fill=SHIRT_TEAR)
    d.point((12, 34), fill=SHIRT_TEAR)
    d.point((15, 35), fill=SHIRT_TEAR)
    d.point((18, 33), fill=SHIRT_WHITE_LIGHT)
    d.point((22, 35), fill=SHIRT_TEAR)
    d.point((25, 34), fill=SHIRT_TEAR)

    # Tied rope waist cord / survivor sash
    d.rectangle([9, 27, 27, 28], fill=LEATHER_MID)
    d.rectangle([16, 28, 18, 33], fill=LEATHER_LIGHT) # knot hanging down

    # Short sleeves capped at shoulders
    d.rectangle([5, 8, 10, 16], fill=SHIRT_WHITE_MID)
    d.rectangle([26, 8, 31, 16], fill=SHIRT_WHITE_MID)

    im.save(os.path.join(out_dir, "torso_female.png"))

# ==========================================
# 4. MALE TORSO (36x42) - Ragged Khaki Short-Sleeve
# ==========================================
def generate_torso_male():
    im = create_canvas(36, 42)
    d = ImageDraw.Draw(im)

    # Neck
    d.rectangle([13, 2, 23, 8], fill=SKIN_MID)
    d.rectangle([15, 4, 21, 8], fill=SKIN_LIGHT)

    # Ragged Khaki T-Shirt
    d.rectangle([7, 8, 29, 32], fill=SHIRT_MALE_MID)
    d.rectangle([9, 10, 27, 28], fill=SHIRT_MALE_LIGHT)
    d.rectangle([14, 8, 22, 11], fill=SKIN_LIGHT)

    # Ragged bottom hem
    d.rectangle([7, 30, 29, 34], fill=SHIRT_MALE_SHADE)
    d.point((10, 35), fill=OUTLINE)
    d.point((14, 35), fill=OUTLINE)
    d.point((21, 35), fill=OUTLINE)
    d.point((26, 35), fill=OUTLINE)

    # Leather belt
    d.rectangle([8, 28, 28, 30], fill=LEATHER_DARK)
    d.rectangle([16, 28, 20, 30], fill=(210, 180, 80, 255)) # brass buckle

    # Sleeves
    d.rectangle([4, 8, 9, 16], fill=SHIRT_MALE_MID)
    d.rectangle([27, 8, 32, 16], fill=SHIRT_MALE_MID)

    im.save(os.path.join(out_dir, "torso_male.png"))

# ==========================================
# 5. RIGHT ARM + STARTER WEAPON (52x48)
# Pivot at shoulder: (10, 14)
# Bare arm + Wooden/Steel Survivor Blade
# ==========================================
def generate_arm_r_starter():
    im = create_canvas(52, 48)
    d = ImageDraw.Draw(im)

    # Sleeve rim at shoulder
    d.rectangle([7, 8, 14, 13], fill=SHIRT_WHITE_MID)

    # Bare Skin Arm
    d.rectangle([8, 13, 14, 23], fill=SKIN_LIGHT)
    d.rectangle([10, 15, 13, 21], fill=SKIN_MID)
    # Forearm
    d.rectangle([9, 22, 15, 29], fill=SKIN_LIGHT)
    # Clenched hand gripping weapon
    d.rectangle([11, 28, 16, 33], fill=SKIN_MID)

    # Starter Weapon: Weathered Survivor Sword (환도 / 단검)
    # Wooden/Wrapped Grip
    d.rectangle([13, 24, 15, 36], fill=LEATHER_DARK)
    d.rectangle([10, 32, 18, 34], fill=LEATHER_LIGHT) # Guard / Tsuba

    # Chipped Steel Blade (Angled forward/upward)
    for i in range(26):
        bx = 18 + i
        by = 32 - int(i * 0.72)
        if 0 <= bx < 52 and 0 <= by < 48:
            d.point((bx, by - 1), fill=(140, 150, 160, 255)) # dull steel back
            d.point((bx, by), fill=(210, 220, 230, 255))     # blade core
            d.point((bx, by + 1), fill=(255, 255, 255, 255)) # sharp edge shine
    
    # Sharp tip shine
    d.point((43, 13), fill=(255, 255, 255, 255))

    im.save(os.path.join(out_dir, "arm_r_katana.png"))
    im.save(os.path.join(out_dir, "arm_r_starter.png"))

# ==========================================
# 6. LEFT ARM (28x38)
# Pivot at shoulder: (20, 8)
# Bare Skin Arm + Wrapped Bandage Wrist
# ==========================================
def generate_arm_l_starter():
    im = create_canvas(28, 38)
    d = ImageDraw.Draw(im)

    # Sleeve rim
    d.rectangle([16, 6, 23, 11], fill=SHIRT_WHITE_MID)

    # Bare Skin Arm
    d.rectangle([15, 11, 21, 20], fill=SKIN_LIGHT)
    d.rectangle([13, 19, 19, 26], fill=SKIN_MID)

    # White Cloth Bandage on Wrist
    d.rectangle([11, 25, 17, 30], fill=BANDAGE_LIGHT)
    d.point((13, 27), fill=BANDAGE_SHADE)
    d.point((15, 28), fill=BANDAGE_SHADE)

    # Hand / Fist
    d.rectangle([9, 29, 16, 35], fill=SKIN_MID)
    d.rectangle([10, 30, 15, 34], fill=SKIN_LIGHT)

    im.save(os.path.join(out_dir, "arm_l.png"))
    im.save(os.path.join(out_dir, "arm_l_starter.png"))

# ==========================================
# 7. LEGS (40x46) - Ragged Shorts & Bare Knees
# Pivot at hips: (20, 6)
# ==========================================
def generate_legs_starter():
    im = create_canvas(40, 46)
    d = ImageDraw.Draw(im)

    # Pelvis Base / Belt
    d.rectangle([10, 2, 30, 8], fill=SHORTS_DENIM_SHADE)

    # Left Short (Frayed denim)
    d.rectangle([8, 8, 19, 18], fill=SHORTS_DENIM_MID)
    d.rectangle([9, 10, 18, 17], fill=SHORTS_DENIM_LIGHT)
    # Frayed hem threads
    d.point((8, 19), fill=SHORTS_DENIM_TEAR)
    d.point((11, 20), fill=SHORTS_DENIM_TEAR)
    d.point((14, 19), fill=SHORTS_DENIM_TEAR)
    d.point((17, 20), fill=SHORTS_DENIM_TEAR)

    # Right Short (Frayed denim)
    d.rectangle([21, 8, 32, 18], fill=SHORTS_DENIM_MID)
    d.rectangle([22, 10, 31, 17], fill=SHORTS_DENIM_LIGHT)
    d.point((21, 19), fill=SHORTS_DENIM_TEAR)
    d.point((24, 20), fill=SHORTS_DENIM_TEAR)
    d.point((28, 19), fill=SHORTS_DENIM_TEAR)
    d.point((31, 20), fill=SHORTS_DENIM_TEAR)

    # Bare Skin Legs (Thigh to Knee)
    d.rectangle([10, 19, 17, 28], fill=SKIN_LIGHT)
    d.rectangle([23, 19, 30, 28], fill=SKIN_LIGHT)
    # Knee definition
    d.point((13, 26), fill=SKIN_SHADE)
    d.point((26, 26), fill=SKIN_SHADE)

    # Bandage wrap on right shin
    d.rectangle([23, 28, 30, 35], fill=BANDAGE_LIGHT)
    d.point((25, 30), fill=BANDAGE_SHADE)
    d.point((27, 33), fill=BANDAGE_SHADE)
    # Bare Left shin
    d.rectangle([10, 28, 17, 36], fill=SKIN_MID)

    # Survivor Shoes / Simple Boots
    d.rectangle([8, 36, 18, 43], fill=LEATHER_MID)
    d.rectangle([9, 41, 18, 44], fill=LEATHER_DARK) # Sole
    d.rectangle([21, 35, 31, 43], fill=LEATHER_MID)
    d.rectangle([22, 41, 31, 44], fill=LEATHER_DARK) # Sole

    im.save(os.path.join(out_dir, "legs.png"))
    im.save(os.path.join(out_dir, "legs_starter.png"))

if __name__ == "__main__":
    generate_head_female()
    generate_head_male()
    generate_torso_female()
    generate_torso_male()
    generate_arm_r_starter()
    generate_arm_l_starter()
    generate_legs_starter()
    print("All ragged anime survivor pixel parts generated successfully!")
