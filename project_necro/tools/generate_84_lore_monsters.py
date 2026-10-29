# -*- coding: utf-8 -*-
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

MONSTERS_DIR = r"D:\workspace\GEMINI\project_necro\assets\monsters"
os.makedirs(MONSTERS_DIR, exist_ok=True)


def clamp(v):
    return max(0, min(255, int(v)))


def draw_bezier_tube(draw, p0, p1, p2, r0, r1, r2, fill_color, outline_color=None, steps=30):
    if outline_color:
        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            r = (1 - t) ** 2 * r0 + 2 * (1 - t) * t * r1 + t ** 2 * r2 + 2.2
            draw.ellipse([x - r, y - r, x + r, y + r], fill=outline_color)
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        r = (1 - t) ** 2 * r0 + 2 * (1 - t) * t * r1 + t ** 2 * r2
        if r > 0.4:
            draw.ellipse([x - r, y - r, x + r, y + r], fill=fill_color)


def finish_sprite(canvas_2x, target_size=(128, 128)):
    w, h = canvas_2x.size
    px = canvas_2x.load()
    bbox = canvas_2x.getbbox()
    if bbox:
        bx0, by0, bx1, by1 = bbox
        bw = max(1, bx1 - bx0)
        bh = max(1, by1 - by0)
        for y in range(by0, by1):
            ny = (y - by0) / bh
            for x in range(bx0, bx1):
                r, g, b, a = px[x, y]
                if a > 20:
                    nx = (x - bx0) / bw
                    light = (0.45 - nx) * 28 + (0.38 - ny) * 36
                    dither = 5 if ((x // 2 + y // 2) % 2 == 0) else -5
                    delta = light + dither
                    px[x, y] = (clamp(r + delta), clamp(g + delta), clamp(b + delta), a)

    img = canvas_2x.resize(target_size, Image.Resampling.NEAREST)
    alpha = img.split()[3]
    expanded = alpha.filter(ImageFilter.MaxFilter(5))
    out = Image.new("RGBA", target_size, (0, 0, 0, 0))
    out_px = out.load()
    src_px = img.load()
    exp_px = expanded.load()
    tw, th = target_size
    for y in range(th):
        for x in range(tw):
            if src_px[x, y][3] > 60:
                out_px[x, y] = src_px[x, y]
            elif exp_px[x, y] > 60:
                out_px[x, y] = (10, 7, 5, 255)
    return out


OL = (12, 8, 6, 255)


def draw_arachnid(d, col_main, col_hi, col_eye, is_boss=False, is_scorpion=False):
    # Giant spider / arachne / scorpion (facing right)
    cx, cy = 128, 142
    # Back abdomen
    d.ellipse([36, 86, 136, 172], fill=col_main, outline=OL, width=3)
    d.ellipse([50, 96, 118, 145], fill=col_hi)
    # Spots / rune markings on abdomen
    for sx, sy in [(68, 112), (92, 125), (75, 142)]:
        d.polygon([(sx, sy - 10), (sx + 10, sy), (sx, sy + 10), (sx - 10, sy)], fill=col_eye, outline=OL)

    if is_scorpion:
        # Curved segmented scorpion stinger tail arching over the back to the right
        draw_bezier_tube(d, (55, 105), (35, 25), (165, 38), 16, 12, 7, col_main, OL)
        d.polygon([(165, 38), (195, 28), (178, 56)], fill=col_eye, outline=OL)

    if is_boss and not is_scorpion:
        # Arachne Queen upper torso emerging from spider body
        d.polygon([(125, 118), (112, 62), (156, 62), (148, 118)], fill=(210, 195, 225, 255), outline=OL)
        d.ellipse([118, 26, 154, 62], fill=(230, 215, 245, 255), outline=OL, width=3)
        # Crown & glowing spider eyes
        d.polygon([(116, 30), (126, 10), (136, 26), (146, 8), (156, 30)], fill=col_eye, outline=OL)
        d.ellipse([138, 38, 148, 46], fill=col_eye)
        # Venom magic staff/claws
        draw_bezier_tube(d, (145, 76), (185, 58), (222, 82), 8, 6, 3, col_eye, OL)

    # Cephalothorax & fangs (facing right)
    d.ellipse([116, 108, 184, 166], fill=col_main, outline=OL, width=3)
    for ey in [122, 134, 144]:
        d.ellipse([162, ey, 174, ey + 8], fill=col_eye, outline=OL)
    # Mandibles / pincers
    draw_bezier_tube(d, (175, 138), (208, 125), (226, 148), 10, 8, 3, col_hi, OL)
    draw_bezier_tube(d, (175, 150), (208, 162), (224, 145), 9, 7, 3, col_hi, OL)

    # 8 Jointed legs
    leg_anchors = [(78, 148, 34, 98, 22, 212), (98, 152, 74, 104, 68, 220), (126, 152, 138, 102, 152, 222), (150, 148, 188, 104, 212, 216)]
    for x0, y0, xm, ym, x1, y1 in leg_anchors:
        draw_bezier_tube(d, (x0, y0), (xm, ym), (x1, y1), 8, 7, 3, col_main, OL)


def draw_mounted_knight_or_warrior(d, col_armor, col_hi, col_glow, weapon_type="greatsword", headless=False, mounted=False, crown=False):
    # Used for Dullahan Arthur, Sword King Baek Dohoon, Samurai/Ninja, Imperial Guard, Skeleton Soldier
    if mounted:
        # Armored skeletal/war steed facing right
        draw_bezier_tube(d, (55, 165), (32, 195), (42, 232), 10, 7, 5, col_armor, OL)
        draw_bezier_tube(d, (82, 168), (78, 200), (86, 232), 10, 7, 5, col_armor, OL)
        draw_bezier_tube(d, (152, 165), (175, 195), (188, 232), 10, 7, 5, col_armor, OL)
        draw_bezier_tube(d, (172, 162), (205, 185), (218, 224), 10, 7, 5, col_armor, OL)
        # Horse body & armored barding
        d.ellipse([48, 122, 188, 182], fill=col_armor, outline=OL, width=3)
        d.polygon([(60, 135), (178, 135), (192, 175), (45, 175)], fill=col_hi, outline=OL)
        # Horse neck & head facing right
        draw_bezier_tube(d, (165, 142), (195, 102), (215, 86), 20, 16, 12, col_armor, OL)
        d.polygon([(202, 72), (242, 92), (235, 114), (195, 104)], fill=col_hi, outline=OL)
        d.ellipse([214, 84, 224, 92], fill=col_glow)
        rider_y_offset = -34
    else:
        # Standing powerful legs facing right
        draw_bezier_tube(d, (92, 156), (82, 195), (74, 232), 14, 11, 9, col_armor, OL)
        draw_bezier_tube(d, (132, 156), (148, 195), (162, 232), 14, 11, 9, col_armor, OL)
        rider_y_offset = 0

    ty = 95 + rider_y_offset
    # Dynamic cape billowing left
    d.polygon([(95, ty), (24, ty + 35), (16, ty + 95), (88, ty + 72)], fill=(col_glow[0] // 2, col_glow[1] // 2, col_glow[2] // 2, 240), outline=OL)

    # Armored Torso
    d.polygon([(82, ty), (152, ty), (142, ty + 68), (92, ty + 68)], fill=col_armor, outline=OL)
    d.polygon([(92, ty + 8), (142, ty + 8), (134, ty + 56), (100, ty + 56)], fill=col_hi, outline=OL)
    # Glowing core on chest
    d.polygon([(117, ty + 18), (129, ty + 32), (117, ty + 46), (105, ty + 32)], fill=col_glow, outline=OL)

    # Pauldrons (Shoulder armor)
    d.ellipse([66, ty - 8, 106, ty + 26], fill=col_hi, outline=OL, width=3)
    d.ellipse([128, ty - 8, 168, ty + 26], fill=col_hi, outline=OL, width=3)

    if headless:
        # Dullahan neck flames + holding helmet under left arm
        for i in range(5):
            fx = 105 + i * 6
            d.polygon([(fx, ty), (fx + 6, ty - 28 - (i % 2) * 12), (fx + 12, ty)], fill=col_glow)
        # Held head at waist
        d.ellipse([62, ty + 28, 100, ty + 64], fill=col_hi, outline=OL, width=3)
        d.ellipse([82, ty + 42, 94, ty + 50], fill=col_glow)
    else:
        # Helmet / Head facing right
        d.ellipse([94, ty - 46, 144, ty + 4], fill=col_hi, outline=OL, width=3)
        # Visor slit glowing
        d.polygon([(114, ty - 26), (142, ty - 22), (138, ty - 12), (114, ty - 14)], fill=col_glow, outline=OL)
        if crown:
            d.polygon([(94, ty - 38), (104, ty - 64), (118, ty - 44), (132, ty - 66), (144, ty - 38)], fill=(255, 215, 0, 255), outline=OL)

    # Weapon in right hand extending forward
    if weapon_type == "greatsword":
        d.polygon([(152, ty + 28), (244, ty - 42), (250, ty - 26), (162, ty + 42)], fill=col_hi, outline=OL)
        d.line([(160, ty + 32), (242, ty - 34)], fill=col_glow, width=4)
    elif weapon_type == "dragon_sword":
        # Blue dragon aura katana
        draw_bezier_tube(d, (148, ty + 26), (198, ty + 5), (248, ty - 36), 7, 6, 2, (220, 250, 255, 255), OL)
        draw_bezier_tube(d, (135, ty + 40), (195, ty - 25), (246, ty - 45), 14, 10, 4, col_glow, None)
    elif weapon_type == "dual_axes":
        draw_bezier_tube(d, (148, ty + 32), (192, ty + 10), (226, ty - 18), 6, 6, 5, col_hi, OL)
        d.polygon([(195, ty - 32), (242, ty - 15), (232, ty + 28), (190, ty + 8)], fill=col_glow, outline=OL)
    elif weapon_type == "spear":
        d.line([(75, ty + 48), (246, ty - 12)], fill=col_hi, width=7)
        d.polygon([(220, ty - 18), (252, ty - 16), (230, ty + 6)], fill=col_glow, outline=OL)


def draw_colossus_or_mech(d, col_body, col_hi, col_core, is_tank_mech=False, is_volcanic=False):
    # Used for Obsidian Golem, Incheon Heavy Destroyer, Pyongyang Adamantium Colossus, Boris, Lava Behemoth
    # Massive legs
    d.rectangle([68, 165, 112, 236], fill=col_body, outline=OL, width=3)
    d.rectangle([138, 165, 182, 236], fill=col_body, outline=OL, width=3)
    if is_tank_mech:
        # Caterpillar treads at base
        d.rectangle([48, 198, 208, 240], fill=(45, 50, 58, 255), outline=OL, width=4)
        for wx in range(62, 198, 32):
            d.ellipse([wx, 206, wx + 24, 232], fill=col_hi, outline=OL, width=2)

    # Hulking torso
    d.polygon([(52, 64), (198, 64), (182, 174), (68, 174)], fill=col_body, outline=OL)
    d.polygon([(68, 78), (182, 78), (168, 158), (82, 158)], fill=col_hi, outline=OL)

    # Chest furnace / reactor core
    d.ellipse([102, 92, 154, 144], fill=OL)
    d.ellipse([108, 98, 148, 138], fill=col_core)
    d.ellipse([118, 108, 138, 128], fill=(255, 255, 255, 255))

    # Head / Turret visor
    d.rectangle([96, 28, 162, 68], fill=col_hi, outline=OL, width=3)
    d.rectangle([112, 42, 158, 54], fill=col_core, outline=OL)

    # Giant right arm / cannon / magma fist extending right
    draw_bezier_tube(d, (176, 86), (218, 105), (232, 152), 24, 26, 28, col_body, OL)
    d.ellipse([204, 128, 250, 176], fill=col_core if is_volcanic else col_hi, outline=OL, width=3)
    if is_tank_mech:
        # Shoulder twin missile pods / railgun
        d.rectangle([152, 22, 238, 52], fill=col_hi, outline=OL, width=3)
        d.ellipse([226, 26, 244, 48], fill=col_core, outline=OL)


def draw_dragon_or_wyvern(d, col_bone, col_wing, col_ice, is_boss=False):
    # Frost Bone Dragon, Wyvern, Black Dragon King
    # Giant bat/bone wing spreading upper left
    d.polygon([(115, 112), (18, 22), (88, 18), (142, 42), (138, 105)], fill=col_wing, outline=OL)
    draw_bezier_tube(d, (115, 112), (65, 58), (18, 22), 9, 7, 4, col_bone, OL)
    for wx, wy in [(48, 88), (76, 96), (102, 102)]:
        d.line([(72, 48), (wx, wy)], fill=col_bone, width=4)

    # Coiled tail & hind legs
    draw_bezier_tube(d, (88, 162), (34, 188), (18, 228), 14, 9, 3, col_bone, OL)
    # Ribcage & body
    d.ellipse([78, 108, 176, 178], fill=col_bone, outline=OL, width=3)
    for rx in range(92, 162, 14):
        d.arc([rx, 114, rx + 18, 170], start=270, end=90, fill=OL, width=3)
    d.ellipse([104, 124, 148, 158], fill=col_ice)

    # S-curved dragon neck & horned skull facing right
    draw_bezier_tube(d, (158, 128), (182, 78), (206, 56), 16, 14, 12, col_bone, OL)
    # Horned sweep back
    draw_bezier_tube(d, (196, 48), (162, 24), (132, 16), 8, 5, 2, col_ice, OL)
    # Dragon jaws open breathing frost/energy right
    d.polygon([(192, 42), (246, 54), (236, 74), (192, 68)], fill=col_bone, outline=OL)
    d.polygon([(196, 68), (240, 82), (232, 94), (192, 78)], fill=col_bone, outline=OL)
    d.ellipse([206, 48, 218, 58], fill=col_ice)
    if is_boss:
        # Breath beam at mouth
        d.polygon([(226, 62), (254, 48), (254, 88)], fill=col_ice)


def draw_kraken_or_sea_horror(d, col_body, col_hi, col_glow, is_boss=False):
    # Kraken Golem, Leviathan, Siren, Anglerfish, Jellyfish
    # Writhing tentacles radiating forward and down
    tentacles = [
        ((95, 155), (52, 195), (24, 228)),
        ((115, 162), (98, 208), (82, 242)),
        ((138, 165), (154, 212), (172, 242)),
        ((158, 158), (202, 196), (238, 222)),
        ((166, 138), (214, 148), (246, 172)),
        ((164, 118), (212, 102), (244, 116)),
    ]
    for p0, p1, p2 in tentacles:
        draw_bezier_tube(d, p0, p1, p2, 12 if is_boss else 9, 8, 3, col_body, OL)
        d.ellipse([p1[0] - 4, p1[1] - 4, p1[0] + 4, p1[1] + 4], fill=col_glow)

    # Mantle / Giant cephalopod head
    d.polygon([(58, 82), (148, 32), (186, 118), (88, 162)], fill=col_body, outline=OL)
    d.polygon([(74, 88), (140, 48), (170, 112), (98, 146)], fill=col_hi, outline=OL)
    # Glowing abyssal eyes
    d.ellipse([136, 98, 166, 126], fill=OL)
    d.ellipse([142, 104, 160, 120], fill=col_glow)
    if is_boss:
        # Abyssal crown / shell spikes
        for sx, sy in [(95, 52), (122, 38), (148, 28)]:
            d.polygon([(sx, sy), (sx + 10, sy - 22), (sx + 18, sy + 4)], fill=col_glow, outline=OL)


def draw_onmyoji_or_caster(d, col_robe, col_trim, col_magic, is_boss=False):
    # Abeno Onmyoji, Cultist, Talisman Shikigami, Alien Inquisitor, Belloc
    # Floating aura circle behind
    if is_boss:
        d.ellipse([44, 28, 212, 196], outline=col_magic, width=5)
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            rx = 128 + math.cos(rad) * 84
            ry = 112 + math.sin(rad) * 84
            d.rectangle([rx - 7, ry - 11, rx + 7, ry + 11], fill=(250, 235, 190, 255), outline=col_magic, width=2)

    # Flowing robes
    d.polygon([(92, 92), (164, 92), (188, 228), (68, 228)], fill=col_robe, outline=OL)
    d.polygon([(108, 96), (148, 96), (162, 224), (94, 224)], fill=col_trim, outline=OL)
    # Wide sleeves raised casting right
    d.polygon([(138, 102), (212, 84), (204, 148), (142, 142)], fill=col_robe, outline=OL)
    # Head / Tall Onmyoji Eboshi hat or hood
    d.ellipse([104, 52, 152, 98], fill=(225, 210, 200, 255), outline=OL, width=3)
    d.polygon([(106, 58), (128, 12), (150, 58)], fill=col_trim, outline=OL)
    d.ellipse([132, 68, 144, 78], fill=col_magic)
    # Floating magic orb / shikigami talismans in front (right)
    d.ellipse([196, 54, 242, 100], fill=col_magic, outline=OL, width=3)
    d.ellipse([208, 66, 230, 88], fill=(255, 255, 255, 255))


def draw_beast_or_wolf(d, col_fur, col_hi, col_eye, kind="wolf"):
    # Rat, Wolf, Hound, Boar, Bear, Yeti
    # Four legs lunging right
    draw_bezier_tube(d, (62, 152), (42, 188), (34, 224), 11, 8, 5, col_fur, OL)
    draw_bezier_tube(d, (88, 156), (78, 192), (74, 226), 11, 8, 5, col_fur, OL)
    draw_bezier_tube(d, (154, 152), (176, 188), (188, 226), 12, 9, 6, col_fur, OL)
    draw_bezier_tube(d, (174, 144), (212, 168), (232, 198), 12, 9, 6, col_fur, OL)
    # Tail
    draw_bezier_tube(d, (58, 136), (26, 118), (16, 94), 9, 6, 3, col_hi, OL)
    # Muscular body
    d.ellipse([54, 108, 188, 174], fill=col_fur, outline=OL, width=3)
    d.ellipse([72, 114, 168, 152], fill=col_hi)
    # Head & fangs facing right
    d.ellipse([156, 78, 222, 138], fill=col_fur, outline=OL, width=3)
    d.polygon([(198, 96), (248, 108), (238, 132), (194, 128)], fill=col_hi, outline=OL)
    # Ears / Horns / Tusks
    d.polygon([(164, 84), (154, 52), (182, 74)], fill=col_hi, outline=OL)
    d.polygon([(184, 82), (182, 48), (204, 74)], fill=col_hi, outline=OL)
    if kind == "boar":
        draw_bezier_tube(d, (218, 124), (238, 112), (246, 88), 6, 4, 2, (250, 245, 230, 255), OL)
    d.ellipse([198, 92, 210, 102], fill=col_eye)


def draw_drone_or_turret(d, col_metal, col_hi, col_laser):
    # Drone, Turret, Bomber, Plasma Probe
    # Glowing antigrav thrusters
    d.ellipse([82, 162, 174, 196], fill=col_laser)
    # Armored saucer / mech pod body
    d.ellipse([56, 84, 200, 168], fill=col_metal, outline=OL, width=3)
    d.ellipse([74, 94, 182, 146], fill=col_hi, outline=OL, width=2)
    # Twin forward plasma cannons pointing right
    d.rectangle([176, 112, 244, 128], fill=col_metal, outline=OL, width=3)
    d.rectangle([176, 134, 238, 148], fill=col_metal, outline=OL, width=3)
    d.ellipse([236, 110, 252, 130], fill=col_laser)
    # Central scanner eye
    d.ellipse([138, 104, 174, 138], fill=OL)
    d.ellipse([146, 112, 168, 130], fill=col_laser)


# Master table mapping (region 1..14, slot: 1,2,3,4,'named','boss') -> archetype & palette
REGION_MONSTER_SPECS = {
    1: {
        1: ("beast", (95, 102, 92, 255), (145, 158, 138, 255), (0, 255, 140, 255), "rat"),
        2: ("knight", (78, 98, 86, 255), (125, 152, 134, 255), (0, 255, 140, 255), "claws"),
        3: ("knight", (185, 190, 178, 255), (230, 235, 220, 255), (0, 255, 170, 255), "spear"),
        4: ("arachnid", (72, 118, 68, 255), (124, 188, 102, 255), (180, 255, 0, 255), False),
        "named": ("colossus", (112, 82, 68, 255), (168, 124, 98, 255), (255, 60, 80, 255), False),
        "boss": ("arachnid_boss", (68, 38, 88, 255), (138, 72, 175, 255), (0, 255, 140, 255), True),
    },
    2: {
        1: ("beast", (145, 175, 205, 255), (210, 235, 255, 255), (0, 240, 255, 255), "wolf"),
        2: ("knight", (175, 195, 215, 255), (225, 240, 255, 255), (0, 240, 255, 255), "greatsword"),
        3: ("caster", (62, 84, 128, 255), (120, 165, 220, 255), (0, 240, 255, 255), False),
        4: ("dragon", (88, 96, 112, 255), (138, 150, 172, 255), (0, 220, 255, 255), False),
        "named": ("colossus", (58, 68, 88, 255), (112, 132, 168, 255), (0, 240, 255, 255), False),
        "boss": ("dullahan_boss", (42, 46, 64, 255), (96, 108, 142, 255), (185, 65, 255, 255), True),
    },
    3: {
        1: ("knight", (92, 72, 58, 255), (152, 118, 92, 255), (255, 165, 40, 255), "spear"),
        2: ("beast", (118, 76, 52, 255), (178, 122, 84, 255), (255, 90, 30, 255), "wolf"),
        3: ("drone", (128, 104, 68, 255), (188, 154, 102, 255), (255, 180, 0, 255), False),
        4: ("caster", (88, 56, 78, 255), (148, 96, 132, 255), (255, 140, 40, 255), False),
        "named": ("knight", (68, 52, 44, 255), (138, 102, 78, 255), (255, 80, 40, 255), "dual_axes"),
        "boss": ("mech_boss", (135, 95, 52, 255), (205, 152, 88, 255), (255, 195, 0, 255), True),
    },
    4: {
        1: ("beast", (135, 175, 210, 255), (200, 235, 255, 255), (0, 240, 255, 255), "boar"),
        2: ("colossus", (195, 220, 245, 255), (235, 248, 255, 255), (0, 220, 255, 255), False),
        3: ("knight", (110, 155, 195, 255), (185, 225, 250, 255), (0, 240, 255, 255), "dragon_sword"),
        4: ("caster", (130, 200, 240, 255), (210, 245, 255, 255), (0, 255, 220, 255), False),
        "named": ("knight", (75, 130, 185, 255), (155, 210, 250, 255), (0, 240, 255, 255), "dragon_sword"),
        "boss": ("sword_king_boss", (48, 105, 165, 255), (175, 235, 255, 255), (0, 255, 230, 255), True),
    },
    5: {
        1: ("arachnid", (98, 102, 78, 255), (154, 162, 118, 255), (255, 60, 40, 255), False),
        2: ("knight", (72, 88, 68, 255), (122, 148, 112, 255), (255, 90, 30, 255), "spear"),
        3: ("drone", (112, 92, 64, 255), (172, 142, 98, 255), (255, 110, 20, 255), False),
        4: ("beast", (108, 68, 82, 255), (168, 108, 128, 255), (255, 40, 90, 255), "wolf"),
        "named": ("colossus", (88, 96, 104, 255), (148, 162, 175, 255), (255, 140, 0, 255), False),
        "boss": ("mech_boss", (76, 84, 96, 255), (148, 164, 184, 255), (255, 50, 50, 255), True),
    },
    6: {
        1: ("knight", (45, 42, 58, 255), (92, 86, 118, 255), (210, 60, 255, 255), "dragon_sword"),
        2: ("dragon", (52, 38, 68, 255), (108, 78, 138, 255), (255, 50, 110, 255), False),
        3: ("caster", (195, 180, 155, 255), (240, 228, 205, 255), (255, 45, 95, 255), False),
        4: ("knight", (118, 38, 52, 255), (188, 68, 88, 255), (200, 60, 255, 255), "greatsword"),
        "named": ("knight", (32, 28, 45, 255), (82, 72, 112, 255), (195, 50, 255, 255), "dragon_sword"),
        "boss": ("onmyoji_boss", (125, 28, 48, 255), (215, 185, 95, 255), (210, 65, 255, 255), True),
    },
    7: {
        1: ("knight", (48, 42, 38, 255), (112, 96, 78, 255), (255, 205, 0, 255), "spear"),
        2: ("knight", (135, 38, 42, 255), (205, 78, 68, 255), (255, 210, 0, 255), "dual_axes"),
        3: ("caster", (122, 24, 48, 255), (192, 52, 84, 255), (255, 40, 100, 255), False),
        4: ("colossus", (185, 142, 32, 255), (245, 210, 88, 255), (255, 40, 110, 255), False),
        "named": ("knight", (155, 28, 45, 255), (225, 165, 52, 255), (255, 215, 0, 255), "dual_axes"),
        "boss": ("dragon_boss", (58, 42, 28, 255), (225, 175, 42, 255), (255, 215, 0, 255), True),
    },
    8: {
        1: ("beast", (105, 128, 148, 255), (168, 198, 222, 255), (0, 240, 255, 255), "boar"),
        2: ("knight", (58, 96, 128, 255), (112, 164, 204, 255), (0, 255, 200, 255), "spear"),
        3: ("drone", (88, 148, 188, 255), (162, 218, 248, 255), (0, 245, 255, 255), False),
        4: ("colossus", (78, 112, 138, 255), (142, 184, 216, 255), (0, 240, 255, 255), False),
        "named": ("knight", (82, 118, 148, 255), (158, 198, 228, 255), (255, 195, 0, 255), "greatsword"),
        "boss": ("mech_boss", (92, 132, 168, 255), (185, 222, 248, 255), (0, 245, 255, 255), True),
    },
    9: {
        1: ("kraken", (38, 92, 118, 255), (78, 162, 192, 255), (0, 255, 210, 255), False),
        2: ("colossus", (64, 118, 128, 255), (118, 184, 196, 255), (0, 255, 190, 255), False),
        3: ("caster", (48, 112, 152, 255), (102, 188, 228, 255), (0, 245, 255, 255), False),
        4: ("kraken", (68, 52, 118, 255), (128, 98, 192, 255), (195, 70, 255, 255), False),
        "named": ("dragon", (32, 108, 148, 255), (84, 188, 228, 255), (0, 255, 220, 255), False),
        "boss": ("kraken_boss", (42, 78, 128, 255), (96, 168, 218, 255), (0, 255, 210, 255), True),
    },
    10: {
        1: ("caster", (135, 175, 215, 255), (205, 235, 255, 255), (0, 240, 255, 255), False),
        2: ("knight", (115, 148, 182, 255), (182, 215, 242, 255), (0, 245, 255, 255), "spear"),
        3: ("dragon", (165, 195, 225, 255), (225, 242, 255, 255), (0, 240, 255, 255), False),
        4: ("colossus", (142, 188, 228, 255), (212, 242, 255, 255), (0, 245, 255, 255), False),
        "named": ("colossus", (112, 152, 198, 255), (188, 225, 252, 255), (180, 90, 255, 255), False),
        "boss": ("dragon_boss", (185, 212, 238, 255), (235, 248, 255, 255), (0, 245, 255, 255), True),
    },
    11: {
        1: ("knight_mounted", (135, 165, 195, 255), (205, 228, 248, 255), (0, 240, 255, 255), "spear"),
        2: ("scorpion", (185, 132, 62, 255), (238, 188, 102, 255), (255, 210, 0, 255), False),
        3: ("knight", (175, 128, 48, 255), (235, 192, 92, 255), (255, 195, 0, 255), "greatsword"),
        4: ("caster", (205, 138, 52, 255), (252, 205, 108, 255), (255, 95, 30, 255), False),
        "named": ("knight", (168, 108, 42, 255), (238, 178, 84, 255), (255, 185, 0, 255), "dual_axes"),
        "boss": ("scorpion_boss", (195, 138, 52, 255), (248, 212, 118, 255), (255, 50, 110, 255), True),
    },
    12: {
        1: ("beast", (128, 48, 38, 255), (196, 88, 58, 255), (255, 140, 0, 255), "wolf"),
        2: ("dragon", (138, 52, 42, 255), (208, 96, 64, 255), (255, 120, 0, 255), False),
        3: ("caster", (168, 58, 32, 255), (238, 118, 52, 255), (255, 200, 0, 255), False),
        4: ("colossus", (96, 52, 44, 255), (178, 88, 58, 255), (255, 110, 0, 255), False),
        "named": ("dragon", (118, 32, 58, 255), (192, 68, 98, 255), (255, 80, 0, 255), False),
        "boss": ("volcanic_boss", (92, 38, 32, 255), (188, 72, 42, 255), (255, 165, 0, 255), True),
    },
    13: {
        1: ("knight", (168, 138, 58, 255), (232, 198, 102, 255), (0, 240, 255, 255), "spear"),
        2: ("drone", (175, 148, 64, 255), (238, 210, 118, 255), (0, 245, 255, 255), False),
        3: ("caster", (128, 88, 168, 255), (192, 148, 238, 255), (0, 245, 255, 255), False),
        4: ("colossus", (165, 132, 52, 255), (232, 195, 98, 255), (0, 245, 255, 255), False),
        "named": ("onmyoji_boss", (78, 128, 168, 255), (148, 212, 248, 255), (0, 255, 180, 255), True),
        "boss": ("mech_boss", (185, 148, 48, 255), (248, 215, 108, 255), (0, 245, 255, 255), True),
    },
    14: {
        1: ("knight", (128, 42, 92, 255), (208, 98, 168, 255), (255, 42, 109, 255), "greatsword"),
        2: ("knight", (58, 38, 88, 255), (128, 88, 188, 255), (0, 240, 255, 255), "dragon_sword"),
        3: ("drone", (138, 52, 108, 255), (218, 118, 188, 255), (255, 42, 109, 255), False),
        4: ("colossus", (98, 48, 128, 255), (178, 108, 218, 255), (255, 42, 109, 255), False),
        "named": ("knight", (158, 38, 78, 255), (238, 108, 158, 255), (255, 210, 0, 255), "dual_axes"),
        "boss": ("emperor_boss", (195, 165, 78, 255), (252, 238, 168, 255), (255, 42, 109, 255), True),
    },
}


def build_monster(r_id, slot, spec):
    kind, c1, c2, c3, extra = spec
    W, H = 256, 256
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)

    is_boss = slot == "boss"
    is_named = slot == "named"

    # Subtle ground shadow / aura for named & boss
    if is_boss or is_named:
        d.ellipse([36, 206, 220, 244], fill=(c3[0], c3[1], c3[2], 95))

    if kind == "arachnid":
        draw_arachnid(d, c1, c2, c3, is_boss=False, is_scorpion=False)
    elif kind == "arachnid_boss":
        draw_arachnid(d, c1, c2, c3, is_boss=True, is_scorpion=False)
    elif kind == "scorpion":
        draw_arachnid(d, c1, c2, c3, is_boss=False, is_scorpion=True)
    elif kind == "scorpion_boss":
        draw_arachnid(d, c1, c2, c3, is_boss=True, is_scorpion=True)
    elif kind == "dullahan_boss":
        draw_mounted_knight_or_warrior(d, c1, c2, c3, weapon_type="greatsword", headless=True, mounted=True)
    elif kind == "knight_mounted":
        draw_mounted_knight_or_warrior(d, c1, c2, c3, weapon_type=extra, headless=False, mounted=True)
    elif kind == "sword_king_boss":
        draw_mounted_knight_or_warrior(d, c1, c2, c3, weapon_type="dragon_sword", headless=False, mounted=False, crown=True)
    elif kind == "emperor_boss":
        # Cosmic Emperor with 6 floating diamond wings + royal greatsword + golden halo
        d.ellipse([48, 18, 208, 178], outline=c3, width=5)
        for wy in [48, 88, 128]:
            draw_bezier_tube(d, (96, wy + 20), (38, wy - 12), (14, wy - 24), 10, 7, 3, c2, OL)
            draw_bezier_tube(d, (144, wy + 20), (202, wy - 12), (236, wy - 24), 10, 7, 3, c2, OL)
        draw_mounted_knight_or_warrior(d, c1, c2, c3, weapon_type="greatsword", headless=False, mounted=False, crown=True)
    elif kind == "knight":
        draw_mounted_knight_or_warrior(d, c1, c2, c3, weapon_type=extra if isinstance(extra, str) else "greatsword", headless=False, mounted=False, crown=is_named)
    elif kind == "colossus":
        draw_colossus_or_mech(d, c1, c2, c3, is_tank_mech=False, is_volcanic=False)
    elif kind == "mech_boss":
        draw_colossus_or_mech(d, c1, c2, c3, is_tank_mech=True, is_volcanic=False)
    elif kind == "volcanic_boss":
        draw_colossus_or_mech(d, c1, c2, c3, is_tank_mech=False, is_volcanic=True)
    elif kind == "dragon":
        draw_dragon_or_wyvern(d, c1, c2, c3, is_boss=False)
    elif kind == "dragon_boss":
        draw_dragon_or_wyvern(d, c1, c2, c3, is_boss=True)
    elif kind == "kraken":
        draw_kraken_or_sea_horror(d, c1, c2, c3, is_boss=False)
    elif kind == "kraken_boss":
        draw_kraken_or_sea_horror(d, c1, c2, c3, is_boss=True)
    elif kind == "caster":
        draw_onmyoji_or_caster(d, c1, c2, c3, is_boss=False)
    elif kind == "onmyoji_boss":
        draw_onmyoji_or_caster(d, c1, c2, c3, is_boss=True)
    elif kind == "beast":
        draw_beast_or_wolf(d, c1, c2, c3, kind=extra if isinstance(extra, str) else "wolf")
    elif kind == "drone":
        draw_drone_or_turret(d, c1, c2, c3)

    out_size = (144, 144) if is_boss else ((132, 132) if is_named else (116, 116))
    out = finish_sprite(c, target_size=out_size)
    fn = f"m_{r_id}_{slot}.png"
    out_path = os.path.join(MONSTERS_DIR, fn)
    out.save(out_path)
    return fn, os.path.getsize(out_path)


if __name__ == "__main__":
    total = 0
    for r_id, slots in REGION_MONSTER_SPECS.items():
        for slot, spec in slots.items():
            fn, sz = build_monster(r_id, slot, spec)
            total += 1
    print(f"Successfully generated {total} lore-accurate pixel monster sprites in {MONSTERS_DIR}")
