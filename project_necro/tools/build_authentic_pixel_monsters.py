# -*- coding: utf-8 -*-
import os, sys
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

SRC_DIR = r"D:\workspace\GEMINI\project2100\assets\monsters"
DST_DIR = r"D:\workspace\GEMINI\project_necro\assets\monsters"
os.makedirs(DST_DIR, exist_ok=True)

# Crop out bottom text labels on specific source files where AI text appeared at bottom/top
CROP_OVERRIDES = {
    "m_4_1.png": (0.0, 0.0, 1.0, 0.87),
    "m_4_3.png": (0.0, 0.0, 1.0, 0.88),
    "m_7_boss.png": (0.0, 0.0, 1.0, 0.90),
    "m_7_named.png": (0.0, 0.0, 1.0, 0.90),
    "m_11_3.png": (0.0, 0.12, 1.0, 1.0),
    "m_11_4.png": (0.0, 0.12, 1.0, 1.0),
    "m_14_named.png": (0.0, 0.12, 1.0, 1.0),
}

# Exact visual 1:1 mapping: (region_id, slot) -> (source_file, hue_tint_rgb_or_none)
MONSTER_REMAP = {
    # Region 1: 서울 지하철 미궁 & 을지로 [철문]
    (1, 1): ("m_2_4.png", None),       # 지하철 감염 쥐 (Mutant Rat)
    (1, 2): ("m_4_4.png", None),       # 동공 구울 (Undead Ghoul)
    (1, 3): ("m_2_3.png", None),       # 녹슨 철도 해골 (Armored Skeleton)
    (1, 4): ("m_12_3.png", None),      # 맹독 거미줄 유충 (Toxic Larva)
    (1, "named"): ("m_11_named.png", None), # 미궁의 도살자 오거 (Heavy Brute)
    (1, "boss"): ("m_11_3.png", (1.15, 0.85, 1.35)), # 🕷️ 철갑 맹독 여왕 아라크네 (Giant Armored Arachnid)

    # Region 2: 북한산 비밀 성역 & 은문 [은문]
    (2, 1): ("m_1_1.png", None),       # 은빛 침엽수 늑대 (Silver Ice Wolf)
    (2, 2): ("m_10_4.png", None),      # 고대 제단 해골병 (Silver Spectral Knight)
    (2, 3): ("m_14_2.png", None),      # 결계 망령 술사 (Masked Wraith Mage)
    (2, 4): ("m_4_1.png", None),       # 흑요석 가고일 (Stone Gargoyle)
    (2, "named"): ("m_1_4.png", None), # 흑요석의 수호 골렘 (Rock Golem)
    (2, "boss"): ("m_7_boss.png", (0.85, 0.88, 1.35)), # 🏇 단두대의 기사 듀라한 아서 (Armored Death Knight on Steed)

    # Region 3: 인천항 제4부두 암시장 [동문]
    (3, 1): ("m_5_3.png", None),       # 밀수단 단검 조폭 (Smuggler Raider)
    (3, 2): ("m_11_2.png", None),      # 부두 개조 사냥개 (Cybernetic Hound)
    (3, 3): ("m_3_2.png", None),       # 컨테이너 마도 포수 (Heavy Artillery Turret)
    (3, 4): ("m_13_1.png", None),      # 암시장 연금 주술사 (Gas-mask Alchemist)
    (3, "named"): ("m_2_named.png", None), # 제4부두 행동대장 크로우 (Enforcer Captain)
    (3, "boss"): ("m_11_boss.png", None),  # ⚓ 카르텔 마도 중장갑 파괴자 (Armored Steam Juggernaut)

    # Region 4: 설악산 대청봉 설원 [은문]
    (4, 1): ("m_1_3.png", None),       # 설산 빙결 큰뿔사슴 (Ice Stag Beast)
    (4, 2): ("m_10_named.png", None),  # 대청봉 설인(예티) (White Yeti)
    (4, 3): ("m_10_1.png", None),      # 설악검문 수호 가고일 (Frost Winged Guardian)
    (4, 4): ("m_3_4.png", None),       # 청풍 검기 환영 (Cyan Sword Spirit)
    (4, "named"): ("m_1_named.png", None), # 설악검문 수문장 (Frost Axe Master)
    (4, "boss"): ("m_14_named.png", None), # 🐉 설악산 대청봉 설원 패왕 (Ice Horned Sovereign)

    # Region 5: DMZ 휴전선 & 평양 벙커 [동문]
    (5, 1): ("m_3_3.png", None),       # 휴전선 지뢰 거미 (Mechanical Spider Mine)
    (5, 2): ("m_13_3.png", None),      # 북측 강화 기갑병 (Tracked Armored Soldier)
    (5, 3): ("m_13_4.png", None),      # 지하 벙커 생체 실험체 (Mad Lab Mutant)
    (5, 4): ("m_7_2.png", None),       # 벙커 군용 장갑견 (Armored War Hound)
    (5, "named"): ("m_13_named.png", None), # 친위대장 강철 지휘관 (Bunker Commander)
    (5, "boss"): ("m_13_boss.png", None),   # 🤖 지하 50m 아다만티움 거신병 (Giant Gatling Mech)

    # Region 6: 양재동 & 도쿄 음양사 본가 [은문]
    (6, 1): ("m_4_2.png", None),       # 열도 그림자 박쥐 요괴 (Shadow Bat Yokai)
    (6, 2): ("m_7_4.png", None),       # 까마귀 텐구 요괴 (Dark Crow Vulture)
    (6, 3): ("m_6_2.png", None),       # 종이 식신 주술사 (Talisman Witch Caster)
    (6, 4): ("m_6_4.png", None),       # 주술 원령 군집체 (Spirit Swarm)
    (6, "named"): ("m_3_named.png", None), # 🥷 어둠의 칼날 카게미츠 (Katana Cyber Ninja)
    (6, "boss"): ("m_6_boss.png", None),   # 👹 도쿄 본가 대음양사 원령신 (Horned Spirit Overlord)

    # Region 7: 마카오 불야성 VIP 카지노 [금문]
    (7, 1): ("m_11_1.png", None),      # 카지노 흑복 보안관 (Corrupted Officer)
    (7, 2): ("m_7_1.png", None),       # 불야성 황금 투우 전차 (Golden Mecha Bull)
    (7, 3): ("m_4_3.png", None),       # 불야성 혈마법 슬라임 (Blood Magic Blob)
    (7, 4): ("m_6_named.png", (1.25, 1.05, 0.65)), # 황금 룰렛 거신 (Golden Golem)
    (7, "named"): ("m_4_named.png", None), # 삼합회 부두목 혈귀 (Vampire Noble)
    (7, "boss"): ("m_12_boss.png", (1.25, 1.05, 0.55)), # 🐲 마카오 삼합회 삼두 금룡왕 (Three-Headed Golden Dragon)

    # Region 8: 블라디보스토크 해저 기지 [금문]
    (8, 1): ("m_1_2.png", None),       # 동토의 극저온 슬라임 (Cryo Slime)
    (8, 2): ("m_10_2.png", None),      # 해저 동굴 얼음박쥐 (Ice Bat)
    (8, 3): ("m_3_1.png", None),       # 극저온 강습 바이크 드론 (Cyber Assault Bike)
    (8, 4): ("m_10_3.png", None),      # 아다만티움 빙정 골렘 (Cryo Crystal Golem)
    (8, "named"): ("m_7_named.png", (0.75, 1.05, 1.35)), # 신디케이트 기갑 부관 이반
    (8, "boss"): ("m_1_boss.png", None),   # 🦾 동토의 빙하 괴수 ‘베히모스 카이드’ (Giant Ice Tusker Boss)

    # Region 9: 태평양 미지의 해연 게이트 [플래티넘문]
    (9, 1): ("m_9_3.png", None),       # 심해 발광 아귀 괴수 (Deep Sea Anglerfish)
    (9, 2): ("m_9_named.png", None),   # 해연 소라게 골렘 (Hermit Crab Golem)
    (9, 3): ("m_9_4.png", None),       # 수압 파쇄 세이렌 (Abyssal Siren)
    (9, 4): ("m_9_2.png", None),       # 심연 촉수 해파리 (Giant Abyssal Jellyfish)
    (9, "named"): ("m_9_1.png", None), # 해연 초음파 괴수 (Sonic Sea Beast)
    (9, "boss"): ("m_9_boss.png", None),   # 🦑 심해의 지배자 레비아탄 (Sea Dragon Leviathan)

    # Region 10: 히말라야 고룡 묘지 [플래티넘문]
    (10, 1): ("m_6_1.png", (0.8, 1.1, 1.3)), # 해발 8천 설산 빙혼 (Frost Wisp)
    (10, 2): ("m_2_1.png", (0.75, 1.05, 1.35)), # 얼어붙은 등반가 구울 (Frozen Climber Ghoul)
    (10, 3): ("m_14_1.png", None),     # 빙룡 결정 정령 (Ice Crystal Elemental)
    (10, 4): ("m_10_3.png", (0.85, 1.15, 1.35)), # 만년설 빙하 골렘 (Glacier Golem)
    (10, "named"): ("m_10_named.png", (0.8, 1.05, 1.35)), # 고룡 묘지 설산 수호신
    (10, "boss"): ("m_10_boss.png", None), # 🦴 태고의 재앙 ‘서리 드래곤’ (Frost Dragon Boss)

    # Region 11: 시베리아 & 타클라마칸 [금문]
    (11, 1): ("m_7_3.png", None),      # 황무지 기병 창병 (Desert Cavalry Lancer)
    (11, 2): ("m_5_4.png", None),      # 타클라마칸 모래 전갈 (Desert Scorpion)
    (11, 3): ("m_5_1.png", None),      # 고대 사막 미라 전사 (Bandaged Mummy)
    (11, 4): ("m_5_2.png", None),      # 사막 황금 스카라베 (Golden Scarab Beetle)
    (11, "named"): ("m_5_named.png", None), # 모래지옥 대주술사 사하라 (Desert Necromancer)
    (11, "boss"): ("m_8_3.png", (1.25, 1.05, 0.65)), # 🦂 타클라마칸 사막 여왕 스콜피온 (Giant Venom Scorpion Queen)

    # Region 12: 독일 라인강 & 북미 로키산맥 [플래티넘문]
    (12, 1): ("m_8_1.png", None),      # 로키산맥 화염 폭탄충 (Fire Bomb Beast)
    (12, 2): ("m_8_2.png", None),      # 마그마 등껍질 거북 (Magma Tortoise)
    (12, 3): ("m_8_4.png", None),      # 화산 잿더미 불타는 좀비 (Burning Ash Zombie)
    (12, 4): ("m_14_3.png", None),     # 마그마 암석 거인 (Obsidian Lava Golem)
    (12, "named"): ("m_8_named.png", None), # 화염마 군단장 나이트메어 (Flaming Hellsteed)
    (12, "boss"): ("m_2_boss.png", None),   # 🌋 북미 대재앙 ‘용암 베히모스’ (Molten Magma Behemoth)

    # Region 13: 태평양 성층권 금문 모함 [금문]
    (13, 1): ("m_12_1.png", None),     # 성층권 플라즈마 스포어 (Alien Plasma Spore)
    (13, 2): ("m_12_2.png", None),     # 외계 생체 두꺼비 변이체 (Alien Bio Toad)
    (13, 3): ("m_12_4.png", None),     # 모함 기생 촉수 덩굴 (Alien Tendril Vine)
    (13, 4): ("m_11_4.png", None),     # 반중력 코어 슬라임 (Alien Core Mind)
    (13, "named"): ("m_12_named.png", None), # 🧬 외계 파충류 참모 벨록 (Reptilian Alien Tactician)
    (13, "boss"): ("m_3_boss.png", None),    # 🛸 성층권 모함 중추 코어 ‘타르코스’ (Orbital Mechanical Core Boss)

    # Region 14: 2070 성층권 다이아몬드문 [다이아몬드문]
    (14, 1): ("m_8_boss.png", None),   # 황실 홍련 근위대장 (Crimson Flame Knight)
    (14, 2): ("m_14_4.png", None),     # 아공간 차원 팬텀 (Cosmic Void Phantom)
    (14, 3): ("m_6_3.png", None),      # 차원 침식 마계 식물 (Dimensional Thorn)
    (14, 4): ("m_13_2.png", None),     # 차원 방사능 부정체 (Abyssal Ooze)
    (14, "named"): ("m_14_boss.png", None), # ⚔️ 외계 대장군 볼가르 (Horned Winged Warlord)
    (14, "boss"): ("m_4_boss.png", None),   # 👑 외계 제국 ‘무감정의 황제’ (Crowned Ruthless Emperor)
}


def convert_to_16bit_pixel_sprite(src_filename, tint=None, is_boss=False, is_named=False):
    src_path = os.path.join(SRC_DIR, src_filename)
    im = Image.open(src_path).convert("RGBA")

    # Apply crop override if needed to remove any bottom/top text artifact
    if src_filename in CROP_OVERRIDES:
        x0, y0, x1, y1 = CROP_OVERRIDES[src_filename]
        w, h = im.size
        im = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))

    # Tightly crop to non-transparent bounding box
    alpha = im.split()[3]
    bbox = alpha.point(lambda p: 255 if p > 30 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)

    # Optional RGB tint to differentiate variants cleanly
    if tint:
        rm, gm, bm = tint
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a > 0:
                    px[x, y] = (
                        max(0, min(255, int(r * rm))),
                        max(0, min(255, int(g * gm))),
                        max(0, min(255, int(b * bm))),
                        a
                    )

    # Boost saturation & contrast for vibrant 16-bit arcade pixel look
    r, g, b, a = im.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageEnhance.Color(rgb).enhance(1.22)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.18)

    # Fit inside high-density 16-bit sprite canvas (180x180 normal, 200x200 named, 224x224 boss) — NO blurry 68x68 crushing!
    grid_res = 224 if is_boss else (200 if is_named else 180)
    inner_res = grid_res - 8

    ratio = min(inner_res / max(1, im.width), inner_res / max(1, im.height))
    nw = max(1, int(im.width * ratio))
    nh = max(1, int(im.height * ratio))

    small_rgb = rgb.resize((nw, nh), Image.Resampling.LANCZOS)
    small_a = a.resize((nw, nh), Image.Resampling.LANCZOS).point(lambda p: 255 if p > 90 else 0)

    # Quantize to 64 clean colors with NO noisy Floyd-Steinberg speckle dithering
    quant = small_rgb.quantize(colors=64, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).convert("RGBA")
    quant.putalpha(small_a)

    # Place on grid_res canvas
    grid_canvas = Image.new("RGBA", (grid_res, grid_res), (0, 0, 0, 0))
    ox = (grid_res - nw) // 2
    oy = (grid_res - nh) // 2
    grid_canvas.alpha_composite(quant, (ox, oy))

    # Crisp 2px dark pixel outline
    ga = grid_canvas.split()[3]
    dilated = ga.filter(ImageFilter.MaxFilter(5))
    outlined = Image.new("RGBA", (grid_res, grid_res), (0, 0, 0, 0))
    out_px = outlined.load()
    src_px = grid_canvas.load()
    dil_px = dilated.load()
    for y in range(grid_res):
        for x in range(grid_res):
            if src_px[x, y][3] > 128:
                out_px[x, y] = src_px[x, y]
            elif dil_px[x, y] > 128:
                out_px[x, y] = (10, 7, 5, 255)

    return outlined


if __name__ == "__main__":
    count = 0
    for (r_id, slot), (src_fn, tint) in MONSTER_REMAP.items():
        is_boss = (slot == "boss")
        is_named = (slot == "named")
        out_img = convert_to_16bit_pixel_sprite(src_fn, tint=tint, is_boss=is_boss, is_named=is_named)
        dst_fn = f"m_{r_id}_{slot}.png"
        dst_path = os.path.join(DST_DIR, dst_fn)
        out_img.save(dst_path)
        count += 1
    print(f"Successfully converted & remapped {count} authentic 16-bit pixel monsters!")
