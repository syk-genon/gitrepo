# -*- coding: utf-8 -*-
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"D:\workspace\GEMINI\project_necro"
GATES_DIR = os.path.join(BASE_DIR, "assets", "ui", "gates")
os.makedirs(GATES_DIR, exist_ok=True)


def clamp(v):
    return max(0, min(255, int(v)))


def draw_bezier_tube(draw, p0, p1, p2, r0, r1, r2, fill_color, outline_color=None, steps=36):
    if outline_color:
        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            r = (1 - t) ** 2 * r0 + 2 * (1 - t) * t * r1 + t ** 2 * r2 + 2.5
            draw.ellipse([x - r, y - r, x + r, y + r], fill=outline_color)
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        r = (1 - t) ** 2 * r0 + 2 * (1 - t) * t * r1 + t ** 2 * r2
        if r > 0.5:
            draw.ellipse([x - r, y - r, x + r, y + r], fill=fill_color)


def apply_16bit_shading_and_outline(canvas_2x, target_size=(160, 180)):
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
                    light = (0.42 - nx) * 32 + (0.38 - ny) * 38
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


GATE_SPECS = [
    {
        "id": "iron",
        "filename": "gate_iron.png",
        "frame_main": (105, 112, 122, 255),
        "frame_hi": (165, 175, 188, 255),
        "frame_dark": (52, 56, 64, 255),
        "portal_outer": (0, 185, 130, 235),
        "portal_inner": (120, 255, 210, 255),
        "crest_col": (190, 200, 215, 255),
        "style": "arch_iron"
    },
    {
        "id": "bronze",
        "filename": "gate_bronze.png",
        "frame_main": (175, 108, 56, 255),
        "frame_hi": (235, 165, 100, 255),
        "frame_dark": (92, 50, 22, 255),
        "portal_outer": (40, 195, 150, 235),
        "portal_inner": (160, 255, 220, 255),
        "crest_col": (245, 185, 110, 255),
        "style": "arch_bronze"
    },
    {
        "id": "silver",
        "filename": "gate_silver.png",
        "frame_main": (175, 195, 218, 255),
        "frame_hi": (235, 245, 255, 255),
        "frame_dark": (85, 102, 125, 255),
        "portal_outer": (0, 195, 255, 240),
        "portal_inner": (190, 245, 255, 255),
        "crest_col": (240, 250, 255, 255),
        "style": "arch_silver"
    },
    {
        "id": "gold",
        "filename": "gate_gold.png",
        "frame_main": (230, 175, 35, 255),
        "frame_hi": (255, 238, 120, 255),
        "frame_dark": (128, 84, 12, 255),
        "portal_outer": (255, 165, 0, 240),
        "portal_inner": (255, 245, 170, 255),
        "crest_col": (255, 235, 95, 255),
        "style": "arch_gold"
    },
    {
        "id": "platinum",
        "filename": "gate_platinum.png",
        "frame_main": (160, 215, 235, 255),
        "frame_hi": (235, 252, 255, 255),
        "frame_dark": (65, 115, 145, 255),
        "portal_outer": (165, 65, 255, 240),
        "portal_inner": (235, 190, 255, 255),
        "crest_col": (0, 245, 255, 255),
        "style": "arch_platinum"
    },
    {
        "id": "diamond",
        "filename": "gate_diamond.png",
        "frame_main": (110, 225, 255, 255),
        "frame_hi": (235, 255, 255, 255),
        "frame_dark": (45, 95, 155, 255),
        "portal_outer": (255, 45, 135, 245),
        "portal_inner": (255, 225, 250, 255),
        "crest_col": (255, 230, 90, 255),
        "style": "arch_diamond"
    }
]


def generate_gate_sprite(spec):
    W, H = 320, 360
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    cx, cy = 160, 190
    OL = (12, 8, 6, 255)

    fm = spec["frame_main"]
    fh = spec["frame_hi"]
    fd = spec["frame_dark"]
    po = spec["portal_outer"]
    pi = spec["portal_inner"]
    cr = spec["crest_col"]
    st = spec["style"]

    # 1. Outer ambient aura / energy wisps
    for r in range(138, 95, -8):
        alpha = clamp(35 + (138 - r) * 2)
        d.ellipse([cx - r, cy - r - 10, cx + r, cy + r - 10], fill=(po[0], po[1], po[2], alpha))

    # 2. Stepped stone/metal pedestal base
    d.rectangle([34, 308, 286, 336], fill=fd, outline=OL, width=3)
    d.rectangle([42, 312, 278, 326], fill=fm)
    d.rectangle([22, 328, 298, 348], fill=fd, outline=OL, width=3)
    d.rectangle([30, 332, 290, 342], fill=fh)

    # 3. Inner dimensional vortex / portal abyss
    d.polygon([(76, 308), (76, 145), (105, 86), (160, 66), (215, 86), (244, 145), (244, 308)], fill=(12, 10, 22, 255), outline=OL)

    # Swirling vortex rings inside the gate
    for ring in range(6, 0, -1):
        rx = ring * 13
        ry = ring * 18
        col = po if ring % 2 == 0 else pi
        alpha = clamp(120 + (6 - ring) * 22)
        d.ellipse([cx - rx, cy - ry + 8, cx + rx, cy + ry + 8], fill=(col[0], col[1], col[2], alpha))

    # Spiral energy streams inside portal
    random.seed(hash(spec["id"]))
    for i in range(10):
        ang0 = i * (math.pi / 5)
        x0 = cx + math.cos(ang0) * 68
        y0 = cy + 8 + math.sin(ang0) * 92
        xm = cx + math.cos(ang0 + 0.7) * 36
        ym = cy + 8 + math.sin(ang0 + 0.7) * 48
        draw_bezier_tube(d, (x0, y0), (xm, ym), (cx, cy + 8), 5, 3, 1, pi, po)

    # 4. Left & Right heavy pillars
    for px_left in [52, 232]:
        d.rectangle([px_left, 128, px_left + 36, 310], fill=fm, outline=OL, width=3)
        d.rectangle([px_left + 6, 134, px_left + 16, 304], fill=fh)
        d.rectangle([px_left + 22, 134, px_left + 30, 304], fill=fd)
        # Pillar runes / rivets
        for ry in range(152, 298, 34):
            d.rectangle([px_left + 8, ry, px_left + 28, ry + 14], fill=po, outline=OL, width=2)
            d.ellipse([px_left + 13, ry + 3, px_left + 23, ry + 11], fill=pi)

    # 5. Grand Archway top (Bezier curve arch)
    draw_bezier_tube(d, (68, 135), (160, 18), (252, 135), 22, 26, 22, fm, OL, steps=45)
    draw_bezier_tube(d, (72, 135), (160, 28), (248, 135), 10, 12, 10, fh, None, steps=45)

    # 6. Tier-specific crowns, horns, wings, or crystal spires
    if st in ("arch_silver", "arch_gold", "arch_platinum", "arch_diamond"):
        # Side wings / spires
        draw_bezier_tube(d, (54, 135), (18, 85), (28, 38), 12, 8, 3, fh, OL)
        draw_bezier_tube(d, (266, 135), (302, 85), (292, 38), 12, 8, 3, fh, OL)
    if st in ("arch_gold", "arch_platinum", "arch_diamond"):
        # Upper floating runes / spires
        draw_bezier_tube(d, (88, 92), (52, 42), (66, 14), 10, 6, 2, cr, OL)
        draw_bezier_tube(d, (232, 92), (268, 42), (254, 14), 10, 6, 2, cr, OL)
    if st == "arch_diamond":
        # Giant floating diamond prism crown at the apex + cosmic crystal shards
        for sx, sy in [(26, 175), (294, 175), (34, 245), (286, 245)]:
            d.polygon([(sx, sy - 22), (sx + 12, sy), (sx, sy + 22), (sx - 12, sy)], fill=pi, outline=OL)
            d.polygon([(sx, sy - 14), (sx + 6, sy), (sx, sy + 14), (sx - 6, sy)], fill=po)

    # 7. Keystone Crest at top center of arch (cx=160, y=58)
    d.polygon([(cx, 20), (cx + 28, 56), (cx, 92), (cx - 28, 56)], fill=cr, outline=OL)
    d.polygon([(cx, 30), (cx + 18, 56), (cx, 82), (cx - 18, 56)], fill=po, outline=OL)
    d.ellipse([cx - 8, 48, cx + 8, 64], fill=pi)

    # 8. Half-open Heavy Gate Doors with iron bars / runes
    # Left door leaf slightly ajar revealing the glowing portal
    d.polygon([(86, 140), (124, 152), (124, 304), (86, 308)], fill=fd, outline=OL)
    d.polygon([(234, 140), (196, 152), (196, 304), (234, 308)], fill=fd, outline=OL)
    for dy in range(175, 295, 36):
        d.line([(88, dy), (122, dy + 6)], fill=fh, width=4)
        d.line([(232, dy), (198, dy + 6)], fill=fh, width=4)

    out = apply_16bit_shading_and_outline(c, target_size=(160, 180))
    out_path = os.path.join(GATES_DIR, spec["filename"])
    out.save(out_path)
    return out_path, os.path.getsize(out_path)


if __name__ == "__main__":
    for s in GATE_SPECS:
        p, sz = generate_gate_sprite(s)
        print(f"Generated {os.path.basename(p)} ({sz:,} bytes)")
