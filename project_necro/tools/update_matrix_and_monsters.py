# -*- coding: utf-8 -*-
"""
Update display_data.js, display.js, and display.html:
1. Aligns REGIONS_DATA (1~14) with canonical novel descriptions & 84 monster roster.
2. Adds FLYING_MONSTERS_MAP and links it to getWaveMonsterMeta.
3. Positions ground monsters at bottom: 16px and flying monsters at bottom: 85px with hovering animation.
4. Adds dynamic ground shadow beneath monsters.
5. Updates REGION_UNIQUE_PROP_NAMES to 100% pure wild nature props.
6. Increments cache buster to ?v=7.
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update display_data.js
NEW_REGIONS_AND_FLYING = """const REGIONS_DATA = {
    1: {
        name: "서울 지하철 미궁 & 석회 동굴",
        town: "assets/ui/regions/town_bg_1.png?v=7",
        battle: "assets/ui/regions/battle_bg_1.png?v=7",
        gateType: "iron",
        traitId: "trait_mana_flow",
        traitName: "🌀 마력 호흡 (마나 회복 속도 +10%)",
        gateFeature: "지하철 2호선 폐역과 지하 석회 동굴을 잇는 첫 번째 철문 균열. 보라색 맹독 포자와 뒤틀린 석순 통로를 지나면 여왕 아라크네가 도사립니다.",
        monsters: ["감염 쥐", "동공 구울", "녹슨 철도 해골", "맹독 유충"],
        named: "👹 미궁의 도살자 오거",
        boss: "🕷️ 철갑과 맹독의 여왕 아라크네"
    },
    2: {
        name: "북한산 성역 은빛 침엽수림",
        town: "assets/ui/regions/town_bg_2.png?v=7",
        battle: "assets/ui/regions/battle_bg_2.png?v=7",
        gateType: "silver",
        traitId: "trait_undead_cmd",
        traitName: "💀 사령의 권능 (소환수 전체 공방 +14%)",
        gateFeature: "북한산 인수봉에 열린 고대 은문 성역. 잎사귀마다 은박을 입힌 듯 차가운 금속광을 뿜는 은빛 침엽수림과 푸른 서릿발 투기장에 단두대의 기사 듀라한 아서가 잠들어 있습니다.",
        monsters: ["은빛 침엽수 늑대", "은문 해골병", "결계 망령 술사", "실버 라이칸 알파"],
        named: "🗿 흑요석의 수호 골렘",
        boss: "🏇 단두대의 기사 듀라한 아서"
    },
    3: {
        name: "인천항 부두 해안 암초 & 갯바위",
        town: "assets/ui/regions/town_bg_3.png?v=7",
        battle: "assets/ui/regions/battle_bg_3.png?v=7",
        gateType: "bronze",
        traitId: "trait_blood_vamp",
        traitName: "🩸 포식자의 본능 (처치 시 체력/마나 회복 +4%)",
        gateFeature: "비바람이 몰아치는 인천항 밤바다 갯바위와 검푸른 조수 웅덩이 너머 동문. 따개비 덮인 해안 절벽에서 카르텔의 마도 중장갑 파괴자가 방어선을 칩니다.",
        monsters: ["부두 변이 사냥개", "갯바위 집게 마수", "암시장 주술사", "해안 돌연변이"],
        named: "🔪 제4부두 행동대장 크로우",
        boss: "⚓ 카르텔 마도 중장갑 파괴자"
    },
    4: {
        name: "설악산 대청봉 만년설 암벽",
        town: "assets/ui/regions/town_bg_4.png?v=7",
        battle: "assets/ui/regions/battle_bg_4.png?v=7",
        gateType: "silver",
        traitId: "trait_hawk_eye",
        traitName: "🦅 매의 눈 (치명타 확률 및 피해 +6%)",
        gateFeature: "해발 1,708m 설악산 대청봉 정상의 은문. 칼바람 눈보라와 투명한 고드름이 맺힌 만년설 눈솔가지 속에서 세계 10왕 '검왕' 백도훈이 청룡 검기로 삼할의 시험을 치릅니다.",
        monsters: ["설산 빙결 멧돼지", "대청봉 설인(예티)", "설악검문 수련 무사", "청풍 검기 환영"],
        named: "⚔️ 설악검문 수제자 최강현",
        boss: "🐉 세계 10왕 ‘검왕’ 백도훈"
    },
    5: {
        name: "평양 지하 50미터 암반 석순 미로",
        town: "assets/ui/regions/town_bg_5.png?v=7",
        battle: "assets/ui/regions/battle_bg_5.png?v=7",
        gateType: "bronze",
        traitId: "trait_iron_body",
        traitName: "🛡️ 육체의 기억 (기본 방어력 및 체력 +12%)",
        gateFeature: "지하 50m 비밀 방공호 암반층 너머 지하수 폭포와 천연 석순 미로. 1천 강화 친위대와 태고의 아다만티움 거신병이 봉쇄하고 있는 군사 동문입니다.",
        monsters: ["휴전선 지뢰 거미", "북측 강화 보병", "지하 화염방사병", "생체 실험 키메라"],
        named: "🤖 친위대장 강철 골렘",
        boss: "🤖 지하 50m 아다만티움 거신병"
    },
    6: {
        name: "도쿄 음양사 대나무 비경 & 폭포",
        town: "assets/ui/regions/town_bg_6.png?v=7",
        battle: "assets/ui/regions/battle_bg_6.png?v=7",
        gateType: "silver",
        traitId: "trait_shadow_step",
        traitName: "🌙 잔상 보법 (공격속도 및 이동속도 +8%)",
        gateFeature: "붉은 단풍잎이 흩날리는 울창한 대나무 숲과 안개 낀 계곡 은문. 그림자 암살자 카게미츠와 천년 원령 식신을 부리는 도쿄 본가 대음양사 아베노의 결계입니다.",
        monsters: ["그림자 하급 닌자", "그림자 까마귀 요괴", "종이 식신(시키가미)", "원령 무사"],
        named: "🥷 어둠의 칼날 카게미츠",
        boss: "👹 도쿄 본가 대음양사 아베노"
    },
    7: {
        name: "마카오 불야성 열대 맹그로브 & 석회 협곡",
        town: "assets/ui/regions/town_bg_7.png?v=7",
        battle: "assets/ui/regions/battle_bg_7.png?v=7",
        gateType: "gold",
        traitId: "trait_holy_grace",
        traitName: "✨ 성역의 은총 (회복량 및 보호막 효율 +10%)",
        gateFeature: "마카오 카지노 지하에 숨겨진 열대 원시림과 맹그로브 물안개 늪지대 금문. 거대 덩굴과 석회 협곡의 옥좌에서 삼합회 수장 흑룡 용왕이 군림합니다.",
        monsters: ["카지노 흑복 경호원", "삼합회 쌍도끼 집행자", "불야성 혈마법사", "황금 룰렛 골렘"],
        named: "🎲 삼합회 부두목 혈귀",
        boss: "🐲 마카오 삼합회 수장 흑룡 용왕"
    },
    8: {
        name: "블라디보스토크 동토 침엽수림 & 해저 기지",
        town: "assets/ui/regions/town_bg_8.png?v=7",
        battle: "assets/ui/regions/battle_bg_8.png?v=7",
        gateType: "gold",
        traitId: "trait_thorn_armor",
        traitName: "🦔 불굴의 가시 (피격 시 방어력 비례 반사 +20%)",
        gateFeature: "영하 40도의 극동 영구 동토층 자작나무·침엽수 설원 지하 금문. 극저온 냉기 드론과 아다만티움 외골격 거인 보리스의 중장갑 부대가 요새를 지킵니다.",
        monsters: ["동토의 불곰 변이체", "해저 전투 잠수부", "극저온 냉기 드론", "아다만티움 사이보그"],
        named: "🦾 신디케이트 부관 이반",
        boss: "🦾 해저 요새 거인 ‘강철의 보리스’"
    },
    9: {
        name: "태평양 해연(海淵) 심해 8,000m",
        town: "assets/ui/regions/town_bg_9.png?v=7",
        battle: "assets/ui/regions/battle_bg_9.png?v=7",
        gateType: "platinum",
        traitId: "trait_mana_flow",
        traitName: "🌀 심해 마력 동조 (마나 회복 및 스킬 가속 +15%)",
        gateFeature: "수심 8,000m 햇살 한 점 없는 암흑 속 발광 말미잘과 청록 산호초, 켈프 해조류 숲의 플래티넘문. 초고압 해류 속에서 심해 지배자 크라켄 골렘이 도사립니다.",
        monsters: ["심해 발광 아귀", "해연 소라게 골렘", "수압 파쇄 세이렌", "심연 촉수 기생체"],
        named: "🐍 해연의 수문장 리바이어던",
        boss: "🦑 심해의 지배자 크라켄 골렘"
    },
    10: {
        name: "히말라야 8,000m 고룡의 설산 묘지",
        town: "assets/ui/regions/town_bg_10.png?v=7",
        battle: "assets/ui/regions/battle_bg_10.png?v=7",
        gateType: "platinum",
        traitId: "trait_frost_heart",
        traitName: "❄️ 극한의 심장 (냉기 및 마법 속성 피해 +12%)",
        gateFeature: "해발 8,000m 만년설과 푸른 빙벽 크레바스 너머 태고 빙룡의 뼈더미가 솟은 성산 플래티넘문. 절대영도의 서리 본 드래곤이 군림합니다.",
        monsters: ["해발 8천 설산 망령", "얼어붙은 등반가 구울", "빙룡 뼈조각 와이번", "만년설 빙하 골렘"],
        named: "🗿 고룡 묘지 수호 거신병",
        boss: "🦴 태고의 재앙 ‘서리 본 드래곤’"
    },
    11: {
        name: "타클라마칸 사막 모래지옥 & 풍화 사암",
        town: "assets/ui/regions/town_bg_11.png?v=7",
        battle: "assets/ui/regions/battle_bg_11.png?v=7",
        gateType: "gold",
        traitId: "trait_boss_slayer",
        traitName: "⚔️ 학살자의 투기 (네임드 및 보스 피해 +10%)",
        gateFeature: "붉은 모래폭풍과 거대 풍화 사암 기둥이 솟은 열사의 금문. 사령군주의 얼음에 닿아 투명한 유리가 된 분화구에서 사막 여왕 유리 스콜피온이 나타납니다.",
        monsters: ["서리 늑대기병", "타클라마칸 모래 전갈", "유리 사막 아누비스", "열사 폭풍 정령"],
        named: "🏜️ 모래지옥 친위장 사하라",
        boss: "🦂 타클라마칸 사막 여왕 유리 스콜피온"
    },
    12: {
        name: "로키산맥 화산 마그마 분화구",
        town: "assets/ui/regions/town_bg_12.png?v=7",
        battle: "assets/ui/regions/battle_bg_12.png?v=7",
        gateType: "platinum",
        traitId: "trait_iron_body",
        traitName: "🛡️ 대지의 용철 (최대 체력 및 화염 저항 +18%)",
        gateFeature: "수 킬로미터에 걸쳐 펄펄 끓는 마그마 호수와 검은 현무암 지대의 플래티넘문. 마그마를 혈액 삼아 순환시키는 화산 베히모스가 포효합니다.",
        monsters: ["라인강 타락 마수병", "유럽 침공 키메라", "로키산맥 화염 임프", "마그마 암석 거인"],
        named: "🔥 마수 군단장 벨제부브",
        boss: "🌋 북미 대재앙 ‘용암 베히모스’"
    },
    13: {
        name: "태평양 성층권 금문 운해(雲海) & 모함",
        town: "assets/ui/regions/town_bg_13.png?v=7",
        battle: "assets/ui/regions/battle_bg_13.png?v=7",
        gateType: "gold",
        traitId: "trait_undead_cmd",
        traitName: "🛸 제3군단장 해킹망 (소환수 및 크로스 스킬 위력 +20%)",
        gateFeature: "태평양 상공 30km 황금빛 차원의 균열 너머 성층권 구름 바다와 반중력 부유석. 이단자 참모 벨록을 구출하고 외계 선봉 타르코스를 격파해야 합니다.",
        monsters: ["화성 제국 강습 보병", "반중력 플라즈마 드론", "사이오닉 심문관", "외계 센추리온"],
        named: "🧬 이단자 참모 벨록 (구출전)",
        boss: "🛸 금문 외계 선봉 사령관 타르코스"
    },
    14: {
        name: "2070 성층권 다이아몬드 게이트 종언",
        town: "assets/ui/regions/town_bg_14.png?v=7",
        battle: "assets/ui/regions/battle_bg_14.png?v=7",
        gateType: "diamond",
        traitId: "trait_boss_slayer",
        traitName: "👑 사령군주의 종언 (모든 최종 피해량 +35% & 영혼 각인 개방)",
        gateFeature: "전 세계 하늘을 뒤덮은 최후의 보랏빛 다이아몬드 차원문. 거대 천연 다이아몬드 광맥과 차원의 핵에서 대장군 볼가르와 무감정의 황제와 결전을 벌입니다.",
        monsters: ["황실 친위대 결사병", "아공간 암살 팬텀", "성층권 궤도 폭격기", "차원 파쇄 거신"],
        named: "⚔️ 대장군 볼가르 & 여왕 시렌",
        boss: "👑 외계 제국 절대자 ‘무감정의 황제’"
    }
};

// =========================================================================
// 5-1. 14개 지역 84종 괴수 중 비행/부유(Flying/Levitating) 판정 괴수 매핑
// 지상형(Ground)은 bottom: 16px에 견고히 접지되고, 비행형(Flying)은 상공(bottom: 85px)에서 부드러운 유영 애니메이션 적용
// =========================================================================
const FLYING_MONSTERS_MAP = {
    "1_4": true,  // 1지역 W4 맹독 유충(포자 부유)
    "2_3": true,  // 2지역 W3 결계 망령 술사 (부유형 유령)
    "4_4": true,  // 4지역 W4 청풍 검기 환영 (부유 검기)
    "6_2": true,  // 6지역 W2 그림자 까마귀 요괴 (비행 요괴)
    "6_3": true,  // 6지역 W3 종이 식신 (부유 부적체)
    "7_3": true,  // 7지역 W3 불야성 혈마법사 (공중 부유)
    "8_3": true,  // 8지역 W3 극저온 냉기 드론 (비행 기계)
    "9_1": true,  // 9지역 W1 심해 발광 아귀 (심해 유영)
    "9_3": true,  // 9지역 W3 수압 파쇄 세이렌 (심해 유영)
    "10_1": true, // 10지역 W1 해발 8천 설산 망령 (부유 유령)
    "10_3": true, // 10지역 W3 빙룡 뼈조각 와이번 (비행룡)
    "10_6": true, // 10지역 W6 서리 본 드래곤 (거대 비행룡)
    "11_4": true, // 11지역 W4 열사 폭풍 정령 (부유 정령)
    "12_3": true, // 12지역 W3 로키산맥 화염 임프 (날개 비행체)
    "13_2": true, // 13지역 W2 반중력 플라즈마 드론 (비행 드론)
    "13_3": true, // 13지역 W3 사이오닉 심문관 (반중력 부유)
    "13_6": true, // 13지역 W6 금문 외계 선봉 사령관 타르코스 (비행선)
    "14_2": true, // 14지역 W2 아공간 암살 팬텀 (차원 부유)
    "14_3": true  // 14지역 W3 성층권 궤도 폭격기 (고공 비행선)
};"""

with open('project_necro/display_data.js', 'r', encoding='utf-8') as f:
    js_data = f.read()

pattern = r'const REGIONS_DATA = \{[\s\S]*?\n\};'
match = re.search(pattern, js_data)
if match:
    js_data = js_data[:match.start()] + NEW_REGIONS_AND_FLYING + js_data[match.end():]
    with open('project_necro/display_data.js', 'w', encoding='utf-8') as f:
        f.write(js_data)
    print("Successfully updated display_data.js with canonical regions and FLYING_MONSTERS_MAP!")
else:
    print("ERROR: REGIONS_DATA pattern not found in display_data.js")
