# -*- coding: utf-8 -*-
import re

with open("D:/workspace/GEMINI/project_necro/index.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. gameState.player 에 lastSaveTime 추가
code = code.replace(
    'maxRegionUnlocked: 1\n    },',
    'maxRegionUnlocked: 1,\n        lastSaveTime: Date.now()\n    },'
)

# 2. gameState.battle 에 autoNextRegion 및 세션 통계 추가
code = code.replace(
    'auto: true,\n        playerCooldowns: {},',
    'auto: true,\n        autoNextRegion: false,\n        sessionDamage: 0,\n        sessionGold: 0,\n        sessionKills: 0,\n        sessionStartTime: 0,\n        playerCooldowns: {},'
)

# 3. saveGameState 에 lastSaveTime 갱신
old_save = '''function saveGameState(notify = false) {
    try {
        localStorage.setItem(SAVE_KEY, JSON.stringify({ player: gameState.player }));'''

new_save = '''function saveGameState(notify = false) {
    try {
        gameState.player.lastSaveTime = Date.now();
        localStorage.setItem(SAVE_KEY, JSON.stringify({ player: gameState.player }));'''

code = code.replace(old_save, new_save)

# 4. loadGameState 끝에 checkOfflineProgress() 및 syncSoundButtons() 호출
old_load_end = '''                if (gameState.player.talents) {
                    Object.keys(gameState.player.talents).forEach(k => {
                        if (!TALENTS_DATA[k]) delete gameState.player.talents[k];
                    });
                }
            }
        }
    } catch (e) {
        console.error("세이브 로드 오류:", e);
    }
}'''

new_load_end = '''                if (gameState.player.talents) {
                    Object.keys(gameState.player.talents).forEach(k => {
                        if (!TALENTS_DATA[k]) delete gameState.player.talents[k];
                    });
                }
            }
        }
        checkOfflineProgress();
        syncSoundButtons();
    } catch (e) {
        console.error("세이브 로드 오류:", e);
    }
}'''

code = code.replace(old_load_end, new_load_end)

# 5. 오프라인 방치 보상 및 사운드/연속돌파 제어 함수 추가
helper_functions = '''
// =========================================================================
// 고도화 2: 오프라인 방치 보상 시스템 (Idle Offline Progression)
// =========================================================================
let pendingOfflineRewards = null;

function checkOfflineProgress() {
    if (!gameState.player || !gameState.player.lastSaveTime) return;
    const now = Date.now();
    const elapsedMs = now - gameState.player.lastSaveTime;
    const elapsedMinutes = Math.floor(elapsedMs / (1000 * 60));

    // 최소 1분 이상 부재 시 방치 보상 계산 (최대 12시간 = 720분)
    if (elapsedMinutes >= 1) {
        const cappedMinutes = Math.min(720, elapsedMinutes);
        const maxReg = Math.max(1, gameState.player.maxRegionUnlocked || 1);
        const regCount = gameState.player.regressionCount || 0;
        const multiplier = 1 + (regCount * 0.15);

        const earnedGold = Math.floor(cappedMinutes * 120 * maxReg * multiplier);
        const earnedExp = Math.floor(cappedMinutes * 45 * maxReg * multiplier);

        pendingOfflineRewards = {
            minutes: cappedMinutes,
            gold: earnedGold,
            exp: earnedExp,
            maxReg: maxReg
        };

        const hours = Math.floor(cappedMinutes / 60);
        const mins = cappedMinutes % 60;
        const durEl = document.getElementById("offlineDurationText");
        const regEl = document.getElementById("offlineMaxRegionText");
        const goldEl = document.getElementById("offlineGoldText");
        const expEl = document.getElementById("offlineExpText");
        const modal = document.getElementById("modal-offline-reward");

        if (durEl) durEl.textContent = `${hours}시간 ${mins}분`;
        if (regEl) regEl.textContent = `지역 ${maxReg}`;
        if (goldEl) goldEl.textContent = `+${earnedGold.toLocaleString()}`;
        if (expEl) expEl.textContent = `+${earnedExp.toLocaleString()}`;
        if (modal) modal.classList.add("active");
    }
}

function claimOfflineRewards() {
    if (pendingOfflineRewards) {
        gameState.player.gold += pendingOfflineRewards.gold;
        gainExp(pendingOfflineRewards.exp);
        SoundEngine.levelUp();
        showFloatingText(document.body, `🎁 방치 보상: +${pendingOfflineRewards.gold.toLocaleString()}G / +${pendingOfflineRewards.exp.toLocaleString()} EXP 수령!`, "var(--neon-gold)");
        pendingOfflineRewards = null;
        saveGameState(false);
        refreshHubUI();
    }
    const modal = document.getElementById("modal-offline-reward");
    if (modal) modal.classList.remove("active");
}

function toggleSoundEngine() {
    const isEnabled = SoundEngine.toggle();
    syncSoundButtons();
    if (isEnabled) {
        SoundEngine.click();
        const curScreen = document.querySelector(".game-screen.active");
        if (curScreen && curScreen.id === "screen-battle") SoundEngine.startBgm('battle');
        else if (curScreen && curScreen.id === "screen-hub") SoundEngine.startBgm('hub');
    }
}

function syncSoundButtons() {
    const label = SoundEngine.enabled ? "🔊 ON" : "🔇 OFF";
    const fullLabel = SoundEngine.enabled ? "🔊 소리: ON" : "🔇 소리: OFF";
    const bStart = document.getElementById("btnSoundToggleStart");
    const bHub = document.getElementById("btnSoundToggleHub");
    const bBat = document.getElementById("btnSoundToggleBattle");
    if (bStart) bStart.textContent = fullLabel;
    if (bHub) bHub.textContent = fullLabel;
    if (bBat) bBat.textContent = label;
}

function toggleAutoNextRegion() {
    gameState.battle.autoNextRegion = !gameState.battle.autoNextRegion;
    const btn = document.getElementById("btnAutoNextRegion");
    if (btn) {
        btn.textContent = gameState.battle.autoNextRegion ? "🔄 연속 돌파: ON" : "🔄 연속 돌파: OFF";
        btn.style.color = gameState.battle.autoNextRegion ? "var(--neon-green)" : "var(--neon-purple)";
    }
    SoundEngine.click();
}
'''

# 6. switchScreen 에 BGM 전환 추가
old_switch = '''        if (screenId === "screen-hub") {
            refreshHubUI();
        }'''

new_switch = '''        if (screenId === "screen-hub") {
            refreshHubUI();
            SoundEngine.startBgm('hub');
        } else if (screenId === "screen-battle") {
            SoundEngine.startBgm('battle');
        } else if (screenId === "screen-start") {
            SoundEngine.stopBgm();
        }'''

code = code.replace(old_switch, new_switch)

# 7. toggleBattleSpeed 에 8배속 지원
old_speed = '''function toggleBattleSpeed() {
    if (gameState.battle.speed === 1) gameState.battle.speed = 2;
    else if (gameState.battle.speed === 2) gameState.battle.speed = 4;
    else gameState.battle.speed = 1;

    const btn = document.getElementById("btnBattleSpeed");
    if (btn) btn.textContent = `⚡ 배속: ${gameState.battle.speed}x`;
}'''

new_speed = '''function toggleBattleSpeed() {
    if (gameState.battle.speed === 1) gameState.battle.speed = 2;
    else if (gameState.battle.speed === 2) gameState.battle.speed = 4;
    else if (gameState.battle.speed === 4) gameState.battle.speed = 8;
    else gameState.battle.speed = 1;

    const btn = document.getElementById("btnBattleSpeed");
    if (btn) {
        btn.textContent = gameState.battle.speed === 8 ? "⚡ 8x (초고속)" : `⚡ ${gameState.battle.speed}x`;
        btn.style.color = gameState.battle.speed >= 4 ? "var(--neon-pink)" : "var(--neon-gold)";
    }
    SoundEngine.click();
}'''

code = code.replace(old_speed, new_speed)

# 8. startGateBattle 에 통계 초기화 및 BGM 시작
old_start_battle = '''    gameState.battle.playerAttackTimer = 0;
    gameState.battle.enemyAttackTimer = 0;
    gameState.battle.autoCastTimer = 0;'''

new_start_battle = '''    gameState.battle.playerAttackTimer = 0;
    gameState.battle.enemyAttackTimer = 0;
    gameState.battle.autoCastTimer = 0;
    gameState.battle.sessionDamage = 0;
    gameState.battle.sessionGold = 0;
    gameState.battle.sessionKills = 0;
    gameState.battle.sessionStartTime = performance.now();
    SoundEngine.startBgm('battle');'''

code = code.replace(old_start_battle, new_start_battle)

# 9. spawnWaveMonster 에서 보스 경보 사운드
old_spawn_boss = '''    if (w === 6) {
        logBattleMessage(`🚨 [경고] 보스 몬스터 [${mon.name}]이(가) 등장했습니다!`);
    }'''

new_spawn_boss = '''    if (w === 6) {
        logBattleMessage(`🚨 [경고] 보스 몬스터 [${mon.name}]이(가) 등장했습니다!`);
        SoundEngine.boss();
    }'''

code = code.replace(old_spawn_boss, new_spawn_boss)

# 10. executeSkillLogic 에 스킬 사운드 및 통계 누적
old_skill_exec = '''        e.hp -= dealtDmg;
        triggerScreenShake(isUlt);'''

new_skill_exec = '''        e.hp -= dealtDmg;
        gameState.battle.sessionDamage += dealtDmg;
        if (isCrit) SoundEngine.crit(); else SoundEngine.hit();
        triggerScreenShake(isUlt);'''

code = code.replace(old_skill_exec, new_skill_exec)

# 11. playSkillSequence 에서 skill sound
old_play_seq = '''function playSkillSequence(skill, isUlt) {
    const overlay = document.getElementById("battleVfxOverlay");
    if (!overlay) return;'''

new_play_seq = '''function playSkillSequence(skill, isUlt) {
    SoundEngine.skill();
    const overlay = document.getElementById("battleVfxOverlay");
    if (!overlay) return;'''

code = code.replace(old_play_seq, new_play_seq)

# 12. playerBasicAttack 에서 타격 사운드 및 통계
old_basic_atk = '''    e.hp -= dmg;
    triggerScreenShake(false);'''

new_basic_atk = '''    e.hp -= dmg;
    gameState.battle.sessionDamage += dmg;
    if (isCrit) SoundEngine.crit(); else SoundEngine.hit();
    triggerScreenShake(false);'''

code = code.replace(old_basic_atk, new_basic_atk)

# 13. usePotion 사운드
old_use_potion = '''    gameState.player.potions[type] -= 1;'''
new_use_potion = '''    gameState.player.potions[type] -= 1;
    SoundEngine.potion();'''
code = code.replace(old_use_potion, new_use_potion, 1)

# 14. performEnhancement 사운드
old_enhance_success = '''    const resultEl = document.getElementById("forgeResultMsg");
    if (resultEl) {
        resultEl.textContent = `✨ 강화 성공! ${item.name}이(가) +${item.enhance}강이 되었습니다!`;
        resultEl.style.color = "var(--neon-gold)";
    }'''

new_enhance_success = '''    SoundEngine.enhance();
    const resultEl = document.getElementById("forgeResultMsg");
    if (resultEl) {
        resultEl.textContent = `✨ 강화 성공! ${item.name}이(가) +${item.enhance}강이 되었습니다!`;
        resultEl.style.color = "var(--neon-gold)";
    }'''

code = code.replace(old_enhance_success, new_enhance_success)

# 15. onEnemyDefeated 에 킬/골드 통계 및 연속 돌파 (Auto Next Region)
old_boss_clear = '''        // 보스 격파 -> 승리 모달
        gameState.battle.active = false;
        const curR = gameState.battle.regionId;
        if (gameState.player.maxRegionUnlocked <= curR && curR < 14) {
            gameState.player.maxRegionUnlocked = curR + 1;
        }

        const victoryGold = Math.floor(reg.baseGold * 4.5);
        const victoryExp = Math.floor(reg.baseExp * 4.0);
        gameState.player.gold += victoryGold;
        gainExp(victoryExp);

        saveGameState(false);
        openVictoryModal(victoryGold, victoryExp);'''

new_boss_clear = '''        // 보스 격파
        gameState.battle.active = false;
        SoundEngine.levelUp();
        const curR = gameState.battle.regionId;
        if (gameState.player.maxRegionUnlocked <= curR && curR < 14) {
            gameState.player.maxRegionUnlocked = curR + 1;
        }

        const victoryGold = Math.floor(reg.baseGold * 4.5);
        const victoryExp = Math.floor(reg.baseExp * 4.0);
        gameState.player.gold += victoryGold;
        gameState.battle.sessionGold += victoryGold;
        gainExp(victoryExp);

        saveGameState(false);

        if (gameState.battle.autoNextRegion) {
            showFloatingText(document.body, `🏆 [지역 ${curR}] 정복 완료! 1.5초 후 다음 차원문으로 진격합니다...`, "var(--neon-gold)");
            setTimeout(() => {
                const nextR = Math.min(14, curR + 1);
                startGateBattle(nextR);
            }, 1500);
        } else {
            openVictoryModal(victoryGold, victoryExp);
        }'''

code = code.replace(old_boss_clear, new_boss_clear)

# 일반 몬스터 처치 시 통계
old_mob_defeat = '''        gameState.player.gold += goldDrop;
        gainExp(expDrop);'''

new_mob_defeat = '''        gameState.player.gold += goldDrop;
        gameState.battle.sessionGold += goldDrop;
        gameState.battle.sessionKills += 1;
        gainExp(expDrop);'''

code = code.replace(old_mob_defeat, new_mob_defeat)

# 16. gameLoop 에 DPS 및 전투 통계 실시간 갱신 추가
old_gameloop_end = '''        // 적 몬스터 공격
        gameState.battle.enemyAttackTimer += delta * spd;
        if (gameState.battle.enemyAttackTimer >= 2.4) {
            gameState.battle.enemyAttackTimer = 0;
            executeEnemyAttack();
        }
    }

    requestAnimationFrame(gameLoop);'''

new_gameloop_end = '''        // 적 몬스터 공격
        gameState.battle.enemyAttackTimer += delta * spd;
        if (gameState.battle.enemyAttackTimer >= 2.4) {
            gameState.battle.enemyAttackTimer = 0;
            executeEnemyAttack();
        }

        // 실시간 DPS 및 세션 통계 갱신
        const elapsedSec = (performance.now() - (gameState.battle.sessionStartTime || performance.now())) / 1000;
        const liveDps = elapsedSec > 0.4 ? Math.floor(gameState.battle.sessionDamage / elapsedSec) : 0;
        const dpsEl = document.getElementById("battleLiveDpsText");
        const goldEl = document.getElementById("battleSessionGoldText");
        const killsEl = document.getElementById("battleSessionKillsText");
        if (dpsEl) dpsEl.textContent = liveDps.toLocaleString();
        if (goldEl) goldEl.textContent = (gameState.battle.sessionGold || 0).toLocaleString();
        if (killsEl) killsEl.textContent = (gameState.battle.sessionKills || 0).toLocaleString();
    }

    requestAnimationFrame(gameLoop);'''

code = code.replace(old_gameloop_end, new_gameloop_end)

# helper_functions 를 switchScreen 앞에 삽입
code = code.replace('function switchScreen(screenId) {', helper_functions + '\nfunction switchScreen(screenId) {')

with open("D:/workspace/GEMINI/project_necro/index.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Upgrade complete! File written.")
