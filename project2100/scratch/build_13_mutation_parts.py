import os, math
from PIL import Image, ImageDraw

hero_dir = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
mut_dir = os.path.join(hero_dir, "mutations")
os.makedirs(mut_dir, exist_ok=True)

CANVAS_W = 120
CANVAS_H = 120
OUTLINE = (20, 16, 25, 255)

def create_frame():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# 1. HORNS (body_mutation)
def draw_horns(d, cx, cy):
    ox, oy = cx - 20, cy - 20
    d.polygon([(ox+10, oy+8), (ox+2, oy-8), (ox+14, oy+4)], fill=(180, 30, 40, 255), outline=OUTLINE)
    d.polygon([(ox+5, oy-4), (ox+3, oy-8), (ox+9, oy-2)], fill=(255, 120, 60, 255))
    d.polygon([(ox+30, oy+8), (ox+38, oy-8), (ox+26, oy+4)], fill=(180, 30, 40, 255), outline=OUTLINE)
    d.polygon([(ox+35, oy-4), (ox+37, oy-8), (ox+31, oy-2)], fill=(255, 120, 60, 255))
    d.polygon([(ox+18, oy+4), (ox+20, oy-4), (ox+22, oy+4)], fill=(240, 190, 40, 255), outline=OUTLINE)

# 2. TAIL (energy_discharge)
def draw_tail(d, cx, cy, wave=0):
    ox, oy = cx - 20, cy - 8
    pts = [
        (ox+6, oy+10),
        (ox-6, oy+16 + wave),
        (ox-16, oy+14 + wave*2),
        (ox-24, oy+8 + wave),
        (ox-32, oy-2)
    ]
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=(60, 40, 75, 255), width=4)
        d.line([pts[i], pts[i+1]], fill=(0, 240, 255, 255), width=2)
    tx, ty = pts[-1]
    d.polygon([(tx, ty), (tx-8, ty-6), (tx-4, ty+6)], fill=(255, 40, 80, 255), outline=OUTLINE)

# 3. VISOR (sensory_tech)
def draw_visor(d, cx, cy):
    ox, oy = cx - 20, cy - 20
    d.rectangle([ox+15, oy+17, ox+28, oy+22], fill=(255, 20, 60, 240), outline=(255, 255, 255, 255))
    d.line([(ox+16, oy+19), (ox+27, oy+19)], fill=(255, 220, 240, 255))
    d.line([(ox+12, oy+16), (ox+14, oy+22)], fill=(120, 130, 150, 255), width=2)
    d.point((ox+11, oy+14), fill=(0, 240, 255, 255))

# 4. WINGS (blood_absorption)
def draw_wings(d, cx, cy, wing_flare=0):
    ox, oy = cx - 18, cy - 18
    # Left Wing
    d.polygon([(ox+4, oy+14), (ox-24 - wing_flare, oy-18), (ox-14, oy+8), (ox-28 - wing_flare, oy+4), (ox-6, oy+22)], 
              fill=(45, 25, 60, 240), outline=OUTLINE)
    d.line([(ox+4, oy+14), (ox-24 - wing_flare, oy-18)], fill=(180, 50, 220, 255), width=2)
    d.polygon([(ox-2, oy+12), (ox-18 - wing_flare, oy-8), (ox-8, oy+16)], fill=(220, 60, 100, 200))
    # Right Wing
    d.polygon([(ox+28, oy+14), (ox+54 + wing_flare, oy-18), (ox+44, oy+8), (ox+58 + wing_flare, oy+4), (ox+36, oy+22)], 
              fill=(45, 25, 60, 240), outline=OUTLINE)
    d.line([(ox+28, oy+14), (ox+54 + wing_flare, oy-18)], fill=(180, 50, 220, 255), width=2)
    d.polygon([(ox+30, oy+12), (ox+48 + wing_flare, oy-8), (ox+38, oy+16)], fill=(220, 60, 100, 200))

# 5. SHELL (cellular_shield)
def draw_shell(d, cx, cy):
    ox, oy = cx - 20, cy - 10
    # Chitinous tortoise/beetle shell on back
    d.ellipse([ox-14, oy+4, ox+8, oy+32], fill=(35, 65, 55, 240), outline=OUTLINE)
    d.ellipse([ox-11, oy+7, ox+5, oy+29], fill=(50, 95, 80, 255))
    # Glowing biomechanical shield seams
    d.line([(ox-9, oy+18), (ox+3, oy+18)], fill=(0, 255, 200, 255), width=2)
    d.line([(ox-3, oy+8), (ox-3, oy+28)], fill=(0, 255, 200, 255), width=2)

# 6. FAIRY_WINGS (fairy_magic)
def draw_fairy_wings(d, cx, cy, wing_flare=0):
    ox, oy = cx - 18, cy - 18
    # Ethereal translucent radiant wings with golden-cyan sparkles
    d.polygon([(ox+4, oy+12), (ox-28 - wing_flare, oy-22), (ox-16, oy+4), (ox-24, oy+16), (ox+2, oy+20)],
              fill=(160, 240, 255, 180), outline=(255, 255, 255, 220))
    d.polygon([(ox+26, oy+12), (ox+52 + wing_flare, oy-22), (ox+42, oy+4), (ox+48, oy+16), (ox+24, oy+20)],
              fill=(255, 210, 240, 180), outline=(255, 255, 255, 220))
    # Glowing sparkles
    for spx, spy in [(ox-15, oy-10), (ox-8, oy-5), (ox+38, oy-10), (ox+32, oy-5)]:
        d.point((spx, spy), fill=(255, 255, 200, 255))

# 7. BOOSTER (power_overload)
def draw_booster(d, cx, cy, flare=0):
    ox, oy = cx - 18, cy - 12
    # Twin rocket booster thrusters on back
    d.rectangle([ox-10, oy+8, ox-2, oy+24], fill=(50, 55, 65, 255), outline=OUTLINE)
    d.rectangle([ox-14, oy+10, ox-10, oy+22], fill=(80, 85, 95, 255))
    # Plasma exhaust flame
    d.polygon([(ox-8, oy+24), (ox-4, oy+24), (ox-6, oy+34 + flare*3)], fill=(0, 220, 255, 240))
    d.polygon([(ox-13, oy+22), (ox-11, oy+22), (ox-12, oy+30 + flare*2)], fill=(255, 200, 50, 240))

# 8. SPIKES (thermal_control)
def draw_spikes(d, cx, cy):
    ox, oy = cx - 18, cy - 18
    # Flaming volcanic spikes on both shoulders
    d.polygon([(ox-2, oy+10), (ox-12, oy-4), (ox+6, oy+6)], fill=(220, 70, 20, 255), outline=OUTLINE)
    d.polygon([(ox-8, oy-1), (ox-11, oy-3), (ox-4, oy+3)], fill=(255, 220, 40, 255))
    d.polygon([(ox+32, oy+10), (ox+42, oy-4), (ox+24, oy+6)], fill=(220, 70, 20, 255), outline=OUTLINE)
    d.polygon([(ox+38, oy-1), (ox+41, oy-3), (ox+34, oy+3)], fill=(255, 220, 40, 255))

# 9. ANTENNAE (ultrasonic_disruption)
def draw_antennae(d, cx, cy):
    ox, oy = cx - 20, cy - 20
    # Twin sonic sensor antennae on forehead
    d.line([(ox+14, oy+8), (ox+8, oy-12), (ox+4, oy-16)], fill=(0, 240, 255, 255), width=2)
    d.line([(ox+26, oy+8), (ox+32, oy-12), (ox+36, oy-16)], fill=(0, 240, 255, 255), width=2)
    # Sensor bulbs
    d.ellipse([ox+2, oy-18, ox+6, oy-14], fill=(255, 255, 255, 255))
    d.ellipse([ox+34, oy-18, ox+38, oy-14], fill=(255, 255, 255, 255))

# 10. CLAWS (berserker_madness)
def draw_claws(d, cx, cy):
    ox, oy = cx - 18, cy - 18
    # Front hand beast frenzy claws (right hand around ox+32, oy+32)
    for i in range(3):
        d.line([(ox+30 + i*4, oy+30), (ox+34 + i*4, oy+40)], fill=(220, 20, 40, 255), width=2)
        d.point((ox+34 + i*4, oy+41), fill=(255, 180, 180, 255))

# 11. CORE (radiation_assimilation)
def draw_core(d, cx, cy):
    ox, oy = cx - 18, cy - 18
    # Radiant Arc Bio-Reactor Core on Chest
    d.ellipse([ox+14, oy+14, ox+22, oy+22], fill=(0, 240, 255, 255), outline=(255, 255, 255, 255))
    d.point((ox+18, oy+18), fill=(255, 255, 255, 255))
    d.line([(ox+10, oy+18), (ox+14, oy+18)], fill=(0, 200, 240, 255), width=2)
    d.line([(ox+22, oy+18), (ox+26, oy+18)], fill=(0, 200, 240, 255), width=2)
    d.line([(ox+18, oy+10), (ox+18, oy+14)], fill=(0, 200, 240, 255), width=2)
    d.line([(ox+18, oy+22), (ox+18, oy+26)], fill=(0, 200, 240, 255), width=2)

# 12. CRYSTALS (meltdown_control)
def draw_crystals(d, cx, cy):
    ox, oy = cx - 18, cy - 18
    # Glowing green/amber radioactive spine crystals erupting from back
    d.polygon([(ox-2, oy+8), (ox-14, oy-2), (ox-6, oy+16)], fill=(80, 240, 60, 240), outline=OUTLINE)
    d.polygon([(ox-4, oy+16), (ox-18, oy+12), (ox-6, oy+24)], fill=(120, 255, 90, 240), outline=OUTLINE)
    d.polygon([(ox-2, oy+24), (ox-12, oy+24), (ox-4, oy+30)], fill=(80, 240, 60, 240), outline=OUTLINE)
    d.line([(ox-2, oy+8), (ox-14, oy-2)], fill=(220, 255, 180, 255), width=1)

# 13. HALO (hightech_engineering)
def draw_halo(d, cx, cy):
    ox, oy = cx - 20, cy - 20
    # High-tech holographic ring / orbital drone hovering above head
    d.ellipse([ox+4, oy-24, ox+36, oy-14], fill=None, outline=(0, 240, 255, 220), width=2)
    # Hologram node points
    d.ellipse([ox+2, oy-20, ox+6, oy-18], fill=(255, 255, 255, 255))
    d.ellipse([ox+34, oy-20, ox+38, oy-18], fill=(255, 255, 255, 255))
    d.ellipse([ox+18, oy-25, ox+22, oy-23], fill=(0, 255, 200, 255))

ALL_PARTS = {
    "horns": draw_horns,
    "tail": draw_tail,
    "visor": draw_visor,
    "wings": draw_wings,
    "shell": draw_shell,
    "fairy_wings": draw_fairy_wings,
    "booster": draw_booster,
    "spikes": draw_spikes,
    "antennae": draw_antennae,
    "claws": draw_claws,
    "core": draw_core,
    "crystals": draw_crystals,
    "halo": draw_halo,
}

def generate_all_mutations():
    print("=== Generating 13 Distinct Mutation Parts ===")
    cx, cy = 60, 52
    
    for part_name, draw_fn in ALL_PARTS.items():
        # IDLE (4 frames)
        for i in range(4):
            im = create_frame()
            d = ImageDraw.Draw(im)
            bob = -2 if i in [1, 2] else 0
            if part_name in ["wings", "fairy_wings"]:
                draw_fn(d, cx, cy + bob, wing_flare=i*2)
            elif part_name == "tail":
                draw_fn(d, cx, cy + bob, wave=i*2)
            elif part_name == "booster":
                draw_fn(d, cx, cy + bob, flare=i)
            else:
                draw_fn(d, cx, cy + bob)
            im.save(os.path.join(mut_dir, f"{part_name}_idle_{i}.png"))
            
        # RUN (6 frames)
        for i in range(6):
            im = create_frame()
            d = ImageDraw.Draw(im)
            bob = -2 if i in [0, 3] else 0
            tilt = 2 if i in [0, 1, 3, 4] else 0
            if part_name in ["wings", "fairy_wings"]:
                draw_fn(d, cx + tilt, cy + bob, wing_flare=(i%3)*3)
            elif part_name == "tail":
                draw_fn(d, cx + tilt, cy + bob, wave=(i%3)*3)
            elif part_name == "booster":
                draw_fn(d, cx + tilt, cy + bob, flare=i%3)
            else:
                draw_fn(d, cx + tilt, cy + bob)
            im.save(os.path.join(mut_dir, f"{part_name}_run_{i}.png"))

        # ATTACK (4 frames)
        lunges = [0, 8, 6, 0]
        for i, lx in enumerate(lunges):
            im = create_frame()
            d = ImageDraw.Draw(im)
            if part_name in ["wings", "fairy_wings"]:
                draw_fn(d, cx + lx, cy, wing_flare=6 if i==1 else 0)
            elif part_name == "tail":
                draw_fn(d, cx + lx, cy, wave=4 if i==1 else 0)
            elif part_name == "booster":
                draw_fn(d, cx + lx, cy, flare=3 if i==1 else 0)
            else:
                draw_fn(d, cx + lx, cy)
            im.save(os.path.join(mut_dir, f"{part_name}_attack_{i}.png"))

        # SKILL (4 frames)
        lx_ly = [(0, 4), (4, -14), (6, -18), (4, 4)]
        for i, (lx, ly) in enumerate(lx_ly):
            im = create_frame()
            d = ImageDraw.Draw(im)
            if part_name in ["wings", "fairy_wings"]:
                draw_fn(d, cx + lx, cy + ly, wing_flare=8 if i==2 else 2)
            elif part_name == "tail":
                draw_fn(d, cx + lx, cy + ly, wave=6 if i==2 else 0)
            elif part_name == "booster":
                draw_fn(d, cx + lx, cy + ly, flare=4 if i==2 else 1)
            else:
                draw_fn(d, cx + lx, cy + ly)
            im.save(os.path.join(mut_dir, f"{part_name}_skill_{i}.png"))
            
    print(f"Successfully generated all 13 mutation parts ({len(ALL_PARTS) * 18} files)!")

if __name__ == "__main__":
    generate_all_mutations()
