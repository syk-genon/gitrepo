# -*- coding: utf-8 -*-
# Python script to generate all 78 2-trait fusions with complete metadata

traits = [
    ("body_mutation", "신체 변이"),
    ("energy_discharge", "에너지 방출"),
    ("sensory_tech", "감각 변이/테크"),
    ("blood_absorption", "혈액 흡수"),
    ("cellular_shield", "세포 차폐"),
    ("fairy_magic", "요정 마법"),
    ("power_overload", "동력 과부하"),
    ("thermal_control", "열에너지 제어"),
    ("ultrasonic_disruption", "초음파 정신 교란"),
    ("berserker_madness", "버서커 광기"),
    ("radiation_assimilation", "오염 동화"),
    ("meltdown_control", "멜트다운 제어"),
    ("hightech_engineering", "하이테크 공학")
]

# 78 Custom designed fusions
FUSIONS_CONFIG = {
    # 1. body_mutation pairs (12)
    ("body_mutation", "energy_discharge"): ("bio_plasma_burst", "생체 플라즈마포", "변이 충격파 발동 시 플라즈마 탄막이 동시 방출되어 살아있는 적 전체에 1.8배 광역 타격"),
    ("body_mutation", "sensory_tech"): ("primal_predator", "원시 포식자", "치명타 발생 시 100% 확률로 신체 변이 충격파가 강제 연계 발동"),
    ("body_mutation", "blood_absorption"): ("vampiric_chimera", "뱀파이어 키메라", "신체 괴력 흡혈 (흡혈량 60% + 변이 충격파 발동 시 HP 250 추가 회복)"),
    ("body_mutation", "cellular_shield"): ("chitin_carapace", "키틴질 외골격", "받는 모든 피해 35% 상시 경감 + 물리 타격 시 방어력의 100% 추가 고정 피해"),
    ("body_mutation", "fairy_magic"): ("fairy_beast_surge", "요정 야수화", "스킬 사용 시 괴수 근력이 폭발하여 스킬 대미지 2.5배 증폭 및 최대 체력 20% 회복"),
    ("body_mutation", "power_overload"): ("brutal_overdrive", "야수 오버드라이브", "오버로드 연속 타격 시 2번째 타격이 무조건 방어 무시 변이 충격파로 적중"),
    ("body_mutation", "thermal_control"): ("magma_juggernaut", "마그마 저거너트", "충격파 적중 시 대상에게 지옥화염 3중첩 즉시 부여 및 200의 고열 폭발 피해"),
    ("body_mutation", "ultrasonic_disruption"): ("seismic_roar", "대지 파열의 포효", "충격파 발동 시 적 전체에 50% 확률로 초음파 기절 동시 부여"),
    ("body_mutation", "berserker_madness"): ("pandemonium_beast", "판데모니움 비스트", "잃은 체력 비례 공격력 상승폭 2배 + 체력 30% 이하 시 충격파 100% 확정 발동"),
    ("body_mutation", "radiation_assimilation"): ("nuclear_colossus", "방사능 거신", "보유 Rad 1000당 신체 변이 추가 공격력 +15% 및 방어력 +15%"),
    ("body_mutation", "meltdown_control"): ("meltdown_titan", "노심 타이탄", "체력 35% 이하 시 충격파 피해 2.5배 증폭 및 방사능 반사율 50%로 상승"),
    ("body_mutation", "hightech_engineering"): ("cyborg_mutant", "사이보그 뮤턴트", "나노 쉴드가 켜져 있는 동안 기본 공격력 +40% 및 방어 무시 확률 +25%"),

    # 2. energy_discharge pairs (11)
    ("energy_discharge", "sensory_tech"): ("tactical_railgun", "전술 레일건", "에너지 방관율이 60%로 상승하고, 치명타 발생 시 적 전체 관통 레이저 사격"),
    ("energy_discharge", "blood_absorption"): ("plasma_leech", "플라즈마 리치", "플라즈마 볼트 탄막으로 입힌 모든 광역 피해의 35%를 체력으로 즉시 흡혈"),
    ("energy_discharge", "cellular_shield"): ("energy_barrier_deflection", "에너지 편향 필드", "피격 시 방출된 에너지로 적 투사체를 튕겨내며 30% 피해 역반사"),
    ("energy_discharge", "fairy_magic"): ("spark_fairy_storm", "요정 스파크 폭풍", "스킬 시전 시 탄막 수 2배 증가 및 적 전체에 감전 연쇄 피해"),
    ("energy_discharge", "power_overload"): ("hyper_discharge", "하이퍼 과충전", "연속 타격 발동 시 매 타격마다 플라즈마 볼트 탄막이 100% 확정 분출"),
    ("energy_discharge", "thermal_control"): ("plasma_hellfire", "플라즈마 헬파이어", "플라즈마 탄막에 화염이 융합되어 모든 적에게 화상 도트 피해 2배 적용"),
    ("energy_discharge", "ultrasonic_disruption"): ("emp_shockwave", "EMP 충격파", "탄막 타격 시 적의 전자 신경계를 마비시켜 45% 확률로 행동 스킵"),
    ("energy_discharge", "berserker_madness"): ("furious_lightning", "광란의 뇌전", "체력이 낮을수록 에너지 방출 공격력 최대 120% 폭증"),
    ("energy_discharge", "radiation_assimilation"): ("gamma_ray_burst", "감마선 버스트", "보유 Rad 1000당 탄막 피해 +20% 및 적 처치 시 추가 150 Rad 흡수"),
    ("energy_discharge", "meltdown_control"): ("apocalypse_ragnarok", "아포칼립스 파편", "에너지 방출 시 멜트다운 폭발이 연쇄되어 방어력 100% 완전 무시"),
    ("energy_discharge", "hightech_engineering"): ("hardlight_battery", "하드라이트 배터리", "나노 쉴드가 피격될 때마다 에너지가 충전되어 다음 공격력 +50%"),

    # 3. sensory_tech pairs (10)
    ("sensory_tech", "blood_absorption"): ("artery_targeting", "동맥 정밀 타격", "치명타 타격 시 흡혈량이 100%로 3배 증폭"),
    ("sensory_tech", "cellular_shield"): ("predictive_evasion", "예측 회피 기동", "치명타 적중 후 다음 턴 동안 적 공격 완전 회피(무효화) 확률 +35%"),
    ("sensory_tech", "fairy_magic"): ("clairvoyant_mystic", "천리안 신비술", "치명타 발생 시 스킬 공격력 +60% 및 즉시 아군 체력 15% 회복"),
    ("sensory_tech", "power_overload"): ("cyber_overclock", "사이버 오버클럭", "모든 공격 치명타 100% 확정 + 100% 확정 2연속 타격 발동"),
    ("sensory_tech", "thermal_control"): ("laser_pyrolysis", "레이저 열분해", "치명타 적중 시 대상의 화상 디버프를 즉시 폭파하여 300의 추가 폭발 피해"),
    ("sensory_tech", "ultrasonic_disruption"): ("neural_shatter", "뉴럴 셰터", "초음파 기절 확률 65% 폭증 + 기절한 적 타격 시 300% 분쇄 피해"),
    ("sensory_tech", "berserker_madness"): ("death_reckoning", "사선 직감", "체력 35% 이하 시 치명타 피해량이 3.0배로 극대화"),
    ("sensory_tech", "radiation_assimilation"): ("quantum_scanner", "양자 방사능 스캐너", "치명타 발생 시 100% 확률로 80 Rad 즉시 생성"),
    ("sensory_tech", "meltdown_control"): ("critical_meltdown", "임계점 저격", "치명타 적중 시 적 노심을 파괴하여 대상 공격력 30% 영구 감소"),
    ("sensory_tech", "hightech_engineering"): ("hud_tactical_matrix", "HUD 전술 매트릭스", "쉴드가 유지되는 동안 치명타 피해 +80% 및 턴 가속 확률 40%로 상승"),

    # 4. blood_absorption pairs (9)
    ("blood_absorption", "cellular_shield"): ("immortal_carapace", "불사신 갑각", "흡혈로 초과된 회복량이 나노 차폐 쉴드로 자동 전환 (최대 400)"),
    ("blood_absorption", "fairy_magic"): ("vampiric_pixie", "요정의 흡혈 축복", "스킬 발동 시 흡혈량이 아군 전체 회복으로 전환되어 최대 HP 30% 회복"),
    ("blood_absorption", "power_overload"): ("blood_rush", "피의 폭주", "흡혈 성공 시 50% 확률로 즉시 추가 턴 행동"),
    ("blood_absorption", "thermal_control"): ("boiling_blood", "끓어오르는 혈액", "흡혈 시 대상에게 작열 피해를 입히고 공격력 +25% 화염 버프 획득"),
    ("blood_absorption", "ultrasonic_disruption"): ("vampiric_screech", "흡혈박쥐 초음파", "흡혈 성공 시 대상에게 45% 확률로 초음파 기절 부여"),
    ("blood_absorption", "berserker_madness"): ("blood_berserker", "블러드 버서커", "체력이 낮을수록 흡혈량과 공격력이 지수 폭증 (최대 공격력 3배 + 80% 흡혈)"),
    ("blood_absorption", "radiation_assimilation"): ("irradiated_blood", "방사능 오염 혈액", "적의 피를 흡수할 때마다 체내 방사선 정제 (+50 Rad) 및 공격력 +15%"),
    ("blood_absorption", "meltdown_control"): ("sanguine_meltdown", "혈액 노심 용해", "HP 30% 이하 시 흡혈량 100%로 고정 및 피격 피해 50% 반사"),
    ("blood_absorption", "hightech_engineering"): ("nanite_blood_infusion", "나노 혈청 주입", "흡혈 발생 시 나노 쉴드 150 자동 재충전"),

    # 5. cellular_shield pairs (8)
    ("cellular_shield", "fairy_magic"): ("pixie_sanctuary", "요정의 성역", "배리어 유지 중 스킬 공격력 +50% 및 피격 시 요정 가루로 공격 무효화"),
    ("cellular_shield", "power_overload"): ("reactive_dynamo", "반응형 발전기", "배리어가 적 공격을 무효화할 때마다 동력이 완충되어 다음 공격 2연타 확정"),
    ("cellular_shield", "thermal_control"): ("flame_retardant_shell", "내열 단열 외피", "화염/도트 피해 완전 면역 및 피격 시 적에게 화상 반사"),
    ("cellular_shield", "ultrasonic_disruption"): ("sonic_resonance_barrier", "음향 공명 방벽", "배리어가 적 공격을 방어할 때 적 전체에 초음파 기절 파동 방출"),
    ("cellular_shield", "berserker_madness"): ("undying_tenacity", "불굴의 버서커", "체력이 1 이하로 떨어질 위기 시 1회 한정 배리어 3회 즉시 비상 충전"),
    ("cellular_shield", "radiation_assimilation"): ("lead_nanite_coat", "납-나노 차폐 코팅", "받는 모든 물리/방사선 피해 25% 고정 경감 + 영구 방어력 +35%"),
    ("cellular_shield", "meltdown_control"): ("core_containment_vessel", "격납 용기 제어", "노심 폭발 피해를 차폐막이 억제하여 생존력 극대화 및 반사율 +40%"),
    ("cellular_shield", "hightech_engineering"): ("aegis_barrier", "이지스 나노 배리어", "라운드 시작 쉴드량 2배 (HP의 60%) + 매 턴 방어막 200 자동 복구"),

    # 6. fairy_magic pairs (7)
    ("fairy_magic", "power_overload"): ("chrono_fairy", "크로노스 페어리", "스킬 무한 연타 시동 + 35% 확률로 적 턴 강제 스킵"),
    ("fairy_magic", "thermal_control"): ("fairy_will_o_wisp", "요정 도깨비불", "스킬 사용 시 푸른 도깨비불이 적 전체에 번져 지옥화염 3중첩 부착"),
    ("fairy_magic", "ultrasonic_disruption"): ("siren_lullaby", "세이렌의 자장가", "스킬 시전 시 적 전체 50% 확률로 수면/기절 상태 돌입"),
    ("fairy_magic", "berserker_madness"): ("valkyrie_rage", "발키리의 분노", "체력이 낮을수록 스킬 피해량이 최대 2.8배까지 증폭"),
    ("fairy_magic", "radiation_assimilation"): ("aurora_fairy", "오로라 정령", "스킬 시전 시 보유 Rad 비례 광역 섬광 대미지 (Rad 1000당 25% 추가딜)"),
    ("fairy_magic", "meltdown_control"): ("phoenix_rebirth", "불사조 환생", "사망 직전 체력 40%로 즉시 부활하며 요정 스킬 마법 자동 난사"),
    ("fairy_magic", "hightech_engineering"): ("techno_fairy_matrix", "테크노 페어리", "스킬 발동 시 나노 쉴드 250 즉시 전개"),

    # 7. power_overload pairs (6)
    ("power_overload", "thermal_control"): ("overheated_exhaust", "과열 배기 폭발", "2연속 타격 시 2번째 타격에 200 화염 폭발 + 화상 2중첩"),
    ("power_overload", "ultrasonic_disruption"): ("vibrational_impact", "진동 연타 타격", "연속 공격 시 적에게 초음파 뇌진탕 부여 (적 방어력 30% 깎음)"),
    ("power_overload", "berserker_madness"): ("berserk_flurry", "광전사 난무", "체력 40% 이하 시 3연속 타격으로 업그레이드"),
    ("power_overload", "radiation_assimilation"): ("atomic_turbocharger", "원자력 터보차저", "연속 공격 발동 확률이 40% -> 60%로 상승"),
    ("power_overload", "meltdown_control"): ("meltdown_thruster", "멜트다운 추진기", "연속 타격 시마다 피격 반사율 15% 영구 누적 상승"),
    ("power_overload", "hightech_engineering"): ("kinetic_generator", "운동 에너지 발전기", "연속 타격 시 타격당 나노 쉴드 100 충전"),

    # 8. thermal_control pairs (5)
    ("thermal_control", "ultrasonic_disruption"): ("thermo_acoustic_blast", "열음향 폭발", "화상 상태인 적 타격 시 초음파 공명으로 2배 폭발 대미지"),
    ("thermal_control", "berserker_madness"): ("blazing_fury", "타오르는 분노", "체력이 잃을수록 화상 도트 피해가 틱당 최대 12%까지 폭등"),
    ("thermal_control", "radiation_assimilation"): ("dirty_bomb_detonator", "더티밤 기폭장치", "화상 걸린 적이 쓰러지면 방사능 핵분열 폭풍으로 주변 적에 300 광역 피해"),
    ("thermal_control", "meltdown_control"): ("chernobyl_inferno", "체르노빌 연옥", "지옥화염 도트 피해 2배 + 멜트다운 방사능 반사 피해 50%로 상승"),
    ("thermal_control", "hightech_engineering"): ("thermal_shielding", "열차폐 나노 장갑", "피격 시 화염 반사 장벽이 작동하여 공격자에게 즉시 화상 부여"),

    # 9. ultrasonic_disruption pairs (4)
    ("ultrasonic_disruption", "berserker_madness"): ("mind_rending_howl", "정신 분쇄 포효", "체력 35% 이하 시 공격마다 적 전체에 50% 확률 기절 부여"),
    ("ultrasonic_disruption", "radiation_assimilation"): ("gamma_synapse_scrambler", "감마 시냅스 교란기", "기절한 적을 타격할 때마다 120 Rad 강탈"),
    ("ultrasonic_disruption", "meltdown_control"): ("meltdown_panic", "멜트다운 공황", "기절한 적은 멜트다운 방사선에 취약해져 받는 피해 50% 증폭"),
    ("ultrasonic_disruption", "hightech_engineering"): ("sonic_defense_grid", "음향 방어 그리드", "나노 쉴드가 켜져 있을 때 공격한 적에게 35% 확률로 역기절 카운터"),

    # 10. berserker_madness pairs (3)
    ("berserker_madness", "radiation_assimilation"): ("irradiated_berserker", "피폭의 광전사", "보유 Rad 1000당 잃은 체력 비례 공격력 상승폭 20% 추가 증가"),
    ("berserker_madness", "meltdown_control"): ("suicide_meltdown", "임계돌파 자폭기", "체력 25% 이하 시 모든 공격력 3배 + 받는 피해의 70%를 적에게 반사"),
    ("berserker_madness", "hightech_engineering"): ("adrenalin_exoskeleton", "아드레날린 외골격", "체력이 50% 이하가 되면 나노 쉴드 500이 1회 비상 긴급 전개"),

    # 11. radiation_assimilation pairs (2)
    ("radiation_assimilation", "meltdown_control"): ("chernobyl_meltdown", "체르노빌 임계돌파", "방사능 피해 반사 50% + 공격 시 체르노빌 핵분열 폭풍 발동"),
    ("radiation_assimilation", "hightech_engineering"): ("radiation_converter", "방사선 변환 반응로", "라운드 시작 시 보유 Rad 1000당 나노 쉴드 150 추가 생성"),

    # 12. meltdown_control pairs (1)
    ("meltdown_control", "hightech_engineering"): ("core_reinforcement", "노심 보강 프레임", "나노 쉴드가 활성화되어 있어도 멜트다운 30% 피해 반사가 100% 정상 작동")
}

print(f"Total configured pairs: {len(FUSIONS_CONFIG)}")
assert len(FUSIONS_CONFIG) == 78, f"Expected 78 pairs, got {len(FUSIONS_CONFIG)}"

# Generate JS code string
js_lines = ["const FUSION_DATA = {"]
for i, ((t1, t2), (f_id, name, desc)) in enumerate(FUSIONS_CONFIG.items()):
    comma = "," if i < 77 else ""
    js_lines.append(f'  {f_id}: {{')
    js_lines.append(f'    id: "{f_id}",')
    js_lines.append(f'    name: "{name}",')
    js_lines.append(f'    req: ["{t1}", "{t2}"],')
    js_lines.append(f'    description: "{desc}"')
    js_lines.append(f'  }}{comma}')
js_lines.append("};")

js_code = "\n".join(js_lines)

with open("scratch/generated_78_fusions.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print("Successfully written scratch/generated_78_fusions.js")
