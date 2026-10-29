# -*- coding: utf-8 -*-
"""
Build 100% pure wild nature panoramic battle backgrounds (2400x360) and 
nature prop parallax layers (2400x360) for all 14 regions from the new master sheets.
"""
import os
import sys
from PIL import Image, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

P_SHEET_1 = r'C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f\regions_1_to_4_nature_stages_spritesheet_1793174209123.jpg'
P_SHEET_2 = r'C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f\regions_5_8_pixel_nature_grid_1793174220514.jpg'
P_SHEET_3 = r'C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f\regions_9_to_14_pixel_art_spritesheet_clean_1793174303649.jpg'
P_PROPS = r'C:\Users\exbxda13\.gemini\antigravity-cli\brain\1c1fbbe7-1183-4922-91fc-f7bcdcaf125f\nature_props_spritesheet_png_1793174245523.jpg'

OUTPUT_DIR = 'project_necro/assets/ui/regions'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Extract 12 Nature Props from Sheet 4
im_props = Image.open(P_PROPS).convert('RGB')
PW = 1200 // 4  # 300
PH = 896 // 3   # 298

def extract_prop(r, c, bg_thresh=26):
    cell = im_props.crop((c * PW, r * PH, (c + 1) * PW, (r + 1) * PH))
    w, h = cell.size
    corners = [cell.getpixel((4, 4)), cell.getpixel((w - 5, 4)), cell.getpixel((4, h - 5)), cell.getpixel((w - 5, h - 5))]
    bg_r = sum(p[0] for p in corners) / 4.0
    bg_g = sum(p[1] for p in corners) / 4.0
    bg_b = sum(p[2] for p in corners) / 4.0

    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            pr, pg, pb = cell.getpixel((x, y))
            d = ((pr - bg_r)**2 + (pg - bg_g)**2 + (pb - bg_b)**2)**0.5
            if d > bg_thresh:
                if d < bg_thresh + 6:
                    alpha = int(255 * ((d - bg_thresh) / 6.0))
                else:
                    alpha = 255
                out.putpixel((x, y), (pr, pg, pb, alpha))

    bbox = out.getbbox()
    if bbox:
        return out.crop(bbox)
    return out

print("Extracting 12 nature props...")
PROPS = {}
# Row 0: Canopy props
PROPS['canopy_stalactites'] = extract_prop(0, 0) # 석회 종유석
PROPS['canopy_snow_pine']   = extract_prop(0, 1) # 눈솔가지 & 고드름
PROPS['canopy_red_maple']   = extract_prop(0, 2) # 단풍나무 가지
PROPS['canopy_jungle_vines'] = extract_prop(0, 3) # 밀림 덩굴

# Row 1: Ground flora & reef
PROPS['ground_mushrooms']   = extract_prop(1, 0) # 발광 버섯 바위
PROPS['ground_tidal_reef']  = extract_prop(1, 1) # 해안 갯바위 따개비
PROPS['ground_bamboo_stones'] = extract_prop(1, 2) # 대나무 죽순 하천석
PROPS['ground_coral_reef']  = extract_prop(1, 3) # 발광 심해 산호

# Row 2: Elemental ground crystals & rocks
PROPS['ground_blue_ice']    = extract_prop(2, 0) # 청빙 빙하 수정
PROPS['ground_sandstone']   = extract_prop(2, 1) # 사막 풍화 사암
PROPS['ground_lava_rock']   = extract_prop(2, 2) # 마그마 화산석
PROPS['ground_diamonds']    = extract_prop(2, 3) # 다이아몬드 수정체

for k, p in PROPS.items():
    print(f"  Prop '{k}': size={p.size}")

# 2. Slice 14 background panels from Sheets 1, 2, and 3
im_s1 = Image.open(P_SHEET_1).convert('RGB')
im_s2 = Image.open(P_SHEET_2).convert('RGB')
im_s3 = Image.open(P_SHEET_3).convert('RGB')

def slice_panel_2x2(im, r, c):
    w, h = 688, 384
    return im.crop((c * w + 6, r * h + 6, (c + 1) * w - 6, (r + 1) * h - 6))

def slice_panel_2x3(im, r, c):
    w, h = 458, 384
    return im.crop((c * w + 6, r * h + 6, (c + 1) * w - 6, (r + 1) * h - 6))

BASE_PANELS = {
    1: slice_panel_2x2(im_s1, 0, 0), # 서울 지하철 미궁 석회 동굴
    2: slice_panel_2x2(im_s1, 0, 1), # 북한산 은빛 침엽수림
    3: slice_panel_2x2(im_s1, 1, 0), # 인천항 부두 해안 갯바위
    4: slice_panel_2x2(im_s1, 1, 1), # 설악산 대청봉 만년설
    5: slice_panel_2x2(im_s2, 0, 0), # 평양 지하 50m 폭포 석순
    6: slice_panel_2x2(im_s2, 0, 1), # 도쿄 음양사 대나무 숲
    7: slice_panel_2x2(im_s2, 1, 0), # 마카오 열대 맹그로브 늪
    8: slice_panel_2x2(im_s2, 1, 1), # 블라디보스토크 동토 침엽수림
    9: slice_panel_2x3(im_s3, 0, 0), # 태평양 해연 8천m 심해
    10: slice_panel_2x3(im_s3, 0, 1), # 히말라야 8천m 빙룡 묘지
    11: slice_panel_2x3(im_s3, 0, 2), # 타클라마칸 사막 유리 분화구
    12: slice_panel_2x3(im_s3, 1, 0), # 로키 화산 마그마 분화구
    13: slice_panel_2x3(im_s3, 1, 1), # 태평양 성층권 운해 & 부유암
    14: slice_panel_2x3(im_s3, 1, 2), # 2070 다이아몬드문 종언
}

# 3. Prop assignment per region (canopy prop, ground prop)
REGION_PROP_MAPPING = {
    1:  ('canopy_stalactites',  'ground_mushrooms'),
    2:  ('canopy_snow_pine',    'ground_blue_ice'),
    3:  ('canopy_stalactites',  'ground_tidal_reef'),
    4:  ('canopy_snow_pine',    'ground_blue_ice'),
    5:  ('canopy_stalactites',  'ground_bamboo_stones'),
    6:  ('canopy_red_maple',    'ground_bamboo_stones'),
    7:  ('canopy_jungle_vines', 'ground_mushrooms'),
    8:  ('canopy_snow_pine',    'ground_blue_ice'),
    9:  ('canopy_jungle_vines', 'ground_coral_reef'),
    10: ('canopy_snow_pine',    'ground_blue_ice'),
    11: ('canopy_red_maple',    'ground_sandstone'),
    12: ('canopy_stalactites',  'ground_lava_rock'),
    13: ('canopy_red_maple',    'ground_sandstone'),
    14: ('canopy_stalactites',  'ground_diamonds'),
}

PANO_W = 2400
PANO_H = 360

print("\nBuilding 2400x360 battle panoramas & grounded/canopy prop layers for all 14 regions...")
for rId in range(1, 15):
    panel = BASE_PANELS[rId]
    pw, ph = panel.size
    scaled_w = int(pw * (PANO_H / ph))
    panel_scaled = panel.resize((scaled_w, PANO_H), Image.Resampling.LANCZOS)

    # 1) Build 2400x360 Background Strip with progressive environmental depth
    pano_bg = Image.new('RGB', (PANO_W, PANO_H))
    
    # Tile across 2400px width with smooth cross-blending and progressive tone
    # Zone 1 (0..400), Zone 2 (400..800), Zone 3 (800..1200), Zone 4 (1200..1600), Zone 5 (1600..2000), Zone 6 (2000..2400)
    for x_offset in range(0, PANO_W, scaled_w - 40):
        # Progressively enhance contrast/vibrancy as we get deeper into the gate (towards boss)
        progress = min(1.0, x_offset / PANO_W)
        enhancer = ImageEnhance.Color(panel_scaled)
        col_panel = enhancer.enhance(0.92 + progress * 0.22)
        enhancer_b = ImageEnhance.Brightness(col_panel)
        bright_panel = enhancer_b.enhance(0.94 + progress * 0.14)
        
        # Paste with overlap
        pano_bg.paste(bright_panel, (x_offset, 0))

    out_bg_path = os.path.join(OUTPUT_DIR, f'battle_pano_{rId}.png')
    pano_bg.save(out_bg_path, 'PNG')

    # 2) Build 2400x360 Parallax Props Strip
    pano_props = Image.new('RGBA', (PANO_W, PANO_H), (0, 0, 0, 0))
    canopy_key, ground_key = REGION_PROP_MAPPING[rId]
    canopy_img = PROPS[canopy_key]
    ground_img = PROPS[ground_key]

    # Wave zone anchor X positions across 2400px (Wave 1: ~180px, Wave 2: ~580px, Wave 3: ~980px, Wave 4: ~1380px, Wave 5: ~1780px, Wave 6: ~2180px)
    wave_x_anchors = [160, 560, 960, 1360, 1760, 2160]

    for wave_idx, base_x in enumerate(wave_x_anchors, 1):
        # Place CANOPY PROP hanging from CEILING (y = 0)
        c_scale = 0.55 if wave_idx % 2 == 1 else 0.48
        cw = int(canopy_img.width * c_scale)
        ch = int(canopy_img.height * c_scale)
        c_resized = canopy_img.resize((cw, ch), Image.Resampling.NEAREST)
        # Flip every other wave for natural variation
        if wave_idx % 2 == 0:
            c_resized = c_resized.transpose(Image.FLIP_LEFT_RIGHT)
        c_x = base_x + (wave_idx * 17) % 70 - 30
        c_y = 0  # CRITICAL: Hung firmly from the top ceiling, never floats!
        pano_props.paste(c_resized, (c_x, c_y), c_resized)

        # Place GROUND PROP resting on FLOOR (y = PANO_H - h - 10)
        g_scale = 0.52 if wave_idx % 2 == 0 else 0.60
        gw = int(ground_img.width * g_scale)
        gh = int(ground_img.height * g_scale)
        g_resized = ground_img.resize((gw, gh), Image.Resampling.NEAREST)
        if wave_idx % 2 == 1:
            g_resized = g_resized.transpose(Image.FLIP_LEFT_RIGHT)
        g_x = base_x + 120 + (wave_idx * 23) % 60
        g_y = PANO_H - gh - 12  # CRITICAL: Planted firmly on the bottom ground, never floats!
        pano_props.paste(g_resized, (g_x, g_y), g_resized)

    out_props_path = os.path.join(OUTPUT_DIR, f'nature_props_pano_{rId}.png')
    pano_props.save(out_props_path, 'PNG')

    # 3) Also update town backgrounds town_bg_${rId}_f0..3.png and region_obj_${rId}_f0..3.png
    town_base = panel.resize((600, 360), Image.Resampling.LANCZOS)
    for f in range(4):
        # Gentle 4-frame breathing pulse for town
        sway_y = 1 if f in (1, 2) else 0
        f_town = Image.new('RGB', (600, 360))
        f_town.paste(town_base, (0, sway_y))
        f_town.save(os.path.join(OUTPUT_DIR, f'town_bg_{rId}_f{f}.png'), 'PNG')

        # 4-frame gentle foliage/prop overlay for town
        f_obj = Image.new('RGBA', (600, 360), (0, 0, 0, 0))
        # Place 1 canopy at top-right and 1 ground at bottom-left
        cw = int(canopy_img.width * 0.45)
        ch = int(canopy_img.height * 0.45)
        c_res = canopy_img.resize((cw, ch), Image.Resampling.NEAREST)
        f_obj.paste(c_res, (600 - cw - 10, 0), c_res)

        gw = int(ground_img.width * 0.5)
        gh = int(ground_img.height * 0.5)
        g_res = ground_img.resize((gw, gh), Image.Resampling.NEAREST)
        f_obj.paste(g_res, (15, 360 - gh - 12 + sway_y), g_res)
        f_obj.save(os.path.join(OUTPUT_DIR, f'region_obj_{rId}_f{f}.png'), 'PNG')

    print(f"  [Region {rId}] Done: battle_pano, nature_props_pano, town_bg (f0..3), region_obj (f0..3)")

print("\nALL 14 REGIONS PERFECTLY REBUILT WITH 100% PURE WILD NATURE!")
