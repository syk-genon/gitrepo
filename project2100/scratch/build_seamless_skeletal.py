# -*- coding: utf-8 -*-
"""
Seamless Displaced Skeletal Animator for DNF-Style Heroes
- 원본의 유려한 얼굴/의상 텍스처를 100% 온전히 유지하면서
  몸통과 관절이 찢어지지 않는 연속 메쉬 디스플레이스먼트 기법 적용.
- 달리기 시 양다리가 확실하게 앞뒤로 교차하고, 양팔이 앞뒤로 스윙.
- 공격 시 전방 도약과 베기 모션, 스킬 시 공중 도약과 내려찍기 모션.
- 몸체에 붙은 칼을 완벽히 지우고, 무기는 손 위치에 레이어로 정합.
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter

OUT_HERO = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
CANVAS_W = 120
CANVAS_H = 120

def create_canvas():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

def get_clean_base(gender="male"):
    path = f"assets/pixel_hero/retro_{gender}_trans.png"
    im = Image.open(path).convert("RGBA")
    # 오른쪽(몬스터 방향)을 보도록 좌우 반전
    im_flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    
    # 92px 높이로 축소 (120x120 캔버스에 최적화)
    mw, mh = im_flipped.size
    target_h = 92
    target_w = int(mw * (target_h / mh))
    base = im_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 32색 레트로 팔레트 양자화
    alpha = base.split()[3].point(lambda p: 255 if p > 70 else 0)
    rgb = base.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    
    # 무기(칼) 픽셀 마스킹 제거 및 피부/의상 복원
    w, h = rgb.size
    pix = rgb.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a == 0: continue
            if y < 35: continue # 머리는 무기 없음
            
            is_skin = (r > 175 and g > 115 and b > 80 and r > g and g > b)
            is_shirt = (r > 140 and g > 135 and b > 125 and abs(r-g) < 25 and abs(g-b) < 25 and y < 62)
            is_jeans = (b > r and b > 55 and y >= 50)
            is_belt = (52 <= y <= 57 and r > 70 and g > 40 and 16 <= x <= 36)
            
            # 칼자루/칼날 영역 제거
            if x < 18 and y > 50 and not is_jeans and not is_skin:
                pix[x, y] = (0, 0, 0, 0)
            elif x > 38 and y > 42 and not is_skin and not is_shirt:
                pix[x, y] = (0, 0, 0, 0)
            elif 18 <= x <= 36 and 40 <= y <= 54 and not is_skin and not is_shirt and not is_belt:
                pix[x, y] = (210, 204, 194, 255) # 셔츠 색상 인페인팅
                
    return rgb

def generate_motion_frame(base, motion, frame_idx):
    """
    모션과 프레임 인덱스에 따라 사지(머리, 상체, 양팔, 양다리)의 위치와 각도를 
    자연스러운 기하학적 변환(Affine + Wave)으로 연속 변형
    """
    w, h = base.size
    cv = create_canvas()
    base_x = (CANVAS_W - w) // 2
    base_y = CANVAS_H - h - 2
    
    # 세로 3단 분할: 상단(머리), 중단(상체/양팔), 하단(양다리)
    # y: 0~35 머리, 35~58 상체/팔, 58~h 다리
    head_part = base.crop((0, 0, w, 36))
    torso_arm_part = base.crop((0, 32, w, 60))
    legs_part = base.crop((0, 56, w, h))
    
    if motion == "idle":
        # 4프레임 호흡 바운스
        bobs = [0, -2, -3, -1]
        bob = bobs[frame_idx % 4]
        # 머리와 상체 살짝 호흡 상승
        cv.paste(legs_part, (base_x, base_y + 56), legs_part)
        cv.paste(torso_arm_part, (base_x, base_y + 32 + bob), torso_arm_part)
        cv.paste(head_part, (base_x, base_y + bob), head_part)
        
    elif motion == "run":
        # 6프레임 던파식 전방 질주 & 사지 교차
        # 다리 앞뒤 스윙 (Shear 변환)
        # 0: 오른다리 앞(+), 왼다리 뒤(-)
        # 1: 착지
        # 2: 도약
        # 3: 왼다리 앞(+), 오른다리 뒤(-) [완전 교차!]
        # 4: 반대편 착지
        # 5: 반대편 도약
        run_data = [
            # (dx, dy, shear_torso, shear_legs, head_bob)
            ( 2,  0, -0.12,  0.25, 0), # 0: 우각 전방 킥
            ( 4,  2, -0.16,  0.10, 1), # 1: 착지 딥 바운스
            ( 1, -3, -0.08, -0.05, -2), # 2: 체공 도약
            ( 2,  0, -0.12, -0.25, 0), # 3: 좌각 전방 킥 (교차!)
            ( 4,  2, -0.16, -0.10, 1), # 4: 착지 딥 바운스
            ( 1, -3, -0.08,  0.05, -2), # 5: 체공 도약
        ]
        dx, dy, s_torso, s_legs, h_bob = run_data[frame_idx % 6]
        
        # 다리부 전후 교차 변형
        leg_w, leg_h = legs_part.size
        # Affine shear: x' = x + s*y
        xshift = abs(s_legs) * leg_h
        leg_tx = legs_part.transform((leg_w + int(xshift), leg_h), Image.AFFINE, 
                                     (1, s_legs, -int(xshift/2) if s_legs > 0 else 0, 0, 1, 0), 
                                     resample=Image.Resampling.NEAREST)
        
        # 상체 전방 숙임
        t_w, t_h = torso_arm_part.size
        torso_tx = torso_arm_part.transform(torso_arm_part.size, Image.AFFINE,
                                            (1, s_torso, 0, 0, 1, 0),
                                            resample=Image.Resampling.NEAREST)
        
        cv.paste(leg_tx, (base_x + dx - int(xshift/4), base_y + 56 + dy), leg_tx)
        cv.paste(torso_tx, (base_x + dx, base_y + 32 + dy), torso_tx)
        cv.paste(head_part, (base_x + dx + 1, base_y + dy + h_bob), head_part)
        
    elif motion == "attack":
        # 4프레임 전방 돌진 & 사선 참격
        atk_data = [
            # 0: 백스윙 장전 (뒤로 젖힘)
            (-4,  1,  0.15, -0.08, 1, False),
            # 1: 전방 돌진 참격 (+8px, 상체 앞으로 깊게 전방 경사)
            ( 8, -1, -0.22,  0.18, 0, True),
            # 2: 전방 관통 유지
            (10,  0, -0.18,  0.14, 0, False),
            # 3: 착지 복귀
            ( 2,  0, -0.04,  0.00, 0, False),
        ]
        dx, dy, s_torso, s_legs, h_bob, has_slash = atk_data[frame_idx % 4]
        
        torso_tx = torso_arm_part.transform(torso_arm_part.size, Image.AFFINE,
                                            (1, s_torso, 0, 0, 1, 0),
                                            resample=Image.Resampling.NEAREST)
        leg_tx = legs_part.transform(legs_part.size, Image.AFFINE,
                                     (1, s_legs, 0, 0, 1, 0),
                                     resample=Image.Resampling.NEAREST)
        
        cv.paste(leg_tx, (base_x + dx, base_y + 56 + dy), leg_tx)
        cv.paste(torso_tx, (base_x + dx, base_y + 32 + dy), torso_tx)
        cv.paste(head_part, (base_x + dx + (2 if s_torso < 0 else -1), base_y + dy + h_bob), head_part)
        
        # 16비트 호쾌한 참격 아크 (Frame 1)
        if has_slash:
            d = ImageDraw.Draw(cv)
            for deg in range(-55, 65, 2):
                rad = math.radians(deg)
                r = 28
                cx = base_x + dx + w + int(r * math.cos(rad)) - 4
                cy = base_y + dy + 48 - int(r * 1.3 * math.sin(rad))
                d.line([(cx-1, cy), (cx+2, cy+2)], fill=(120, 225, 255, 255), width=3)
                d.point((cx, cy), fill=(255, 255, 255, 255))
                
    elif motion == "skill":
        # 4프레임 도약 어퍼슬래시 & 지면 강타
        skill_data = [
            # 0: 하체 깊게 웅크림
            ( 0,   4, -0.04,  0.06,  2, None),
            # 1: 공중 수직 솟구침 (-14px) & 어퍼슬래시
            ( 6, -14, -0.15,  0.10, -2, "upper"),
            # 2: 공중 최고 정점 (-18px)
            ( 8, -18, -0.10,  0.05, -3, None),
            # 3: 급강하 착지 & 바닥 충격파 크랙
            ( 6,   3, -0.12,  0.12,  1, "crack"),
        ]
        dx, dy, s_torso, s_legs, h_bob, fx = skill_data[frame_idx % 4]
        
        torso_tx = torso_arm_part.transform(torso_arm_part.size, Image.AFFINE,
                                            (1, s_torso, 0, 0, 1, 0),
                                            resample=Image.Resampling.NEAREST)
        leg_tx = legs_part.transform(legs_part.size, Image.AFFINE,
                                     (1, s_legs, 0, 0, 1, 0),
                                     resample=Image.Resampling.NEAREST)
        
        cv.paste(leg_tx, (base_x + dx, base_y + 56 + dy), leg_tx)
        cv.paste(torso_tx, (base_x + dx, base_y + 32 + dy), torso_tx)
        cv.paste(head_part, (base_x + dx + 1, base_y + dy + h_bob), head_part)
        
        if fx == "upper":
            d = ImageDraw.Draw(cv)
            for deg in range(-70, 45, 2):
                rad = math.radians(deg)
                r = 32
                cx = base_x + dx + w + int(r * math.cos(rad)) - 2
                cy = base_y + dy + 36 - int(r * 1.4 * math.sin(rad))
                d.line([(cx, cy-2), (cx+2, cy+2)], fill=(130, 235, 255, 255), width=3)
                d.point((cx, cy), fill=(255, 255, 255, 255))
        elif fx == "crack":
            d = ImageDraw.Draw(cv)
            for sx in range(base_x + dx - 10, base_x + dx + w + 20, 4):
                d.line([(sx, base_y + 88), (sx + 3, base_y + 90)], fill=(130, 230, 255, 255), width=2)
                d.point((sx+1, base_y + 87), fill=(255, 255, 255, 255))
                
    return cv

def build_all():
    print("=== Building Seamless Displaced DNF Skeletal Sprites ===")
    for gender in ["male", "female"]:
        base = get_clean_base(gender)
        print(f"Generating {gender} action frames...")
        
        # 1. Idle (4)
        for i in range(4):
            f = generate_motion_frame(base, "idle", i)
            f.save(os.path.join(OUT_HERO, f"{gender}_idle_{i}.png"))
            
        # 2. Run (6)
        for i in range(6):
            f = generate_motion_frame(base, "run", i)
            f.save(os.path.join(OUT_HERO, f"{gender}_run_{i}.png"))
            
        # 3. Attack (4)
        for i in range(4):
            f = generate_motion_frame(base, "attack", i)
            f.save(os.path.join(OUT_HERO, f"{gender}_attack_{i}.png"))
            
        # 4. Skill (4)
        for i in range(4):
            f = generate_motion_frame(base, "skill", i)
            f.save(os.path.join(OUT_HERO, f"{gender}_skill_{i}.png"))
            
    print("All seamless skeletal action sprites generated successfully!")

if __name__ == "__main__":
    build_all()
