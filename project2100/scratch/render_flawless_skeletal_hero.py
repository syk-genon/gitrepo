# -*- coding: utf-8 -*-
"""
Flawless Retro Master Skeletal Generator (DNF / StoneAge / HwanseChwihojeon Style)
- Generates weapon-free base frames facing RIGHT towards monsters
- Limbs move dynamically with natural limb rotation & perspective
- Empty hands line up perfectly with paperdoll weapon overlays
"""
import os
from PIL import Image

OUT_HERO = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
CANVAS_W = 120
CANVAS_H = 120

def load_master_and_flip(path, target_h=90):
    im = Image.open(path).convert("RGBA")
    # Face RIGHT towards monsters
    im_flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    mw, mh = im_flipped.size
    target_w = int(mw * (target_h / mh))
    base = im_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    alpha = base.split()[3].point(lambda p: 255 if p > 70 else 0)
    rgb = base.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    return rgb

def extract_parts(master, female=False):
    w, h = master.size
    
    # In flipped right-facing master:
    # Male: w ~ 56, h = 90
    # Female: w ~ 45, h = 90
    head_h = 36 if not female else 38
    torso_bottom = 60
    
    head = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head.paste(master.crop((0, 0, w, head_h)), (0, 0))
    
    torso = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso.paste(master.crop((int(w*0.18), head_h - 4, int(w*0.82), torso_bottom)), (int(w*0.18), head_h - 4))
    
    # Back arm (left arm when facing right): x: 0..w*0.35, y: head_h - 2..torso_bottom + 4
    l_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_arm.paste(master.crop((0, head_h - 2, int(w*0.36), torso_bottom + 4)), (0, head_h - 2))
    
    # Front arm (right arm when facing right): x: w*0.55..w, y: head_h - 2..torso_bottom + 6
    r_arm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_arm.paste(master.crop((int(w*0.52), head_h - 2, w, torso_bottom + 6)), (int(w*0.52), head_h - 2))
    
    # Back leg: x: int(w*0.10)..int(w*0.48), y: torso_bottom - 4..h
    l_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    l_leg.paste(master.crop((int(w*0.10), torso_bottom - 4, int(w*0.48), h)), (int(w*0.10), torso_bottom - 4))
    
    # Front leg: x: int(w*0.45)..w, y: torso_bottom - 4..h
    r_leg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_leg.paste(master.crop((int(w*0.45), torso_bottom - 4, w, h)), (int(w*0.45), torso_bottom - 4))
    
    return head, torso, l_arm, r_arm, l_leg, r_leg

def rotate_part(part_img, pivot_xy, angle_deg):
    if angle_deg == 0:
        return part_img
    return part_img.rotate(-angle_deg, resample=Image.Resampling.NEAREST, center=pivot_xy)

def build_skeletal_actions():
    for female in [False, True]:
        prefix = "female" if female else "male"
        src_master = f"assets/pixel_hero/master_{prefix}_clean.png"
        master = load_master_and_flip(src_master, target_h=90)
        mw, mh = master.size
        
        head, torso, l_arm, r_arm, l_leg, r_leg = extract_parts(master, female=female)
        
        base_x = (CANVAS_W - mw) // 2
        base_y = CANVAS_H - mh - 2
        
        p_head = (mw // 2, 34)
        p_torso = (mw // 2, 46)
        p_l_arm = (int(mw * 0.22), 36)
        p_r_arm = (int(mw * 0.68), 38)
        p_l_leg = (int(mw * 0.28), 58)
        p_r_leg = (int(mw * 0.62), 58)

        def composite_frame(head_deg=0, head_off=(0,0),
                            torso_deg=0, torso_off=(0,0),
                            la_deg=0, la_off=(0,0),
                            ra_deg=0, ra_off=(0,0),
                            ll_deg=0, ll_off=(0,0),
                            rl_deg=0, rl_off=(0,0)):
            canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
            
            # Layer order:
            # 1. Back Arm (left arm)
            rot_la = rotate_part(l_arm, p_l_arm, la_deg)
            canvas.paste(rot_la, (base_x + la_off[0], base_y + la_off[1]), rot_la)
            
            # 2. Back Leg (left leg)
            rot_ll = rotate_part(l_leg, p_l_leg, ll_deg)
            canvas.paste(rot_ll, (base_x + ll_off[0], base_y + ll_off[1]), rot_ll)
            
            # 3. Torso
            rot_t = rotate_part(torso, p_torso, torso_deg)
            canvas.paste(rot_t, (base_x + torso_off[0], base_y + torso_off[1]), rot_t)
            
            # 4. Front Leg (right leg)
            rot_rl = rotate_part(r_leg, p_r_leg, rl_deg)
            canvas.paste(rot_rl, (base_x + rl_off[0], base_y + rl_off[1]), rot_rl)
            
            # 5. Head
            rot_h = rotate_part(head, p_head, head_deg)
            canvas.paste(rot_h, (base_x + head_off[0], base_y + head_off[1]), rot_h)
            
            # 6. Front Arm (right arm)
            rot_ra = rotate_part(r_arm, p_r_arm, ra_deg)
            canvas.paste(rot_ra, (base_x + ra_off[0], base_y + ra_off[1]), rot_ra)
            
            return canvas

        # IDLE (4 frames)
        idle_frames = [
            composite_frame(head_off=(0, 0), torso_off=(0, 0), la_deg=-2, ra_deg=2, ll_deg=0, rl_deg=0),
            composite_frame(head_off=(0, -1), torso_off=(0, -1), la_deg=-5, ra_deg=5, ll_deg=0, rl_deg=0),
            composite_frame(head_off=(0, -2), torso_off=(0, -2), la_deg=-7, ra_deg=7, ll_deg=-1, rl_deg=1),
            composite_frame(head_off=(0, -1), torso_off=(0, -1), la_deg=-4, ra_deg=4, ll_deg=0, rl_deg=0),
        ]
        for i, fr in enumerate(idle_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_idle_{i}.png"))

        # RUN (6 frames - Dynamic DNF/StoneAge leg crossing and arm swinging!)
        run_frames = [
            # 0: Right leg forward, left leg back, left arm forward, right arm back
            composite_frame(torso_deg=4, torso_off=(2, 1), head_off=(3, 1),
                            la_deg=20, la_off=(2, 1), ra_deg=-16, ra_off=(2, 1),
                            ll_deg=-20, ll_off=(-1, 1), rl_deg=18, rl_off=(2, 0)),
            # 1: Landing compression
            composite_frame(torso_deg=6, torso_off=(3, 2), head_off=(4, 2),
                            la_deg=10, la_off=(3, 2), ra_deg=-8, ra_off=(3, 2),
                            ll_deg=-10, ll_off=(0, 2), rl_deg=8, rl_off=(2, 1)),
            # 2: Mid-jump air time
            composite_frame(torso_deg=3, torso_off=(2, -3), head_off=(3, -3),
                            la_deg=0, la_off=(2, -3), ra_deg=0, ra_off=(2, -3),
                            ll_deg=-3, ll_off=(1, -3), rl_deg=3, rl_off=(2, -3)),
            # 3: Left leg forward, right leg back, right arm forward, left arm back (Counter cross!)
            composite_frame(torso_deg=4, torso_off=(2, 1), head_off=(3, 1),
                            la_deg=-16, la_off=(2, 1), ra_deg=20, ra_off=(2, 1),
                            ll_deg=18, ll_off=(2, 0), rl_deg=-20, rl_off=(-1, 1)),
            # 4: Counter landing compression
            composite_frame(torso_deg=6, torso_off=(3, 2), head_off=(4, 2),
                            la_deg=-8, la_off=(3, 2), ra_deg=10, ra_off=(3, 2),
                            ll_deg=8, ll_off=(2, 1), rl_deg=-10, rl_off=(0, 2)),
            # 5: Counter mid-jump air time
            composite_frame(torso_deg=3, torso_off=(2, -3), head_off=(3, -3),
                            la_deg=0, la_off=(2, -3), ra_deg=0, ra_off=(2, -3),
                            ll_deg=3, ll_off=(2, -3), rl_deg=-3, rl_off=(1, -3)),
        ]
        for i, fr in enumerate(run_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_run_{i}.png"))

        # ATTACK (4 frames - Windup -> Lunge Thrust/Slash -> Followthrough -> Recovery)
        attack_frames = [
            # 0: Windup back
            composite_frame(torso_deg=-5, torso_off=(-2, 1), head_off=(-3, 1),
                            la_deg=16, la_off=(-2, 1), ra_deg=-38, ra_off=(-3, 0),
                            ll_deg=-6, rl_deg=10),
            # 1: Powerful forward lunge slash!
            composite_frame(torso_deg=8, torso_off=(8, 0), head_off=(9, 0),
                            la_deg=-22, la_off=(7, 0), ra_deg=48, ra_off=(9, -1),
                            ll_deg=-14, rl_deg=16),
            # 2: Forward penetration sustain
            composite_frame(torso_deg=6, torso_off=(6, 0), head_off=(7, 0),
                            la_deg=-14, la_off=(6, 0), ra_deg=55, ra_off=(7, -1),
                            ll_deg=-12, rl_deg=18),
            # 3: Guard recovery
            composite_frame(torso_deg=2, torso_off=(1, 0), head_off=(1, 0),
                            la_deg=4, ra_deg=8, ll_deg=-2, rl_deg=2),
        ]
        for i, fr in enumerate(attack_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_attack_{i}.png"))

        # SKILL (4 frames - Charge -> Skyward Burst Slash -> Climax Beam -> Landing)
        skill_frames = [
            # 0: Power crouching charge
            composite_frame(torso_deg=4, torso_off=(0, 4), head_off=(0, 4),
                            la_deg=-10, la_off=(0, 4), ra_deg=-12, ra_off=(0, 4),
                            ll_deg=-8, rl_deg=8),
            # 1: Skyward burst
            composite_frame(torso_deg=6, torso_off=(4, -14), head_off=(5, -16),
                            la_deg=-25, la_off=(3, -14), ra_deg=65, ra_off=(6, -16),
                            ll_deg=10, rl_deg=10),
            # 2: Mid-air climax power burst
            composite_frame(torso_deg=4, torso_off=(6, -18), head_off=(7, -20),
                            la_deg=-18, la_off=(5, -18), ra_deg=50, ra_off=(7, -18),
                            ll_deg=14, rl_deg=8),
            # 3: Heavy landing
            composite_frame(torso_deg=5, torso_off=(3, 3), head_off=(3, 3),
                            la_deg=12, la_off=(3, 3), ra_deg=26, ra_off=(4, 2),
                            ll_deg=8, rl_deg=-6),
        ]
        for i, fr in enumerate(skill_frames):
            fr.save(os.path.join(OUT_HERO, f"{prefix}_skill_{i}.png"))

        print(f"Generated immaculate skeletal frames for {prefix}!")

if __name__ == "__main__":
    build_skeletal_actions()
