// PROJECT 2100 - Display Data Extracted from index.js
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

// Weapon and Armor Definitions
const DISPLAY_WEAPONS = [
  { id: "none", name: "맨손 / 빈손 (Bare Hands)" },
  { id: "katana", name: "카타나 (Katana)" },
  { id: "axe", name: "전투 도끼 (Axe)" },
  { id: "crystal_sword", name: "크리스탈 소드 (Crystal Sword)" },
  { id: "heavy_cannon", name: "중기관포 (Heavy Cannon)" },
  { id: "lava_launcher", name: "용암 런처 (Lava Launcher)" }
];

const DISPLAY_ARMORS = [
  { id: "none", name: "기본 낡은 셔츠 & 반바지 (Ragged Clothes)" },
  { id: "military", name: "조선 군복 (Joseon Military)" },
  { id: "leather", name: "납 차폐 가죽 코트 (Shielded Leather)" },
  { id: "nano_carbon", name: "나노 카본 외골격 (Nano Carbon)" },
  { id: "hardlight", name: "중성자 하드라이트 슈트 (Hardlight)" },
  { id: "yeti_fur", name: "빅풋 예티 퍼 코트 (Yeti Fur)" }
];

if (typeof module !== 'undefined') {
  module.exports = { MONSTERS_DATABASE, TRAIT_MUTATIONS, TRAIT_PART_NAMES, TRAITS_DATA, FUSION_DATA, DISPLAY_WEAPONS, DISPLAY_ARMORS };
}
