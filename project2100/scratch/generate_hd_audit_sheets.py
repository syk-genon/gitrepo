import os
from PIL import Image, ImageDraw

HERO_DIR = "assets/pixel_hero"
WEAPONS_DIR = os.path.join(HERO_DIR, "weapons")
ARMORS_DIR = os.path.join(HERO_DIR, "armors")
MUT_DIR = os.path.join(HERO_DIR, "mutations")
MONSTER_DIR = "assets/monsters"
SCRATCH_DIR = "scratch"
os.makedirs(SCRATCH_DIR, exist_ok=True)

def create_bg_tile(w, h):
    bg = Image.new("RGBA", (w, h), (15, 23, 42, 255))
    draw = ImageDraw.Draw(bg)
    draw.rectangle([2, 2, w - 3, h - 3], outline=(51, 65, 85, 255), width=1)
    return bg

# 1. All 4 Characters across 5 Frames + Monster Quality Comparison
chars = ["male", "female", "male_nemesis", "female_nemesis"]
frames_to_show = [("idle", 0), ("run", 0), ("attack", 1), ("attack", 2), ("skill", 1)]
cell_w, cell_h = 220, 230
sheet1 = Image.new("RGBA", (cell_w * 6, cell_h * 4 + 40), (9, 13, 22, 255))
d1 = ImageDraw.Draw(sheet1)
d1.text((15, 10), "240x240 HD HERO & NEMESIS SPRITES vs MONSTER ILLUSTRATION QUALITY", fill=(0, 240, 255, 255))

monster_files = sorted([f for f in os.listdir(MONSTER_DIR) if f.endswith(".png")])
sample_monsters = monster_files[:4] if len(monster_files) >= 4 else ["m_1_1.png"] * 4
for r, ch in enumerate(chars):
    for c, (act, frame_idx) in enumerate(frames_to_show):
        tile = create_bg_tile(cell_w - 8, cell_h - 8)
        p = os.path.join(HERO_DIR, f"{ch}_{act}_{frame_idx}.png")
        if os.path.exists(p):
            sp = Image.open(p).convert("RGBA").resize((200, 200), Image.Resampling.LANCZOS)
            tile.alpha_composite(sp, (6, 20))
        dt = ImageDraw.Draw(tile)
        dt.text((8, 6), f"{ch} | {act}_{frame_idx}", fill=(226, 232, 240, 255))
        sheet1.alpha_composite(tile, (c * cell_w + 4, r * cell_h + 36))

    # Col 5: Sample Monster comparison at same size
    tile = create_bg_tile(cell_w - 8, cell_h - 8)
    mp = os.path.join(MONSTER_DIR, sample_monsters[r])
    if os.path.exists(mp):
        msp = Image.open(mp).convert("RGBA")
        msp.thumbnail((190, 190), Image.Resampling.LANCZOS)
        tile.alpha_composite(msp, ((cell_w - 8 - msp.width) // 2, 28))
    dt = ImageDraw.Draw(tile)
    dt.text((8, 6), f"MONSTER: {sample_monsters[r]}", fill=(251, 191, 36, 255))
    sheet1.alpha_composite(tile, (5 * cell_w + 4, r * cell_h + 36))

sheet1.save(os.path.join(SCRATCH_DIR, "audit_hd_chars_vs_monsters.png"))

# 2. All 5 Armors + 5 Weapons Assembled on Male & Female (idle_0 & attack_1)
armors = ["military", "leather", "nano_carbon", "hardlight", "yeti_fur"]
weapons = ["katana", "axe", "crystal_sword", "heavy_cannon", "lava_launcher"]
sheet2 = Image.new("RGBA", (cell_w * 5, cell_h * 4 + 40), (9, 13, 22, 255))
d2 = ImageDraw.Draw(sheet2)
d2.text((15, 10), "240x240 HD ASSEMBLED ARMORS & WEAPONS (MALE & FEMALE)", fill=(0, 240, 255, 255))

for i in range(5):
    arm = armors[i]
    wpn = weapons[i]
    configs = [
        ("male", "idle", 0),
        ("male", "attack", 1),
        ("female", "idle", 0),
        ("female", "attack", 1),
    ]
    for r, (g, act, fi) in enumerate(configs):
        tile = create_bg_tile(cell_w - 8, cell_h - 8)
        comp = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
        arm_prefix = f"female_{arm}" if g == "female" else arm
        for layer_path in [
            os.path.join(HERO_DIR, f"{g}_{act}_{fi}.png"),
            os.path.join(ARMORS_DIR, f"{arm_prefix}_{act}_{fi}.png"),
            os.path.join(WEAPONS_DIR, f"{wpn}_{act}_{fi}.png"),
        ]:
            if os.path.exists(layer_path):
                comp.alpha_composite(Image.open(layer_path).convert("RGBA"))
        comp_sm = comp.resize((200, 200), Image.Resampling.LANCZOS)
        tile.alpha_composite(comp_sm, (6, 20))
        dt = ImageDraw.Draw(tile)
        dt.text((8, 6), f"{g} | {arm} + {wpn} ({act})", fill=(226, 232, 240, 255))
        sheet2.alpha_composite(tile, (i * cell_w + 4, r * cell_h + 36))

sheet2.save(os.path.join(SCRATCH_DIR, "audit_hd_armors_weapons.png"))

# 3. All 13 Mutations Assembled on Male/Female
mutations = [
    "wings", "fairy_wings", "tail", "booster", "shell", "crystals",
    "core", "horns", "spikes", "visor", "halo", "antennae", "claws"
]
BACK_LAYERS = {"wings", "fairy_wings", "tail", "booster", "shell", "crystals"}
sheet3 = Image.new("RGBA", (cell_w * 5, cell_h * 3 + 40), (9, 13, 22, 255))
d3 = ImageDraw.Draw(sheet3)
d3.text((15, 10), "240x240 HD 13 MUTATION PARTS ASSEMBLED", fill=(0, 240, 255, 255))

for idx, mut in enumerate(mutations):
    r = idx // 5
    c = idx % 5
    g = "male" if idx % 2 == 0 else "female"
    tile = create_bg_tile(cell_w - 8, cell_h - 8)
    comp = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    body_im = Image.open(os.path.join(HERO_DIR, f"{g}_idle_0.png")).convert("RGBA")
    mut_im = Image.open(os.path.join(MUT_DIR, f"{mut}_idle_0.png")).convert("RGBA")
    if mut in BACK_LAYERS:
        comp.alpha_composite(mut_im)
        comp.alpha_composite(body_im)
    else:
        comp.alpha_composite(body_im)
        comp.alpha_composite(mut_im)
    comp_sm = comp.resize((200, 200), Image.Resampling.LANCZOS)
    tile.alpha_composite(comp_sm, (6, 20))
    dt = ImageDraw.Draw(tile)
    dt.text((8, 6), f"{mut} ({g})", fill=(226, 232, 240, 255))
    sheet3.alpha_composite(tile, (c * cell_w + 4, r * cell_h + 36))

sheet3.save(os.path.join(SCRATCH_DIR, "audit_hd_13_mutations.png"))
print("Generated all 3 HD audit sheets!")
