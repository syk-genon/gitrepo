import os
import math
import shutil
from PIL import Image, ImageDraw

out_dir = r"C:\Users\exbxda13\project2100\assets\pixel_hero"
os.makedirs(out_dir, exist_ok=True)

CANVAS_W = 120
CANVAS_H = 120

def create_canvas():
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

def build_action_frames(female=True):
    prefix = "female" if female else "male"
    src_trans = f"assets/pixel_hero/retro_{prefix}_trans.png"
    master = Image.open(src_trans).convert("RGBA")
    
    # ⭐️ 몬스터(오른쪽)를 바라보도록 완벽히 좌우 반전(FLIP_LEFT_RIGHT) 적용!
    master_flipped = master.transpose(Image.FLIP_LEFT_RIGHT)
    mw, mh = master_flipped.size
    
    # Target character height on canvas: 94px
    target_h = 94
    target_w = int(mw * (target_h / mh))
    base_sprite = master_flipped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Quantize colors to vibrant 32-color retro arcade palette
    alpha = base_sprite.split()[3].point(lambda p: 255 if p > 75 else 0)
    rgb = base_sprite.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    
    sw, sh = rgb.size
    base_x = (CANVAS_W - sw) // 2
    base_y = CANVAS_H - sh - 2
    
    # ---------------------------------------------------------
    # 1. IDLE (4 frames) - 오른쪽 몬스터를 주시하며 호흡
    # ---------------------------------------------------------
    bobs = [0, -2, -3, -1]
    for i, bob in enumerate(bobs):
        cv = create_canvas()
        cv.paste(rgb, (base_x, base_y + bob), rgb)
        cv.save(os.path.join(out_dir, f"{prefix}_idle_{i}.png"))

    # ---------------------------------------------------------
    # 2. RUN (6 frames) - 오른쪽으로 몸을 숙이며 전방 질주
    # ---------------------------------------------------------
    run_offsets = [
        (2, -1),   # 0: 전방 착지
        (3,  1),   # 1: 딥 바운스
        (1, -2),   # 2: 도약
        (2, -1),   # 3: 보폭 교차
        (3,  1),   # 4: 딥 바운스
        (1, -2)    # 5: 가속
    ]
    for i, (rx, ry) in enumerate(run_offsets):
        cv = create_canvas()
        # 오른쪽으로 질주하듯 상체 전방 경사 (-0.10 shear)
        frame_spr = rgb.transform(rgb.size, Image.AFFINE, (1, -0.10, 0, 0, 1, 0), resample=Image.Resampling.NEAREST)
        cv.paste(frame_spr, (base_x + rx, base_y + ry), frame_spr)
        cv.save(os.path.join(out_dir, f"{prefix}_run_{i}.png"))

    # ---------------------------------------------------------
    # 3. ATTACK (4 frames) - 전방(오른쪽)을 향한 쾌속 발도 참격!
    # ---------------------------------------------------------
    # Frame 0: 뒤로 상체를 젖히며 검을 뽑는 백스윙 (b = 0.12)
    f0 = create_canvas()
    spr_windup = rgb.transform(rgb.size, Image.AFFINE, (1, 0.12, 0, 0, 1, 0), resample=Image.Resampling.NEAREST)
    f0.paste(spr_windup, (base_x - 6, base_y), spr_windup)
    f0.save(os.path.join(out_dir, f"{prefix}_attack_0.png"))

    # Frame 1: 몬스터를 향해 전방 돌진하며 시원하게 그어버리는 반달 참격파! (b = -0.16)
    f1 = create_canvas()
    spr_slash = rgb.transform(rgb.size, Image.AFFINE, (1, -0.16, 0, 0, 1, 0), resample=Image.Resampling.NEAREST)
    f1.paste(spr_slash, (base_x + 8, base_y), spr_slash)
    
    # 캐릭터 앞쪽(오른쪽)에 호쾌하게 터지는 푸른빛 참격 호(Slash Arc)
    slash_draw = ImageDraw.Draw(f1)
    for deg in range(-55, 65, 2):
        rad = math.radians(deg)
        r = 26
        cx = base_x + sw + int(r * math.cos(rad))
        cy = base_y + 52 - int(r * 1.3 * math.sin(rad))
        slash_draw.line([(cx-1, cy), (cx+2, cy+2)], fill=(120, 220, 255, 255), width=3)
        slash_draw.point((cx, cy), fill=(255, 255, 255, 255))
        slash_draw.point((cx+1, cy+1), fill=(255, 255, 255, 255))
    f1.save(os.path.join(out_dir, f"{prefix}_attack_1.png"))

    # Frame 2: 칼끝 전방 관통 및 섬광
    f2 = create_canvas()
    f2.paste(spr_slash, (base_x + 8, base_y), spr_slash)
    tip_draw = ImageDraw.Draw(f2)
    tx, ty = base_x + sw + 16, base_y + 52
    tip_draw.line([(tx-5, ty), (tx+5, ty)], fill=(255, 255, 255, 255), width=2)
    tip_draw.line([(tx, ty-5), (tx, ty+5)], fill=(255, 255, 255, 255), width=2)
    tip_draw.point((tx, ty), fill=(160, 240, 255, 255))
    f2.save(os.path.join(out_dir, f"{prefix}_attack_2.png"))

    # Frame 3: 검을 회수하며 착지 가드
    f3 = create_canvas()
    f3.paste(rgb, (base_x + 3, base_y), rgb)
    f3.save(os.path.join(out_dir, f"{prefix}_attack_3.png"))

    # ---------------------------------------------------------
    # 4. SKILL (4 frames) - 전방 도약 어퍼슬래시 & 지면 강타
    # ---------------------------------------------------------
    # Frame 0: 하단 웅크리기
    s0 = create_canvas()
    s0.paste(rgb, (base_x - 2, base_y + 5), rgb)
    s0.save(os.path.join(out_dir, f"{prefix}_skill_0.png"))

    # Frame 1: 공중으로 솟구치며 수직 상승 어퍼슬래시!
    s1 = create_canvas()
    s1.paste(rgb, (base_x + 6, base_y - 14), rgb)
    v_draw = ImageDraw.Draw(s1)
    arc_v_x = base_x + sw + 2
    arc_v_y = base_y + 36
    for deg in range(-70, 45, 2):
        rad = math.radians(deg)
        r = 30
        cx = arc_v_x + int(r * math.cos(rad))
        cy = arc_v_y - int(r * 1.4 * math.sin(rad))
        v_draw.line([(cx, cy-2), (cx+2, cy+2)], fill=(130, 230, 255, 255), width=3)
        v_draw.point((cx, cy), fill=(255, 255, 255, 255))
    s1.save(os.path.join(out_dir, f"{prefix}_skill_1.png"))

    # Frame 2: 공중 최고점 자세
    s2 = create_canvas()
    s2.paste(rgb, (base_x + 8, base_y - 18), rgb)
    s2.save(os.path.join(out_dir, f"{prefix}_skill_2.png"))

    # Frame 3: 지면 급강하 착지 & 충격파 크랙
    s3 = create_canvas()
    s3.paste(rgb, (base_x + 8, base_y + 4), rgb)
    slam_draw = ImageDraw.Draw(s3)
    for sx in range(base_x - 6, base_x + sw + 26, 4):
        slam_draw.line([(sx, base_y + 92), (sx + 3, base_y + 94)], fill=(120, 220, 255, 255), width=2)
        slam_draw.point((sx+1, base_y + 91), fill=(255, 255, 255, 255))
    s3.save(os.path.join(out_dir, f"{prefix}_skill_3.png"))

    print(f"Generated all {prefix} action frames (Faced Right -> Towards Monsters) successfully!")

def sync_avatars():
    # Sync idle_0 as default preview and base trainee in pixel_agents
    shutil.copy("assets/pixel_hero/female_idle_0.png", "assets/pixel_agents/agent_female_trainee_1.png")
    shutil.copy("assets/pixel_hero/male_idle_0.png", "assets/pixel_agents/agent_male_trainee_1.png")
    shutil.copy("assets/pixel_hero/female_idle_0.png", "assets/pixel_hero/preview_classic_female.png")
    shutil.copy("assets/pixel_hero/male_idle_0.png", "assets/pixel_hero/preview_classic_male.png")
    
    # Also flip high-res original agent trainee 1 so illustration mode also faces right
    for g in ["female", "male"]:
        path = f"assets/agents/agent_{g}_trainee_1.png"
        if os.path.exists(path):
            im = Image.open(path).convert("RGBA")
            # Save right-facing version
            flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
            flipped.save(path)
            print(f"Flipped illustration mode {path} to face right!")

if __name__ == "__main__":
    build_action_frames(female=True)
    build_action_frames(female=False)
    sync_avatars()
    print("All flipped action sprites & avatars fully synced!")
