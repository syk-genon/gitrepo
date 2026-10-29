import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

SUMMONS_DIR = r"D:\workspace\GEMINI\project_necro\assets\summons"
SKILLS_DIR = r"D:\workspace\GEMINI\project_necro\assets\pixel_vfx\skills"
os.makedirs(SUMMONS_DIR, exist_ok=True)
os.makedirs(SKILLS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. 16비트 도트 부하(소환수) 스프라이트 생성
# -------------------------------------------------------------
def create_skeleton_warrior():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # 두개골 (Skull)
    d.rectangle([26, 12, 37, 24], fill=(225, 220, 205, 255))
    d.rectangle([28, 24, 35, 27], fill=(200, 195, 180, 255)) # 턱
    # 녹색 영혼 불꽃 안광
    d.point([(29, 18), (34, 18)], fill=(0, 255, 170, 255))
    d.point([(28, 18), (30, 18), (33, 18), (35, 18)], fill=(0, 200, 130, 200))
    # 이마 균열
    d.line([(31, 13), (33, 16)], fill=(120, 110, 95, 255))
    
    # 목 척추
    d.line([(31, 28), (31, 31)], fill=(190, 185, 170, 255), width=2)
    
    # 흉곽 갈비뼈 (Ribcage)
    d.line([(29, 32), (33, 32)], fill=(210, 205, 190, 255), width=2)
    d.line([(27, 35), (35, 35)], fill=(210, 205, 190, 255), width=2)
    d.line([(28, 38), (34, 38)], fill=(210, 205, 190, 255), width=2)
    d.line([(30, 41), (32, 41)], fill=(180, 175, 160, 255), width=2)
    d.line([(31, 32), (31, 42)], fill=(160, 150, 135, 255), width=2) # 척추골
    
    # 녹색 영혼의 핵 (흉곽 내부 영혼석)
    d.ellipse([29, 34, 33, 38], fill=(0, 255, 150, 220))
    
    # 골반 & 다리 뼈
    d.rectangle([28, 43, 34, 45], fill=(195, 190, 175, 255))
    # 왼다리
    d.line([(29, 46), (28, 54)], fill=(205, 200, 185, 255), width=2)
    d.line([(28, 54), (27, 60)], fill=(190, 185, 170, 255), width=2)
    d.point([(26, 60), (27, 60), (28, 60)], fill=(160, 150, 135, 255))
    # 오른다리
    d.line([(33, 46), (34, 54)], fill=(205, 200, 185, 255), width=2)
    d.line([(34, 54), (35, 60)], fill=(190, 185, 170, 255), width=2)
    d.point([(34, 60), (35, 60), (36, 60)], fill=(160, 150, 135, 255))
    
    # 왼팔: 낡은 방패 들기
    d.line([(27, 33), (22, 38)], fill=(200, 195, 180, 255), width=2)
    d.line([(22, 38), (20, 43)], fill=(180, 175, 160, 255), width=2)
    # 녹슨 원형 방패 (Rust Shield)
    d.ellipse([12, 33, 24, 49], fill=(90, 60, 45, 255), outline=(140, 100, 70, 255), width=2)
    d.ellipse([16, 39, 20, 43], fill=(70, 70, 80, 255), outline=(160, 150, 130, 255))
    
    # 오른팔: 녹슨 뼈검 (Bone Blade)
    d.line([(35, 33), (40, 37)], fill=(200, 195, 180, 255), width=2)
    d.line([(40, 37), (43, 41)], fill=(180, 175, 160, 255), width=2)
    # 뼈검 칼날 (우상향으로 비스듬히 겨눔)
    d.line([(43, 41), (55, 25)], fill=(230, 225, 215, 255), width=3)
    d.line([(44, 40), (56, 24)], fill=(0, 255, 170, 180), width=1) # 칼날 영혼광
    d.rectangle([41, 41, 45, 43], fill=(120, 90, 50, 255)) # 힐트
    
    img.save(os.path.join(SUMMONS_DIR, "minion_skeleton_warrior.png"))

def create_skeleton_archer():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # 두개골 & 누더기 두건
    d.rectangle([25, 11, 38, 20], fill=(65, 45, 75, 255)) # 자주색 두건
    d.rectangle([27, 16, 36, 25], fill=(225, 220, 205, 255))
    d.rectangle([29, 25, 34, 27], fill=(190, 185, 170, 255))
    # 안광
    d.point([(30, 19), (34, 19)], fill=(0, 255, 200, 255))
    
    # 척추 및 갈비뼈
    d.line([(31, 28), (31, 42)], fill=(180, 170, 155, 255), width=2)
    d.line([(28, 32), (34, 32)], fill=(210, 205, 190, 255), width=2)
    d.line([(27, 36), (35, 36)], fill=(210, 205, 190, 255), width=2)
    d.line([(29, 40), (33, 40)], fill=(190, 185, 170, 255), width=2)
    # 등에 멘 화살통
    d.line([(24, 28), (28, 44)], fill=(110, 75, 45, 255), width=3)
    d.line([(23, 24), (25, 29)], fill=(220, 220, 200, 255), width=1) # 화살 깃
    d.line([(25, 24), (27, 29)], fill=(220, 220, 200, 255), width=1)
    
    # 골반 & 다리
    d.rectangle([28, 43, 34, 45], fill=(195, 190, 175, 255))
    d.line([(29, 46), (28, 59)], fill=(200, 195, 180, 255), width=2)
    d.line([(33, 46), (35, 59)], fill=(200, 195, 180, 255), width=2)
    
    # 팔과 뼈 활 (Bone Bow) 조준
    d.line([(27, 33), (23, 36)], fill=(200, 195, 180, 255), width=2)
    d.line([(35, 33), (45, 33)], fill=(200, 195, 180, 255), width=2)
    # 활대 곡선
    d.arc([40, 18, 54, 48], start=270, end=90, fill=(215, 205, 185, 255), width=3)
    d.line([(47, 18), (47, 48)], fill=(0, 255, 220, 200), width=1) # 시위 (빛의 활시위)
    # 걸린 영혼 화살
    d.line([(38, 33), (55, 33)], fill=(0, 255, 170, 255), width=2)
    d.polygon([(55, 31), (59, 33), (55, 35)], fill=(100, 255, 220, 255))
    
    img.save(os.path.join(SUMMONS_DIR, "minion_skeleton_archer.png"))

def create_skeleton_mage():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # 로브 (Tattered Necro Robe)
    d.polygon([(31, 24), (20, 60), (42, 60)], fill=(35, 25, 50, 255), outline=(75, 50, 100, 255))
    d.line([(22, 60), (40, 60)], fill=(15, 10, 25, 255), width=2)
    
    # 해골 얼굴 & 로브 후드
    d.ellipse([24, 10, 38, 25], fill=(25, 15, 35, 255))
    d.rectangle([27, 15, 35, 24], fill=(225, 220, 205, 255))
    d.point([(29, 18), (33, 18)], fill=(180, 0, 255, 255)) # 보라색 비전 안광
    
    # 목걸이 영혼 펜던트
    d.ellipse([29, 28, 33, 32], fill=(0, 255, 200, 255), outline=(255, 215, 0, 255))
    
    # 사령 지팡이 (Necromancer Bone Staff)
    d.line([(45, 12), (45, 58)], fill=(140, 110, 80, 255), width=3)
    # 지팡이 머리: 미니 스컬 오브
    d.ellipse([41, 6, 49, 14], fill=(230, 225, 215, 255), outline=(120, 90, 60, 255))
    d.point([(43, 9), (47, 9)], fill=(0, 255, 150, 255))
    # 지팡이 상단 회전하는 소환 룬 링
    d.ellipse([38, 2, 52, 16], outline=(0, 255, 180, 180), width=1)
    d.ellipse([36, 0, 54, 18], outline=(150, 50, 255, 130), width=1)
    
    # 마법 시전하는 왼손
    d.line([(25, 30), (18, 32)], fill=(200, 195, 180, 255), width=2)
    d.ellipse([14, 29, 19, 34], fill=(0, 255, 180, 255)) # 손끝 마법구
    
    img.save(os.path.join(SUMMONS_DIR, "minion_skeleton_mage.png"))

def create_death_knight():
    img = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # 망토 (Tattered Dark Cape)
    d.polygon([(26, 26), (12, 66), (40, 66)], fill=(20, 10, 30, 255), outline=(60, 20, 80, 255))
    
    # 풀 플레이트 흑철 갑옷 몸체
    d.rectangle([28, 24, 46, 46], fill=(45, 45, 55, 255), outline=(80, 80, 100, 255), width=2)
    # 가슴팍 룬 해골 문양
    d.ellipse([34, 30, 40, 36], fill=(20, 15, 25, 255), outline=(160, 0, 220, 255))
    
    # 투구 (뿔 달린 암흑 투구)
    d.rectangle([30, 12, 44, 24], fill=(55, 55, 65, 255), outline=(90, 90, 115, 255), width=2)
    # 붉은/보라 바이저 안광
    d.line([(32, 18), (42, 18)], fill=(255, 0, 90, 255), width=2)
    # 좌우 투구 뿔 (Demonic Horns)
    d.line([(30, 14), (24, 6)], fill=(120, 120, 140, 255), width=3)
    d.line([(44, 14), (50, 6)], fill=(120, 120, 140, 255), width=3)
    
    # 스파이크 견갑 (Shoulder Plates)
    d.polygon([(24, 22), (28, 22), (22, 30)], fill=(70, 70, 85, 255), outline=(100, 100, 130, 255))
    d.polygon([(46, 22), (50, 22), (52, 30)], fill=(70, 70, 85, 255), outline=(100, 100, 130, 255))
    
    # 중갑 다리
    d.rectangle([29, 47, 36, 68], fill=(45, 45, 55, 255), outline=(80, 80, 100, 255))
    d.rectangle([38, 47, 45, 68], fill=(45, 45, 55, 255), outline=(80, 80, 100, 255))
    
    # 저주받은 대검 (Cursed Greatsword)
    d.line([(52, 10), (52, 64)], fill=(160, 160, 180, 255), width=4)
    d.line([(52, 14), (52, 54)], fill=(220, 0, 120, 220), width=2) # 검날 흑염 오라
    d.rectangle([(47, 48), (57, 51)], fill=(200, 160, 40, 255)) # 십자 코등이
    d.line([(52, 51), (52, 60)], fill=(90, 60, 30, 255), width=3) # 손잡이
    d.ellipse([(50, 60), (54, 64)], fill=(180, 0, 0, 255)) # 폼멜 보석
    
    img.save(os.path.join(SUMMONS_DIR, "minion_death_knight.png"))

def create_frost_dragon():
    img = Image.new("RGBA", (128, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # 빙룡(Frost Dragon) 영체: 반투명 얼음 날개
    d.polygon([(64, 45), (10, 15), (35, 65)], fill=(140, 220, 255, 140), outline=(200, 245, 255, 220), width=2)
    d.polygon([(64, 45), (118, 15), (93, 65)], fill=(140, 220, 255, 140), outline=(200, 245, 255, 220), width=2)
    # 날개 뼈대 고드름
    d.line([(64, 45), (12, 16)], fill=(230, 250, 255, 255), width=3)
    d.line([(64, 45), (116, 16)], fill=(230, 250, 255, 255), width=3)
    
    # 용 몸체 (뱀처럼 유려한 얼음 척추)
    body_points = [(64, 25), (66, 38), (62, 52), (65, 66), (62, 80), (60, 90)]
    for i in range(len(body_points)-1):
        d.line([body_points[i], body_points[i+1]], fill=(160, 230, 255, 255), width=7 - i)
    
    # 용 머리
    d.polygon([(56, 12), (72, 12), (64, 28)], fill=(180, 240, 255, 255), outline=(230, 255, 255, 255), width=2)
    # 얼음 뿔
    d.line([(58, 12), (52, 2)], fill=(220, 250, 255, 255), width=3)
    d.line([(70, 12), (76, 2)], fill=(220, 250, 255, 255), width=3)
    # 사령 푸른 안광
    d.point([(60, 18), (68, 18)], fill=(0, 255, 240, 255))
    
    # 브레스 입자 (다이아몬드 더스트)
    for bx, by in [(64, 32), (62, 38), (66, 42), (58, 48), (70, 48), (64, 55)]:
        d.rectangle([bx-1, by-1, bx+1, by+1], fill=(240, 255, 255, 230))
        
    img.save(os.path.join(SUMMONS_DIR, "minion_frost_dragon.png"))

def create_shadow_clone():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 암살자 섀도우 분신
    d.ellipse([26, 12, 38, 24], fill=(20, 10, 30, 200))
    d.rectangle([25, 24, 39, 44], fill=(30, 15, 45, 200))
    d.rectangle([26, 44, 32, 60], fill=(20, 10, 30, 200))
    d.rectangle([33, 44, 39, 60], fill=(20, 10, 30, 200))
    # 붉은 눈빛
    d.point([(29, 17), (35, 17)], fill=(255, 20, 60, 255))
    # 그림자 단도 쌍검
    d.line([(22, 35), (14, 45)], fill=(120, 40, 160, 240), width=3)
    d.line([(42, 35), (50, 45)], fill=(120, 40, 160, 240), width=3)
    # 암흑 안개 아지랑이
    for py in range(10, 60, 4):
        d.arc([20, py, 44, py+8], start=0, end=180, fill=(80, 20, 120, 120), width=1)
    img.save(os.path.join(SUMMONS_DIR, "minion_shadow_clone.png"))

def create_holy_guardian():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 성스러운 황금 수호령
    # 날개
    d.polygon([(32, 28), (10, 10), (22, 45)], fill=(255, 240, 180, 170), outline=(255, 215, 0, 255), width=2)
    d.polygon([(32, 28), (54, 10), (42, 45)], fill=(255, 240, 180, 170), outline=(255, 215, 0, 255), width=2)
    # 황금 갑주 몸체
    d.rectangle([26, 20, 38, 42], fill=(240, 195, 60, 255), outline=(255, 255, 200, 255), width=2)
    # 투구와 천사 링
    d.ellipse([27, 8, 37, 18], fill=(255, 220, 90, 255), outline=(255, 255, 255, 255))
    d.ellipse([25, 2, 39, 7], outline=(255, 255, 150, 255), width=2)
    # 황금 대방패
    d.polygon([(38, 22), (52, 22), (48, 52), (38, 48)], fill=(255, 215, 0, 255), outline=(255, 255, 240, 255), width=2)
    d.line([(45, 26), (45, 44)], fill=(255, 255, 255, 255), width=2)
    d.line([(40, 34), (50, 34)], fill=(255, 255, 255, 255), width=2)
    img.save(os.path.join(SUMMONS_DIR, "minion_holy_guardian.png"))

print("Generating 7 minion sprites...")
create_skeleton_warrior()
create_skeleton_archer()
create_skeleton_mage()
create_death_knight()
create_frost_dragon()
create_shadow_clone()
create_holy_guardian()
print("Minion sprites generated successfully!")

# -------------------------------------------------------------
# 2. 고퀄리티 16비트 도트 마법진 및 비주얼 이펙트 생성기 (72종)
# -------------------------------------------------------------
def draw_magic_circle(draw, center, radius, color_outer, color_inner, rune_type="geom"):
    cx, cy = center
    # 외곽 룬 링
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=color_outer, width=2)
    draw.ellipse([cx - radius + 4, cy - radius + 4, cx + radius - 4, cy + radius - 4], outline=color_inner, width=1)
    
    # 내부 기하학 문양
    if rune_type == "star":
        # 6각성 (Hexagram)
        pts1 = [(cx + radius * math.cos(i * math.pi / 3), cy + radius * math.sin(i * math.pi / 3)) for i in range(6)]
        for i in range(6):
            draw.line([pts1[i], pts1[(i+2)%6]], fill=color_inner, width=1)
    elif rune_type == "square":
        # 이중 사각형
        r_in = radius * 0.7
        draw.polygon([(cx, cy-r_in), (cx+r_in, cy), (cx, cy+r_in), (cx-r_in, cy)], outline=color_inner)
        draw.polygon([(cx-r_in*0.7, cy-r_in*0.7), (cx+r_in*0.7, cy-r_in*0.7), (cx+r_in*0.7, cy+r_in*0.7), (cx-r_in*0.7, cy+r_in*0.7)], outline=color_outer)
    elif rune_type == "cross":
        # 성스러운 십자가
        draw.line([(cx, cy - radius + 6), (cx, cy + radius - 6)], fill=color_inner, width=3)
        draw.line([(cx - radius + 8), cy, (cx + radius - 8), cy], fill=color_inner, width=3)
        draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill=color_outer)
    elif rune_type == "spiral":
        # 소용돌이
        for a in range(0, 360, 15):
            rad = math.radians(a)
            r = (a / 360.0) * radius
            px = int(cx + r * math.cos(rad))
            py = int(cy + r * math.sin(rad))
            draw.point([(px, py), (px+1, py)], fill=color_inner)
    elif rune_type == "skull":
        # 사령 해골 심볼
        draw.ellipse([cx-10, cy-12, cx+10, cy+6], fill=color_inner)
        draw.rectangle([cx-6, cy+5, cx+6, cy+11], fill=color_inner)
        draw.point([(cx-4, cy-3), (cx+4, cy-3)], fill=(0, 0, 0, 255))
        draw.line([(cx-3, cy+10), (cx+3, cy+10)], fill=(0, 0, 0, 255))

    # 외곽 룬 문자 점들
    for a in range(0, 360, 30):
        rad = math.radians(a)
        rx = int(cx + (radius - 2) * math.cos(rad))
        ry = int(cy + (radius - 2) * math.sin(rad))
        draw.rectangle([rx-1, ry-1, rx+1, ry+1], fill=color_outer)

def generate_enhanced_skills_vfx():
    # 72종 스킬 비주얼 테마 정의
    configs = {
        # 💀 네크로맨서
        "vfx_necro_1": ("skull", (0, 255, 170, 255), (20, 80, 50, 220), "circle"),
        "vfx_necro_2": ("spiral", (255, 40, 80, 255), (120, 0, 40, 220), "blood_burst"),
        "vfx_necro_3": ("geom", (220, 220, 200, 255), (0, 255, 170, 200), "spear"),
        "vfx_necro_4": ("square", (0, 255, 200, 255), (20, 50, 70, 220), "shield"),
        "vfx_necro_5": ("spiral", (180, 0, 255, 255), (50, 0, 100, 220), "curse"),
        "vfx_necro_ult": ("star", (100, 240, 255, 255), (0, 255, 200, 240), "dragon_blizzard"),

        # 🛡️ 가디언
        "vfx_guard_1": ("square", (255, 215, 0, 255), (255, 160, 20, 220), "shield"),
        "vfx_guard_2": ("cross", (255, 230, 100, 255), (200, 140, 0, 220), "slash"),
        "vfx_guard_3": ("star", (255, 200, 50, 255), (255, 255, 180, 240), "taunt"),
        "vfx_guard_4": ("square", (0, 230, 255, 255), (255, 215, 0, 220), "iron_wall"),
        "vfx_guard_5": ("geom", (255, 180, 0, 255), (150, 70, 0, 240), "slam"),
        "vfx_guard_ult": ("cross", (255, 245, 150, 255), (255, 190, 0, 255), "aegis_domain"),

        # 🏹 스나이퍼
        "vfx_snip_1": ("cross", (0, 255, 255, 255), (255, 0, 80, 220), "crosshair"),
        "vfx_snip_2": ("geom", (0, 240, 255, 255), (100, 200, 255, 200), "piercing_shot"),
        "vfx_snip_3": ("spiral", (255, 140, 0, 255), (255, 50, 0, 220), "bomb"),
        "vfx_snip_4": ("square", (0, 255, 180, 255), (0, 150, 100, 200), "camou"),
        "vfx_snip_5": ("cross", (255, 0, 100, 255), (0, 255, 255, 220), "headshot"),
        "vfx_snip_ult": ("star", (0, 255, 255, 255), (255, 0, 120, 255), "orbital_laser"),

        # ✝️ 프리스트
        "vfx_priest_1": ("cross", (255, 240, 180, 255), (255, 215, 0, 220), "heal"),
        "vfx_priest_2": ("cross", (255, 255, 220, 255), (255, 180, 0, 240), "holy_light"),
        "vfx_priest_3": ("star", (255, 215, 0, 255), (255, 255, 255, 200), "blessing"),
        "vfx_priest_4": ("square", (255, 240, 120, 255), (200, 170, 50, 200), "dispel"),
        "vfx_priest_5": ("cross", (255, 255, 200, 255), (255, 120, 0, 220), "judgment"),
        "vfx_priest_ult": ("star", (255, 255, 255, 255), (255, 215, 0, 255), "sanctuary"),

        # ⚔️ 소드마스터
        "vfx_sm_1": ("geom", (255, 255, 200, 255), (100, 180, 255, 220), "slash"),
        "vfx_sm_2": ("spiral", (120, 200, 255, 255), (255, 255, 255, 240), "iaido"),
        "vfx_sm_3": ("star", (80, 180, 255, 255), (200, 230, 255, 220), "sword_aura"),
        "vfx_sm_4": ("square", (255, 220, 100, 255), (255, 255, 255, 220), "parry"),
        "vfx_sm_5": ("geom", (100, 220, 255, 255), (50, 100, 255, 220), "wind_cutter"),
        "vfx_sm_ult": ("star", (255, 230, 100, 255), (80, 200, 255, 255), "dragon_slash"),

        # 🗡️ 암살자
        "vfx_as_1": ("spiral", (255, 30, 90, 255), (50, 10, 30, 220), "shadow_step"),
        "vfx_as_2": ("geom", (255, 0, 60, 255), (160, 0, 90, 220), "backstab"),
        "vfx_as_3": ("spiral", (0, 255, 120, 255), (140, 0, 200, 220), "poison"),
        "vfx_as_4": ("square", (100, 50, 150, 255), (30, 15, 45, 220), "smoke"),
        "vfx_as_5": ("geom", (255, 50, 100, 255), (200, 0, 60, 240), "twin_fang"),
        "vfx_as_ult": ("star", (255, 0, 70, 255), (20, 10, 40, 255), "shadow_dance"),

        # 🔥 버서커
        "vfx_ber_1": ("spiral", (255, 40, 0, 255), (150, 0, 0, 240), "blood_slash"),
        "vfx_ber_2": ("spiral", (255, 80, 0, 255), (255, 0, 40, 240), "whirlwind"),
        "vfx_ber_3": ("star", (255, 0, 0, 255), (255, 120, 0, 220), "frenzy"),
        "vfx_ber_4": ("geom", (255, 100, 20, 255), (120, 20, 0, 220), "earthquake"),
        "vfx_ber_5": ("cross", (255, 20, 20, 255), (200, 0, 80, 220), "life_drain"),
        "vfx_ber_ult": ("star", (255, 200, 50, 255), (255, 0, 0, 255), "hellbound"),

        # ❄️ 크라이오맨서
        "vfx_cryo_1": ("geom", (180, 240, 255, 255), (100, 200, 255, 220), "ice_spear"),
        "vfx_cryo_2": ("star", (200, 245, 255, 255), (80, 180, 255, 220), "frost_nova"),
        "vfx_cryo_3": ("square", (160, 230, 255, 255), (220, 250, 255, 200), "ice_shield"),
        "vfx_cryo_4": ("spiral", (140, 220, 255, 255), (50, 150, 255, 220), "blizzard"),
        "vfx_cryo_5": ("geom", (220, 250, 255, 255), (100, 210, 255, 240), "glacier_prison"),
        "vfx_cryo_ult": ("star", (240, 255, 255, 255), (120, 220, 255, 255), "diamond_dust"),

        # ⚡ 뇌신술사
        "vfx_storm_1": ("geom", (255, 255, 100, 255), (180, 100, 255, 220), "lightning"),
        "vfx_storm_2": ("spiral", (200, 255, 255, 255), (255, 230, 50, 220), "chain_lightning"),
        "vfx_storm_3": ("star", (255, 255, 150, 255), (150, 50, 255, 220), "thunder_surge"),
        "vfx_storm_4": ("square", (255, 255, 200, 255), (100, 200, 255, 220), "plasma_shield"),
        "vfx_storm_5": ("geom", (255, 240, 80, 255), (200, 50, 255, 240), "lightning_rod"),
        "vfx_storm_ult": ("star", (255, 255, 255, 255), (255, 220, 50, 255), "god_of_thunder"),

        # 👊 권왕 (몽크)
        "vfx_mk_1": ("spiral", (255, 180, 40, 255), (255, 230, 100, 220), "hadouken"),
        "vfx_mk_2": ("geom", (255, 200, 50, 255), (200, 100, 20, 220), "dragon_kick"),
        "vfx_mk_3": ("star", (255, 230, 120, 255), (255, 160, 20, 220), "iron_body"),
        "vfx_mk_4": ("square", (255, 215, 0, 255), (255, 255, 200, 220), "inch_punch"),
        "vfx_mk_5": ("spiral", (255, 150, 30, 255), (255, 240, 120, 220), "palm_strike"),
        "vfx_mk_ult": ("star", (255, 255, 150, 255), (255, 140, 0, 255), "108_fists"),

        # 🔮 초능력자
        "vfx_psi_1": ("spiral", (180, 80, 255, 255), (0, 240, 255, 220), "telekinesis"),
        "vfx_psi_2": ("star", (200, 100, 255, 255), (100, 0, 200, 220), "warp_bubble"),
        "vfx_psi_3": ("square", (150, 120, 255, 255), (0, 255, 255, 200), "psi_barrier"),
        "vfx_psi_4": ("geom", (220, 150, 255, 255), (255, 50, 150, 220), "mind_blast"),
        "vfx_psi_5": ("cross", (160, 80, 255, 255), (0, 220, 255, 220), "singularity"),
        "vfx_psi_ult": ("star", (255, 100, 255, 255), (0, 255, 255, 255), "dimensional_rift"),

        # 💀 데스나이트
        "vfx_dk_1": ("geom", (255, 20, 80, 255), (40, 10, 40, 240), "death_strike"),
        "vfx_dk_2": ("cross", (200, 0, 60, 255), (120, 0, 180, 220), "soul_reap"),
        "vfx_dk_3": ("star", (160, 0, 220, 255), (30, 10, 40, 220), "dark_aura"),
        "vfx_dk_4": ("square", (220, 0, 100, 255), (60, 20, 80, 220), "bone_shield"),
        "vfx_dk_5": ("spiral", (255, 40, 100, 255), (140, 0, 200, 220), "blood_drain"),
        "vfx_dk_ult": ("skull", (255, 0, 60, 255), (180, 0, 255, 255), "black_guillotine")
    }

    print("Generating enhanced 72 skills pixel VFX...")
    for filename, (rune_style, c1, c2, shape) in configs.items():
        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        # 1. 중앙 회전 룬 마법진 (반경 42px)
        draw_magic_circle(d, (64, 64), 42, c1, c2, rune_type=rune_style)
        
        # 2. 중심부 고유 스킬 모양 드로잉
        if "spear" in shape:
            d.line([(28, 96), (98, 28)], fill=c1, width=5)
            d.polygon([(98, 28), (106, 20), (90, 26)], fill=c2)
            d.line([(32, 92), (94, 32)], fill=(255, 255, 255, 255), width=2)
        elif "crosshair" in shape:
            d.ellipse([44, 44, 84, 84], outline=c1, width=2)
            d.line([(64, 36), (64, 92)], fill=c1, width=2)
            d.line([(36, 64), (92, 64)], fill=c1, width=2)
            d.ellipse([60, 60, 68, 68], fill=c2)
        elif "shield" in shape:
            d.polygon([(64, 30), (88, 42), (80, 88), (64, 102), (48, 88), (40, 42)], fill=c2, outline=c1, width=3)
            d.line([(64, 34), (64, 96)], fill=(255, 255, 255, 200), width=2)
        elif "slash" in shape:
            d.arc([24, 24, 104, 104], start=190, end=350, fill=c1, width=6)
            d.arc([30, 30, 98, 98], start=200, end=340, fill=(255, 255, 255, 255), width=3)
        elif "lightning" in shape:
            pts = [(64, 16), (54, 48), (74, 52), (58, 80), (76, 82), (64, 112)]
            for i in range(len(pts)-1):
                d.line([pts[i], pts[i+1]], fill=c1, width=5)
                d.line([pts[i], pts[i+1]], fill=(255, 255, 255, 255), width=2)
        elif "blood_burst" in shape:
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                dist = random.randint(25, 48)
                bx = int(64 + dist * math.cos(rad))
                by = int(64 + dist * math.sin(rad))
                r = random.randint(3, 7)
                d.ellipse([bx-r, by-r, bx+r, by+r], fill=c1)
        elif "dragon" in shape or "hellbound" in shape:
            d.polygon([(64, 18), (86, 44), (74, 82), (64, 110), (54, 82), (42, 44)], fill=c2, outline=c1, width=3)
            d.line([(64, 18), (20, 60)], fill=c1, width=3)
            d.line([(64, 18), (108, 60)], fill=c1, width=3)
        else:
            # 기본 찬란한 에너지 코어
            d.ellipse([50, 50, 78, 78], fill=c2, outline=c1, width=2)
            d.ellipse([58, 58, 70, 70], fill=(255, 255, 255, 240))

        # 3. 반짝이는 스파크 파티클들 (마법 입자감)
        for _ in range(16):
            px = random.randint(20, 108)
            py = random.randint(20, 108)
            d.point([(px, py), (px+1, py), (px, py+1)], fill=c1)

        target_path = os.path.join(SKILLS_DIR, f"{filename}.png")
        img.save(target_path)

    print("All 72 enhanced VFX images generated successfully!")

generate_enhanced_skills_vfx()
