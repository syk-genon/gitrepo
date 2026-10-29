# -*- coding: utf-8 -*-
import os

path = r"D:\workspace\GEMINI\project_necro\display_data.js"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start_idx = text.find("// 5. 6대 차원문(Gate) 등급 메타데이터")
if start_idx == -1:
    start_idx = text.find("// 5. 14개 지역 메타데이터")
end_idx = text.find("// =========================================================================", start_idx)

new_block = """// 5. 6대 차원문(Gate) 등급 메타데이터 & 14개 지역 84종 몬스터·특성 매핑
const GATES_DATA = {
    "iron": {
        id: "iron",
        name: "🚪 철문 (Iron Gate)",
        sprite: "assets/ui/gates/gate_iron.png",
        color: "#a8b4c4",
        tier: "Tier 1 · 초급 지하 균열",
        envModifier: "🌫️ [지하 탁기] 시야 협소 · 맹독 포자 발생 (초당 최대체력 1% 침식)",
        dropBonus: "기본 마력석 ×1.0 · 철문 하급 유물 드랍",
        rewardGold: 1500
    },
    "bronze": {
        id: "bronze",
        name: "🚪 동문 (Bronze Gate)",
        sprite: "assets/ui/gates/gate_bronze.png",
        color: "#e69650",
        tier: "Tier 2 · 중급 군사 균열",
        envModifier: "⚙️ [중장갑 요새화] 적 괴수 방어력 +20% · 폭발물 및 지뢰 함정 활성화",
        dropBonus: "마력석 획득 ×1.5 · 청동 무기고 장비 상자 드랍",
        rewardGold: 3200
    },
    "silver": {
        id: "silver",
        name: "🚪 은문 (Silver Gate)",
        sprite: "assets/ui/gates/gate_silver.png",
        color: "#00f0ff",
        tier: "Tier 3 · 상급 고대 성역",
        envModifier: "❄️ [은빛 마력 한기] 영웅 마나 회복 +30% · 언데드 및 검기 계열 적 공격력 +25%",
        dropBonus: "마력석 획득 ×2.5 · 신화 세트(Set) 파츠 드랍률 2배",
        rewardGold: 6500
    },
    "gold": {
        id: "gold",
        name: "🚪 금문 (Gold Gate)",
        sprite: "assets/ui/gates/gate_gold.png",
        color: "#ffd000",
        tier: "Tier 4 · 대재앙급 황금 균열",
        envModifier: "⚡ [황금 과부하 역장] 적 전체 슈퍼아머 부여 · 치명타 피해량 +50% 증폭",
        dropBonus: "마력석 획득 ×4.5 · 고유(Unique) 유물 및 스킬 비급서 드랍",
        rewardGold: 14000
    },
    "platinum": {
        id: "platinum",
        name: "🚪 플래티넘문 (Platinum Gate)",
        sprite: "assets/ui/gates/gate_platinum.png",
        color: "#c850ff",
        tier: "Tier 5 · 신화 심연 게이트",
        envModifier: "🌌 [심연 중력 왜곡] 쿨타임 가속 +25% · 보스 사망 시 1회 광폭화 부활 패턴 발동",
        dropBonus: "마력석 획득 ×8.0 · 10왕/고룡급 신화 코어 확정 드랍",
        rewardGold: 30000
    },
    "diamond": {
        id: "diamond",
        name: "🚪 다이아몬드문 (Diamond Gate)",
        sprite: "assets/ui/gates/gate_diamond.png",
        color: "#ff2a6d",
        tier: "Tier 6 · 종언의 성층권 게이트",
        envModifier: "👑 [황제의 절대 권역] 모든 적 피해량 +100% · 영웅 영혼 각인 슬롯 위력 2배 개방",
        dropBonus: "마력석 획득 ×15.0 · 종결 신화 5세트 & 외계 황제 유물 확정 드랍",
        rewardGold: 75000
    }
};

const REGIONS_DATA = {
    1: {
        name: "서울 지하철 미궁 & 을지로",
        town: "assets/ui/regions/town_bg_1.png",
        battle: "assets/ui/regions/battle_bg_1.png",
        gateType: "iron",
        traitId: "trait_mana_flow",
        traitName: "🌀 마력 호흡 (마나 회복 속도 +10%)",
        gateFeature: "지하철 2호선 폐역과 을지로 대장간을 잇는 첫 번째 철문 균열. 맹독 거미줄과 부식된 철도 해골이 출몰합니다.",
        monsters: ["지하철 감염 쥐", "동공 구울", "녹슨 철도 해골", "맹독 거미줄 유충"],
        named: "👹 미궁의 도살자 오거",
        boss: "🕷️ 철갑 맹독 여왕 아라크네"
    },
    2: {
        name: "북한산 비밀 성역 & 은문",
        town: "assets/ui/regions/town_bg_2.png",
        battle: "assets/ui/regions/battle_bg_2.png",
        gateType: "silver",
        traitId: "trait_undead_cmd",
        traitName: "💀 사령의 권능 (소환수 전체 공방 +14%)",
        gateFeature: "북한산 인수봉 정상에 열린 고대 은문 성역. 사령군주 제1군단장 듀라한 아서가 잠들어 있는 망자의 결계입니다.",
        monsters: ["은빛 침엽수 늑대", "고대 제단 해골병", "결계 망령 술사", "흑요석 가고일"],
        named: "🗿 흑요석의 수호 골렘",
        boss: "🏇 단두대의 기사 듀라한 아서"
    },
    3: {
        name: "인천항 제4부두 암시장",
        town: "assets/ui/regions/town_bg_3.png",
        battle: "assets/ui/regions/battle_bg_3.png",
        gateType: "bronze",
        traitId: "trait_blood_vamp",
        traitName: "🩸 포식자의 본능 (처치 시 체력/마나 회복 +4%)",
        gateFeature: "밀수 카르텔이 점거한 제4부두 컨테이너 동문. 마도 개조 사냥개와 중장갑 크레인 파쇄기가 방어선을 구축하고 있습니다.",
        monsters: ["밀수단 단검 조폭", "부두 개조 사냥개", "컨테이너 마도 포수", "암시장 주술사"],
        named: "🔪 제4부두 행동대장 크로우",
        boss: "⚓ 카르텔 마도 중장갑 파괴자"
    },
    4: {
        name: "설악산 대청봉 설원",
        town: "assets/ui/regions/town_bg_4.png",
        battle: "assets/ui/regions/battle_bg_4.png",
        gateType: "silver",
        traitId: "trait_hawk_eye",
        traitName: "🦅 매의 눈 (치명타 확률 및 피해 +6%)",
        gateFeature: "만년설이 몰아치는 설악산 대청봉의 은문. 검왕 백도훈의 청룡 검기가 공간을 가르는 극한의 무림 시험장입니다.",
        monsters: ["설산 빙결 멧돼지", "대청봉 설인(예티)", "설악검문 수련 무사", "청풍 검기 환영"],
        named: "⚔️ 설악검문 수제자 최강현",
        boss: "🐉 세계 10왕 ‘검왕’ 백도훈"
    },
    5: {
        name: "DMZ 휴전선 & 평양 벙커",
        town: "assets/ui/regions/town_bg_5.png",
        battle: "assets/ui/regions/battle_bg_5.png",
        gateType: "bronze",
        traitId: "trait_iron_body",
        traitName: "🛡️ 육체의 기억 (기본 방어력 및 체력 +12%)",
        gateFeature: "지하 50m 비밀 방공호에 발생한 군사 동문. 지뢰 거미와 아다만티움 생체 병기들이 복도를 봉쇄하고 있습니다.",
        monsters: ["휴전선 지뢰 거미", "북측 강화 보병", "지하 벙커 화염방사병", "생체 실험 키메라"],
        named: "🤖 친위대장 강철 골렘",
        boss: "🤖 지하 50m 아다만티움 거신병"
    },
    6: {
        name: "양재동 & 도쿄 음양사 본가",
        town: "assets/ui/regions/town_bg_6.png",
        battle: "assets/ui/regions/battle_bg_6.png",
        gateType: "silver",
        traitId: "trait_shadow_step",
        traitName: "🌙 잔상 보법 (공격속도 및 이동속도 +8%)",
        gateFeature: "붉은 도리이와 부적 결계로 뒤덮인 음양사 은문. 그림자 닌자 카게미츠와 천년 원령 식신들이 어둠 속에서 기습합니다.",
        monsters: ["열도 하급 닌자", "그림자 까마귀 요괴", "종이 식신(시키가미)", "주술 원령 무사"],
        named: "🥷 어둠의 칼날 카게미츠",
        boss: "👹 도쿄 본가 대음양사 아베노"
    },
    7: {
        name: "마카오 불야성 VIP 카지노",
        town: "assets/ui/regions/town_bg_7.png",
        battle: "assets/ui/regions/battle_bg_7.png",
        gateType: "gold",
        traitId: "trait_holy_grace",
        traitName: "✨ 성역의 은총 (회복량 및 보호막 효율 +10%)",
        gateFeature: "황금 샹들리에가 빛나는 마카오 불야성 금문. 주사위 확률 조작 마법과 삼합회 흑룡 용왕의 황금 결계가 작동합니다.",
        monsters: ["카지노 흑복 경호원", "삼합회 쌍도끼 집행자", "불야성 혈마법사", "황금 룰렛 골렘"],
        named: "🎲 삼합회 부두목 혈귀",
        boss: "🐲 마카오 삼합회 흑룡 용왕"
    },
    8: {
        name: "블라디보스토크 해저 기지",
        town: "assets/ui/regions/town_bg_8.png",
        battle: "assets/ui/regions/battle_bg_8.png",
        gateType: "gold",
        traitId: "trait_thorn_armor",
        traitName: "🦔 불굴의 가시 (피격 시 방어력 비례 반사 +20%)",
        gateFeature: "극동 얼음 바다 밑바닥에 건설된 해저 금문 요새. 극저온 냉기 드론과 강철 거인 보리스의 중장갑 부대가 주둔합니다.",
        monsters: ["동토의 불곰 변이체", "해저 기지 전투 잠수부", "극저온 냉기 드론", "아다만티움 사이보그"],
        named: "🦾 신디케이트 부관 이반",
        boss: "🦾 아다만티움 거인 ‘강철의 보리스’"
    },
    9: {
        name: "태평양 미지의 해연 게이트",
        town: "assets/ui/regions/town_bg_9.png",
        battle: "assets/ui/regions/battle_bg_9.png",
        gateType: "platinum",
        traitId: "trait_mana_flow",
        traitName: "🌀 심해 마력 동조 (마나 회복 및 스킬 가속 +15%)",
        gateFeature: "수심 1만 미터 마리아나 해연에 개방된 플래티넘문. 초고압 해류와 심해 거대 괴수 크라켄의 촉수가 전장을 덮칩니다.",
        monsters: ["심해 발광 아귀 괴수", "해연 소라게 골렘", "수압 파쇄 세이렌", "심연 촉수 기생체"],
        named: "🐍 해연의 수문장 리바이어던",
        boss: "🦑 심해의 지배자 크라켄 골렘"
    },
    10: {
        name: "히말라야 고룡 묘지",
        town: "assets/ui/regions/town_bg_10.png",
        battle: "assets/ui/regions/battle_bg_10.png",
        gateType: "platinum",
        traitId: "trait_frost_heart",
        traitName: "❄️ 극한의 심장 (냉기 및 마법 속성 피해 +12%)",
        gateFeature: "해발 8,800m 고룡들의 뼈가 묻힌 성산 플래티넘문. 태고의 서리 본 드래곤이 절대영도의 브레스로 침입자를 얼립니다.",
        monsters: ["해발 8천 설산 망령", "얼어붙은 등반가 구울", "빙룡 뼈조각 와이번", "만년설 빙하 골렘"],
        named: "🗿 고룡 묘지 수호 거신병",
        boss: "🦴 태고의 재앙 ‘서리 본 드래곤’"
    },
    11: {
        name: "시베리아 & 타클라마칸",
        town: "assets/ui/regions/town_bg_11.png",
        battle: "assets/ui/regions/battle_bg_11.png",
        gateType: "gold",
        traitId: "trait_boss_slayer",
        traitName: "⚔️ 학살자의 투기 (네임드 및 보스 피해 +10%)",
        gateFeature: "유리 사막의 열사와 동토의 혹한이 교차하는 대륙 금문. 모래폭풍 속에서 유리 스콜피온 여왕이 맹독 침을 노립니다.",
        monsters: ["동토의 서리 늑대기병", "타클라마칸 모래 전갈", "유리 사막 아누비스", "열사 폭풍 정령"],
        named: "🏜️ 모래지옥 친위장 사하라",
        boss: "🦂 사막 여왕 유리 스콜피온"
    },
    12: {
        name: "독일 라인강 & 북미 로키산맥",
        town: "assets/ui/regions/town_bg_12.png",
        battle: "assets/ui/regions/battle_bg_12.png",
        gateType: "platinum",
        traitId: "trait_iron_body",
        traitName: "🛡️ 대지의 용철 (최대 체력 및 화염 저항 +18%)",
        gateFeature: "화산 마그마가 분출하는 로키산맥의 플래티넘문. 대륙을 녹이는 대재앙 용암 베히모스와 화염 마수 군단이 포효합니다.",
        monsters: ["라인강 타락 마수병", "유럽 침공 키메라", "로키산맥 화염 임프", "마그마 암석 거인"],
        named: "🔥 마수 군단장 벨제부브",
        boss: "🌋 북미 대재앙 ‘용암 베히모스’"
    },
    13: {
        name: "태평양 성층권 금문 모함",
        town: "assets/ui/regions/town_bg_13.png",
        battle: "assets/ui/regions/battle_bg_13.png",
        gateType: "gold",
        traitId: "trait_undead_cmd",
        traitName: "🛸 제3군단장 해킹망 (소환수 및 크로스 스킬 위력 +20%)",
        gateFeature: "성층권 상공 30km에 떠 있는 외계 선봉 모함 금문. 이단자 참모 벨록을 구출하고 선봉 사령관 타르코스를 격파해야 합니다.",
        monsters: ["화성 제국 강습 보병", "반중력 플라즈마 드론", "사이오닉 심문관", "외계 중장갑 센추리온"],
        named: "🧬 이단자 참모 벨록 (구출전)",
        boss: "🛸 외계 선봉 사령관 타르코스"
    },
    14: {
        name: "2070 성층권 다이아몬드문",
        town: "assets/ui/regions/town_bg_14.png",
        battle: "assets/ui/regions/battle_bg_14.png",
        gateType: "diamond",
        traitId: "trait_boss_slayer",
        traitName: "👑 사령군주의 종언 (모든 최종 피해량 +35% & 영혼 각인 개방)",
        gateFeature: "인류 멸망의 날 열렸던 최후의 성층권 다이아몬드문. 대장군 볼가르와 여왕 시렌을 넘어 외계 제국 무감정의 황제와 결전을 벌입니다.",
        monsters: ["황실 친위대 결사병", "아공간 암살 팬텀", "성층권 궤도 폭격기", "차원 파쇄 거신"],
        named: "⚔️ 대장군 볼가르 & 여왕 시렌",
        boss: "👑 외계 제국 ‘무감정의 황제’"
    }
};

"""

assert start_idx != -1 and end_idx != -1
updated = text[:start_idx] + new_block + text[end_idx:]
with open(path, "w", encoding="utf-8") as f:
    f.write(updated)
print("Successfully enriched REGIONS_DATA and GATES_DATA in display_data.js")
