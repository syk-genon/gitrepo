import os
import math
from PIL import Image, ImageDraw

hero_dir = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
mut_dir = os.path.join(hero_dir, "mutations")
os.makedirs(mut_dir, exist_ok=True)

CANVAS_W = 120
CANVAS_H = 120

OUTLINE = (20, 16, 25, 255)

def create_frame():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# =============================================================
# 1. HORNS (Demonic / Chitin Spikes on Head)
# =============================================================
def draw_horns(d, cx, cy):
    # cx, cy: face center (56, 28)
    ox, oy = cx - 20, cy - 20
    # Left Horn
    d.polygon([(ox+10, oy+8), (ox+2, oy-8), (ox+14, oy+4)], fill=(180, 30, 40, 255), outline=OUTLINE)
    d.polygon([(ox+5, oy-4), (ox+3, oy-8), (ox+9, oy-2)], fill=(255, 120, 60, 255))
    # Right Horn
    d.polygon([(ox+30, oy+8), (ox+38, oy-8), (ox+26, oy+4)], fill=(180, 30, 40, 255), outline=OUTLINE)
    d.polygon([(ox+35, oy-4), (ox+37, oy-8), (ox+31, oy-2)], fill=(255, 120, 60, 255))
    # Crown Spike
    d.polygon([(ox+18, oy+4), (ox+20, oy-4), (ox+22, oy+4)], fill=(240, 190, 40, 255), outline=OUTLINE)

# =============================================================
# 2. WINGS (Biomechanical / Demon Chitin Wings on Back)
# =============================================================
def draw_wings(d, cx, cy, wing_flare=0):
    # cx, cy: chest center (56, 52)
    ox, oy = cx - 18, cy - 18
    # Left Wing (spreads left & up)
    d.polygon([(ox+4, oy+14), (ox-24 - wing_flare, oy-18), (ox-14, oy+8), (ox-28 - wing_flare, oy+4), (ox-6, oy+22)], 
              fill=(45, 25, 60, 240), outline=OUTLINE)
    d.line([(ox+4, oy+14), (ox-24 - wing_flare, oy-18)], fill=(180, 50, 220, 255), width=2)
    d.polygon([(ox-2, oy+12), (ox-18 - wing_flare, oy-8), (ox-8, oy+16)], fill=(220, 60, 100, 200))

    # Right Wing (spreads right & up behind shoulder)
    d.polygon([(ox+28, oy+14), (ox+54 + wing_flare, oy-18), (ox+44, oy+8), (ox+58 + wing_flare, oy+4), (ox+36, oy+22)], 
              fill=(45, 25, 60, 240), outline=OUTLINE)
    d.line([(ox+28, oy+14), (ox+54 + wing_flare, oy-18)], fill=(180, 50, 220, 255), width=2)
    d.polygon([(ox+30, oy+12), (ox+48 + wing_flare, oy-8), (ox+38, oy+16)], fill=(220, 60, 100, 200))

# =============================================================
# 3. TAIL (Prehensile Bio-Mechanical Spiked Tail)
# =============================================================
def draw_tail(d, cx, cy, wave=0):
    # cx, cy: hips center (56, 72)
    ox, oy = cx - 20, cy - 8
    # Segments trailing left/down
    pts = [
        (ox+6, oy+10),
        (ox-4, oy+16 + wave),
        (ox-14, oy+14 + wave*2),
        (ox-22, oy+8 + wave),
        (ox-28, oy-2)
    ]
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=(60, 40, 75, 255), width=4)
        d.line([pts[i], pts[i+1]], fill=(0, 240, 255, 255), width=2)
    # Stinger / Blade tip
    tx, ty = pts[-1]
    d.polygon([(tx, ty), (tx-8, ty-6), (tx-4, ty+6)], fill=(255, 40, 80, 255), outline=OUTLINE)

# =============================================================
# 4. CORE (Luminescent Bio-Reactor Chest Core & Shoulder Shield)
# =============================================================
def draw_core(d, cx, cy):
    # cx, cy: chest center (56, 52)
    ox, oy = cx - 18, cy - 18
    # Radiant Core on Chest
    d.ellipse([ox+14, oy+14, ox+22, oy+22], fill=(0, 240, 255, 255), outline=(255, 255, 255, 255))
    d.point((ox+18, oy+18), fill=(255, 255, 255, 255))
    d.point((ox+17, oy+17), fill=(255, 255, 255, 255))
    # Bio-energy conduits
    d.line([(ox+10, oy+18), (ox+14, oy+18)], fill=(0, 200, 240, 255), width=2)
    d.line([(ox+22, oy+18), (ox+26, oy+18)], fill=(0, 200, 240, 255), width=2)
    d.line([(ox+18, oy+10), (ox+18, oy+14)], fill=(0, 200, 240, 255), width=2)
    d.line([(ox+18, oy+22), (ox+18, oy+26)], fill=(0, 200, 240, 255), width=2)

# =============================================================
# 5. VISOR (Cybernetic Sensor Eye / Tactical Visor)
# =============================================================
def draw_visor(d, cx, cy):
    # cx, cy: face center (56, 28)
    ox, oy = cx - 20, cy - 20
    # Glowing Crimson/Cyan Scanner Visor across eyes
    d.rectangle([ox+15, oy+17, ox+28, oy+22], fill=(255, 20, 60, 240), outline=(255, 255, 255, 255))
    d.line([(ox+16, oy+19), (ox+27, oy+19)], fill=(255, 220, 240, 255))
    # Earpiece antenna
    d.line([(ox+12, oy+16), (ox+14, oy+22)], fill=(120, 130, 150, 255), width=2)
    d.point((ox+11, oy+14), fill=(0, 240, 255, 255))

# =============================================================
# Generate 18 frames for each mutation part
# =============================================================
def generate_all_mutations():
    part_drawers = {
        "horns": draw_horns,
        "wings": draw_wings,
        "tail": draw_tail,
        "core": draw_core,
        "visor": draw_visor
    }

    # IDLE (4 frames)
    for i in range(4):
        bob = -2 if i in [1, 2] else 0
        wave = 2 if i in [1, 2] else 0
        for name, drawer in part_drawers.items():
            im = create_frame()
            d = ImageDraw.Draw(im)
            if name in ["horns", "visor"]:
                drawer(d, 56, 28 + bob)
            elif name == "wings":
                drawer(d, 56, 52 + bob, wing_flare=(4 if i in [1, 2] else 0))
            elif name == "core":
                drawer(d, 56, 52 + bob)
            elif name == "tail":
                drawer(d, 56, 72, wave=wave)
            im.save(os.path.join(mut_dir, f"{name}_idle_{i}.png"))

    # RUN (6 frames)
    leg_bob = [-2, 0, 0, -2, 0, 0]
    for i in range(6):
        bob = leg_bob[i]
        wave = 3 if i % 2 == 1 else -2
        for name, drawer in part_drawers.items():
            im = create_frame()
            d = ImageDraw.Draw(im)
            if name in ["horns", "visor"]:
                drawer(d, 58, 28 + bob)
            elif name == "wings":
                drawer(d, 56, 52 + bob, wing_flare=6)
            elif name == "core":
                drawer(d, 56, 52 + bob)
            elif name == "tail":
                drawer(d, 56, 72, wave=wave)
            im.save(os.path.join(mut_dir, f"{name}_run_{i}.png"))

    # ATTACK (4 frames)
    lunges = [0, 8, 6, 0]
    for i, lx in enumerate(lunges):
        wave = 4 if i == 1 else 0
        for name, drawer in part_drawers.items():
            im = create_frame()
            d = ImageDraw.Draw(im)
            if name in ["horns", "visor"]:
                drawer(d, 56 + lx, 28)
            elif name == "wings":
                drawer(d, 56 + lx, 52, wing_flare=(8 if i == 1 else 2))
            elif name == "core":
                drawer(d, 56 + lx, 52)
            elif name == "tail":
                drawer(d, 56 + lx, 72, wave=wave)
            im.save(os.path.join(mut_dir, f"{name}_attack_{i}.png"))

    # SKILL (4 frames)
    lx_ly = [(0, 4), (4, -14), (6, -18), (4, 4)]
    for i, (lx, ly) in enumerate(lx_ly):
        for name, drawer in part_drawers.items():
            im = create_frame()
            d = ImageDraw.Draw(im)
            if name in ["horns", "visor"]:
                drawer(d, 56 + lx, 28 + ly)
            elif name == "wings":
                drawer(d, 56 + lx, 52 + ly, wing_flare=12)
            elif name == "core":
                drawer(d, 56 + lx, 52 + ly)
            elif name == "tail":
                drawer(d, 56 + lx, 72 + (ly if ly > 0 else ly//2), wave=-4)
            im.save(os.path.join(mut_dir, f"{name}_skill_{i}.png"))

if __name__ == "__main__":
    generate_all_mutations()
    print("All 5 mutation parts (horns, wings, tail, core, visor) x 18 action frames generated cleanly!")
