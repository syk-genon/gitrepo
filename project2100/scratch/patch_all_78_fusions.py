import re

# Read original index.js
with open("index.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update getDerivedStats
old_stats_marker = "// 융합 시너지 스탯 효과"
new_stats_block = """  // 융합 시너지 스탯 효과
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
  }"""

code = re.sub(
    r"  // 융합 시너지 스탯 효과[\s\S]*?return derived;",
    new_stats_block + "\n\n  return derived;",
    code
)

# 2. Update initBattleStage
new_init_stage = """function initBattleStage() {
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
  STATE.meltdownThrusterBonus = 0;"""

code = re.sub(
    r"function initBattleStage\(\) \{[\s\S]*?STATE\.phoenixUsed = false;",
    new_init_stage,
    code
)

# 3. Update executeCombatTurn
new_combat_turn = """// 전투 턴 로직 (13대 특성 및 78대 초월 융합 시스템 완전 가동)
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
}"""

code = re.sub(
    r"// 전투 턴 로직[\s\S]*?function calculateDamage",
    new_combat_turn + "\n\n// 대미지 공식 연산\nfunction calculateDamage",
    code
)

# 4. Clean up handlePlayerDefeat (remove immortal_leviathan dead code)
new_defeat = """// 요원 전멸
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
  }"""

code = re.sub(
    r"// 요원 전멸[\s\S]*?stopBattleLoop\(\);",
    new_defeat + "\n\n  stopBattleLoop();",
    code
)

# Write updated code
with open("index.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Applied 78 fusions to index.js successfully!")
