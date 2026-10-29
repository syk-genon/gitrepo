// =========================================================================
// 《목적을 잃지 않는 사령군주》 전시관 컨트롤러 (display.js)
// =========================================================================

let currentClassId = "necro";
let currentView = "side"; // "side" (우향 전투) or "front" (정면 비전투)
let currentAnim = "idle";
let animFrameIndex = 0;
let animInterval = null;

// 회귀 상태 모델
const regressionState = {
    count: 0,
    maxTraitSlots: 1,
    maxTalentSlots: 1,
    hasSoulSlot: false,
    ownedTraits: { "trait_mana_flow": 1 },
    ownedTalents: { "talent_exp_surge": 1 },
    soulEngravedIds: [],
    equippedTraits: ["trait_mana_flow"],
    equippedTalents: ["talent_exp_surge"],
    equippedSoulSlot: null
};

// 10프레임 바운스 키프레임 정의 (통통 튀는 던그리드 스타일)
const ANIM_10FRAMES = {
    idle: [
        { y: 0, rot: 0, scaleY: 1.0 },
        { y: -2, rot: 0, scaleY: 1.02 },
        { y: -4, rot: 1, scaleY: 1.04 },
        { y: -6, rot: 1, scaleY: 1.06 },
        { y: -4, rot: 0, scaleY: 1.04 },
        { y: -2, rot: 0, scaleY: 1.02 },
        { y: 0, rot: -1, scaleY: 0.98 },
        { y: 2, rot: -1, scaleY: 0.96 },
        { y: 1, rot: 0, scaleY: 0.98 },
        { y: 0, rot: 0, scaleY: 1.0 }
    ],
    walk: [
        { y: 0, rot: 3, scaleY: 1.0 },
        { y: -4, rot: 6, scaleY: 1.05 },
        { y: -8, rot: 4, scaleY: 1.08 },
        { y: -5, rot: 0, scaleY: 1.04 },
        { y: 0, rot: -3, scaleY: 0.96 },
        { y: 0, rot: -3, scaleY: 1.0 },
        { y: -4, rot: -6, scaleY: 1.05 },
        { y: -8, rot: -4, scaleY: 1.08 },
        { y: -5, rot: 0, scaleY: 1.04 },
        { y: 0, rot: 3, scaleY: 0.96 }
    ],
    attack: [
        { y: 0, rot: -6, scaleY: 0.95 },
        { y: -3, rot: -12, scaleY: 0.92 },
        { y: -6, rot: -18, scaleY: 0.9 },
        { y: -4, rot: -10, scaleY: 0.95 },
        { y: 4, rot: 15, scaleY: 1.15 }, // 타격 프레임
        { y: 6, rot: 20, scaleY: 1.2 },
        { y: 3, rot: 12, scaleY: 1.1 },
        { y: 1, rot: 6, scaleY: 1.05 },
        { y: 0, rot: 2, scaleY: 1.0 },
        { y: 0, rot: 0, scaleY: 1.0 }
    ],
    cast: [
        { y: 0, rot: -3, scaleY: 1.0 },
        { y: -4, rot: -6, scaleY: 1.05 },
        { y: -8, rot: -10, scaleY: 1.1 },
        { y: -12, rot: -12, scaleY: 1.15 },
        { y: -14, rot: -4, scaleY: 1.2 },
        { y: -6, rot: 12, scaleY: 1.1 }, // 방출 프레임
        { y: -3, rot: 8, scaleY: 1.05 },
        { y: -1, rot: 4, scaleY: 1.02 },
        { y: 0, rot: 2, scaleY: 1.0 },
        { y: 0, rot: 0, scaleY: 1.0 }
    ]
};

// 1. 클래스 선택 & 실제 16비트 스프라이트 렌더링
function selectClass(classId) {
    currentClassId = classId;
    document.querySelectorAll('#classSelectorTabs .btn-chip').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.class === classId);
    });
    
    const cData = CLASSES_DATA[classId];
    document.getElementById('currentClassName').textContent = cData.name;
    document.getElementById('currentClassModel').textContent = cData.model;
    document.getElementById('currentClassStat').textContent = cData.mainStat;
    document.getElementById('currentClassDesc').textContent = cData.desc;
    document.getElementById('currentClassPassive').textContent = cData.passive;
    document.getElementById('currentClassUlt').textContent = cData.ultimate;
    
    // 소환수 및 드래곤 상태 초기화
    clearMinions();
    
    // 사령군주(네크로맨서) 선택 시 자동으로 해골 호위병 3기 기본 소환
    if (classId === 'necro') {
        spawnMinionUnit('warrior', 2);
        spawnMinionUnit('archer', 1);
    }
    
    // 실제 16비트 캐릭터 일러스트 도트 갱신
    updateHeroSprite();
    renderClassSetItems();
    renderClassSkills();
    const townHeroImg = document.getElementById('townHeroImg');
    if (townHeroImg && cData.sprite) townHeroImg.src = cData.sprite;
    const battleHeroImg = document.getElementById('battleHeroSpriteImg');
    if (battleHeroImg && cData.sprite) battleHeroImg.src = cData.sprite;
}

function switchView(view) {
    currentView = view;
    document.getElementById('btnViewSide').classList.toggle('active', view === 'side');
    document.getElementById('btnViewFront').classList.toggle('active', view === 'front');
    
    const sprite = document.getElementById('heroPixelSprite');
    if (view === 'side') {
        // 우향 전투 뷰: 정방향
        sprite.style.transform = 'scaleX(1)';
    } else {
        // 비전투 뷰
        sprite.style.transform = 'scaleX(1)';
    }
}

const MOTION_FRAME_COUNTS = {
    idle: 4,
    walk: 6,
    attack: 4,
    cast: 4
};

function getMotionKey(anim) {
    if (anim === 'walk') return 'run';
    if (anim === 'cast') return 'skill';
    return anim;
}

function updateHeroSprite() {
    tickAnimationFrame(true);
}

// 2. 18프레임 다중 레이어 페이퍼돌 애니메이션 루프
function setAnimation(animName) {
    currentAnim = animName;
    document.querySelectorAll('#animButtons .btn-chip').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.anim === animName);
    });
    animFrameIndex = 0;
    tickAnimationFrame(true);
}

function tickAnimationFrame(forceUpdate = false) {
    const motionKey = getMotionKey(currentAnim);
    const maxFrames = MOTION_FRAME_COUNTS[currentAnim] || 4;
    
    if (!forceUpdate) {
        animFrameIndex = (animFrameIndex + 1) % maxFrames;
    }
    
    const indicator = document.getElementById('currentFrameIndicator');
    if (indicator) {
        indicator.textContent = `FRAME: ${animFrameIndex + 1}/${maxFrames} (${currentAnim.toUpperCase()} [${motionKey}_${animFrameIndex}])`;
    }
    
    const frames = ANIM_10FRAMES[currentAnim] || ANIM_10FRAMES.idle;
    const f = frames[animFrameIndex % frames.length];
    const container = document.getElementById('heroSpriteContainer');
    if (container) {
        container.style.transform = `translateY(${f.y}px) rotate(${f.rot}deg) scaleY(${f.scaleY})`;
    }

    // 240x240 다중 레이어 페이퍼돌 업데이트
    const cfg = (typeof CLASS_PAPERDOLL_CONFIG !== 'undefined' && CLASS_PAPERDOLL_CONFIG[currentClassId]) 
        ? CLASS_PAPERDOLL_CONFIG[currentClassId] 
        : { body: "male_nemesis", armor: null, weapon: "crystal", mutation: "wings", wings: null };

    const lBody = document.getElementById('layerBody');
    const lArmor = document.getElementById('layerArmor');
    const lWeapon = document.getElementById('layerWeapon');
    const lMutation = document.getElementById('layerMutation');
    const lWings = document.getElementById('layerWings');
    
    if (lBody) {
        lBody.src = `assets/pixel_hero/${cfg.body}_${motionKey}_${animFrameIndex}.png?v=10`;
    }
    if (lArmor) {
        if (cfg.armor) {
            lArmor.src = `assets/pixel_hero/armors/${cfg.armor}_${motionKey}_${animFrameIndex}.png?v=10`;
            lArmor.style.display = 'block';
        } else {
            lArmor.style.display = 'none';
        }
    }
    if (lWeapon) {
        if (cfg.weapon) {
            lWeapon.src = `assets/pixel_hero/weapons/${cfg.weapon}_${motionKey}_${animFrameIndex}.png?v=10`;
            lWeapon.style.display = 'block';
        } else {
            lWeapon.style.display = 'none';
        }
    }
    if (lMutation) {
        if (cfg.mutation) {
            lMutation.src = `assets/pixel_hero/mutations/${cfg.mutation}_${motionKey}_${animFrameIndex}.png?v=10`;
            lMutation.style.display = 'block';
        } else {
            lMutation.style.display = 'none';
        }
    }
    if (lWings) {
        if (cfg.wings) {
            lWings.src = `assets/pixel_hero/mutations/${cfg.wings}_${motionKey}_${animFrameIndex}.png?v=10`;
            lWings.style.display = 'block';
        } else {
            lWings.style.display = 'none';
        }
    }
}

// 3. 세트 아이템 및 스킬 렌더링
function renderClassSetItems() {
    const cData = CLASSES_DATA[currentClassId];
    const container = document.getElementById('classSetPartsList');
    if (!container) return;
    
    container.innerHTML = cData.setParts.map(p => `
        <div class="set-item-row">
            <img src="${p.icon}" class="set-item-icon" alt="${p.part}">
            <div style="flex: 1;">
                <div style="color: var(--neon-gold); font-size: 0.84rem;">${p.name}</div>
                <div style="color: var(--text-muted); font-size: 0.72rem;">${p.effect}</div>
            </div>
            <label class="custom-checkbox">
                <input type="checkbox" checked onchange="toggleSetPartAura()">
                <span class="checkmark"></span>
            </label>
        </div>
    `).join('');
    toggleSetPartAura();
}

function toggleSetPartAura() {
    const aura = document.getElementById('partSetAura');
    const checkedCount = document.querySelectorAll('#classSetPartsList input[type="checkbox"]:checked').length;
    const countBadge = document.getElementById('equippedSetCountBadge');
    if (countBadge) countBadge.textContent = `${checkedCount}/5 부위 장착 [${checkedCount === 5 ? '신화 5세트 완성!' : '세트 조율 중'}]`;
    
    if (aura) {
        if (checkedCount === 5) {
            aura.style.display = 'block';
            aura.style.boxShadow = `0 0 30px ${CLASSES_DATA[currentClassId].color}, inset 0 0 20px ${CLASSES_DATA[currentClassId].color}`;
        } else {
            aura.style.display = 'none';
        }
    }
}

function renderClassSkills() {
    const cData = CLASSES_DATA[currentClassId];
    const container = document.getElementById('classSkillsGrid');
    if (!container) return;
    
    container.innerHTML = cData.skills.map(s => `
        <div class="skill-card ${s.type === 'ult' ? 'skill-card-ult' : ''}" onclick="testSkillVfx('${s.name}', '${s.vfx}', '${s.type}', '${s.id}')" style="cursor:pointer; display:flex; align-items:center; gap:12px; padding:10px 12px; transition:transform 0.15s, border-color 0.15s;">
            <div style="flex-shrink:0; width:52px; height:52px; background:#080605; border:2px solid ${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--neon-gold)'}; border-radius:4px; display:flex; align-items:center; justify-content:center; overflow:hidden; box-shadow:0 0 8px rgba(0,0,0,0.8);">
                <img src="${s.vfx}" alt="${s.name}" style="width:44px; height:44px; object-fit:contain; image-rendering:pixelated; filter:drop-shadow(0 0 6px ${s.type === 'ult' ? 'rgba(255,0,85,0.7)' : 'rgba(255,204,0,0.7)'});">
            </div>
            <div style="flex:1;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--neon-gold)'}; font-size:0.88rem; font-weight:bold;">${s.name}</span>
                    <span class="skill-type-tag" style="background:${s.type === 'ult' ? 'rgba(255,0,85,0.2)' : 'rgba(255,204,0,0.15)'}; border:1px solid ${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--neon-gold)'}; color:${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--neon-gold)'}; font-size:0.65rem; padding:2px 6px; border-radius:3px;">${(s.badge || s.type).toUpperCase()}</span>
                </div>
                <div style="color:var(--text-muted); font-size:0.72rem; margin-top:3px; line-height:1.3;">${s.desc}</div>
                <div style="color:var(--neon-cyan); font-size:0.68rem; margin-top:3px; background:rgba(0,240,255,0.08); padding:2px 5px; border-radius:2px;">고유 효과: <strong>${s.buffDesc || s.desc}</strong></div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:5px;">
                    <span style="font-size:0.65rem; color:${s.target === 'self' ? 'var(--neon-green)' : (s.target === 'both' ? 'var(--neon-gold)' : 'var(--neon-pink)')};">
                        ${s.target === 'self' ? '🛡️ 본체 전용 방어/버프' : (s.target === 'both' ? '✨ 아군/적군 동시 작렬' : '⚔️ 전방 적진 타격기')}
                    </span>
                    <button class="btn-ctrl" style="font-size:0.68rem; padding:2px 8px;">스킬 발동 ▶</button>
                </div>
            </div>
        </div>
    `).join('');
}

// -------------------------------------------------------------
// 3-B. 소환수 부하 군단 관리 시스템 (Minions Legion System)
// -------------------------------------------------------------
let summonedMinions = [];

const MINION_CONFIGS = {
    warrior: {
        type: 'warrior',
        name: '해골 전사',
        sprite: 'assets/summons/minion_skeleton_warrior.png?v=10',
        width: 44,
        height: 44,
        atk: 320,
        hp: 1200
    },
    archer: {
        type: 'archer',
        name: '해골 궁병',
        sprite: 'assets/summons/minion_skeleton_archer.png?v=10',
        width: 44,
        height: 44,
        atk: 480,
        hp: 750
    },
    mage: {
        type: 'mage',
        name: '해골 술사',
        sprite: 'assets/summons/minion_skeleton_mage.png?v=10',
        width: 44,
        height: 44,
        atk: 620,
        hp: 600
    },
    knight: {
        type: 'knight',
        name: '데스나이트',
        sprite: 'assets/summons/minion_death_knight.png?v=10',
        width: 52,
        height: 52,
        atk: 1450,
        hp: 4500
    },
    shadow: {
        type: 'shadow',
        name: '그림자 분신',
        sprite: 'assets/summons/minion_shadow_clone.png?v=10',
        width: 44,
        height: 44,
        atk: 900,
        hp: 1800
    },
    guardian: {
        type: 'guardian',
        name: '수호 천사령',
        sprite: 'assets/summons/minion_holy_guardian.png?v=10',
        width: 48,
        height: 48,
        atk: 500,
        hp: 5000
    }
};

function spawnMinionUnit(minionType, count = 1) {
    const config = MINION_CONFIGS[minionType] || MINION_CONFIGS.warrior;
    const maxMinions = 10;
    
    for (let i = 0; i < count; i++) {
        if (summonedMinions.length >= maxMinions) {
            summonedMinions.shift();
        }
        summonedMinions.push({
            id: 'minion_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
            ...config
        });
    }
    
    renderMinionsUi();
    const logBox = document.getElementById('skillCombatLog');
    if (logBox) {
        logBox.innerHTML = `<span style="color:var(--neon-green)">▶ [군단 소환] 대지에서 <strong>${config.name}</strong> ${count}기가 소환되어 군주의 뒤편에 집결했습니다!</span>`;
    }
}

function renderMinionsUi() {
    const container = document.getElementById('heroMinionsContainer');
    const badge = document.getElementById('minionArmyCountBadge');
    const buffText = document.getElementById('minionArmyBuffText');
    
    if (badge) badge.textContent = `${summonedMinions.length}기 소환 중`;
    if (buffText) {
        const totalBonus = summonedMinions.reduce((sum, m) => sum + (m.type === 'knight' ? 30 : m.type === 'mage' ? 20 : 10), 0);
        buffText.textContent = `군단 버프: +${totalBonus}% (DPS: +${summonedMinions.reduce((s, m) => s + m.atk, 0).toLocaleString()})`;
    }
    
    if (!container) return;
    
    container.innerHTML = summonedMinions.map((m, idx) => `
        <div class="minion-unit" id="${m.id}" style="z-index: ${10 + idx};">
            <div style="font-size:0.55rem; color:var(--neon-cyan); text-shadow:0 0 3px #000; margin-bottom:-2px; white-space:nowrap;">${m.name}</div>
            <img src="${m.sprite}" alt="${m.name}" style="width:${m.width}px; height:${m.height}px;">
        </div>
    `).join('');
}

function commandMinionsAttack() {
    if (summonedMinions.length === 0) {
        const logBox = document.getElementById('skillCombatLog');
        if (logBox) logBox.textContent = `▶ 현재 소환된 부하 군단이 없습니다. 먼저 부하를 소환하십시오!`;
        return;
    }
    
    shakeStage();
    
    document.querySelectorAll('.minion-unit').forEach(el => {
        el.classList.add('attacking');
        setTimeout(() => el.classList.remove('attacking'), 400);
    });
    
    setAnimation('attack');
    setTimeout(() => setAnimation('idle'), 600);
    
    const totalDmg = summonedMinions.reduce((sum, m) => sum + m.atk * 3, 0);
    const vfxBox = document.getElementById('studioVfxLayer');
    const logBox = document.getElementById('skillCombatLog');
    
    if (logBox) {
        logBox.innerHTML = `<span style="color:var(--neon-gold)">⚔️ [군단 일제 돌격] 소환된 <strong>${summonedMinions.length}기</strong>의 부하들이 일제히 화살과 칼날을 투사하여 총 <strong>${totalDmg.toLocaleString()}</strong>의 피해를 입혔습니다!</span>`;
    }
    
    if (vfxBox) {
        vfxBox.innerHTML = `
            <div style="position:relative; display:flex; flex-direction:column; align-items:center; animation:vfxPopAnim 0.75s ease-out forwards;">
                <div style="font-size:1.15rem; font-weight:bold; color:#ffcc00; text-shadow:0 0 10px #000, 0 0 8px #ffcc00;">
                    💥 ARMY CRUSH ${totalDmg.toLocaleString()}!
                </div>
                <img src="assets/pixel_vfx/skills/vfx_necro_1.png?v=10" style="width:140px; height:140px; object-fit:contain; image-rendering:pixelated; filter:drop-shadow(0 0 16px #00ffaa);">
            </div>
        `;
        setTimeout(() => { vfxBox.innerHTML = ''; }, 750);
    }
}

function corpseExplodeMinion() {
    if (summonedMinions.length === 0) {
        const logBox = document.getElementById('skillCombatLog');
        if (logBox) logBox.textContent = `▶ 폭파할 시체/부하가 없습니다! 먼저 해골 군단을 소환하십시오.`;
        return;
    }
    
    shakeStage();
    
    const victim = summonedMinions.pop();
    renderMinionsUi();
    
    const vfxBox = document.getElementById('studioVfxLayer');
    const logBox = document.getElementById('skillCombatLog');
    const expDmg = Math.floor(victim.hp * 2.8 + 25000);
    
    if (logBox) {
        logBox.innerHTML = `<span style="color:var(--neon-pink)">💥 [시체 폭발 연계] <strong>${victim.name}</strong>의 시신이 맹렬하게 폭발하며 반경 내 적들에게 <strong>${expDmg.toLocaleString()}</strong>의 암흑 파편 피해!</span>`;
    }
    
    if (vfxBox) {
        vfxBox.innerHTML = `
            <div style="position:relative; display:flex; flex-direction:column; align-items:center; animation:vfxPopAnim 0.75s ease-out forwards;">
                <div style="font-size:1.25rem; font-weight:bold; color:#ff0055; text-shadow:0 0 12px #000, 0 0 10px #ff0055;">
                    💀 CORPSE BURST ${expDmg.toLocaleString()}!
                </div>
                <img src="assets/pixel_vfx/skills/vfx_necro_2.png?v=10" style="width:160px; height:160px; object-fit:contain; image-rendering:pixelated; filter:drop-shadow(0 0 24px #ff0055);">
            </div>
        `;
        setTimeout(() => { vfxBox.innerHTML = ''; }, 750);
    }
}

function clearMinions() {
    summonedMinions = [];
    const dragonLayer = document.getElementById('heroDragonLayer');
    if (dragonLayer) dragonLayer.style.display = 'none';
    renderMinionsUi();
    const logBox = document.getElementById('skillCombatLog');
    if (logBox) logBox.textContent = `▶ 모든 소환수가 해산되어 명계로 복귀했습니다.`;
}

function shakeStage() {
    const stage = document.getElementById('studioStage');
    if (stage) {
        stage.classList.add('shaking');
        setTimeout(() => stage.classList.remove('shaking'), 400);
    }
}

function showHeroFloatingText(text, color = '#00ffaa') {
    const floatLayer = document.getElementById('heroFloatingLayer');
    if (!floatLayer) return;
    const bubble = document.createElement('div');
    bubble.className = 'hero-floating-bubble';
    bubble.style.color = color;
    bubble.innerHTML = text;
    floatLayer.appendChild(bubble);
    setTimeout(() => {
        if (bubble.parentNode) bubble.parentNode.removeChild(bubble);
    }, 1250);
}

function triggerHeroShieldDome(type = 'blue', durationMs = 2500) {
    const dome = document.getElementById('heroShieldDome');
    if (!dome) return;
    
    if (type === 'mana' || type === 'blue') {
        dome.style.border = '3px solid #00f0ff';
        dome.style.background = 'radial-gradient(circle, rgba(0, 240, 255, 0.28) 0%, rgba(0, 240, 255, 0.05) 70%, transparent 100%)';
        dome.style.boxShadow = '0 0 32px #00f0ff, inset 0 0 20px #00f0ff';
    } else if (type === 'gold' || type === 'aegis') {
        dome.style.border = '3px solid #ffd000';
        dome.style.background = 'radial-gradient(circle, rgba(255, 208, 0, 0.3) 0%, rgba(255, 208, 0, 0.08) 70%, transparent 100%)';
        dome.style.boxShadow = '0 0 35px #ffd000, inset 0 0 25px #ffd000';
    } else if (type === 'bone' || type === 'green') {
        dome.style.border = '3px solid #00ffaa';
        dome.style.background = 'radial-gradient(circle, rgba(0, 255, 170, 0.28) 0%, rgba(0, 255, 170, 0.06) 70%, transparent 100%)';
        dome.style.boxShadow = '0 0 32px #00ffaa, inset 0 0 20px #00ffaa';
    } else if (type === 'diamond' || type === 'ice') {
        dome.style.border = '3px solid #c8f5ff';
        dome.style.background = 'radial-gradient(circle, rgba(200, 245, 255, 0.45) 0%, rgba(100, 220, 255, 0.18) 70%, transparent 100%)';
        dome.style.boxShadow = '0 0 38px #c8f5ff, inset 0 0 25px #00e5ff';
    }
    dome.style.display = 'block';
    setTimeout(() => {
        dome.style.display = 'none';
    }, durationMs);
}

function testSkillVfx(name, vfxPath, type = 'core', skillId = '') {
    const vfxBox = document.getElementById('studioVfxLayer');
    const logBox = document.getElementById('skillCombatLog');
    const dragonLayer = document.getElementById('heroDragonLayer');
    const heroContainer = document.getElementById('heroSpriteContainer');
    const isUlt = type === 'ult';
    
    // 스킬 메타데이터 탐색
    let sData = null;
    if (CLASSES_DATA[currentClassId] && CLASSES_DATA[currentClassId].skills) {
        sData = CLASSES_DATA[currentClassId].skills.find(s => s.id === skillId);
    }
    if (!sData) {
        Object.values(CLASSES_DATA).forEach(cd => {
            if (!sData && cd.skills) {
                const f = cd.skills.find(s => s.id === skillId);
                if (f) sData = f;
            }
        });
    }
    
    const kind = sData ? sData.kind : 'attack';
    const target = sData ? sData.target : 'enemy';
    const flText = sData ? sData.floatingText : (isUlt ? '💥 CRITICAL!' : 'HIT!');
    const logMsg = sData ? sData.logMsg : '전용 16비트 도트 VFX 투사 및 타격 판정!';
    
    // 모션 분기
    if (kind === 'shield' || kind === 'blink_shield' || kind === 'heal' || kind === 'buff' || isUlt) {
        setAnimation('cast');
    } else {
        setAnimation('attack');
    }
    setTimeout(() => setAnimation('idle'), 750);
    
    // 특수 군단 및 소환 메커니즘
    if (skillId === 'necro_1') {
        spawnMinionUnit('warrior', 2);
        spawnMinionUnit('archer', 1);
    } else if (skillId === 'necro_2') {
        corpseExplodeMinion();
        return;
    } else if (skillId === 'necro_5') {
        spawnMinionUnit('knight', 1);
    } else if (skillId === 'necro_ult') {
        if (dragonLayer) dragonLayer.style.display = 'block';
        spawnMinionUnit('knight', 1);
    } else if (skillId === 'as_4') {
        spawnMinionUnit('shadow', 2);
    } else if (skillId === 'guard_ult' || skillId === 'priest_ult') {
        spawnMinionUnit('guardian', 1);
    } else if (skillId === 'dk_ult') {
        spawnMinionUnit('knight', 1);
    }

    // 1. 방어막 / 마나실드 계열 (주인공 본체 위에 돔 & 쉴드 텍스트 팝업)
    if (kind === 'shield' || kind === 'blink_shield') {
        const domeType = (skillId === 'storm_4') ? 'mana' 
                       : (skillId === 'necro_4') ? 'bone' 
                       : (skillId === 'guard_4' || skillId === 'priest_4') ? 'aegis' : 'blue';
        
        triggerHeroShieldDome(domeType, 2500);
        showHeroFloatingText(flText, '#00f0ff');
        
        if (kind === 'blink_shield' && heroContainer) {
            heroContainer.style.transform = 'translateX(-30px)';
            setTimeout(() => {
                heroContainer.style.transform = 'none';
            }, 250);
        }
        
        if (logBox) {
            logBox.innerHTML = `<span style="color:var(--neon-cyan)">🛡️ [보호막 & 회피] <strong>${name}</strong>: ${logMsg}</span>`;
        }
        return; // 적진 타격 없음!
    }

    // 2. 치유 (Heal) 계열 (주인공 치유 텍스트 & 황금/초록 오라)
    if (kind === 'heal') {
        triggerHeroShieldDome('gold', 1500);
        showHeroFloatingText(flText, '#00ff88');
        
        if (logBox) {
            logBox.innerHTML = `<span style="color:var(--neon-green)">✨ [성역 치유] <strong>${name}</strong>: ${logMsg}</span>`;
        }
        
        // 홀리 라이트닝처럼 아군 치유 + 적 타격이 동시에 있는 경우
        if (target !== 'both') return;
    }

    // 3. 무적 / 패링 / 결정화 계열
    if (kind === 'invulnerable' || kind === 'parry') {
        const domeType = (skillId === 'cryo_4') ? 'diamond' : 'gold';
        triggerHeroShieldDome(domeType, 2500);
        showHeroFloatingText(flText, '#ffd000');
        
        if (heroContainer) {
            heroContainer.style.filter = (skillId === 'cryo_4') 
                ? 'drop-shadow(0 0 25px #00f0ff) brightness(1.6)' 
                : 'brightness(2.2) drop-shadow(0 0 25px #ffd000)';
            setTimeout(() => {
                heroContainer.style.filter = 'none';
            }, 2000);
        }
        
        if (logBox) {
            logBox.innerHTML = `<span style="color:var(--neon-gold)">🌟 [절대 무적/패링] <strong>${name}</strong>: ${logMsg}</span>`;
        }
        
        if (kind === 'parry') {
            // 패링 300% 반격 즉시 작렬
            shakeStage();
            if (vfxBox) {
                vfxBox.innerHTML = `
                    <div style="position:relative; display:flex; flex-direction:column; align-items:center; animation:vfxPopAnim 0.75s ease-out forwards;">
                        <div style="font-size:1.25rem; font-weight:bold; color:#ff2a6d; text-shadow:0 0 10px #000, 0 0 8px #ff2a6d;">
                            ⚔️ 300% PARRY COUNTER 84,000!
                        </div>
                        <img src="${vfxPath}" style="width:160px; height:160px; object-fit:contain; image-rendering:pixelated; filter:drop-shadow(0 0 20px #ff2a6d);">
                    </div>
                `;
                setTimeout(() => { vfxBox.innerHTML = ''; }, 750);
            }
        }
        return;
    }

    // 4. 은신 (Stealth) 계열
    if (kind === 'stealth') {
        showHeroFloatingText(flText, '#c850ff');
        if (heroContainer) {
            heroContainer.style.opacity = '0.35';
            heroContainer.style.filter = 'drop-shadow(0 0 15px #a028ff)';
            setTimeout(() => {
                heroContainer.style.opacity = '1';
                heroContainer.style.filter = 'none';
            }, 3000);
        }
        if (logBox) {
            logBox.innerHTML = `<span style="color:var(--neon-purple)">🕶️ [완전 은신] <strong>${name}</strong>: ${logMsg}</span>`;
        }
        return; // 적진 타격 없음!
    }

    // 5. 버프 (Buff) 계열
    if (kind === 'buff' && target === 'self') {
        showHeroFloatingText(flText, '#ffd000');
        if (heroContainer) {
            heroContainer.style.filter = 'drop-shadow(0 0 20px #ffcc00)';
            setTimeout(() => {
                heroContainer.style.filter = 'none';
            }, 1800);
        }
        if (logBox) {
            logBox.innerHTML = `<span style="color:var(--neon-gold)">⚡ [강화 버프] <strong>${name}</strong>: ${logMsg}</span>`;
        }
        return; // 적진 타격 없음!
    }

    // 6. 소환 (Summon) 계열 (소환수만 생성되고 적진 타격 없음)
    if (kind === 'summon' && target === 'self') {
        showHeroFloatingText(flText, '#00ffaa');
        if (logBox) {
            logBox.innerHTML = `<span style="color:var(--neon-green)">💀 [군단 소환] <strong>${name}</strong>: ${logMsg}</span>`;
        }
        return;
    }

    // 7. 공격기 / 투사체 / CC / 결전기 (적진 타격존에 고유 플로팅 및 VFX 작렬)
    shakeStage();
    if (logBox) {
        logBox.innerHTML = `<span style="color:${isUlt ? 'var(--neon-pink)' : 'var(--neon-cyan)'}">⚔️ [스킬 전개] <strong>${name}</strong>: ${logMsg}</span>`;
    }

    if (!vfxBox) return;
    const dmg = isUlt ? Math.floor(Math.random() * 60000 + 75000) : Math.floor(Math.random() * 14000 + 6000);
    
    vfxBox.innerHTML = `
        <div style="position:relative; display:flex; flex-direction:column; align-items:center; animation:vfxPopAnim 0.8s ease-out forwards;">
            <div style="font-size:1.15rem; font-weight:bold; color:${isUlt ? '#ff0055' : '#ffcc00'}; text-shadow:0 0 10px #000, 0 0 8px ${isUlt ? '#ff0055' : '#ffcc00'}; letter-spacing:1px; margin-bottom:-10px; z-index:5;">
                ${flText} [${dmg.toLocaleString()}]
            </div>
            <img src="${vfxPath}" style="width:160px; height:160px; object-fit:contain; image-rendering:pixelated; filter:drop-shadow(0 0 20px ${isUlt ? 'rgba(255,0,85,0.95)' : 'rgba(0,255,200,0.95)'});">
        </div>
    `;
    setTimeout(() => {
        vfxBox.innerHTML = '';
    }, 800);
}

// 4. 회귀(Regression) 시뮬레이터 로직
function getLevelMultiplier(level) {
    const lv = Math.max(1, Math.min(10, level));
    return 1 + 0.5 * (lv - 1);
}

function calcEffectiveStat(baseValue, level) {
    return Number((baseValue * getLevelMultiplier(level)).toFixed(1));
}

function renderRegressionUi() {
    document.getElementById('regressionCountDisplay').textContent = `${regressionState.count}회`;
    document.getElementById('traitSlotsInfo').textContent = `특성 슬롯: ${regressionState.equippedTraits.length}/${regressionState.maxTraitSlots}칸`;
    document.getElementById('talentSlotsInfo').textContent = `재능 슬롯: ${regressionState.equippedTalents.length}/${regressionState.maxTalentSlots}칸`;
    
    const soulSlotBox = document.getElementById('soulSlotBox');
    if (soulSlotBox) {
        if (regressionState.hasSoulSlot) {
            soulSlotBox.style.display = 'block';
            document.getElementById('soulSlotStatus').innerHTML = regressionState.equippedSoulSlot 
                ? `<span style="color: var(--neon-gold); font-weight: bold;">[각인 장착됨] ${regressionState.equippedSoulSlot} (Lv.10 만렙)</span>`
                : `<span style="color: var(--neon-cyan);">[슬롯 개방됨] 만렙 특성/재능 장착 대기 중</span>`;
        } else {
            soulSlotBox.style.display = 'none';
        }
    }
    
    // 장착된 특성 목록 렌더링
    const traitsList = document.getElementById('equippedTraitsList');
    if (traitsList) {
        traitsList.innerHTML = regressionState.equippedTraits.map(id => {
            const t = TRAITS_DATA[id];
            const lv = regressionState.ownedTraits[id] || 1;
            const eff = calcEffectiveStat(t.baseVal, lv);
            const isMax = lv === 10;
            return `
                <div class="trait-slot-card ${isMax ? 'master-soul-card' : ''}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color: ${isMax ? 'var(--neon-gold)' : 'var(--neon-green)'}; font-size:0.86rem;">${t.name}</span>
                        <span class="lv-badge ${isMax ? 'master' : ''}">Lv.${lv} ${isMax ? '★만렙' : ''}</span>
                    </div>
                    <div style="font-size:0.74rem; color:var(--text-ivory); margin-top:3px;">
                        효과: <strong style="color:var(--neon-cyan);">+${eff}${t.unit}</strong> <span style="color:#888;">(기본 ${t.baseVal}${t.unit} × ${getLevelMultiplier(lv)}배)</span>
                    </div>
                    <div style="font-size:0.68rem; color:var(--text-muted); margin-top:2px;">${t.desc}</div>
                </div>
            `;
        }).join('');
    }
    
    // 장착된 재능 목록 렌더링
    const talentsList = document.getElementById('equippedTalentsList');
    if (talentsList) {
        talentsList.innerHTML = regressionState.equippedTalents.map(id => {
            const t = TALENTS_DATA[id];
            const lv = regressionState.ownedTalents[id] || 1;
            const eff = calcEffectiveStat(t.baseVal, lv);
            const isMax = lv === 10;
            return `
                <div class="trait-slot-card ${isMax ? 'master-soul-card' : ''}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color: ${isMax ? 'var(--neon-gold)' : 'var(--neon-purple)'}; font-size:0.86rem;">${t.name}</span>
                        <span class="lv-badge ${isMax ? 'master' : ''}">Lv.${lv} ${isMax ? '★만렙' : ''}</span>
                    </div>
                    <div style="font-size:0.74rem; color:var(--text-ivory); margin-top:3px;">
                        효과: <strong style="color:var(--neon-cyan);">+${eff}${t.unit}</strong> <span style="color:#888;">(기본 ${t.baseVal}${t.unit} × ${getLevelMultiplier(lv)}배)</span>
                    </div>
                    <div style="font-size:0.68rem; color:var(--text-muted); margin-top:2px;">${t.desc}</div>
                </div>
            `;
        }).join('');
    }
}

function openRegressionModal() {
    const modal = document.getElementById('regressionSelectModal');
    if (!modal) return;
    
    // 특성 선택지 생성
    const traitSelect = document.getElementById('regressionTraitSelect');
    traitSelect.innerHTML = Object.keys(TRAITS_DATA).map(id => {
        const t = TRAITS_DATA[id];
        const curLv = regressionState.ownedTraits[id] || 0;
        const nextLv = Math.min(10, curLv + 1);
        return `<option value="${id}">${t.name} (현재 Lv.${curLv} -> Lv.${nextLv})</option>`;
    }).join('');
    
    // 재능 선택지 생성
    const talentSelect = document.getElementById('regressionTalentSelect');
    talentSelect.innerHTML = Object.keys(TALENTS_DATA).map(id => {
        const t = TALENTS_DATA[id];
        const curLv = regressionState.ownedTalents[id] || 0;
        const nextLv = Math.min(10, curLv + 1);
        return `<option value="${id}">${t.name} (현재 Lv.${curLv} -> Lv.${nextLv})</option>`;
    }).join('');
    
    modal.classList.add('active');
}

function confirmRegression() {
    const traitId = document.getElementById('regressionTraitSelect').value;
    const talentId = document.getElementById('regressionTalentSelect').value;
    
    regressionState.count += 1;
    if (regressionState.count === 1) {
        regressionState.maxTraitSlots += 1;
        regressionState.maxTalentSlots += 1;
    }
    
    // 특성 레벨업 또는 추가
    if (regressionState.ownedTraits[traitId]) {
        if (regressionState.ownedTraits[traitId] < 10) regressionState.ownedTraits[traitId] += 1;
    } else {
        regressionState.ownedTraits[traitId] = 1;
        if (regressionState.equippedTraits.length < regressionState.maxTraitSlots) {
            regressionState.equippedTraits.push(traitId);
        }
    }
    
    // 재능 레벨업 또는 추가
    if (regressionState.ownedTalents[talentId]) {
        if (regressionState.ownedTalents[talentId] < 10) regressionState.ownedTalents[talentId] += 1;
    } else {
        regressionState.ownedTalents[talentId] = 1;
        if (regressionState.equippedTalents.length < regressionState.maxTalentSlots) {
            regressionState.equippedTalents.push(talentId);
        }
    }
    
    // 만렙 영혼 각인 체크
    if (regressionState.ownedTraits[traitId] === 10 && !regressionState.soulEngravedIds.includes(traitId)) {
        regressionState.soulEngravedIds.push(traitId);
        if (!regressionState.hasSoulSlot) {
            regressionState.hasSoulSlot = true;
            regressionState.equippedSoulSlot = TRAITS_DATA[traitId].name;
        }
    }
    if (regressionState.ownedTalents[talentId] === 10 && !regressionState.soulEngravedIds.includes(talentId)) {
        regressionState.soulEngravedIds.push(talentId);
        if (!regressionState.hasSoulSlot) {
            regressionState.hasSoulSlot = true;
            regressionState.equippedSoulSlot = TALENTS_DATA[talentId].name;
        }
    }
    
    closeRegressionModal();
    renderRegressionUi();
}

function closeRegressionModal() {
    const modal = document.getElementById('regressionSelectModal');
    if (modal) modal.classList.remove('active');
}

// 5. 고유(Unique) 아이템 36종 렌더링
function renderUniqueItems() {
    const grid = document.getElementById('uniqueItemsGrid');
    if (!grid) return;
    grid.innerHTML = UNIQUE_ITEMS_DATA.map(item => `
        <div class="unique-item-card">
            <div style="display:flex; align-items:center; gap:8px;">
                <img src="${item.icon}" style="width:36px; height:36px; image-rendering:pixelated;" alt="icon">
                <div>
                    <div style="color:var(--neon-gold); font-size:0.84rem;">${item.name}</div>
                    <div style="color:var(--neon-cyan); font-size:0.68rem;">출처: ${item.source}</div>
                </div>
            </div>
            <div style="font-size:0.72rem; color:var(--text-muted); margin-top:6px; line-height:1.3;">
                ${item.effect}
            </div>
        </div>
    `).join('');
}

// 6. 14대 지역별 [마을 ➔ 6대 차원문(Gate) 진입 ➔ 6웨이브(84종 괴수) 실전 시뮬레이터]
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

    let spritePath = `assets/monsters/m_${rId}_${waveNum}.png?v=10`;
    let monsterName = (rData.monsters && rData.monsters[waveNum - 1]) ? rData.monsters[waveNum - 1] : `지역 ${rId} 괴수 #${waveNum}`;
    let roleLabel = `WAVE ${waveNum}/6 · 일반 괴수`;
    let hpMult = 1.0;

    if (waveNum === 5) {
        spritePath = `assets/monsters/m_${rId}_named.png?v=10`;
        monsterName = rData.named || `지역 ${rId} 수문장`;
        roleLabel = `WAVE 5/6 · ⚡ 차원문 수문장 (Named)`;
        hpMult = 4.2;
    } else if (waveNum === 6) {
        spritePath = `assets/monsters/m_${rId}_boss.png?v=10`;
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

    // 마을 배경 & 전투 배경 4프레임 루프 에셋 프리로드 및 초기 프레임 적용
    preloadRegion4FrameBackgrounds(rId);
    applyRegionSwayFrame(rId, bgFoliageFrameIdx);

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

// 7. 전 12개 직업 72종 전용 스킬 VFX 도감
let currentSkillGalleryFilter = 'all';
function setSkillGalleryFilter(filter) {
    currentSkillGalleryFilter = filter;
    document.querySelectorAll('#skillGalleryFilterTabs .btn-chip').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    renderAllSkillsGallery();
}

function renderAllSkillsGallery() {
    const container = document.getElementById('allSkillsVfxGrid');
    if (!container) return;
    
    let allSkills = [];
    Object.keys(CLASSES_DATA).forEach(cKey => {
        if (currentSkillGalleryFilter !== 'all' && currentSkillGalleryFilter !== cKey) return;
        const cData = CLASSES_DATA[cKey];
        cData.skills.forEach(s => {
            allSkills.push({
                ...s,
                className: cData.name,
                classId: cKey
            });
        });
    });
    
    container.innerHTML = allSkills.map(s => `
        <div class="skill-card ${s.type === 'ult' ? 'skill-card-ult' : ''}" style="display:flex; flex-direction:column; justify-content:space-between; padding:10px; border-radius:4px; background:rgba(20,15,10,0.85); border:1px solid ${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--border-wood-light)'};">
            <div style="display:flex; gap:10px; align-items:center;">
                <div style="width:48px; height:48px; flex-shrink:0; background:#080605; border:1px solid ${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--neon-gold)'}; border-radius:4px; display:flex; align-items:center; justify-content:center;">
                    <img src="${s.vfx}" alt="${s.name}" style="width:40px; height:40px; object-fit:contain; image-rendering:pixelated;">
                </div>
                <div style="flex:1; min-width:0;">
                    <div style="font-size:0.7rem; color:var(--neon-cyan);">${s.className}</div>
                    <div style="font-size:0.84rem; font-weight:bold; color:${s.type === 'ult' ? 'var(--neon-pink)' : 'var(--neon-gold)'}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${s.name}</div>
                    <span class="skill-type-tag" style="font-size:0.6rem; padding:1px 4px;">${s.type.toUpperCase()}</span>
                </div>
            </div>
            <div style="font-size:0.68rem; color:var(--text-muted); margin-top:6px; line-height:1.25;">
                ${s.desc}
            </div>
            <div style="font-size:0.68rem; color:var(--neon-green); margin-top:4px; line-height:1.25; background:rgba(0,255,170,0.06); padding:3px 5px; border-radius:2px;">
                효과: <strong>${s.buffDesc || s.desc}</strong>
            </div>
            <div style="font-size:0.65rem; color:${s.target === 'self' ? 'var(--neon-green)' : (s.target === 'both' ? 'var(--neon-gold)' : 'var(--neon-pink)')}; margin-top:4px;">
                ${s.target === 'self' ? '🛡️ 본체 전용 방어/버프' : (s.target === 'both' ? '✨ 아군/적군 동시 작렬' : '⚔️ 전방 적진 타격기')}
            </div>
            <button class="btn-ctrl" onclick="selectClass('${s.classId}'); testSkillVfx('${s.name}', '${s.vfx}', '${s.type}', '${s.id}'); window.scrollTo({top:0, behavior:'smooth'});" style="margin-top:8px; font-size:0.68rem; width:100%;">
                ⚡ 스튜디오 시전 시험
            </button>
        </div>
    `).join('');
}

// =========================================================================
// 8. 14대 지역별 고유 환경 오브젝트 4프레임 루프 애니메이션 엔진 (7 FPS)
//    - 구름 레이어 완전 제거 (지역 몰입감 유지)
//    - 1~14지역마다 완전히 다른 고유 전경 오브젝트(`region_obj_${rId}_f0..3.png`)가 4프레임 주기로 작동
// =========================================================================
let bgFoliageFrameIdx = 0;
let isFoliageLoopActive = true;
let foliageLoopTimer = null;
const preloadedRegionBgs = {};

const REGION_UNIQUE_PROP_NAMES = {
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
};

const FOLIAGE_FRAME_LABELS = [
    "Frame 1/4 (기본 위치 · 0px)",
    "Frame 2/4 (살짝 흔들림/타오름 · +1단계)",
    "Frame 3/4 (최대 흔들림/파동 · +2단계)",
    "Frame 4/4 (복귀 중간 단계 · +1단계)"
];

function preloadRegion4FrameBackgrounds(rId) {
    if (preloadedRegionBgs[rId]) return;
    preloadedRegionBgs[rId] = [];
    for (let f = 0; f < 4; f++) {
        const tImg = new Image();
        tImg.src = `assets/ui/regions/town_bg_${rId}_f${f}.png?v=10`;
        const bImg = new Image();
        bImg.src = `assets/ui/regions/battle_bg_${rId}_f${f}.png?v=10`;
        const oImg = new Image();
        oImg.src = `assets/ui/regions/region_obj_${rId}_f${f}.png?v=10`;
        preloadedRegionBgs[rId].push(tImg, bImg, oImg);
    }
}

function applyRegionSwayFrame(rId, fIdx) {
    const townView = document.getElementById('townBgView');
    if (townView) {
        townView.style.backgroundImage = `url('assets/ui/regions/town_bg_${rId}_f${fIdx}.png?v=10')`;
    }
    const battleView = document.getElementById('battleBgView');
    if (battleView) {
        battleView.style.backgroundImage = `url('assets/ui/regions/battle_pano_${rId}.png?v=10')`;
    }
    const studioStage = document.getElementById('studioStage');
    if (studioStage) {
        studioStage.style.backgroundImage = `url('assets/ui/regions/town_bg_${rId}_f${fIdx}.png?v=10')`;
    }

    // 각 지역(1~14)마다 고유한 4프레임 환경 오브젝트 오버레이 적용!
    const overlayUrl = `url('assets/ui/regions/region_obj_${rId}_f${fIdx}.png?v=10')`;
    const townFol = document.getElementById('townFoliageLayer');
    if (townFol) townFol.style.backgroundImage = overlayUrl;
    const battleFol = document.getElementById('battleFoliageLayer');
    if (battleFol) battleFol.style.backgroundImage = `url('assets/ui/regions/nature_props_pano_${rId}.png?v=10')`;
    const studioFol = document.getElementById('studioFoliageLayer');
    if (studioFol) studioFol.style.backgroundImage = overlayUrl;

    const propBadge = document.getElementById('regionPropNameBadge');
    if (propBadge) {
        propBadge.textContent = REGION_UNIQUE_PROP_NAMES[rId] || REGION_UNIQUE_PROP_NAMES[1];
    }

    const statusEl = document.getElementById('foliageLoopStatusText');
    if (statusEl) {
        statusEl.textContent = `${FOLIAGE_FRAME_LABELS[fIdx]} (7 FPS)`;
    }
}

function tickFoliage4FrameLoop() {
    if (!isFoliageLoopActive) return;
    bgFoliageFrameIdx = (bgFoliageFrameIdx + 1) % 4;
    applyRegionSwayFrame(currentRegionId, bgFoliageFrameIdx);

    // 4프레임 주기마다 전투장 몬스터와 영웅도 고전 16비트 특유의 대기 호흡 연출
    const bossSprite = document.getElementById('battleBossSprite');
    if (bossSprite) {
        const meta = getWaveMonsterMeta(currentRegionId, currentGateWave);
        if (!meta.isFlying) {
            // 지상 몬스터: 발바닥을 바닥에 완벽히 고정한 채 미세한 호흡(Breathing) 연출 (붕 뜸 원천 차단)
            const breathScale = (bgFoliageFrameIdx % 2 === 1) ? 1.015 : 1.0;
            bossSprite.style.transformOrigin = 'bottom center';
            bossSprite.style.transform = `scaleX(-1) scaleY(${breathScale})`;
        }
    }
    const battleHeroImg = document.getElementById('battleHeroSpriteImg');
    if (battleHeroImg) {
        const heroBobY = (bgFoliageFrameIdx % 2 === 1) ? -2 : 0;
        battleHeroImg.style.transform = `scaleX(1) translateY(${heroBobY}px)`;
    }
}

function toggleFoliageSwayLoop() {
    isFoliageLoopActive = !isFoliageLoopActive;
    const btn = document.getElementById('btnToggleFoliageLoop');
    if (btn) {
        btn.classList.toggle('active', isFoliageLoopActive);
        btn.textContent = `🌿 은문 스타일 부드러운 유영(Float) 모션: ${isFoliageLoopActive ? 'ON' : 'OFF'}`;
    }
}

// 초기화
window.addEventListener('DOMContentLoaded', () => {
    selectClass("necro");
    switchView("side");
    setAnimation("idle");
    animInterval = setInterval(tickAnimationFrame, 100);

    // 지역별 고유 환경 오브젝트 4프레임 루프: 초당 약 7 FPS (142ms 간격)
    foliageLoopTimer = setInterval(tickFoliage4FrameLoop, 260);

    renderRegressionUi();
    renderUniqueItems();
    renderAllSkillsGallery();
    switchRegionTheme(1);
});
