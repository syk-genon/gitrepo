# -*- coding: utf-8 -*-
"""
Slice, chroma-key, defringe, and integrate canonical novel bosses and skills VFX.
- 8 Canonical Bosses from necromancer_bosses_spritesheet_1793173688288.jpg
- 8 Canonical Skills VFX from necromancer_skills_spritesheet_1793173693000.jpg
"""
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

P_BOSSES = r'C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f\necromancer_bosses_spritesheet_1793173688288.jpg'
P_SKILLS = r'C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f\necromancer_skills_spritesheet_1793173693000.jpg'

MONSTER_DIR = 'project_necro/assets/monsters'
SKILL_DIR = 'project_necro/assets/pixel_vfx/skills'
os.makedirs(MONSTER_DIR, exist_ok=True)
os.makedirs(SKILL_DIR, exist_ok=True)

def extract_cell(im, x, y, w, h, bg_thresh=25, is_skill=False):
    cell = im.crop((x, y, x + w, y + h))
    # Sample corner bg color
    corners = [cell.getpixel((0,0)), cell.getpixel((w-1,0)), cell.getpixel((0,h-1)), cell.getpixel((w-1,h-1)),
               cell.getpixel((2,2)), cell.getpixel((w-3,2)), cell.getpixel((2,h-3)), cell.getpixel((w-3,h-3))]
    bg_r = sum(c[0] for c in corners) / len(corners)
    bg_g = sum(c[1] for c in corners) / len(corners)
    bg_b = sum(c[2] for c in corners) / len(corners)

    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for cy in range(h):
        for cx in range(w):
            r, g, b = cell.getpixel((cx, cy))
            d = ((r - bg_r)**2 + (g - bg_g)**2 + (b - bg_b)**2)**0.5
            if d > bg_thresh:
                # Soft alpha for transition edge pixels to prevent harsh artifacts
                if d < bg_thresh + 8:
                    alpha = int(255 * ((d - bg_thresh) / 8.0))
                else:
                    alpha = 255
                out.putpixel((cx, cy), (r, g, b, alpha))

    bbox = out.getbbox()
    if not bbox:
        return out
    return out.crop(bbox)

def place_in_canvas(sprite, target_w=224, target_h=224, anchor='bottom'):
    sw, sh = sprite.size
    # Scale to fit inside canvas with 10% padding
    max_w = target_w - 16
    max_h = target_h - 16
    scale = min(max_w / sw, max_h / sh)
    nw = max(1, int(sw * scale))
    nh = max(1, int(sh * scale))
    resized = sprite.resize((nw, nh), Image.Resampling.NEAREST)

    canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    ox = (target_w - nw) // 2
    if anchor == 'bottom':
        oy = target_h - nh - 4
    elif anchor == 'center':
        oy = (target_h - nh) // 2
    else:
        oy = 4
    canvas.paste(resized, (ox, oy), resized)
    return canvas

# 1. Process 8 Bosses
im_bosses = Image.open(P_BOSSES).convert('RGB')
CELL_W = 344
CELL_H = 384

boss_mappings = [
    # (row, col, target_filenames, anchor, name)
    (0, 0, ['m_1_boss.png'], 'bottom', '1지역 아라크네 나이트 (Arachne Knight)'),
    (0, 1, ['m_2_boss.png', 'm_2_named.png'], 'bottom', '2지역 듀라한 아서 (Dullahan Arthur)'),
    (0, 2, ['m_4_boss.png'], 'bottom', '4지역 검왕 백도훈 (Sword King Baek Do-hoon)'),
    (0, 3, ['m_6_named.png'], 'bottom', '6지역 그림자 암살자 카게미츠 (Kagemitsu)'),
    (1, 0, ['m_9_boss.png'], 'center', '9지역 크라켄 골렘 (Kraken Golem)'),
    (1, 1, ['m_10_boss.png'], 'center', '10지역 서리 본 드래곤 (Frost Bone Dragon)'),
    (1, 2, ['m_12_boss.png'], 'bottom', '12지역 라바 베히모스 (Lava Behemoth)'),
    (1, 3, ['m_14_boss.png'], 'center', '14지역 무감정의 황제 (Emperor of Indifference)'),
]

print("=== SLICING CANONICAL NOVEL BOSSES ===")
for r, c, filenames, anchor, bname in boss_mappings:
    x = c * CELL_W
    y = r * CELL_H
    sprite = extract_cell(im_bosses, x, y, CELL_W, CELL_H, bg_thresh=26)
    final_canvas = place_in_canvas(sprite, 224, 224, anchor=anchor)
    for fn in filenames:
        out_path = os.path.join(MONSTER_DIR, fn)
        final_canvas.save(out_path, 'PNG')
        print(f"Saved {bname} -> {out_path} (size: {final_canvas.size})")

# 2. Process 8 Skills VFX
im_skills = Image.open(P_SKILLS).convert('RGB')

skills_mappings = [
    # (row, col, target_filenames, name)
    (0, 0, ['vfx_necro_2.png'], '시체 폭발 (Corpse Explosion)'),
    (0, 1, ['vfx_necro_ult.png', 'vfx_cryo_ult.png'], '진(眞) 블리자드 (Absolute Blizzard)'),
    (0, 2, ['vfx_necro_1.png', 'vfx_necro_3.png'], '관통 뼈창 & 해골 군단 (Bone Spear & Skeletons)'),
    (0, 3, ['vfx_assassin_ult.png', 'vfx_necro_5.png'], '그림자 군세 (Shadow Horde)'),
    (1, 0, ['vfx_guard_1.png', 'vfx_guard_ult.png', 'vfx_guard_4.png'], '아이기스 절대 방벽 (Aegis Citadel Wall)'),
    (1, 1, ['vfx_snip_1.png', 'vfx_snip_2.png', 'vfx_snip_ult.png'], '차원 관통 저격 & 매의 눈 (Dimensional Railgun)'),
    (1, 2, ['vfx_storm_2.png', 'vfx_storm_3.png', 'vfx_storm_ult.png'], '과부하 볼케이노 & 체인 라이트닝 (Overload Volcano)'),
    (1, 3, ['vfx_priest_1.png', 'vfx_priest_ult.png', 'vfx_priest_5.png'], '대성역 & 천벌의 빛기둥 (Celestial Sanctuary)'),
]

print("\n=== SLICING CANONICAL NOVEL SKILLS VFX ===")
for r, c, filenames, sname in skills_mappings:
    x = c * CELL_W
    y = r * CELL_H
    sprite = extract_cell(im_skills, x, y, CELL_W, CELL_H, bg_thresh=22, is_skill=True)
    final_canvas = place_in_canvas(sprite, 128, 128, anchor='center')
    for fn in filenames:
        out_path = os.path.join(SKILL_DIR, fn)
        final_canvas.save(out_path, 'PNG')
        print(f"Saved {sname} -> {out_path} (size: {final_canvas.size})")

print("\nAll canonical novel bosses and skills VFX successfully integrated!")
