# -*- coding: utf-8 -*-
import os, sys, math
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

REGIONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\ui\regions"
os.makedirs(REGIONS_DIR, exist_ok=True)

ARTIFACT_DIR = r"C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f"
USER_SAMPLE_IMG = r"C:\Users\exbxda13\Downloads\Gemini_Generated_Image_ve9fa4ve9fa4ve9f.png"

MASTER_TOWN_1 = Image.open(os.path.join(ARTIFACT_DIR, "town_bg_1_1793147727296.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.NEAREST)
MASTER_TOWN_2 = Image.open(os.path.join(ARTIFACT_DIR, "town_bg_2_1793147728821.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.NEAREST)
MASTER_TOWN_3 = Image.open(os.path.join(ARTIFACT_DIR, "town_bg_3_1793147731093.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.NEAREST)
MASTER_WORLD1 = MASTER_TOWN_3.copy()

MASTER_BATTLE_1 = Image.open(os.path.join(ARTIFACT_DIR, "battle_bg_1_1793147708706.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.NEAREST)
MASTER_BATTLE_2 = Image.open(os.path.join(ARTIFACT_DIR, "battle_bg_2_1793147709966.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.NEAREST)
MASTER_BATTLE_3 = Image.open(os.path.join(ARTIFACT_DIR, "battle_bg_3_1793147711700.jpg")).convert("RGBA").resize((640, 360), Image.Resampling.NEAREST)


def clamp(v):
    return max(0, min(255, int(v)))


def is_foliage_or_sway_pixel(r, g, b, y, h):
    """Detects tree leaves, bushes, grass tufts, lanterns, or glowing crystals/flames for GIMP/Krita layer masking."""
    # Green foliage / bushes / pine needles
    if g > r + 14 and g > b + 10 and g > 40:
        return True
    # Glowing cyan/emerald crystals, aurora, or magic flames
    if (g > 180 and b > 150 and r < 120) or (r > 200 and g > 100 and b < 70 and y > h * 0.25):
        return True
    # Foreground grass band at the bottom 12%
    if y > h * 0.86 and g > r:
        return True
    return False


def create_gimp_4frame_sway_sequence(base_img, r_mod=1.0, g_mod=1.0, b_mod=1.0, r_add=0, g_add=0, b_add=0, flip_x=False):
    """
    Applies GIMP/Krita style color grading on pixel-art grid (320x180), then separates the Foliage/Canopy/Grass/Lantern layer
    and applies a 4-frame pixel wind-shear cycle:
      Frame 0: 0px (기본 위치)
      Frame 1: +1px right bend (오른쪽 살짝 휨)
      Frame 2: +2px max right bend + 1px rustle (최대 휨)
      Frame 3: +1px return bend (돌아오는 중간 단계)
    """
    work = base_img.copy()
    if flip_x:
        work = work.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    # Work at 320x180 pixel grid so 1px shift = 2px crisp retro pixel block at 640x360
    W, H = 320, 180
    small = work.resize((W, H), Image.Resampling.NEAREST)
    spx = small.load()

    # Color grade
    for y in range(H):
        for x in range(W):
            r, g, b, a = spx[x, y]
            spx[x, y] = (
                clamp(r * r_mod + r_add),
                clamp(g * g_mod + g_add),
                clamp(b * b_mod + b_add),
                255,
            )

    # Build Foliage/Sway Mask (True where tree canopy / bushes / grass / lanterns are)
    mask = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            r, g, b, _ = spx[x, y]
            if is_foliage_or_sway_pixel(r, g, b, y, H):
                mask[y][x] = True

    # Dilate mask by 1px so the black pixel outline of the tree leaves/bushes moves TOGETHER with the leaves!
    dilated_mask = [[False] * W for _ in range(H)]
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if mask[y][x] or mask[y - 1][x] or mask[y + 1][x] or mask[y][x - 1] or mask[y][x + 1]:
                dilated_mask[y][x] = True

    sway_shifts = [0, 1, 2, 1]
    frames = []

    for f_idx, dx_shift in enumerate(sway_shifts):
        if dx_shift == 0:
            frames.append(small.resize((640, 360), Image.Resampling.NEAREST))
            continue

        frame_im = small.copy()
        fpx = frame_im.load()

        for y in range(2, H - 2):
            # Vertical wind wave factor: upper canopy bends full dx_shift, lower bush bends half
            local_dx = dx_shift
            if dx_shift == 2 and (y // 6) % 2 == 0:
                local_dx = 2
            elif dx_shift == 2:
                local_dx = 1

            for x in range(W - 1, local_dx, -1):
                if dilated_mask[y][x - local_dx]:
                    fpx[x, y] = spx[x - local_dx, y]

        frames.append(frame_im.resize((640, 360), Image.Resampling.NEAREST))

    return frames


def build_seamless_cloud_strip():
    """Creates a transparent 640x140 pixel-art cloud & wind-particle layer for continuous 1px horizontal scrolling."""
    W, H = 320, 70
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = im.load()
    OL = (10, 7, 5, 220)
    C_HI = (248, 252, 255, 235)
    C_SHADE = (190, 212, 238, 225)

    clouds = [(38, 18, 22, 7), (124, 28, 16, 5), (218, 15, 26, 8), (288, 25, 14, 5)]
    for cx, cy, rx, ry in clouds:
        for dy in range(-ry - 1, ry + 2):
            for dx in range(-rx - 1, rx + 2):
                # Bumpy retro cloud silhouette
                bump = math.sin(dx * 0.45) * 1.5
                dist = (dx * dx) / ((rx + 1) ** 2) + ((dy - bump) ** 2) / ((ry + 1) ** 2)
                if dist <= 1.0:
                    x = (cx + dx) % W
                    y = cy + dy
                    if 0 <= y < H:
                        px[x, y] = OL
        for dy in range(-ry, ry + 1):
            for dx in range(-rx, rx + 1):
                bump = math.sin(dx * 0.45) * 1.5
                dist = (dx * dx) / (rx * rx) + ((dy - bump) ** 2) / (ry * ry)
                if dist <= 1.0:
                    x = (cx + dx) % W
                    y = cy + dy
                    if 0 <= y < H:
                        px[x, y] = C_SHADE if dy >= ry * 0.35 else C_HI

    return im.resize((640, 140), Image.Resampling.NEAREST)


def build_4frame_foliage_overlay():
    """
    Creates a dedicated 4-frame transparent pixel-art Tree Canopy & Grass Tuft layer (640x360)
    following the exact 4-frame retro cycle:
      Frame 0: 기본 위치 (dx=0)
      Frame 1: 오른쪽 살짝 휨 (dx=+1px)
      Frame 2: 최대 휨 (dx=+2px, dy=+1px)
      Frame 3: 돌아오는 중간 단계 (dx=+1px)
    """
    W, H = 320, 180
    # Extract real pixel-art tree canopy clusters from MASTER_TOWN_3 and add crisp pixel grass blades at bottom
    src = MASTER_TOWN_3.resize((W, H), Image.Resampling.NEAREST)
    spx = src.load()

    base_foliage = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bpx = base_foliage.load()

    # 1) Copy real pixel-art green tree leaves from MASTER_TOWN_3 and place canopy clusters in top-left & top-right corners
    for y in range(15, 95):
        for x in range(0, 145):
            r, g, b, a = spx[x, y]
            if g > r + 12 and g > b + 8 and g > 38:
                # Place on left canopy overhang
                tx, ty = int(x * 0.55), int(y * 0.75)
                if 0 <= tx < W and 0 <= ty < H:
                    bpx[tx, ty] = (r, g, b, 255)
                # Mirror on right canopy overhang
                rx_pos = W - 1 - tx
                if 0 <= rx_pos < W and 0 <= ty < H:
                    bpx[rx_pos, ty] = (r, g, b, 255)

    # 2) Add crisp 16-bit pixel art grass tufts along the bottom ground border (y = 162..179)
    G_DARK = (24, 68, 34, 255)
    G_MID = (46, 124, 52, 255)
    G_HI = (98, 186, 72, 255)
    tuft_xs = [8, 18, 29, 44, 62, 78, 95, 225, 242, 258, 274, 290, 304, 312]
    for tx in tuft_xs:
        for blade in (-3, 0, 3):
            bx = tx + blade
            bh = 7 + ((tx + blade) % 5)
            for by in range(bh):
                py = H - 1 - by
                px_x = bx + (by // 3) * (1 if blade >= 0 else -1)
                if 0 <= px_x < W and 0 <= py < H:
                    col = G_HI if by >= bh - 2 else (G_MID if by >= 3 else G_DARK)
                    bpx[px_x, py] = col

    # Add 1px retro black outline around all non-transparent foliage pixels
    outlined = base_foliage.copy()
    opx = outlined.load()
    OL = (10, 7, 5, 240)
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if bpx[x, y][3] == 0:
                if (
                    bpx[x - 1, y][3] > 0
                    or bpx[x + 1, y][3] > 0
                    or bpx[x, y - 1][3] > 0
                    or bpx[x, y + 1][3] > 0
                ):
                    opx[x, y] = OL

    # Generate the 4 frames: [0, 1, 2, 1] wind bend
    sway_shifts = [(0, 0), (1, 0), (2, 1), (1, 0)]
    frames = []
    for f_idx, (dx_max, dy_max) in enumerate(sway_shifts):
        fim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fpx = fim.load()
        for y in range(H):
            # Leaves near branch tips / grass tips bend more than roots
            if y < 90:
                factor = min(1.0, y / 45.0)
            else:
                factor = min(1.0, (H - y) / 10.0)
            dx = int(round(dx_max * factor))
            dy = int(round(dy_max * factor)) if y < 90 else 0
            for x in range(W):
                c = opx[x, y]
                if c[3] > 0:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        fpx[nx, ny] = c
        frames.append(fim.resize((640, 360), Image.Resampling.NEAREST))
    return frames


REGION_CONFIGS = {
    # Region 1 uses the user's exact WORLD 1-1 pixel art village master for Town & Joseon Megacity for Battle!
    1:  (MASTER_WORLD1, MASTER_BATTLE_3, 1.00, 1.00, 1.00, 0, 0, 0, False),
    2:  (MASTER_TOWN_1, MASTER_BATTLE_1, 0.92, 1.05, 1.18, 0, 8, 20, False),
    3:  (MASTER_TOWN_2, MASTER_BATTLE_2, 1.08, 0.98, 0.88, 10, 0, -5, False),
    4:  (MASTER_TOWN_1, MASTER_BATTLE_1, 0.88, 1.12, 1.28, 15, 22, 38, True),
    5:  (MASTER_TOWN_2, MASTER_BATTLE_2, 1.05, 0.95, 0.82, 8, 0, -10, True),
    6:  (MASTER_TOWN_3, MASTER_BATTLE_3, 1.15, 0.88, 1.12, 18, -8, 15, False),
    7:  (MASTER_TOWN_2, MASTER_BATTLE_3, 1.22, 1.05, 0.82, 22, 10, -10, True),
    8:  (MASTER_TOWN_1, MASTER_BATTLE_1, 0.78, 1.08, 1.28, -8, 12, 32, False),
    9:  (MASTER_TOWN_3, MASTER_BATTLE_1, 0.72, 1.15, 1.32, -12, 18, 38, True),
    10: (MASTER_TOWN_1, MASTER_BATTLE_1, 0.95, 1.08, 1.25, 12, 18, 32, True),
    11: (MASTER_WORLD1, MASTER_BATTLE_2, 1.22, 1.08, 0.78, 28, 12, -20, False),
    12: (MASTER_TOWN_2, MASTER_BATTLE_2, 1.32, 0.82, 0.72, 35, -10, -18, True),
    13: (MASTER_TOWN_3, MASTER_BATTLE_3, 1.18, 1.12, 0.88, 20, 15, 0, False),
    14: (MASTER_TOWN_3, MASTER_BATTLE_2, 1.18, 0.85, 1.32, 20, -8, 35, False),
}

if __name__ == "__main__":
    cloud_strip = build_seamless_cloud_strip()
    cloud_strip.save(os.path.join(REGIONS_DIR, "clouds_strip.png"))
    print("Saved seamless scrolling cloud strip: clouds_strip.png")

    foliage_frames = build_4frame_foliage_overlay()
    for f_idx, f_im in enumerate(foliage_frames):
        f_im.save(os.path.join(REGIONS_DIR, f"foliage_overlay_f{f_idx}.png"))
    print("Saved 4-frame transparent foliage/grass layer: foliage_overlay_f0..3.png")

    for r_id, (t_master, b_master, rm, gm, bm, ra, ga, ba, flip) in REGION_CONFIGS.items():
        t_frames = create_gimp_4frame_sway_sequence(t_master, rm, gm, bm, ra, ga, ba, flip_x=flip)
        b_frames = create_gimp_4frame_sway_sequence(b_master, rm, gm, bm, ra, ga, ba, flip_x=flip)

        for f_idx in range(4):
            t_frames[f_idx].save(os.path.join(REGIONS_DIR, f"town_bg_{r_id}_f{f_idx}.png"))
            b_frames[f_idx].save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}_f{f_idx}.png"))

        t_frames[0].save(os.path.join(REGIONS_DIR, f"town_bg_{r_id}.png"))
        b_frames[0].save(os.path.join(REGIONS_DIR, f"battle_bg_{r_id}.png"))
        print(f"Region {r_id:02d}: generated 4-frame GIMP-warped town_bg_{r_id}_f0..3.png & battle_bg_{r_id}_f0..3.png")
