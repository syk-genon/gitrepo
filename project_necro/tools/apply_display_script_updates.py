# -*- coding: utf-8 -*-
"""
Applies monster ground/flying mechanics, updated prop labels, and cache busters to display.js and display.html.
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update display.js
with open('project_necro/display.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Update getWaveMonsterMeta
old_get_wave = r'function getWaveMonsterMeta\(rId, waveNum\) \{[\s\S]*?\n\}'
new_get_wave = """function getWaveMonsterMeta(rId, waveNum) {
    const rData = REGIONS_DATA[rId] || REGIONS_DATA[1];
    const gData = (typeof GATES_DATA !== 'undefined' && GATES_DATA[rData.gateType]) ? GATES_DATA[rData.gateType] : { name: "🚪 철문", color: "#a8b4c4", rewardGold: 1500 };
    const regionScale = Math.pow(1.45, rId - 1);
    const waveScale = 1 + (waveNum - 1) * 0.28;

    let spritePath = `assets/monsters/m_${rId}_${waveNum}.png?v=7`;
    let monsterName = (rData.monsters && rData.monsters[waveNum - 1]) ? rData.monsters[waveNum - 1] : `지역 ${rId} 괴수 #${waveNum}`;
    let roleLabel = `WAVE ${waveNum}/6 · 일반 괴수`;
    let hpMult = 1.0;

    if (waveNum === 5) {
        spritePath = `assets/monsters/m_${rId}_named.png?v=7`;
        monsterName = rData.named || `지역 ${rId} 수문장`;
        roleLabel = `WAVE 5/6 · ⚡ 차원문 수문장 (Named)`;
        hpMult = 4.2;
    } else if (waveNum === 6) {
        spritePath = `assets/monsters/m_${rId}_boss.png?v=7`;
        monsterName = rData.boss || `지역 ${rId} 보스`;
        roleLabel = `WAVE 6/6 · 👑 차원문 지배자 (BOSS)`;
        hpMult = 12.0;
    }

    const key = `${rId}_${waveNum}`;
    const isFlying = (typeof FLYING_MONSTERS_MAP !== 'undefined') ? !!FLYING_MONSTERS_MAP[key] : false;

    const maxHp = Math.round(1200 * regionScale * waveScale * hpMult);
    return {
        rId,
        waveNum,
        spritePath,
        monsterName,
        roleLabel,
        maxHp,
        isFlying,
        gateData: gData
    };
}"""

js_text = re.sub(old_get_wave, new_get_wave, js_text, count=1)

# Update renderRegionMonstersRoster
old_roster = r'function renderRegionMonstersRoster\(rId\) \{[\s\S]*?\n\}'
new_roster = """function renderRegionMonstersRoster(rId) {
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
        const stanceBadge = meta.isFlying ? '🪽 공중 부유' : '🐾 지상 접지';
        const stanceCol = meta.isFlying ? '#64dcff' : '#a8b4c4';

        cardsHtml += `
            <div onclick="setGateWave(${w})" style="cursor:pointer; background:rgba(15,11,8,0.9); border:2px solid ${currentGateWave === w ? 'var(--neon-gold)' : borderCol}; padding:8px; text-align:center; border-radius:4px; transition:transform 0.15s;" onmouseover="this.style.transform='translateY(-3px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-size:0.62rem; color:${tagCol}; font-weight:bold;">${tagText}</span>
                    <span style="font-size:0.55rem; color:${stanceCol}; background:rgba(0,0,0,0.6); padding:1px 3px; border-radius:2px;">${stanceBadge}</span>
                </div>
                <div style="height:68px; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.45); border:1px solid #2a1f18; margin-bottom:5px;">
                    <img src="${meta.spritePath}" alt="${meta.monsterName}" style="max-width:62px; max-height:62px; object-fit:contain; image-rendering:pixelated; transform:scaleX(-1);">
                </div>
                <div style="font-size:0.7rem; color:var(--text-ivory); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${meta.monsterName}</div>
                <div style="font-size:0.62rem; color:var(--text-muted); margin-top:2px;">HP ${meta.maxHp.toLocaleString()}</div>
            </div>
        `;
    }
    grid.innerHTML = cardsHtml;
}"""

js_text = re.sub(old_roster, new_roster, js_text, count=1)

# Update setGateWave
old_set_gate_wave = r'function setGateWave\(waveNum\) \{[\s\S]*?\n    \}\n\}'
new_set_gate_wave = """function setGateWave(waveNum) {
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
        const stanceText = meta.isFlying ? ' [🪽 공중 부유]' : ' [🐾 지상 접지]';
        roleTag.textContent = `${meta.roleLabel} · ${meta.monsterName}${stanceText}`;
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

    // 🐾 지상 몬스터 vs 🪽 비행/부유 몬스터 위치 & 연출 제어
    const monsterContainer = document.getElementById('battleMonsterContainer');
    const groundShadow = document.getElementById('battleMonsterGroundShadow');
    if (monsterContainer) {
        if (meta.isFlying) {
            // 상공 85px로 자연스럽게 도약하여 부유 유영 모션
            monsterContainer.style.bottom = '85px';
            monsterContainer.style.transition = 'bottom 0.4s cubic-bezier(0.2, 0.9, 0.3, 1)';
            if (bossSprite) {
                bossSprite.style.animation = 'minionBob 2.2s ease-in-out infinite alternate';
            }
            if (groundShadow) {
                groundShadow.style.opacity = '0.28';
                groundShadow.style.transform = 'scale(0.65)';
            }
        } else {
            // 지면에 단단히 접지 (bottom: 16px, 붕 뜸 제로)
            monsterContainer.style.bottom = '16px';
            monsterContainer.style.transition = 'bottom 0.4s cubic-bezier(0.2, 0.9, 0.3, 1)';
            if (bossSprite) {
                bossSprite.style.animation = 'none';
            }
            if (groundShadow) {
                groundShadow.style.opacity = '0.75';
                groundShadow.style.transform = 'scale(1.0)';
            }
        }
    }

    updateGateWaveHpUI();
    renderRegionMonstersRoster(currentRegionId);

    // 🌊 [웨이브 진행에 따른 2400px 순수 자연 파노라마 전장 스크롤링]
    // Wave 1: 0% -> Wave 2: 20% -> Wave 3: 40% -> Wave 4: 60% -> Wave 5: 80% (수문장) -> Wave 6: 100% (최심부 보스 둥지)
    const waveScrollPct = (waveNum - 1) * 20;
    const bView = document.getElementById('battleBgView');
    if (bView) {
        bView.style.backgroundPosition = `${waveScrollPct}% center`;
    }
    const bFol = document.getElementById('battleFoliageLayer');
    if (bFol) {
        bFol.style.backgroundPosition = `${waveScrollPct}% center`;
    }

    // 영웅 전진 보행 카메라 패닝 연출
    const bHero = document.getElementById('battleHeroPartyBox');
    if (bHero && isHeroInsideGate) {
        bHero.style.transform = 'translateX(28px)';
        setTimeout(() => {
            if (bHero) bHero.style.transform = 'translateX(10px)';
        }, 750);
    }
}"""

js_text = re.sub(old_set_gate_wave, new_set_gate_wave, js_text, count=1)

# Update REGION_UNIQUE_PROP_NAMES
old_props = r'const REGION_UNIQUE_PROP_NAMES = \{[\s\S]*?\n\};'
new_props = """const REGION_UNIQUE_PROP_NAMES = {
    1:  "🍄 [1지역 원시 자연] 축축한 이끼 바위 & 보라·청록 발광 버섯 군락",
    2:  "🌲 [2지역 원시 자연] 은빛 솔잎 수관 가지 & 푸른 서릿발 고목 뿌리",
    3:  "🪨 [3지역 원시 자연] 젖은 몽돌 갯바위 & 따개비 해안 조수 웅덩이",
    4:  "❄️ [4지역 원시 자연] 투명한 고드름 눈솔가지 & 만년설 암벽 바위",
    5:  "💧 [5지역 원시 자연] 지하수 폭포 종유석 & 물이끼 석회 석순 암석",
    6:  "🎋 [6지역 원시 자연] 붉은 단풍잎 수관 가지 & 푸른 죽순 바위 덤불",
    7:  "🌿 [7지역 원시 자연] 늘어진 열대 밀림 덩굴(Vines) & 거대 고사리 바위",
    8:  "🌲 [8지역 원시 자연] 눈 덮인 가문비나무 가지 & 동토의 서리 암석",
    9:  "🪸 [9지역 원시 자연] 발광 켈프 해조류 숲 & 청록 산호초 말미잘 군락",
    10: "🧊 [10지역 원시 자연] 거꾸로 솟은 거대 고드름 종유석 & 청빙(Blue Ice) 수정 암반",
    11: "🏜️ [11지역 원시 자연] 메마른 사막 고목 & 붉은 풍화 사암 암석",
    12: "🌋 [12지역 원시 자연] 그을린 현무암 천장 암반 & 끓어오르는 용암 화산석",
    13: "☁️ [13지역 원시 자연] 성층권 천공 바위 아치 & 반중력 부유석 암편",
    14: "💎 [14지역 원시 자연] 천장 다이아몬드 석순 & 바닥 천연 다이아몬드 수정체 군락"
};"""

js_text = re.sub(old_props, new_props, js_text, count=1)

# Replace all v=6 with v=7 in display.js
js_text = js_text.replace('?v=6', '?v=7')

with open('project_necro/display.js', 'w', encoding='utf-8') as f:
    f.write(js_text)
print("Successfully updated display.js!")

# 2. Update display.html
with open('project_necro/display.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

# Add ground shadow under battleBossSprite if not present
if 'id="battleMonsterGroundShadow"' not in html_text:
    old_sprite_line = '<div id="battleBossSprite" onclick="attackGateWaveMonster()" title="클릭하여 몬스터 타격!" style="width: 138px; height: 138px; cursor: pointer; background-repeat: no-repeat; background-position: center bottom; background-size: contain; transform: scaleX(-1); image-rendering: pixelated; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.9)); transition: transform 0.15s, filter 0.15s;"></div>'
    new_sprite_line = old_sprite_line + '\n                    <div id="battleMonsterGroundShadow" style="width: 100px; height: 14px; background: radial-gradient(ellipse at center, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0) 75%); border-radius: 50%; margin-top: -6px; transition: all 0.4s ease-out; pointer-events: none;"></div>'
    html_text = html_text.replace(old_sprite_line, new_sprite_line)

# Update transition for battleMonsterContainer
html_text = html_text.replace(
    'id="battleMonsterContainer" style="position: absolute; bottom: 16px; right: 32px; display: flex; flex-direction: column; align-items: center; z-index: 14;"',
    'id="battleMonsterContainer" style="position: absolute; bottom: 16px; right: 32px; display: flex; flex-direction: column; align-items: center; z-index: 14; transition: bottom 0.4s cubic-bezier(0.2, 0.9, 0.3, 1);"'
)

# Update script tags to ?v=7
html_text = re.sub(r'display_data\.js\?v=\d+', 'display_data.js?v=7', html_text)
html_text = re.sub(r'display\.js\?v=\d+', 'display.js?v=7', html_text)

with open('project_necro/display.html', 'w', encoding='utf-8') as f:
    f.write(html_text)
print("Successfully updated display.html!")
