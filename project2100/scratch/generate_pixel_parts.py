import os
from PIL import Image, ImageDraw

out_dir = r"C:\Users\exbxda13\project2100\assets\pixel_parts"
os.makedirs(out_dir, exist_ok=True)

# Helper function to create RGBA canvas
def create_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def draw_pixel_rect(draw, x1, y1, x2, y2, fill, outline=None):
    draw.rectangle([x1, y1, x2, y2], fill=fill, outline=outline)

# 1. HEAD FEMALE (40x34)
# Ponytail, tactical HUD visor (Cyan), cheek guard
def generate_head_female():
    im = create_canvas(40, 34)
    d = ImageDraw.Draw(im)
    
    # Hair / Helmet base (Dark slate navy)
    d.rectangle([10, 4, 30, 24], fill=(24, 32, 47, 255))
    d.rectangle([12, 2, 28, 5], fill=(35, 46, 68, 255)) # top
    # Ponytail extending to the left
    d.rectangle([4, 6, 11, 14], fill=(16, 22, 34, 255))
    d.rectangle([2, 10, 8, 18], fill=(12, 17, 28, 255))
    d.rectangle([3, 8, 6, 10], fill=(0, 240, 255, 255)) # hair tie / cyan cyber clip
    
    # Face / Visor area
    d.rectangle([16, 10, 32, 18], fill=(0, 240, 255, 255)) # Cyan Glowing Visor
    d.rectangle([18, 12, 30, 16], fill=(180, 250, 255, 255)) # Visor inner core bright
    d.rectangle([16, 10, 32, 11], fill=(0, 180, 200, 255)) # visor upper shade
    
    # Lower face mask / respirator
    d.rectangle([16, 19, 30, 27], fill=(45, 55, 72, 255))
    d.rectangle([20, 22, 26, 26], fill=(20, 25, 35, 255)) # respirator vent
    d.rectangle([21, 23, 25, 24], fill=(0, 240, 255, 200)) # tiny filter glow
    
    # Headset / ear piece
    d.rectangle([12, 14, 16, 22], fill=(71, 85, 105, 255))
    d.rectangle([13, 16, 15, 20], fill=(255, 230, 0, 255)) # Yellow status LED
    
    # Dark pixel outline
    for x in range(10, 31):
        d.point((x, 1), fill=(10, 15, 25, 255))
        d.point((x, 28), fill=(10, 15, 25, 255))
    for y in range(4, 28):
        d.point((9, y), fill=(10, 15, 25, 255))
        d.point((32, y), fill=(10, 15, 25, 255))
        
    im.save(os.path.join(out_dir, "head_female.png"))

# 2. HEAD MALE (40x34)
# Heavy tactical helmet, Amber Visor, antenna
def generate_head_male():
    im = create_canvas(40, 34)
    d = ImageDraw.Draw(im)
    
    # Helmet dome
    d.rectangle([10, 4, 32, 25], fill=(30, 41, 59, 255))
    d.rectangle([12, 2, 30, 6], fill=(51, 65, 85, 255))
    # Hazard yellow accent stripe on helmet
    d.rectangle([18, 2, 22, 10], fill=(255, 230, 0, 255))
    
    # Amber Visor
    d.rectangle([18, 10, 34, 17], fill=(255, 170, 0, 255))
    d.rectangle([20, 12, 32, 15], fill=(255, 235, 150, 255))
    
    # Heavy blast chin/jaw guard
    d.rectangle([16, 18, 33, 28], fill=(40, 50, 65, 255))
    d.rectangle([22, 21, 28, 26], fill=(15, 20, 30, 255))
    d.rectangle([23, 22, 27, 23], fill=(255, 170, 0, 200)) # glow
    
    # Comm antenna
    d.rectangle([8, 0, 10, 14], fill=(100, 116, 139, 255))
    d.point((9, 0), fill=(255, 0, 60, 255)) # red beacon on top
    
    # Outline
    for x in range(10, 34):
        d.point((x, 1), fill=(10, 15, 25, 255))
        d.point((x, 29), fill=(10, 15, 25, 255))
    for y in range(3, 29):
        d.point((9, y), fill=(10, 15, 25, 255))
        d.point((35, y), fill=(10, 15, 25, 255))
        
    im.save(os.path.join(out_dir, "head_male.png"))

# 3. HEAD NEMESIS (40x34)
# Void demon horns, Crimson visor
def generate_head_nemesis():
    im = create_canvas(40, 34)
    d = ImageDraw.Draw(im)
    
    # Horns
    d.rectangle([4, 0, 10, 8], fill=(180, 0, 40, 255))
    d.rectangle([6, 2, 8, 12], fill=(255, 50, 90, 255))
    d.rectangle([30, 0, 36, 8], fill=(180, 0, 40, 255))
    d.rectangle([32, 2, 34, 12], fill=(255, 50, 90, 255))
    
    # Dark Obsidian Skull
    d.rectangle([10, 6, 30, 26], fill=(15, 10, 20, 255))
    
    # Dual Crimson Slit Eyes
    d.rectangle([16, 12, 21, 15], fill=(255, 0, 80, 255))
    d.rectangle([25, 12, 30, 15], fill=(255, 0, 80, 255))
    d.point((18, 13), fill=(255, 200, 220, 255))
    d.point((27, 13), fill=(255, 200, 220, 255))
    
    # Sharp chin
    d.rectangle([16, 22, 24, 28], fill=(30, 15, 35, 255))
    im.save(os.path.join(out_dir, "head_nemesis.png"))

# 4. TORSO FEMALE (32x38)
# Sleek armor, Cyan Arc Core
def generate_torso_female():
    im = create_canvas(32, 38)
    d = ImageDraw.Draw(im)
    
    # Shoulders / Neck
    d.rectangle([8, 2, 24, 8], fill=(30, 41, 59, 255))
    # Chest Armor Plates
    d.rectangle([4, 6, 28, 24], fill=(45, 55, 75, 255))
    d.rectangle([6, 8, 26, 20], fill=(60, 75, 100, 255)) # highlight plate
    
    # Glowing Arc Reactor Core (Center)
    d.rectangle([13, 11, 19, 17], fill=(0, 240, 255, 255))
    d.rectangle([14, 12, 18, 16], fill=(220, 255, 255, 255)) # pure bright center
    
    # Tactical Abdomen / Belt
    d.rectangle([8, 23, 24, 32], fill=(25, 30, 42, 255))
    d.rectangle([6, 30, 26, 35], fill=(15, 20, 28, 255)) # Utility Belt
    d.rectangle([14, 31, 18, 34], fill=(255, 230, 0, 255)) # Yellow belt buckle
    d.rectangle([8, 31, 11, 35], fill=(70, 80, 95, 255)) # Pouch 1
    d.rectangle([21, 31, 24, 35], fill=(70, 80, 95, 255)) # Pouch 2
    
    # Dark Outline
    d.rectangle([4, 6, 5, 24], fill=(15, 20, 30, 255))
    d.rectangle([27, 6, 28, 24], fill=(15, 20, 30, 255))
    d.rectangle([6, 35, 26, 36], fill=(15, 20, 30, 255))
    im.save(os.path.join(out_dir, "torso_female.png"))

# 5. TORSO MALE (32x38)
# Heavy armor plate, Hazard stripes, Reactor
def generate_torso_male():
    im = create_canvas(32, 38)
    d = ImageDraw.Draw(im)
    
    # Heavy Shoulders & Chest
    d.rectangle([4, 4, 28, 24], fill=(50, 60, 80, 255))
    d.rectangle([6, 6, 26, 18], fill=(70, 85, 110, 255))
    
    # Hazard diagonal stripes
    d.rectangle([6, 6, 10, 9], fill=(255, 230, 0, 255))
    d.rectangle([14, 6, 18, 9], fill=(255, 230, 0, 255))
    d.rectangle([22, 6, 26, 9], fill=(255, 230, 0, 255))
    
    # Reactor
    d.rectangle([13, 12, 19, 18], fill=(0, 240, 255, 255))
    d.rectangle([14, 13, 18, 17], fill=(230, 255, 255, 255))
    
    # Heavy belt
    d.rectangle([6, 25, 26, 35], fill=(20, 25, 35, 255))
    d.rectangle([13, 29, 19, 34], fill=(255, 180, 0, 255))
    im.save(os.path.join(out_dir, "torso_male.png"))

# 6. TORSO NEMESIS (32x38)
def generate_torso_nemesis():
    im = create_canvas(32, 38)
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, 28, 26], fill=(20, 10, 25, 255))
    d.rectangle([6, 6, 26, 22], fill=(40, 20, 50, 255))
    # Crimson void rift in chest
    d.rectangle([12, 10, 20, 20], fill=(255, 0, 80, 255))
    d.rectangle([14, 12, 18, 18], fill=(255, 180, 220, 255))
    d.rectangle([6, 26, 26, 35], fill=(15, 8, 20, 255))
    im.save(os.path.join(out_dir, "torso_nemesis.png"))

# 7. RIGHT ARM + KATANA (48x44)
# Pivot at shoulder: (8, 10)
def generate_arm_r_katana():
    im = create_canvas(48, 44)
    d = ImageDraw.Draw(im)
    
    # Shoulder Pauldron (Upper Arm)
    d.rectangle([4, 6, 14, 16], fill=(50, 65, 85, 255))
    d.rectangle([6, 7, 12, 13], fill=(70, 90, 115, 255))
    d.rectangle([6, 16, 12, 24], fill=(35, 45, 60, 255)) # Forearm
    d.rectangle([7, 24, 12, 28], fill=(25, 30, 40, 255)) # Hand / Gauntlet
    
    # Katana Hilt & Guard
    d.rectangle([9, 20, 11, 32], fill=(20, 20, 25, 255)) # Hilt
    d.rectangle([6, 28, 14, 30], fill=(255, 230, 0, 255)) # Gold Tsuba/Guard
    
    # Luminous High-Frequency Plasma Blade (Extends forward/upward)
    # Blade length ~28px
    for i in range(28):
        bx = 14 + i
        by = 28 - int(i * 0.7)
        if 0 <= bx < 48 and 0 <= by < 44:
            # Outer cyan glow
            d.point((bx, by - 1), fill=(0, 200, 255, 180))
            d.point((bx, by), fill=(0, 240, 255, 255))
            d.point((bx, by + 1), fill=(180, 250, 255, 255)) # white-cyan sharp edge
            d.point((bx, by + 2), fill=(0, 160, 220, 180))
            
    # Tip of blade
    d.point((42, 8), fill=(255, 255, 255, 255))
    im.save(os.path.join(out_dir, "arm_r_katana.png"))

# 8. RIGHT ARM NEMESIS (48x44)
def generate_arm_r_nemesis():
    im = create_canvas(48, 44)
    d = ImageDraw.Draw(im)
    d.rectangle([4, 6, 14, 16], fill=(30, 15, 35, 255))
    d.rectangle([6, 16, 12, 28], fill=(50, 20, 50, 255))
    # Crimson Void Blade
    for i in range(30):
        bx = 12 + i
        by = 28 - int(i * 0.75)
        if 0 <= bx < 48 and 0 <= by < 44:
            d.point((bx, by - 1), fill=(200, 0, 50, 180))
            d.point((bx, by), fill=(255, 0, 80, 255))
            d.point((bx, by + 1), fill=(255, 200, 230, 255))
    im.save(os.path.join(out_dir, "arm_r_nemesis.png"))

# 9. LEFT ARM (26x36)
# Pivot at shoulder: (18, 8)
def generate_arm_l():
    im = create_canvas(26, 36)
    d = ImageDraw.Draw(im)
    
    # Shoulder & Upper Arm
    d.rectangle([12, 6, 22, 16], fill=(40, 50, 70, 255))
    d.rectangle([14, 8, 20, 14], fill=(55, 70, 95, 255))
    
    # Forearm with shield projector nodule
    d.rectangle([8, 16, 18, 26], fill=(30, 40, 55, 255))
    d.rectangle([10, 18, 14, 23], fill=(0, 240, 255, 255)) # Shield emitter glow
    
    # Fist / Glove
    d.rectangle([6, 26, 14, 32], fill=(20, 25, 35, 255))
    im.save(os.path.join(out_dir, "arm_l.png"))

def generate_arm_l_nemesis():
    im = create_canvas(26, 36)
    d = ImageDraw.Draw(im)
    d.rectangle([12, 6, 22, 16], fill=(25, 12, 30, 255))
    d.rectangle([8, 16, 18, 26], fill=(45, 18, 50, 255))
    d.rectangle([10, 18, 14, 23], fill=(255, 0, 80, 255))
    # Claws
    d.rectangle([4, 26, 14, 33], fill=(20, 10, 25, 255))
    d.point((4, 34), fill=(255, 50, 90, 255))
    d.point((7, 34), fill=(255, 50, 90, 255))
    im.save(os.path.join(out_dir, "arm_l_nemesis.png"))

# 10. LEGS (36x44)
# Pivot at hips: (18, 4)
def generate_legs():
    im = create_canvas(36, 44)
    d = ImageDraw.Draw(im)
    
    # Pelvis
    d.rectangle([8, 2, 28, 8], fill=(25, 32, 45, 255))
    
    # Left Leg (Trousers & Knee)
    d.rectangle([6, 8, 16, 22], fill=(35, 45, 60, 255))
    d.rectangle([8, 18, 15, 24], fill=(55, 70, 90, 255)) # Knee Pad
    d.rectangle([7, 24, 15, 36], fill=(25, 32, 45, 255)) # Shin
    d.rectangle([4, 36, 16, 42], fill=(15, 20, 28, 255)) # Heavy Boot
    d.rectangle([4, 40, 17, 43], fill=(45, 55, 70, 255)) # Sole
    
    # Right Leg (Slightly spread)
    d.rectangle([20, 8, 30, 22], fill=(35, 45, 60, 255))
    d.rectangle([21, 18, 28, 24], fill=(55, 70, 90, 255)) # Knee Pad
    d.rectangle([21, 24, 29, 36], fill=(25, 32, 45, 255)) # Shin
    d.rectangle([20, 36, 32, 42], fill=(15, 20, 28, 255)) # Heavy Boot
    d.rectangle([19, 40, 32, 43], fill=(45, 55, 70, 255)) # Sole
    
    im.save(os.path.join(out_dir, "legs.png"))

def generate_legs_nemesis():
    im = create_canvas(36, 44)
    d = ImageDraw.Draw(im)
    d.rectangle([8, 2, 28, 8], fill=(20, 10, 25, 255))
    d.rectangle([6, 8, 16, 24], fill=(35, 15, 40, 255))
    d.rectangle([8, 20, 15, 25], fill=(255, 0, 80, 255)) # Red vent
    d.rectangle([5, 25, 16, 42], fill=(15, 8, 20, 255))
    d.rectangle([20, 8, 30, 24], fill=(35, 15, 40, 255))
    d.rectangle([21, 20, 28, 25], fill=(255, 0, 80, 255))
    d.rectangle([20, 25, 31, 42], fill=(15, 8, 20, 255))
    im.save(os.path.join(out_dir, "legs_nemesis.png"))

# 11. SLASH VFX SPRITE (64x64)
def generate_slash_vfx():
    im = create_canvas(64, 64)
    d = ImageDraw.Draw(im)
    # Dynamic crescent slash arc
    import math
    for deg in range(30, 150):
        rad = math.radians(deg)
        r = 28
        cx = 24 + int(r * math.cos(rad))
        cy = 32 - int(r * math.sin(rad))
        d.line([(cx-1, cy), (cx+2, cy+2)], fill=(0, 240, 255, 255), width=2)
        d.point((cx, cy), fill=(255, 255, 255, 255))
    im.save(os.path.join(out_dir, "vfx_slash.png"))

if __name__ == "__main__":
    generate_head_female()
    generate_head_male()
    generate_head_nemesis()
    generate_torso_female()
    generate_torso_male()
    generate_torso_nemesis()
    generate_arm_r_katana()
    generate_arm_r_nemesis()
    generate_arm_l()
    generate_arm_l_nemesis()
    generate_legs()
    generate_legs_nemesis()
    generate_slash_vfx()
    print("All pixel character parts generated successfully!")
