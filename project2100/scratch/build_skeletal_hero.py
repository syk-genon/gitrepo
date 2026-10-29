# -*- coding: utf-8 -*-
"""
16-Bit Arcade Retro Paperdoll & Skeletal Animator (DNF / 환세취호전 Style)
- 사지가 독립적으로 관절에 맞춰 움직이는 도트 캐릭터 생성기
- 베이스 캐릭터는 무기 없이 순수한 '누더기 반팔 티셔츠 + 청반바지 + 샌들'
- 남성(male) / 여성(female) 지원
- Idle(4f), Run(6f), Attack(4f), Skill(4f)
- 캐릭터는 항상 몬스터(오른쪽)를 향함
"""
import os, math
from PIL import Image, ImageDraw

hero_dir = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
weapons_dir = os.path.join(hero_dir, "weapons")
armors_dir = os.path.join(hero_dir, "armors")
os.makedirs(hero_dir, exist_ok=True)
os.makedirs(weapons_dir, exist_ok=True)
os.makedirs(armors_dir, exist_ok=True)

CANVAS_W = 120
CANVAS_H = 120

# -------------------------------------------------------------
# DNF 16-Bit Arcade Color Palettes
# -------------------------------------------------------------
OUTLINE = (26, 20, 32, 255)

# Skin (따뜻한 레트로 살구빛 피부톤)
SKIN_HL   = (255, 238, 222, 255)
SKIN_BASE = (250, 206, 172, 255)
SKIN_SHD  = (218, 154, 118, 255)
SKIN_DK   = (168, 102,  72, 255)

# Male Hair (스톤에이지/환세취호전 아타호/던파 귀검사 스타일 흑청색 삐죽머리)
M_HAIR_HL  = ( 88,  92, 120, 255)
M_HAIR_MID = ( 42,  44,  64, 255)
M_HAIR_SHD = ( 24,  22,  36, 255)
M_HAIR_DK  = ( 12,  10,  18, 255)

# Female Hair (환세취호전 린샹/던파 격투가 스타일 금발 포니테일 + 레드 리본)
F_HAIR_HL  = (255, 246, 170, 255)
F_HAIR_MID = (240, 198,  82, 255)
F_HAIR_SHD = (182, 134,  44, 255)
F_HAIR_DK  = (102,  70,  20, 255)
RIBBON_RED = (225,  45,  55, 255)

# 누더기 반팔 티셔츠 (Ragged Off-White Shirt)
SHIRT_HL   = (248, 245, 238, 255)
SHIRT_MID  = (215, 208, 196, 255)
SHIRT_SHD  = (160, 150, 138, 255)
SHIRT_FRY  = (115, 105,  94, 255) # 찢어진 깃/밑단 실밥

# 누더기 찢어진 청반바지 (Ragged Denim Shorts)
JEANS_HL   = ( 90, 128, 172, 255)
JEANS_MID  = ( 54,  84, 124, 255)
JEANS_SHD  = ( 36,  56,  88, 255)
JEANS_FRY  = (135, 162, 198, 255) # 찢어진 데님 올
BELT_BRN   = ( 90,  50,  30, 255)
BUCKLE_GLD = (245, 200,  50, 255)

# 샌들 / 붕대 (Footwear)
SANDAL_STRAP = ( 65,  40,  25, 255)
SANDAL_SOLE  = ( 35,  22,  15, 255)
BANDAGE_WHT  = (230, 230, 235, 255)

def create_frame():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# -------------------------------------------------------------
# 1. HEAD (머리 & 표정 - 우측 몬스터를 주시)
# -------------------------------------------------------------
def draw_head(d, cx, cy, female=False):
    ox = cx - 18
    oy = cy - 24

    if female:
        # 금발 포니테일 (뒤통수 좌측으로 흩날림)
        d.polygon([(ox+4, oy+8), (ox-8, oy+14), (ox-12, oy+28), (ox-2, oy+36), (ox+6, oy+20)], fill=F_HAIR_SHD, outline=OUTLINE)
        d.polygon([(ox+3, oy+10), (ox-6, oy+16), (ox-9, oy+26), (ox-1, oy+32)], fill=F_HAIR_MID)
        d.line([(ox-4, oy+18), (ox-7, oy+26)], fill=F_HAIR_HL, width=2)
        # 레드 리본
        d.rectangle([ox+2, oy+6, ox+7, oy+12], fill=RIBBON_RED, outline=OUTLINE)
        d.point((ox+4, oy+8), fill=(255, 160, 160, 255))
        
        # 얼굴 윤곽 (오른쪽을 바라봄)
        d.rectangle([ox+8, oy+10, ox+26, oy+26], fill=SKIN_BASE)
        d.rectangle([ox+10, oy+11, ox+24, oy+24], fill=SKIN_HL)
        # 턱선
        d.polygon([(ox+10, oy+26), (ox+25, oy+26), (ox+22, oy+31), (ox+14, oy+31)], fill=SKIN_SHD, outline=OUTLINE)
        d.rectangle([ox+15, oy+30, ox+21, oy+31], fill=SKIN_BASE)

        # 앞머리 & 옆머리
        d.polygon([(ox+7, oy+4), (ox+27, oy+4), (ox+25, oy+14), (ox+7, oy+12)], fill=F_HAIR_MID, outline=OUTLINE)
        d.polygon([(ox+10, oy+6), (ox+24, oy+6), (ox+22, oy+12), (ox+12, oy+12)], fill=F_HAIR_HL)
        d.polygon([(ox+23, oy+8), (ox+28, oy+18), (ox+24, oy+16)], fill=F_HAIR_SHD)

        # 눈 (오른쪽 응시)
        d.rectangle([ox+18, oy+16, ox+24, oy+22], fill=OUTLINE)
        d.rectangle([ox+19, oy+17, ox+23, oy+21], fill=(130, 60, 20, 255))
        d.point((ox+22, oy+17), fill=(255, 255, 255, 255)) # 하이라이트
        d.point((ox+20, oy+20), fill=(210, 130, 40, 255))
        # 홍조 & 미소
        d.point((ox+16, oy+23), fill=(255, 140, 140, 255))
        d.line([(ox+20, oy+26), (ox+23, oy+26)], fill=OUTLINE)
    else:
        # 남성 삐죽 흑발 (환세취호전 / 귀검사풍)
        # 뒷머리 스파이크
        d.polygon([(ox+5, oy+6), (ox-6, oy+2), (ox+4, oy+14)], fill=M_HAIR_DK, outline=OUTLINE)
        d.polygon([(ox+3, oy+12), (ox-8, oy+16), (ox+4, oy+24)], fill=M_HAIR_DK, outline=OUTLINE)
        # 정수리 & 앞머리 스파이크 (위 & 우측으로 역동적 뻗침)
        d.polygon([(ox+8, oy+6), (ox+14, oy-6), (ox+20, oy+6)], fill=M_HAIR_MID, outline=OUTLINE)
        d.polygon([(ox+18, oy+4), (ox+28, oy-4), (ox+28, oy+8)], fill=M_HAIR_MID, outline=OUTLINE)
        d.polygon([(ox+24, oy+8), (ox+34, oy+4), (ox+28, oy+15)], fill=M_HAIR_MID, outline=OUTLINE)
        d.line([(ox+14, oy-2), (ox+18, oy+5)], fill=M_HAIR_HL, width=2)
        d.line([(ox+25, oy-1), (ox+27, oy+6)], fill=M_HAIR_HL, width=2)

        # 얼굴 피부
        d.rectangle([ox+10, oy+10, ox+27, oy+26], fill=SKIN_BASE)
        d.rectangle([ox+12, oy+12, ox+25, oy+24], fill=SKIN_HL)
        # 각진 열혈 턱선
        d.polygon([(ox+11, oy+26), (ox+26, oy+26), (ox+23, oy+32), (ox+15, oy+32)], fill=SKIN_SHD, outline=OUTLINE)
        d.rectangle([ox+16, oy+31, ox+22, oy+32], fill=SKIN_BASE)

        # 결의에 찬 눈썹 & 눈 (우측 몬스터 응시)
        d.line([(ox+18, oy+15), (ox+26, oy+17)], fill=OUTLINE, width=2)
        d.rectangle([ox+19, oy+18, ox+25, oy+23], fill=OUTLINE)
        d.rectangle([ox+20, oy+19, ox+24, oy+22], fill=(40, 80, 150, 255))
        d.point((ox+23, oy+19), fill=(255, 255, 255, 255)) # 눈동자 광채
        # 뺨의 반창고 / 흉터 (서바이버 디테일)
        d.line([(ox+14, oy+23), (ox+17, oy+23)], fill=(60, 120, 180, 255), width=2)
        # 입매
        d.line([(ox+20, oy+27), (ox+24, oy+26)], fill=OUTLINE)

# -------------------------------------------------------------
# 2. TORSO (누더기 반팔 티셔츠 & 찢어진 청반바지 - 무기 없음!)
# -------------------------------------------------------------
def draw_torso(d, cx, cy, tilt=0):
    ox = cx - 14 + tilt
    oy = cy - 14

    # 목
    d.rectangle([ox+11, oy+6, ox+17, oy+11], fill=SKIN_SHD, outline=OUTLINE)
    
    # 누더기 반팔 티셔츠 (몸통)
    d.rectangle([ox+6, oy+11, ox+22, oy+27], fill=SHIRT_MID, outline=OUTLINE)
    d.rectangle([ox+8, oy+12, ox+20, oy+24], fill=SHIRT_HL)
    # 올 풀린 V넥 칼라
    d.polygon([(ox+11, oy+11), (ox+17, oy+11), (ox+14, oy+16)], fill=SKIN_SHD, outline=OUTLINE)
    # 티셔츠 밑단 찢어진 실밥 디테일
    for sx in range(ox+7, ox+22, 3):
        d.line([(sx, oy+27), (sx+1, oy+29)], fill=SHIRT_FRY)

    # 허리 가죽 벨트
    d.rectangle([ox+6, oy+26, ox+22, oy+29], fill=BELT_BRN, outline=OUTLINE)
    d.rectangle([ox+13, oy+26, ox+16, oy+29], fill=BUCKLE_GLD)

    # 찢어진 데님 청반바지 (골반/엉덩이부)
    d.rectangle([ox+6, oy+29, ox+22, oy+35], fill=JEANS_MID, outline=OUTLINE)
    d.rectangle([ox+8, oy+30, ox+20, oy+33], fill=JEANS_HL)
    d.line([(ox+14, oy+30), (ox+14, oy+35)], fill=JEANS_SHD) # 바지 중심선

# -------------------------------------------------------------
# 3. LEGS (양다리: 허벅지, 찢어진 바짓단, 무릎, 샌들 발)
# -------------------------------------------------------------
def draw_leg_left(d, cx, cy, angle_deg=0, bend_px=0):
    """왼다리 (뒤쪽 다리 - 원근감 음영)"""
    rad = math.radians(angle_deg)
    # 골반 시작점
    bx = cx - 4
    by = cy + 20
    # 허벅지 찢어진 바짓단
    d.rectangle([bx-5, by, bx+3, by+8], fill=JEANS_SHD, outline=OUTLINE)
    d.line([(bx-5, by+8), (bx+3, by+8)], fill=JEANS_FRY)
    
    # 무릎 & 종아리 (각도에 따라 회전)
    kx = bx + int(12 * math.sin(rad))
    ky = by + int(12 * math.cos(rad)) + bend_px
    d.line([(bx-1, by+8), (kx, ky)], fill=SKIN_SHD, width=6)
    
    # 발목 & 샌들
    fx = kx + int(10 * math.sin(rad * 0.7)) + 2
    fy = ky + int(10 * math.cos(rad * 0.7))
    d.line([(kx, ky), (fx, fy)], fill=SKIN_SHD, width=5)
    # 샌들 밑창
    d.rectangle([fx-2, fy, fx+8, fy+3], fill=SANDAL_SOLE, outline=OUTLINE)
    d.line([(fx, fy-1), (fx+4, fy-1)], fill=SANDAL_STRAP, width=2)

def draw_leg_right(d, cx, cy, angle_deg=0, bend_px=0):
    """오른다리 (앞쪽 다리 - 하이라이트)"""
    rad = math.radians(angle_deg)
    bx = cx + 4
    by = cy + 20
    # 허벅지 찢어진 바짓단
    d.rectangle([bx-3, by, bx+6, by+8], fill=JEANS_MID, outline=OUTLINE)
    d.line([(bx-3, by+8), (bx+6, by+8)], fill=JEANS_FRY)
    
    # 무릎 & 종아리
    kx = bx + int(12 * math.sin(rad))
    ky = by + int(12 * math.cos(rad)) + bend_px
    d.line([(bx+1, by+8), (kx, ky)], fill=SKIN_BASE, width=6)
    d.point((kx, ky-2), fill=SKIN_HL) # 무릎 하이라이트
    
    # 발목 & 샌들
    fx = kx + int(10 * math.sin(rad * 0.7)) + 3
    fy = ky + int(10 * math.cos(rad * 0.7))
    d.line([(kx, ky), (fx, fy)], fill=SKIN_BASE, width=5)
    # 샌들 밑창
    d.rectangle([fx-2, fy, fx+9, fy+3], fill=SANDAL_SOLE, outline=OUTLINE)
    d.line([(fx+1, fy-1), (fx+5, fy-1)], fill=SANDAL_STRAP, width=2)

# -------------------------------------------------------------
# 4. ARMS (양팔: 반팔 소매, 팔뚝, 주먹 손 - 무기 없음!)
# -------------------------------------------------------------
def draw_arm_left(d, cx, cy, angle_deg=0):
    """왼팔 (뒤쪽 팔 - 원근감 섀도우)"""
    rad = math.radians(angle_deg)
    # 어깨 위치
    sx = cx - 9
    sy = cy - 2
    # 반팔 소매
    d.rectangle([sx-3, sy-1, sx+3, sy+5], fill=SHIRT_SHD, outline=OUTLINE)
    # 팔꿈치
    ex = sx + int(9 * math.sin(rad))
    ey = sy + int(9 * math.cos(rad))
    d.line([(sx, sy+4), (ex, ey)], fill=SKIN_SHD, width=5)
    # 손 (주먹)
    wx = ex + int(8 * math.sin(rad * 0.8))
    wy = ey + int(8 * math.cos(rad * 0.8))
    d.line([(ex, ey), (wx, wy)], fill=SKIN_SHD, width=4)
    d.rectangle([wx-2, wy-2, wx+3, wy+3], fill=SKIN_DK, outline=OUTLINE)

def draw_arm_right(d, cx, cy, angle_deg=0, hand_pose="fist"):
    """오른팔 (앞쪽 팔 - 밝은 피부톤, 무기를 쥘 수 있는 빈 손)"""
    rad = math.radians(angle_deg)
    sx = cx + 8
    sy = cy - 2
    # 반팔 소매
    d.rectangle([sx-3, sy-1, sx+4, sy+5], fill=SHIRT_MID, outline=OUTLINE)
    # 팔꿈치
    ex = sx + int(10 * math.sin(rad))
    ey = sy + int(10 * math.cos(rad))
    d.line([(sx, sy+4), (ex, ey)], fill=SKIN_BASE, width=5)
    # 손목 붕대/아대
    d.rectangle([ex-2, ey-1, ex+2, ey+2], fill=SANDAL_STRAP)
    # 손 (빈 주먹 - 무기 레이어가 여기에 손잡이를 맞춤)
    wx = ex + int(9 * math.sin(rad * 0.8))
    wy = ey + int(9 * math.cos(rad * 0.8))
    d.line([(ex, ey), (wx, wy)], fill=SKIN_BASE, width=4)
    d.rectangle([wx-3, wy-3, wx+4, wy+4], fill=SKIN_BASE, outline=OUTLINE)
    d.point((wx, wy), fill=SKIN_HL)
    return (wx, wy) # 손 중심 좌표 반환 (무기 위치 정렬용)

# -------------------------------------------------------------
# 5. WEAPONS (무기 레이어 - 손 위치에 정확히 쥐어지는 도트 무기)
# -------------------------------------------------------------
def draw_weapon_katana(d, hx, hy, angle_deg):
    """카타나: 손(hx, hy)을 기준으로 뻗어 나가는 강철 블레이드"""
    rad = math.radians(angle_deg)
    # 손잡이 (뒤쪽으로 6px)
    px = hx - int(8 * math.cos(rad))
    py = hy - int(8 * math.sin(rad))
    d.line([(px, py), (hx, hy)], fill=(80, 45, 25, 255), width=3)
    # 코등이 (가드)
    gx1 = hx + int(4 * math.sin(rad))
    gy1 = hy - int(4 * math.cos(rad))
    gx2 = hx - int(4 * math.sin(rad))
    gy2 = hy + int(4 * math.cos(rad))
    d.line([(gx1, gy1), (gx2, gy2)], fill=BUCKLE_GLD, width=2)
    # 칼날 (앞쪽으로 28px)
    bx = hx + int(28 * math.cos(rad))
    by = hy + int(28 * math.sin(rad))
    d.line([(hx, hy), (bx, by)], fill=(215, 230, 248, 255), width=3)
    d.line([(hx, hy), (bx-2, by-2)], fill=(255, 255, 255, 255), width=1)
    d.point((bx, by), fill=(255, 255, 255, 255))

def draw_weapon_axe(d, hx, hy, angle_deg):
    """전투 도끼"""
    rad = math.radians(angle_deg)
    bx = hx + int(26 * math.cos(rad))
    by = hy + int(26 * math.sin(rad))
    # 자루
    d.line([(hx - int(6*math.cos(rad)), hy - int(6*math.sin(rad))), (bx, by)], fill=(90, 55, 30, 255), width=3)
    # 도끼날
    d.polygon([(bx-4, by-8), (bx+6, by-4), (bx+8, by+4), (bx-2, by+8)], fill=(180, 195, 215, 255), outline=OUTLINE)
    d.line([(bx+5, by-4), (bx+7, by+4)], fill=(255, 255, 255, 255), width=2)

def draw_weapon_crystal_sword(d, hx, hy, angle_deg):
    """크리스탈 소드"""
    rad = math.radians(angle_deg)
    bx = hx + int(30 * math.cos(rad))
    by = hy + int(30 * math.sin(rad))
    d.line([(hx, hy), (bx, by)], fill=(120, 220, 255, 255), width=4)
    d.line([(hx, hy), (bx, by)], fill=(255, 255, 255, 255), width=2)

def draw_weapon_heavy_cannon(d, hx, hy, angle_deg):
    """중기관포"""
    rad = math.radians(angle_deg)
    bx = hx + int(24 * math.cos(rad))
    by = hy + int(24 * math.sin(rad))
    d.line([(hx, hy), (bx, by)], fill=(60, 65, 80, 255), width=6)
    d.line([(hx, hy), (bx, by)], fill=(140, 150, 175, 255), width=2)
    d.point((bx, by), fill=(255, 120, 50, 255))

def draw_weapon_lava_launcher(d, hx, hy, angle_deg):
    """용암 런처"""
    rad = math.radians(angle_deg)
    bx = hx + int(26 * math.cos(rad))
    by = hy + int(26 * math.sin(rad))
    d.line([(hx, hy), (bx, by)], fill=(120, 40, 20, 255), width=6)
    d.line([(hx, hy), (bx, by)], fill=(255, 100, 30, 255), width=3)
    d.point((bx, by), fill=(255, 240, 100, 255))

WEAPON_DRAWERS = {
    "katana": draw_weapon_katana,
    "axe": draw_weapon_axe,
    "crystal_sword": draw_weapon_crystal_sword,
    "heavy_cannon": draw_weapon_heavy_cannon,
    "lava_launcher": draw_weapon_lava_launcher
}

# -------------------------------------------------------------
# 6. ARMORS (방어구 오버레이 레이어)
# -------------------------------------------------------------
def draw_armor(d, cx, cy, armor_key):
    ox = cx - 14
    oy = cy - 14
    if armor_key == "military":
        # 군복 조끼
        d.rectangle([ox+5, oy+11, ox+23, oy+27], fill=(65, 85, 55, 255), outline=OUTLINE)
        d.rectangle([ox+7, oy+13, ox+21, oy+25], fill=(95, 120, 80, 255))
        d.line([(ox+14, oy+11), (ox+14, oy+27)], fill=(45, 60, 40, 255), width=2)
    elif armor_key == "leather":
        # 가죽 갑옷
        d.rectangle([ox+5, oy+11, ox+23, oy+27], fill=(125, 75, 45, 255), outline=OUTLINE)
        d.rectangle([ox+8, oy+14, ox+20, oy+24], fill=(160, 105, 65, 255))
        d.rectangle([ox+10, oy+17, ox+18, oy+22], fill=BUCKLE_GLD)
    elif armor_key == "nano_carbon":
        # 나노 카본 슈트
        d.rectangle([ox+5, oy+11, ox+23, oy+27], fill=(30, 35, 45, 255), outline=OUTLINE)
        d.rectangle([ox+8, oy+13, ox+20, oy+25], fill=(55, 65, 85, 255))
        d.line([(ox+14, oy+13), (ox+14, oy+25)], fill=(60, 200, 255, 255))
    elif armor_key == "hardlight":
        # 하드라이트 에너지 아머
        d.rectangle([ox+5, oy+11, ox+23, oy+27], fill=(40, 140, 200, 200), outline=(100, 220, 255, 255))
        d.rectangle([ox+8, oy+13, ox+20, oy+25], fill=(120, 230, 255, 220))
    elif armor_key == "yeti_fur":
        # 예티 모피 코트
        d.rectangle([ox+4, oy+10, ox+24, oy+28], fill=(230, 235, 245, 255), outline=OUTLINE)
        d.rectangle([ox+7, oy+12, ox+21, oy+26], fill=(255, 255, 255, 255))

# -------------------------------------------------------------
# 7. SKELETAL MOTION COMPOSITOR (사지 독립 관절 합성)
# -------------------------------------------------------------
def render_skeletal_frame(cx, cy, female, 
                          head_offset=(0, 0),
                          torso_tilt=0,
                          l_arm_angle=0,
                          r_arm_angle=0,
                          l_leg_angle=0,
                          r_leg_angle=0,
                          leg_bend=0,
                          weapon_angle=45,
                          vfx_type=None):
    """
    레이어 순서 (깊이 버퍼):
    1. 뒤쪽 왼팔 (L-Arm)
    2. 뒤쪽 왼다리 (L-Leg)
    3. 몸통 (Torso)
    4. 앞쪽 오른다리 (R-Leg)
    5. 머리 (Head)
    6. 앞쪽 오른팔 (R-Arm) -> 손 위치 반환
    7. 무기 레이어 (Weapons)
    8. 참격 VFX
    """
    frame_body = create_frame()
    d_body = ImageDraw.Draw(frame_body)

    # 1. 왼팔
    draw_arm_left(d_body, cx, cy, l_arm_angle)
    # 2. 왼다리
    draw_leg_left(d_body, cx, cy, l_leg_angle, leg_bend)
    # 3. 몸통
    draw_torso(d_body, cx, cy, torso_tilt)
    # 4. 오른다리
    draw_leg_right(d_body, cx, cy, r_leg_angle, leg_bend)
    # 5. 머리
    draw_head(d_body, cx + head_offset[0], cy + head_offset[1], female)
    # 6. 오른팔 (손 좌표 반환)
    hand_pos = draw_arm_right(d_body, cx, cy, r_arm_angle)

    # 무기별 개별 프레임 생성
    weapon_frames = {}
    for w_name, w_drawer in WEAPON_DRAWERS.items():
        w_img = create_frame()
        w_d = ImageDraw.Draw(w_img)
        w_drawer(w_d, hand_pos[0], hand_pos[1], weapon_angle)
        weapon_frames[w_name] = w_img

    # 방어구별 개별 프레임 생성
    armor_frames = {}
    for a_name in ["military", "leather", "nano_carbon", "hardlight", "yeti_fur"]:
        a_img = create_frame()
        a_d = ImageDraw.Draw(a_img)
        draw_armor(a_d, cx, cy, a_name)
        armor_frames[a_name] = a_img

    # VFX 프레임 (필요 시)
    vfx_img = None
    if vfx_type == "slash":
        vfx_img = create_frame()
        v_d = ImageDraw.Draw(vfx_img)
        # 호쾌한 참격 아크
        for deg in range(-50, 65, 2):
            rad = math.radians(deg)
            r = 30
            vx = hand_pos[0] + 12 + int(r * math.cos(rad))
            vy = hand_pos[1] - int(r * 1.3 * math.sin(rad))
            v_d.line([(vx-1, vy), (vx+2, vy+2)], fill=(120, 225, 255, 240), width=3)
            v_d.point((vx, vy), fill=(255, 255, 255, 255))
    elif vfx_type == "upper":
        vfx_img = create_frame()
        v_d = ImageDraw.Draw(vfx_img)
        for deg in range(-70, 40, 2):
            rad = math.radians(deg)
            r = 34
            vx = hand_pos[0] + 8 + int(r * math.cos(rad))
            vy = hand_pos[1] - 8 - int(r * 1.4 * math.sin(rad))
            v_d.line([(vx, vy-2), (vx+2, vy+2)], fill=(140, 235, 255, 250), width=3)
            v_d.point((vx, vy), fill=(255, 255, 255, 255))

    return frame_body, weapon_frames, armor_frames, vfx_img

# -------------------------------------------------------------
# 8. MASTER ANIMATION BUILDER
# -------------------------------------------------------------
def build_all_characters():
    print("=== Generating DNF-Style 16-Bit Skeletal Animations ===")
    
    # 기본 중심 좌표
    BASE_CX = 56
    BASE_CY = 60

    for female in [False, True]:
        prefix = "female" if female else "male"
        print(f"Rendering {prefix} skeletal action frames...")

        # ---------------------------------------------------------
        # (1) IDLE (4 프레임) - 자연스러운 호흡과 미세 관절 리듬
        # ---------------------------------------------------------
        idle_configs = [
            # cy_off, head_off, torso_tilt, l_arm, r_arm, l_leg, r_leg, w_angle
            ( 0, ( 0,  0),  0, -10,  15,  -5,   5,  35), # 0: 기본 자세
            (-1, ( 0, -1),  0,  -8,  12,  -4,   4,  32), # 1: 들숨 (가슴 팽창)
            (-2, ( 0, -2),  0,  -5,   8,  -2,   2,  28), # 2: 최고점
            (-1, ( 0, -1),  0,  -8,  12,  -4,   4,  32), # 3: 날숨
        ]
        for i, cfg in enumerate(idle_configs):
            cy_off, h_off, t_tilt, la, ra, ll, rl, wa = cfg
            body, w_dict, a_dict, _ = render_skeletal_frame(
                BASE_CX, BASE_CY + cy_off, female,
                head_offset=h_off, torso_tilt=t_tilt,
                l_arm_angle=la, r_arm_angle=ra,
                l_leg_angle=ll, r_leg_angle=rl,
                weapon_angle=wa
            )
            body.save(os.path.join(hero_dir, f"{prefix}_idle_{i}.png"))
            for w_name, w_im in w_dict.items():
                w_im.save(os.path.join(weapons_dir, f"{w_name}_idle_{i}.png"))
            for a_name, a_im in a_dict.items():
                a_im.save(os.path.join(armors_dir, f"{a_name}_idle_{i}.png"))

        # ---------------------------------------------------------
        # (2) RUN (6 프레임) - 진짜 사지가 교차하는 던파식 전방 질주!
        # ---------------------------------------------------------
        run_configs = [
            # cy, head, tilt, la, ra, ll, rl, bend, wa
            ( 1, ( 2, 0),  1, -30,  35,  25, -25,  0,  45), # 0: 오른다리 앞, 왼다리 뒤 킥
            (-1, ( 3, -1), 2, -15,  18,  12, -10, -2,  35), # 1: 가속 바운스
            (-4, ( 2, -2), 1,   5, -10,  -5,   5, -3,  25), # 2: 체공 도약
            ( 1, ( 2, 0),  1,  35, -30, -25,  25,  0,  20), # 3: 왼다리 앞, 오른다리 뒤 킥 (교차!)
            (-1, ( 3, -1), 2,  18, -15, -10,  12, -2,  30), # 4: 가속 바운스
            (-4, ( 2, -2), 1, -10,   5,   5,  -5, -3,  40), # 5: 체공 도약
        ]
        for i, cfg in enumerate(run_configs):
            cy_off, h_off, t_tilt, la, ra, ll, rl, bend, wa = cfg
            body, w_dict, a_dict, _ = render_skeletal_frame(
                BASE_CX, BASE_CY + cy_off, female,
                head_offset=h_off, torso_tilt=t_tilt,
                l_arm_angle=la, r_arm_angle=ra,
                l_leg_angle=ll, r_leg_angle=rl,
                leg_bend=bend, weapon_angle=wa
            )
            body.save(os.path.join(hero_dir, f"{prefix}_run_{i}.png"))
            for w_name, w_im in w_dict.items():
                w_im.save(os.path.join(weapons_dir, f"{w_name}_run_{i}.png"))
            for a_name, a_im in a_dict.items():
                a_im.save(os.path.join(armors_dir, f"{a_name}_run_{i}.png"))

        # ---------------------------------------------------------
        # (3) ATTACK (4 프레임) - 백스윙 와인드업 -> 전방 쾌속 참격 스윙!
        # ---------------------------------------------------------
        attack_configs = [
            # 0: 상체 뒤로 젖히며 검을 뒤로 뽑는 발도 백스윙
            ( 1, (-3,  1), -2, -40, -55, -15,  15,  2, -120, None),
            # 1: 전방으로 돌진하며 시원하게 그어버리는 수평 참격!
            (-1, ( 5,  0),  3,  20,  65,  20, -18, -1,   15, "slash"),
            # 2: 전방 완전 관통 팔로우스루
            ( 0, ( 6,  0),  2,  15,  75,  24, -20,  0,   30, None),
            # 3: 칼끝을 회수하며 착지 가드
            ( 0, ( 1,  0),  0, -15,  25,  -5,   5,  0,   45, None),
        ]
        for i, cfg in enumerate(attack_configs):
            cy_off, h_off, t_tilt, la, ra, ll, rl, bend, wa, vfx = cfg
            body, w_dict, a_dict, v_img = render_skeletal_frame(
                BASE_CX, BASE_CY + cy_off, female,
                head_offset=h_off, torso_tilt=t_tilt,
                l_arm_angle=la, r_arm_angle=ra,
                l_leg_angle=ll, r_leg_angle=rl,
                leg_bend=bend, weapon_angle=wa, vfx_type=vfx
            )
            body.save(os.path.join(hero_dir, f"{prefix}_attack_{i}.png"))
            for w_name, w_im in w_dict.items():
                w_im.save(os.path.join(weapons_dir, f"{w_name}_attack_{i}.png"))
            for a_name, a_im in a_dict.items():
                a_im.save(os.path.join(armors_dir, f"{a_name}_attack_{i}.png"))

        # ---------------------------------------------------------
        # (4) SKILL (4 프레임) - 하체 웅크림 -> 공중 어퍼슬래시 & 강타
        # ---------------------------------------------------------
        skill_configs = [
            # 0: 하체 깊게 웅크리기
            ( 5, ( 0,  3),  1, -15, -20, -10,  10,  6,  -45, None),
            # 1: 공중으로 솟구치며 수직 상승 어퍼슬래시!
            (-12, ( 2, -8), 2, -35,  85,  15,  10, -5,   80, "upper"),
            # 2: 공중 최고 정점
            (-16, ( 3, -10), 1, -25, 75,  20,  12, -6,   60, None),
            # 3: 급강하 착지 충격파
            ( 4, ( 2,  2),  2,  20,  45,  15, -10,  4,   15, None),
        ]
        for i, cfg in enumerate(skill_configs):
            cy_off, h_off, t_tilt, la, ra, ll, rl, bend, wa, vfx = cfg
            body, w_dict, a_dict, v_img = render_skeletal_frame(
                BASE_CX, BASE_CY + cy_off, female,
                head_offset=h_off, torso_tilt=t_tilt,
                l_arm_angle=la, r_arm_angle=ra,
                l_leg_angle=ll, r_leg_angle=rl,
                leg_bend=bend, weapon_angle=wa, vfx_type=vfx
            )
            body.save(os.path.join(hero_dir, f"{prefix}_skill_{i}.png"))
            for w_name, w_im in w_dict.items():
                w_im.save(os.path.join(weapons_dir, f"{w_name}_skill_{i}.png"))
            for a_name, a_im in a_dict.items():
                a_im.save(os.path.join(armors_dir, f"{a_name}_skill_{i}.png"))

    print("All male/female skeletal action frames generated successfully!")

if __name__ == "__main__":
    build_all_characters()
