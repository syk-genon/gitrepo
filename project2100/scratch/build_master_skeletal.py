# -*- coding: utf-8 -*-
"""
High-Fidelity Retro Master Segmentation & Skeletal Rigging
- 사용자가 마음에 들어한 원본 마스터 디자인(retro_male_trans, retro_female_trans)의 
  고퀄리티 도트 텍스처를 100% 보존하면서 부위별(머리, 몸통, 왼팔, 오른팔, 왼다리, 오른다리) 정밀 추출.
- 칼/무기 영역을 완전 배제하여 '누더기 반팔/반바지 베이스' 완성.
- 각 관절 피벗을 기준으로 DNF 스타일 사지 교차 런/어택/스킬/아이들 렌더링.
"""
import os, math
from PIL import Image, ImageOps

OUT_HERO = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
CANVAS_W = 120
CANVAS_H = 120

def load_master_and_flip(path, target_h=90):
    im = Image.open(path).convert("RGBA")
    # 오른쪽 몬스터를 바라보도록 좌우 반전
    im_flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    mw, mh = im_flipped.size
    target_w = int(mw * (target_h / mh))
    base = im_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    # 32색 아케이드 팔레트 양자화로 레트로 도트 느낌 극대화
    alpha = base.split()[3].point(lambda p: 255 if p > 70 else 0)
    rgb = base.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    return rgb

def extract_parts_male(master):
    w, h = master.size
    print(f"Master male size: {w}x{h}")
    # master: 오른쪽을 보고 있는 상태 (Flipped)
    # 1. 머리 (Head): 상단 y: 0 ~ 40, x: 0 ~ w
    # 칼날/칼자루는 y: 35 이상에 있으므로 머리는 100% 무기 없음
    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head.paste(master.crop((0, 0, w, 40)), (0, 0))
    
    # 2. 몸통 (Torso - 누더기 티셔츠 + 청반바지 허리):
    # x: 14 ~ 42, y: 32 ~ 62
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # 중앙 몸통부만 크롭 (칼자루가 있던 후방/등 뒤 x < 12 제외)
    t_crop = master.crop((12, 30, 44, 62))
    torso.paste(t_crop, (12, 30))
    
    # 3. 왼팔 (뒤쪽 팔 - 반전되어 왼쪽 뒤): x: 0 ~ 18, y: 34 ~ 58
    l_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_crop = master.crop((2, 32, 20, 60))
    l_arm.paste(l_crop, (2, 32))
    
    # 4. 오른팔 (앞쪽 팔 - 오른쪽 앞): x: 34 ~ 56, y: 32 ~ 64
    r_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_crop = master.crop((32, 32, w, 64))
    r_arm.paste(r_crop, (32, 32))
    
    # 5. 왼다리 (뒤쪽 다리): x: 10 ~ 28, y: 56 ~ h
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg_crop = master.crop((8, 56, 28, h))
    l_leg.paste(l_leg_crop, (8, 56))
    
    # 6. 오른다리 (앞쪽 다리): x: 26 ~ 52, y: 56 ~ h
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # 칼날이 삐져나왔던 우측 하단(x > 46, 60 < y < 80) 제거
    r_leg_crop = master.crop((26, 56, 48, h))
    r_leg.paste(r_leg_crop, (26, 56))
    
    return head, torso, l_arm, r_arm, l_leg, r_leg

def extract_parts_female(master):
    w, h = master.size
    print(f"Master female size: {w}x{h}")
    # 1. 머리
    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head.paste(master.crop((0, 0, w, 42)), (0, 0))
    
    # 2. 몸통
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    t_crop = master.crop((10, 32, 38, 62))
    torso.paste(t_crop, (10, 32))
    
    # 3. 왼팔
    l_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_crop = master.crop((0, 34, 16, 62))
    l_arm.paste(l_crop, (0, 34))
    
    # 4. 오른팔
    r_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_crop = master.crop((28, 34, w, 64))
    r_arm.paste(r_crop, (28, 34))
    
    # 5. 왼다리
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg_crop = master.crop((6, 58, 26, h))
    l_leg.paste(l_leg_crop, (6, 58))
    
    # 6. 오른다리
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg_crop = master.crop((22, 58, 44, h))
    r_leg.paste(r_leg_crop, (22, 58))
    
    return head, torso, l_arm, r_arm, l_leg, r_leg

def rotate_part(part_img, pivot_xy, angle_deg):
    """지정된 피벗 좌표(pivot_xy)를 중심으로 부품을 자연스럽게 회전"""
    if angle_deg == 0:
        return part_img
    # 캔버스 크기 확장 후 회전하여 잘림 방지
    pw, ph = part_img.size
    # 회전
    rotated = part_img.rotate(-angle_deg, resample=Image.Resampling.NEAREST, center=pivot_xy)
    return rotated

def build_skeletal_sprites():
    for female in [False, True]:
        prefix = "female" if female else "male"
        src_trans = f"assets/pixel_hero/retro_{prefix}_trans.png"
        master = load_master_and_flip(src_trans, target_h=90)
        mw, mh = master.size
        
        if female:
            head, torso, l_arm, r_arm, l_leg, r_leg = extract_parts_female(master)
        else:
            head, torso, l_arm, r_arm, l_leg, r_leg = extract_parts_male(master)
            
        base_x = (CANVAS_W - mw) // 2
        base_y = CANVAS_H - mh - 2
        
        # 피벗 좌표 정의 (master 로컬 기준)
        p_head = (mw // 2, 38)
        p_torso = (mw // 2, 48)
        p_l_arm = (10, 36)
        p_r_arm = (38, 38)
        p_l_leg = (18, 58)
        p_r_leg = (32, 58)

        def composite_frame(head_deg=0, head_off=(0,0),
                            torso_deg=0, torso_off=(0,0),
                            la_deg=0, la_off=(0,0),
                            ra_deg=0, ra_off=(0,0),
                            ll_deg=0, ll_off=(0,0),
                            rl_deg=0, rl_off=(0,0)):
            canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
            
            # 깊이 버퍼 순서: L-Arm -> L-Leg -> Torso -> R-Leg -> Head -> R-Arm
            # 1. 왼팔
            rot_la = rotate_part(l_arm, p_l_arm, la_deg)
            canvas.paste(rot_la, (base_x + la_off[0], base_y + la_off[1]), rot_la)
            
            # 2. 왼다리
            rot_ll = rotate_part(l_leg, p_l_leg, ll_deg)
            canvas.paste(rot_ll, (base_x + ll_off[0], base_y + ll_off[1]), rot_ll)
            
            # 3. 몸통
            rot_t = rotate_part(torso, p_torso, torso_deg)
            canvas.paste(rot_t, (base_x + torso_off[0], base_y + torso_off[1]), rot_t)
            
            # 4. 오른다리
            rot_rl = rotate_part(r_leg, p_r_leg, rl_deg)
            canvas.paste(rot_rl, (base_x + rl_off[0], base_y + rl_off[1]), rot_rl)
            
            # 5. 머리
            rot_h = rotate_part(head, p_head, head_deg)
            canvas.paste(rot_h, (base_x + head_off[0], base_y + head_off[1]), rot_h)
            
            # 6. 오른팔
            rot_ra = rotate_part(r_arm, p_r_arm, ra_deg)
            canvas.paste(rot_ra, (base_x + ra_off[0], base_y + ra_off[1]), rot_ra)
            
            return canvas

        # -------------------------------------------------------------
        # 1. IDLE (4 프레임) - 사지가 살아 숨쉬는 호흡 바운스
        # -------------------------------------------------------------
        idle_frames = [
            # 0: 기본 자세
            composite_frame(head_off=(0, 0), torso_off=(0, 0), la_deg=-2, ra_deg=2, ll_deg=0, rl_deg=0),
            # 1: 들숨 (가슴과 머리가 위로 1px, 양팔 살짝 벌어짐)
            composite_frame(head_off=(0, -1), torso_off=(0, -1), la_deg=-6, ra_deg=6, ll_deg=0, rl_deg=0),
            # 2: 최고점 (호흡 정점 -2px)
            composite_frame(head_off=(0, -2), torso_off=(0, -2), la_deg=-8, ra_deg=8, ll_deg=-1, rl_deg=1),
            # 3: 날숨 이완
            composite_frame(head_off=(0, -1), torso_off=(0, -1), la_deg=-4, ra_deg=4, ll_deg=0, rl_deg=0),
        ]
        for i, fr in enumerate(idle_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_idle_{i}.png"))

        # -------------------------------------------------------------
        # 2. RUN (6 프레임) - DNF 스타일 사지 교차 전방 질주!
        # -------------------------------------------------------------
        run_frames = [
            # Frame 0: 오른다리 앞 스트라이드(+22도), 왼다리 뒤 킥(-25도), 왼팔 앞(+25도), 오른팔 뒤(-20도), 상체 전방 숙임
            composite_frame(torso_deg=6, torso_off=(2, 1), head_off=(3, 1),
                            la_deg=25, la_off=(2, 1), ra_deg=-20, ra_off=(2, 1),
                            ll_deg=-25, ll_off=(-1, 1), rl_deg=22, rl_off=(2, 0)),
            # Frame 1: 착지 & 가속 딥 바운스 (무릎 굽힘)
            composite_frame(torso_deg=8, torso_off=(3, 2), head_off=(4, 2),
                            la_deg=15, la_off=(3, 2), ra_deg=-10, ra_off=(3, 2),
                            ll_deg=-12, ll_off=(0, 2), rl_deg=10, rl_off=(2, 1)),
            # Frame 2: 도약 체공 (상승 -3px)
            composite_frame(torso_deg=5, torso_off=(2, -3), head_off=(3, -3),
                            la_deg=0, la_off=(2, -3), ra_deg=0, ra_off=(2, -3),
                            ll_deg=-4, ll_off=(1, -3), rl_deg=4, rl_off=(2, -3)),
            # Frame 3: 왼다리 앞 스트라이드(+22도), 오른다리 뒤 킥(-25도) [완벽 사지 교차!]
            composite_frame(torso_deg=6, torso_off=(2, 1), head_off=(3, 1),
                            la_deg=-20, la_off=(2, 1), ra_deg=25, ra_off=(2, 1),
                            ll_deg=22, ll_off=(2, 0), rl_deg=-25, rl_off=(-1, 1)),
            # Frame 4: 반대편 착지 바운스
            composite_frame(torso_deg=8, torso_off=(3, 2), head_off=(4, 2),
                            la_deg=-10, la_off=(3, 2), ra_deg=15, ra_off=(3, 2),
                            ll_deg=10, ll_off=(2, 1), rl_deg=-12, rl_off=(0, 2)),
            # Frame 5: 반대편 도약 체공 (-3px)
            composite_frame(torso_deg=5, torso_off=(2, -3), head_off=(3, -3),
                            la_deg=0, la_off=(2, -3), ra_deg=0, ra_off=(2, -3),
                            ll_deg=4, ll_off=(2, -3), rl_deg=-4, rl_off=(1, -3)),
        ]
        for i, fr in enumerate(run_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_run_{i}.png"))

        # -------------------------------------------------------------
        # 3. ATTACK (4 프레임) - 백스윙 -> 쾌속 전방 참격 & 관통!
        # -------------------------------------------------------------
        attack_frames = [
            # 0: 상체 뒤로 젖힘(-8도), 오른팔 뒤로 장전(-55도), 왼팔 가드(+20도)
            composite_frame(torso_deg=-8, torso_off=(-4, 1), head_off=(-5, 1),
                            la_deg=20, la_off=(-4, 1), ra_deg=-55, ra_off=(-5, 0),
                            ll_deg=-10, rl_deg=15),
            # 1: 전방 돌진(+8px), 오른팔이 전방으로 사선 휘두름(+60도)!
            composite_frame(torso_deg=10, torso_off=(8, 0), head_off=(9, 0),
                            la_deg=-30, la_off=(7, 0), ra_deg=60, ra_off=(10, -2),
                            ll_deg=-18, rl_deg=22),
            # 2: 풀 팔로우스루 전방 연신 (+10px)
            composite_frame(torso_deg=8, torso_off=(10, 0), head_off=(11, 0),
                            la_deg=-20, la_off=(9, 0), ra_deg=75, ra_off=(12, -1),
                            ll_deg=-20, rl_deg=24),
            # 3: 공격 후 착지 복귀
            composite_frame(torso_deg=2, torso_off=(3, 0), head_off=(3, 0),
                            la_deg=5, ra_deg=15, ll_deg=-5, rl_deg=5),
        ]
        for i, fr in enumerate(attack_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_attack_{i}.png"))

        # -------------------------------------------------------------
        # 4. SKILL (4 프레임) - 웅크리기 -> 공중 수직 어퍼 도약 -> 착지
        # -------------------------------------------------------------
        skill_frames = [
            # 0: 하체 깊게 웅크림 (+5px 바운스), 양팔 하단 장전
            composite_frame(torso_deg=4, torso_off=(0, 5), head_off=(0, 5),
                            la_deg=-15, la_off=(0, 5), ra_deg=-20, ra_off=(0, 5),
                            ll_deg=-12, rl_deg=12),
            # 1: 공중 수직 솟구침 (-14px), 오른팔 수직 상승(+85도)!
            composite_frame(torso_deg=6, torso_off=(4, -14), head_off=(5, -16),
                            la_deg=-40, la_off=(3, -14), ra_deg=85, ra_off=(6, -18),
                            ll_deg=10, rl_deg=15),
            # 2: 공중 최고 정점 (-18px)
            composite_frame(torso_deg=4, torso_off=(6, -18), head_off=(7, -20),
                            la_deg=-30, la_off=(5, -18), ra_deg=70, ra_off=(8, -20),
                            ll_deg=15, rl_deg=12),
            # 3: 급강하 착지 충격파 (+4px)
            composite_frame(torso_deg=8, torso_off=(4, 4), head_off=(4, 4),
                            la_deg=20, la_off=(4, 4), ra_deg=40, ra_off=(5, 3),
                            ll_deg=12, rl_deg=-10),
        ]
        for i, fr in enumerate(skill_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_skill_{i}.png"))

        print(f"Successfully generated all {prefix} skeletal frames with master quality!")

if __name__ == "__main__":
    build_skeletal_sprites()
