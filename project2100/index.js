/* -------------------------------------------------------------
 * 🧬 PROJECT 2100 - 포레저 스타일 통합 엔진 스크립트 (Forager Retro Engine)
 * ------------------------------------------------------------- */

// 1. 14개 지역별 6종 적 유닛 (총 84종) 몬스터 데이터베이스
const MONSTERS_DATABASE = {
  1: [
    { name: "눈보라 좀비 늑대", type: "normal", hp: 120, def: 8, atk: 15, img: "assets/monsters/m_1_1.png" },
    { name: "핵겨울 서리 슬라임", type: "normal", hp: 100, def: 12, atk: 12, img: "assets/monsters/m_1_2.png" },
    { name: "방사능 침식 노루", type: "normal", hp: 140, def: 5, atk: 18, img: "assets/monsters/m_1_3.png" },
    { name: "설산 돌가루 원혼", type: "normal", hp: 110, def: 15, atk: 14, img: "assets/monsters/m_1_4.png" },
    { name: "서리이빨 카이드 우두머리", type: "named", hp: 280, def: 20, atk: 28, img: "assets/monsters/m_1_named.png" },
    { name: "설원 폭군 카이드 키메라", type: "boss", hp: 550, def: 35, atk: 45, img: "assets/monsters/m_1_boss.png" }
  ],
  2: [
    { name: "냉각수 오염 돌연변이", type: "normal", hp: 160, def: 10, atk: 18, img: "assets/monsters/m_2_1.png" },
    { name: "원전 방출 슬러지", type: "normal", hp: 130, def: 8, atk: 22, img: "assets/monsters/m_2_2.png" },
    { name: "납차폐복 입은 구울", type: "normal", hp: 180, def: 15, atk: 16, img: "assets/monsters/m_2_3.png" },
    { name: "멜트다운 오염 서생원", type: "normal", hp: 110, def: 5, atk: 25, img: "assets/monsters/m_2_4.png" },
    { name: "노심 경비 좀비 대장", type: "named", hp: 320, def: 25, atk: 35, img: "assets/monsters/m_2_named.png" },
    { name: "임계초과 노심 융합체", type: "boss", hp: 650, def: 40, atk: 55, img: "assets/monsters/m_2_boss.png" }
  ],
  3: [
    { name: "오작동 나노 스파이더", type: "normal", hp: 140, def: 12, atk: 20, img: "assets/monsters/m_3_1.png" },
    { name: "버려진 순찰 드론", type: "normal", hp: 120, def: 18, atk: 18, img: "assets/monsters/m_3_2.png" },
    { name: "해킹된 보안 터렛", type: "normal", hp: 150, def: 22, atk: 24, img: "assets/monsters/m_3_3.png" },
    { name: "데이터 파편 유령", type: "normal", hp: 100, def: 5, atk: 30, img: "assets/monsters/m_3_4.png" },
    { name: "글리치 마스터 닌자", type: "named", hp: 300, def: 18, atk: 45, img: "assets/monsters/m_3_named.png" },
    { name: "메가시티 중앙 AI '제논'", type: "boss", hp: 700, def: 45, atk: 60, img: "assets/monsters/m_3_boss.png" }
  ],
  4: [
    { name: "낙진 오염 가고일", type: "normal", hp: 180, def: 20, atk: 22, img: "assets/monsters/m_4_1.png" },
    { name: "방사성 어둠 박쥐", type: "normal", hp: 110, def: 6, atk: 28, img: "assets/monsters/m_4_2.png" },
    { name: "오염된 혈액 점토체", type: "normal", hp: 200, def: 5, atk: 18, img: "assets/monsters/m_4_3.png" },
    { name: "핏빛 나노 구울", type: "normal", hp: 150, def: 12, atk: 24, img: "assets/monsters/m_4_4.png" },
    { name: "밤의 추적자 네스", type: "named", hp: 350, def: 20, atk: 40, img: "assets/monsters/m_4_named.png" },
    { name: "루마니아 흡혈귀 군주", type: "boss", hp: 750, def: 35, atk: 65, img: "assets/monsters/m_4_boss.png" }
  ],
  5: [
    { name: "모래 먼지 전갈 좀비", type: "normal", hp: 150, def: 18, atk: 20, img: "assets/monsters/m_5_1.png" },
    { name: "미라화된 방사선 해골", type: "normal", hp: 130, def: 10, atk: 24, img: "assets/monsters/m_5_2.png" },
    { name: "모래바람 딱정벌레", type: "normal", hp: 170, def: 15, atk: 18, img: "assets/monsters/m_5_3.png" },
    { name: "무덤 도굴 오염체", type: "normal", hp: 140, def: 14, atk: 22, img: "assets/monsters/m_5_4.png" },
    { name: "유적 방사능 대주술사", type: "named", hp: 380, def: 22, atk: 42, img: "assets/monsters/m_5_named.png" },
    { name: "미라 대장 아누비스", type: "boss", hp: 800, def: 42, atk: 70, img: "assets/monsters/m_5_boss.png" }
  ],
  6: [
    { name: "낙진 네온 위습", type: "normal", hp: 120, def: 5, atk: 26, img: "assets/monsters/m_6_1.png" },
    { name: "보랏빛 낙진 마녀", type: "normal", hp: 140, def: 8, atk: 28, img: "assets/monsters/m_6_2.png" },
    { name: "오염된 가시 덩굴손", type: "normal", hp: 190, def: 15, atk: 18, img: "assets/monsters/m_6_3.png" },
    { name: "변이 요정 군집체", type: "normal", hp: 130, def: 10, atk: 22, img: "assets/monsters/m_6_4.png" },
    { name: "숲의 파괴자 골리앗", type: "named", hp: 420, def: 30, atk: 38, img: "assets/monsters/m_6_named.png" },
    { name: "숲의 망령 대정령", type: "boss", hp: 850, def: 45, atk: 72, img: "assets/monsters/m_6_boss.png" }
  ],
  7: [
    { name: "메카 탄소 돌진황소", type: "normal", hp: 200, def: 25, atk: 24, img: "assets/monsters/m_7_1.png" },
    { name: "핵추진 사냥 맹견", type: "normal", hp: 130, def: 12, atk: 26, img: "assets/monsters/m_7_2.png" },
    { name: "기병대 오염 창병", type: "normal", hp: 160, def: 16, atk: 28, img: "assets/monsters/m_7_3.png" },
    { name: "방사성 청동 대머리수리", type: "normal", hp: 120, def: 10, atk: 30, img: "assets/monsters/m_7_4.png" },
    { name: "몽골 약탈 기병대장", type: "named", hp: 450, def: 28, atk: 45, img: "assets/monsters/m_7_named.png" },
    { name: "기갑 제국 칸 '바투'", type: "boss", hp: 900, def: 50, atk: 80, img: "assets/monsters/m_7_boss.png" }
  ],
  8: [
    { name: "화염 가스 폭탄충", type: "normal", hp: 110, def: 5, atk: 35, img: "assets/monsters/m_8_1.png" },
    { name: "마그마 등껍질 거북", type: "normal", hp: 220, def: 30, atk: 18, img: "assets/monsters/m_8_2.png" },
    { name: "방사능 불꽃 전갈", type: "normal", hp: 150, def: 14, atk: 28, img: "assets/monsters/m_8_3.png" },
    { name: "잿더미 유인 좀비", type: "normal", hp: 170, def: 10, atk: 25, img: "assets/monsters/m_8_4.png" },
    { name: "불타는 재앙의 전마", type: "named", hp: 460, def: 25, atk: 50, img: "assets/monsters/m_8_named.png" },
    { name: "대지 붕괴 주신 이프리트", type: "boss", hp: 950, def: 48, atk: 85, img: "assets/monsters/m_8_boss.png" }
  ],
  9: [
    { name: "변이 초음파 돌고래", type: "normal", hp: 150, def: 12, atk: 25, img: "assets/monsters/m_9_1.png" },
    { name: "산성 방출 거대 해파리", type: "normal", hp: 130, def: 8, atk: 30, img: "assets/monsters/m_9_2.png" },
    { name: "오염 심해 아귀", type: "normal", hp: 180, def: 18, atk: 26, img: "assets/monsters/m_9_3.png" },
    { name: "바다 침식 세이렌 좀비", type: "normal", hp: 160, def: 10, atk: 28, img: "assets/monsters/m_9_4.png" },
    { name: "지중해 심해 청소부", type: "named", hp: 480, def: 30, atk: 48, img: "assets/monsters/m_9_named.png" },
    { name: "바다의 종말 레비아탄", type: "boss", hp: 1000, def: 52, atk: 90, img: "assets/monsters/m_9_boss.png" }
  ],
  10: [
    { name: "오로라 빙하 좀비곰", type: "normal", hp: 240, def: 20, atk: 26, img: "assets/monsters/m_10_1.png" },
    { name: "EMP 방출 야생늑대", type: "normal", hp: 140, def: 12, atk: 28, img: "assets/monsters/m_10_2.png" },
    { name: "오로라 결정 광부좀비", type: "normal", hp: 160, def: 22, atk: 22, img: "assets/monsters/m_10_3.png" },
    { name: "의지 잃은 오딘 전사", type: "normal", hp: 180, def: 15, atk: 30, img: "assets/monsters/m_10_4.png" },
    { name: "버서커 족장 그림", type: "named", hp: 520, def: 28, atk: 55, img: "assets/monsters/m_10_named.png" },
    { name: "오로라 타락체 발키리", type: "boss", hp: 1100, def: 55, atk: 95, img: "assets/monsters/m_10_boss.png" }
  ],
  11: [
    { name: "오염된 삼두우 좀비", type: "normal", hp: 220, def: 18, atk: 25, img: "assets/monsters/m_11_1.png" },
    { name: "방사선 코브라 변이종", type: "normal", hp: 130, def: 10, atk: 32, img: "assets/monsters/m_11_2.png" },
    { name: "정신지배 오염 신도", type: "normal", hp: 150, def: 8, atk: 28, img: "assets/monsters/m_11_3.png" },
    { name: "카르마 낙진 정령", type: "normal", hp: 120, def: 25, atk: 24, img: "assets/monsters/m_11_4.png" },
    { name: "타락한 은둔 구루", type: "named", hp: 500, def: 32, atk: 52, img: "assets/monsters/m_11_named.png" },
    { name: "사성 오염체 브라만", type: "boss", hp: 1150, def: 58, atk: 100, img: "assets/monsters/m_11_boss.png" }
  ],
  12: [
    { name: "체르노빌 냉각수 오염물", type: "normal", hp: 170, def: 14, atk: 28, img: "assets/monsters/m_12_1.png" },
    { name: "노심 용해 피각종", type: "normal", hp: 190, def: 20, atk: 30, img: "assets/monsters/m_12_2.png" },
    { name: "맹독 방사선 고치좀비", type: "normal", hp: 140, def: 28, atk: 24, img: "assets/monsters/m_12_3.png" },
    { name: "방사능 침식 야생멧돼지", type: "normal", hp: 210, def: 16, atk: 26, img: "assets/monsters/m_12_4.png" },
    { name: "체르노빌 고공 습격자", type: "named", hp: 540, def: 35, atk: 60, img: "assets/monsters/m_12_named.png" },
    { name: "노심 파괴수 코어브레이커", type: "boss", hp: 1200, def: 60, atk: 110, img: "assets/monsters/m_12_boss.png" }
  ],
  13: [
    { name: "중성자 가드 방어드론", type: "normal", hp: 130, def: 30, atk: 22, img: "assets/monsters/m_13_1.png" },
    { name: "침입 감지 중형 터렛", type: "normal", hp: 180, def: 25, atk: 32, img: "assets/monsters/m_13_2.png" },
    { name: "나노 경화 보초병", type: "normal", hp: 200, def: 35, atk: 25, img: "assets/monsters/m_13_3.png" },
    { name: "오작동 궤도 청소차", type: "normal", hp: 150, def: 15, atk: 30, img: "assets/monsters/m_13_4.png" },
    { name: "벙커 연방 수호 부동병", type: "named", hp: 600, def: 40, atk: 58, img: "assets/monsters/m_13_named.png" },
    { name: "센트리 마스터 '아이언웰'", type: "boss", hp: 1300, def: 65, atk: 120, img: "assets/monsters/m_13_boss.png" }
  ],
  14: [
    { name: "에베레스트 예티", type: "normal", hp: 250, def: 22, atk: 32, img: "assets/monsters/m_14_1.png" },
    { name: "얼어붙은 조난자 좀비", type: "normal", hp: 190, def: 18, atk: 30, img: "assets/monsters/m_14_2.png" },
    { name: "고대 얼음정령", type: "normal", hp: 220, def: 35, atk: 28, img: "assets/monsters/m_14_3.png" },
    { name: "변이 스노우 레오파드", type: "normal", hp: 180, def: 15, atk: 38, img: "assets/monsters/m_14_4.png" },
    { name: "에베레스트 클라이머좀비", type: "named", hp: 650, def: 45, atk: 68, img: "assets/monsters/m_14_named.png" },
    { name: "최종 7성 재앙 보스 [빅풋]", type: "boss", hp: 1600, def: 75, atk: 140, img: "assets/monsters/m_14_boss.png" }
  ]
};

// 2. 지역 및 특성 칩셋 데이터 (13대 고유 신체 변이 파츠)
const TRAIT_MUTATIONS = {
  body_mutation: "horns",
  energy_discharge: "tail",
  sensory_tech: "visor",
  blood_absorption: "wings",
  cellular_shield: "shell",
  fairy_magic: "fairy_wings",
  power_overload: "booster",
  thermal_control: "spikes",
  ultrasonic_disruption: "antennae",
  berserker_madness: "claws",
  radiation_assimilation: "core",
  meltdown_control: "crystals",
  hightech_engineering: "halo"
};

const TRAIT_PART_NAMES = {
  horns: "흑요석 악마 뿔 (Horns)",
  tail: "전격 생체 꼬리 (Tail)",
  visor: "사이버 센서 바이저 (Visor)",
  wings: "흡혈 악마 날개 (Wings)",
  shell: "외골격 키틴 등껍질 (Shell)",
  fairy_wings: "영롱한 요정 날개 (Fairy Wings)",
  booster: "플라즈마 부스터 배기구 (Booster)",
  spikes: "화염 어깨 가시 견갑 (Spikes)",
  antennae: "초음파 감각 안테나 (Antennae)",
  claws: "핏빛 야수 손톱 (Claws)",
  core: "방사능 아크 코어 (Core)",
  crystals: "용융 척추 크리스탈 (Crystals)",
  halo: "하이테크 홀로그램 링 (Halo)"
};

const TRAITS_DATA = {
  body_mutation: { 
    id: "body_mutation", 
    name: "신체 변이", 
    category: "mutation", 
    region: 1, 
    radCost: 250, 
    mutationPart: "horns",
    description: "신체 부위가 괴수화되어 공격 시 30% 확률로 [변이 충격파] 발동 (1.6배 피해 + 적 방어 완전 무시). 영구 스탯 공격력 +25%, 체력 +20%." 
  },
  energy_discharge: { 
    id: "energy_discharge", 
    name: "에너지 방출", 
    category: "offense", 
    region: 2, 
    radCost: 250, 
    mutationPart: "tail",
    description: "꼬리에서 고전압 에너지를 방출하여 방어력 관통 35% 기본 적용. 공격 시 30% 확률로 [플라즈마 볼트 탄막]을 방출하여 모든 살아있는 적 동시 타격." 
  },
  sensory_tech: { 
    id: "sensory_tech", 
    name: "감각 변이/테크", 
    category: "mutation", 
    region: 3, 
    radCost: 250, 
    mutationPart: "visor",
    description: "생체 바이저로 적의 급소를 정밀 분석. 치명타 확률 +30%, 치명타 피해 +50% 증가. 공격 시 25% 확률로 턴 딜레이 없이 즉시 추가 행동." 
  },
  blood_absorption: { 
    id: "blood_absorption", 
    name: "혈액 흡수", 
    category: "survival", 
    region: 4, 
    radCost: 250, 
    mutationPart: "wings",
    description: "키메라 날개로 적의 생명력을 흡수하여 가한 피해의 35%를 체력으로 즉시 흡혈. 체력 50% 이하 시 흡혈량 2배 (70%)로 폭증." 
  },
  cellular_shield: { 
    id: "cellular_shield", 
    name: "세포 차폐", 
    category: "survival", 
    region: 5, 
    radCost: 250, 
    mutationPart: "shell",
    description: "외골격 키틴 등껍질에서 세포 나노 차폐막 전개. 라운드 개시 시 2회의 피해 완전 무효화 배리어 충전. 피격 시 30% 확률로 피해를 0으로 상쇄." 
  },
  fairy_magic: { 
    id: "fairy_magic", 
    name: "요정 마법", 
    category: "control", 
    region: 6, 
    radCost: 250, 
    mutationPart: "fairy_wings",
    description: "발광 요정 날개가 공명하여 특수 스킬 발동 확률이 30%에서 60%로 상승. 스킬 공격력 2배 증폭 및 시전 시 최대 체력 15% 회복." 
  },
  power_overload: { 
    id: "power_overload", 
    name: "동력 과부하", 
    category: "control", 
    region: 7, 
    radCost: 250, 
    mutationPart: "booster",
    description: "플라즈마 부스터 배기구 과부하 가속. 공격 시 40% 확률로 [오버로드 연속 타격]이 발동하여 적에게 2연속 타격을 쏟아부음." 
  },
  thermal_control: { 
    id: "thermal_control", 
    name: "열에너지 제어", 
    category: "offense", 
    region: 8, 
    radCost: 250, 
    mutationPart: "spikes",
    description: "화염 어깨 가시 견갑에서 고열 방출. 요원의 모든 공격에 [지옥 화염]을 부착하여 매 턴 적 최대 체력의 5% 소각 도트 피해를 입힘." 
  },
  ultrasonic_disruption: { 
    id: "ultrasonic_disruption", 
    name: "초음파 정신 교란", 
    category: "control", 
    region: 9, 
    radCost: 250, 
    mutationPart: "antennae",
    description: "초음파 감각 안테나에서 펄스 방출. 공격 시 35% 확률로 대상을 [초음파 혼란/기절] 상태로 빠뜨려 다음 턴 행동을 강제 스킵시킴." 
  },
  berserker_madness: { 
    id: "berserker_madness", 
    name: "버서커 광기", 
    category: "mutation", 
    region: 10, 
    radCost: 250, 
    mutationPart: "claws",
    description: "핏빛 야수 손톱이 붉게 물들며 잃은 체력 10%당 공격력 15% 증가. 체력 30% 이하 시 [분노 각성] 상태가 되어 공격력이 2.5배로 폭증." 
  },
  radiation_assimilation: { 
    id: "radiation_assimilation", 
    name: "오염 동화", 
    category: "mutation", 
    region: 11, 
    radCost: 250, 
    mutationPart: "core",
    description: "방사능 아크 코어가 오염 물질을 에너지로 변환. 보유 Rad 1000당 공격력과 방어력 +15% 증가. 전투 중 괴수 처치 시 100 Rad 추가 흡수." 
  },
  meltdown_control: { 
    id: "meltdown_control", 
    name: "멜트다운 제어", 
    category: "offense", 
    region: 12, 
    radCost: 250, 
    mutationPart: "crystals",
    description: "용융 척추 크리스탈이 노심 융해를 제어. 피격 시 받은 피해의 30%를 적에게 [방사능 반사]로 되돌려주며, 체력 35% 이하 시 전 스탯이 70% 폭증." 
  },
  hightech_engineering: { 
    id: "hightech_engineering", 
    name: "하이테크 공학", 
    category: "survival", 
    region: 13, 
    radCost: 250, 
    mutationPart: "halo",
    description: "하이테크 홀로그램 링 연산 가동. 라운드 시작 시 최대 체력의 30%에 해당하는 [나노 쉴드(보호막)]를 자동 전개하여 체력 손실을 방어." 
  }
};

const FUSION_DATA = {
  bio_plasma_burst: {
    id: "bio_plasma_burst",
    name: "생체 플라즈마포",
    req: ["body_mutation", "energy_discharge"],
    description: "변이 충격파 발동 시 플라즈마 탄막이 동시 방출되어 살아있는 적 전체에 1.8배 광역 타격"
  },
  primal_predator: {
    id: "primal_predator",
    name: "원시 포식자",
    req: ["body_mutation", "sensory_tech"],
    description: "치명타 발생 시 100% 확률로 신체 변이 충격파가 강제 연계 발동"
  },
  vampiric_chimera: {
    id: "vampiric_chimera",
    name: "뱀파이어 키메라",
    req: ["body_mutation", "blood_absorption"],
    description: "신체 괴력 흡혈 (흡혈량 60% + 변이 충격파 발동 시 HP 250 추가 회복)"
  },
  chitin_carapace: {
    id: "chitin_carapace",
    name: "키틴질 외골격",
    req: ["body_mutation", "cellular_shield"],
    description: "받는 모든 피해 35% 상시 경감 + 물리 타격 시 방어력의 100% 추가 고정 피해"
  },
  fairy_beast_surge: {
    id: "fairy_beast_surge",
    name: "요정 야수화",
    req: ["body_mutation", "fairy_magic"],
    description: "스킬 사용 시 괴수 근력이 폭발하여 스킬 대미지 2.5배 증폭 및 최대 체력 20% 회복"
  },
  brutal_overdrive: {
    id: "brutal_overdrive",
    name: "야수 오버드라이브",
    req: ["body_mutation", "power_overload"],
    description: "오버로드 연속 타격 시 2번째 타격이 무조건 방어 무시 변이 충격파로 적중"
  },
  magma_juggernaut: {
    id: "magma_juggernaut",
    name: "마그마 저거너트",
    req: ["body_mutation", "thermal_control"],
    description: "충격파 적중 시 대상에게 지옥화염 3중첩 즉시 부여 및 200의 고열 폭발 피해"
  },
  seismic_roar: {
    id: "seismic_roar",
    name: "대지 파열의 포효",
    req: ["body_mutation", "ultrasonic_disruption"],
    description: "충격파 발동 시 적 전체에 50% 확률로 초음파 기절 동시 부여"
  },
  pandemonium_beast: {
    id: "pandemonium_beast",
    name: "판데모니움 비스트",
    req: ["body_mutation", "berserker_madness"],
    description: "잃은 체력 비례 공격력 상승폭 2배 + 체력 30% 이하 시 충격파 100% 확정 발동"
  },
  nuclear_colossus: {
    id: "nuclear_colossus",
    name: "방사능 거신",
    req: ["body_mutation", "radiation_assimilation"],
    description: "보유 Rad 1000당 신체 변이 추가 공격력 +15% 및 방어력 +15%"
  },
  meltdown_titan: {
    id: "meltdown_titan",
    name: "노심 타이탄",
    req: ["body_mutation", "meltdown_control"],
    description: "체력 35% 이하 시 충격파 피해 2.5배 증폭 및 방사능 반사율 50%로 상승"
  },
  cyborg_mutant: {
    id: "cyborg_mutant",
    name: "사이보그 뮤턴트",
    req: ["body_mutation", "hightech_engineering"],
    description: "나노 쉴드가 켜져 있는 동안 기본 공격력 +40% 및 방어 무시 확률 +25%"
  },
  tactical_railgun: {
    id: "tactical_railgun",
    name: "전술 레일건",
    req: ["energy_discharge", "sensory_tech"],
    description: "에너지 방관율이 60%로 상승하고, 치명타 발생 시 적 전체 관통 레이저 사격"
  },
  plasma_leech: {
    id: "plasma_leech",
    name: "플라즈마 리치",
    req: ["energy_discharge", "blood_absorption"],
    description: "플라즈마 볼트 탄막으로 입힌 모든 광역 피해의 35%를 체력으로 즉시 흡혈"
  },
  energy_barrier_deflection: {
    id: "energy_barrier_deflection",
    name: "에너지 편향 필드",
    req: ["energy_discharge", "cellular_shield"],
    description: "피격 시 방출된 에너지로 적 투사체를 튕겨내며 30% 피해 역반사"
  },
  spark_fairy_storm: {
    id: "spark_fairy_storm",
    name: "요정 스파크 폭풍",
    req: ["energy_discharge", "fairy_magic"],
    description: "스킬 시전 시 탄막 수 2배 증가 및 적 전체에 감전 연쇄 피해"
  },
  hyper_discharge: {
    id: "hyper_discharge",
    name: "하이퍼 과충전",
    req: ["energy_discharge", "power_overload"],
    description: "연속 타격 발동 시 매 타격마다 플라즈마 볼트 탄막이 100% 확정 분출"
  },
  plasma_hellfire: {
    id: "plasma_hellfire",
    name: "플라즈마 헬파이어",
    req: ["energy_discharge", "thermal_control"],
    description: "플라즈마 탄막에 화염이 융합되어 모든 적에게 화상 도트 피해 2배 적용"
  },
  emp_shockwave: {
    id: "emp_shockwave",
    name: "EMP 충격파",
    req: ["energy_discharge", "ultrasonic_disruption"],
    description: "탄막 타격 시 적의 전자 신경계를 마비시켜 45% 확률로 행동 스킵"
  },
  furious_lightning: {
    id: "furious_lightning",
    name: "광란의 뇌전",
    req: ["energy_discharge", "berserker_madness"],
    description: "체력이 낮을수록 에너지 방출 공격력 최대 120% 폭증"
  },
  gamma_ray_burst: {
    id: "gamma_ray_burst",
    name: "감마선 버스트",
    req: ["energy_discharge", "radiation_assimilation"],
    description: "보유 Rad 1000당 탄막 피해 +20% 및 적 처치 시 추가 150 Rad 흡수"
  },
  apocalypse_ragnarok: {
    id: "apocalypse_ragnarok",
    name: "아포칼립스 파편",
    req: ["energy_discharge", "meltdown_control"],
    description: "에너지 방출 시 멜트다운 폭발이 연쇄되어 방어력 100% 완전 무시"
  },
  hardlight_battery: {
    id: "hardlight_battery",
    name: "하드라이트 배터리",
    req: ["energy_discharge", "hightech_engineering"],
    description: "나노 쉴드가 피격될 때마다 에너지가 충전되어 다음 공격력 +50%"
  },
  artery_targeting: {
    id: "artery_targeting",
    name: "동맥 정밀 타격",
    req: ["sensory_tech", "blood_absorption"],
    description: "치명타 타격 시 흡혈량이 100%로 3배 증폭"
  },
  predictive_evasion: {
    id: "predictive_evasion",
    name: "예측 회피 기동",
    req: ["sensory_tech", "cellular_shield"],
    description: "치명타 적중 후 다음 턴 동안 적 공격 완전 회피(무효화) 확률 +35%"
  },
  clairvoyant_mystic: {
    id: "clairvoyant_mystic",
    name: "천리안 신비술",
    req: ["sensory_tech", "fairy_magic"],
    description: "치명타 발생 시 스킬 공격력 +60% 및 즉시 아군 체력 15% 회복"
  },
  cyber_overclock: {
    id: "cyber_overclock",
    name: "사이버 오버클럭",
    req: ["sensory_tech", "power_overload"],
    description: "모든 공격 치명타 100% 확정 + 100% 확정 2연속 타격 발동"
  },
  laser_pyrolysis: {
    id: "laser_pyrolysis",
    name: "레이저 열분해",
    req: ["sensory_tech", "thermal_control"],
    description: "치명타 적중 시 대상의 화상 디버프를 즉시 폭파하여 300의 추가 폭발 피해"
  },
  neural_shatter: {
    id: "neural_shatter",
    name: "뉴럴 셰터",
    req: ["sensory_tech", "ultrasonic_disruption"],
    description: "초음파 기절 확률 65% 폭증 + 기절한 적 타격 시 300% 분쇄 피해"
  },
  death_reckoning: {
    id: "death_reckoning",
    name: "사선 직감",
    req: ["sensory_tech", "berserker_madness"],
    description: "체력 35% 이하 시 치명타 피해량이 3.0배로 극대화"
  },
  quantum_scanner: {
    id: "quantum_scanner",
    name: "양자 방사능 스캐너",
    req: ["sensory_tech", "radiation_assimilation"],
    description: "치명타 발생 시 100% 확률로 80 Rad 즉시 생성"
  },
  critical_meltdown: {
    id: "critical_meltdown",
    name: "임계점 저격",
    req: ["sensory_tech", "meltdown_control"],
    description: "치명타 적중 시 적 노심을 파괴하여 대상 공격력 30% 영구 감소"
  },
  hud_tactical_matrix: {
    id: "hud_tactical_matrix",
    name: "HUD 전술 매트릭스",
    req: ["sensory_tech", "hightech_engineering"],
    description: "쉴드가 유지되는 동안 치명타 피해 +80% 및 턴 가속 확률 40%로 상승"
  },
  immortal_carapace: {
    id: "immortal_carapace",
    name: "불사신 갑각",
    req: ["blood_absorption", "cellular_shield"],
    description: "흡혈로 초과된 회복량이 나노 차폐 쉴드로 자동 전환 (최대 400)"
  },
  vampiric_pixie: {
    id: "vampiric_pixie",
    name: "요정의 흡혈 축복",
    req: ["blood_absorption", "fairy_magic"],
    description: "스킬 발동 시 흡혈량이 아군 전체 회복으로 전환되어 최대 HP 30% 회복"
  },
  blood_rush: {
    id: "blood_rush",
    name: "피의 폭주",
    req: ["blood_absorption", "power_overload"],
    description: "흡혈 성공 시 50% 확률로 즉시 추가 턴 행동"
  },
  boiling_blood: {
    id: "boiling_blood",
    name: "끓어오르는 혈액",
    req: ["blood_absorption", "thermal_control"],
    description: "흡혈 시 대상에게 작열 피해를 입히고 공격력 +25% 화염 버프 획득"
  },
  vampiric_screech: {
    id: "vampiric_screech",
    name: "흡혈박쥐 초음파",
    req: ["blood_absorption", "ultrasonic_disruption"],
    description: "흡혈 성공 시 대상에게 45% 확률로 초음파 기절 부여"
  },
  blood_berserker: {
    id: "blood_berserker",
    name: "블러드 버서커",
    req: ["blood_absorption", "berserker_madness"],
    description: "체력이 낮을수록 흡혈량과 공격력이 지수 폭증 (최대 공격력 3배 + 80% 흡혈)"
  },
  irradiated_blood: {
    id: "irradiated_blood",
    name: "방사능 오염 혈액",
    req: ["blood_absorption", "radiation_assimilation"],
    description: "적의 피를 흡수할 때마다 체내 방사선 정제 (+50 Rad) 및 공격력 +15%"
  },
  sanguine_meltdown: {
    id: "sanguine_meltdown",
    name: "혈액 노심 용해",
    req: ["blood_absorption", "meltdown_control"],
    description: "HP 30% 이하 시 흡혈량 100%로 고정 및 피격 피해 50% 반사"
  },
  nanite_blood_infusion: {
    id: "nanite_blood_infusion",
    name: "나노 혈청 주입",
    req: ["blood_absorption", "hightech_engineering"],
    description: "흡혈 발생 시 나노 쉴드 150 자동 재충전"
  },
  pixie_sanctuary: {
    id: "pixie_sanctuary",
    name: "요정의 성역",
    req: ["cellular_shield", "fairy_magic"],
    description: "배리어 유지 중 스킬 공격력 +50% 및 피격 시 요정 가루로 공격 무효화"
  },
  reactive_dynamo: {
    id: "reactive_dynamo",
    name: "반응형 발전기",
    req: ["cellular_shield", "power_overload"],
    description: "배리어가 적 공격을 무효화할 때마다 동력이 완충되어 다음 공격 2연타 확정"
  },
  flame_retardant_shell: {
    id: "flame_retardant_shell",
    name: "내열 단열 외피",
    req: ["cellular_shield", "thermal_control"],
    description: "화염/도트 피해 완전 면역 및 피격 시 적에게 화상 반사"
  },
  sonic_resonance_barrier: {
    id: "sonic_resonance_barrier",
    name: "음향 공명 방벽",
    req: ["cellular_shield", "ultrasonic_disruption"],
    description: "배리어가 적 공격을 방어할 때 적 전체에 초음파 기절 파동 방출"
  },
  undying_tenacity: {
    id: "undying_tenacity",
    name: "불굴의 버서커",
    req: ["cellular_shield", "berserker_madness"],
    description: "체력이 1 이하로 떨어질 위기 시 1회 한정 배리어 3회 즉시 비상 충전"
  },
  lead_nanite_coat: {
    id: "lead_nanite_coat",
    name: "납-나노 차폐 코팅",
    req: ["cellular_shield", "radiation_assimilation"],
    description: "받는 모든 물리/방사선 피해 25% 고정 경감 + 영구 방어력 +35%"
  },
  core_containment_vessel: {
    id: "core_containment_vessel",
    name: "격납 용기 제어",
    req: ["cellular_shield", "meltdown_control"],
    description: "노심 폭발 피해를 차폐막이 억제하여 생존력 극대화 및 반사율 +40%"
  },
  aegis_barrier: {
    id: "aegis_barrier",
    name: "이지스 나노 배리어",
    req: ["cellular_shield", "hightech_engineering"],
    description: "라운드 시작 쉴드량 2배 (HP의 60%) + 매 턴 방어막 200 자동 복구"
  },
  chrono_fairy: {
    id: "chrono_fairy",
    name: "크로노스 페어리",
    req: ["fairy_magic", "power_overload"],
    description: "스킬 무한 연타 시동 + 35% 확률로 적 턴 강제 스킵"
  },
  fairy_will_o_wisp: {
    id: "fairy_will_o_wisp",
    name: "요정 도깨비불",
    req: ["fairy_magic", "thermal_control"],
    description: "스킬 사용 시 푸른 도깨비불이 적 전체에 번져 지옥화염 3중첩 부착"
  },
  siren_lullaby: {
    id: "siren_lullaby",
    name: "세이렌의 자장가",
    req: ["fairy_magic", "ultrasonic_disruption"],
    description: "스킬 시전 시 적 전체 50% 확률로 수면/기절 상태 돌입"
  },
  valkyrie_rage: {
    id: "valkyrie_rage",
    name: "발키리의 분노",
    req: ["fairy_magic", "berserker_madness"],
    description: "체력이 낮을수록 스킬 피해량이 최대 2.8배까지 증폭"
  },
  aurora_fairy: {
    id: "aurora_fairy",
    name: "오로라 정령",
    req: ["fairy_magic", "radiation_assimilation"],
    description: "스킬 시전 시 보유 Rad 비례 광역 섬광 대미지 (Rad 1000당 25% 추가딜)"
  },
  phoenix_rebirth: {
    id: "phoenix_rebirth",
    name: "불사조 환생",
    req: ["fairy_magic", "meltdown_control"],
    description: "사망 직전 체력 40%로 즉시 부활하며 요정 스킬 마법 자동 난사"
  },
  techno_fairy_matrix: {
    id: "techno_fairy_matrix",
    name: "테크노 페어리",
    req: ["fairy_magic", "hightech_engineering"],
    description: "스킬 발동 시 나노 쉴드 250 즉시 전개"
  },
  overheated_exhaust: {
    id: "overheated_exhaust",
    name: "과열 배기 폭발",
    req: ["power_overload", "thermal_control"],
    description: "2연속 타격 시 2번째 타격에 200 화염 폭발 + 화상 2중첩"
  },
  vibrational_impact: {
    id: "vibrational_impact",
    name: "진동 연타 타격",
    req: ["power_overload", "ultrasonic_disruption"],
    description: "연속 공격 시 적에게 초음파 뇌진탕 부여 (적 방어력 30% 깎음)"
  },
  berserk_flurry: {
    id: "berserk_flurry",
    name: "광전사 난무",
    req: ["power_overload", "berserker_madness"],
    description: "체력 40% 이하 시 3연속 타격으로 업그레이드"
  },
  atomic_turbocharger: {
    id: "atomic_turbocharger",
    name: "원자력 터보차저",
    req: ["power_overload", "radiation_assimilation"],
    description: "연속 공격 발동 확률이 40% -> 60%로 상승"
  },
  meltdown_thruster: {
    id: "meltdown_thruster",
    name: "멜트다운 추진기",
    req: ["power_overload", "meltdown_control"],
    description: "연속 타격 시마다 피격 반사율 15% 영구 누적 상승"
  },
  kinetic_generator: {
    id: "kinetic_generator",
    name: "운동 에너지 발전기",
    req: ["power_overload", "hightech_engineering"],
    description: "연속 타격 시 타격당 나노 쉴드 100 충전"
  },
  thermo_acoustic_blast: {
    id: "thermo_acoustic_blast",
    name: "열음향 폭발",
    req: ["thermal_control", "ultrasonic_disruption"],
    description: "화상 상태인 적 타격 시 초음파 공명으로 2배 폭발 대미지"
  },
  blazing_fury: {
    id: "blazing_fury",
    name: "타오르는 분노",
    req: ["thermal_control", "berserker_madness"],
    description: "체력이 잃을수록 화상 도트 피해가 틱당 최대 12%까지 폭등"
  },
  dirty_bomb_detonator: {
    id: "dirty_bomb_detonator",
    name: "더티밤 기폭장치",
    req: ["thermal_control", "radiation_assimilation"],
    description: "화상 걸린 적이 쓰러지면 방사능 핵분열 폭풍으로 주변 적에 300 광역 피해"
  },
  chernobyl_inferno: {
    id: "chernobyl_inferno",
    name: "체르노빌 연옥",
    req: ["thermal_control", "meltdown_control"],
    description: "지옥화염 도트 피해 2배 + 멜트다운 방사능 반사 피해 50%로 상승"
  },
  thermal_shielding: {
    id: "thermal_shielding",
    name: "열차폐 나노 장갑",
    req: ["thermal_control", "hightech_engineering"],
    description: "피격 시 화염 반사 장벽이 작동하여 공격자에게 즉시 화상 부여"
  },
  mind_rending_howl: {
    id: "mind_rending_howl",
    name: "정신 분쇄 포효",
    req: ["ultrasonic_disruption", "berserker_madness"],
    description: "체력 35% 이하 시 공격마다 적 전체에 50% 확률 기절 부여"
  },
  gamma_synapse_scrambler: {
    id: "gamma_synapse_scrambler",
    name: "감마 시냅스 교란기",
    req: ["ultrasonic_disruption", "radiation_assimilation"],
    description: "기절한 적을 타격할 때마다 120 Rad 강탈"
  },
  meltdown_panic: {
    id: "meltdown_panic",
    name: "멜트다운 공황",
    req: ["ultrasonic_disruption", "meltdown_control"],
    description: "기절한 적은 멜트다운 방사선에 취약해져 받는 피해 50% 증폭"
  },
  sonic_defense_grid: {
    id: "sonic_defense_grid",
    name: "음향 방어 그리드",
    req: ["ultrasonic_disruption", "hightech_engineering"],
    description: "나노 쉴드가 켜져 있을 때 공격한 적에게 35% 확률로 역기절 카운터"
  },
  irradiated_berserker: {
    id: "irradiated_berserker",
    name: "피폭의 광전사",
    req: ["berserker_madness", "radiation_assimilation"],
    description: "보유 Rad 1000당 잃은 체력 비례 공격력 상승폭 20% 추가 증가"
  },
  suicide_meltdown: {
    id: "suicide_meltdown",
    name: "임계돌파 자폭기",
    req: ["berserker_madness", "meltdown_control"],
    description: "체력 25% 이하 시 모든 공격력 3배 + 받는 피해의 70%를 적에게 반사"
  },
  adrenalin_exoskeleton: {
    id: "adrenalin_exoskeleton",
    name: "아드레날린 외골격",
    req: ["berserker_madness", "hightech_engineering"],
    description: "체력이 50% 이하가 되면 나노 쉴드 500이 1회 비상 긴급 전개"
  },
  chernobyl_meltdown: {
    id: "chernobyl_meltdown",
    name: "체르노빌 임계돌파",
    req: ["radiation_assimilation", "meltdown_control"],
    description: "방사능 피해 반사 50% + 공격 시 체르노빌 핵분열 폭풍 발동"
  },
  radiation_converter: {
    id: "radiation_converter",
    name: "방사선 변환 반응로",
    req: ["radiation_assimilation", "hightech_engineering"],
    description: "라운드 시작 시 보유 Rad 1000당 나노 쉴드 150 추가 생성"
  },
  core_reinforcement: {
    id: "core_reinforcement",
    name: "노심 보강 프레임",
    req: ["meltdown_control", "hightech_engineering"],
    description: "나노 쉴드가 활성화되어 있어도 멜트다운 30% 피해 반사가 100% 정상 작동"
  }
};

const REGIONS_METADATA = {
  1: { name: "시베리아 대황무지", env: "지독한 혹한과 방사능이 섞인 땅", trait: "body_mutation", coords: { x: 30, y: 35 } },
  2: { name: "서유럽 원전 지대", env: "고농도 방사능 데드존 및 슬러지 지대", trait: "energy_discharge", coords: { x: 18, y: 45 } },
  3: { name: "동아시아 메가시티", env: "데이터 잔해와 오작동 보안 기계 구역", trait: "sensory_tech", coords: { x: 42, y: 48 } },
  4: { name: "루마니아", env: "피와 전력을 갈구하는 약탈자 지대", trait: "blood_absorption", coords: { x: 26, y: 42 } },
  5: { name: "이집트", env: "세포 변이로 썩지 않는 미라 무덤 유적", trait: "cellular_shield", coords: { x: 28, y: 55 } },
  6: { name: "영국", env: "푸르고 보랏빛 낙진이 가득한 요정 황무지", trait: "fairy_magic", coords: { x: 14, y: 38 } },
  7: { name: "몽골", env: "방사능 거대마와 신체를 결합한 기병대", trait: "power_overload", coords: { x: 36, y: 44 } },
  8: { name: "중동 유전지대", env: "유전 폭발로 100년째 불타오르는 화염 대지", trait: "thermal_control", coords: { x: 24, y: 50 } },
  9: { name: "그리스 지중해", env: "해수면 상승으로 잠긴 초음파 해양 괴물 구역", trait: "ultrasonic_disruption", coords: { x: 20, y: 50 } },
  10: { name: "북유럽 오로라숲", env: "EMP 폭풍과 버서커 세력이 지배하는 숲", trait: "berserker_madness", coords: { x: 19, y: 32 } },
  11: { name: "인도 오염 사원", env: "오염도가 극에 달한 삼두우 오염 숭배지", trait: "radiation_assimilation", coords: { x: 34, y: 56 } },
  12: { name: "체르노빌 수색지", env: "원전 폭발 중심부의 극위험 파밍 구역", trait: "meltdown_control", coords: { x: 23, y: 40 } },
  13: { name: "스위스 벙커", env: "인간성을 버린 기계 보초병 부대 수용소", trait: "hightech_engineering", coords: { x: 16, y: 44 } },
  14: { name: "에베레스트 산맥", env: "7성 거수 빅풋이 지배하는 세계의 끝", trait: "nemesis", coords: { x: 38, y: 53 } }
};

// 3. 10프레임 캐릭터 정밀 사지(Limb) 독립 애니메이션 오프셋 데이터
const ANIMATION_METADATA = {
  idle: [
    { frame: 0, head: {x: 0, y: 0, rot: 0}, torso: {x: 0, y: 0, rot: 0}, rArm: {x: 0, y: 0, rot: 0}, lArm: {x: 0, y: 0, rot: 0}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 1, head: {x: 0, y: -1, rot: 1}, torso: {x: 0, y: -1, rot: 0}, rArm: {x: 0, y: -1, rot: -2}, lArm: {x: 0, y: -1, rot: 2}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 2, head: {x: 0, y: -2, rot: 2}, torso: {x: 0, y: -2, rot: 0}, rArm: {x: 0, y: -2, rot: -5}, lArm: {x: 0, y: -2, rot: 4}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 3, head: {x: 0, y: -3, rot: 2}, torso: {x: 0, y: -3, rot: 0}, rArm: {x: 0, y: -3, rot: -6}, lArm: {x: 0, y: -3, rot: 5}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 4, head: {x: 0, y: -2, rot: 1}, torso: {x: 0, y: -2, rot: 0}, rArm: {x: 0, y: -2, rot: -4}, lArm: {x: 0, y: -2, rot: 3}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 5, head: {x: 0, y: -1, rot: 0}, torso: {x: 0, y: -1, rot: 0}, rArm: {x: 0, y: -1, rot: -2}, lArm: {x: 0, y: -1, rot: 1}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 6, head: {x: 0, y: 0, rot: -1}, torso: {x: 0, y: 0, rot: 0}, rArm: {x: 0, y: 0, rot: 1}, lArm: {x: 0, y: 0, rot: -1}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 7, head: {x: 0, y: 1, rot: -2}, torso: {x: 0, y: 1, rot: 0}, rArm: {x: 0, y: 1, rot: 3}, lArm: {x: 0, y: 1, rot: -2}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 8, head: {x: 0, y: 1, rot: -1}, torso: {x: 0, y: 1, rot: 0}, rArm: {x: 0, y: 1, rot: 2}, lArm: {x: 0, y: 1, rot: -1}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 9, head: {x: 0, y: 0, rot: 0}, torso: {x: 0, y: 0, rot: 0}, rArm: {x: 0, y: 0, rot: 0}, lArm: {x: 0, y: 0, rot: 0}, legs: {x: 0, y: 0, rot: 0} }
  ],
  run: [
    { frame: 0, head: {x: 2, y: -1, rot: 2}, torso: {x: 2, y: -1, rot: 4}, rArm: {x: 2, y: -1, rot: 25}, lArm: {x: 2, y: -1, rot: -25}, legs: {x: 0, y: 0, rot: -18} },
    { frame: 1, head: {x: 3, y: 0, rot: 1}, torso: {x: 3, y: 0, rot: 5}, rArm: {x: 3, y: 0, rot: 16}, lArm: {x: 3, y: 0, rot: -16}, legs: {x: 0, y: 0, rot: -10} },
    { frame: 2, head: {x: 2, y: 1, rot: 0}, torso: {x: 2, y: 1, rot: 4}, rArm: {x: 2, y: 1, rot: 0}, lArm: {x: 2, y: 1, rot: 0}, legs: {x: 0, y: 0, rot: 0} },
    { frame: 3, head: {x: 1, y: -1, rot: 1}, torso: {x: 1, y: -1, rot: 5}, rArm: {x: 1, y: -1, rot: -16}, lArm: {x: 1, y: -1, rot: 16}, legs: {x: 0, y: 0, rot: 10} },
    { frame: 4, head: {x: 0, y: -2, rot: 2}, torso: {x: 0, y: -2, rot: 6}, rArm: {x: 0, y: -2, rot: -28}, lArm: {x: 0, y: -2, rot: 28}, legs: {x: 0, y: 0, rot: 18} },
    { frame: 5, head: {x: 1, y: -1, rot: 1}, torso: {x: 1, y: -1, rot: 5}, rArm: {x: 1, y: -1, rot: -20}, lArm: {x: 1, y: -1, rot: 20}, legs: {x: 0, y: 0, rot: 12} },
    { frame: 6, head: {x: 2, y: 0, rot: 0}, torso: {x: 2, y: 0, rot: 4}, rArm: {x: 2, y: 0, rot: -8}, lArm: {x: 2, y: 0, rot: 8}, legs: {x: 0, y: 0, rot: 4} },
    { frame: 7, head: {x: 2, y: 1, rot: 0}, torso: {x: 2, y: 1, rot: 4}, rArm: {x: 2, y: 1, rot: 8}, lArm: {x: 2, y: 1, rot: -8}, legs: {x: 0, y: 0, rot: -6} },
    { frame: 8, head: {x: 1, y: 0, rot: 1}, torso: {x: 1, y: 0, rot: 5}, rArm: {x: 1, y: 0, rot: 18}, lArm: {x: 1, y: 0, rot: -18}, legs: {x: 0, y: 0, rot: -14} },
    { frame: 9, head: {x: 2, y: -1, rot: 2}, torso: {x: 2, y: -1, rot: 5}, rArm: {x: 2, y: -1, rot: 26}, lArm: {x: 2, y: -1, rot: -26}, legs: {x: 0, y: 0, rot: -18} }
  ],
  attack: [
    { frame: 0, head: {x: -2, y: 0, rot: -3}, torso: {x: -2, y: 0, rot: -4}, rArm: {x: -2, y: 0, rot: -40}, lArm: {x: 0, y: 0, rot: 15}, legs: {x: 0, y: 0, rot: -4} },
    { frame: 1, head: {x: -4, y: -1, rot: -6}, torso: {x: -4, y: -1, rot: -8}, rArm: {x: -4, y: -1, rot: -75}, lArm: {x: -2, y: 0, rot: 28}, legs: {x: 0, y: 0, rot: -8} },
    { frame: 2, head: {x: -6, y: -2, rot: -10}, torso: {x: -6, y: -2, rot: -12}, rArm: {x: -6, y: -2, rot: -95}, lArm: {x: -3, y: 0, rot: 35}, legs: {x: 0, y: 0, rot: -10} },
    { frame: 3, head: {x: 3, y: 1, rot: 5}, torso: {x: 4, y: 1, rot: 8}, rArm: {x: 4, y: 0, rot: 30}, lArm: {x: 0, y: 0, rot: -15}, legs: {x: 0, y: 0, rot: 6}, vfx: {show: true, x: 0, y: 0, rot: 15} },
    { frame: 4, head: {x: 6, y: 2, rot: 10}, torso: {x: 8, y: 2, rot: 14}, rArm: {x: 8, y: 1, rot: 90}, lArm: {x: -2, y: 0, rot: -30}, legs: {x: 0, y: 0, rot: 12}, vfx: {show: true, x: 6, y: 2, rot: 45} },
    { frame: 5, head: {x: 8, y: 2, rot: 12}, torso: {x: 10, y: 2, rot: 16}, rArm: {x: 10, y: 2, rot: 105}, lArm: {x: -4, y: 0, rot: -35}, legs: {x: 0, y: 0, rot: 14}, vfx: {show: true, x: 10, y: 4, rot: 70} },
    { frame: 6, head: {x: 5, y: 1, rot: 8}, torso: {x: 7, y: 1, rot: 10}, rArm: {x: 7, y: 1, rot: 75}, lArm: {x: -2, y: 0, rot: -20}, legs: {x: 0, y: 0, rot: 10} },
    { frame: 7, head: {x: 3, y: 0, rot: 4}, torso: {x: 4, y: 0, rot: 6}, rArm: {x: 4, y: 0, rot: 45}, lArm: {x: 0, y: 0, rot: -10}, legs: {x: 0, y: 0, rot: 6} },
    { frame: 8, head: {x: 1, y: 0, rot: 2}, torso: {x: 2, y: 0, rot: 2}, rArm: {x: 2, y: 0, rot: 20}, lArm: {x: 0, y: 0, rot: -4}, legs: {x: 0, y: 0, rot: 2} },
    { frame: 9, head: {x: 0, y: 0, rot: 0}, torso: {x: 0, y: 0, rot: 0}, rArm: {x: 0, y: 0, rot: 0}, lArm: {x: 0, y: 0, rot: 0}, legs: {x: 0, y: 0, rot: 0} }
  ],
  skill: [
    { frame: 0, head: {x: 0, y: 2, rot: 4}, torso: {x: 0, y: 3, rot: 6}, rArm: {x: 0, y: 2, rot: -35}, lArm: {x: 0, y: 2, rot: 15}, legs: {x: 0, y: 2, rot: 6} },
    { frame: 1, head: {x: -2, y: -8, rot: -6}, torso: {x: -2, y: -8, rot: -8}, rArm: {x: -2, y: -8, rot: -95}, lArm: {x: -2, y: -8, rot: 30}, legs: {x: 0, y: -6, rot: -15} },
    { frame: 2, head: {x: -3, y: -16, rot: -10}, torso: {x: -3, y: -16, rot: -14}, rArm: {x: -3, y: -16, rot: -155}, lArm: {x: -3, y: -16, rot: 45}, legs: {x: 0, y: -12, rot: -24} },
    { frame: 3, head: {x: 2, y: -4, rot: 3}, torso: {x: 2, y: -4, rot: 4}, rArm: {x: 2, y: -4, rot: -60}, lArm: {x: 0, y: -4, rot: 0}, legs: {x: 0, y: -2, rot: 0} },
    { frame: 4, head: {x: 5, y: 6, rot: 18}, torso: {x: 6, y: 6, rot: 20}, rArm: {x: 6, y: 6, rot: 110}, lArm: {x: -3, y: 4, rot: -40}, legs: {x: 0, y: 4, rot: 14}, vfx: {show: true, x: 8, y: 10, rot: 90} },
    { frame: 5, head: {x: 6, y: 7, rot: 20}, torso: {x: 7, y: 7, rot: 22}, rArm: {x: 7, y: 7, rot: 125}, lArm: {x: -4, y: 5, rot: -45}, legs: {x: 0, y: 5, rot: 16}, vfx: {show: true, x: 12, y: 12, rot: 110} },
    { frame: 6, head: {x: 3, y: 4, rot: 14}, torso: {x: 4, y: 4, rot: 15}, rArm: {x: 4, y: 4, rot: 90}, lArm: {x: -2, y: 2, rot: -30}, legs: {x: 0, y: 3, rot: 10} },
    { frame: 7, head: {x: 2, y: 2, rot: 8}, torso: {x: 2, y: 2, rot: 8}, rArm: {x: 2, y: 2, rot: 50}, lArm: {x: 0, y: 1, rot: -15}, legs: {x: 0, y: 1, rot: 6} },
    { frame: 8, head: {x: 1, y: 1, rot: 3}, torso: {x: 1, y: 1, rot: 4}, rArm: {x: 1, y: 1, rot: 20}, lArm: {x: 0, y: 0, rot: -5}, legs: {x: 0, y: 0, rot: 2} },
    { frame: 9, head: {x: 0, y: 0, rot: 0}, torso: {x: 0, y: 0, rot: 0}, rArm: {x: 0, y: 0, rot: 0}, lArm: {x: 0, y: 0, rot: 0}, legs: {x: 0, y: 0, rot: 0} }
  ]
};

// 4. 게임 글로벌 상태값 (STATE)
const STATE = {
  gender: "female",
  unlockedRegion: 1,
  currentRad: 500,
  radCapacity: 1000,
  
  // 영구 훈련 능력치
  baseStats: {
    atk: 120,
    def: 30,
    traitPower: 0,
    maxHp: 1000,
    hp: 1000
  },
  
  // 전투 인게임 상태
  selectedRegion: 1,
  currentRound: 1, // 1~6라운드
  gameSpeed: 1,    // 1, 2, 4 배속
  renderMode: "pixel", // "pixel", "illustration", "parts"
  currentMotion: "idle",
  currentFrame: 0,

  // 인벤토리 & 장비
  equipped: {
    weapon: null,
    armor: null,
    accessory: null
  },
  inventory: [], // 최대 20개 슬롯 가방
  
  // 특성 슬롯 및 돌연변이 시스템 (사용자 설정: 슬롯 3개, 최초 1개만 개방 & 1개 보유, 2/3번 자물쇠 잠김)
  unlockedTraitSlots: 1, // 최초 1개 개방 (2번 마을 클리어 시 2, 3번 마을 클리어 시 3)
  equippedTraits: ["body_mutation", null, null], // 3개 특성 슬롯
  ownedTraits: ["body_mutation"], // 최초 1개 기본 특성 보유
  activeFusions: [],
  everestCleared: false,
  nemesisEvolved: false,
  activeAi: null,

  // 전투 데이터 & 특수 버프/상태
  combatRunning: false,
  playerHp: 1000,
  playerShield: 0,              // 하이테크 공학 및 이지스 배리어 나노 보호막
  cellularShieldCharges: 0,     // 세포 차폐 면역 배리어 잔여 횟수
  monsterBurns: [0, 0, 0],      // 열에너지 제어 적 화상 잔여 턴수
  monsterStuns: [false, false, false], // 초음파 교란 적 기절 여부
  monsterHps: [0, 0, 0],
  monsterMaxHps: [0, 0, 0],
  monsterParty: [],
  combatTimer: null,
  animTimer: null
};

// 5. 아이템 데이터베이스 및 제네레이터
const ITEM_NAMES = {
  weapon: ["조선 환도", "낙진 벌목용 도끼", "고주파 크리스탈 검", "전자기 중기관포", "용암 발사 런처"],
  armor: ["다포형 군복", "납 차폐 가죽 코트", "나노 카본 플레이트", "중성자 하드라이트 방패갑", "빅풋 예티 털외투"],
  accessory: ["방사선 계측 링", "전압 안정화 코일 목걸이", "초음파 공명 진동자", "네메시스 광학 고글", "핵융합 나노 코어"]
};

function generateRandomItem(regionLevel) {
  const slots = ["weapon", "armor", "accessory"];
  const slot = slots[Math.floor(Math.random() * slots.length)];
  const namePool = ITEM_NAMES[slot];
  const name = namePool[Math.floor(Math.random() * namePool.length)] + ` (Lv.${regionLevel})`;

  const rarities = ["common", "rare", "epic", "legendary"];
  const randVal = Math.random();
  let rarity = "common";
  let rarityMult = 1.0;
  if (randVal > 0.95) { rarity = "legendary"; rarityMult = 2.5; }
  else if (randVal > 0.8) { rarity = "epic"; rarityMult = 1.8; }
  else if (randVal > 0.5) { rarity = "rare"; rarityMult = 1.3; }

  const baseVal = regionLevel * 10;
  const statVal = Math.floor(baseVal * rarityMult * (0.8 + Math.random() * 0.4));
  
  let effectText = "";
  let stats = { atk: 0, def: 0, traitPower: 0, maxHp: 0 };
  if (slot === "weapon") {
    stats.atk = statVal;
    effectText = `공격력 +${statVal}`;
  } else if (slot === "armor") {
    stats.def = Math.floor(statVal / 3) + 1;
    stats.maxHp = statVal * 8;
    effectText = `방어력 +${stats.def}, 체력 +${stats.maxHp}`;
  } else {
    stats.traitPower = Math.floor(statVal / 4) + 1;
    stats.maxHp = statVal * 5;
    effectText = `특성력 +${stats.traitPower}, 체력 +${stats.maxHp}`;
  }

  return {
    id: "item_" + Math.random().toString(36).substr(2, 9),
    name: name,
    slot: slot,
    rarity: rarity,
    stats: stats,
    effectText: effectText,
    desc: `유라시아 챕터 ${regionLevel} 환경 낙진 수색 중 수집된 특수 장비입니다.`,
    cost: Math.floor(regionLevel * 60 * rarityMult)
  };
}

// 6. DOM 요소들
const DOM = {
  // Screens
  screens: {
    start: document.getElementById("screen-start"),
    map: document.getElementById("screen-map"),
    battle: document.getElementById("screen-battle"),
    town: document.getElementById("screen-town")
  },
  
  // Map
  mapCanvas: document.getElementById("mapCanvas"),
  modalRegionInfo: document.getElementById("modal-region-info"),
  regionInfoTitle: document.getElementById("region-info-title"),
  regionInfoEnv: document.getElementById("region-info-env"),
  regionInfoTrait: document.getElementById("region-info-trait"),
  regionMonsterList: document.getElementById("region-monster-list"),
  btnStartBattle: document.getElementById("btn-start-battle"),

  // Battle
  battleRegionText: document.getElementById("battle-region-text"),
  battleProgressText: document.getElementById("battle-progress-text"),
  btnGameSpeed: document.getElementById("btn-game-speed"),
  battleAgentHp: document.getElementById("battleAgentHp"),
  battleAgentHpText: document.getElementById("battleAgentHpText"),
  battleAgentAvatar: document.getElementById("battleAgentAvatar"),
  battleConsole: document.getElementById("battleConsole"),
  overlayClear: document.getElementById("overlay-clear"),
  clearRewardInfo: document.getElementById("clear-reward-info"),
  btnGoTown: document.getElementById("btn-go-town"),
  overlayDefeat: document.getElementById("overlay-defeat"),
  btnDefeatTown: document.getElementById("btn-defeat-town"),
  battleStageContainer: document.getElementById("battleStageContainer"),
  battleScreenFlash: document.getElementById("battleScreenFlash"),

  // Modals
  inventoryGrid: document.getElementById("inventoryGrid"),
  modalItemInfo: document.getElementById("modal-item-info"),
  itemInfoName: document.getElementById("item-info-name"),
  itemInfoImg: document.getElementById("item-info-img"),
  itemInfoRarity: document.getElementById("item-info-rarity"),
  itemInfoEffects: document.getElementById("item-info-effects"),
  itemInfoDesc: document.getElementById("item-info-desc"),
  btnItemEquip: document.getElementById("btn-item-equip"),
  btnItemDiscard: document.getElementById("btn-item-discard"),
  btnItemSell: document.getElementById("btn-item-sell"),

  // Stats upgrade
  statAtk: document.getElementById("stat-val-atk"),
  statDef: document.getElementById("stat-val-def"),
  statTrait: document.getElementById("stat-val-trait"),
  statHp: document.getElementById("stat-val-hp"),
  costUpAtk: document.getElementById("cost-up-atk"),
  costUpDef: document.getElementById("cost-up-def"),
  costUpTrait: document.getElementById("cost-up-trait"),
  costUpHp: document.getElementById("cost-up-hp"),
  btnUpAtk: document.getElementById("btn-up-atk"),
  btnUpDef: document.getElementById("btn-up-def"),
  btnUpTrait: document.getElementById("btn-up-trait"),
  btnUpHp: document.getElementById("btn-up-hp"),

  // Traits & Slots
  modalTraitsGrid: document.getElementById("modalTraitsGrid"),
  modalFusionList: document.getElementById("modalFusionList"),
  modalTraitCount: document.getElementById("modal-trait-count"),
  modalFusionCount: document.getElementById("modal-fusion-count"),
  unlockedSlotCounter: document.getElementById("unlocked-slot-counter"),
  traitSlotsGrid: document.getElementById("traitSlotsGrid"),
  activeFusionsBox: document.getElementById("activeFusionsBox"),
  activeFusionsList: document.getElementById("activeFusionsList"),
  labUnlockedSlotCounter: document.getElementById("lab-unlocked-slot-counter"),
  labTraitSlotsGrid: document.getElementById("labTraitSlotsGrid"),

  // Shop & Lab
  shopBuyGrid: document.getElementById("shopBuyGrid"),
  shopSellGrid: document.getElementById("shopSellGrid"),
  labTraitsGrid: document.getElementById("labTraitsGrid"),
  labFusionList: document.getElementById("labFusionList"),
  labNemesisStatus: document.getElementById("labNemesisStatus"),
  btnLabEvolveNemesis: document.getElementById("btnLabEvolveNemesis"),
  townRadValue: document.getElementById("town-rad-value")
};

// 7. 스크린 & 모달 제어
function showScreen(screenId) {
  Object.keys(DOM.screens).forEach(key => {
    if (key === screenId) {
      DOM.screens[key].classList.add("active");
    } else {
      DOM.screens[key].classList.remove("active");
    }
  });

  // 전투 퇴각 시 처리
  if (screenId !== "battle") {
    stopBattleLoop();
  } else {
    initBattleStage();
  }

  // 마을 정보 동기화
  if (screenId === "town") {
    DOM.townRadValue.textContent = STATE.currentRad;
  }
}

function openModal(modalId) {
  document.getElementById(modalId).classList.add("active");
  if (modalId === "modal-inventory") renderInventory();
  if (modalId === "modal-stats") renderStatsWindow();
  if (modalId === "modal-traits") renderTraitsWindow();
  if (modalId === "modal-shop") renderShopWindow();
  if (modalId === "modal-trait-lab") renderTraitLab();
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove("active");
}

// 8. 능력치 산출 엔진 (영구강화 + 인벤토리 장비 합산)
function getDerivedStats() {
  const derived = {
    atk: STATE.baseStats.atk,
    def: STATE.baseStats.def,
    traitPower: STATE.baseStats.traitPower,
    maxHp: STATE.baseStats.maxHp
  };

  // 장착 중인 무기, 방어구, 특수장비 보너스 합산
  Object.values(STATE.equipped).forEach(item => {
    if (item) {
      derived.atk += item.stats.atk;
      derived.def += item.stats.def;
      derived.traitPower += item.stats.traitPower;
      derived.maxHp += item.stats.maxHp;
    }
  });

  // 특성 슬롯 장착 스탯 효과
  // 1) 신체 변이: 공격력 +25%, 체력 +20%
  if (STATE.equippedTraits.includes("body_mutation")) {
    derived.atk += Math.floor(STATE.baseStats.atk * 0.25);
    derived.maxHp += Math.floor(STATE.baseStats.maxHp * 0.20);
  }
  // 2) 오염 동화: 보유 Rad 1000당 공격력 및 방어력 +15%
  if (STATE.equippedTraits.includes("radiation_assimilation")) {
    const scale = Math.floor(STATE.currentRad / 1000);
    derived.atk += Math.floor(STATE.baseStats.atk * 0.15 * scale);
    derived.def += Math.floor(STATE.baseStats.def * 0.15 * scale);
  }

  // 융합 시너지 스탯 효과
  // 키틴질 외골격: 방어력 +50%
  if (hasFusion("chitin_carapace")) {
    derived.def = Math.floor(derived.def * 1.50);
  }
  // 납-나노 차폐 코팅: 영구 방어력 +35%
  if (hasFusion("lead_nanite_coat")) {
    derived.def = Math.floor(derived.def * 1.35);
  }
  // 방사능 거신: 보유 Rad 1000당 추가 공/방 +15%
  if (hasFusion("nuclear_colossus")) {
    const scale = Math.floor(STATE.currentRad / 1000);
    derived.atk += Math.floor(STATE.baseStats.atk * 0.15 * scale);
    derived.def += Math.floor(STATE.baseStats.def * 0.15 * scale);
  }
  // 판데모니움 비스트: 올스탯 100% 폭증 (2배)
  if (hasFusion("pandemonium_beast")) {
    derived.atk = Math.floor(derived.atk * 2.0);
    derived.def = Math.floor(derived.def * 2.0);
    derived.traitPower = Math.floor(derived.traitPower * 2.0);
    derived.maxHp = Math.floor(derived.maxHp * 2.0);
  }
  // 감마선 버스트: Rad 1000당 탄막/스킬 위력 +20%
  if (hasFusion("gamma_ray_burst")) {
    const scale = Math.floor(STATE.currentRad / 1000);
    derived.traitPower += Math.floor(derived.traitPower * 0.20 * scale);
  }
  // 오로라 정령: Rad 1000당 스킬 위력 +25%
  if (hasFusion("aurora_fairy")) {
    const scale = Math.floor(STATE.currentRad / 1000);
    derived.traitPower += Math.floor(derived.traitPower * 0.25 * scale);
  }
  // 피폭의 광전사: Rad 1000당 공격력 +20%
  if (hasFusion("irradiated_berserker")) {
    const scale = Math.floor(STATE.currentRad / 1000);
    derived.atk += Math.floor(STATE.baseStats.atk * 0.20 * scale);
  }

  return derived;
}

// 9. 인벤토리 렌더링
function renderInventory() {
  const grid = DOM.inventoryGrid;
  grid.innerHTML = "";

  // 1) 상단 장착창 싱크
  const slots = ["weapon", "armor", "accessory"];
  slots.forEach(slot => {
    const slotBox = document.getElementById("slot-" + slot);
    const item = STATE.equipped[slot];
    if (item) {
      slotBox.className = `equip-slot-box rarity-${item.rarity}`;
      slotBox.innerHTML = `
        <span class="slot-placeholder">${slot.toUpperCase()}</span>
        <strong style="font-size: 0.72rem; text-align:center;">${item.name}</strong>
      `;
      slotBox.onclick = () => showItemInfoModal(item, true);
    } else {
      slotBox.className = "equip-slot-box";
      let label = "무기 빈칸";
      if (slot === "armor") label = "방어구 빈칸";
      if (slot === "accessory") label = "특수장비 빈칸";
      slotBox.innerHTML = `<span class="slot-placeholder">${label}</span>`;
      slotBox.onclick = null;
    }
  });

  // 2) 가방 그리드 렌더링 (5x4 = 20개 슬롯 채우기)
  for (let i = 0; i < 20; i++) {
    const slotEl = document.createElement("div");
    const item = STATE.inventory[i];
    if (item) {
      slotEl.className = `inv-slot rarity-${item.rarity}`;
      let icon = "item_weapon.png";
      if (item.slot === "armor") icon = "item_armor.png";
      if (item.slot === "accessory") icon = "item_accessory.png";
      
      slotEl.innerHTML = `<div class="item-icon-img" style="background-image: url('assets/ui/${icon}');"></div>`;
      slotEl.onclick = () => showItemInfoModal(item, false, i);
    } else {
      slotEl.className = "inv-slot empty";
    }
    grid.appendChild(slotEl);
  }
}

function showItemInfoModal(item, isEquipped, index = -1) {
  DOM.itemInfoName.textContent = item.name;
  DOM.itemInfoRarity.textContent = item.rarity.toUpperCase();
  DOM.itemInfoRarity.className = `item-rarity-badge rarity-${item.rarity}`;
  DOM.itemInfoEffects.textContent = item.effectText;
  DOM.itemInfoDesc.textContent = item.desc;
  
  let icon = "item_weapon.png";
  if (item.slot === "armor") icon = "item_armor.png";
  if (item.slot === "accessory") icon = "item_accessory.png";
  DOM.itemInfoImg.style.backgroundImage = `url('assets/ui/${icon}')`;

  // 액션 버튼 제어
  if (isEquipped) {
    DOM.btnItemEquip.textContent = "해제하기";
    DOM.btnItemEquip.onclick = () => {
      // 해제 후 가방으로 돌려놓기 (가방 남는 자리 있는지 검사)
      if (STATE.inventory.length >= 20) {
        alert("가방 공간이 부족합니다!");
        return;
      }
      STATE.equipped[item.slot] = null;
      STATE.inventory.push(item);
      closeModal("modal-item-info");
      renderInventory();
      writeBattleLog(`⚙️ 장비 해제: ${item.name}`, "system");
    };
  } else {
    DOM.btnItemEquip.textContent = "장착하기";
    DOM.btnItemEquip.onclick = () => {
      // 해당 슬롯 기존 장비는 가방으로 보내고 신규 장착
      const prevEquipped = STATE.equipped[item.slot];
      STATE.equipped[item.slot] = item;
      STATE.inventory.splice(index, 1);
      if (prevEquipped) {
        STATE.inventory.push(prevEquipped);
      }
      closeModal("modal-item-info");
      renderInventory();
      writeBattleLog(`🛡️ 장비 장착: ${item.name}`, "system");
    };
  }

  // 버리기 버튼
  DOM.btnItemDiscard.onclick = () => {
    if (confirm("정말 버리시겠습니까?")) {
      if (isEquipped) {
        STATE.equipped[item.slot] = null;
      } else {
        STATE.inventory.splice(index, 1);
      }
      closeModal("modal-item-info");
      renderInventory();
      writeBattleLog(`🗑️ 장비 파기: ${item.name}`, "warning");
    }
  };

  // 판매하기 대응 (상점이 켜져 있는 상황 대응)
  const isShopOpen = document.getElementById("modal-shop").classList.contains("active");
  if (isShopOpen && !isEquipped) {
    DOM.btnItemSell.style.display = "block";
    DOM.btnItemSell.textContent = `판매하기 (+${item.cost} Rad)`;
    DOM.btnItemSell.onclick = () => {
      STATE.currentRad += item.cost;
      STATE.inventory.splice(index, 1);
      closeModal("modal-item-info");
      renderInventory();
      renderShopWindow();
      DOM.townRadValue.textContent = STATE.currentRad;
      writeBattleLog(`💰 장비 판매: ${item.name} (+${item.cost} Rad)`, "system");
    };
  } else {
    DOM.btnItemSell.style.display = "none";
  }

  openModal("modal-item-info");
}

// 10. 능력치 강화 렌더링
function renderStatsWindow() {
  const stats = getDerivedStats();
  DOM.statAtk.textContent = stats.atk;
  DOM.statDef.textContent = stats.def;
  DOM.statTrait.textContent = stats.traitPower;
  DOM.statHp.textContent = `${STATE.baseStats.hp}/${stats.maxHp}`;

  // 강화 비용 공식: 해당 스탯 / 5 * 100
  const costAtk = Math.floor(STATE.baseStats.atk / 10) * 80;
  const costDef = Math.floor(STATE.baseStats.def) * 40;
  const costTrait = (STATE.baseStats.traitPower + 1) * 150;
  const costHp = Math.floor(STATE.baseStats.maxHp / 100) * 80;

  DOM.costUpAtk.textContent = `${costAtk} Rad`;
  DOM.costUpDef.textContent = `${costDef} Rad`;
  DOM.costUpTrait.textContent = `${costTrait} Rad`;
  DOM.costUpHp.textContent = `${costHp} Rad`;

  DOM.btnUpAtk.onclick = () => upgradeStat("atk", costAtk, 15);
  DOM.btnUpDef.onclick = () => upgradeStat("def", costDef, 4);
  DOM.btnUpTrait.onclick = () => upgradeStat("traitPower", costTrait, 1);
  DOM.btnUpHp.onclick = () => upgradeStat("maxHp", costHp, 150);
}

function upgradeStat(statName, cost, increaseAmount) {
  if (STATE.currentRad >= cost) {
    STATE.currentRad -= cost;
    STATE.baseStats[statName] += increaseAmount;
    if (statName === "maxHp") {
      // 체력 상승 시 현재 체력도 비율 증가
      STATE.baseStats.hp += increaseAmount;
    }
    renderStatsWindow();
    if (DOM.townRadValue) DOM.townRadValue.textContent = STATE.currentRad;
    writeBattleLog(`🔥 영구 신체 훈련 완료! [${statName}] 증가`, "system");
  } else {
    alert("소지한 Rad 광석이 부족합니다!");
  }
}

// === 10-1. 특성 슬롯 및 돌연변이 제어 헬퍼 함수 ===
function hasEquipped(traitId) {
  return STATE.equippedTraits.includes(traitId);
}

function hasFusion(fusionId) {
  return STATE.activeFusions.includes(fusionId);
}

function getActiveMutationParts() {
  const parts = new Set();
  STATE.equippedTraits.forEach(traitId => {
    if (traitId && TRAIT_MUTATIONS[traitId]) {
      parts.add(TRAIT_MUTATIONS[traitId]);
    }
  });
  return Array.from(parts);
}

function getActiveAuraStage() {
  const count = STATE.equippedTraits.filter(t => t !== null).length;
  if (count >= 3) return 2; // 진홍/보라 코스믹 폭주 오라
  if (count >= 2) return 1; // 청록 방사능 오라
  return 0; // 없음
}

function getPairFusion(t1, t2) {
  if (!t1 || !t2 || t1 === t2) return null;
  return Object.values(FUSION_DATA).find(f => 
    (f.req[0] === t1 && f.req[1] === t2) || (f.req[0] === t2 && f.req[1] === t1)
  ) || null;
}

function checkActiveFusions() {
  STATE.activeFusions = [];
  const s0 = STATE.equippedTraits[0];
  const s1 = STATE.equippedTraits[1];
  const s2 = STATE.equippedTraits[2];

  const equippedCount = [s0, s1, s2].filter(t => t !== null).length;

  if (equippedCount === 2) {
    // 2개 장착 시: 장착된 2개 특성 간의 2중 융합 1개 발동
    const valid = [s0, s1, s2].filter(t => t !== null);
    const f = getPairFusion(valid[0], valid[1]);
    if (f && !STATE.activeFusions.includes(f.id)) {
      STATE.activeFusions.push(f.id);
    }
  } else if (equippedCount === 3) {
    // 3개 장착 시: 슬롯 1+2 융합 및 슬롯 2+3 융합 (총 2개의 2중 융합 동시 발동!)
    const f1 = getPairFusion(s0, s1);
    const f2 = getPairFusion(s1, s2);
    if (f1 && !STATE.activeFusions.includes(f1.id)) STATE.activeFusions.push(f1.id);
    if (f2 && !STATE.activeFusions.includes(f2.id)) STATE.activeFusions.push(f2.id);
  }
}

function equipTrait(traitId) {
  if (!traitId || !TRAITS_DATA[traitId]) return;
  if (!STATE.ownedTraits.includes(traitId)) {
    writeBattleLog(`⚠️ [미보유 특성] 해당 특성을 먼저 연구/해금해야 합니다.`, "warning");
    return;
  }
  if (STATE.equippedTraits.includes(traitId)) {
    writeBattleLog(`ℹ️ 이미 장착 중인 특성입니다.`, "system");
    return;
  }

  // 첫 번째 빈 개방 슬롯 탐색
  let targetSlot = -1;
  for (let i = 0; i < STATE.unlockedTraitSlots; i++) {
    if (STATE.equippedTraits[i] === null) {
      targetSlot = i;
      break;
    }
  }

  if (targetSlot === -1) {
    alert(`모든 개방 슬롯(${STATE.unlockedTraitSlots}개)이 가득 찼습니다!\n기존 슬롯을 클릭해 해제한 후 다시 장착해 주십시오.`);
    return;
  }

  STATE.equippedTraits[targetSlot] = traitId;
  checkActiveFusions();
  const trait = TRAITS_DATA[traitId];
  const partName = TRAIT_PART_NAMES[TRAIT_MUTATIONS[traitId]] || "돌연변이";
  writeBattleLog(`🧬 [특성 장착] 슬롯 ${targetSlot + 1}에 [${trait.name}] 장착 완료! (신체 파츠: ${partName} 발현)`, "system");

  if (STATE.activeFusions.length > 0) {
    writeBattleLog(`⚡ [초월 융합 발동] ${STATE.activeFusions.length}개의 특성 시너지가 활성화되었습니다!`, "warning");
  }

  renderTraitsWindow();
  renderTraitLab();
}

function unequipTraitSlot(slotIdx) {
  if (slotIdx >= STATE.unlockedTraitSlots) return;
  const oldTrait = STATE.equippedTraits[slotIdx];
  if (!oldTrait) return;

  STATE.equippedTraits[slotIdx] = null;
  checkActiveFusions();
  writeBattleLog(`🧬 [특성 해제] 슬롯 ${slotIdx + 1}의 [${TRAITS_DATA[oldTrait].name}] 해제 완료.`, "system");

  renderTraitsWindow();
  renderTraitLab();
}

function renderTraitSlotsUI(gridId, counterId, fusionBoxId, fusionCountId, fusionListId) {
  const grid = document.getElementById(gridId);
  if (!grid) return;

  const counter = document.getElementById(counterId);
  if (counter) {
    counter.textContent = `${STATE.unlockedTraitSlots}/3 개방`;
  }

  grid.innerHTML = "";
  for (let i = 0; i < 3; i++) {
    const isLocked = (i >= STATE.unlockedTraitSlots);
    const traitId = STATE.equippedTraits[i];
    const card = document.createElement("div");

    if (isLocked) {
      card.className = "trait-slot-card locked";
      const unlockCond = (i === 1) ? "지역 2(서유럽) 클리어 시 해금" : "지역 3(동아시아) 클리어 시 해금";
      card.innerHTML = `
        <div class="slot-lock-icon">🔒</div>
        <div class="slot-lock-title">슬롯 ${i + 1} 잠김</div>
        <div class="slot-lock-condition">${unlockCond}</div>
      `;
    } else if (traitId) {
      const trait = TRAITS_DATA[traitId];
      const partKey = TRAIT_MUTATIONS[traitId];
      const partName = TRAIT_PART_NAMES[partKey] || "돌연변이";
      card.className = "trait-slot-card equipped";
      card.innerHTML = `
        <div class="slot-trait-name">${trait.name}</div>
        <div class="slot-part-badge">🧬 ${partName}</div>
        <div class="slot-unequip-tag">클릭 시 해제 ✖</div>
      `;
      card.onclick = () => unequipTraitSlot(i);
    } else {
      card.className = "trait-slot-card empty";
      card.innerHTML = `
        <div class="slot-placeholder-title">+ 슬롯 ${i + 1} 비어있음</div>
        <div class="slot-placeholder-desc">아래 보유 특성을 클릭해 장착</div>
      `;
    }
    grid.appendChild(card);
  }

  // 활성 융합 배너 갱신
  if (fusionCountId) {
    const countEl = document.getElementById(fusionCountId);
    if (countEl) countEl.textContent = STATE.activeFusions.length;
  }
  if (fusionListId) {
    const listEl = document.getElementById(fusionListId);
    if (listEl) {
      listEl.innerHTML = "";
      if (STATE.activeFusions.length === 0) {
        listEl.innerHTML = `<span class="no-fusions-text">장착된 특성 간 활성화된 2중 융합이 없습니다. 2개 이상의 특성을 조합해 보십시오. (총 78종 2중 융합 지원)</span>`;
      } else {
        STATE.activeFusions.forEach((fId, idx) => {
          const fusion = FUSION_DATA[fId];
          if (fusion) {
            const reqNames = fusion.req.map(rId => TRAITS_DATA[rId] ? TRAITS_DATA[rId].name : rId).join(" + ");
            const slotTag = (STATE.equippedTraits.filter(t=>t).length === 3) 
              ? `<span style="font-size:0.65rem; color:#facc15; margin-right:4px;">[융합 ${idx + 1}]</span>` 
              : '';
            const item = document.createElement("div");
            item.className = "active-fusion-item";
            item.innerHTML = `
              <div class="f-name">⚡ ${slotTag}${fusion.name} <span style="font-size:0.68rem; color:#38bdf8; font-weight:normal;">(${reqNames})</span></div>
              <div class="f-desc">${fusion.description}</div>
            `;
            listEl.appendChild(item);
          }
        });
      }
    }
  }
}

// 11. 특성 및 융합 상태창 렌더링
function renderTraitsWindow() {
  checkActiveFusions();
  DOM.modalTraitCount.textContent = `${STATE.ownedTraits.length}/13`;
  DOM.modalFusionCount.textContent = `${STATE.activeFusions.length}/78`;

  // 1) 3개 슬롯 UI 렌더
  renderTraitSlotsUI("traitSlotsGrid", "unlocked-slot-counter", "activeFusionsBox", "modal-fusion-count", "activeFusionsList");

  // 2) 13대 고유 특성 칩셋 그리드 렌더
  const grid = DOM.modalTraitsGrid;
  grid.innerHTML = "";
  Object.values(TRAITS_DATA).forEach(trait => {
    const isAcquired = STATE.ownedTraits.includes(trait.id);
    const isSlotted = STATE.equippedTraits.includes(trait.id);
    const partName = TRAIT_PART_NAMES[TRAIT_MUTATIONS[trait.id]] || "돌연변이";

    const item = document.createElement("div");
    item.className = `trait-item-chip ${isAcquired ? 'acquired' : ''} ${isSlotted ? 'is-slotted' : ''}`;
    
    let statusBadge = isSlotted 
      ? `<span class="slotted-badge">장착 중</span>` 
      : (isAcquired ? `<span style="font-size:0.6rem; color:#4ade80;">[장착 가능]</span>` : `<span style="font-size:0.6rem; color:#94a3b8;">[미보유]</span>`);

    item.innerHTML = `
      <span class="category">${trait.category}</span>
      <strong>${trait.name}</strong>
      <div style="font-size:0.6rem; color:#7dd3fc; margin-top:2px;">🧬 ${partName}</div>
      ${statusBadge}
    `;

    item.title = trait.description;
    item.onclick = () => {
      if (!isAcquired) {
        alert(`[${trait.name}]\n${trait.description}\n\n* 획득처: 지역 ${trait.region} 클리어 또는 마을 특성진화소에서 연구 가능`);
      } else if (isSlotted) {
        const slotIdx = STATE.equippedTraits.indexOf(trait.id);
        unequipTraitSlot(slotIdx);
      } else {
        equipTrait(trait.id);
      }
    };
    grid.appendChild(item);
  });

  // 3) 78종 융합 도감 리스트 렌더 (발동 중인 융합을 최상단에 우선 정렬)
  const fList = DOM.modalFusionList;
  fList.innerHTML = "";
  const sortedFusions = Object.values(FUSION_DATA).slice().sort((a, b) => {
    const aActive = STATE.activeFusions.includes(a.id) ? 1 : 0;
    const bActive = STATE.activeFusions.includes(b.id) ? 1 : 0;
    return bActive - aActive;
  });

  sortedFusions.forEach(fusion => {
    const isActive = STATE.activeFusions.includes(fusion.id);
    const reqNames = fusion.req.map(rId => TRAITS_DATA[rId] ? TRAITS_DATA[rId].name : rId).join(" + ");
    const item = document.createElement("div");
    item.className = `fusion-item-chip ${isActive ? 'active' : ''}`;
    item.innerHTML = `
      <div class="f-title">${isActive ? '⚡ [발동 중] ' : ''}${fusion.name} <span style="font-size:0.7rem; color:#38bdf8;">(${reqNames})</span></div>
      <div>${fusion.description}</div>
    `;
    fList.appendChild(item);
  });
}

// 12. 마을 상점 시스템
let shopBuyItems = [];
function renderShopWindow() {
  // 상점 탭 전환
  const tabBuy = DOM.shopBuyGrid.parentNode;
  const tabSell = document.getElementById("panel-shop-sell");
  
  document.getElementById("tab-shop-buy").onclick = () => {
    tabBuy.style.display = "block";
    tabSell.style.display = "none";
    document.getElementById("tab-shop-buy").classList.add("active");
    document.getElementById("tab-shop-sell").classList.remove("active");
  };

  document.getElementById("tab-shop-sell").onclick = () => {
    tabBuy.style.display = "none";
    tabSell.style.display = "block";
    document.getElementById("tab-shop-buy").classList.remove("active");
    document.getElementById("tab-shop-sell").classList.add("active");
    renderShopSellGrid();
  };

  // 구매용 보급품 생성 (상점 열릴 때 1회 로드)
  if (shopBuyItems.length === 0) {
    refreshShopSupply();
  }

  const buyGrid = DOM.shopBuyGrid;
  buyGrid.innerHTML = "";
  shopBuyItems.forEach((item, i) => {
    const card = document.createElement("div");
    card.className = `shop-item-card rarity-${item.rarity}`;
    let icon = "item_weapon.png";
    if (item.slot === "armor") icon = "item_armor.png";
    if (item.slot === "accessory") icon = "item_accessory.png";

    card.innerHTML = `
      <div class="item-image-large" style="width:50px; height:50px; background-image: url('assets/ui/${icon}')"></div>
      <div class="shop-item-info">
        <span class="shop-item-name">${item.name}</span>
        <span class="shop-item-cost">💰 가격: ${item.cost} Rad</span>
      </div>
    `;
    card.onclick = () => buyShopItem(item, i);
    buyGrid.appendChild(card);
  });
}

function refreshShopSupply() {
  shopBuyItems = [];
  // 현재 맵 해금된 지역 레벨 기준으로 아이템 4종 리스폰
  for (let i = 0; i < 4; i++) {
    shopBuyItems.push(generateRandomItem(STATE.unlockedRegion));
  }
}

function buyShopItem(item, index) {
  if (STATE.currentRad >= item.cost) {
    if (STATE.inventory.length >= 20) {
      alert("가방 가득 참!");
      return;
    }
    STATE.currentRad -= item.cost;
    STATE.inventory.push(item);
    shopBuyItems.splice(index, 1); // 상점에서 제거
    renderShopWindow();
    DOM.townRadValue.textContent = STATE.currentRad;
    writeBattleLog(`🏪 상점 보급 구매 성공: ${item.name}`, "system");
  } else {
    alert("Rad가 부족합니다!");
  }
}

function renderShopSellGrid() {
  const sellGrid = document.getElementById("shopSellGrid");
  sellGrid.innerHTML = "";
  for (let i = 0; i < 20; i++) {
    const slotEl = document.createElement("div");
    const item = STATE.inventory[i];
    if (item) {
      slotEl.className = `inv-slot rarity-${item.rarity}`;
      let icon = "item_weapon.png";
      if (item.slot === "armor") icon = "item_armor.png";
      if (item.slot === "accessory") icon = "item_accessory.png";
      slotEl.innerHTML = `<div class="item-icon-img" style="background-image: url('assets/ui/${icon}');"></div>`;
      // 클릭 시 판매 전용 상세 팝업
      slotEl.onclick = () => showItemInfoModal(item, false, i);
    } else {
      slotEl.className = "inv-slot empty";
    }
    sellGrid.appendChild(slotEl);
  }
}

// 13. 특성 진화소 개조 연구실 (마을)
function renderTraitLab() {
  checkActiveFusions();

  // 1) 연구소 내 슬롯 UI 동적 렌더
  renderTraitSlotsUI("labTraitSlotsGrid", "lab-unlocked-slot-counter");

  // 2) 13대 특성 칩셋 동적 렌더링
  const grid = DOM.labTraitsGrid;
  grid.innerHTML = "";

  Object.values(TRAITS_DATA).forEach(trait => {
    const isAcquired = STATE.ownedTraits.includes(trait.id);
    const isSlotted = STATE.equippedTraits.includes(trait.id);
    const partName = TRAIT_PART_NAMES[TRAIT_MUTATIONS[trait.id]] || "돌연변이";

    const chip = document.createElement("div");
    chip.className = `trait-item-chip ${isAcquired ? 'acquired' : ''} ${isSlotted ? 'is-slotted' : ''}`;
    
    let actionBadge = isSlotted 
      ? '<span class="slotted-badge">장착 중</span>' 
      : (isAcquired ? '<span style="font-size:0.6rem; color:#4ade80;">[장착하기]</span>' : '<span style="font-size:0.6rem; color:#facc15;">[연구: 250 Rad]</span>');

    chip.innerHTML = `
      <span class="category">${trait.category}</span>
      <strong>${trait.name}</strong>
      <div style="font-size:0.6rem; color:#7dd3fc; margin-top:2px;">🧬 ${partName}</div>
      ${actionBadge}
    `;
    chip.title = trait.description;
    chip.onclick = () => toggleTraitLab(trait.id);
    grid.appendChild(chip);
  });

  // 3) 78종 융합 칩 동적 출력 (발동 중인 융합을 최상단에 우선 정렬)
  const fList = DOM.labFusionList;
  fList.innerHTML = "";
  const sortedFusions = Object.values(FUSION_DATA).slice().sort((a, b) => {
    const aActive = STATE.activeFusions.includes(a.id) ? 1 : 0;
    const bActive = STATE.activeFusions.includes(b.id) ? 1 : 0;
    return bActive - aActive;
  });

  sortedFusions.forEach(fusion => {
    const isActive = STATE.activeFusions.includes(fusion.id);
    const reqNames = fusion.req.map(rId => TRAITS_DATA[rId] ? TRAITS_DATA[rId].name : rId).join(" + ");
    const item = document.createElement("div");
    item.className = `fusion-item-chip ${isActive ? 'active' : ''}`;
    item.innerHTML = `
      <div class="f-title">${isActive ? '⚡ [활성] ' : ''}${fusion.name} <span style="font-size:0.7rem; color:#38bdf8;">(${reqNames})</span></div>
      <div>${fusion.description}</div>
    `;
    fList.appendChild(item);
  });

  // 4) 네메시스 승화 자격 판정
  const isEverest = STATE.everestCleared;
  const activeFusionsCount = STATE.activeFusions.length;
  // 네메시스 해금 조건: 에베레스트 클리어 및 융합 2종 활성화 (3슬롯 장착)
  const isUnlocked = isEverest && activeFusionsCount >= 2;

  if (STATE.nemesisEvolved) {
    DOM.labNemesisStatus.textContent = "⚡ 네메시스 주신 최종 승화 강림 완료 (몬스터화 면역)";
    document.getElementById("btnLabEvolveNemesis").textContent = "네메시스 승화 해제";
    document.getElementById("btnLabEvolveNemesis").disabled = false;
    document.getElementById("btnLabEvolveNemesis").classList.add("active");
  } else if (isUnlocked) {
    DOM.labNemesisStatus.textContent = "🔓 승화 강림 조건 달성! 최종 승화 준비 완료 (비용: 1200 Rad)";
    document.getElementById("btnLabEvolveNemesis").disabled = false;
    document.getElementById("btnLabEvolveNemesis").classList.remove("active");
  } else {
    DOM.labNemesisStatus.textContent = `🔒 잠김 (조건: 에베레스트 완파 + 2중 융합 시너지 2종 활성화 [현재: ${activeFusionsCount}/2])`;
    document.getElementById("btnLabEvolveNemesis").disabled = true;
    document.getElementById("btnLabEvolveNemesis").classList.remove("active");
  }
}

function toggleTraitLab(id) {
  const trait = TRAITS_DATA[id];
  const isAcquired = STATE.ownedTraits.includes(id);
  const isSlotted = STATE.equippedTraits.includes(id);

  if (!isAcquired) {
    // 특성 연구 구매
    if (STATE.currentRad >= trait.radCost) {
      STATE.ownedTraits.push(id);
      STATE.currentRad -= trait.radCost;
      writeBattleLog(`🧪 [특성 연구 완료] ${trait.name} 유전자 연구 성공 (-${trait.radCost} Rad)`, "system");
      // 빈 슬롯이 있으면 즉시 장착
      equipTrait(id);
    } else {
      alert("Rad 광석이 부족합니다! (연구 비용: " + trait.radCost + " Rad 필요)");
    }
  } else if (isSlotted) {
    // 이미 슬롯에 장착 중인 경우 클릭 시 슬롯 해제
    const slotIdx = STATE.equippedTraits.indexOf(id);
    unequipTraitSlot(slotIdx);
  } else {
    // 보유 중이고 슬롯에 미장착인 경우 슬롯 장착 시도
    equipTrait(id);
  }

  DOM.townRadValue.textContent = STATE.currentRad;
  renderTraitLab();
}

function refreshFusions() {
  checkActiveFusions();
}

// 네메시스 이벤트 바인딩
document.getElementById("btnLabEvolveNemesis").onclick = () => {
  if (STATE.nemesisEvolved) {
    STATE.nemesisEvolved = false;
    STATE.currentRad += 1200;
    writeBattleLog(`🌌 네메시스 주신 승화 해제 (+1200 Rad)`, "warning");
  } else {
    if (STATE.currentRad >= 1200) {
      STATE.nemesisEvolved = true;
      STATE.currentRad -= 1200;
      writeBattleLog(`⚡ 7성 주신 네메시스(Nemesis) 승화 강림 완료!`, "system");
    } else {
      alert("Rad 광석이 부족합니다!");
    }
  }
  DOM.townRadValue.textContent = STATE.currentRad;
  renderTraitLab();
};

// 14. 유라시아 전역 지도 거점 렌더링
function renderWorldMapPins() {
  const mapCanvas = DOM.mapCanvas;
  // 기존 핀 제거 후 신규 배치
  mapCanvas.querySelectorAll(".map-pin").forEach(el => el.remove());

  Object.entries(REGIONS_METADATA).forEach(([idStr, region]) => {
    const id = parseInt(idStr);
    const pin = document.createElement("div");
    
    let stateClass = "locked";
    if (id <= STATE.unlockedRegion) {
      stateClass = (id < STATE.unlockedRegion) ? "cleared" : "unlocked";
    }

    pin.className = `map-pin ${stateClass}`;
    pin.style.left = `${region.coords.x}%`;
    pin.style.top = `${region.coords.y}%`;
    pin.textContent = id;
    
    if (stateClass !== "locked") {
      pin.onclick = () => showRegionInfoModal(id);
    } else {
      pin.onclick = () => alert("이전 챕터를 격퇴하여 지도를 개방하십시오.");
    }

    mapCanvas.appendChild(pin);
  });
}

function showRegionInfoModal(regionId) {
  STATE.selectedRegion = regionId;
  const region = REGIONS_METADATA[regionId];
  
  DOM.regionInfoTitle.textContent = `${regionId}. ${region.name}`;
  DOM.regionInfoEnv.textContent = region.env;
  
  const traitDetails = TRAITS_DATA[region.trait];
  DOM.regionInfoTrait.textContent = traitDetails ? `${traitDetails.name} (${traitDetails.description})` : "네메시스 최종 구역";

  // 몬스터 목록 썸네일 노출
  const mList = DOM.regionMonsterList;
  mList.innerHTML = "";
  const monsters = MONSTERS_DATABASE[regionId] || MONSTERS_DATABASE[1];
  
  monsters.forEach(m => {
    const thumb = document.createElement("div");
    thumb.className = "monster-thumb";
    thumb.title = `${m.name} (HP: ${m.hp}, ATK: ${m.atk})`;
    thumb.style.backgroundImage = `url('${m.img}')`;
    
    // 로드 실패 시 폴백
    const imgLoader = new Image();
    imgLoader.src = m.img;
    imgLoader.onerror = () => {
      let fallback = "assets/monsters/m_1_1.png";
      if (m.type === "named") fallback = "assets/monsters/m_1_named.png";
      if (m.type === "boss") fallback = "assets/monsters/m_1_boss.png";
      thumb.style.backgroundImage = `url('${fallback}')`;
    };

    mList.appendChild(thumb);
  });

  // 전투 집입 바인딩
  DOM.btnStartBattle.onclick = () => {
    closeModal("modal-region-info");
    STATE.currentRound = 1;
    showScreen("battle");
  };

  openModal("modal-region-info");
}

// 14-1. 장착 장비 비주얼 매핑 (페이퍼돌 시스템)
function getEquippedVisualKeys() {
  let weaponKey = "katana";
  if (STATE.equipped.weapon) {
    const wName = STATE.equipped.weapon.name;
    if (wName.includes("도끼")) weaponKey = "axe";
    else if (wName.includes("크리스탈")) weaponKey = "crystal_sword";
    else if (wName.includes("기관포")) weaponKey = "heavy_cannon";
    else if (wName.includes("런처")) weaponKey = "lava_launcher";
  }
  let armorKey = null;
  if (STATE.equipped.armor) {
    const aName = STATE.equipped.armor.name;
    if (aName.includes("군복")) armorKey = "military";
    else if (aName.includes("가죽")) armorKey = "leather";
    else if (aName.includes("카본")) armorKey = "nano_carbon";
    else if (aName.includes("하드라이트")) armorKey = "hardlight";
    else if (aName.includes("예티")) armorKey = "yeti_fur";
  }
  return { weaponKey, armorKey };
}

// 14-2. 프리뷰 아바타 (마을, 인벤토리, 스탯창) 실시간 동기화
function updatePreviewAvatars(genderSuffix, isNemesis, weaponKey, armorKey, fIdx) {
  let bodyPath, armorPath = null, weaponPath = null;
  if (isNemesis) {
    bodyPath = `assets/pixel_hero/${genderSuffix}_nemesis_idle_${fIdx}.png`;
  } else {
    bodyPath = `assets/pixel_hero/${genderSuffix}_idle_${fIdx}.png`;
    if (armorKey) {
      const aPrefix = genderSuffix === "female" ? `female_${armorKey}` : armorKey;
      armorPath = `assets/pixel_hero/armors/${aPrefix}_idle_${fIdx}.png`;
    }
    weaponPath = `assets/pixel_hero/weapons/${weaponKey}_idle_${fIdx}.png`;
  }

  const activeParts = getActiveMutationParts();
  const auraStage = getActiveAuraStage();
  const allParts = [
    "wings", "fairy_wings", "tail", "booster", "shell", "crystals",
    "core", "horns", "spikes", "visor", "antennae", "halo", "claws"
  ];
  const targets = ["town", "inv", "stats"];

  for (const t of targets) {
    const elBody = document.getElementById(`${t}-layer-body`);
    const elArmor = document.getElementById(`${t}-layer-armor`);
    const elWeapon = document.getElementById(`${t}-layer-weapon`);
    const elAura = document.getElementById(`${t}-layer-aura`);

    if (elBody) {
      elBody.style.backgroundImage = `url('${bodyPath}')`;
    }
    if (elArmor) {
      if (armorPath) {
        elArmor.style.display = "block";
        elArmor.style.backgroundImage = `url('${armorPath}')`;
      } else {
        elArmor.style.display = "none";
      }
    }
    if (elWeapon) {
      if (weaponPath) {
        elWeapon.style.display = "block";
        elWeapon.style.backgroundImage = `url('${weaponPath}')`;
      } else {
        elWeapon.style.display = "none";
      }
    }

    // 오라 이펙트 (2개: aura-stage-1, 3개: aura-stage-2)
    if (elAura) {
      elAura.classList.remove("aura-stage-1", "aura-stage-2");
      if (auraStage === 1) elAura.classList.add("aura-stage-1");
      else if (auraStage === 2) elAura.classList.add("aura-stage-2");
    }

    // 돌연변이 파츠 레이어 (horns, wings, tail, core, visor)
    allParts.forEach(p => {
      const elPart = document.getElementById(`${t}-layer-${p}`);
      if (elPart) {
        if (activeParts.includes(p)) {
          elPart.style.display = "block";
          elPart.style.backgroundImage = `url('assets/pixel_hero/mutations/${p}_idle_${fIdx}.png')`;
        } else {
          elPart.style.display = "none";
        }
      }
    });
  }

  const charTag = document.getElementById("statsCharRole");
  if (charTag) {
    if (isNemesis) charTag.textContent = "🔥 네메시스 각성체 (Nemesis)";
    else if (armorKey && STATE.equipped.armor) charTag.textContent = `전투원 (${STATE.equipped.armor.name.split(" ")[0]})`;
    else charTag.textContent = "생존자 / 베이스 훈련생";
  }
}

// 15. 16비트 아케이드 애니메이션 루프 구동
function startAnimationLoop() {
  if (STATE.animTimer) clearInterval(STATE.animTimer);
  
  const tickDuration = 200 / STATE.gameSpeed; // 배속에 비례해 단축 (기존 100ms -> 200ms 절반 감속)
  
  STATE.animTimer = setInterval(() => {
    // 0~9 프레임 순환
    STATE.currentFrame = (STATE.currentFrame + 1) % 10;
    
    // 모션별 애니메이션 분기
    const frames = ANIMATION_METADATA[STATE.currentMotion] || ANIMATION_METADATA.idle;
    const fData = frames[STATE.currentFrame] || frames[0];

    const battleScreen = document.getElementById("screen-battle");
    const isNemesis = STATE.nemesisEvolved;
    const genderSuffix = STATE.gender === "female" ? "female" : "male";
    const { weaponKey, armorKey } = getEquippedVisualKeys();

    // 마을, 스탯창, 인벤토리 프리뷰 동기화
    const idleFIdx = STATE.currentFrame % 4;
    updatePreviewAvatars(genderSuffix, isNemesis, weaponKey, armorKey, idleFIdx);

    // 각 파츠 돔 갱신
    const pHead = document.getElementById("battle-head");
    const pTorso = document.getElementById("battle-torso");
    const pRArm = document.getElementById("battle-r-arm");
    const pLArm = document.getElementById("battle-l-arm");
    const pLegs = document.getElementById("battle-legs");
    const pVfx = document.getElementById("battle-slash-vfx");

    if (pHead && pTorso && pRArm && pLArm && pLegs) {
      const h = fData.head || {x: 0, y: 0, rot: 0};
      const t = fData.torso || {x: 0, y: 0, rot: 0};
      const ra = fData.rArm || {x: 0, y: 0, rot: 0};
      const la = fData.lArm || {x: 0, y: 0, rot: 0};
      const l = fData.legs || {x: 0, y: 0, rot: 0};

      if (STATE.renderMode === "pixel") {
        if (battleScreen) battleScreen.classList.add("pixel-mode");
        DOM.battleAgentAvatar.classList.remove("parts-mode");

        // 부품 개별 블록 숨김 처리 (완성형 던파 액션 스프라이트로 렌더)
        pHead.style.display = "none";
        pTorso.style.display = "none";
        pRArm.style.display = "none";
        pLArm.style.display = "none";
        pLegs.style.display = "none";
        if (pVfx) pVfx.style.display = "none";

        // 모션별 프레임 수 연산
        let motion = STATE.currentMotion || "idle";
        let frameCount = 4;
        if (motion === "run") frameCount = 6;
        else if (motion === "attack") frameCount = 4;
        else if (motion === "skill") frameCount = 4;

        const fIdx = STATE.currentFrame % frameCount;

        // 16비트 레트로 페이퍼돌 레이어 패스 연산
        let bodyPath, armorPath = null, weaponPath = null;
        if (isNemesis) {
          bodyPath = `assets/pixel_hero/${genderSuffix}_nemesis_${motion}_${fIdx}.png`;
        } else {
          bodyPath = `assets/pixel_hero/${genderSuffix}_${motion}_${fIdx}.png`;
          if (armorKey) {
            const aPrefix = genderSuffix === "female" ? `female_${armorKey}` : armorKey;
            armorPath = `assets/pixel_hero/armors/${aPrefix}_${motion}_${fIdx}.png`;
          }
          weaponPath = `assets/pixel_hero/weapons/${weaponKey}_${motion}_${fIdx}.png`;
        }

        const lBody = document.getElementById("pixel-layer-body");
        const lArmor = document.getElementById("pixel-layer-armor");
        const lWeapon = document.getElementById("pixel-layer-weapon");
        const lAura = document.getElementById("pixel-layer-aura");

        if (lBody) {
          lBody.style.display = "block";
          lBody.style.backgroundImage = `url('${bodyPath}')`;
        }
        if (lArmor) {
          if (armorPath) {
            lArmor.style.display = "block";
            lArmor.style.backgroundImage = `url('${armorPath}')`;
          } else {
            lArmor.style.display = "none";
          }
        }
        if (lWeapon) {
          if (weaponPath) {
            lWeapon.style.display = "block";
            lWeapon.style.backgroundImage = `url('${weaponPath}')`;
          } else {
            lWeapon.style.display = "none";
          }
        }

        // 전투 아바타 오라 이펙트 (2개: aura-stage-1, 3개: aura-stage-2)
        if (lAura) {
          const auraStage = getActiveAuraStage();
          lAura.classList.remove("aura-stage-1", "aura-stage-2");
          if (auraStage === 1) lAura.classList.add("aura-stage-1");
          else if (auraStage === 2) lAura.classList.add("aura-stage-2");
        }

        // 전투 아바타 13대 돌연변이 파츠
        const activeParts = getActiveMutationParts();
        const allParts = [
          "wings", "fairy_wings", "tail", "booster", "shell", "crystals",
          "core", "horns", "spikes", "visor", "antennae", "halo", "claws"
        ];
        allParts.forEach(p => {
          const lPart = document.getElementById(`pixel-layer-${p}`);
          if (lPart) {
            if (activeParts.includes(p)) {
              lPart.style.display = "block";
              lPart.style.backgroundImage = `url('assets/pixel_hero/mutations/${p}_${motion}_${fIdx}.png')`;
            } else {
              lPart.style.display = "none";
            }
          }
        });

        DOM.battleAgentAvatar.style.backgroundImage = "none";
        DOM.battleAgentAvatar.style.transform = "none";
      } else if (STATE.renderMode === "parts") {
        if (battleScreen) battleScreen.classList.remove("pixel-mode");
        DOM.battleAgentAvatar.classList.add("parts-mode");
        DOM.battleAgentAvatar.style.backgroundImage = "none";

        pHead.style.display = "block";
        pTorso.style.display = "block";
        pRArm.style.display = "block";
        pLArm.style.display = "block";
        pLegs.style.display = "block";

        pHead.className = "part part-head drawn drawn-head";
        pTorso.className = "part part-torso drawn drawn-torso";
        pRArm.className = "part part-r-arm drawn drawn-arm";
        pLArm.className = "part part-l-arm drawn drawn-arm";
        pLegs.className = "part part-legs drawn drawn-legs";

        pHead.style.backgroundImage = "none";
        pTorso.style.backgroundImage = "none";
        pRArm.style.backgroundImage = "none";
        pLArm.style.backgroundImage = "none";
        pLegs.style.backgroundImage = "none";
        if (pVfx) pVfx.style.display = "none";

        pHead.style.transform = `translate(${h.x}px, ${h.y}px) rotate(${h.rot}deg)`;
        pTorso.style.transform = `translate(${t.x}px, ${t.y}px) rotate(${t.rot}deg)`;
        pRArm.style.transform = `translate(${ra.x}px, ${ra.y}px) rotate(${ra.rot}deg)`;
        pLArm.style.transform = `translate(${la.x}px, ${la.y}px) rotate(${la.rot}deg)`;
        pLegs.style.transform = `translate(${l.x}px, ${l.y}px) rotate(${l.rot}deg)`;
      } else {
        // 일러스트 모드
        if (battleScreen) battleScreen.classList.remove("pixel-mode");
        DOM.battleAgentAvatar.classList.remove("parts-mode");
        pHead.style.display = "none";
        pTorso.style.display = "none";
        pRArm.style.display = "none";
        pLArm.style.display = "none";
        pLegs.style.display = "none";
        if (pVfx) pVfx.style.display = "none";

        let skinImg = `assets/agents/agent_${genderSuffix}_trainee_${STATE.selectedRegion}.png`;
        if (STATE.nemesisEvolved) skinImg = `assets/agents/agent_${genderSuffix}_nemesis.png`;
        else if (STATE.ownedTraits.length > 0) skinImg = `assets/agents/agent_${genderSuffix}_body_mutation.png`;

        if (DOM.battleAgentAvatar.dataset.skin !== skinImg) {
          DOM.battleAgentAvatar.style.backgroundImage = `url('${skinImg}')`;
          DOM.battleAgentAvatar.dataset.skin = skinImg;
        }

        // 2.5D 유기적 관절 스웨잉 & 호흡 바운스
        const swayTilt = (h.rot * 0.6);
        const bobY = (t.y);
        DOM.battleAgentAvatar.style.transform = `translateY(${bobY}px) rotate(${swayTilt}deg)`;
      }
    }

    // 몬스터 다프레임 액션 스프라이트 (Idle 호흡 / 돌진 / 피격)
    if (STATE.renderMode === "pixel" && STATE.monsterParty && STATE.monsterParty.length > 0) {
      const mFrameIdx = STATE.currentFrame % 4;
      for (let i = 0; i < 3; i++) {
        const mAv = document.getElementById(`battleMonsterAvatar${i}`);
        const mInst = STATE.monsterParty[i];
        if (mAv && mInst && STATE.monsterHps[i] > 0) {
          const mWrapper = document.getElementById(`battleMonsterWrapper${i}`);
          let actionSuffix = `_idle_${mFrameIdx}.png`;
          if (mWrapper && mWrapper.classList.contains("monster-motion-lunge")) {
            actionSuffix = "_attack.png";
          } else if (mWrapper && mWrapper.classList.contains("monster-motion-knockback")) {
            actionSuffix = "_hit.png";
          }
          const pixelImg = mInst.img.replace("assets/monsters/", "assets/pixel_monsters/").replace(".png", actionSuffix);
          mAv.style.backgroundImage = `url('${pixelImg}')`;
        }
      }
    }
  }, tickDuration);
}

// 16. 전투 엔진 및 라운드 루프
function updateAgentHpDisplay(stats) {
  let hpTxt = `${STATE.playerHp}/${stats.maxHp}`;
  if (STATE.playerShield > 0) {
    hpTxt += ` (🛡️${STATE.playerShield})`;
  }
  DOM.battleAgentHpText.textContent = hpTxt;
  const hpPct = Math.max(0, Math.min(100, (STATE.playerHp / stats.maxHp) * 100));
  document.getElementById("battleAgentHp").style.width = `${hpPct}%`;
}

function initBattleStage() {
  STATE.combatRunning = true;
  STATE.currentMotion = "run";
  STATE.currentFrame = 0;
  startAnimationLoop();

  // 특성 및 시너지 상태 동기화
  checkActiveFusions();
  const stats = getDerivedStats();
  STATE.playerHp = stats.maxHp;

  // 1) 하이테크 공학 나노 쉴드 및 이지스 나노 배리어 연산
  STATE.playerShield = 0;
  if (hasEquipped("hightech_engineering")) {
    const shieldRate = hasFusion("aegis_barrier") ? 0.60 : 0.30;
    STATE.playerShield = Math.floor(stats.maxHp * shieldRate);
    writeBattleLog(`🛡️ [하이테크 공학] 나노 쉴드 (${STATE.playerShield}) 전개 완료!`, "system");
  }
  // 방사선 변환 반응로: 보유 Rad 1000당 나노 쉴드 150 추가 생성
  if (hasFusion("radiation_converter")) {
    const radBonus = Math.floor((STATE.currentRad / 1000) * 150);
    if (radBonus > 0) {
      STATE.playerShield = (STATE.playerShield || 0) + radBonus;
      writeBattleLog(`☢️ [방사선 변환 반응로] Rad 축적 에너지로 나노 쉴드 +${radBonus} 추가 생성!`, "system");
    }
  }

  // 2) 세포 차폐 배리어 충전
  STATE.cellularShieldCharges = hasEquipped("cellular_shield") ? 2 : 0;
  if (STATE.cellularShieldCharges > 0) {
    writeBattleLog(`🛡️ [세포 차폐] 2회 물리 강습 완전 무효화 배리어 충전 완료!`, "system");
  }

  // 3) 디버프 및 시너지 플래그 초기화
  STATE.monsterBurns = [0, 0, 0];
  STATE.monsterStuns = [false, false, false];
  STATE.phoenixUsed = false;
  STATE.adrenalinExoUsed = false;
  STATE.undyingTenacityUsed = false;
  STATE.shieldHitLastTurn = false;
  STATE.barrierBlockedLastTurn = false;
  STATE.critLastTurn = false;
  STATE.meltdownThrusterBonus = 0;

  updateAgentHpDisplay(stats);
  
  const agentWrapper = document.getElementById("battleAgentWrapper");
  agentWrapper.classList.remove("defeated", "agent-motion-dash", "agent-motion-skill", "agent-motion-knockback", "agent-combat-idle");
  agentWrapper.classList.add("agent-motion-entrance");
  document.getElementById("battleAgentAvatar").classList.remove("defeated");

  // 진입 달리기 완료 후 대기 전투 자세 전환
  setTimeout(() => {
    if (STATE.combatRunning) {
      agentWrapper.classList.remove("agent-motion-entrance");
      agentWrapper.classList.add("agent-combat-idle");
      STATE.currentMotion = "idle";
    }
  }, 1300 / STATE.gameSpeed);

  // 몬스터 3마리 소환
  const regionNum = STATE.selectedRegion;
  const regionMonsters = MONSTERS_DATABASE[regionNum] || MONSTERS_DATABASE[1];
  
  STATE.monsterParty = [];
  for (let i = 0; i < 3; i++) {
    // 보스전(6라운드)의 경우 무조건 최종 보스를 스폰
    let monsterTemplate;
    if (STATE.currentRound === 6) {
      monsterTemplate = regionMonsters.find(m => m.type === "boss") || regionMonsters[5];
    } else if (STATE.currentRound >= 4) {
      monsterTemplate = regionMonsters.find(m => m.type === "named") || regionMonsters[4];
    } else {
      // 일반 잡몹 4종 중 무작위
      monsterTemplate = regionMonsters[Math.floor(Math.random() * 4)];
    }
    
    // 사본 주입
    const mInstance = JSON.parse(JSON.stringify(monsterTemplate));
    STATE.monsterParty.push(mInstance);
    STATE.monsterHps[i] = mInstance.hp;
    STATE.monsterMaxHps[i] = mInstance.hp;

    // 몬스터 UI 갱신
    document.getElementById(`monster-name-${i}`).textContent = `${mInstance.name} (Lv.${regionNum})`;
    const mAvatar = document.getElementById(`battleMonsterAvatar${i}`);
    mAvatar.classList.remove("defeated");

    // 몬스터 스프라이트 이미지 세팅 (도트 모드 vs 일러스트 모드)
    let monsterImg = mInstance.img;
    if (STATE.renderMode === "pixel") {
      monsterImg = mInstance.img.replace("assets/monsters/", "assets/pixel_monsters/");
    }
    mAvatar.style.backgroundImage = `url('${monsterImg}')`;
    mAvatar.style.backgroundSize = "contain";
    mAvatar.style.backgroundRepeat = "no-repeat";
    mAvatar.style.backgroundPosition = "bottom center";
    mAvatar.classList.remove("defeated");

    // 이미지 에러 폴백
    const imgLoader = new Image();
    imgLoader.src = monsterImg;
    imgLoader.onerror = () => {
      let fallback = STATE.renderMode === "pixel" ? "assets/pixel_monsters/m_1_1.png" : "assets/monsters/m_1_1.png";
      if (mInstance.type === "named") fallback = STATE.renderMode === "pixel" ? "assets/pixel_monsters/m_1_named.png" : "assets/monsters/m_1_named.png";
      if (mInstance.type === "boss") fallback = STATE.renderMode === "pixel" ? "assets/pixel_monsters/m_1_boss.png" : "assets/monsters/m_1_boss.png";
      mAvatar.style.backgroundImage = `url('${fallback}')`;
    };

    document.getElementById(`battleMonsterHp${i}`).style.width = "100%";
  }

  // 4) 아포칼립스 라그나로크 개전 핵폭발 강림
  if (hasFusion("apocalypse_ragnarok")) {
    writeBattleLog(`☄️ [아포칼립스 라그나로크] 개전 즉시 핵폭발 강림! 모든 적 체력 50% 분쇄!`, "warning");
    for (let i = 0; i < 3; i++) {
      const dmg = Math.floor(STATE.monsterMaxHps[i] * 0.5);
      STATE.monsterHps[i] = Math.max(1, STATE.monsterHps[i] - dmg);
      document.getElementById(`battleMonsterHp${i}`).style.width = `${(STATE.monsterHps[i] / STATE.monsterMaxHps[i]) * 100}%`;
    }
  }

  DOM.battleRegionText.textContent = `지역 ${regionNum}: ${REGIONS_METADATA[regionNum].name}`;
  DOM.battleProgressText.textContent = `라운드 ${STATE.currentRound}/6 (챕터 클리어 조건: 6라운드 격파)`;
  DOM.battleConsole.innerHTML = `<div class="log-item system">⚔️ 라운드 ${STATE.currentRound} 전투 개시! (장착 특성: ${STATE.equippedTraits.filter(t=>t).map(t=>TRAITS_DATA[t]?.name).join(", ") || "없음"})</div>`;

  // 자동 전투 타이머 가동
  startCombatTimer();
}

function startCombatTimer() {
  if (STATE.combatTimer) clearInterval(STATE.combatTimer);

  const turnDelay = 2400 / STATE.gameSpeed; // 배속에 비례해 속도 단축 (기존 1200ms -> 2400ms 절반 감속)

  STATE.combatTimer = setInterval(() => {
    if (!STATE.combatRunning) return;
    executeCombatTurn();
  }, turnDelay);
}

function stopBattleLoop() {
  STATE.combatRunning = false;
  STATE.currentMotion = "idle";
  if (STATE.combatTimer) clearInterval(STATE.combatTimer);
}

// 전투 로그 기록
function writeBattleLog(msg, type = "combat") {
  const line = document.createElement("div");
  line.className = `log-item ${type}`;
  line.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  DOM.battleConsole.appendChild(line);
  DOM.battleConsole.scrollTop = DOM.battleConsole.scrollHeight;
}

// 전투 턴 로직 (13대 특성 및 78대 초월 융합 시스템 완전 가동)
function executeCombatTurn() {
  const stats = getDerivedStats();

  // 0) 턴 개시 시 지속 효과 처리 (화상 도트, 배리어 자동 복구)
  // (A) 이지스 나노 배리어 매 턴 쉴드 200 복구 (최대 HP의 150% 캡)
  if (hasFusion("aegis_barrier")) {
    const shieldCap = Math.floor(stats.maxHp * 1.5);
    STATE.playerShield = Math.min(shieldCap, (STATE.playerShield || 0) + 200);
    updateAgentHpDisplay(stats);
    writeBattleLog(`🛡️ [이지스 나노 배리어] 매 턴 보호막 +200 자동 복구! (현재 쉴드: ${STATE.playerShield})`, "system");
  }

  // (B) 열에너지 제어 / 플라즈마 헬파이어 / 체르노빌 연옥 / 타오르는 분노 화상 도트 대미지
  for (let i = 0; i < 3; i++) {
    if (STATE.monsterHps[i] > 0 && STATE.monsterBurns[i] > 0) {
      STATE.monsterBurns[i]--;
      let burnPct = (hasFusion("plasma_hellfire") || hasFusion("chernobyl_inferno")) ? 0.10 : 0.05;
      if (hasFusion("blazing_fury")) {
        const lostHpRatio = (stats.maxHp - STATE.playerHp) / stats.maxHp;
        burnPct = Math.min(0.12, burnPct + lostHpRatio * 0.07);
      }
      const burnDmg = Math.max(15, Math.floor(STATE.monsterMaxHps[i] * burnPct));
      STATE.monsterHps[i] = Math.max(0, STATE.monsterHps[i] - burnDmg);
      document.getElementById(`battleMonsterHp${i}`).style.width = `${(STATE.monsterHps[i] / STATE.monsterMaxHps[i]) * 100}%`;
      const mName = STATE.monsterParty[i]?.name || "괴수";
      writeBattleLog(`🔥 [지옥 화염] ${mName}에게 소각 피해 ${burnDmg} 발생! (남은 화상: ${STATE.monsterBurns[i]}턴)`, "damage");
      if (STATE.monsterHps[i] <= 0) {
        document.getElementById(`battleMonsterAvatar${i}`).classList.add("defeated");
        writeBattleLog(`💀 괴수 [${mName}]이(가) 화염에 전소되었습니다!`, "system");
        if (hasFusion("dirty_bomb_detonator")) {
          for (let k = 0; k < 3; k++) {
            if (k !== i && STATE.monsterHps[k] > 0) {
              STATE.monsterHps[k] = Math.max(0, STATE.monsterHps[k] - 300);
              document.getElementById(`battleMonsterHp${k}`).style.width = `${(STATE.monsterHps[k] / STATE.monsterMaxHps[k]) * 100}%`;
            }
          }
          writeBattleLog(`☢️ [더티밤 기폭장치] 화상 사망 연쇄 핵폭발! 주변 적에 300 광역 피해!`, "warning");
        }
      }
    }
  }

  // 1) 살아 있는 몬스터 타겟 지정
  let targetIndex = -1;
  for (let i = 0; i < 3; i++) {
    if (STATE.monsterHps[i] > 0) {
      targetIndex = i;
      break;
    }
  }

  // 몬스터 전멸 시 승리 처리
  if (targetIndex === -1) {
    handleRoundVictory();
    return;
  }

  // 2) 아군 공격 판정
  // 스킬 발동 확률
  let skillRate = 0.30;
  if (hasEquipped("fairy_magic")) skillRate = 0.60;
  if (hasFusion("chrono_fairy")) skillRate = 0.75;
  const isSkill = Math.random() < skillRate;

  // 연속 공격 횟수 판정
  let totalHits = 1;
  if (hasFusion("cyber_overclock")) {
    totalHits = 2;
  } else if (hasFusion("chrono_fairy") && Math.random() < 0.50) {
    totalHits = 2;
  } else if (hasEquipped("power_overload")) {
    const multiChance = hasFusion("atomic_turbocharger") ? 0.60 : 0.40;
    if (Math.random() < multiChance) totalHits = 2;
  }
  // 광전사 난무: 체력 40% 이하 시 3연속 타격
  if (hasFusion("berserk_flurry") && (STATE.playerHp / stats.maxHp <= 0.40)) {
    totalHits = 3;
    writeBattleLog(`⚔️ [광전사 난무] 체력 한계 돌파! 3연속 타격 난무 시동!`, "warning");
  }
  // 반응형 발전기: 이전 턴 배리어 방어 성공 시 확정 2연타
  if (hasFusion("reactive_dynamo") && STATE.barrierBlockedLastTurn) {
    totalHits = Math.max(totalHits, 2);
    STATE.barrierBlockedLastTurn = false;
    writeBattleLog(`⚡ [반응형 발전기] 충격 흡수 에너지 방출로 확정 2연타 가동!`, "warning");
  }

  // 크로노스 페어리 35% 확률 적 턴 강제 스킵
  if (hasFusion("chrono_fairy") && Math.random() < 0.35) {
    for (let m = 0; m < 3; m++) STATE.monsterStuns[m] = true;
    writeBattleLog(`⏳ [크로노스 페어리] 시간 정지 마법 시전! 모든 괴수의 턴 강제 스킵!`, "warning");
  }

  STATE.currentMotion = isSkill ? "skill" : "attack";
  STATE.currentFrame = 0;
  
  const agentWrapper = document.getElementById("battleAgentWrapper");
  if (agentWrapper) {
    agentWrapper.classList.remove("agent-combat-idle", "agent-motion-dash", "agent-motion-skill", "agent-motion-knockback");
    void agentWrapper.offsetWidth; // re-flow
    agentWrapper.classList.add(isSkill ? "agent-motion-skill" : "agent-motion-dash");
  }

  setTimeout(() => {
    if (STATE.combatRunning) {
      STATE.currentMotion = "idle";
      if (agentWrapper) {
        agentWrapper.classList.remove("agent-motion-dash", "agent-motion-skill");
        agentWrapper.classList.add("agent-combat-idle");
      }
    }
  }, (isSkill ? 1040 : 760) / STATE.gameSpeed);

  // 연타 루프 실행
  for (let hit = 1; hit <= totalHits; hit++) {
    // 멜트다운 추진기: 연속 타격 시 반사율 15% 영구 누적 상승
    if (hasFusion("meltdown_thruster") && hit > 1) {
      STATE.meltdownThrusterBonus = (STATE.meltdownThrusterBonus || 0) + 0.15;
    }

    // 타겟 재검색 (이전 연타로 몬스터가 쓰러졌을 경우 다음 타겟으로 자동 전이)
    let curTarget = -1;
    for (let i = 0; i < 3; i++) {
      if (STATE.monsterHps[i] > 0) {
        curTarget = i;
        break;
      }
    }
    if (curTarget === -1) break;

    const targetMonster = STATE.monsterParty[curTarget];

    // 치명타율 연산
    let critRate = 0.10;
    let critMult = 1.5;
    if (hasEquipped("sensory_tech")) {
      critRate += 0.30;
      critMult = 2.0;
    }
    if (hasFusion("cyber_overclock")) {
      critRate = 1.0;
      critMult = 2.2;
    }
    // HUD 전술 매트릭스: 쉴드 유지 중 치명타 피해 +80%
    if (hasFusion("hud_tactical_matrix") && STATE.playerShield > 0) {
      critMult += 0.80;
    }
    // 사선 직감: 체력 35% 이하 시 치명타 피해량 3.0배
    if (hasFusion("death_reckoning") && (STATE.playerHp / stats.maxHp <= 0.35)) {
      critMult = 3.0;
    }
    const isCrit = Math.random() < critRate;
    if (isCrit) STATE.critLastTurn = true;

    // 공격력 보정
    let rawAtk = stats.atk;
    // 버서커 광기: 잃은 체력 10%당 공격력 15% 증가
    if (hasEquipped("berserker_madness")) {
      const lostHpPct = (stats.maxHp - STATE.playerHp) / stats.maxHp;
      const scaleRate = hasFusion("irradiated_berserker") ? 1.8 : 1.5;
      rawAtk += Math.floor(rawAtk * (lostHpPct * scaleRate));
      if (STATE.playerHp / stats.maxHp <= 0.30) {
        rawAtk = Math.floor(rawAtk * 2.5); // 분노 각성
      }
    }
    // 임계돌파 자폭기: 체력 25% 이하 시 모든 공격력 3배
    if (hasFusion("suicide_meltdown") && (STATE.playerHp / stats.maxHp <= 0.25)) {
      rawAtk = Math.floor(rawAtk * 3.0);
      writeBattleLog(`🔥 [임계돌파 자폭기] 노심 한계 폭주! 공격력 3배 극대화!`, "warning");
    }
    // 사이보그 뮤턴트: 나노 쉴드 켜져 있는 동안 공격력 +40%
    if (hasFusion("cyborg_mutant") && STATE.playerShield > 0) {
      rawAtk = Math.floor(rawAtk * 1.40);
    }
    // 하드라이트 배터리: 쉴드 피격 후 다음 공격력 +50%
    if (hasFusion("hardlight_battery") && STATE.shieldHitLastTurn) {
      rawAtk = Math.floor(rawAtk * 1.50);
      STATE.shieldHitLastTurn = false;
      writeBattleLog(`💡 [하드라이트 배터리] 피격 축적 에너지 방출! 공격력 +50% 방출!`, "warning");
    }
    // 멜트다운 제어
    if (hasEquipped("meltdown_control") && (STATE.playerHp / stats.maxHp <= 0.35)) {
      rawAtk = Math.floor(rawAtk * 1.7);
    }
    // 판데모니움 비스트 융합
    if (hasFusion("pandemonium_beast")) {
      rawAtk = Math.floor(rawAtk * 2.0);
    }

    // 방어 관통
    let enemyDef = targetMonster.def;
    if (hasFusion("apocalypse_ragnarok")) {
      enemyDef = 0; // 100% 방관
    } else if (hasFusion("tactical_railgun")) {
      enemyDef = Math.floor(enemyDef * 0.40); // 60% 방관
    } else if (hasFusion("cyborg_mutant") && Math.random() < 0.25) {
      enemyDef = 0; // 25% 확률 방어 무시
    } else if (hasEquipped("energy_discharge")) {
      enemyDef = Math.floor(enemyDef * 0.65); // 35% 방관
    }

    // 스킬 계수
    let skillMult = isSkill ? 1.8 : 1.0;
    if (isSkill) {
      if (hasFusion("fairy_beast_surge")) {
        skillMult = 2.5; // 요정 야수화 2.5배
        const fbHeal = Math.floor(stats.maxHp * 0.20);
        STATE.playerHp = Math.min(stats.maxHp, STATE.playerHp + fbHeal);
        updateAgentHpDisplay(stats);
        writeBattleLog(`🧚‍♂️ [요정 야수화] 괴수 근력 폭발! 스킬 대미지 2.5배 증폭 및 최대 체력 20% (+${fbHeal}) 회복!`, "warning");
      } else if (hasFusion("valkyrie_rage")) {
        const lostRatio = (stats.maxHp - STATE.playerHp) / stats.maxHp;
        skillMult = 2.4 + lostRatio * 0.4; // 최대 2.8배
      } else if (hasEquipped("fairy_magic")) {
        skillMult = 2.4; // 요정 마법 스킬 증폭
      }
      if (hasFusion("fairy_will_o_wisp")) {
        for (let j = 0; j < 3; j++) {
          if (STATE.monsterHps[j] > 0) STATE.monsterBurns[j] = 3;
        }
        writeBattleLog(`🔥 [요정 도깨비불] 푸른 도깨비불이 적 전체에 번져 지옥화염 3중첩 부착!`, "warning");
      }
      if (hasFusion("siren_lullaby")) {
        for (let j = 0; j < 3; j++) {
          if (STATE.monsterHps[j] > 0 && Math.random() < 0.50) {
            STATE.monsterStuns[j] = true;
            writeBattleLog(`💤 [세이렌의 자장가] ${STATE.monsterParty[j].name}이(가) 수면/기절 상태에 돌입했습니다!`, "system");
          }
        }
      }
      if (hasFusion("techno_fairy_matrix")) {
        const shieldCap = Math.floor(stats.maxHp * 1.5);
        STATE.playerShield = Math.min(shieldCap, (STATE.playerShield || 0) + 250);
        writeBattleLog(`🛡️ [테크노 페어리] 스킬 발동 나노 쉴드 +250 즉시 전개!`, "system");
      }
    }

    // 천리안 신비술: 치명타 발생 시 스킬 공격력 +60% 및 아군 체력 15% 회복
    if (hasFusion("clairvoyant_mystic") && isCrit) {
      skillMult *= 1.6;
      const cmHeal = Math.floor(stats.maxHp * 0.15);
      STATE.playerHp = Math.min(stats.maxHp, STATE.playerHp + cmHeal);
      updateAgentHpDisplay(stats);
      writeBattleLog(`🔮 [천리안 신비술] 치명타 영기 폭발! 스킬 대미지 +60% 및 체력 +${cmHeal} 즉시 회복!`, "system");
    }

    // 신체 변이 [변이 충격파] 판정
    let isShockwave = false;
    if (hasFusion("primal_predator") && isCrit) {
      isShockwave = true;
      writeBattleLog(`⚡ [원시 포식자] 치명타 연계! 신체 변이 충격파 100% 강제 연계 발동!`, "warning");
    } else if (hasFusion("pandemonium_beast") && (STATE.playerHp / stats.maxHp <= 0.30)) {
      isShockwave = true;
    } else if (hasEquipped("body_mutation") && Math.random() < 0.30) {
      isShockwave = true;
    }
    // 야수 오버드라이브: 2번째 타격이 무조건 방어 무시 변이 충격파
    if (hasFusion("brutal_overdrive") && hit === 2) {
      isShockwave = true;
      writeBattleLog(`💥 [야수 오버드라이브] 2번째 타격이 방어 무시 변이 충격파로 적중!`, "warning");
    }

    if (isShockwave) {
      enemyDef = 0; // 방어 무시
      const swScale = (hasFusion("meltdown_titan") && (STATE.playerHp / stats.maxHp <= 0.35)) ? 2.5 : 1.6;
      skillMult *= swScale;
    }

    // 뉴럴 셰터 (기절한 적 대상 300% 분쇄 피해)
    if (hasFusion("neural_shatter") && STATE.monsterStuns[curTarget]) {
      skillMult *= 3.0;
    }
    // 멜트다운 공황: 기절한 적 받는 피해 50% 증폭
    if (hasFusion("meltdown_panic") && STATE.monsterStuns[curTarget]) {
      skillMult *= 1.5;
    }

    let damage = calculateDamage(rawAtk, enemyDef, skillMult, isCrit);

    // 키틴질 외골격 추가 고정 피해
    if (hasFusion("chitin_carapace")) {
      damage += stats.def;
    }

    // 진동 연타 타격: 연속 공격 시 적 방어력 30% 영구 감소
    if (hasFusion("vibrational_impact") && hit > 1) {
      targetMonster.def = Math.max(0, Math.floor(targetMonster.def * 0.70));
    }
    // 운동 에너지 발전기: 연속 타격 시 타격당 나노 쉴드 100 충전
    if (hasFusion("kinetic_generator") && hit > 1) {
      const shieldCap = Math.floor(stats.maxHp * 1.5);
      STATE.playerShield = Math.min(shieldCap, (STATE.playerShield || 0) + 100);
      writeBattleLog(`🔋 [운동 에너지 발전기] 연타 발전으로 나노 쉴드 +100 충전!`, "system");
    }
    // 과열 배기 폭발: 2연속 타격 시 2번째 타격에 200 화염 폭발 + 화상 2중첩
    if (hasFusion("overheated_exhaust") && hit === 2) {
      damage += 200;
      STATE.monsterBurns[curTarget] = Math.max(STATE.monsterBurns[curTarget] || 0, 2);
      writeBattleLog(`💥 [과열 배기 폭발] 연타 배기 폭발! +200 추가 피해 및 화상 2중첩!`, "warning");
    }
    // 열음향 폭발: 화상 상태인 적 타격 시 2배 폭발 대미지
    if (hasFusion("thermo_acoustic_blast") && (STATE.monsterBurns[curTarget] > 0)) {
      damage = Math.floor(damage * 2.0);
      writeBattleLog(`🔥 [열음향 폭발] 화염 공명 폭발! 피해량 2배 증폭!`, "warning");
    }
    // 레이저 열분해: 치명타 적중 시 화상 디버프 폭파 300 추가 폭발 피해
    if (hasFusion("laser_pyrolysis") && isCrit && (STATE.monsterBurns[curTarget] > 0)) {
      damage += 300;
      writeBattleLog(`💥 [레이저 열분해] 화상 디버프 폭파! 300의 추가 폭발 피해!`, "warning");
    }
    // 임계점 저격: 치명타 적중 시 적 노심 파괴하여 공격력 30% 영구 감소
    if (hasFusion("critical_meltdown") && isCrit) {
      targetMonster.atk = Math.max(5, Math.floor(targetMonster.atk * 0.70));
      writeBattleLog(`☣️ [임계점 저격] ${targetMonster.name}의 노심 파괴! 공격력 30% 영구 감소!`, "system");
    }
    // 양자 방사능 스캐너: 치명타 시 80 Rad 즉시 생성
    if (hasFusion("quantum_scanner") && isCrit) {
      STATE.currentRad += 80;
      DOM.townRadValue.textContent = STATE.currentRad;
    }
    // 감마 시냅스 교란기: 기절한 적 타격 시 120 Rad 강탈
    if (hasFusion("gamma_synapse_scrambler") && STATE.monsterStuns[curTarget]) {
      STATE.currentRad += 120;
      DOM.townRadValue.textContent = STATE.currentRad;
    }

    // 신체 변이 파생 융합 효과
    if (isShockwave) {
      // 대지 파열의 포효: 적 전체 50% 확률 초음파 기절
      if (hasFusion("seismic_roar")) {
        for (let j = 0; j < 3; j++) {
          if (STATE.monsterHps[j] > 0 && Math.random() < 0.50) {
            STATE.monsterStuns[j] = true;
            writeBattleLog(`📢 [대지 파열의 포효] 충격파 포효에 ${STATE.monsterParty[j].name} 기절!`, "system");
          }
        }
      }
      // 마그마 저거너트: 지옥화염 3중첩 + 200 고열 폭발 피해
      if (hasFusion("magma_juggernaut")) {
        STATE.monsterBurns[curTarget] = Math.max(STATE.monsterBurns[curTarget] || 0, 3);
        damage += 200;
        writeBattleLog(`🌋 [마그마 저거너트] 지옥화염 3중첩 및 200 고열 폭발 피해!`, "warning");
      }
      // 생체 플라즈마포: 적 전체에 1.8배 광역 타격
      if (hasFusion("bio_plasma_burst")) {
        const bioDmg = Math.floor(damage * 1.8);
        for (let j = 0; j < 3; j++) {
          if (j !== curTarget && STATE.monsterHps[j] > 0) {
            STATE.monsterHps[j] = Math.max(0, STATE.monsterHps[j] - bioDmg);
            document.getElementById(`battleMonsterHp${j}`).style.width = `${(STATE.monsterHps[j] / STATE.monsterMaxHps[j]) * 100}%`;
            triggerHitVFX(j, false);
          }
        }
        writeBattleLog(`☄️ [생체 플라즈마포] 변이 탄막이 적 전체에 1.8배 광역 타격 (${bioDmg})!`, "warning");
      }
    }

    // 피격 연출 & 투사체
    triggerHitVFX(curTarget, false);
    triggerProjectile(isSkill ? "skill" : "attack");

    STATE.monsterHps[curTarget] = Math.max(0, STATE.monsterHps[curTarget] - damage);
    document.getElementById(`battleMonsterHp${curTarget}`).style.width = `${(STATE.monsterHps[curTarget] / STATE.monsterMaxHps[curTarget]) * 100}%`;

    // 타격 로그
    if (hit > 1) {
      writeBattleLog(`⚡ [연속 공격 ${hit}타] 오버로드 가속 타격! ${targetMonster.name}에게 ${damage}의 피해!`, "combat");
    } else if (isShockwave) {
      writeBattleLog(`💥 [신체 변이 충격파] 괴수 분쇄 강타! ${targetMonster.name}에게 방어 무시 ${damage}의 치명상!`, "warning");
    } else if (isCrit) {
      writeBattleLog(`💥 치명타 작렬! 요원이 ${targetMonster.name}에게 ${damage}의 급소 피해!`, "warning");
    } else {
      writeBattleLog(`⚔️ 요원이 ${targetMonster.name}에게 ${damage}의 타격을 가했습니다.`, "combat");
    }

    // 광역 확산 피해 (에너지 방출 플라즈마 탄막 / 판데모니움 비스트 / 플라즈마 헬파이어 / 전술 레일건 / 하이퍼 과충전 / 스파크 페어리)
    const isCleave = hasFusion("pandemonium_beast") || hasFusion("plasma_hellfire") || hasFusion("apocalypse_ragnarok") ||
                     (hasFusion("tactical_railgun") && isCrit) ||
                     (hasFusion("hyper_discharge") && totalHits > 1) ||
                     (hasFusion("spark_fairy_storm") && isSkill) ||
                     (hasEquipped("energy_discharge") && (Math.random() < 0.35 || isSkill));

    if (isCleave) {
      let aoeRatio = 0.45;
      if (hasFusion("furious_lightning")) {
        const lostHpRatio = (stats.maxHp - STATE.playerHp) / stats.maxHp;
        aoeRatio = Math.min(1.0, 0.45 + lostHpRatio * 0.55); // 최대 120% 폭증
      }
      const aoeDamage = Math.max(15, Math.floor(damage * aoeRatio));
      let totalAoeDealt = 0;
      for (let j = 0; j < 3; j++) {
        if (j !== curTarget && STATE.monsterHps[j] > 0) {
          STATE.monsterHps[j] = Math.max(0, STATE.monsterHps[j] - aoeDamage);
          totalAoeDealt += aoeDamage;
          document.getElementById(`battleMonsterHp${j}`).style.width = `${(STATE.monsterHps[j] / STATE.monsterMaxHps[j]) * 100}%`;
          triggerHitVFX(j, false);

          // EMP 충격파: 탄막 타격 시 45% 확률 행동 스킵
          if (hasFusion("emp_shockwave") && Math.random() < 0.45) {
            STATE.monsterStuns[j] = true;
            writeBattleLog(`⚡ [EMP 충격파] ${STATE.monsterParty[j].name} 전자 신경계 마비(기절)!`, "system");
          }

          if (STATE.monsterHps[j] <= 0) {
            document.getElementById(`battleMonsterAvatar${j}`).classList.add("defeated");
            writeBattleLog(`💀 괴수 [${STATE.monsterParty[j].name}]이(가) 광역 탄막에 격파되었습니다!`, "system");
            if (hasFusion("dirty_bomb_detonator") && (STATE.monsterBurns[j] > 0)) {
              for (let k = 0; k < 3; k++) {
                if (k !== j && STATE.monsterHps[k] > 0) {
                  STATE.monsterHps[k] = Math.max(0, STATE.monsterHps[k] - 300);
                  document.getElementById(`battleMonsterHp${k}`).style.width = `${(STATE.monsterHps[k] / STATE.monsterMaxHps[k]) * 100}%`;
                }
              }
              writeBattleLog(`☢️ [더티밤 기폭장치] 화상 사망 연쇄 핵폭발! 주변 적에 300 광역 피해!`, "warning");
            }
          }
        }
      }
      writeBattleLog(`☄️ [플라즈마 탄막/광역 타격] 다른 적 전체에게 ${aoeDamage}의 확산 피해 동시 타격!`, "combat");

      // 플라즈마 리치: 광역 피해의 35%를 체력으로 즉시 흡혈
      if (hasFusion("plasma_leech") && totalAoeDealt > 0) {
        const plHeal = Math.floor(totalAoeDealt * 0.35);
        STATE.playerHp = Math.min(stats.maxHp, STATE.playerHp + plHeal);
        updateAgentHpDisplay(stats);
        writeBattleLog(`🧬 [플라즈마 리치] 탄막 광역 피해의 35% 흡혈 (+${plHeal} HP)!`, "system");
      }
    }

    // 디버프 부여: 열에너지 제어 (지옥 화염)
    if (hasEquipped("thermal_control") || hasFusion("plasma_hellfire")) {
      STATE.monsterBurns[curTarget] = 3; // 3턴 화상
    }

    // 디버프 부여: 초음파 정신 교란 (기절)
    if (hasEquipped("ultrasonic_disruption")) {
      const stunChance = hasFusion("neural_shatter") ? 0.65 : 0.35;
      if (Math.random() < stunChance) {
        STATE.monsterStuns[curTarget] = true;
        writeBattleLog(`💫 [초음파 혼란/기절] ${targetMonster.name}이(가) 초음파 펄스에 뇌를 타격당해 기절했습니다! (다음 턴 행동 불가)`, "system");
      }
    }

    // 정신 분쇄 포효: 체력 35% 이하 시 공격마다 적 전체에 50% 확률 기절 부여
    if (hasFusion("mind_rending_howl") && (STATE.playerHp / stats.maxHp <= 0.35)) {
      for (let j = 0; j < 3; j++) {
        if (STATE.monsterHps[j] > 0 && Math.random() < 0.50) {
          STATE.monsterStuns[j] = true;
          writeBattleLog(`📢 [정신 분쇄 포효] 광전사 포효에 ${STATE.monsterParty[j].name} 기절!`, "system");
        }
      }
    }

    // 흡혈 및 요정 회복
    if (hasEquipped("blood_absorption")) {
      let lsPct = (STATE.playerHp / stats.maxHp <= 0.50) ? 0.70 : 0.35;
      if (hasFusion("vampiric_chimera")) lsPct = 0.60;
      if (hasFusion("artery_targeting") && isCrit) lsPct = 1.0; // 동맥 정밀 타격 치명타 시 100% 흡혈
      if (hasFusion("sanguine_meltdown") && (STATE.playerHp / stats.maxHp <= 0.30)) lsPct = 1.0;
      if (hasFusion("blood_berserker")) lsPct = Math.min(0.85, 0.40 + (1 - STATE.playerHp / stats.maxHp) * 0.60);
      let heal = Math.floor(damage * lsPct);
      if (hasFusion("vampiric_chimera") && isShockwave) heal += 250;
      if (hasFusion("vampiric_pixie") && isSkill) heal = Math.floor(stats.maxHp * 0.30); // 아군 전체 회복 (30%)
      
      const prevHp = STATE.playerHp;
      STATE.playerHp = Math.min(stats.maxHp, STATE.playerHp + heal);
      const overflow = (prevHp + heal) - stats.maxHp;
      if (overflow > 0 && hasFusion("immortal_carapace")) {
        const shieldGain = Math.min(400, overflow);
        const shieldCap = Math.floor(stats.maxHp * 1.5);
        STATE.playerShield = Math.min(shieldCap, (STATE.playerShield || 0) + shieldGain);
        writeBattleLog(`🛡️ [불사신 갑각] 초과 흡혈량 ${shieldGain}이 나노 차폐 쉴드로 자동 전환! (현재 쉴드: ${STATE.playerShield})`, "system");
      }
      if (hasFusion("nanite_blood_infusion")) {
        const shieldCap = Math.floor(stats.maxHp * 1.5);
        STATE.playerShield = Math.min(shieldCap, (STATE.playerShield || 0) + 150);
        writeBattleLog(`💉 [나노 혈청 주입] 흡혈 발생으로 나노 쉴드 +150 재충전!`, "system");
      }
      if (hasFusion("blood_rush") && Math.random() < 0.50 && hit === totalHits) {
        writeBattleLog(`🩸 [피의 폭주] 흡혈로 아드레날린 분출! 즉시 추가 행동 개시!`, "warning");
        totalHits++;
      }
      if (hasFusion("boiling_blood")) {
        STATE.monsterBurns[curTarget] = Math.max(STATE.monsterBurns[curTarget] || 0, 2);
        writeBattleLog(`🔥 [끓어오르는 혈액] 흡혈 대상에게 작열 피해 부여 및 공격력 버프 획득!`, "system");
      }
      if (hasFusion("vampiric_screech") && Math.random() < 0.45) {
        STATE.monsterStuns[curTarget] = true;
        writeBattleLog(`🦇 [흡혈박쥐 초음파] 흡혈 충격으로 대상 기절 부여!`, "system");
      }
      if (hasFusion("irradiated_blood")) {
        STATE.currentRad += 50;
        DOM.townRadValue.textContent = STATE.currentRad;
        writeBattleLog(`☢️ [방사능 오염 혈액] 적의 혈청을 정제하여 +50 Rad 획득!`, "system");
      }
      updateAgentHpDisplay(stats);
      writeBattleLog(`🧬 [혈액 흡수] 괴수의 혈청을 흡수하여 체력 +${heal} 회복!`, "system");
    }

    if (hasEquipped("fairy_magic") && isSkill) {
      const fairyHeal = Math.floor(stats.maxHp * 0.15);
      STATE.playerHp = Math.min(stats.maxHp, STATE.playerHp + fairyHeal);
      updateAgentHpDisplay(stats);
      writeBattleLog(`✨ [요정 마법] 요정의 축복으로 체력 +${fairyHeal} 회복!`, "system");
    }

    // 감각 변이 즉시 추가 턴 행동
    const accelChance = (hasFusion("hud_tactical_matrix") && STATE.playerShield > 0) ? 0.40 : 0.25;
    if (hasEquipped("sensory_tech") && Math.random() < accelChance && hit === totalHits) {
      writeBattleLog(`⚡ [초감각 전술 가속] 초감각 반응으로 즉시 추가 공격을 개시합니다!`, "system");
      totalHits++;
    }

    // 몬스터 사망 판정
    if (STATE.monsterHps[curTarget] <= 0) {
      document.getElementById(`battleMonsterAvatar${curTarget}`).classList.add("defeated");
      writeBattleLog(`💀 괴수 [${targetMonster.name}]이(가) 완전히 쓰러졌습니다!`, "system");
      if (hasEquipped("radiation_assimilation")) {
        const radEarn = hasFusion("gamma_ray_burst") ? 250 : 100;
        STATE.currentRad += radEarn;
        DOM.townRadValue.textContent = STATE.currentRad;
        writeBattleLog(`☢️ [오염 동화] 괴수의 방사능 잔해 흡수 완료 (+${radEarn} Rad)`, "system");
      }
      if (hasFusion("dirty_bomb_detonator") && (STATE.monsterBurns[curTarget] > 0)) {
        for (let k = 0; k < 3; k++) {
          if (k !== curTarget && STATE.monsterHps[k] > 0) {
            STATE.monsterHps[k] = Math.max(0, STATE.monsterHps[k] - 300);
            document.getElementById(`battleMonsterHp${k}`).style.width = `${(STATE.monsterHps[k] / STATE.monsterMaxHps[k]) * 100}%`;
          }
        }
        writeBattleLog(`☢️ [더티밤 기폭장치] 화상 사망 연쇄 핵폭발! 주변 적에 300 광역 피해!`, "warning");
      }
    }
  }

  // 3) 생존 괴수의 역습 페이즈
  setTimeout(() => {
    if (!STATE.combatRunning) return;
    
    // 생존 괴수 전수 반격
    for (let i = 0; i < 3; i++) {
      if (STATE.monsterHps[i] > 0 && STATE.playerHp > 0) {
        const monster = STATE.monsterParty[i];
        
        // 기절 상태 검사
        if (STATE.monsterStuns[i]) {
          STATE.monsterStuns[i] = false; // 기절 소진
          writeBattleLog(`💫 [행동 불가] ${monster.name}이(가) 초음파 기절로 턴을 스킵했습니다!`, "system");
          continue;
        }

        // 예측 회피 기동: 치명타 후 35% 완전 회피
        if (hasFusion("predictive_evasion") && STATE.critLastTurn && Math.random() < 0.35) {
          writeBattleLog(`🌀 [예측 회피 기동] 적의 궤적을 예측하여 공격을 완전 회피했습니다!`, "system");
          continue;
        }

        // 요정의 성역: 배리어/쉴드 유지 중 피격 시 30% 확률 공격 무효화
        if (hasFusion("pixie_sanctuary") && (STATE.playerShield > 0 || STATE.cellularShieldCharges > 0) && Math.random() < 0.30) {
          writeBattleLog(`✨ [요정의 성역] 요정 가루가 피격 궤적을 지워 공격을 완전 무효화했습니다!`, "system");
          continue;
        }

        // 몬스터 돌진 모션 연출
        const mWrapper = document.getElementById(`battleMonsterWrapper${i}`);
        if (mWrapper) {
          mWrapper.classList.remove("monster-motion-lunge");
          void mWrapper.offsetWidth;
          mWrapper.classList.add("monster-motion-lunge");
          setTimeout(() => mWrapper.classList.remove("monster-motion-lunge"), 760 / STATE.gameSpeed);
        }

        // 세포 차폐 면역 배리어 검사
        if (STATE.cellularShieldCharges > 0) {
          STATE.cellularShieldCharges--;
          STATE.barrierBlockedLastTurn = true;
          writeBattleLog(`🛡️ [세포 차폐 배리어] 나노 차폐막이 괴수의 강습을 완전 무효화했습니다! (남은 배리어: ${STATE.cellularShieldCharges}회)`, "system");
          if (hasFusion("sonic_resonance_barrier")) {
            for (let m = 0; m < 3; m++) STATE.monsterStuns[m] = true;
            writeBattleLog(`📢 [음향 공명 방벽] 방벽 방어 충격파로 적 전체 초음파 기절!`, "warning");
          }
          continue;
        }
        if (hasEquipped("cellular_shield") && Math.random() < 0.30) {
          STATE.barrierBlockedLastTurn = true;
          writeBattleLog(`🛡️ [세포 나노 차폐막] 세포 자가경화로 공격 피해를 0으로 상쇄!`, "system");
          if (hasFusion("sonic_resonance_barrier")) {
            for (let m = 0; m < 3; m++) STATE.monsterStuns[m] = true;
            writeBattleLog(`📢 [음향 공명 방벽] 방벽 방어 충격파로 적 전체 초음파 기절!`, "warning");
          }
          continue;
        }

        // 괴수 공격력 산출
        let mDamage = Math.max(5, Math.floor(monster.atk * 1.5 - stats.def));
        if (hasFusion("chitin_carapace")) mDamage = Math.floor(mDamage * 0.65); // 35% 상시 경감
        if (hasFusion("lead_nanite_coat")) mDamage = Math.floor(mDamage * 0.75); // 25% 고정 경감

        const initialDamage = mDamage;

        // 나노 쉴드(보호막) 우선 흡수
        if (STATE.playerShield > 0) {
          STATE.shieldHitLastTurn = true;
          if (hasFusion("sonic_defense_grid") && Math.random() < 0.35) {
            STATE.monsterStuns[i] = true;
            writeBattleLog(`⚡ [음향 방어 그리드] 쉴드 피격 시 초음파 카운터로 ${monster.name} 기절!`, "warning");
          }
          const absorbed = Math.min(STATE.playerShield, mDamage);
          STATE.playerShield -= absorbed;
          mDamage -= absorbed;
          writeBattleLog(`🛡️ [나노 쉴드 흡수] 보호막이 ${absorbed} 피해를 방어했습니다. (남은 쉴드: ${STATE.playerShield})`, "system");
        }

        // 에너지 편향 필드: 피격 시 30% 피해 역반사
        if (hasFusion("energy_barrier_deflection")) {
          const deflDmg = Math.max(10, Math.floor(initialDamage * 0.30));
          STATE.monsterHps[i] = Math.max(0, STATE.monsterHps[i] - deflDmg);
          writeBattleLog(`💫 [에너지 편향 필드] 투사체 역편향! ${monster.name}에게 ${deflDmg}의 반사 피해!`, "system");
        }

        // 열차폐 나노 장갑 / 내열 단열 외피: 화상 반사
        if (hasFusion("thermal_shielding") || hasFusion("flame_retardant_shell")) {
          STATE.monsterBurns[i] = Math.max(STATE.monsterBurns[i] || 0, 3);
          writeBattleLog(`🔥 [열차폐 장갑] 공격한 ${monster.name}에게 즉시 화상 반사 부여!`, "system");
        }

        // 잔여 대미지 HP 차감
        if (mDamage > 0) {
          STATE.playerHp = Math.max(0, STATE.playerHp - mDamage);
          triggerHitVFX(-1, true);
          writeBattleLog(`💥 강습 피격: ${monster.name}이(가) 요원에게 ${mDamage}의 타격을 가했습니다.`, "damage");
        }

        // 아드레날린 외골격: 체력 50% 이하 시 1회 비상 쉴드 500 전개
        if (hasFusion("adrenalin_exoskeleton") && !STATE.adrenalinExoUsed && (STATE.playerHp / stats.maxHp <= 0.50)) {
          STATE.adrenalinExoUsed = true;
          STATE.playerShield = (STATE.playerShield || 0) + 500;
          writeBattleLog(`🚨 [아드레날린 외골격] 체력 50% 이하 감지! 비상 나노 쉴드 +500 긴급 전개!`, "warning");
        }

        // 불굴의 버서커: 체력 1 이하 위기 시 1회 한정 HP 1로 생존 및 배리어 3회 비상 충전
        if (hasFusion("undying_tenacity") && !STATE.undyingTenacityUsed && STATE.playerHp <= 0) {
          STATE.undyingTenacityUsed = true;
          STATE.playerHp = 1;
          STATE.cellularShieldCharges = 3;
          writeBattleLog(`💀 [불굴의 버서커] 결사의 의지 발동! HP 1로 버텨내며 나노 배리어 3회 비상 충전!`, "warning");
        }

        updateAgentHpDisplay(stats);

        // 멜트다운 방사능 반사 및 코어 보강 프레임
        if (hasEquipped("meltdown_control") || hasFusion("core_containment_vessel")) {
          const canReflect = (mDamage > 0) || hasFusion("core_reinforcement");
          if (canReflect) {
            let reflectPct = 0.30;
            if (hasFusion("chernobyl_meltdown") || hasFusion("chernobyl_inferno") || hasFusion("meltdown_titan")) reflectPct = 0.50;
            if (hasFusion("suicide_meltdown") && (STATE.playerHp / stats.maxHp <= 0.25)) reflectPct = 0.70;
            if (hasFusion("sanguine_meltdown") && (STATE.playerHp / stats.maxHp <= 0.30)) reflectPct = 0.50;
            if (hasFusion("core_containment_vessel")) reflectPct += 0.40;
            if (STATE.meltdownThrusterBonus) reflectPct += STATE.meltdownThrusterBonus;

            const reflectDmg = Math.max(10, Math.floor(initialDamage * reflectPct));
            STATE.monsterHps[i] = Math.max(0, STATE.monsterHps[i] - reflectDmg);
            document.getElementById(`battleMonsterHp${i}`).style.width = `${(STATE.monsterHps[i] / STATE.monsterMaxHps[i]) * 100}%`;
            writeBattleLog(`☢️ [멜트다운 반사] 피격 방사능 충격 반사! ${monster.name}에게 ${reflectDmg}의 반사 피해 (${Math.floor(reflectPct*100)}%)!`, "warning");
            if (STATE.monsterHps[i] <= 0) {
              document.getElementById(`battleMonsterAvatar${i}`).classList.add("defeated");
              writeBattleLog(`💀 괴수 [${monster.name}]이(가) 방사능 반사 피해로 파괴되었습니다!`, "system");
            }
          }
        }

        if (STATE.playerHp <= 0) {
          handlePlayerDefeat();
          break;
        }
      }
    }
  }, 800 / STATE.gameSpeed);
}

// 대미지 공식 연산
function calculateDamage(atk, def, multiplier, isCrit) {
  let baseDmg = (atk * multiplier) - def;
  const minDmg = atk * 0.1;
  if (baseDmg < minDmg) baseDmg = minDmg;
  
  if (isCrit) baseDmg *= 1.5;
  return Math.floor(baseDmg);
}

// VFX 제어 (16비트 아케이드 이펙트 및 타격 스파크)
function triggerHitVFX(targetIndex, isPlayer) {
  if (isPlayer) {
    const aWrapper = document.getElementById("battleAgentWrapper");
    if (aWrapper) {
      aWrapper.classList.add("hit-blink");
      setTimeout(() => aWrapper.classList.remove("hit-blink"), 120);

      aWrapper.classList.remove("agent-combat-idle", "agent-motion-knockback");
      void aWrapper.offsetWidth;
      aWrapper.classList.add("agent-motion-knockback");
      setTimeout(() => {
        if (STATE.combatRunning) {
          aWrapper.classList.remove("agent-motion-knockback");
          aWrapper.classList.add("agent-combat-idle");
        }
      }, 560 / STATE.gameSpeed);
    }
    
    DOM.battleScreenFlash.style.opacity = "0.5";
    setTimeout(() => DOM.battleScreenFlash.style.opacity = "0", 80);
  } else {
    const mWrapper = document.getElementById(`battleMonsterWrapper${targetIndex}`);
    const mAv = document.getElementById(`battleMonsterAvatar${targetIndex}`);
    if (mWrapper) {
      mWrapper.classList.add("hit-blink");
      setTimeout(() => mWrapper.classList.remove("hit-blink"), 120);

      mWrapper.classList.remove("monster-motion-knockback", "monster-motion-lunge");
      void mWrapper.offsetWidth;
      mWrapper.classList.add("monster-motion-knockback");
      
      // 피격 액션 프레임 전환
      if (mAv && STATE.renderMode === "pixel" && STATE.monsterParty[targetIndex]) {
        const hitImg = STATE.monsterParty[targetIndex].img.replace("assets/monsters/", "assets/pixel_monsters/").replace(".png", "_hit.png");
        mAv.style.backgroundImage = `url('${hitImg}')`;
      }

      setTimeout(() => mWrapper.classList.remove("monster-motion-knockback"), 560 / STATE.gameSpeed);
    }

    // 16비트 아케이드 폭발 타격 스파크
    const sparkEl = document.getElementById("effectHitSpark");
    if (sparkEl && targetIndex >= 0) {
      const topPcts = [18, 48, 78];
      sparkEl.style.top = `${topPcts[targetIndex] || 50}%`;
      sparkEl.style.right = "90px";
      sparkEl.classList.remove("burst");
      void sparkEl.offsetWidth;
      sparkEl.classList.add("burst");
      setTimeout(() => sparkEl.classList.remove("burst"), 400);
    }
  }

  // 화면 흔들림
  DOM.battleStageContainer.classList.add("shake-anim");
  setTimeout(() => DOM.battleStageContainer.classList.remove("shake-anim"), 150);
}

// 16비트 아케이드 투사체 트리거 (무기 및 각성폼 매칭)
function triggerProjectile(actionType) {
  const { weaponKey } = getEquippedVisualKeys();
  let projEl = document.getElementById("effectSlash");

  if (STATE.nemesisEvolved) {
    projEl = document.getElementById("effectNemesisSlash") || projEl;
  } else if (weaponKey === "axe") {
    projEl = document.getElementById("effectAxe") || projEl;
  } else if (weaponKey === "crystal_sword" || weaponKey === "heavy_cannon" || weaponKey === "lava_launcher") {
    projEl = document.getElementById("effectLaser") || projEl;
  } else if (actionType === "skill") {
    projEl = Math.random() < 0.5 ? document.getElementById("effectLaser") : document.getElementById("effectAxe");
  }

  if (projEl) {
    projEl.style.top = `${28 + Math.random() * 38}%`;
    const projClass = projEl.id.replace("effect","").toLowerCase();
    projEl.className = `battle-projectile ${projClass} fire-right`;
    
    setTimeout(() => {
      projEl.className = `battle-projectile ${projClass}`;
    }, 700 / STATE.gameSpeed);
  }
}

// 라운드 승리
function handleRoundVictory() {
  writeBattleLog(`🏆 라운드 ${STATE.currentRound} 토벌 완료!`, "system");
  
  if (STATE.currentRound < 6) {
    // 다음 라운드 진입
    STATE.currentRound++;
    setTimeout(() => {
      if (STATE.combatRunning) initBattleStage();
    }, 1600 / STATE.gameSpeed);
  } else {
    // 6라운드 최종 승리 -> 챕터 완료!
    stopBattleLoop();
    
    // Rad 보상 정산
    const radReward = STATE.selectedRegion * 150 + 200;
    STATE.currentRad += radReward;
    DOM.townRadValue.textContent = STATE.currentRad;

    // 아이템 드롭 생성 및 가방에 밀어넣기
    const dropItem = generateRandomItem(STATE.selectedRegion);
    let invFullMessage = "";
    if (STATE.inventory.length < 20) {
      STATE.inventory.push(dropItem);
    } else {
      invFullMessage = " (가방이 가득 차 전리품을 유실했습니다!)";
    }

    // 슬롯 해금 판정 (2번째 마을 클리어 시 2번 슬롯, 3번째 마을 클리어 시 3번 슬롯 해금)
    let slotUnlockMessage = "";
    if (STATE.selectedRegion === 2 && STATE.unlockedTraitSlots < 2) {
      STATE.unlockedTraitSlots = 2;
      slotUnlockMessage = "\n\n🔓 [특성 슬롯 해금!] 제 2 특성 슬롯이 개방되었습니다!\n이제 2개의 특성을 동시에 착용하여 청록 돌연변이 오라 및 2중 융합 시너지를 발동할 수 있습니다!";
      writeBattleLog("🎉 [특성 슬롯 해금] 서유럽 원전 지대 토벌 완료! 제 2 특성 슬롯이 개방되었습니다!", "system");
      setTimeout(() => alert("🎉 축하합니다! 2번째 지역을 클리어하여 [제 2 특성 슬롯]이 해금되었습니다!\n특성창(🧬)에서 2개의 특성을 장착하여 돌연변이 오라 효과와 초월 융합 능력을 발동해 보세요!"), 600);
    } else if (STATE.selectedRegion === 3 && STATE.unlockedTraitSlots < 3) {
      STATE.unlockedTraitSlots = 3;
      slotUnlockMessage = "\n\n🔓 [특성 슬롯 해금!] 제 3 특성 슬롯이 개방되었습니다!\n이제 3개의 특성을 동시에 착용하여 진홍/보라 코스믹 완전체 각성 오라와 2개의 2중 융합 시너지를 동시에 발동할 수 있습니다!";
      writeBattleLog("🎉 [특성 슬롯 해금] 동아시아 메가시티 토벌 완료! 제 3 특성 슬롯이 개방되었습니다!", "system");
      setTimeout(() => alert("🎉 축하합니다! 3번째 지역을 클리어하여 [제 3 특성 슬롯]이 해금되었습니다!\n모든 3개 슬롯이 개방되어 완전체 코스믹 각성 오라와 슬롯 간 2개의 2중 융합 시너지를 동시에 발동할 수 있습니다!"), 600);
    }

    // 해당 지역 고유 특성 칩셋 획득
    const regTrait = REGIONS_METADATA[STATE.selectedRegion]?.trait;
    let traitAcquiredMsg = "";
    if (regTrait && TRAITS_DATA[regTrait] && !STATE.ownedTraits.includes(regTrait)) {
      STATE.ownedTraits.push(regTrait);
      traitAcquiredMsg = `\n🧬 지역 고유 특성 칩셋 [${TRAITS_DATA[regTrait].name}] 획득!`;
      writeBattleLog(`🧬 신규 특성 칩셋 획득: ${TRAITS_DATA[regTrait].name}`, "system");
    }

    // 맵 진척도 갱신
    if (STATE.selectedRegion === STATE.unlockedRegion) {
      STATE.unlockedRegion = Math.min(14, STATE.unlockedRegion + 1);
      // 14챕터 최종 클리어 플래그
      if (STATE.selectedRegion === 14) {
        STATE.everestCleared = true;
      }
    }

    DOM.clearRewardInfo.textContent = `전리품 정산: +${radReward} Rad 광석 및 장비 [${dropItem.name}] 획득!${invFullMessage}${traitAcquiredMsg}${slotUnlockMessage}`;
    DOM.overlayClear.style.display = "flex";
  }
}

// 요원 전멸
function handlePlayerDefeat() {
  writeBattleLog(`💀 요원이 침식되어 쓰러졌습니다! 전투 불능 상태.`, "warning");

  // 불사조 환생 (요정 마법 + 멜트다운 제어 2중 융합)
  if (hasFusion("phoenix_rebirth") && !STATE.phoenixUsed) {
    STATE.phoenixUsed = true;
    const stats = getDerivedStats();
    STATE.playerHp = Math.floor(stats.maxHp * 0.40);
    updateAgentHpDisplay(stats);
    writeBattleLog(`🔥 [불사조 환생] 요정-노심 환생 기적 발동! 체력 40%로 즉시 부활!`, "system");
    return;
  }

  stopBattleLoop();
  const agentWrapper = document.getElementById("battleAgentWrapper");
  if (agentWrapper) agentWrapper.classList.remove("agent-combat-idle", "agent-motion-dash", "agent-motion-skill", "agent-motion-knockback", "agent-motion-entrance");
  document.getElementById("battleAgentAvatar").classList.add("defeated");

  setTimeout(() => {
    if (DOM.overlayDefeat) {
      DOM.overlayDefeat.style.display = "flex";
    } else {
      alert("시뮬레이션 전멸! 안전 구역 마을로 회송 조치됩니다.");
      showScreen("town");
    }
  }, 600);
}

// 17. 배속 및 조립 렌더링 모드 토글 바인딩
DOM.btnGameSpeed.onclick = () => {
  if (STATE.gameSpeed === 1) {
    STATE.gameSpeed = 2;
  } else if (STATE.gameSpeed === 2) {
    STATE.gameSpeed = 4;
  } else {
    STATE.gameSpeed = 1;
  }
  DOM.btnGameSpeed.textContent = `⚡ 배속: ${STATE.gameSpeed}x`;
  
  // 전투 진행 중이면 타이머 재가동
  if (STATE.combatRunning) {
    startCombatTimer();
    startAnimationLoop();
  }
};

// 렌더 모드 토글 버튼 추가 장착 (레트로 도트 / 고화질 원화 / 파츠 조립)
const toggleRenderBtn = document.createElement("button");
toggleRenderBtn.id = "btn-render-mode";
toggleRenderBtn.className = "btn-forager btn-speed";
toggleRenderBtn.style.marginLeft = "10px";
toggleRenderBtn.textContent = "🎮 모드: 레트로 도트";
const battleHeader = document.querySelector(".battle-info-left");
if (battleHeader && battleHeader.parentNode) {
  battleHeader.parentNode.appendChild(toggleRenderBtn);
}

toggleRenderBtn.onclick = () => {
  const battleScreen = document.getElementById("screen-battle");
  if (STATE.renderMode === "pixel") {
    STATE.renderMode = "illustration";
    toggleRenderBtn.textContent = "🎨 모드: 고화질 원화";
    if (battleScreen) battleScreen.classList.remove("pixel-mode");
    writeBattleLog("🎨 렌더러 전환: 원화 일러스트 2.5D 스웨잉 모드", "system");
  } else if (STATE.renderMode === "illustration") {
    STATE.renderMode = "parts";
    toggleRenderBtn.textContent = "⚙️ 모드: 파츠 조립";
    if (battleScreen) battleScreen.classList.remove("pixel-mode");
    writeBattleLog("🤖 렌더러 전환: 10프레임 정적 메카닉 파츠 조립 모드", "system");
  } else {
    STATE.renderMode = "pixel";
    toggleRenderBtn.textContent = "🎮 모드: 레트로 도트";
    if (battleScreen) battleScreen.classList.add("pixel-mode");
    writeBattleLog("🎮 렌더러 전환: 감성 레트로 픽셀 도트 아트 모드", "system");
  }

  // 페이퍼돌 레이어 표시 제어
  const lBody = document.getElementById("pixel-layer-body");
  const lArmor = document.getElementById("pixel-layer-armor");
  const lWeapon = document.getElementById("pixel-layer-weapon");
  const showPaperdoll = (STATE.renderMode === "pixel");
  if (lBody) lBody.style.display = showPaperdoll ? "block" : "none";
  if (lArmor) lArmor.style.display = showPaperdoll ? "block" : "none";
  if (lWeapon) lWeapon.style.display = showPaperdoll ? "block" : "none";

  // 아바타 스킨 갱신 트리거
  if (DOM.battleAgentAvatar) {
    DOM.battleAgentAvatar.dataset.skin = "";
  }

  // 몬스터 스프라이트 즉시 갱신
  if (STATE.monsterParty && STATE.monsterParty.length > 0) {
    for (let i = 0; i < STATE.monsterParty.length; i++) {
      const mInst = STATE.monsterParty[i];
      const mAv = document.getElementById(`battleMonsterAvatar${i}`);
      if (mInst && mAv) {
        let mImg = mInst.img;
        if (STATE.renderMode === "pixel") {
          mImg = mInst.img.replace("assets/monsters/", "assets/pixel_monsters/").replace(".png", "_idle_0.png");
        }
        mAv.style.backgroundImage = `url('${mImg}')`;
      }
    }
  }

  // 파츠 오프셋 초기화
  const pHead = document.getElementById("battle-head");
  const pTorso = document.getElementById("battle-torso");
  const pRArm = document.getElementById("battle-r-arm");
  const pLArm = document.getElementById("battle-l-arm");
  const pLegs = document.getElementById("battle-legs");
  if (pHead && pTorso && pRArm && pLArm && pLegs) {
    pHead.style.transform = "none";
    pTorso.style.transform = "none";
    pRArm.style.transform = "none";
    pLArm.style.transform = "none";
    pLegs.style.transform = "none";
  }
};

// 18. 전체 이벤트 위임 및 초기화
function initGame() {
  // 첫 화면 시작
  document.getElementById("btn-game-start").onclick = () => {
    showScreen("map");
    renderWorldMapPins();
  };

  // 마을 거점 클릭 이벤트 바인딩
  document.getElementById("town-building-shop").onclick = () => openModal("modal-shop");
  document.getElementById("town-building-lab").onclick = () => openModal("modal-trait-lab");
  document.getElementById("town-building-travel").onclick = () => {
    showScreen("map");
    renderWorldMapPins();
  };

  // 마을 요원 아바타 클릭 시 능력치창 오픈
  const townAgent = document.getElementById("townAgentBox");
  if (townAgent) {
    townAgent.onclick = () => openModal("modal-stats");
  }

  // 클리어 창 -> 마을 이동
  DOM.btnGoTown.onclick = () => {
    DOM.overlayClear.style.display = "none";
    showScreen("town");
  };

  // 패배 창 -> 마을 이동
  if (DOM.btnDefeatTown) {
    DOM.btnDefeatTown.onclick = () => {
      if (DOM.overlayDefeat) DOM.overlayDefeat.style.display = "none";
      showScreen("town");
    };
  }

  // 기본 가방 장비 2종 지원 초기 셋업
  STATE.inventory.push(generateRandomItem(1));
  STATE.inventory.push(generateRandomItem(1));
  
  // 디버깅 방사능 초기 셋업
  STATE.currentRad = 500;

  // 특성 슬롯 및 돌연변이 시스템 초기 상태 셋업 (슬롯 1개 개방, 신체 변이 1개 장착 및 보유)
  STATE.unlockedTraitSlots = 1;
  STATE.equippedTraits = ["body_mutation", null, null];
  STATE.ownedTraits = ["body_mutation"];
  checkActiveFusions();

  // 16비트 아케이드 글로벌 애니메이션 루프 즉시 시작
  startAnimationLoop();
  
  writeBattleLog("🧬 PROJECT 2100 시뮬레이션 시스템이 완전히 적재되었습니다. (초기 특성: 신체 변이 장착 중)", "system");
}

window.onload = () => {
  initGame();
};
