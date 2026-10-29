# -*- coding: utf-8 -*-
"""
High-Fidelity Retro Master Skeletal Generator (Clean Weapon-Free Base)
"""
import os, math
from PIL import Image, ImageDraw

OUT_HERO = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
CANVAS_W = 120
CANVAS_H = 120

def load_master_and_flip(path, target_h=90):
    im = Image.open(path).convert("RGBA")
    im_flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    mw, mh = im_flipped.size
    target_w = int(mw * (target_h / mh))
    base = im_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    alpha = base.split()[3].point(lambda p: 255 if p > 70 else 0)
    rgb = base.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    return rgb

def clean_weapon_pixels(im):
    """마스터 스프라이트에서 칼자루, 코등이, 칼날 영역을 정밀하게 투명화"""
    w, h = im.size
    pix = im.load()
    out = im.copy()
    opix = out.load()
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            
            # 머리(y < 34)는 건드리지 않음
            if y < 34:
                continue
                
            is_skin = (r > 175 and g > 115 and b > 80 and r > g and g > b)
            is_shirt = (r > 140 and g > 135 and b > 125 and abs(r-g) < 25 and abs(g-b) < 25 and y < 62)
            is_jeans = (b > r and b > 55 and y >= 50)
            is_belt = (52 <= y <= 57 and r > 70 and g > 40 and 16 <= x <= 36)
            
            # 1) 등 뒤/허리 왼쪽 뒤로 삐져나온 칼자루/칼끝 (x < 16, y > 52)
            if x < 18 and y > 50 and not is_jeans and not is_skin:
                opix[x, y] = (0, 0, 0, 0)
                continue
                
            # 2) 오른손 뒤쪽/우측으로 삐져나온 칼자루 (x > 36, y > 40)
            if x > 36 and y > 40 and not is_skin and not is_shirt:
                opix[x, y] = (0, 0, 0, 0)
                continue
                
            # 3) 등 뒤 사선 칼집 (x in 18..36, y in 40..54)
            if 18 <= x <= 36 and 40 <= y <= 54 and not is_skin and not is_shirt and not is_belt:
                # 셔츠 색상으로 자연스럽게 인페인팅
                opix[x, y] = (210, 204, 194, 255)
                continue
                
    return out

def extract_clean_parts_male(master):
    cleaned = clean_weapon_pixels(master)
    w, h = cleaned.size
    
    # 1. 머리 (Head): y: 0 ~ 36
    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head.paste(cleaned.crop((0, 0, w, 36)), (0, 0))
    
    # 2. 몸통 (Torso): x: 12 ~ 42, y: 32 ~ 60
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso.paste(cleaned.crop((12, 32, 42, 60)), (12, 32))
    
    # 3. 왼팔 (L-Arm): x: 2 ~ 20, y: 32 ~ 58
    l_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_arm.paste(cleaned.crop((2, 32, 20, 58)), (2, 32))
    
    # 4. 오른팔 (R-Arm): x: 30 ~ 52, y: 32 ~ 62
    r_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_arm.paste(cleaned.crop((30, 32, 52, 62)), (30, 32))
    
    # 5. 왼다리 (L-Leg): x: 8 ~ 26, y: 56 ~ h
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg.paste(cleaned.crop((8, 56, 26, h)), (8, 56))
    
    # 6. 오른다리 (R-Leg): x: 26 ~ 46, y: 56 ~ h
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg.paste(cleaned.crop((26, 56, 46, h)), (26, 56))
    
    return head, torso, l_arm, r_arm, l_leg, r_leg

def extract_clean_parts_female(master):
    cleaned = clean_weapon_pixels(master)
    w, h = cleaned.size
    
    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head.paste(cleaned.crop((0, 0, w, 38)), (0, 0))
    
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso.paste(cleaned.crop((10, 32, 38, 60)), (10, 32))
    
    l_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_arm.paste(cleaned.crop((0, 32, 16, 58)), (0, 32))
    
    r_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_arm.paste(cleaned.crop((26, 32, 46, 62)), (26, 32))
    
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg.paste(cleaned.crop((6, 56, 24, h)), (6, 56))
    
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg.paste(cleaned.crop((22, 56, 42, h)), (22, 56))
    
    return head, torso, l_arm, r_arm, l_leg, r_leg

def rotate_part(part_img, pivot_xy, angle_deg):
    if angle_deg == 0:
        return part_img
    return part_img.rotate(-angle_deg, resample=Image.Resampling.NEAREST, center=pivot_xy)

def build_all():
    print("=== Generating Master Clean Skeletal Sprites (No Baked Weapons) ===")
    
    for female in [False, True]:
        prefix = "female" if female else "male"
        src_trans = f"assets/pixel_hero/retro_{prefix}_trans.png"
        master = load_master_and_flip(src_trans, target_h=90)
        mw, mh = master.size
        
        if female:
            head, torso, l_arm, r_arm, l_leg, r_leg = extract_clean_parts_female(master)
        else:
            head, torso, l_arm, r_arm, l_leg, r_leg = extract_clean_parts_male(master)
            
        base_x = (CANVAS_W - mw) // 2
        base_y = CANVAS_H - mh - 2
        
        p_head = (mw // 2, 34)
        p_torso = (mw // 2, 46)
        p_l_arm = (10, 34)
        p_r_arm = (36, 36)
        p_l_leg = (16, 56)
        p_r_leg = (30, 56)

        def composite_frame(head_deg=0, head_off=(0,0),
                            torso_deg=0, torso_off=(0,0),
                            la_deg=0, la_off=(0,0),
                            ra_deg=0, ra_off=(0,0),
                            ll_deg=0, ll_off=(0,0),
                            rl_deg=0, rl_off=(0,0)):
            canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
            
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

        # IDLE (4 프레임)
        idle_frames = [
            composite_frame(head_off=(0, 0), torso_off=(0, 0), la_deg=-2, ra_deg=2, ll_deg=0, rl_deg=0),
            composite_frame(head_off=(0, -1), torso_off=(0, -1), la_deg=-5, ra_deg=5, ll_deg=0, rl_deg=0),
            composite_frame(head_off=(0, -2), torso_off=(0, -2), la_deg=-7, ra_deg=7, ll_deg=-1, rl_deg=1),
            composite_frame(head_off=(0, -1), torso_off=(0, -1), la_deg=-4, ra_deg=4, ll_deg=0, rl_deg=0),
        ]
        for i, fr in enumerate(idle_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_idle_{i}.png"))

        # RUN (6 프레임 - 역동적 사지 교차!)
        run_frames = [
            # 0: 오른다리 앞, 왼다리 뒤, 왼팔 앞, 오른팔 뒤
            composite_frame(torso_deg=5, torso_off=(2, 1), head_off=(3, 1),
                            la_deg=22, la_off=(2, 1), ra_deg=-18, ra_off=(2, 1),
                            ll_deg=-22, ll_off=(-1, 1), rl_deg=20, rl_off=(2, 0)),
            # 1: 착지 가속
            composite_frame(torso_deg=7, torso_off=(3, 2), head_off=(4, 2),
                            la_deg=12, la_off=(3, 2), ra_deg=-8, ra_off=(3, 2),
                            ll_deg=-10, ll_off=(0, 2), rl_deg=8, rl_off=(2, 1)),
            # 2: 도약 체공
            composite_frame(torso_deg=4, torso_off=(2, -3), head_off=(3, -3),
                            la_deg=0, la_off=(2, -3), ra_deg=0, ra_off=(2, -3),
                            ll_deg=-3, ll_off=(1, -3), rl_deg=3, rl_off=(2, -3)),
            # 3: 왼다리 앞, 오른다리 뒤, 오른팔 앞, 왼팔 뒤 (반대 교차!)
            composite_frame(torso_deg=5, torso_off=(2, 1), head_off=(3, 1),
                            la_deg=-18, la_off=(2, 1), ra_deg=22, ra_off=(2, 1),
                            ll_deg=20, ll_off=(2, 0), rl_deg=-22, rl_off=(-1, 1)),
            # 4: 반대편 착지 가속
            composite_frame(torso_deg=7, torso_off=(3, 2), head_off=(4, 2),
                            la_deg=-8, la_off=(3, 2), ra_deg=12, ra_off=(3, 2),
                            ll_deg=8, ll_off=(2, 1), rl_deg=-10, rl_off=(0, 2)),
            # 5: 반대편 도약 체공
            composite_frame(torso_deg=4, torso_off=(2, -3), head_off=(3, -3),
                            la_deg=0, la_off=(2, -3), ra_deg=0, ra_off=(2, -3),
                            ll_deg=3, ll_off=(2, -3), rl_deg=-3, rl_off=(1, -3)),
        ]
        for i, fr in enumerate(run_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_run_{i}.png"))

        # ATTACK (4 프레임)
        attack_frames = [
            # 0: 백스윙 장전
            composite_frame(torso_deg=-6, torso_off=(-3, 1), head_off=(-4, 1),
                            la_deg=18, la_off=(-3, 1), ra_deg=-45, ra_off=(-4, 0),
                            ll_deg=-8, rl_deg=12),
            # 1: 전방 돌진 참격!
            composite_frame(torso_deg=8, torso_off=(7, 0), head_off=(8, 0),
                            la_deg=-25, la_off=(6, 0), ra_deg=50, ra_off=(8, -1),
                            ll_deg=-15, rl_deg=18),
            # 2: 전방 관통 유지
            composite_frame(torso_deg=6, torso_off=(8, 0), head_off=(9, 0),
                            la_deg=-15, la_off=(7, 0), ra_deg=60, ra_off=(9, -1),
                            ll_deg=-16, rl_deg=20),
            # 3: 착지 가드
            composite_frame(torso_deg=2, torso_off=(2, 0), head_off=(2, 0),
                            la_deg=5, ra_deg=10, ll_deg=-4, rl_deg=4),
        ]
        for i, fr in enumerate(attack_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_attack_{i}.png"))

        # SKILL (4 프레임)
        skill_frames = [
            composite_frame(torso_deg=4, torso_off=(0, 4), head_off=(0, 4),
                            la_deg=-12, la_off=(0, 4), ra_deg=-15, ra_off=(0, 4),
                            ll_deg=-10, rl_deg=10),
            composite_frame(torso_deg=6, torso_off=(3, -12), head_off=(4, -14),
                            la_deg=-30, la_off=(2, -12), ra_deg=70, ra_off=(5, -15),
                            ll_deg=8, rl_deg=12),
            composite_frame(torso_deg=4, torso_off=(5, -16), head_off=(6, -18),
                            la_deg=-20, la_off=(4, -16), ra_deg=55, ra_off=(6, -17),
                            ll_deg=12, rl_deg=10),
            composite_frame(torso_deg=6, torso_off=(3, 3), head_off=(3, 3),
                            la_deg=15, la_off=(3, 3), ra_deg=30, ra_off=(4, 2),
                            ll_deg=10, rl_deg=-8),
        ]
        for i, fr in enumerate(skill_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_skill_{i}.png"))

        print(f"Generated clean weapon-free {prefix} skeletal frames successfully!")

if __name__ == "__main__":
    build_all()
