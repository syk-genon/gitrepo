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