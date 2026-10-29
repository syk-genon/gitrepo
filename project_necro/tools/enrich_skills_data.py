# -*- coding: utf-8 -*-
"""
ENRICH 72 SKILLS WITH REAL MECHANICS & EFFECTS
Matches user requirement:
"스킬이랑 효과가 안맞는게 너무 많거든? 특히 마나쉴드 및 점멸 이런건 회피율증가 및 임시체력 생성 이런거 아이기스 패 이런거면 방어력 증가 혹은 몇번 무적 이런거여야 하는데 그냥 다 공격기인거같아. 모든 스킬 각 스킬 이름에 맞게 만들어줘"
"""
import re

DATA_PATH = r"D:\workspace\GEMINI\project_necro\display_data.js"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Detailed mechanics table for all 72 skills
SKILL_MECHANICS = {
    # 01. Necromancer
    "necro_1": {
        "kind": "summon", "target": "self", "vfxEffect": "summon",
        "badge": "💀 군단 소환", "floatingText": "SUMMONED! +3 MINIONS",
        "buffDesc": "해골 부하 3기 소환 & 소환수 공격력 +30%",
        "log": "대지에서 해골 병사들을 부활시켜 군주 뒤편에 결집시켰습니다!"
    },
    "necro_2": {
        "kind": "corpse_burst", "target": "enemy", "vfxEffect": "corpse_burst",
        "badge": "💥 시체 폭발", "floatingText": "💀 CORPSE BURST!",
        "buffDesc": "소환수/사체 자폭: 반경 350px 암흑 파편 피해",
        "log": "소환된 해골 부하가 적진으로 뛰어들어 암흑 혈무와 뼈파편으로 대폭발을 일으켰습니다!"
    },
    "necro_3": {
        "kind": "projectile", "target": "enemy", "vfxEffect": "projectile",
        "badge": "🎯 관통 뼈창", "floatingText": "PIERCE ×5!",
        "buffDesc": "관통 뼈창 5연사 (적 방어력 40% 무시)",
        "log": "칠흑의 뼈창 5발이 일직선상의 모든 적을 꿰뚫으며 관통 피해를 입혔습니다!"
    },
    "necro_4": {
        "kind": "shield", "target": "self", "vfxEffect": "bone_shield",
        "badge": "🛡️ 뼈방패 & 유령화", "floatingText": "🛡️ BONE SHIELD +18,000",
        "buffDesc": "피해 50% 흡수 보호막 + 이동속도 +40% & 회피율 +25%",
        "log": "회전하는 백골 방패가 영웅을 감싸 18,000의 보호막을 생성하고 유령화 보법으로 이동속도가 증가했습니다!"
    },
    "necro_5": {
        "kind": "summon", "target": "self", "vfxEffect": "summon_elite",
        "badge": "⚔️ 군단장 아서", "floatingText": "ARTHUR SUMMONED!",
        "buffDesc": "제1군단장 듀라한 아서 강림 & 전방 흑염 돌격",
        "log": "제1군단장 듀라한 아서가 칠흑의 대검을 들고 참전하여 전방을 가로질렀습니다!"
    },
    "necro_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "ice_cataclysm",
        "badge": "❄️ 진 블리자드", "floatingText": "❄️ ABSOLUTE BLIZZARD!",
        "buffDesc": "빙룡 강림 + 전장 영구 동결 + 거대 빙창 폭격",
        "log": "상공에 전설의 서리 본 드래곤이 강림하며 전장에 칠흑 얼음창을 쏟아부어 전원을 동결시켰습니다!"
    },

    # 02. Guardian
    "guard_1": {
        "kind": "buff", "target": "self", "vfxEffect": "iron_wall",
        "badge": "🛡️ 철벽 & 가시 반사", "floatingText": "🛡️ DEF +80% & THORN ON",
        "buffDesc": "방어력 +80% 증가 & 피격 시 방어력 150% 가시 반사 (3회 무효화)",
        "log": "아이기스의 철벽을 전개하여 방어력이 폭증하고 적 공격을 100% 흘려내며 가시 반사 태세에 돌입했습니다!"
    },
    "guard_2": {
        "kind": "cc", "target": "enemy", "vfxEffect": "shield_bash",
        "badge": "🔨 방패 돌진", "floatingText": "STUN 2.5s & KNOCKBACK!",
        "buffDesc": "전방 돌진 넉백 + 광역 기절 2.5초",
        "log": "용철 대방패로 지면을 박차고 돌진하여 전방 적들을 강타하고 2.5초간 기절시켰습니다!"
    },
    "guard_3": {
        "kind": "attack", "target": "enemy", "vfxEffect": "earthquake",
        "badge": "🌋 대지 분쇄", "floatingText": "EARTHQUAKE DEF×3.0!",
        "buffDesc": "현재 방어력의 300% 대지 지진파 피해",
        "log": "대방패를 지면에 내리찍어 방어력에 비례한 거대한 지진파 충격으로 대지를 함몰시켰습니다!"
    },
    "guard_4": {
        "kind": "shield", "target": "self", "vfxEffect": "aegis_shield",
        "badge": "🏰 연대 방진 방벽", "floatingText": "🛡️ CITADEL SHIELD +32,000",
        "buffDesc": "최대 체력의 50%에 달하는 은백색 요새 보호막 생성",
        "log": "성채급 은백색 방진 결계를 전개하여 32,000의 임시 체력 보호막을 생성했습니다!"
    },
    "guard_5": {
        "kind": "debuff", "target": "enemy", "vfxEffect": "taunt_roar",
        "badge": "📢 도발의 포효", "floatingText": "TAUNT! ATK -40% DRAIN",
        "buffDesc": "주변 적 공격력 -40% 강탈 & 영웅 방어력 +60% 흡수 증폭",
        "log": "포효를 내질러 적들의 전의를 꺾고 공격력을 40% 강탈하여 자신의 방패에 축적했습니다!"
    },
    "guard_ult": {
        "kind": "invulnerable", "target": "both", "vfxEffect": "aegis_nova",
        "badge": "🌟 아이기스 노바", "floatingText": "🌟 10s INVINCIBLE & NOVA!",
        "buffDesc": "10초간 절대 무적(Invulnerable) 성채 + 누적 방어량 500% 폭발",
        "log": "절대 방벽 아이기스 노바를 가동하여 10초간 완전 무적 성채에 돌입하고 전장에 충격파를 방출했습니다!"
    },

    # 03. Storm Wizard
    "storm_1": {
        "kind": "buff", "target": "self", "vfxEffect": "overcharge",
        "badge": "⚡ 마력 동조망 과충전", "floatingText": "⚡ OVERCHARGE! MP COST 0",
        "buffDesc": "마력 과충전: 스킬 마나 소모 0 & 마법 범위 +50%",
        "log": "성층권 마력 동조망과 공명하여 마력 과충전 상태에 진입! 마나 소모 없이 마법 폭풍을 전개합니다!"
    },
    "storm_2": {
        "kind": "attack", "target": "enemy", "vfxEffect": "chain_lightning",
        "badge": "⚡ 체인 라이트닝", "floatingText": "CHAIN LIGHTNING ×8!",
        "buffDesc": "적 8기 연쇄 뇌격 및 감전 유발",
        "log": "고전압 푸른 벼락이 적 8기의 몸체를 연쇄적으로 튀며 전신을 감전시켰습니다!"
    },
    "storm_3": {
        "kind": "attack", "target": "enemy", "vfxEffect": "meteor",
        "badge": "☄️ 헬파이어 메테오", "floatingText": "METEOR BURST!",
        "buffDesc": "고열 마도 운석 낙하 + 지면 화염 장판 지속 피해",
        "log": "하늘을 가르고 낙하한 거대한 화염 운석이 적진을 직격하여 불바다로 만들었습니다!"
    },
    "storm_4": {
        "kind": "blink_shield", "target": "self", "vfxEffect": "mana_shield",
        "badge": "🔷 점멸 & 마나실드", "floatingText": "🔷 MANA SHIELD +24,000 & BLINK",
        "buffDesc": "후방 순간이동(회피율 +75%) + 마나 150% 마법 보호막 생성",
        "log": "공간을 굴절시켜 안전지대로 순간 점멸하고, 마력을 응축하여 24,000의 마나 보호막을 둘렀습니다!"
    },
    "storm_5": {
        "kind": "attack", "target": "enemy", "vfxEffect": "artillery",
        "badge": "🚀 마도포 300문", "floatingText": "BARRAGE 30 SHELLS!",
        "buffDesc": "전방 300문 마도포탄 30연속 융단폭격",
        "log": "마도포병여단의 300문 포신이 일제히 불을 뿜으며 전방을 초토화했습니다!"
    },
    "storm_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "arc_nova",
        "badge": "⚡ 템페스트 아크 노바", "floatingText": "⚡ TEMPEST CATACLYSM!",
        "buffDesc": "성층권 뇌전 폭풍 소환: 화면 내 적 전체 분자 증발",
        "log": "성층권에 거대한 뇌운을 소환하여 전장 전체에 메가볼트 벼락을 투하해 적들을 증발시켰습니다!"
    },

    # 04. Sniper
    "snip_1": {
        "kind": "buff", "target": "self", "vfxEffect": "crosshair",
        "badge": "🎯 약점 포착 (매의 눈)", "floatingText": "🎯 WEAKPOINT MARKED!",
        "buffDesc": "적 방어력 100% 무시 & 치명타 확률 +50%",
        "log": "초정밀 매의 눈으로 보스의 동력 코어 약점을 락온하여 방어력을 100% 무력화시켰습니다!"
    },
    "snip_2": {
        "kind": "projectile", "target": "enemy", "vfxEffect": "railgun",
        "badge": "💥 대구경 관통 저격", "floatingText": "PIERCE RAILGUN CRIT!",
        "buffDesc": "마하 7 초고속 탄환 일직선 전원 관통",
        "log": "강두호제 마도총의 방아쇠를 당겨 음속의 7배로 날아간 탄환이 적들의 중심을 꿰뚫었습니다!"
    },
    "snip_3": {
        "kind": "attack", "target": "enemy", "vfxEffect": "claymore",
        "badge": "💣 폭발 크레모아", "floatingText": "CLAYMORE MINE BLAST!",
        "buffDesc": "후방 도약 회피 + 고성능 지뢰 지면 매설 폭발",
        "log": "후방으로 도약하며 지뢰를 매설하여 접근하는 적들을 일제히 폭파시켰습니다!"
    },
    "snip_4": {
        "kind": "stealth", "target": "self", "vfxEffect": "camouflage",
        "badge": "🕶️ 고스트 카모플라주", "floatingText": "🕶️ STEALTH ON & ATK +300%",
        "buffDesc": "완전 은신 (타겟팅 면역, 회피율 +80%) + 다음 탄환 3배 피해",
        "log": "광학 미채 코트로 신체를 숨겨 완전 은신에 돌입했습니다! 다음 사격이 치명타로 적중합니다."
    },
    "snip_5": {
        "kind": "cc", "target": "enemy", "vfxEffect": "core_break",
        "badge": "⚡ 동력 코어 정밀 파괴", "floatingText": "CORE BROKEN! STUN 4s",
        "buffDesc": "보스 방어력 0화 + 4초간 완전 기능 정지 스턴",
        "log": "보스의 중추 동력 코어를 정밀 타격하여 4초간 완전 기능 마비 상태로 만들었습니다!"
    },
    "snip_ult": {
        "kind": "cataclysm", "target": "enemy", "vfxEffect": "space_bullet",
        "badge": "🌌 50km 공간 굴절 저격", "floatingText": "🌌 50km DIMENSIONAL BULLET!",
        "buffDesc": "차원 왜곡 확정 즉사급 탄환 투사",
        "log": "50km 밖에서 쏘아 올린 차원 왜곡 탄환이 시공간을 가르고 보스의 심장에 박혔습니다!"
    },

    # 05. High Priest
    "priest_1": {
        "kind": "buff", "target": "self", "vfxEffect": "overheal",
        "badge": "⚖️ 오버힐 심판 전환", "floatingText": "⚖️ OVERHEAL BURST ON!",
        "buffDesc": "초과 치유량 100%가 신성 고정 피해 벼락으로 전환",
        "log": "신성 성역의 법칙을 발동하여 아군의 초과 회복량을 황금빛 심판 벼락으로 전환합니다!"
    },
    "priest_2": {
        "kind": "heal", "target": "both", "vfxEffect": "holy_bolt",
        "badge": "✨ 홀리 라이트닝", "floatingText": "💚 HEAL +12,000 & SMITE!",
        "buffDesc": "아군/자신 체력 +12,000 회복 + 주변 적 신성 감전",
        "log": "성스러운 빛줄기가 영웅의 상처를 치유하고 적들에게는 성광 타격을 가했습니다!"
    },
    "priest_3": {
        "kind": "heal", "target": "both", "vfxEffect": "holy_flame",
        "badge": "🔥 정화의 성염", "floatingText": "CLEANSE ALL & BURN!",
        "buffDesc": "모든 상태이상/디버프 즉시 해제 + 적 지속 화상",
        "log": "신성한 불길로 영웅에게 걸린 모든 독과 저주를 정화하고 적들을 불태웠습니다!"
    },
    "priest_4": {
        "kind": "shield", "target": "self", "vfxEffect": "angel_barrier",
        "badge": "🪽 천상의 축복 방벽", "floatingText": "✨ CELESTIAL SHIELD +25,000",
        "buffDesc": "전군 공격력 +50% 버프 + 피해 40% 흡수 성광 방벽 생성",
        "log": "천사의 날개가 영웅을 감싸며 25,000의 성광 방벽과 전군 공격력 50% 버프를 부여했습니다!"
    },
    "priest_5": {
        "kind": "heal", "target": "self", "vfxEffect": "pillar_of_light",
        "badge": "☀️ 구원의 빛기둥", "floatingText": "💚 FULL HEAL +50,000!",
        "buffDesc": "하늘에서 빛기둥 강림: 체력 100% 즉시 완전 회복",
        "log": "하늘이 열리고 구원의 빛기둥이 쏟아져 내려와 빈사 상태의 체력을 100% 완치시켰습니다!"
    },
    "priest_ult": {
        "kind": "invulnerable", "target": "both", "vfxEffect": "great_sanctuary",
        "badge": "☀️ 대성역: 천벌의 빛기둥", "floatingText": "☀️ IMMORTAL SANCTUARY 15s!",
        "buffDesc": "15초간 전원 불사(Immortal) 성역 + 오버힐 500% 성광 융단폭격",
        "log": "대성역을 전개하여 15초간 절대 불사 상태를 유지하며 천벌의 신성 벼락으로 적진을 강타했습니다!"
    },

    # 06. Shadow Assassin
    "as_1": {
        "kind": "debuff", "target": "enemy", "vfxEffect": "poison_mark",
        "badge": "🩸 맹독 & 출혈 각인", "floatingText": "POISON & BLEED ×10!",
        "buffDesc": "타격 시 도트 피해 중첩 (최대 10중첩)",
        "log": "적의 혈도에 맹독과 출혈을 각인하여 지속적으로 체력을 갉아먹게 만들었습니다!"
    },
    "as_2": {
        "kind": "attack", "target": "enemy", "vfxEffect": "shadow_step",
        "badge": "🗡️ 그림자 습격", "floatingText": "BACKSTAB CRIT!",
        "buffDesc": "적 배후 순간이동 + 확정 치명타 급소 찌르기",
        "log": "그림자 속으로 녹아들어 적의 사각지대 배후로 이동해 심장을 찔렀습니다!"
    },
    "as_3": {
        "kind": "invulnerable", "target": "enemy", "vfxEffect": "blade_dance",
        "badge": "⚔️ 흑도 난무 (12연참)", "floatingText": "12-HIT BLADE DANCE!",
        "buffDesc": "1.5초간 무적 상태 돌입 + 전방 12연속 참수",
        "log": "무적 상태로 그림자 참격을 연속 12회 작렬시켜 적을 난도질했습니다!"
    },
    "as_4": {
        "kind": "summon", "target": "self", "vfxEffect": "shadow_clone",
        "badge": "👥 그림자 분신술", "floatingText": "SHADOW CLONE ×2 SUMMONED!",
        "buffDesc": "회피율 +50% + 공격을 복제하는 분신 2기 도열",
        "log": "암살자의 그림자 분신 2기가 소환되어 군주 뒤에 집결하고 공격을 복제합니다!"
    },
    "as_5": {
        "kind": "corpse_burst", "target": "enemy", "vfxEffect": "blood_burst",
        "badge": "💥 혈독 폭살진", "floatingText": "💥 BLOOD-TOXIN EXPLOSION!",
        "buffDesc": "적들에게 누적된 모든 출혈/독 스택 일제히 폭파",
        "log": "적의 혈관 속에 잠복해 있던 모든 독과 혈기를 한순간에 기폭시켰습니다!"
    },
    "as_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "time_stop_cut",
        "badge": "🌑 차원 무음 참수", "floatingText": "⏳ TIME STOP & 100 SLASHES!",
        "buffDesc": "3초간 시간 정지 + 100개 환영 일제 참수",
        "log": "전장의 시간을 3초간 멈추고 100개의 그림자 환영이 적의 목을 일제히 베어 넘겼습니다!"
    },

    # 07. Sword Master
    "sm_1": {
        "kind": "buff", "target": "self", "vfxEffect": "aura_blade",
        "badge": "⚔️ 검기 발현 (오러 블레이드)", "floatingText": "⚔️ AURA BLADE ON! REACH ×2",
        "buffDesc": "검 사거리/관통력 2배 & 모든 평타가 검기로 방출",
        "log": "청룡의 기운을 검신에 둘러 푸른 검기를 발현시키고 리치를 2배로 확장했습니다!"
    },
    "sm_2": {
        "kind": "attack", "target": "enemy", "vfxEffect": "flash_slash",
        "badge": "⚡ 발도: 섬광일섬", "floatingText": "FLASH SLASH 1-HIT!",
        "buffDesc": "빛의 속도로 화면 가로축 전체 일도양단",
        "log": "검집에서 검을 뽑아내는 순간 화면 전체가 양단되며 섬광이 작렬했습니다!"
    },
    "sm_3": {
        "kind": "attack", "target": "enemy", "vfxEffect": "slash_5combo",
        "badge": "🌪️ 질풍노도 5연참", "floatingText": "5-COMBO SWORD WIND!",
        "buffDesc": "바람을 가르는 5연속 푸른 검풍 발사",
        "log": "질풍처럼 빠른 속도로 5개의 검풍을 연속 발사하여 적진을 베어 넘겼습니다!"
    },
    "sm_4": {
        "kind": "parry", "target": "self", "vfxEffect": "mind_parry",
        "badge": "👁️ 심안 패링 (흘려내기)", "floatingText": "👁️ PARRY! 300% COUNTER READY",
        "buffDesc": "적 공격 피격 완전 무효화 + 쿨타임 리셋 + 3배 즉시 반격",
        "log": "심안으로 적 공격의 궤적을 읽고 칼등으로 완벽히 흘려내어 무효화했습니다!"
    },
    "sm_5": {
        "kind": "attack", "target": "enemy", "vfxEffect": "blue_dragon",
        "badge": "🐉 청룡참 (Blue Dragon)", "floatingText": "🐉 BLUE DRAGON STRIKE!",
        "buffDesc": "푸른 용 형상의 거대 검기 전방 방출",
        "log": "백도훈의 청룡 신검에서 거대한 푸른 용이 솟구쳐 전방을 분쇄했습니다!"
    },
    "sm_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "ten_thousand_swords",
        "badge": "🐉 만검귀종: 진 청룡참", "floatingText": "🐉 10,000 SWORDS CATACLYSM!",
        "buffDesc": "천 개의 신검 하늘에서 비처럼 낙하 + 대지 폭쇄",
        "log": "하늘에서 천 개의 신검이 쏟아져 내린 후 거대한 청룡이 전장을 뒤흔들었습니다!"
    },

    # 08. Death Knight
    "dk_1": {
        "kind": "buff", "target": "self", "vfxEffect": "blood_thirst",
        "badge": "🩸 피의 갈증", "floatingText": "🩸 LIFESTEAL +35% ACTIVE",
        "buffDesc": "피해의 35% 체력 흡수 & 체력 낮을수록 공격력 증폭",
        "log": "망자의 피의 갈증을 활성화하여 흡혈 능력을 극대화하고 공격력을 축적했습니다!"
    },
    "dk_2": {
        "kind": "attack", "target": "enemy", "vfxEffect": "dark_slash",
        "badge": "🔥 흑염 대검 베기", "floatingText": "HP SACRIFICE × 300% ATK!",
        "buffDesc": "체력 5% 소모 ➔ 300% 흑염 참격 방출",
        "log": "자신의 혈기를 바쳐 대검에 불을 붙이고 흑염의 참격을 날렸습니다!"
    },
    "dk_3": {
        "kind": "cc", "target": "enemy", "vfxEffect": "death_grip",
        "badge": "🖐️ 죽음의 손아귀", "floatingText": "PULL 3 ENEMIES & BIND!",
        "buffDesc": "원거리 적 3기 전방으로 강제 견인 + 2초 속박",
        "log": "어둠의 손길을 뻗어 도망치던 원거리 적들을 영웅 코앞으로 끌고 왔습니다!"
    },
    "dk_4": {
        "kind": "shield", "target": "self", "vfxEffect": "undead_armor",
        "badge": "🛡️ 망자의 갑주", "floatingText": "🛡️ DAMAGE DELAY 50% ABSORB",
        "buffDesc": "받는 피해 50% 즉시 경감 및 10초 분할 지연",
        "log": "어둠의 판금갑이 받는 피해의 절반을 흡수하여 사망의 위기를 넘겼습니다!"
    },
    "dk_5": {
        "kind": "attack", "target": "enemy", "vfxEffect": "guillotine",
        "badge": "⚔️ 단두대 처형", "floatingText": "💀 EXECUTION GUILLOTINE!",
        "buffDesc": "체력 35% 이하 적에게 거대 단두대 즉사급 낙하",
        "log": "하늘에서 칠흑의 단두대 칼날이 떨어져 적의 숨통을 단번에 끊었습니다!"
    },
    "dk_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "avalon_guillotine",
        "badge": "⚔️ 아발론의 흑염 단두대", "floatingText": "⚔️ DULLAHAN LEGION CHARGE!",
        "buffDesc": "듀라한 기사단 전원 소환 돌격 + 전장 흑염 양단",
        "log": "아발론의 듀라한 기사단이 지옥의 불꽃을 휘감고 돌격하여 전장을 갈라놓았습니다!"
    },

    # 09. Martial King
    "mk_1": {
        "kind": "buff", "target": "self", "vfxEffect": "vajra_body",
        "badge": "🥋 금강불괴 (강철 피부)", "floatingText": "🥋 VAJRA BODY! DEF +100%",
        "buffDesc": "방어력 +100% & 피격 경직 및 넉백 완전 면역",
        "log": "곤륜의 금강불괴를 시전하여 전신을 황동빛 강철로 만들어 경직 면역 상태가 되었습니다!"
    },
    "mk_2": {
        "kind": "attack", "target": "enemy", "vfxEffect": "breaker_punch",
        "badge": "👊 파쇄권 (붕권)", "floatingText": "ARMOR PIERCE PUNCH!",
        "buffDesc": "적 방어력 100% 관통 후방 관통 충격파",
        "log": "정권 지르기 한 방으로 적의 방어구를 깨부수고 후방까지 궤멸시켰습니다!"
    },
    "mk_3": {
        "kind": "cc", "target": "enemy", "vfxEffect": "punch_flurry",
        "badge": "🌪️ 폭풍 연환격", "floatingText": "15-HIT STUN FLURRY!",
        "buffDesc": "초당 15타 주먹 난타 + 슈퍼아머 강제 파괴",
        "log": "보이지 않는 속도로 주먹을 쏟아부어 보스의 슈퍼아머를 박살 냈습니다!"
    },
    "mk_4": {
        "kind": "buff", "target": "both", "vfxEffect": "flash_step",
        "badge": "💨 순보 & 내공 폭발", "floatingText": "💨 FLASH STEP & ATK SPD +50%",
        "buffDesc": "적진 순간 돌진 + 주변 넉백 + 공격속도 +50%",
        "log": "순보로 적진 한가운데로 침투하여 내공을 폭발시키고 공속을 대폭 끌어올렸습니다!"
    },
    "mk_5": {
        "kind": "attack", "target": "enemy", "vfxEffect": "haoh_blast",
        "badge": "💥 패왕 열파참", "floatingText": "LAVA ERUPTION WAVE!",
        "buffDesc": "양 주먹으로 지면을 강타해 거대 기공 용암파 분출",
        "log": "지면에 주먹을 박아 넣어 거대한 투기 기둥을 솟구치게 했습니다!"
    },
    "mk_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "taishan_smash",
        "badge": "👊 일격필살: 태산파쇄격", "floatingText": "👊 COSMIC TAISHAN SMASH!",
        "buffDesc": "우주적 투기 응축 펀치로 전장 행성급 함몰",
        "log": "우주적 투기를 맨주먹에 그러모아 전장 전체를 함몰시키는 펀치를 작렬했습니다!"
    },

    # 10. Psionic Tactician
    "psi_1": {
        "kind": "buff", "target": "self", "vfxEffect": "tactical_calc",
        "badge": "🧠 전술 연산 알고리즘", "floatingText": "🧠 CDR +35% & EVA +30%",
        "buffDesc": "스킬 쿨타임 가속 +35% & 아군 전체 회피율 +30%",
        "log": "화성 전술 인공지능을 활성화하여 적 공격 패턴을 연산하고 회피율을 극대화했습니다!"
    },
    "psi_2": {
        "kind": "cc", "target": "enemy", "vfxEffect": "gravity_well",
        "badge": "🕳️ 중력장 압축 (블랙홀)", "floatingText": "BLACK HOLE PULL!",
        "buffDesc": "적들을 한 점으로 강력하게 빨아들이는 중력 구체",
        "log": "시공간을 왜곡하는 미니 블랙홀을 생성하여 흩어진 적들을 한곳으로 흡입했습니다!"
    },
    "psi_3": {
        "kind": "attack", "target": "enemy", "vfxEffect": "talisman",
        "badge": "📜 음양 오행 부적진", "floatingText": "5-ELEMENT BURST!",
        "buffDesc": "5대 속성 부적 회전 후 원소 연쇄 폭발",
        "log": "오행 부적을 회전시켜 5가지 원소의 연쇄 폭발로 적들을 타격했습니다!"
    },
    "psi_4": {
        "kind": "cc", "target": "enemy", "vfxEffect": "mind_hack",
        "badge": "👾 사이오닉 해킹 (세뇌)", "floatingText": "👾 2 ENEMIES BRAINWASHED!",
        "buffDesc": "적 2기를 아군 편으로 8초간 해킹 세뇌",
        "log": "외계 신경망을 해킹하여 적 2기를 아군으로 변절시켜 자폭하도록 유도했습니다!"
    },
    "psi_5": {
        "kind": "summon", "target": "self", "vfxEffect": "drone_laser",
        "badge": "🛸 외계 강습 드론", "floatingText": "DRONES DEPLOYED!",
        "buffDesc": "고출력 플라즈마 레이저 포탑 4기 전개",
        "log": "반중력 드론 포탑 4기를 호출하여 전방에 지속 레이저 탄막을 형성했습니다!"
    },
    "psi_ult": {
        "kind": "cataclysm", "target": "enemy", "vfxEffect": "mothership_beam",
        "badge": "🛸 궤도 모함 해킹: 플라즈마 폭격", "floatingText": "🛸 MOTHERSHIP PLASMA CANNON!",
        "buffDesc": "성층권 적 기함 주포 역해킹 ➔ 플라즈마 폭격",
        "log": "성층권 외계 모함의 주포 제어권을 탈취하여 지상 적진에 플라즈마 폭격을 쏟았습니다!"
    },

    # 11. Gravity Berserker
    "ber_1": {
        "kind": "buff", "target": "self", "vfxEffect": "berserk_rage",
        "badge": "🔥 광전사의 피", "floatingText": "🔥 BERSERK! ATK +250% SPD +40%",
        "buffDesc": "잃은 체력에 비례해 공격력 최대 +300% 폭증",
        "log": "혈액이 끓어오르며 상처를 입을수록 괴물 같은 공격력을 발휘하는 광폭화에 돌입했습니다!"
    },
    "ber_2": {
        "kind": "attack", "target": "enemy", "vfxEffect": "axe_whirl",
        "badge": "🪓 중력 도끼 휠윈드", "floatingText": "WHIRLWIND 360° SPIN!",
        "buffDesc": "이동하며 360도 연속 회전 참격",
        "log": "중력 쌍도끼를 휘두르며 폭풍처럼 회전하여 주변 적들을 토막 냈습니다!"
    },
    "ber_3": {
        "kind": "attack", "target": "enemy", "vfxEffect": "sand_storm",
        "badge": "🌪️ 사막의 혈풍참", "floatingText": "BLOOD SANDSTORM SLASH!",
        "buffDesc": "황금 곡도로 거대한 모래폭풍과 출혈 검풍 발사",
        "log": "사막의 모래폭풍과 피의 검기를 결합해 전방으로 발사했습니다!"
    },
    "ber_4": {
        "kind": "invulnerable", "target": "self", "vfxEffect": "undying_rage",
        "badge": "⚡ 불사 광란 (언다잉)", "floatingText": "⚡ 5s IMMORTAL RAGE!",
        "buffDesc": "5초간 체력이 1 이하로 내려가지 않는 완전 불사 상태",
        "log": "치명상을 거부하고 5초간 어떠한 공격에도 죽지 않는 불사의 광란에 들어섰습니다!"
    },
    "ber_5": {
        "kind": "attack", "target": "enemy", "vfxEffect": "giant_leap",
        "badge": "🪓 거인 학살자의 도약", "floatingText": "GIANT LEAP SLAM!",
        "buffDesc": "공중 높이 도약 후 중력 도끼로 대지 찍기",
        "log": "하늘 높이 도약한 뒤 체중을 실어 대지를 내리찍어 지반을 갈라놓았습니다!"
    },
    "ber_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "ragnarok",
        "badge": "🌌 라그나로크: 중력 붕괴", "floatingText": "🌌 RAGNAROK 1000% COLLAPSE!",
        "buffDesc": "체력을 1로 깎고 전장 전체 중력 붕괴 1000% 광역 파멸",
        "log": "자신의 생명력을 불태워 중력장을 붕괴시키고 전장에 종말의 충격파를 일으켰습니다!"
    },

    # 12. Cryo Empress
    "cryo_1": {
        "kind": "debuff", "target": "enemy", "vfxEffect": "subzero_aura",
        "badge": "❄️ 절대영도의 한기", "floatingText": "❄️ ENEMY SLOW -50% & CHILL",
        "buffDesc": "주변 적들의 공격/이동속도 50% 강제 둔화 오라",
        "log": "절대영도의 한기를 뿜어내어 적들의 관절과 혈관을 얼어붙게 만들었습니다!"
    },
    "cryo_2": {
        "kind": "projectile", "target": "enemy", "vfxEffect": "ice_spears",
        "badge": "🧊 아이스 스피어 개틀링", "floatingText": "ICE GATLING 20-SHOTS!",
        "buffDesc": "초고속 고드름 탄환 20발 연속 기관총 사격",
        "log": "영구동토의 고드름 창 20발을 기관총처럼 연사하여 적들을 꿰뚫었습니다!"
    },
    "cryo_3": {
        "kind": "cc", "target": "enemy", "vfxEffect": "frost_nova",
        "badge": "🧊 프로스트 노바 & 빙벽", "floatingText": "🧊 ALL ENEMIES FROZEN 3s!",
        "buffDesc": "주변 모든 적 3초간 완전 빙결 + 얼음 성벽 차단",
        "log": "발밑에서 얼음 결정을 폭발시켜 반경 내 모든 적을 3초간 영구 동결시켰습니다!"
    },
    "cryo_4": {
        "kind": "invulnerable", "target": "self", "vfxEffect": "ice_jewel",
        "badge": "💎 얼음 여왕의 보석화", "floatingText": "💎 ICE JEWEL 3s INVINCIBLE & MP HEAL",
        "buffDesc": "3초간 완전 무적 얼음 결정체 변신 + 초당 마나 30% 회복",
        "log": "신체를 순수한 빙정 보석으로 결정화하여 모든 피해를 무효화하고 마력을 채웠습니다!"
    },
    "cryo_5": {
        "kind": "attack", "target": "enemy", "vfxEffect": "glacier_fall",
        "badge": "🏔️ 글래시어 폴 (빙하 낙하)", "floatingText": "GLACIER CRUSH!",
        "buffDesc": "거대한 빙하 덩어리를 소환해 적들을 압살",
        "log": "성층권에서 거대한 만년설 빙하를 소환하여 적들을 짓눌렀습니다!"
    },
    "cryo_ult": {
        "kind": "cataclysm", "target": "both", "vfxEffect": "diamond_dust",
        "badge": "❄️ 절대영도: 다이아몬드 더스트", "floatingText": "❄️ DIAMOND DUST SHATTER!",
        "buffDesc": "전장 전체를 영구 동결 후 유리처럼 산산조각 분쇄",
        "log": "다이아몬드 더스트를 휘몰아쳐 전장을 순식간에 얼리고 유리처럼 산산조각 냈습니다!"
    }
}

# Update CLASSES_DATA skills definitions in display_data.js
# For each skill in text, add kind, target, badge, floatingText, buffDesc, logMsg
for s_id, s_info in SKILL_MECHANICS.items():
    # Find { id: "s_id", ... }
    pat = re.compile(rf'(\{{\s*id:\s*"{s_id}",[\s\S]*?vfx:\s*"[^"]+")(\s*\}})')
    def rep_skill(m, info=s_info):
        extra = f', kind: "{info["kind"]}", target: "{info["target"]}", badge: "{info["badge"]}", floatingText: "{info["floatingText"]}", buffDesc: "{info["buffDesc"]}", logMsg: "{info["log"]}"'
        return f"{m.group(1)}{extra}{m.group(2)}"
    text = pat.sub(rep_skill, text)

with open(DATA_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Enriched all 72 skills in display_data.js with genuine mechanics!")
