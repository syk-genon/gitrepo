// =========================================================================
// 《목적을 잃지 않는 사령군주》 2D 도트 RPG 마스터 데이터베이스 (display_data.js)
// 12대 직업 x 6개 스킬 = 총 72개 고유 스킬 & 전용 16비트 도트 VFX 매핑 완비
// =========================================================================

const CLASSES_DATA = {
    "necro": {
        id: "necro",
        name: "💀 네크로맨서",
        model: "최미남 (사령군주)",
        sprite: "assets/agents/agent_male_nemesis.png?v=2",
        mainStat: "INT (마력)",
        color: "#00ffaa",
        desc: "적 처치 시 해골 군단 자동 소환 및 시체 폭발. 빙결 마법과 사령술의 결합.",
        passive: "적 처치 시 35% 확률로 해골 병사 소환. 소환수 공격력 +30%.",
        ultimate: "❄️ [진(眞) 블리자드 & 군단 각성]",
        skills: [
            { id: "necro_1", name: "해골 군단 소환", type: "core", desc: "처치한 적을 해골 전사로 부활시켜 전방에 배치", vfx: "assets/pixel_vfx/skills/vfx_necro_1.png?v=2", kind: "summon", target: "self", badge: "💀 군단 소환", floatingText: "SUMMONED! +3 MINIONS", buffDesc: "해골 부하 3기 소환 & 소환수 공격력 +30%", logMsg: "대지에서 해골 병사들을 부활시켜 군주 뒤편에 결집시켰습니다!" },
            { id: "necro_2", name: "시체 폭발 (Corpse Explosion)", type: "dps", desc: "적 사체를 폭발시켜 반경 내 적들에게 암흑 피해", vfx: "assets/pixel_vfx/skills/vfx_necro_2.png?v=2", kind: "corpse_burst", target: "enemy", badge: "💥 시체 폭발", floatingText: "💀 CORPSE BURST!", buffDesc: "소환수/사체 자폭: 반경 350px 암흑 파편 피해", logMsg: "소환된 해골 부하가 적진으로 뛰어들어 암흑 혈무와 뼈파편으로 대폭발을 일으켰습니다!" },
            { id: "necro_3", name: "본 스피어 (Bone Spear)", type: "dps", desc: "적들을 관통하는 날카로운 뼈창 5연속 투척", vfx: "assets/pixel_vfx/skills/vfx_necro_3.png?v=2", kind: "projectile", target: "enemy", badge: "🎯 관통 뼈창", floatingText: "PIERCE ×5!", buffDesc: "관통 뼈창 5연사 (적 방어력 40% 무시)", logMsg: "칠흑의 뼈창 5발이 일직선상의 모든 적을 꿰뚫으며 관통 피해를 입혔습니다!" },
            { id: "necro_4", name: "본 아머 & 망자 걸음", type: "utility", desc: "뼈방패로 피해를 흡수하고 유령화로 이동속도 증가", vfx: "assets/pixel_vfx/skills/vfx_necro_4.png?v=2", kind: "shield", target: "self", badge: "🛡️ 뼈방패 & 유령화", floatingText: "🛡️ BONE SHIELD +18,000", buffDesc: "피해 50% 흡수 보호막 + 이동속도 +40% & 회피율 +25%", logMsg: "회전하는 백골 방패가 영웅을 감싸 18,000의 보호막을 생성하고 유령화 보법으로 이동속도가 증가했습니다!" },
            { id: "necro_5", name: "군단장 소환: 아서", type: "elite", desc: "제1군단장 듀라한 아서를 소환하여 전방 흑염 돌격", vfx: "assets/pixel_vfx/skills/vfx_necro_5.png?v=2", kind: "summon", target: "self", badge: "⚔️ 군단장 아서", floatingText: "ARTHUR SUMMONED!", buffDesc: "제1군단장 듀라한 아서 강림 & 전방 흑염 돌격", logMsg: "제1군단장 듀라한 아서가 칠흑의 대검을 들고 참전하여 전방을 가로질렀습니다!" },
            { id: "necro_ult", name: "진(眞) 블리자드", type: "ult", desc: "전장 전체에 칠흑 얼음창을 낙하시켜 적 전체 동결 및 파멸", vfx: "assets/pixel_vfx/skills/vfx_necro_ult.png?v=2", kind: "cataclysm", target: "both", badge: "❄️ 진 블리자드", floatingText: "❄️ ABSOLUTE BLIZZARD!", buffDesc: "빙룡 강림 + 전장 영구 동결 + 거대 빙창 폭격", logMsg: "상공에 전설의 서리 본 드래곤이 강림하며 전장에 칠흑 얼음창을 쏟아부어 전원을 동결시켰습니다!" }
        ],
        setName: "이단자의 유물",
        setParts: [
            { part: "ring", name: "💍 이단자의 뼈가락지", icon: "assets/ui/items_sets/set_necro_ring.png?v=2", effect: "마나 회복 +50%, 소환수 공격력 +30%" },
            { part: "weapon", name: "🦯 심연의 척추 지팡이", icon: "assets/ui/items_sets/set_necro_weapon.png?v=2", effect: "[시체 폭발] 해금 & 제1군단장 아서 소환" },
            { part: "armor", name: "🥋 이단자의 늑골 갑옷", icon: "assets/ui/items_sets/set_necro_armor.png?v=2", effect: "소환수 자아 개안 & 제2군단장 카게미츠 소환" },
            { part: "helmet", name: "💀 이단자의 두개골 투구", icon: "assets/ui/items_sets/set_necro_helmet.png?v=2", effect: "정신계 상태이상 완전 면역 & 서리 본 드래곤 소환" },
            { part: "core", name: "💎 이단자의 심장석", icon: "assets/ui/items_sets/set_necro_core.png?v=2", effect: "제3군단장 벨록 소환 & [진(眞) 블리자드] 해금" }
        ]
    },
    "guardian": {
        id: "guardian",
        name: "🛡️ 아이기스 가디언",
        model: "김현태 (제1방패여단장)",
        sprite: "assets/agents/agent_male_cell_shield.png?v=2",
        mainStat: "DEF (방어력)",
        color: "#00f0ff",
        desc: "절대 방벽과 연대 방진. 방어력과 보호막 수치에 비례한 대지 강타 및 가시 반사.",
        passive: "받는 모든 피해 -20%. 피격 시 방어력의 150% 충격파 자동 반격.",
        ultimate: "🛡️ [절대 방벽: 아이기스 노바]",
        skills: [
            { id: "guard_1", name: "아이기스의 철벽", type: "core", desc: "상시 피격 반사 및 방어력의 20%를 공격력에 추가", vfx: "assets/pixel_vfx/skills/vfx_guard_1.png?v=2", kind: "buff", target: "self", badge: "🛡️ 철벽 & 가시 반사", floatingText: "🛡️ DEF +80% & THORN ON", buffDesc: "방어력 +80% 증가 & 피격 시 방어력 150% 가시 반사 (3회 무효화)", logMsg: "아이기스의 철벽을 전개하여 방어력이 폭증하고 적 공격을 100% 흘려내며 가시 반사 태세에 돌입했습니다!" },
            { id: "guard_2", name: "방패 돌진 강타", type: "dps", desc: "용철 대방패로 전방 돌진하여 광역 기절 및 넉백", vfx: "assets/pixel_vfx/skills/vfx_guard_2.png?v=2", kind: "cc", target: "enemy", badge: "🔨 방패 돌진", floatingText: "STUN 2.5s & KNOCKBACK!", buffDesc: "전방 돌진 넉백 + 광역 기절 2.5초", logMsg: "용철 대방패로 지면을 박차고 돌진하여 전방 적들을 강타하고 2.5초간 기절시켰습니다!" },
            { id: "guard_3", name: "대지 분쇄 (Earthquake)", type: "dps", desc: "대지를 내리찍어 방어력의 250%에 달하는 지진파 발생", vfx: "assets/pixel_vfx/skills/vfx_guard_3.png?v=2", kind: "attack", target: "enemy", badge: "🌋 대지 분쇄", floatingText: "EARTHQUAKE DEF×3.0!", buffDesc: "현재 방어력의 300% 대지 지진파 피해", logMsg: "대방패를 지면에 내리찍어 방어력에 비례한 거대한 지진파 충격으로 대지를 함몰시켰습니다!" },
            { id: "guard_4", name: "연대 방진 결속", type: "utility", desc: "최대 체력의 50%에 달하는 은백색 방어막 생성", vfx: "assets/pixel_vfx/skills/vfx_guard_4.png?v=2", kind: "shield", target: "self", badge: "🏰 연대 방진 방벽", floatingText: "🛡️ CITADEL SHIELD +32,000", buffDesc: "최대 체력의 50%에 달하는 은백색 요새 보호막 생성", logMsg: "성채급 은백색 방진 결계를 전개하여 32,000의 임시 체력 보호막을 생성했습니다!" },
            { id: "guard_5", name: "도발의 포효", type: "elite", desc: "주변 적 공격력을 40% 강탈하고 방어력 증폭", vfx: "assets/pixel_vfx/skills/vfx_guard_5.png?v=2", kind: "debuff", target: "enemy", badge: "📢 도발의 포효", floatingText: "TAUNT! ATK -40% DRAIN", buffDesc: "주변 적 공격력 -40% 강탈 & 영웅 방어력 +60% 흡수 증폭", logMsg: "포효를 내질러 적들의 전의를 꺾고 공격력을 40% 강탈하여 자신의 방패에 축적했습니다!" },
            { id: "guard_ult", name: "아이기스 노바", type: "ult", desc: "10초간 무적 성채 전개 + 누적 방어량의 400%로 전장 분쇄", vfx: "assets/pixel_vfx/skills/vfx_guard_ult.png?v=2", kind: "invulnerable", target: "both", badge: "🌟 아이기스 노바", floatingText: "🌟 10s INVINCIBLE & NOVA!", buffDesc: "10초간 절대 무적(Invulnerable) 성채 + 누적 방어량 500% 폭발", logMsg: "절대 방벽 아이기스 노바를 가동하여 10초간 완전 무적 성채에 돌입하고 전장에 충격파를 방출했습니다!" }
        ],
        setName: "아이기스 용철",
        setParts: [
            { part: "ring", name: "💍 거인의 강철 인장", icon: "assets/ui/items_sets/set_guardian_ring.png?v=2", effect: "방어력 +40%, 초당 최대 체력 3% 보호막" },
            { part: "weapon", name: "🛡️ 용철의 대방패", icon: "assets/ui/items_sets/set_guardian_weapon.png?v=2", effect: "[방패 돌진 강타] 해금 및 기절 시간 2배" },
            { part: "armor", name: "🥋 불굴의 성채 두정갑", icon: "assets/ui/items_sets/set_guardian_armor.png?v=2", effect: "체력 비례 방어력 최대 3배 폭증 + 도발 오라" },
            { part: "helmet", name: "🪖 아이기스 청룡 투구", icon: "assets/ui/items_sets/set_guardian_helmet.png?v=2", effect: "적 투사체 50% 확률로 2배 피해 반사" },
            { part: "core", name: "💎 대지의 용철 심장핵", icon: "assets/ui/items_sets/set_guardian_core.png?v=2", effect: "방어력 100% 공격 전환 & [아이기스 노바] 해금" }
        ]
    },
    "storm_wizard": {
        id: "storm_wizard",
        name: "⚡ 스톰 위저드",
        model: "이재성 (마도포병여단장)",
        sprite: "assets/agents/agent_male_energy_discharge.png?v=2",
        mainStat: "INT (마력)",
        color: "#c850ff",
        desc: "뇌전과 화염 폭격. 스킬 3회 시전마다 마력 동조망 과충전으로 범위와 피해 2배.",
        passive: "스킬 연속 사용 시 [마력 과충전] 스택 누적 (최대 5중첩 시 마나 소모 0).",
        ultimate: "⚡ [템페스트 아크 노바]",
        skills: [
            { id: "storm_1", name: "마력 동조망", type: "core", desc: "주변 마법사들과 마력 공명하여 스킬 범위 +40%", vfx: "assets/pixel_vfx/skills/vfx_storm_1.png?v=2", kind: "buff", target: "self", badge: "⚡ 마력 동조망 과충전", floatingText: "⚡ OVERCHARGE! MP COST 0", buffDesc: "마력 과충전: 스킬 마나 소모 0 & 마법 범위 +50%", logMsg: "성층권 마력 동조망과 공명하여 마력 과충전 상태에 진입! 마나 소모 없이 마법 폭풍을 전개합니다!" },
            { id: "storm_2", name: "체인 라이트닝", type: "dps", desc: "적 8기에게 연쇄 낙뢰를 튕기며 감전 유발", vfx: "assets/pixel_vfx/skills/vfx_storm_2.png?v=2", kind: "attack", target: "enemy", badge: "⚡ 체인 라이트닝", floatingText: "CHAIN LIGHTNING ×8!", buffDesc: "적 8기 연쇄 뇌격 및 감전 유발", logMsg: "고전압 푸른 벼락이 적 8기의 몸체를 연쇄적으로 튀며 전신을 감전시켰습니다!" },
            { id: "storm_3", name: "헬파이어 메테오", type: "dps", desc: "고열 마도 운석을 떨어뜨려 장판 지속 화염 피해", vfx: "assets/pixel_vfx/skills/vfx_storm_3.png?v=2", kind: "attack", target: "enemy", badge: "☄️ 헬파이어 메테오", floatingText: "METEOR BURST!", buffDesc: "고열 마도 운석 낙하 + 지면 화염 장판 지속 피해", logMsg: "하늘을 가르고 낙하한 거대한 화염 운석이 적진을 직격하여 불바다로 만들었습니다!" },
            { id: "storm_4", name: "점멸 & 마나실드", type: "utility", desc: "순간이동 후 마나를 소모해 받는 피해 80% 상쇄", vfx: "assets/pixel_vfx/skills/vfx_storm_4.png?v=2", kind: "blink_shield", target: "self", badge: "🔷 점멸 & 마나실드", floatingText: "🔷 MANA SHIELD +24,000 & BLINK", buffDesc: "후방 순간이동(회피율 +75%) + 마나 150% 마법 보호막 생성", logMsg: "공간을 굴절시켜 안전지대로 순간 점멸하고, 마력을 응축하여 24,000의 마나 보호막을 둘렀습니다!" },
            { id: "storm_5", name: "마도포 300문 일제사격", type: "elite", desc: "포병단의 마도포탄 30발이 전방을 융단폭격", vfx: "assets/pixel_vfx/skills/vfx_storm_5.png?v=2", kind: "attack", target: "enemy", badge: "🚀 마도포 300문", floatingText: "BARRAGE 30 SHELLS!", buffDesc: "전방 300문 마도포탄 30연속 융단폭격", logMsg: "마도포병여단의 300문 포신이 일제히 불을 뿜으며 전방을 초토화했습니다!" },
            { id: "storm_ult", name: "템페스트 아크 노바", type: "ult", desc: "성층권 뇌전 폭풍을 소환해 적 함대 및 지상군 증발", vfx: "assets/pixel_vfx/skills/vfx_storm_ult.png?v=2", kind: "cataclysm", target: "both", badge: "⚡ 템페스트 아크 노바", floatingText: "⚡ TEMPEST CATACLYSM!", buffDesc: "성층권 뇌전 폭풍 소환: 화면 내 적 전체 분자 증발", logMsg: "성층권에 거대한 뇌운을 소환하여 전장 전체에 메가볼트 벼락을 투하해 적들을 증발시켰습니다!" }
        ],
        setName: "제네바 마도왕",
        setParts: [
            { part: "ring", name: "💍 동조망 에테르 반지", icon: "assets/ui/items_sets/set_storm_wizard_ring.png?v=2", effect: "스킬 쿨타임 가속 +30%, 마법 관통력 +25%" },
            { part: "weapon", name: "🔮 아르카나의 뇌전 보주", icon: "assets/ui/items_sets/set_storm_wizard_weapon.png?v=2", effect: "[체인 라이트닝] 연쇄 횟수 16기로 증가" },
            { part: "armor", name: "🥋 성운의 대마도 로브", icon: "assets/ui/items_sets/set_storm_wizard_armor.png?v=2", effect: "피격 시 자동으로 광역 감전 충격파 발동" },
            { part: "helmet", name: "👑 대현자의 황금 서클릿", icon: "assets/ui/items_sets/set_storm_wizard_helmet.png?v=2", effect: "모든 마법 스킬에 치명타 확률 +30% 부여" },
            { part: "core", name: "💎 태초의 마력 폭풍핵", icon: "assets/ui/items_sets/set_storm_wizard_core.png?v=2", effect: "마나 소모 영구 0 & [템페스트 아크 노바] 해금" }
        ]
    },
    "sniper": {
        id: "sniper",
        name: "🎯 팬텀 스나이퍼",
        model: "박동석 (특수저격대장)",
        sprite: "assets/agents/agent_male_sensory_mutation.png?v=2",
        mainStat: "AGI (민첩)",
        color: "#ff7800",
        desc: "초장거리 마도 저격총과 공간 굴절 탄환. 단 한 발로 보스의 동력 코어를 꿰뚫는 헤드샷.",
        passive: "사거리 비례 치명타 확률 증가 (최대 100% 확정 치명타).",
        ultimate: "🎯 [50km 공간 굴절 저격]",
        skills: [
            { id: "snip_1", name: "매의 눈 (약점 포착)", type: "core", desc: "화면 내 보스 약점을 표시하여 방어력 100% 무시", vfx: "assets/pixel_vfx/skills/vfx_snip_1.png?v=2", kind: "buff", target: "self", badge: "🎯 약점 포착 (매의 눈)", floatingText: "🎯 WEAKPOINT MARKED!", buffDesc: "적 방어력 100% 무시 & 치명타 확률 +50%", logMsg: "초정밀 매의 눈으로 보스의 동력 코어 약점을 락온하여 방어력을 100% 무력화시켰습니다!" },
            { id: "snip_2", name: "대구경 관통 저격", type: "dps", desc: "일직선상 모든 적을 꿰뚫는 초고속 탄환 발사", vfx: "assets/pixel_vfx/skills/vfx_snip_2.png?v=2", kind: "projectile", target: "enemy", badge: "💥 대구경 관통 저격", floatingText: "PIERCE RAILGUN CRIT!", buffDesc: "마하 7 초고속 탄환 일직선 전원 관통", logMsg: "강두호제 마도총의 방아쇠를 당겨 음속의 7배로 날아간 탄환이 적들의 중심을 꿰뚫었습니다!" },
            { id: "snip_3", name: "폭발 크레모아 & 탄막", type: "dps", desc: "후방 도약하며 지뢰 매설 후 산탄 발사", vfx: "assets/pixel_vfx/skills/vfx_snip_3.png?v=2", kind: "attack", target: "enemy", badge: "💣 폭발 크레모아", floatingText: "CLAYMORE MINE BLAST!", buffDesc: "후방 도약 회피 + 고성능 지뢰 지면 매설 폭발", logMsg: "후방으로 도약하며 지뢰를 매설하여 접근하는 적들을 일제히 폭파시켰습니다!" },
            { id: "snip_4", name: "고스트 카모플라주", type: "utility", desc: "은신 상태로 진입하며 다음 1발 피해 300% 증폭", vfx: "assets/pixel_vfx/skills/vfx_snip_4.png?v=2", kind: "stealth", target: "self", badge: "🕶️ 고스트 카모플라주", floatingText: "🕶️ STEALTH ON & ATK +300%", buffDesc: "완전 은신 (타겟팅 면역, 회피율 +80%) + 다음 탄환 3배 피해", logMsg: "광학 미채 코트로 신체를 숨겨 완전 은신에 돌입했습니다! 다음 사격이 치명타로 적중합니다." },
            { id: "snip_5", name: "동력 코어 정밀 파괴", type: "elite", desc: "보스의 핵심 부품을 저격하여 5초간 무력화", vfx: "assets/pixel_vfx/skills/vfx_snip_5.png?v=2", kind: "cc", target: "enemy", badge: "⚡ 동력 코어 정밀 파괴", floatingText: "CORE BROKEN! STUN 4s", buffDesc: "보스 방어력 0화 + 4초간 완전 기능 정지 스턴", logMsg: "보스의 중추 동력 코어를 정밀 타격하여 4초간 완전 기능 마비 상태로 만들었습니다!" },
            { id: "snip_ult", name: "50km 공간 굴절 저격", type: "ult", desc: "차원을 왜곡해 50km 밖에서 쏘아 올린 즉사급 결전탄", vfx: "assets/pixel_vfx/skills/vfx_snip_ult.png?v=2", kind: "cataclysm", target: "enemy", badge: "🌌 50km 공간 굴절 저격", floatingText: "🌌 50km DIMENSIONAL BULLET!", buffDesc: "차원 왜곡 확정 즉사급 탄환 투사", logMsg: "50km 밖에서 쏘아 올린 차원 왜곡 탄환이 시공간을 가르고 보스의 심장에 박혔습니다!" }
        ],
        setName: "팬텀 호크아이",
        setParts: [
            { part: "ring", name: "💍 무음의 탄도 반지", icon: "assets/ui/items_sets/set_sniper_ring.png?v=2", effect: "치명타 확률 +35%, 치명타 피해 +80%" },
            { part: "weapon", name: "🔫 강두호제 대구경 마도총", icon: "assets/ui/items_sets/set_sniper_weapon.png?v=2", effect: "[대구경 관통 저격] 탄환 관통 손실 제거" },
            { part: "armor", name: "🥋 고스트 스텔스 코트", icon: "assets/ui/items_sets/set_sniper_armor.png?v=2", effect: "적과 거리 100px당 회피율 +5% (최대 50%)" },
            { part: "helmet", name: "🕶️ 사신의 외안경(사탕)", icon: "assets/ui/items_sets/set_sniper_helmet.png?v=2", effect: "보스 대상 최종 피해 +70% 및 사탕 버프" },
            { part: "core", name: "💎 아공간 굴절 코어", icon: "assets/ui/items_sets/set_sniper_core.png?v=2", effect: "공간 절단 탄환 & [50km 공간 굴절 저격] 해금" }
        ]
    },
    "priest": {
        id: "priest",
        name: "✨ 하이 프리스트",
        model: "오진석 (성역의무단장)",
        sprite: "assets/agents/agent_male_contamination_assimilation.png?v=2",
        mainStat: "WIS (신성력)",
        color: "#ffd000",
        desc: "상시 황금 성역 전개. 초과 회복량(Overheal)이 그대로 적을 찢는 성광 벼락으로 전환.",
        passive: "초당 체력 5% 자동 회복. 체력 100%일 때 회복량의 200%를 성광 고정 피해로 전환.",
        ultimate: "☀️ [대성역: 천벌의 빛기둥]",
        skills: [
            { id: "priest_1", name: "오버힐 심판 전환", type: "core", desc: "아군/자신 치유 시 초과된 치유량이 적에게 신성 낙뢰로 투사", vfx: "assets/pixel_vfx/skills/vfx_priest_1.png?v=2", kind: "buff", target: "self", badge: "⚖️ 오버힐 심판 전환", floatingText: "⚖️ OVERHEAL BURST ON!", buffDesc: "초과 치유량 100%가 신성 고정 피해 벼락으로 전환", logMsg: "신성 성역의 법칙을 발동하여 아군의 초과 회복량을 황금빛 심판 벼락으로 전환합니다!" },
            { id: "priest_2", name: "홀리 라이트닝", type: "dps", desc: "성스러운 번개로 아군은 치유하고 적군은 감전", vfx: "assets/pixel_vfx/skills/vfx_priest_2.png?v=2", kind: "heal", target: "both", badge: "✨ 홀리 라이트닝", floatingText: "💚 HEAL +12,000 & SMITE!", buffDesc: "아군/자신 체력 +12,000 회복 + 주변 적 신성 감전", logMsg: "성스러운 빛줄기가 영웅의 상처를 치유하고 적들에게는 성광 타격을 가했습니다!" },
            { id: "priest_3", name: "정화의 성염", type: "dps", desc: "신성한 불길로 상태이상 정화 및 적에게 지속 화상", vfx: "assets/pixel_vfx/skills/vfx_priest_3.png?v=2", kind: "heal", target: "both", badge: "🔥 정화의 성염", floatingText: "CLEANSE ALL & BURN!", buffDesc: "모든 상태이상/디버프 즉시 해제 + 적 지속 화상", logMsg: "신성한 불길로 영웅에게 걸린 모든 독과 저주를 정화하고 적들을 불태웠습니다!" },
            { id: "priest_4", name: "천상의 축복 방벽", type: "utility", desc: "전군 공격력 +50% 및 피해 40% 흡수 보호막", vfx: "assets/pixel_vfx/skills/vfx_priest_4.png?v=2", kind: "shield", target: "self", badge: "🪽 천상의 축복 방벽", floatingText: "✨ CELESTIAL SHIELD +25,000", buffDesc: "전군 공격력 +50% 버프 + 피해 40% 흡수 성광 방벽 생성", logMsg: "천사의 날개가 영웅을 감싸며 25,000의 성광 방벽과 전군 공격력 50% 버프를 부여했습니다!" },
            { id: "priest_5", name: "구원의 빛기둥", type: "elite", desc: "하늘에서 빛기둥이 내려와 전원 체력 즉시 100% 완치", vfx: "assets/pixel_vfx/skills/vfx_priest_5.png?v=2", kind: "heal", target: "self", badge: "☀️ 구원의 빛기둥", floatingText: "💚 FULL HEAL +50,000!", buffDesc: "하늘에서 빛기둥 강림: 체력 100% 즉시 완전 회복", logMsg: "하늘이 열리고 구원의 빛기둥이 쏟아져 내려와 빈사 상태의 체력을 100% 완치시켰습니다!" },
            { id: "priest_ult", name: "대성역: 천벌의 빛기둥", type: "ult", desc: "15초간 전원 불사(Immortal) + 초과회복 500% 성광 폭격", vfx: "assets/pixel_vfx/skills/vfx_priest_ult.png?v=2", kind: "invulnerable", target: "both", badge: "☀️ 대성역: 천벌의 빛기둥", floatingText: "☀️ IMMORTAL SANCTUARY 15s!", buffDesc: "15초간 전원 불사(Immortal) 성역 + 오버힐 500% 성광 융단폭격", logMsg: "대성역을 전개하여 15초간 절대 불사 상태를 유지하며 천벌의 신성 벼락으로 적진을 강타했습니다!" }
        ],
        setName: "대성역 사도",
        setParts: [
            { part: "ring", name: "💍 성녀의 눈물 반지", icon: "assets/ui/items_sets/set_priest_ring.png?v=2", effect: "신성력 +50%, 모든 치유량 및 성역 범위 +40%" },
            { part: "weapon", name: "🔱 구원의 백금 석장", icon: "assets/ui/items_sets/set_priest_weapon.png?v=2", effect: "[홀리 라이트닝] 투사체 4갈래로 분기" },
            { part: "armor", name: "🥋 심판관의 황금 성의", icon: "assets/ui/items_sets/set_priest_armor.png?v=2", effect: "성역 내 아군 피해 40% 감소 + 상태이상 면역" },
            { part: "helmet", name: "👑 광휘의 천사 면류관", icon: "assets/ui/items_sets/set_priest_helmet.png?v=2", effect: "사망 시 체력 100%로 1회 즉시 부활" },
            { part: "core", name: "💎 태초의 성흔 코어", icon: "assets/ui/items_sets/set_priest_core.png?v=2", effect: "오버힐 전환율 500%로 폭증 & [천벌의 빛기둥] 해금" }
        ]
    },
    "assassin": {
        id: "assassin",
        name: "🗡️ 섀도우 어쌔신",
        model: "카게미츠 (그림자 암살자)",
        sprite: "assets/agents/agent_male_blood_absorption.png?v=2",
        mainStat: "AGI (민첩)",
        color: "#a028ff",
        desc: "그림자 분신술과 맹독 출혈 중첩. 회피 성공 시 분신 3기가 모든 참격을 복제.",
        passive: "기본 회피율 +25%. 회피 성공 시 그림자 분신이 소환되어 참격 복제.",
        ultimate: "🌙 [차원 무음 참수]",
        skills: [
            { id: "as_1", name: "맹독과 출혈 각인", type: "core", desc: "타격 시마다 적에게 도트 피해 중첩 (최대 10스택)", vfx: "assets/pixel_vfx/skills/vfx_as_1.png?v=2", kind: "debuff", target: "enemy", badge: "🩸 맹독 & 출혈 각인", floatingText: "POISON & BLEED ×10!", buffDesc: "타격 시 도트 피해 중첩 (최대 10중첩)", logMsg: "적의 혈도에 맹독과 출혈을 각인하여 지속적으로 체력을 갉아먹게 만들었습니다!" },
            { id: "as_2", name: "그림자 습격", type: "dps", desc: "가장 먼 적의 배후로 순간이동하여 급소 찌르기", vfx: "assets/pixel_vfx/skills/vfx_as_2.png?v=2", kind: "attack", target: "enemy", badge: "🗡️ 그림자 습격", floatingText: "BACKSTAB CRIT!", buffDesc: "적 배후 순간이동 + 확정 치명타 급소 찌르기", logMsg: "그림자 속으로 녹아들어 적의 사각지대 배후로 이동해 심장을 찔렀습니다!" },
            { id: "as_3", name: "흑도 난무 (12연참)", type: "dps", desc: "무적 상태로 전방의 적들을 12번 연속 참수", vfx: "assets/pixel_vfx/skills/vfx_as_3.png?v=2", kind: "invulnerable", target: "enemy", badge: "⚔️ 흑도 난무 (12연참)", floatingText: "12-HIT BLADE DANCE!", buffDesc: "1.5초간 무적 상태 돌입 + 전방 12연속 참수", logMsg: "무적 상태로 그림자 참격을 연속 12회 작렬시켜 적을 난도질했습니다!" },
            { id: "as_4", name: "그림자 분신술", type: "utility", desc: "적 공격을 흘리고 본체의 공격을 복제하는 분신 2기 생성", vfx: "assets/pixel_vfx/skills/vfx_as_4.png?v=2", kind: "summon", target: "self", badge: "👥 그림자 분신술", floatingText: "SHADOW CLONE ×2 SUMMONED!", buffDesc: "회피율 +50% + 공격을 복제하는 분신 2기 도열", logMsg: "암살자의 그림자 분신 2기가 소환되어 군주 뒤에 집결하고 공격을 복제합니다!" },
            { id: "as_5", name: "혈독 폭살진", type: "elite", desc: "적들에게 누적된 모든 출혈과 독 스택을 일제히 폭발", vfx: "assets/pixel_vfx/skills/vfx_as_5.png?v=2", kind: "corpse_burst", target: "enemy", badge: "💥 혈독 폭살진", floatingText: "💥 BLOOD-TOXIN EXPLOSION!", buffDesc: "적들에게 누적된 모든 출혈/독 스택 일제히 폭파", logMsg: "적의 혈관 속에 잠복해 있던 모든 독과 혈기를 한순간에 기폭시켰습니다!" },
            { id: "as_ult", name: "차원 무음 참수", type: "ult", desc: "시간을 3초 정지시키고 100개의 그림자 환영으로 동시 참수", vfx: "assets/pixel_vfx/skills/vfx_as_ult.png?v=2", kind: "cataclysm", target: "both", badge: "🌑 차원 무음 참수", floatingText: "⏳ TIME STOP & 100 SLASHES!", buffDesc: "3초간 시간 정지 + 100개 환영 일제 참수", logMsg: "전장의 시간을 3초간 멈추고 100개의 그림자 환영이 적의 목을 일제히 베어 넘겼습니다!" }
        ],
        setName: "그림자 군주",
        setParts: [
            { part: "ring", name: "💍 칠흑의 암살 가락지", icon: "assets/ui/items_sets/set_assassin_ring.png?v=2", effect: "공격속도 +45%, 회피율 +20%" },
            { part: "weapon", name: "🗡️ 카게미츠의 요도 쌍검", icon: "assets/ui/items_sets/set_assassin_weapon.png?v=2", effect: "[흑도 난무] 타격 횟수 24타로 2배 증가" },
            { part: "armor", name: "🥋 차원 은신 야행복", icon: "assets/ui/items_sets/set_assassin_armor.png?v=2", effect: "적 방어력 60% 무시 + 치명타 시 쿨감 1초" },
            { part: "helmet", name: "🥷 무음의 복면 두건", icon: "assets/ui/items_sets/set_assassin_helmet.png?v=2", effect: "은신 중 가하는 모든 공격 확정 치명타" },
            { part: "core", name: "💎 그림자 여왕의 심장", icon: "assets/ui/items_sets/set_assassin_core.png?v=2", effect: "분신 3기 상시 유지 & [차원 무음 참수] 해금" }
        ]
    },
    "sword_master": {
        id: "sword_master",
        name: "🐉 소드마스터 (검왕)",
        model: "백도훈 (설악산 검왕)",
        sprite: "assets/agents/agent_male_fairy_magic.png?v=2",
        mainStat: "STR (무력)",
        color: "#32b4ff",
        desc: "화면을 가르는 청룡 검기와 발도술. 적의 공격을 일섬으로 패링하고 즉시 카운터.",
        passive: "기본 공격이 원거리 검기(오러 블레이드)로 발사됨. 치명타 피해 +50%.",
        ultimate: "🐉 [만검귀종: 진(眞) 청룡참]",
        skills: [
            { id: "sm_1", name: "검기 발현 (오러 블레이드)", type: "core", desc: "검의 리치와 관통력이 2배 증가하며 검기 방출", vfx: "assets/pixel_vfx/skills/vfx_sm_1.png?v=2", kind: "buff", target: "self", badge: "⚔️ 검기 발현 (오러 블레이드)", floatingText: "⚔️ AURA BLADE ON! REACH ×2", buffDesc: "검 사거리/관통력 2배 & 모든 평타가 검기로 방출", logMsg: "청룡의 기운을 검신에 둘러 푸른 검기를 발현시키고 리치를 2배로 확장했습니다!" },
            { id: "sm_2", name: "발도: 섬광일섬", type: "dps", desc: "빛의 속도로 화면 가로축 전체를 일도양단", vfx: "assets/pixel_vfx/skills/vfx_sm_2.png?v=2", kind: "attack", target: "enemy", badge: "⚡ 발도: 섬광일섬", floatingText: "FLASH SLASH 1-HIT!", buffDesc: "빛의 속도로 화면 가로축 전체 일도양단", logMsg: "검집에서 검을 뽑아내는 순간 화면 전체가 양단되며 섬광이 작렬했습니다!" },
            { id: "sm_3", name: "질풍노도 5연참", type: "dps", desc: "바람과 검기를 결합해 5연속 검풍 사격", vfx: "assets/pixel_vfx/skills/vfx_sm_3.png?v=2", kind: "attack", target: "enemy", badge: "🌪️ 질풍노도 5연참", floatingText: "5-COMBO SWORD WIND!", buffDesc: "바람을 가르는 5연속 푸른 검풍 발사", logMsg: "질풍처럼 빠른 속도로 5개의 검풍을 연속 발사하여 적진을 베어 넘겼습니다!" },
            { id: "sm_4", name: "심안 패링 (흘려내기)", type: "utility", desc: "적 공격 타이밍에 맞춰 피격 무효화 및 3배 반격", vfx: "assets/pixel_vfx/skills/vfx_sm_4.png?v=2", kind: "parry", target: "self", badge: "👁️ 심안 패링 (흘려내기)", floatingText: "👁️ PARRY! 300% COUNTER READY", buffDesc: "적 공격 피격 완전 무효화 + 쿨타임 리셋 + 3배 즉시 반격", logMsg: "심안으로 적 공격의 궤적을 읽고 칼등으로 완벽히 흘려내어 무효화했습니다!" },
            { id: "sm_5", name: "청룡참 (Blue Dragon)", type: "elite", desc: "푸른 용 형상의 거대 검기로 전방 산맥 파괴", vfx: "assets/pixel_vfx/skills/vfx_sm_5.png?v=2", kind: "attack", target: "enemy", badge: "🐉 청룡참 (Blue Dragon)", floatingText: "🐉 BLUE DRAGON STRIKE!", buffDesc: "푸른 용 형상의 거대 검기 전방 방출", logMsg: "백도훈의 청룡 신검에서 거대한 푸른 용이 솟구쳐 전방을 분쇄했습니다!" },
            { id: "sm_ult", name: "만검귀종: 진(眞) 청룡참", type: "ult", desc: "하늘에서 천 개의 신검이 쏟아진 후 거대한 청룡이 전장 폭쇄", vfx: "assets/pixel_vfx/skills/vfx_sm_ult.png?v=2", kind: "cataclysm", target: "both", badge: "🐉 만검귀종: 진 청룡참", floatingText: "🐉 10,000 SWORDS CATACLYSM!", buffDesc: "천 개의 신검 하늘에서 비처럼 낙하 + 대지 폭쇄", logMsg: "하늘에서 천 개의 신검이 쏟아져 내린 후 거대한 청룡이 전장을 뒤흔들었습니다!" }
        ],
        setName: "설악 청룡검왕",
        setParts: [
            { part: "ring", name: "💍 검선의 매듭 반지", icon: "assets/ui/items_sets/set_sword_master_ring.png?v=2", effect: "물리 공격력 +45%, 검기 크기 +50%" },
            { part: "weapon", name: "🗡️ 백도훈의 청룡 신검", icon: "assets/ui/items_sets/set_sword_master_weapon.png?v=2", effect: "[청룡참] 검기가 3갈래로 분기되어 폭발" },
            { part: "armor", name: "🥋 설악 운무 도포", icon: "assets/ui/items_sets/set_sword_master_armor.png?v=2", effect: "이동 중 적의 모든 원거리 공격 자동 튕겨내기" },
            { part: "helmet", name: "👑 검왕의 백발 관모", icon: "assets/ui/items_sets/set_sword_master_helmet.png?v=2", effect: "치명타 적중 시 [청룡의 포효]로 주변 기절" },
            { part: "core", name: "💎 검기(劍氣)의 극의 단전", icon: "assets/ui/items_sets/set_sword_master_core.png?v=2", effect: "모든 공격에 검기 부여 & [만검귀종] 해금" }
        ]
    },
    "death_knight": {
        id: "death_knight",
        name: "⚔️ 데스나이트",
        model: "듀라한 아서 (제1군단장)",
        sprite: "assets/agents/agent_male_berserk_frenzy.png?v=2",
        mainStat: "STR (무력)",
        color: "#ff2850",
        desc: "흑염 대검과 혈기 흡수. 체력을 소모해 폭발적인 공격력을 얻고 적을 베어 피를 회복.",
        passive: "모든 피해의 25%를 체력으로 흡혈. 체력이 낮아질수록 흡혈량 2배 증가.",
        ultimate: "⚔️ [아발론의 흑염 단두대]",
        skills: [
            { id: "dk_1", name: "피의 갈증", type: "core", desc: "체력 흡수율 +20% 및 흡혈 시 공격력 10초간 누적", vfx: "assets/pixel_vfx/skills/vfx_dk_1.png?v=2", kind: "buff", target: "self", badge: "🩸 피의 갈증", floatingText: "🩸 LIFESTEAL +35% ACTIVE", buffDesc: "피해의 35% 체력 흡수 & 체력 낮을수록 공격력 증폭", logMsg: "망자의 피의 갈증을 활성화하여 흡혈 능력을 극대화하고 공격력을 축적했습니다!" },
            { id: "dk_2", name: "흑염 대검 베기", type: "dps", desc: "체력 5%를 소모해 300% 위력의 흑염 참격 발사", vfx: "assets/pixel_vfx/skills/vfx_dk_2.png?v=2", kind: "attack", target: "enemy", badge: "🔥 흑염 대검 베기", floatingText: "HP SACRIFICE × 300% ATK!", buffDesc: "체력 5% 소모 ➔ 300% 흑염 참격 방출", logMsg: "자신의 혈기를 바쳐 대검에 불을 붙이고 흑염의 참격을 날렸습니다!" },
            { id: "dk_3", name: "죽음의 손아귀", type: "dps", desc: "칠흑 손길을 뻗어 원거리 적 3기를 전방으로 강제 견인", vfx: "assets/pixel_vfx/skills/vfx_dk_3.png?v=2", kind: "cc", target: "enemy", badge: "🖐️ 죽음의 손아귀", floatingText: "PULL 3 ENEMIES & BIND!", buffDesc: "원거리 적 3기 전방으로 강제 견인 + 2초 속박", logMsg: "어둠의 손길을 뻗어 도망치던 원거리 적들을 영웅 코앞으로 끌고 왔습니다!" },
            { id: "dk_4", name: "망자의 갑주", type: "utility", desc: "받는 피해의 50%를 10초에 걸쳐 나누어 받도록 지연", vfx: "assets/pixel_vfx/skills/vfx_dk_4.png?v=2", kind: "shield", target: "self", badge: "🛡️ 망자의 갑주", floatingText: "🛡️ DAMAGE DELAY 50% ABSORB", buffDesc: "받는 피해 50% 즉시 경감 및 10초 분할 지연", logMsg: "어둠의 판금갑이 받는 피해의 절반을 흡수하여 사망의 위기를 넘겼습니다!" },
            { id: "dk_5", name: "단두대 처형 (길로틴)", type: "elite", desc: "체력 35% 이하 적에게 거대 단두대 칼날 낙하 (즉사급)", vfx: "assets/pixel_vfx/skills/vfx_dk_5.png?v=2", kind: "attack", target: "enemy", badge: "⚔️ 단두대 처형", floatingText: "💀 EXECUTION GUILLOTINE!", buffDesc: "체력 35% 이하 적에게 거대 단두대 즉사급 낙하", logMsg: "하늘에서 칠흑의 단두대 칼날이 떨어져 적의 숨통을 단번에 끊었습니다!" },
            { id: "dk_ult", name: "아발론의 흑염 단두대", type: "ult", desc: "듀라한 기사단이 돌격하며 화면 전체를 흑염으로 양단", vfx: "assets/pixel_vfx/skills/vfx_dk_ult.png?v=2", kind: "cataclysm", target: "both", badge: "⚔️ 아발론의 흑염 단두대", floatingText: "⚔️ DULLAHAN LEGION CHARGE!", buffDesc: "듀라한 기사단 전원 소환 돌격 + 전장 흑염 양단", logMsg: "아발론의 듀라한 기사단이 지옥의 불꽃을 휘감고 돌격하여 전장을 갈라놓았습니다!" }
        ],
        setName: "아발론 단두대",
        setParts: [
            { part: "ring", name: "💍 망자의 서약 반지", icon: "assets/ui/items_sets/set_death_knight_ring.png?v=2", effect: "흡혈률 +15%, 최대 체력 +40%" },
            { part: "weapon", name: "🗡️ 아서의 흑염 대검", icon: "assets/ui/items_sets/set_death_knight_weapon.png?v=2", effect: "체력 소모 스킬 피해량 2.5배로 증폭" },
            { part: "armor", name: "🥋 아발론 칠흑 판금갑", icon: "assets/ui/items_sets/set_death_knight_armor.png?v=2", effect: "적 처치 시 최대 체력의 10% 즉시 회복" },
            { part: "helmet", name: "🪖 타오르는 듀라한 투구", icon: "assets/ui/items_sets/set_death_knight_helmet.png?v=2", effect: "주변 적에게 [공포] 유발하여 공격력 -35%" },
            { part: "core", name: "💎 불멸 기사의 어둠 성배", icon: "assets/ui/items_sets/set_death_knight_core.png?v=2", effect: "사망 방지 5초 불사 & [아발론 흑염 단두대] 해금" }
        ]
    },
    "martial_king": {
        id: "martial_king",
        name: "👊 권왕 무투가",
        model: "진무극 (곤륜 권왕)",
        sprite: "assets/agents/agent_male_kinetic_overload.png?v=2",
        mainStat: "STR (무력)",
        color: "#ffb432",
        desc: "맨주먹 투기와 금강불괴 강철 육체. 3타마다 터지는 파쇄 충격파로 보스 슈퍼아머 분쇄.",
        passive: "피격 경직 완전 면역. 3타마다 방어력을 무시하는 투기 충격파 폭발.",
        ultimate: "👊 [일격필살: 태산파쇄격]",
        skills: [
            { id: "mk_1", name: "금강불괴", type: "core", desc: "기본 방어력 +50% 및 보스 공격에 넉백되지 않음", vfx: "assets/pixel_vfx/skills/vfx_mk_1.png?v=2", kind: "buff", target: "self", badge: "🥋 금강불괴 (강철 피부)", floatingText: "🥋 VAJRA BODY! DEF +100%", buffDesc: "방어력 +100% & 피격 경직 및 넉백 완전 면역", logMsg: "곤륜의 금강불괴를 시전하여 전신을 황동빛 강철로 만들어 경직 면역 상태가 되었습니다!" },
            { id: "mk_2", name: "파쇄권 (붕권)", type: "dps", desc: "단 한 번의 정권 지르기로 적 방어력을 뚫고 후방 충격파", vfx: "assets/pixel_vfx/skills/vfx_mk_2.png?v=2", kind: "attack", target: "enemy", badge: "👊 파쇄권 (붕권)", floatingText: "ARMOR PIERCE PUNCH!", buffDesc: "적 방어력 100% 관통 후방 관통 충격파", logMsg: "정권 지르기 한 방으로 적의 방어구를 깨부수고 후방까지 궤멸시켰습니다!" },
            { id: "mk_3", name: "폭풍 연환격", type: "dps", desc: "초당 15회의 폭풍 같은 주먹 난타로 보스 기절", vfx: "assets/pixel_vfx/skills/vfx_mk_3.png?v=2", kind: "cc", target: "enemy", badge: "🌪️ 폭풍 연환격", floatingText: "15-HIT STUN FLURRY!", buffDesc: "초당 15타 주먹 난타 + 슈퍼아머 강제 파괴", logMsg: "보이지 않는 속도로 주먹을 쏟아부어 보스의 슈퍼아머를 박살 냈습니다!" },
            { id: "mk_4", name: "순보 & 내공 폭발", type: "utility", desc: "적진 한가운데로 순간 돌진 후 기공파로 전원 넉백", vfx: "assets/pixel_vfx/skills/vfx_mk_4.png?v=2", kind: "buff", target: "both", badge: "💨 순보 & 내공 폭발", floatingText: "💨 FLASH STEP & ATK SPD +50%", buffDesc: "적진 순간 돌진 + 주변 넉백 + 공격속도 +50%", logMsg: "순보로 적진 한가운데로 침투하여 내공을 폭발시키고 공속을 대폭 끌어올렸습니다!" },
            { id: "mk_5", name: "패왕 열파참", type: "elite", desc: "양손 주먹으로 바닥을 쳐 용암 기둥을 솟구치게 함", vfx: "assets/pixel_vfx/skills/vfx_mk_5.png?v=2", kind: "attack", target: "enemy", badge: "💥 패왕 열파참", floatingText: "LAVA ERUPTION WAVE!", buffDesc: "양 주먹으로 지면을 강타해 거대 기공 용암파 분출", logMsg: "지면에 주먹을 박아 넣어 거대한 투기 기둥을 솟구치게 했습니다!" },
            { id: "mk_ult", name: "일격필살: 태산파쇄격", type: "ult", desc: "우주적 투기를 주먹에 모아 행성급 펀치로 전장 함몰", vfx: "assets/pixel_vfx/skills/vfx_mk_ult.png?v=2", kind: "cataclysm", target: "both", badge: "👊 일격필살: 태산파쇄격", floatingText: "👊 COSMIC TAISHAN SMASH!", buffDesc: "우주적 투기 응축 펀치로 전장 행성급 함몰", logMsg: "우주적 투기를 맨주먹에 그러모아 전장 전체를 함몰시키는 펀치를 작렬했습니다!" }
        ],
        setName: "곤륜 무신(武神)",
        setParts: [
            { part: "ring", name: "💍 금강 투기 반지", icon: "assets/ui/items_sets/set_martial_king_ring.png?v=2", effect: "공격속도 +50%, 맨손 공격력 +100%" },
            { part: "weapon", name: "🥊 보리스의 아다만티움 너클", icon: "assets/ui/items_sets/set_martial_king_weapon.png?v=2", effect: "[파쇄권] 충격파 크기 3배로 증가" },
            { part: "armor", name: "🥋 무신의 호포 무도복", icon: "assets/ui/items_sets/set_martial_king_armor.png?v=2", effect: "모든 군중제어 및 기절 시간 80% 단축" },
            { part: "helmet", name: "👑 투신의 붉은 머리띠", icon: "assets/ui/items_sets/set_martial_king_helmet.png?v=2", effect: "연타 횟수 비례 치명타 피해 최대 +150%" },
            { part: "core", name: "💎 내공의 등화 코어", icon: "assets/ui/items_sets/set_martial_king_core.png?v=2", effect: "슈퍼아머 상시 파괴 & [태산파쇄격] 해금" }
        ]
    },
    "psionic_tactician": {
        id: "psionic_tactician",
        name: "🔮 사이오닉 마도사",
        model: "벨록 (화성인 이단참모)",
        sprite: "assets/agents/agent_male_hitech_engineering.png?v=2",
        mainStat: "INT (마력)",
        color: "#b450ff",
        desc: "중력장 왜곡과 외계 드론 포탑 전개. 적 몬스터를 해킹(세뇌)하여 아군 편으로 교란.",
        passive: "적 공격 패턴 연산으로 회피율 +20%. 적 세뇌 시 아군으로 자폭.",
        ultimate: "🛸 [궤도 모함 해킹: 플라즈마 폭격]",
        skills: [
            { id: "psi_1", name: "전술 연산 알고리즘", type: "core", desc: "아군 전체 스킬 명중률 +30% 및 쿨타임 가속", vfx: "assets/pixel_vfx/skills/vfx_psi_1.png?v=2", kind: "buff", target: "self", badge: "🧠 전술 연산 알고리즘", floatingText: "🧠 CDR +35% & EVA +30%", buffDesc: "스킬 쿨타임 가속 +35% & 아군 전체 회피율 +30%", logMsg: "화성 전술 인공지능을 활성화하여 적 공격 패턴을 연산하고 회피율을 극대화했습니다!" },
            { id: "psi_2", name: "중력장 압축 (블랙홀)", type: "dps", desc: "특정 좌표로 적들을 강력하게 빨아들이는 중력 구체", vfx: "assets/pixel_vfx/skills/vfx_psi_2.png?v=2", kind: "cc", target: "enemy", badge: "🕳️ 중력장 압축 (블랙홀)", floatingText: "BLACK HOLE PULL!", buffDesc: "적들을 한 점으로 강력하게 빨아들이는 중력 구체", logMsg: "시공간을 왜곡하는 미니 블랙홀을 생성하여 흩어진 적들을 한곳으로 흡입했습니다!" },
            { id: "psi_3", name: "음양 오행 부적진", type: "dps", desc: "5개 속성 부적을 회전시켜 연속 원소 폭발", vfx: "assets/pixel_vfx/skills/vfx_psi_3.png?v=2", kind: "attack", target: "enemy", badge: "📜 음양 오행 부적진", floatingText: "5-ELEMENT BURST!", buffDesc: "5대 속성 부적 회전 후 원소 연쇄 폭발", logMsg: "오행 부적을 회전시켜 5가지 원소의 연쇄 폭발로 적들을 타격했습니다!" },
            { id: "psi_4", name: "사이오닉 해킹 (세뇌)", type: "utility", desc: "적 괴수 2기를 세뇌하여 8초간 아군으로 싸우게 함", vfx: "assets/pixel_vfx/skills/vfx_psi_4.png?v=2", kind: "cc", target: "enemy", badge: "👾 사이오닉 해킹 (세뇌)", floatingText: "👾 2 ENEMIES BRAINWASHED!", buffDesc: "적 2기를 아군 편으로 8초간 해킹 세뇌", logMsg: "외계 신경망을 해킹하여 적 2기를 아군으로 변절시켜 자폭하도록 유도했습니다!" },
            { id: "psi_5", name: "외계 강습 드론 호출", type: "elite", desc: "고출력 플라즈마 레이저 포탑 4기 전개", vfx: "assets/pixel_vfx/skills/vfx_psi_5.png?v=2", kind: "summon", target: "self", badge: "🛸 외계 강습 드론", floatingText: "DRONES DEPLOYED!", buffDesc: "고출력 플라즈마 레이저 포탑 4기 전개", logMsg: "반중력 드론 포탑 4기를 호출하여 전방에 지속 레이저 탄막을 형성했습니다!" },
            { id: "psi_ult", name: "궤도 모함 해킹: 플라즈마 폭격", type: "ult", desc: "적 강습 모함 주포를 역해킹하여 성층권에서 플라즈마 융단폭격", vfx: "assets/pixel_vfx/skills/vfx_psi_ult.png?v=2", kind: "cataclysm", target: "enemy", badge: "🛸 궤도 모함 해킹: 플라즈마 폭격", floatingText: "🛸 MOTHERSHIP PLASMA CANNON!", buffDesc: "성층권 적 기함 주포 역해킹 ➔ 플라즈마 폭격", logMsg: "성층권 외계 모함의 주포 제어권을 탈취하여 지상 적진에 플라즈마 폭격을 쏟았습니다!" }
        ],
        setName: "화성 이단참모",
        setParts: [
            { part: "ring", name: "💍 텔레파시 증폭 링", icon: "assets/ui/items_sets/set_psionic_tactician_ring.png?v=2", effect: "마나 회복 +40%, 세뇌 지속시간 2배" },
            { part: "weapon", name: "📡 벨록의 홀로그램 제어봉", icon: "assets/ui/items_sets/set_psionic_tactician_weapon.png?v=2", effect: "[외계 강습 드론] 레이저 관통 횟수 3회" },
            { part: "armor", name: "🥋 반중력 연구원 로브", icon: "assets/ui/items_sets/set_psionic_tactician_armor.png?v=2", effect: "지상 함정 및 낙하 공격 완전 면역" },
            { part: "helmet", name: "👓 사이오닉 연산 고글", icon: "assets/ui/items_sets/set_psionic_tactician_helmet.png?v=2", effect: "적의 마법 저항력 50% 강제 차감" },
            { part: "core", name: "💎 화성 제국의 금기 코어", icon: "assets/ui/items_sets/set_psionic_tactician_core.png?v=2", effect: "세뇌 가능 개체수 +3 & [궤도 플라즈마 폭격] 해금" }
        ]
    },
    "berserker": {
        id: "berserker",
        name: "🪓 그래비티 버서커",
        model: "볼가르 (외계 대장군)",
        sprite: "assets/agents/agent_male_thermal_control.png?v=2",
        mainStat: "STR (무력)",
        color: "#ff1e1e",
        desc: "쌍수 중력 도끼 휠윈드. 잃은 체력 1%당 공격력/공속 3% 폭증 및 5초 불사.",
        passive: "체력이 30% 이하로 내려가면 즉시 [광폭화] 발동 (공격속도 2배, 공격력 3배).",
        ultimate: "🪓 [라그나로크: 중력 붕괴]",
        skills: [
            { id: "ber_1", name: "광전사의 피", type: "core", desc: "잃은 체력에 비례하여 최대 공격력 +300% 폭증", vfx: "assets/pixel_vfx/skills/vfx_ber_1.png?v=2", kind: "buff", target: "self", badge: "🔥 광전사의 피", floatingText: "🔥 BERSERK! ATK +250% SPD +40%", buffDesc: "잃은 체력에 비례해 공격력 최대 +300% 폭증", logMsg: "혈액이 끓어오르며 상처를 입을수록 괴물 같은 공격력을 발휘하는 광폭화에 돌입했습니다!" },
            { id: "ber_2", name: "중력 도끼 휠윈드", type: "dps", desc: "이동하면서 360도 회전 참격으로 주변 적 분쇄", vfx: "assets/pixel_vfx/skills/vfx_ber_2.png?v=2", kind: "attack", target: "enemy", badge: "🪓 중력 도끼 휠윈드", floatingText: "WHIRLWIND 360° SPIN!", buffDesc: "이동하며 360도 연속 회전 참격", logMsg: "중력 쌍도끼를 휘두르며 폭풍처럼 회전하여 주변 적들을 토막 냈습니다!" },
            { id: "ber_3", name: "사막의 혈풍참", type: "dps", desc: "황금 곡도를 휘둘러 모래폭풍과 거대한 출혈 검풍 발사", vfx: "assets/pixel_vfx/skills/vfx_ber_3.png?v=2", kind: "attack", target: "enemy", badge: "🌪️ 사막의 혈풍참", floatingText: "BLOOD SANDSTORM SLASH!", buffDesc: "황금 곡도로 거대한 모래폭풍과 출혈 검풍 발사", logMsg: "사막의 모래폭풍과 피의 검기를 결합해 전방으로 발사했습니다!" },
            { id: "ber_4", name: "불사 광란 (언다잉)", type: "utility", desc: "5초간 체력이 1 이하로 떨어지지 않는 불사 상태 돌입", vfx: "assets/pixel_vfx/skills/vfx_ber_4.png?v=2", kind: "invulnerable", target: "self", badge: "⚡ 불사 광란 (언다잉)", floatingText: "⚡ 5s IMMORTAL RAGE!", buffDesc: "5초간 체력이 1 이하로 내려가지 않는 완전 불사 상태", logMsg: "치명상을 거부하고 5초간 어떠한 공격에도 죽지 않는 불사의 광란에 들어섰습니다!" },
            { id: "ber_5", name: "거인 학살자의 도약", type: "elite", desc: "공중으로 높이 뛰어올라 대지를 찍어 광역 지진 분쇄", vfx: "assets/pixel_vfx/skills/vfx_ber_5.png?v=2", kind: "attack", target: "enemy", badge: "🪓 거인 학살자의 도약", floatingText: "GIANT LEAP SLAM!", buffDesc: "공중 높이 도약 후 중력 도끼로 대지 찍기", logMsg: "하늘 높이 도약한 뒤 체중을 실어 대지를 내리찍어 지반을 갈라놓았습니다!" },
            { id: "ber_ult", name: "라그나로크: 중력 붕괴", type: "ult", desc: "체력을 1로 전환하고 전장 전체의 중력을 붕괴시켜 1000% 광역 파멸", vfx: "assets/pixel_vfx/skills/vfx_ber_ult.png?v=2", kind: "cataclysm", target: "both", badge: "🌌 라그나로크: 중력 붕괴", floatingText: "🌌 RAGNAROK 1000% COLLAPSE!", buffDesc: "체력을 1로 깎고 전장 전체 중력 붕괴 1000% 광역 파멸", logMsg: "자신의 생명력을 불태워 중력장을 붕괴시키고 전장에 종말의 충격파를 일으켰습니다!" }
        ],
        setName: "사막의 중력왕",
        setParts: [
            { part: "ring", name: "💍 피의 갈망 반지", icon: "assets/ui/items_sets/set_berserker_ring.png?v=2", effect: "물리 피해량 +40%, 잃은 체력 비례 공속+" },
            { part: "weapon", name: "🪓 볼가르의 중력 쌍도끼", icon: "assets/ui/items_sets/set_berserker_weapon.png?v=2", effect: "[휠윈드] 회전 속도 2배 및 범위 1.5배" },
            { part: "armor", name: "🥋 사막왕의 황금 견갑", icon: "assets/ui/items_sets/set_berserker_armor.png?v=2", effect: "광폭화 중 피격 대미지 50% 추가 감소" },
            { part: "helmet", name: "🪖 광전사의 뿔투구", icon: "assets/ui/items_sets/set_berserker_helmet.png?v=2", effect: "적 처치 시 불사 지속시간 1초씩 연장" },
            { part: "core", name: "💎 폭주하는 베히모스 핵", icon: "assets/ui/items_sets/set_berserker_core.png?v=2", effect: "불사 지속시간 +5초 & [라그나로크] 해금" }
        ]
    },
    "cryo_empress": {
        id: "cryo_empress",
        name: "❄️ 크라이오 엠프레스",
        model: "나탈리야 로마노바 (빙여제)",
        sprite: "assets/agents/agent_male_melt_control.png?v=2",
        mainStat: "INT (마력)",
        color: "#64dcff",
        desc: "절대영도 냉기 마법의 극치. 적을 완전 빙결시키고 얼어붙은 적에게 3배의 파쇄 피해.",
        passive: "모든 공격에 [동상] 중첩. 완전 빙결 상태의 적에게 가하는 피해 3배.",
        ultimate: "❄️ [절대영도: 다이아몬드 더스트]",
        skills: [
            { id: "cryo_1", name: "절대영도의 한기", type: "core", desc: "주변 적들의 공격속도와 이동속도를 40% 강제 둔화", vfx: "assets/pixel_vfx/skills/vfx_cryo_1.png?v=2", kind: "debuff", target: "enemy", badge: "❄️ 절대영도의 한기", floatingText: "❄️ ENEMY SLOW -50% & CHILL", buffDesc: "주변 적들의 공격/이동속도 50% 강제 둔화 오라", logMsg: "절대영도의 한기를 뿜어내어 적들의 관절과 혈관을 얼어붙게 만들었습니다!" },
            { id: "cryo_2", name: "아이스 스피어 개틀링", type: "dps", desc: "초고속 고드름 창 20발을 기관총처럼 연사", vfx: "assets/pixel_vfx/skills/vfx_cryo_2.png?v=2", kind: "projectile", target: "enemy", badge: "🧊 아이스 스피어 개틀링", floatingText: "ICE GATLING 20-SHOTS!", buffDesc: "초고속 고드름 탄환 20발 연속 기관총 사격", logMsg: "영구동토의 고드름 창 20발을 기관총처럼 연사하여 적들을 꿰뚫었습니다!" },
            { id: "cryo_3", name: "프로스트 노바 & 빙벽", type: "dps", desc: "주변 적들을 즉시 얼리고 얼음 성벽으로 길 차단", vfx: "assets/pixel_vfx/skills/vfx_cryo_3.png?v=2", kind: "cc", target: "enemy", badge: "🧊 프로스트 노바 & 빙벽", floatingText: "🧊 ALL ENEMIES FROZEN 3s!", buffDesc: "주변 모든 적 3초간 완전 빙결 + 얼음 성벽 차단", logMsg: "발밑에서 얼음 결정을 폭발시켜 반경 내 모든 적을 3초간 영구 동결시켰습니다!" },
            { id: "cryo_4", name: "얼음 여왕의 보석화", type: "utility", desc: "3초간 얼음 결정체로 변신하여 완전 무적 및 마나 회복", vfx: "assets/pixel_vfx/skills/vfx_cryo_4.png?v=2", kind: "invulnerable", target: "self", badge: "💎 얼음 여왕의 보석화", floatingText: "💎 ICE JEWEL 3s INVINCIBLE & MP HEAL", buffDesc: "3초간 완전 무적 얼음 결정체 변신 + 초당 마나 30% 회복", logMsg: "신체를 순수한 빙정 보석으로 결정화하여 모든 피해를 무효화하고 마력을 채웠습니다!" },
            { id: "cryo_5", name: "글래시어 폴 (빙하 낙하)", type: "elite", desc: "거대한 빙하 덩어리를 소환하여 적들을 압살", vfx: "assets/pixel_vfx/skills/vfx_cryo_5.png?v=2", kind: "attack", target: "enemy", badge: "🏔️ 글래시어 폴 (빙하 낙하)", floatingText: "GLACIER CRUSH!", buffDesc: "거대한 빙하 덩어리를 소환해 적들을 압살", logMsg: "성층권에서 거대한 만년설 빙하를 소환하여 적들을 짓눌렀습니다!" },
            { id: "cryo_ult", name: "절대영도: 다이아몬드 더스트", type: "ult", desc: "전장 전체를 영구 동결 후 유리처럼 산산조각 분쇄", vfx: "assets/pixel_vfx/skills/vfx_cryo_ult.png?v=2", kind: "cataclysm", target: "both", badge: "❄️ 절대영도: 다이아몬드 더스트", floatingText: "❄️ DIAMOND DUST SHATTER!", buffDesc: "전장 전체를 영구 동결 후 유리처럼 산산조각 분쇄", logMsg: "다이아몬드 더스트를 휘몰아쳐 전장을 순식간에 얼리고 유리처럼 산산조각 냈습니다!" }
        ],
        setName: "시베리아 빙여제",
        setParts: [
            { part: "ring", name: "💍 영구동토의 얼음반지", icon: "assets/ui/items_sets/set_cryo_empress_ring.png?v=2", effect: "냉기 피해량 +50%, 동상 지속시간 2배" },
            { part: "weapon", name: "🦯 나탈리야의 빙정 홀", icon: "assets/ui/items_sets/set_cryo_empress_weapon.png?v=2", effect: "[아이스 스피어] 탄환 수 40발로 2배 증가" },
            { part: "armor", name: "🥋 설원 황실의 백색 코트", icon: "assets/ui/items_sets/set_cryo_empress_armor.png?v=2", effect: "근접 공격을 가해온 적을 100% 확률로 2초 동결" },
            { part: "helmet", name: "👑 빙여제의 수정 티아라", icon: "assets/ui/items_sets/set_cryo_empress_helmet.png?v=2", effect: "얼어붙은 적 타격 시 100% 확정 치명타" },
            { part: "core", name: "💎 히말라야 빙룡의 용옥", icon: "assets/ui/items_sets/set_cryo_empress_core.png?v=2", effect: "빙결 면역 적 강제 동결 & [다이아몬드 더스트] 해금" }
        ]
    }
};

// 2. 특성(Traits) 10종 데이터
const TRAITS_DATA = {
    "trait_mana_flow":   { name: "🌀 마력 호흡", baseVal: 10, unit: "%", desc: "마나 회복 속도 증가" },
    "trait_iron_body":   { name: "🛡️ 육체의 기억", baseVal: 12, unit: "%", desc: "기본 방어력 및 최대 체력 증가" },
    "trait_hawk_eye":    { name: "🦅 매의 눈", baseVal: 6, unit: "%", desc: "치명타 확률 및 치명타 피해 증가" },
    "trait_undead_cmd":  { name: "💀 사령의 권능", baseVal: 14, unit: "%", desc: "소환수 전체 공격력 및 방어력 증가" },
    "trait_frost_heart": { name: "❄️ 극한의 심장", baseVal: 12, unit: "%", desc: "냉기 및 마법 속성 피해량 증가" },
    "trait_blood_vamp":  { name: "🩸 포식자의 본능", baseVal: 4, unit: "%", desc: "적 처치 시 체력과 마나 회복" },
    "trait_thorn_armor": { name: "🦔 불굴의 가시", baseVal: 20, unit: "%", desc: "피격 시 방어력 비례 반사 피해" },
    "trait_shadow_step": { name: "🌙 잔상 보법", baseVal: 8, unit: "%", desc: "공격속도 및 이동속도 증가" },
    "trait_holy_grace":  { name: "✨ 성역의 은총", baseVal: 10, unit: "%", desc: "모든 회복량 및 보호막 효율 증가" },
    "trait_boss_slayer": { name: "⚔️ 학살자의 투기", baseVal: 10, unit: "%", desc: "네임드 및 보스 대상 피해량 증가" }
};

// 3. 재능(Talents) 10종 데이터
const TALENTS_DATA = {
    "talent_merchant":     { name: "💰 거상의 안목", baseVal: 10, unit: "%", desc: "마력석(골드) 획득량 및 상점 할인" },
    "talent_blacksmith":   { name: "🔨 을지로의 축복", baseVal: 8, unit: "%", desc: "착용 장비의 기본 스탯 효율 증가" },
    "talent_cooldown":     { name: "⏱️ 초월적 연산", baseVal: 6, unit: "%", desc: "모든 스킬 쿨타임 가속" },
    "talent_relic_finder": { name: "💎 이단자의 직감", baseVal: 10, unit: "%", desc: "세트 및 고유 아이템 드랍률 증가" },
    "talent_exp_surge":    { name: "📖 전생의 깨달음", baseVal: 15, unit: "%", desc: "전투 경험치 획득량 증가" },
    "talent_friend_bond":  { name: "🍕 다섯의 맹세", baseVal: 12, unit: "%", desc: "친구 지원 스킬 호출 위력 증가" },
    "talent_double_cast":  { name: "⚡ 이중 영창", baseVal: 5, unit: "%", desc: "스킬 사용 시 쿨 없이 2회 연속 발동 확률" },
    "talent_gate_breaker": { name: "🚪 차원문 파쇄자", baseVal: 4, unit: "%", desc: "웨이브 시작 시 적 전체 체력 삭감" },
    "talent_soul_harvest": { name: "👻 영혼 수확자", baseVal: 2, unit: "%", desc: "적 처치 시 영구 공격력 누적 보너스" },
    "talent_immortal_will":{ name: "🔥 불굴의 의지", baseVal: 16, unit: "%", desc: "체력 30% 이하 시 최종 피해량 증폭" }
};

// 4. 빌드 체인저 고유(Unique) 아이템 36종
const UNIQUE_ITEMS_DATA = [
    { id: 1, name: "🔨 강두호 장인의 담금질 망치", source: "1지역 을지로 대장간", icon: "assets/ui/items_uniques/unique_1.png?v=2", effect: "착용 중인 방어구·방패의 기본 방어력 수치를 2.0배로 증폭" },
    { id: 2, name: "🍬 박동석의 딸기맛 각성 사탕", source: "2지역 북한산 캠프", icon: "assets/ui/items_uniques/unique_2.png?v=2", effect: "치명타 적중 시 15% 확률로 모든 스킬 쿨타임 즉시 초기화" },
    { id: 3, name: "🐉 백도훈의 부러진 청룡 목검", source: "4지역 설악산 대청봉", icon: "assets/ui/items_uniques/unique_3.png?v=2", effect: "직업 무관 평타 5회마다 [삼할 청룡참] 검기 자동 발사" },
    { id: 4, name: "🪽 타락한 성녀의 검은 성서", source: "12지역 라인강 방어선", icon: "assets/ui/items_uniques/unique_4.png?v=2", effect: "모든 치유 스킬이 400% 위력의 암흑 저주 폭발로 전환" },
    { id: 5, name: "❄️ 시베리아 빙여제의 수정구", source: "11지역 시베리아 요새", icon: "assets/ui/items_uniques/unique_5.png?v=2", effect: "모든 공격에 [냉기] 속성 부여 및 빙결 적 피해 +85%" },
    { id: 6, name: "⚙️ 보리스의 아다만티움 외골격", source: "8지역 블라디보스토크", icon: "assets/ui/items_uniques/unique_6.png?v=2", effect: "이속 -15% 대신 최대 체력 +100% 및 최대체력 15% 물리피해 추가" },
    { id: 7, name: "💀 아서의 말없는 해골 투구", source: "2지역 은문 보스전", icon: "assets/ui/items_uniques/unique_7.png?v=2", effect: "타 직업이어도 제1군단장 듀라한 아서가 상시 호위 기사로 참전" },
    { id: 8, name: "🥷 카게미츠의 그림자 수리검", source: "6지역 도쿄 음양사", icon: "assets/ui/items_uniques/unique_8.png?v=2", effect: "모든 투사체 스킬 발사 개수가 +3개 추가됨" },
    { id: 9, name: "📡 벨록의 전술 해킹 단말기", source: "13지역 금문 함교", icon: "assets/ui/items_uniques/unique_9.png?v=2", effect: "타 직업 스킬을 장착해도 [직업 정통성 보너스(+25% 위력)] 적용" },
    { id: 10, name: "🌋 베히모스의 용암 심장", source: "12지역 로키산맥 화산", icon: "assets/ui/items_uniques/unique_10.png?v=2", effect: "초당 공격력 300% 화염 오라 + 냉기 스킬이 [융해]로 2배 피해" },
    { id: 11, name: "🦑 크라켄의 흡착 촉수", source: "9지역 태평양 해연", icon: "assets/ui/items_uniques/unique_11.png?v=2", effect: "적들을 전방으로 끌어당기며 입힌 피해의 12%를 체력/마나로 흡혈" },
    { id: 12, name: "🐉 히말라야 고룡의 역린", source: "10지역 고룡 묘지", icon: "assets/ui/items_uniques/unique_12.png?v=2", effect: "궁극기 쿨타임 -45% 및 궁극기 시전 중 완전 무적" },
    { id: 13, name: "💍 인천항 거상의 황금 반지", source: "3지역 인천항 블랙마켓", icon: "assets/ui/items_uniques/unique_13.png?v=2", effect: "골드 획득 +100% 및 보유 골드 비례 피해량 최대 +150%" },
    { id: 14, name: "🍕 10주년 약속의 피자 박스", source: "14지역 평화의 서울", icon: "assets/ui/items_uniques/unique_14.png?v=2", effect: "친구 지원 스킬 쿨타임 -50% 및 호출 시 체력/마나 50% 즉시 완치" },
    { id: 15, name: "🍗 한밤의 치킨과 소주잔", source: "서울 보육원 단골 식당", icon: "assets/ui/items_uniques/unique_15.png?v=2", effect: "보스 웨이브 진입 시 20초간 공격/방어/치명타피해 +60% 만찬 버프" },
    { id: 16, name: "🛡️ 박태준 부단장의 특전 방탄복", source: "수도권 사령부", icon: "assets/ui/items_uniques/unique_16.png?v=2", effect: "최대 체력의 25%를 초과하는 피해를 입지 않음 (원콤 방지)" },
    { id: 17, name: "🔥 서유나 대위의 과열 코어", source: "마도포병여단", icon: "assets/ui/items_uniques/unique_17.png?v=2", effect: "마나 소모량 2배 대신 모든 마법/포격 피해량 +90% 증폭" },
    { id: 18, name: "🔭 강민우 관측수의 표적기", source: "특수저격대", icon: "assets/ui/items_uniques/unique_18.png?v=2", effect: "보스에게 자동으로 [표적] 마크 부여 (치명타 확률 +40%)" },
    { id: 19, name: "📿 이수아 사제의 묵주", source: "성역의무단", icon: "assets/ui/items_uniques/unique_19.png?v=2", effect: "보호막 유지 중 모든 상태이상 면역 및 쿨타임 가속 +35%" },
    { id: 20, name: "🧪 한지윤 박사의 마력 영약", source: "판교 마도공학 연구소", icon: "assets/ui/items_uniques/unique_20.png?v=2", effect: "전투 중 장착된 모든 [특성(Trait)]의 적용 레벨을 임시 +2레벨" },
    { id: 21, name: "📜 강태식 협회장의 S급 임명장", source: "대한헌터협회", icon: "assets/ui/items_uniques/unique_21.png?v=2", effect: "아군 소환수 및 용병의 최대 소환 개체수 제한 +3기 증가" },
    { id: 22, name: "🕶️ 윤서연 차관의 기밀 블랙박스", source: "국방부 특임차관실", icon: "assets/ui/items_uniques/unique_22.png?v=2", effect: "보스 처치 시 아이템을 2번 드랍(더블 루팅)할 확률 50%" },
    { id: 23, name: "🕷️ 아라크네의 맹독 갑피", source: "1지역 지하철 미궁", icon: "assets/ui/items_uniques/unique_23.png?v=2", effect: "피격 시 공격자에게 5초간 체력 20%를 깎는 신경독 자동 전염" },
    { id: 24, name: "🎲 마카오 용왕의 속임수 주사위", source: "7지역 마카오 카지노", icon: "assets/ui/items_uniques/unique_24.png?v=2", effect: "모든 공격 피해가 50%~300% 사이로 랜덤 폭발 (777시 7배)" },
    { id: 25, name: "⚡ 뇌제 마커스의 번개 창끝", source: "12지역 북미 연맹", icon: "assets/ui/items_uniques/unique_25.png?v=2", effect: "이동 거리에 비례해 충전되어 다음 스킬에 연쇄 뇌격(600%) 추가" },
    { id: 26, name: "⚔️ 철혈왕 지크프리트의 대검", source: "12지역 라인강 방어선", icon: "assets/ui/items_uniques/unique_26.png?v=2", effect: "체력 50% 이상일 때 모든 공격에 방어 무시 고정 피해 +40%" },
    { id: 27, name: "🏜️ 사막왕 라시드의 모래시계", source: "11지역 타클라마칸", icon: "assets/ui/items_uniques/unique_27.png?v=2", effect: "사망 피해를 입으면 시간을 4초 전으로 되돌려 완치 (전투당 1회)" },
    { id: 28, name: "👊 권왕 진무극의 곤륜 옥패", source: "11지역 곤륜 특구", icon: "assets/ui/items_uniques/unique_28.png?v=2", effect: "무기 해제(맨손) 시 기본 공격력 및 공격속도 3.0배 폭증" },
    { id: 29, name: "🔮 마도왕 아르카나의 수정구", source: "스위스 제네바 마도탑", icon: "assets/ui/items_uniques/unique_29.png?v=2", effect: "마나가 100% 고정되며 최대 마나의 200%만큼 영구 마법 보호막" },
    { id: 30, name: "🛸 타르코스의 중력 제어기", source: "13지역 금문 함교", icon: "assets/ui/items_uniques/unique_30.png?v=2", effect: "화면 내 모든 적의 이동 및 투사체 속도를 70% 둔화시키는 역중력장" },
    { id: 31, name: "🪓 볼가르의 행성 파쇄추", source: "14지역 성층권 결전", icon: "assets/ui/items_uniques/unique_31.png?v=2", effect: "공속 -30% 대신 모든 공격이 범위 폭발 및 확정 치명타" },
    { id: 32, name: "🌑 시렌의 아공간 망토", source: "14지역 성층권 결전", icon: "assets/ui/items_uniques/unique_32.png?v=2", effect: "3초마다 1초씩 차원 은신(타겟팅 해제 및 완전 무적)" },
    { id: 33, name: "👑 외계 황제의 부서진 왕관", source: "14지역 최종 보스", icon: "assets/ui/items_uniques/unique_33.png?v=2", effect: "모든 5부작 세트 요구 장비 수 -1 감소 (4부위로 5세트 발동)" },
    { id: 34, name: "🧬 벨록의 기억 결정체", source: "13지역 벨록의 선물", icon: "assets/ui/items_uniques/unique_34.png?v=2", effect: "전투 경험치 +200% 및 스킬 마법서 드랍률 3배 증가" },
    { id: 35, name: "💎 다이아몬드 차원 파편", source: "14지역 성층권 균열", icon: "assets/ui/items_uniques/unique_35.png?v=2", effect: "장착된 모든 액티브 스킬이 25% 확률로 쿨타임 없이 2연타 발동" },
    { id: 36, name: "🕰️ 회귀자의 태엽 회중시계", source: "1화 회귀 시작 유물", icon: "assets/ui/items_uniques/unique_36.png?v=2", effect: "회귀(Regression) 시 보유 고유 아이템 1개를 소멸시키지 않고 계승" }
];

// 5. 6대 차원문(Gate) 등급 메타데이터 & 14개 지역 84종 몬스터·특성 매핑
const GATES_DATA = {
    "iron": {
        id: "iron",
        name: "🚪 철문 (Iron Gate)",
        sprite: "assets/ui/gates/gate_iron.png?v=2",
        color: "#a8b4c4",
        tier: "Tier 1 · 초급 지하 균열",
        envModifier: "🌫️ [지하 탁기] 시야 협소 · 맹독 포자 발생 (초당 최대체력 1% 침식)",
        dropBonus: "기본 마력석 ×1.0 · 철문 하급 유물 드랍",
        rewardGold: 1500
    },
    "bronze": {
        id: "bronze",
        name: "🚪 동문 (Bronze Gate)",
        sprite: "assets/ui/gates/gate_bronze.png?v=2",
        color: "#e69650",
        tier: "Tier 2 · 중급 군사 균열",
        envModifier: "⚙️ [중장갑 요새화] 적 괴수 방어력 +20% · 폭발물 및 지뢰 함정 활성화",
        dropBonus: "마력석 획득 ×1.5 · 청동 무기고 장비 상자 드랍",
        rewardGold: 3200
    },
    "silver": {
        id: "silver",
        name: "🚪 은문 (Silver Gate)",
        sprite: "assets/ui/gates/gate_silver.png?v=2",
        color: "#00f0ff",
        tier: "Tier 3 · 상급 고대 성역",
        envModifier: "❄️ [은빛 마력 한기] 영웅 마나 회복 +30% · 언데드 및 검기 계열 적 공격력 +25%",
        dropBonus: "마력석 획득 ×2.5 · 신화 세트(Set) 파츠 드랍률 2배",
        rewardGold: 6500
    },
    "gold": {
        id: "gold",
        name: "🚪 금문 (Gold Gate)",
        sprite: "assets/ui/gates/gate_gold.png?v=2",
        color: "#ffd000",
        tier: "Tier 4 · 대재앙급 황금 균열",
        envModifier: "⚡ [황금 과부하 역장] 적 전체 슈퍼아머 부여 · 치명타 피해량 +50% 증폭",
        dropBonus: "마력석 획득 ×4.5 · 고유(Unique) 유물 및 스킬 비급서 드랍",
        rewardGold: 14000
    },
    "platinum": {
        id: "platinum",
        name: "🚪 플래티넘문 (Platinum Gate)",
        sprite: "assets/ui/gates/gate_platinum.png?v=2",
        color: "#c850ff",
        tier: "Tier 5 · 신화 심연 게이트",
        envModifier: "🌌 [심연 중력 왜곡] 쿨타임 가속 +25% · 보스 사망 시 1회 광폭화 부활 패턴 발동",
        dropBonus: "마력석 획득 ×8.0 · 10왕/고룡급 신화 코어 확정 드랍",
        rewardGold: 30000
    },
    "diamond": {
        id: "diamond",
        name: "🚪 다이아몬드문 (Diamond Gate)",
        sprite: "assets/ui/gates/gate_diamond.png?v=2",
        color: "#ff2a6d",
        tier: "Tier 6 · 종언의 성층권 게이트",
        envModifier: "👑 [황제의 절대 권역] 모든 적 피해량 +100% · 영웅 영혼 각인 슬롯 위력 2배 개방",
        dropBonus: "마력석 획득 ×15.0 · 종결 신화 5세트 & 외계 황제 유물 확정 드랍",
        rewardGold: 75000
    }
};

const REGIONS_DATA = {
    1: {
        name: "서울 지하철 미궁 & 석회 동굴",
        town: "assets/ui/regions/town_bg_1.png?v=10",
        battle: "assets/ui/regions/battle_bg_1.png?v=10",
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
        town: "assets/ui/regions/town_bg_2.png?v=10",
        battle: "assets/ui/regions/battle_bg_2.png?v=10",
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
        town: "assets/ui/regions/town_bg_3.png?v=10",
        battle: "assets/ui/regions/battle_bg_3.png?v=10",
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
        town: "assets/ui/regions/town_bg_4.png?v=10",
        battle: "assets/ui/regions/battle_bg_4.png?v=10",
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
        town: "assets/ui/regions/town_bg_5.png?v=10",
        battle: "assets/ui/regions/battle_bg_5.png?v=10",
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
        town: "assets/ui/regions/town_bg_6.png?v=10",
        battle: "assets/ui/regions/battle_bg_6.png?v=10",
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
        town: "assets/ui/regions/town_bg_7.png?v=10",
        battle: "assets/ui/regions/battle_bg_7.png?v=10",
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
        town: "assets/ui/regions/town_bg_8.png?v=10",
        battle: "assets/ui/regions/battle_bg_8.png?v=10",
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
        town: "assets/ui/regions/town_bg_9.png?v=10",
        battle: "assets/ui/regions/battle_bg_9.png?v=10",
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
        town: "assets/ui/regions/town_bg_10.png?v=10",
        battle: "assets/ui/regions/battle_bg_10.png?v=10",
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
        town: "assets/ui/regions/town_bg_11.png?v=10",
        battle: "assets/ui/regions/battle_bg_11.png?v=10",
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
        town: "assets/ui/regions/town_bg_12.png?v=10",
        battle: "assets/ui/regions/battle_bg_12.png?v=10",
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
        town: "assets/ui/regions/town_bg_13.png?v=10",
        battle: "assets/ui/regions/battle_bg_13.png?v=10",
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
        town: "assets/ui/regions/town_bg_14.png?v=10",
        battle: "assets/ui/regions/battle_bg_14.png?v=10",
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
};

// =========================================================================
// 6. 12대 직업 240x240 다중 레이어 페이퍼돌 구성 매핑 (PROJECT 2100 규격)
// =========================================================================
const CLASS_PAPERDOLL_CONFIG = {
    "necro": {
        body: "male_nemesis",
        armor: null,
        weapon: "crystal",
        mutation: "wings",
        wings: null
    },
    "guardian": {
        body: "male",
        armor: "hardlight",
        weapon: "heavy",
        mutation: "spikes",
        wings: null
    },
    "storm_wizard": {
        body: "female",
        armor: null,
        weapon: "crystal",
        mutation: "halo",
        wings: null
    },
    "sniper": {
        body: "male",
        armor: "military",
        weapon: "heavy",
        mutation: "visor",
        wings: null
    },
    "priest": {
        body: "female",
        armor: "female_hardlight",
        weapon: "crystal",
        mutation: "halo",
        wings: "fairy_wings"
    },
    "assassin": {
        body: "male",
        armor: "leather",
        weapon: "katana",
        mutation: "claws",
        wings: null
    },
    "sword_master": {
        body: "male",
        armor: "leather",
        weapon: "katana",
        mutation: "core",
        wings: null
    },
    "death_knight": {
        body: "male_nemesis",
        armor: null,
        weapon: "lava",
        mutation: "horns",
        wings: null
    },
    "martial_king": {
        body: "male",
        armor: "leather",
        weapon: "axe",
        mutation: "booster",
        wings: null
    },
    "psionic_tactician": {
        body: "male",
        armor: null,
        weapon: "crystal",
        mutation: "antennae",
        wings: null
    },
    "berserker": {
        body: "male",
        armor: "leather",
        weapon: "axe",
        mutation: "spikes",
        wings: null
    },
    "cryo_empress": {
        body: "female_nemesis",
        armor: null,
        weapon: "crystal",
        mutation: "crystals",
        wings: null
    }
};
