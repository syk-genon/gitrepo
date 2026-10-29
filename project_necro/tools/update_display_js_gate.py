# -*- coding: utf-8 -*-
import os

js_path = r"D:\workspace\GEMINI\project_necro\display.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# 1. Also update townHeroImg and battleHeroSpriteImg inside selectClass()
old_select_end = """    updateHeroSprite();
    renderClassSetItems();
    renderClassSkills();
}"""

new_select_end = """    updateHeroSprite();
    renderClassSetItems();
    renderClassSkills();
    const townHeroImg = document.getElementById('townHeroImg');
    if (townHeroImg && cData.sprite) townHeroImg.src = cData.sprite;
    const battleHeroImg = document.getElementById('battleHeroSpriteImg');
    if (battleHeroImg && cData.sprite) battleHeroImg.src = cData.sprite;
}"""

if old_select_end in js:
    js = js.replace(old_select_end, new_select_end, 1)

# 2. Replace section 6 (switchRegionTheme) with the complete Gate + 6-Wave + 84 Monsters interactive system
start_marker = "// 6. 지역 전환 및 라이브 전장 렌더링"
end_marker = "// 7. 전 12개 직업 72종 전용 스킬 VFX 도감"

s_idx = js.find(start_marker)
e_idx = js.find(end_marker)
assert s_idx != -1 and e_idx != -1

new_gate_js = """// 6. 14대 지역별 [마을 ➔ 6대 차원문(Gate) 진입 ➔ 6웨이브(84종 괴수) 실전 시뮬레이터]
let currentRegionId = 1;
let currentGateWave = 1;
let currentWaveMonsterHp = 100;
let currentWaveMonsterMaxHp = 100;
let isHeroInsideGate = false;

function getWaveMonsterMeta(rId, waveNum) {
    const rData = REGIONS_DATA[rId] || REGIONS_DATA[1];
    const gData = (typeof GATES_DATA !== 'undefined' && GATES_DATA[rData.gateType]) ? GATES_DATA[rData.gateType] : { name: "🚪 철문", color: "#a8b4c4", rewardGold: 1500 };
    const regionScale = Math.pow(1.45, rId - 1);
    const waveScale = 1 + (waveNum - 1) * 0.28;

    let spritePath = `assets/monsters/m_${rId}_${waveNum}.png`;
    let monsterName = (rData.monsters && rData.monsters[waveNum - 1]) ? rData.monsters[waveNum - 1] : `지역 ${rId} 괴수 #${waveNum}`;
    let roleLabel = `WAVE ${waveNum}/6 · 일반 괴수`;
    let hpMult = 1.0;

    if (waveNum === 5) {
        spritePath = `assets/monsters/m_${rId}_named.png`;
        monsterName = rData.named || `지역 ${rId} 수문장`;
        roleLabel = `WAVE 5/6 · ⚡ 차원문 수문장 (Named)`;
        hpMult = 4.2;
    } else if (waveNum === 6) {
        spritePath = `assets/monsters/m_${rId}_boss.png`;
        monsterName = rData.boss || `지역 ${rId} 보스`;
        roleLabel = `WAVE 6/6 · 👑 차원문 지배자 (BOSS)`;
        hpMult = 12.0;
    }

    const maxHp = Math.round(1200 * regionScale * waveScale * hpMult);
    return {
        rId,
        waveNum,
        spritePath,
        monsterName,
        roleLabel,
        maxHp,
        gateData: gData
    };
}

function switchRegionTheme(rId) {
    currentRegionId = rId;
    const rData = REGIONS_DATA[rId] || REGIONS_DATA[1];
    const gData = (typeof GATES_DATA !== 'undefined' && GATES_DATA[rData.gateType]) ? GATES_DATA[rData.gateType] : GATES_DATA["iron"];

    document.querySelectorAll('#regionSelectorTabs .btn-chip').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.region, 10) === rId);
    });

    // 상단 타이틀 및 차원문 배지 갱신
    const titleEl = document.getElementById('currentRegionTitle');
    if (titleEl) titleEl.textContent = `📍 [${rId}지역] ${rData.name}`;

    const gateBadge = document.getElementById('currentGateBadge');
    if (gateBadge && gData) {
        gateBadge.textContent = `${gData.name} · ${gData.tier}`;
        gateBadge.style.borderColor = gData.color;
        gateBadge.style.color = gData.color;
    }

    // 차원문 고유 특성 & 배경 설명 패널 갱신
    const fTitle = document.getElementById('gateFeatureTitle');
    if (fTitle && gData) {
        fTitle.innerHTML = `<span style="color:${gData.color};">${gData.name}</span> — [${rId}지역: ${rData.name}] 고유 환경`;
    }
    const fDesc = document.getElementById('gateFeatureDesc');
    if (fDesc) fDesc.textContent = rData.gateFeature || "";

    const rTrait = document.getElementById('gateRegionTrait');
    if (rTrait) rTrait.textContent = `획득/공명 특성: ${rData.traitName || "🌀 마력 호흡"}`;

    const envMod = document.getElementById('gateEnvModifier');
    if (envMod && gData) envMod.textContent = gData.envModifier || "";

    const dropBonus = document.getElementById('gateDropBonus');
    if (dropBonus && gData) dropBonus.textContent = gData.dropBonus || "";

    const bossSum = document.getElementById('gateBossSummary');
    if (bossSum) bossSum.textContent = `수문장: ${rData.named} / 보스: ${rData.boss}`;

    // 마을 배경 & 전투 배경 고유 이미지 적용 (1~14지역 모두 개별 에셋)
    const townView = document.getElementById('townBgView');
    if (townView) townView.style.backgroundImage = `url('${rData.town}')`;

    const battleView = document.getElementById('battleBgView');
    if (battleView) battleView.style.backgroundImage = `url('${rData.battle}')`;

    // 마을 내 차원문 오브젝트 & 전투장 미니 입구 포털 스프라이트 교체
    const townGateImg = document.getElementById('townGateSprite');
    if (townGateImg && gData) townGateImg.src = gData.sprite;

    const townGateGlow = document.getElementById('townGateGlow');
    if (townGateGlow && gData) townGateGlow.style.background = gData.color;

    const btnEnterGate = document.getElementById('btnEnterGateAction');
    if (btnEnterGate && gData) {
        btnEnterGate.style.borderColor = gData.color;
        btnEnterGate.style.color = gData.color;
        btnEnterGate.textContent = `${gData.name.split(' ')[0]} ${gData.name.split(' ')[1]} 진입 ▶`;
    }

    const miniGate = document.getElementById('battleEntranceGateMini');
    if (miniGate && gData) miniGate.src = gData.sprite;

    // 지역 변경 시 기본 1웨이브부터 표시 및 하단 6종 몬스터 로스터 렌더링
    renderRegionMonstersRoster(rId);
    setGateWave(1);
}

function renderRegionMonstersRoster(rId) {
    const grid = document.getElementById('regionMonstersRosterGrid');
    if (!grid) return;

    let cardsHtml = '';
    for (let w = 1; w <= 6; w++) {
        const meta = getWaveMonsterMeta(rId, w);
        const isBoss = w === 6;
        const isNamed = w === 5;
        const borderCol = isBoss ? 'var(--neon-pink)' : (isNamed ? 'var(--neon-cyan)' : 'var(--border-wood-light)');
        const tagText = isBoss ? '👑 W6 보스' : (isNamed ? '⚡ W5 수문장' : `👾 W${w} 일반`);
        const tagCol = isBoss ? 'var(--neon-pink)' : (isNamed ? 'var(--neon-cyan)' : 'var(--neon-gold)');

        cardsHtml += `
            <div onclick="setGateWave(${w})" style="cursor:pointer; background:rgba(15,11,8,0.9); border:2px solid ${currentGateWave === w ? 'var(--neon-gold)' : borderCol}; padding:8px; text-align:center; border-radius:4px; transition:transform 0.15s;" onmouseover="this.style.transform='translateY(-3px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size:0.65rem; color:${tagCol}; margin-bottom:4px; font-weight:bold;">${tagText}</div>
                <div style="height:68px; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.45); border:1px solid #2a1f18; margin-bottom:5px;">
                    <img src="${meta.spritePath}" alt="${meta.monsterName}" style="max-width:62px; max-height:62px; object-fit:contain; image-rendering:pixelated; transform:scaleX(-1);">
                </div>
                <div style="font-size:0.7rem; color:var(--text-ivory); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${meta.monsterName}</div>
                <div style="font-size:0.62rem; color:var(--text-muted); margin-top:2px;">HP ${meta.maxHp.toLocaleString()}</div>
            </div>
        `;
    }
    grid.innerHTML = cardsHtml;
}

function setGateWave(waveNum) {
    currentGateWave = waveNum;
    const meta = getWaveMonsterMeta(currentRegionId, waveNum);
    currentWaveMonsterMaxHp = meta.maxHp;
    currentWaveMonsterHp = meta.maxHp;

    document.querySelectorAll('#gateWaveStepsBar .btn-chip').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.wave, 10) === waveNum);
    });

    const waveBadge = document.getElementById('battleStageWaveBadge');
    if (waveBadge) waveBadge.textContent = meta.roleLabel;

    const bossNameEl = document.getElementById('battleBossName');
    if (bossNameEl) bossNameEl.textContent = meta.monsterName;

    const roleTag = document.getElementById('battleMonsterRoleTag');
    if (roleTag) {
        roleTag.textContent = `${meta.roleLabel} · ${meta.monsterName}`;
        roleTag.style.color = waveNum === 6 ? 'var(--neon-pink)' : (waveNum === 5 ? 'var(--neon-cyan)' : 'var(--neon-gold)');
    }

    const bossSprite = document.getElementById('battleBossSprite');
    if (bossSprite) {
        bossSprite.style.backgroundImage = `url('${meta.spritePath}')`;
        bossSprite.style.width = waveNum === 6 ? '152px' : (waveNum === 5 ? '138px' : '118px');
        bossSprite.style.height = waveNum === 6 ? '152px' : (waveNum === 5 ? '138px' : '118px');
        bossSprite.style.transform = 'scaleX(-1) scale(1)';
        bossSprite.style.filter = 'drop-shadow(0 4px 10px rgba(0,0,0,0.9))';
    }

    updateGateWaveHpUI();
    renderRegionMonstersRoster(currentRegionId);
}

function updateGateWaveHpUI() {
    const pct = Math.max(0, Math.min(100, Math.round((currentWaveMonsterHp / currentWaveMonsterMaxHp) * 100)));
    const bar = document.getElementById('battleMonsterHpBar');
    if (bar) bar.style.width = `${pct}%`;
    const txt = document.getElementById('battleMonsterHpText');
    if (txt) txt.textContent = `HP: ${currentWaveMonsterHp.toLocaleString()} / ${currentWaveMonsterMaxHp.toLocaleString()} (${pct}%)`;
}

function enterRegionGate() {
    const rData = REGIONS_DATA[currentRegionId] || REGIONS_DATA[1];
    const gData = GATES_DATA[rData.gateType] || GATES_DATA["iron"];
    const townHero = document.getElementById('townHeroActor');
    const townBadge = document.getElementById('townStatusBadge');
    const flashOverlay = document.getElementById('gatePortalFlashOverlay');
    const battleHeroBox = document.getElementById('battleHeroPartyBox');
    const battleHeroTag = document.getElementById('battleHeroStatusTag');
    const logBar = document.getElementById('gateBattleLogBar');

    // 1. 마을 영웅이 차원문 쪽으로 이동 후 포털 속으로 빨려들어가는 애니메이션
    if (townHero) {
        townHero.style.left = 'calc(100% - 145px)';
        townHero.style.transform = 'scale(0.35) rotate(12deg)';
        townHero.style.opacity = '0.15';
    }
    if (townBadge) {
        townBadge.textContent = `🚪 ${gData.name} 진입 완료 (전투 중)`;
        townBadge.style.color = gData.color;
        townBadge.style.borderColor = gData.color;
    }

    // 2. 차원문 워프 플래시 연출
    if (flashOverlay) {
        flashOverlay.style.background = `radial-gradient(circle, ${gData.color}dd, rgba(0,0,0,0.95))`;
        flashOverlay.innerHTML = `🌀 [${currentRegionId}지역] ${gData.name} 차원 도약 중...`;
        flashOverlay.style.opacity = '1';
        setTimeout(() => {
            flashOverlay.style.opacity = '0';
        }, 420);
    }

    // 3. 우측 전투 전장에 영웅(우향 Facing Right) 등장 및 Wave 1 개시
    setTimeout(() => {
        isHeroInsideGate = true;
        if (battleHeroBox) {
            battleHeroBox.style.opacity = '1';
            battleHeroBox.style.transform = 'translateX(10px)';
        }
        if (battleHeroTag) {
            battleHeroTag.textContent = `⚔️ 교전 중 (${CLASSES_DATA[currentClassId].name})`;
        }
        setGateWave(1);
        if (logBar) {
            logBar.innerHTML = `🚪 <strong>${gData.name}</strong> 내부로 진입했습니다! 환경 효과: <span style="color:var(--neon-cyan);">${gData.envModifier}</span>`;
        }
    }, 320);
}

function returnToTownFromGate() {
    isHeroInsideGate = false;
    const townHero = document.getElementById('townHeroActor');
    const townBadge = document.getElementById('townStatusBadge');
    const battleHeroBox = document.getElementById('battleHeroPartyBox');
    const battleHeroTag = document.getElementById('battleHeroStatusTag');
    const logBar = document.getElementById('gateBattleLogBar');

    if (townHero) {
        townHero.style.left = '36px';
        townHero.style.transform = 'scale(1) rotate(0deg)';
        townHero.style.opacity = '1';
    }
    if (townBadge) {
        townBadge.textContent = '🟢 마을 대기 중 (문을 클릭해 입장)';
        townBadge.style.color = 'var(--neon-green)';
        townBadge.style.borderColor = 'var(--neon-green)';
    }
    if (battleHeroBox) {
        battleHeroBox.style.opacity = '0.45';
        battleHeroBox.style.transform = 'translateX(0)';
    }
    if (battleHeroTag) {
        battleHeroTag.textContent = '차원문 입장 대기';
    }
    if (logBar) {
        logBar.innerHTML = `🏘️ 차원문을 빠져나와 생존자 안전 거점 마을로 귀환했습니다.`;
    }
}

function attackGateWaveMonster() {
    if (!isHeroInsideGate) {
        enterRegionGate();
        return;
    }

    const cData = CLASSES_DATA[currentClassId];
    const attackSkills = cData.skills.filter(s => s.target !== 'self');
    const chosenSkill = attackSkills.length > 0 ? attackSkills[Math.floor(Math.random() * attackSkills.length)] : cData.skills[0];

    const vfxLayer = document.getElementById('gateBattleVfxLayer');
    const bossSprite = document.getElementById('battleBossSprite');
    const logBar = document.getElementById('gateBattleLogBar');

    // 데미지 계산 (2~3타 내 격파)
    const dmg = Math.round(currentWaveMonsterMaxHp * (0.42 + Math.random() * 0.25));
    currentWaveMonsterHp = Math.max(0, currentWaveMonsterHp - dmg);
    updateGateWaveHpUI();

    if (bossSprite) {
        bossSprite.style.transform = 'scaleX(-1) translateX(-14px) scale(0.92)';
        bossSprite.style.filter = 'brightness(2.8) drop-shadow(0 0 18px #ff2a6d)';
        setTimeout(() => {
            bossSprite.style.transform = 'scaleX(-1) scale(1)';
            bossSprite.style.filter = 'drop-shadow(0 4px 10px rgba(0,0,0,0.9))';
        }, 180);
    }

    if (vfxLayer) {
        const fx = document.createElement('div');
        fx.style.cssText = 'position:absolute; right:45px; bottom:45px; display:flex; flex-direction:column; align-items:center; pointer-events:none; animation:vfxPop 0.55s ease-out forwards;';
        fx.innerHTML = `
            <div style="color:var(--neon-gold); font-size:1.05rem; font-weight:bold; text-shadow:2px 2px 0 #000, 0 0 10px #ff0055;">-${dmg.toLocaleString()}!</div>
            <img src="${chosenSkill.vfx}" style="width:92px; height:92px; object-fit:contain; image-rendering:pixelated;">
        `;
        vfxLayer.appendChild(fx);
        setTimeout(() => fx.remove(), 550);
    }

    const meta = getWaveMonsterMeta(currentRegionId, currentGateWave);
    if (currentWaveMonsterHp <= 0) {
        if (currentGateWave < 6) {
            if (logBar) {
                logBar.innerHTML = `💥 <strong>[${chosenSkill.name}]</strong> 적중! <strong>${meta.monsterName}</strong> 처치 완료! 다음 웨이브(Wave ${currentGateWave + 1}/6)로 전진합니다!`;
            }
            setTimeout(() => {
                if (currentWaveMonsterHp <= 0) setGateWave(currentGateWave + 1);
            }, 480);
        } else {
            // 6웨이브 보스 처치 -> 차원문 완전 클리어 보상!
            const rData = REGIONS_DATA[currentRegionId] || REGIONS_DATA[1];
            const gData = GATES_DATA[rData.gateType] || GATES_DATA["iron"];
            regressionState.gold += gData.rewardGold;
            renderRegressionUi();
            if (logBar) {
                logBar.innerHTML = `🏆 <strong>[${gData.name} 완전 정복!]</strong> 최종 보스 <strong>${meta.monsterName}</strong> 격파! 보상으로 <strong>+${gData.rewardGold.toLocaleString()} Gold</strong> 및 <strong>[${rData.traitName}]</strong> 공명을 획득했습니다!`;
            }
        }
    } else {
        if (logBar) {
            logBar.innerHTML = `⚡ <strong>[${chosenSkill.name}]</strong> 시전! <strong>${meta.monsterName}</strong>에게 <span style="color:var(--neon-pink);">-${dmg.toLocaleString()}</span> 피해!`;
        }
    }
}

function nextGateWave() {
    if (!isHeroInsideGate) {
        enterRegionGate();
    }
    const nextW = currentGateWave < 6 ? currentGateWave + 1 : 1;
    setGateWave(nextW);
}

"""

updated_js = js[:s_idx] + new_gate_js + js[e_idx:]
with open(js_path, "w", encoding="utf-8") as f:
    f.write(updated_js)
print("Successfully updated display.js with Gate & 6-Wave combat engine.")
