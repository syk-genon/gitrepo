// =========================================================================
// PROJECT NECRO: 목적을 잃지 않는 사령군주 - 2D 도트 RPG 메인 엔진 (index.js v12)
// 12대 직업 · 72종 스킬 · 60종 신화 세트 · 36종 고유 유물 · 무한 회귀 영혼 각인 완비
// =========================================================================

const SAVE_KEY = "PROJECT_NECRO_SAVE_V1";

// =========================================================================
// 고도화 1: Web Audio API 8비트 레트로 칩튠 신디사이저 사운드 엔진
// =========================================================================
const SoundEngine = {
    ctx: null,
    enabled: true,
    bgmInterval: null,
    bgmMode: null,
    init() {
        if (!this.ctx && typeof AudioContext !== 'undefined') {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume().catch(() => {});
        }
    },
    playTone(freq, type = 'square', duration = 0.1, vol = 0.12, slideTo = null) {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, now);
            if (slideTo) {
                osc.frequency.exponentialRampToValueAtTime(Math.max(10, slideTo), now + duration);
            }
            gain.gain.setValueAtTime(vol, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + duration);
        } catch (e) {}
    },
    playNoise(duration = 0.15, vol = 0.15) {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        try {
            const bufferSize = Math.floor(this.ctx.sampleRate * duration);
            const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const output = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                output[i] = Math.random() * 2 - 1;
            }
            const whiteNoise = this.ctx.createBufferSource();
            whiteNoise.buffer = buffer;
            const gain = this.ctx.createGain();
            const now = this.ctx.currentTime;
            gain.gain.setValueAtTime(vol, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
            whiteNoise.connect(gain);
            gain.connect(this.ctx.destination);
            whiteNoise.start(now);
        } catch (e) {}
    },
    click() { this.playTone(880, 'square', 0.04, 0.08, 1200); },
    hit() { this.playTone(220, 'triangle', 0.07, 0.15, 80); this.playNoise(0.05, 0.08); },
    crit() { this.playTone(587, 'square', 0.08, 0.18, 1174); setTimeout(() => this.playTone(1174, 'square', 0.1, 0.18, 1760), 50); },
    skill() { this.playTone(440, 'triangle', 0.15, 0.14, 880); },
    burst() { this.playTone(160, 'sawtooth', 0.25, 0.2, 40); this.playNoise(0.18, 0.2); },
    potion() {
        [523, 659, 784].forEach((f, i) => setTimeout(() => this.playTone(f, 'sine', 0.09, 0.12), i * 50));
    },
    levelUp() {
        [523, 659, 784, 1046].forEach((f, i) => setTimeout(() => this.playTone(f, 'square', 0.12, 0.15), i * 70));
    },
    enhance() {
        this.playTone(1760, 'square', 0.08, 0.18, 880);
        setTimeout(() => {
            [880, 1108, 1318, 1760].forEach((f, i) => setTimeout(() => this.playTone(f, 'triangle', 0.12, 0.12), i * 50));
        }, 80);
    },
    boss() {
        this.playTone(110, 'sawtooth', 0.45, 0.22, 75);
    },
    startBgm(mode = 'hub') {
        if (this.bgmMode === mode) return;
        this.stopBgm();
        this.bgmMode = mode;
        if (!this.enabled) return;
        let step = 0;
        const hubNotes = [261, 329, 392, 440, 392, 329, 293, 261];
        const battleNotes = [146, 146, 220, 146, 174, 146, 196, 220];
        this.bgmInterval = setInterval(() => {
            if (!this.enabled) return;
            const notes = mode === 'battle' ? battleNotes : hubNotes;
            const note = notes[step % notes.length];
            this.playTone(note, mode === 'battle' ? 'sawtooth' : 'sine', mode === 'battle' ? 0.08 : 0.15, 0.035);
            step++;
        }, mode === 'battle' ? 200 : 420);
    },
    stopBgm() {
        if (this.bgmInterval) { clearInterval(this.bgmInterval); this.bgmInterval = null; }
        this.bgmMode = null;
    },
    toggle() {
        this.enabled = !this.enabled;
        if (!this.enabled) this.stopBgm();
        return this.enabled;
    }
};

// -------------------------------------------------------------------------
// 에셋 경로 정규화 매핑 (C1, C2 버그 해결)
// -------------------------------------------------------------------------
const ASSET = {
    battlePano: (r) => `assets/ui/regions/battle_pano_${r}.png?v=11`,
    propsPano:  (r) => `assets/ui/regions/nature_props_pano_${r}.png?v=11`,
    monster:    (r, w) => `assets/monsters/m_${r}_${w === 5 ? 'named' : w === 6 ? 'boss' : w}.png?v=11`,
    summon:     (key) => `assets/summons/minion_${key}.png?v=11`
};

const SUMMON_DEFS = {
    skeleton_warrior: { name: "해골 전사",   sprite: ASSET.summon("skeleton_warrior"), atkMul: 0.25 },
    skeleton_archer:  { name: "해골 궁수",   sprite: ASSET.summon("skeleton_archer"),  atkMul: 0.25 },
    skeleton_mage:    { name: "해골 마법사", sprite: ASSET.summon("skeleton_mage"),    atkMul: 0.30 },
    arthur:           { name: "듀라한 아서", sprite: ASSET.summon("death_knight"),     atkMul: 0.90 },
    shadow_clone:     { name: "그림자 분신", sprite: ASSET.summon("shadow_clone"),     atkMul: 0.50 },
    drone:            { name: "강습 드론",   sprite: ASSET.summon("lich_mage"),        atkMul: 0.35 }
};

const SKILL_SUMMONS = {
    necro_1: ['skeleton_warrior', 'skeleton_archer', 'skeleton_mage'],
    necro_5: ['arthur'],
    as_4:    ['shadow_clone', 'shadow_clone'],
    psi_5:   ['drone', 'drone', 'drone', 'drone']
};

const BASE_STATS = {
    level: 1,
    exp: 0,
    maxExp: 100,
    maxHp: 1200,
    maxMp: 600,
    baseAtk: 140,
    baseDef: 90,
    critRate: 0.15,
    critDmg: 1.5,
    atkSpeed: 1.0
};

// -------------------------------------------------------------------------
// 고유 유물 조회 헬퍼 (C6 버그 해결: 숫자 ID 1..36)
// -------------------------------------------------------------------------
const getUnique = (id) => UNIQUE_ITEMS_DATA.find(u => u.id === id);
const hasUnique = (id) => gameState.player.equippedUniques && gameState.player.equippedUniques.includes(id);

// -------------------------------------------------------------------------
// 게임 상태 (State)
// -------------------------------------------------------------------------
let gameState = {
    player: {
        classId: "necro",
        name: "💀 최미남 (사령군주)",
        model: "최미남 (사령군주)",
        level: 1,
        exp: 0,
        maxExp: 100,
        hp: 1200,
        maxHp: 1200,
        mp: 600,
        maxMp: 600,
        baseAtk: 140,
        baseDef: 90,
        critRate: 0.15,
        critDmg: 1.5,
        atkSpeed: 1.0,
        gold: 1500,
        potions: { hp: 5, mp: 5 },
        equippedSkills: ["necro_1", "necro_2", "necro_3", "necro_4", "necro_ult"],
        unlockedSkills: ["necro_1", "necro_2", "necro_3", "necro_4", "necro_5", "necro_ult"],
        equippedGear: {
            ring: null,
            weapon: { id: "set_necro_weapon", name: "🦯 심연의 척추 지팡이", part: "weapon", enhance: 0, stat: 60 },
            armor: null,
            helmet: null,
            core: null
        },
        uniqueInventory: [7], // 아서의 해골 투구
        equippedUniques: [7],
        traits: {},           // L3: 올바른 키만 저장
        talents: {},
        masterSoulUnlocked: false,
        masterSoul: null,
        regressionCount: 0,
        maxRegionUnlocked: 1,
        lastSaveTime: Date.now()
    },
    battle: {
        active: false,
        regionId: 1,
        wave: 1,
        speed: 1,
        auto: true,
        autoNextRegion: false,
        sessionDamage: 0,
        sessionGold: 0,
        sessionKills: 0,
        sessionStartTime: 0,
        playerCooldowns: {},
        minions: [],
        enemy: null,
        lastTick: 0,
        playerAttackTimer: 0,
        enemyAttackTimer: 0,
        autoCastTimer: 0,
        lastNoMpWarn: 0,
        reviveUsed: false,
        playerShield: 0,
        playerInvulnUntil: 0,
        dodgeCharges: 0,
        enemyStunUntil: 0,
        enemyDebuffAtkUntil: 0,
        playerBuffAtkUntil: 0
    }
};

let selectedClassTemp = "necro";
let selectedForgeSlot = "weapon";
let selectedSkillSlotIndex = 0;
let currentSkillFilter = "all";

// =========================================================================
// 1. 초기화 및 세이브/로드 시스템
// =========================================================================

window.addEventListener("DOMContentLoaded", () => {
    loadGameState();
    renderStartScreen();
    setupKeybindings();

    setInterval(() => {
        if (gameState.player) saveGameState(false);
    }, 10000);

    requestAnimationFrame(gameLoop);
});

function loadGameState() {
    try {
        const saved = localStorage.getItem(SAVE_KEY);
        if (saved) {
            const data = JSON.parse(saved);
            if (data && data.player) {
                gameState.player = Object.assign(gameState.player, data.player);

                // C6 구버전 문자열 키 ('unique_01')를 숫자(1)로 변환
                const toNum = (v) => typeof v === 'number' ? v : parseInt(String(v).replace('unique_', ''), 10);
                gameState.player.uniqueInventory = (gameState.player.uniqueInventory || []).map(toNum).filter(n => n >= 1 && n <= 36);
                gameState.player.equippedUniques = (gameState.player.equippedUniques || []).map(toNum).filter(n => n >= 1 && n <= 36);

                // L3 없는 traits/talents 키 정리
                if (gameState.player.traits) {
                    Object.keys(gameState.player.traits).forEach(k => {
                        if (!TRAITS_DATA[k]) delete gameState.player.traits[k];
                    });
                }
                if (gameState.player.talents) {
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
}

function saveGameState(notify = false) {
    try {
        gameState.player.lastSaveTime = Date.now();
        localStorage.setItem(SAVE_KEY, JSON.stringify({ player: gameState.player }));
        if (notify) showFloatingText(document.body, "💾 저장되었습니다!", "var(--neon-green)");
    } catch (e) {
        console.error("저장 실패:", e);
    }
}

function resetGameData() {
    if (confirm("정말로 모든 세이브 데이터를 초기화하고 처음부터 다시 시작하시겠습니까?")) {
        localStorage.removeItem(SAVE_KEY);
        location.reload();
    }
}

function setupKeybindings() {
    window.addEventListener("keydown", (e) => {
        if (!gameState.battle.active) return;
        const key = e.key.toUpperCase();
        if (key === "Q") useSkillSlot(0);
        else if (key === "W") useSkillSlot(1);
        else if (key === "E") useSkillSlot(2);
        else if (key === "R") useSkillSlot(3);
        else if (key === " " || key === "SPACEBAR") { e.preventDefault(); useSkillSlot(4); }
        else if (key === "1") usePotion("hp");
        else if (key === "2") usePotion("mp");
    });
}


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
        const curScreen = (typeof document !== "undefined" && document.querySelector) ? document.querySelector(".game-screen.active") : null;
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

function switchScreen(screenId) {
    document.querySelectorAll(".game-screen").forEach(el => el.classList.remove("active"));
    const target = document.getElementById(screenId);
    if (target) {
        target.classList.add("active");
        if (screenId === "screen-hub") {
            refreshHubUI();
            SoundEngine.startBgm('hub');
        } else if (screenId === "screen-battle") {
            SoundEngine.startBgm('battle');
        } else if (screenId === "screen-start") {
            SoundEngine.stopBgm();
        }
    }
}

// =========================================================================
// 2. 타이틀 & 클래스 선택 화면 (L10 새 게임 초기화)
// =========================================================================

function renderStartScreen() {
    const previewContainer = document.getElementById("startClassesIcons");
    if (!previewContainer) return;
    previewContainer.innerHTML = "";

    Object.values(CLASSES_DATA).forEach(cls => {
        const img = document.createElement("img");
        img.className = "start-class-avatar";
        img.src = cls.sprite;
        img.title = `${cls.name} (${cls.model})`;
        img.onclick = () => {
            selectedClassTemp = cls.id;
            switchScreen("screen-class-select");
            renderClassSelectScreen();
        };
        previewContainer.appendChild(img);
    });

    const btnCont = document.getElementById("btnContinueGame");
    const hasSave = localStorage.getItem(SAVE_KEY) !== null;
    if (btnCont) {
        btnCont.disabled = !hasSave;
        btnCont.style.opacity = hasSave ? "1" : "0.5";
    }
}

function startNewGamePrompt() {
    const hasSave = localStorage.getItem(SAVE_KEY) !== null;
    if (hasSave) {
        if (!confirm("기존 진행 데이터가 있습니다. 새로운 여정을 시작하면 이전 기록이 초기화됩니다. 계속하시겠습니까?")) {
            return;
        }
    }
    localStorage.removeItem(SAVE_KEY);
    switchScreen("screen-class-select");
    renderClassSelectScreen();
}

function continueSavedGame() {
    switchScreen("screen-hub");
    refreshHubUI();
}

function renderClassSelectScreen() {
    const grid = document.getElementById("classSelectGrid");
    if (!grid) return;
    grid.innerHTML = "";

    Object.values(CLASSES_DATA).forEach(cls => {
        const card = document.createElement("div");
        card.className = `hanji-card class-card ${selectedClassTemp === cls.id ? 'selected' : ''}`;
        card.onclick = () => {
            selectedClassTemp = cls.id;
            renderClassSelectScreen();
        };

        card.innerHTML = `
            <div class="class-card-header">
                <img src="${cls.sprite}" class="class-card-sprite">
                <div>
                    <div style="font-size: 0.95rem; color: var(--neon-gold); font-weight: bold;">${cls.name}</div>
                    <div style="font-size: 0.72rem; color: var(--neon-cyan);">${cls.model}</div>
                </div>
            </div>
            <div style="font-size: 0.74rem; color: var(--neon-green);">스탯: <strong>${cls.mainStat}</strong></div>
            <div style="font-size: 0.72rem; color: var(--text-muted); line-height: 1.3;">${cls.desc}</div>
            <div style="font-size: 0.7rem; color: var(--neon-gold); margin-top: 4px;">궁극: ${cls.ultimate}</div>
        `;
        grid.appendChild(card);
    });
}

function confirmSelectedClass() {
    const cls = CLASSES_DATA[selectedClassTemp];
    if (!cls) return;

    // 완전히 새로운 캐릭터 생성
    resetLife(gameState.player, null);
    gameState.player.classId = cls.id;
    gameState.player.name = cls.name;
    gameState.player.model = cls.model;

    // 해당 클래스의 기본 스킬 해금
    gameState.player.unlockedSkills = [];
    cls.skills.forEach(s => gameState.player.unlockedSkills.push(s.id));
    gameState.player.equippedSkills = [
        cls.skills[0].id,
        cls.skills[1].id,
        cls.skills[2].id,
        cls.skills[3].id,
        cls.skills[5].id // 궁극기
    ];

    // 시작 장비: 무기 1부위 지급 (세트는 보스 파밍으로 완성)
    gameState.player.equippedGear = makeStarterGear(cls.id);

    saveGameState(false);
    switchScreen("screen-hub");
    refreshHubUI();
}

function makeStarterGear(classId) {
    const cls = CLASSES_DATA[classId];
    const gear = { ring: null, weapon: null, armor: null, helmet: null, core: null };
    if (cls && cls.setParts && cls.setParts[1]) {
        gear.weapon = {
            id: `set_${classId}_weapon`,
            name: cls.setParts[1].name,
            part: "weapon",
            enhance: 0,
            stat: 60
        };
    }
    return gear;
}

// =========================================================================
// 3. 수치 통합 및 능력치 계산 엔진 (L4)
// =========================================================================

const lvMul = (lv) => 1 + 0.5 * (lv - 1);
const tVal = (dict, owned, id) => owned[id] ? dict[id].baseVal * lvMul(owned[id]) / 100 : 0;

function getEffectiveStats() {
    const p = gameState.player;
    const T = (id) => tVal(TRAITS_DATA, p.traits, id);
    const L = (id) => tVal(TALENTS_DATA, p.talents, id);

    const gearMul = 1 + L('talent_blacksmith');
    let atk = p.baseAtk;
    let def = p.baseDef;

    Object.values(p.equippedGear).forEach(g => {
        if (!g) return;
        const s = g.stat * (1 + g.enhance * 0.15) * gearMul;
        if (g.part === 'weapon' || g.part === 'ring' || g.part === 'core') atk += s;
        else def += s;
    });

    if (hasUnique(1)) def *= 2.0; // 강두호의 담금질 망치
    def *= (1 + T('trait_iron_body'));

    const maxHp = Math.round(p.maxHp * (1 + T('trait_iron_body')));
    const maxMp = p.maxMp;

    return {
        atk,
        def,
        maxHp,
        maxMp,
        critRate:   p.critRate + T('trait_hawk_eye'),
        critDmg:    p.critDmg  + T('trait_hawk_eye'),
        atkSpeed:   p.atkSpeed * (1 + T('trait_shadow_step')),
        mpRegen:    15 * (1 + T('trait_mana_flow')),
        minionMul:  1 + T('trait_undead_cmd'),
        skillMul:   (1 + T('trait_frost_heart')) * (hasUnique(17) ? 1.9 : 1),
        bossMul:    1 + T('trait_boss_slayer'),
        killHeal:   T('trait_blood_vamp'),
        reflect:    T('trait_thorn_armor'),
        healMul:    1 + T('trait_holy_grace'),
        goldMul:    (1 + L('talent_merchant')) * (hasUnique(13) ? 2 : 1),
        expMul:     (1 + L('talent_exp_surge')) * (hasUnique(34) ? 3 : 1),
        cdMul:      Math.max(0.2, 1 - L('talent_cooldown')),
        dropMul:    1 + L('talent_relic_finder'),
        doubleCast: L('talent_double_cast'),
        enemyHpMul: Math.max(0.5, 1 - L('talent_gate_breaker')),
        lowHpDR:    L('talent_immortal_will'),
        mpCostMul:  hasUnique(17) ? 2 : 1
    };
}

function calculateCombatPower() {
    const s = getEffectiveStats();
    const p = gameState.player;
    const traitCount = Object.keys(p.traits).length;
    const talentCount = Object.keys(p.talents).length;
    return Math.floor(s.atk * 4.5 + s.def * 3.8 + traitCount * 300 + talentCount * 300 + (p.regressionCount * 600));
}

// =========================================================================
// 4. 거점 마을 (HUB) 시스템
// =========================================================================

function switchHubTab(tabId) {
    document.querySelectorAll(".hub-tab-btn").forEach(btn => {
        btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });
    document.querySelectorAll(".hub-panel").forEach(panel => {
        panel.classList.toggle("active", panel.id === tabId);
    });

    if (tabId === "tab-gates") renderGatesMap();
    else if (tabId === "tab-blacksmith") renderBlacksmith();
    else if (tabId === "tab-skills") renderSkillSanctuary();
    else if (tabId === "tab-inventory") renderInventory();
    else if (tabId === "tab-shop") renderShop();
    else if (tabId === "tab-altar") renderAltar();
}

function refreshHubUI() {
    const p = gameState.player;
    const cls = CLASSES_DATA[p.classId] || CLASSES_DATA["necro"];

    const avatar = document.getElementById("hubPlayerAvatar");
    if (avatar) avatar.src = cls.sprite;

    const nameEl = document.getElementById("hubPlayerName");
    if (nameEl) nameEl.textContent = `${p.name} (Lv.${p.level})`;

    const modelEl = document.getElementById("hubPlayerModel");
    if (modelEl) modelEl.textContent = p.model;

    const goldEl = document.getElementById("hubGoldText");
    if (goldEl) goldEl.textContent = Math.floor(p.gold).toLocaleString();

    const regEl = document.getElementById("hubRegressionText");
    if (regEl) regEl.textContent = `${p.regressionCount}회차`;

    const maxRegEl = document.getElementById("hubMaxRegionUnlockedText");
    if (maxRegEl) {
        const regInfo = REGIONS_DATA[p.maxRegionUnlocked] || REGIONS_DATA[1];
        maxRegEl.textContent = `지역 ${p.maxRegionUnlocked} (${regInfo.name})`;
    }

    const cp = calculateCombatPower();
    const cpEl = document.getElementById("hubCombatPowerText");
    if (cpEl) cpEl.textContent = cp.toLocaleString();

    renderGatesMap();
}

// -------------------------------------------------------------------------
// TAB 1: 차원문 원정
// -------------------------------------------------------------------------
function renderGatesMap() {
    const grid = document.getElementById("gatesMapGrid");
    if (!grid) return;
    grid.innerHTML = "";

    const p = gameState.player;

    for (let r = 1; r <= 14; r++) {
        const reg = REGIONS_DATA[r];
        if (!reg) continue;

        const isUnlocked = r <= p.maxRegionUnlocked;
        const gate = GATES_DATA[reg.gateType] || GATES_DATA["iron"];
        const featureText = (reg.gateFeature || reg.lore || "").slice(0, 60);
        const bossName = reg.boss || "미지의 보스";

        const card = document.createElement("div");
        card.className = `hanji-card gate-card ${isUnlocked ? '' : 'locked'}`;
        card.style.opacity = isUnlocked ? "1" : "0.55";

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="gate-tier-badge" style="color: ${gate.color}; border-color: ${gate.color};">
                        🚪 ${gate.name}
                    </span>
                    <h4 style="font-size: 1rem; color: var(--neon-gold); margin-top: 4px;">${r}. ${reg.name}</h4>
                    <div style="font-size: 0.72rem; color: var(--neon-cyan);">${reg.traitName || ''}</div>
                </div>
                <img src="${gate.sprite}" style="width: 44px; height: 50px; object-fit: contain;">
            </div>

            <div style="font-size: 0.72rem; color: var(--text-muted); margin: 8px 0; line-height: 1.3;">
                ${featureText}...
            </div>

            <div style="font-size: 0.7rem; color: var(--neon-green); margin-bottom: 8px;">
                👾 6웨이브 보스: <strong>${bossName}</strong>
            </div>

            <button class="btn-pixel ${isUnlocked ? 'gold' : ''}" style="width: 100%; font-size: 0.8rem; padding: 6px;"
                    ${isUnlocked ? `onclick="startGateBattle(${r})"` : 'disabled'}>
                ${isUnlocked ? '⚔️ 차원문 출정하기' : '🔒 이전 차원문 클리어 필요'}
            </button>
        `;

        grid.appendChild(card);
    }
}

// -------------------------------------------------------------------------
// TAB 2: 대장간
// -------------------------------------------------------------------------
function renderBlacksmith() {
    const list = document.getElementById("blacksmithEquipList");
    if (!list) return;
    list.innerHTML = "";

    const p = gameState.player;
    const parts = ["weapon", "armor", "helmet", "ring", "core"];

    parts.forEach(partKey => {
        const item = p.equippedGear[partKey];
        const row = document.createElement("div");
        row.className = `btn-pixel ${selectedForgeSlot === partKey ? 'active' : ''}`;
        row.style.width = "100%";
        row.style.justifyContent = "space-between";
        row.style.fontSize = "0.78rem";
        row.onclick = () => {
            selectedForgeSlot = partKey;
            renderBlacksmith();
        };

        if (item) {
            row.innerHTML = `
                <span>${item.name}</span>
                <span style="color: var(--neon-gold); font-weight: bold;">+${item.enhance}강</span>
            `;
        } else {
            row.innerHTML = `<span style="color: var(--text-muted);">${partKey} (미장착)</span><span>-</span>`;
        }
        list.appendChild(row);
    });

    updateForgeTargetUI();
}

function updateForgeTargetUI() {
    const item = gameState.player.equippedGear[selectedForgeSlot];
    const nameEl = document.getElementById("forgeTargetName");
    const statEl = document.getElementById("forgeStatPreview");
    const costEl = document.getElementById("forgeCostPreview");
    const btn = document.getElementById("btnDoEnhance");
    const resultEl = document.getElementById("forgeResultMsg");

    if (resultEl) resultEl.textContent = "";

    if (!item) {
        if (nameEl) nameEl.textContent = "장비 미착용";
        if (statEl) statEl.textContent = "-";
        if (costEl) costEl.textContent = "비용: -";
        if (btn) btn.disabled = true;
        return;
    }

    const currentStat = Math.floor(item.stat * (1 + item.enhance * 0.15));
    const nextStat = Math.floor(item.stat * (1 + (item.enhance + 1) * 0.15));
    const cost = (item.enhance + 1) * 350;

    if (nameEl) nameEl.textContent = `${item.name} (+${item.enhance}강)`;
    if (statEl) statEl.textContent = `능력치: ${currentStat} ➔ ${nextStat} (+15%)`;
    if (costEl) costEl.textContent = `강화 비용: ${cost.toLocaleString()} 골드 (성공률: 100%)`;

    if (btn) {
        btn.disabled = gameState.player.gold < cost || item.enhance >= 15;
        btn.textContent = item.enhance >= 15 ? "⭐ 최대 강화 달성 (+15)" : `🔨 망치질 실행 (+${item.enhance + 1}강)`;
    }
}

function performEnhancement() {
    const item = gameState.player.equippedGear[selectedForgeSlot];
    if (!item || item.enhance >= 15) return;

    const cost = (item.enhance + 1) * 350;
    if (gameState.player.gold < cost) {
        alert("골드가 부족합니다!");
        return;
    }

    gameState.player.gold -= cost;
    item.enhance += 1;

    SoundEngine.enhance();
    const resultEl = document.getElementById("forgeResultMsg");
    if (resultEl) {
        resultEl.textContent = `✨ 강화 성공! ${item.name}이(가) +${item.enhance}강이 되었습니다!`;
        resultEl.style.color = "var(--neon-gold)";
    }

    refreshHubUI();
    renderBlacksmith();
    saveGameState(false);
}

// -------------------------------------------------------------------------
// TAB 3: 스킬 성소
// -------------------------------------------------------------------------
function renderSkillSanctuary() {
    renderEquippedSkillSlots();
    renderSkillFilterTabs();
    renderSkillLibraryGrid();
}

function renderEquippedSkillSlots() {
    const container = document.getElementById("equippedSkillsBar");
    if (!container) return;
    container.innerHTML = "";

    const p = gameState.player;
    const hotkeys = ["Q", "W", "E", "R", "SPACE"];

    for (let i = 0; i < 5; i++) {
        const skillId = p.equippedSkills[i];
        const skill = findSkillById(skillId);

        const slot = document.createElement("div");
        slot.className = `skill-slot-btn ${i === 4 ? 'ult-slot' : ''} ${selectedSkillSlotIndex === i ? 'active' : ''}`;
        slot.onclick = () => {
            selectedSkillSlotIndex = i;
            renderEquippedSkillSlots();
        };

        slot.innerHTML = `
            <span class="skill-hotkey-badge">${hotkeys[i]}</span>
            ${skill ? `<img src="${skill.vfx}" class="skill-slot-icon">` : `<span style="font-size:0.7rem; color:var(--text-muted);">빈 슬롯</span>`}
            <div style="font-size: 0.6rem; color: var(--neon-gold); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 60px;">
                ${skill ? skill.name.split(' ')[0] : '-'}
            </div>
        `;
        container.appendChild(slot);
    }
}

function renderSkillFilterTabs() {
    const tabsContainer = document.getElementById("skillFilterClassTabs");
    if (!tabsContainer) return;
    tabsContainer.innerHTML = "";

    const filterOptions = [
        { id: "all", name: "전체" },
        { id: "necro", name: "사령" },
        { id: "guardian", name: "수호" },
        { id: "storm_wizard", name: "마도" },
        { id: "sniper", name: "저격" },
        { id: "priest", name: "신성" },
        { id: "sword_master", name: "검왕" }
    ];

    filterOptions.forEach(opt => {
        const btn = document.createElement("button");
        btn.className = `btn-pixel ${currentSkillFilter === opt.id ? 'active' : ''}`;
        btn.style.fontSize = "0.68rem";
        btn.style.padding = "2px 8px";
        btn.textContent = opt.name;
        btn.onclick = () => {
            currentSkillFilter = opt.id;
            renderSkillFilterTabs();
            renderSkillLibraryGrid();
        };
        tabsContainer.appendChild(btn);
    });
}

function renderSkillLibraryGrid() {
    const grid = document.getElementById("skillLibraryGrid");
    if (!grid) return;
    grid.innerHTML = "";

    const p = gameState.player;

    Object.values(CLASSES_DATA).forEach(cls => {
        if (currentSkillFilter !== "all" && cls.id !== currentSkillFilter) return;

        cls.skills.forEach(skill => {
            const isUnlocked = p.unlockedSkills.includes(skill.id);
            const isEquipped = p.equippedSkills.includes(skill.id);

            const card = document.createElement("div");
            card.className = `hanji-card ${isUnlocked ? '' : 'locked'}`;
            card.style.padding = "8px 10px";
            card.style.opacity = isUnlocked ? "1" : "0.45";
            card.style.display = "flex";
            card.style.alignItems = "center";
            card.style.justifyContent = "space-between";

            card.innerHTML = `
                <div style="display: flex; align-items: center; gap: 8px;">
                    <img src="${skill.vfx}" style="width: 36px; height: 36px; object-fit: contain; background: #0c0806; border: 1px solid var(--border-wood-light);">
                    <div>
                        <div style="font-size: 0.8rem; color: var(--neon-gold); font-weight: bold;">
                            ${skill.name} ${isEquipped ? '⭐' : ''}
                        </div>
                        <div style="font-size: 0.68rem; color: var(--neon-cyan);">${cls.name} · ${skill.type}</div>
                    </div>
                </div>
                <button class="btn-pixel ${isEquipped ? 'gold' : ''}" style="font-size: 0.68rem; padding: 3px 8px;"
                        ${isUnlocked ? `onclick="equipSkillToSlot('${skill.id}')"` : 'disabled'}>
                    ${isEquipped ? '장착 중' : isUnlocked ? '장착' : '미해금'}
                </button>
            `;

            grid.appendChild(card);
        });
    });
}

function equipSkillToSlot(skillId) {
    if (!gameState.player.unlockedSkills.includes(skillId)) return;
    gameState.player.equippedSkills[selectedSkillSlotIndex] = skillId;
    saveGameState(false);
    renderEquippedSkillSlots();
    renderSkillLibraryGrid();
}

function findSkillById(skillId) {
    if (!skillId) return null;
    for (const cls of Object.values(CLASSES_DATA)) {
        for (const s of cls.skills) {
            if (s.id === skillId) return s;
        }
    }
    return null;
}

// -------------------------------------------------------------------------
// TAB 4: 인벤토리 & 세트 장비
// -------------------------------------------------------------------------
function renderInventory() {
    renderEquippedGearList();
    renderUniqueArtifactsList();
}

function renderEquippedGearList() {
    const list = document.getElementById("equippedGearGrid");
    if (!list) return;
    list.innerHTML = "";

    const p = gameState.player;
    const parts = [
        { key: "ring", label: "💍 반지 (1세트)" },
        { key: "weapon", label: "🦯 주무기 (2세트)" },
        { key: "armor", label: "🥋 갑옷 (3세트)" },
        { key: "helmet", label: "💀 투구 (4세트)" },
        { key: "core", label: "💎 코어 (5세트 완성)" }
    ];

    let equippedCount = 0;

    parts.forEach(pDef => {
        const item = p.equippedGear[pDef.key];
        const row = document.createElement("div");
        row.className = "btn-pixel";
        row.style.width = "100%";
        row.style.justifyContent = "space-between";
        row.style.padding = "8px 12px";

        if (item) {
            equippedCount++;
            const enhancedStat = Math.floor(item.stat * (1 + item.enhance * 0.15));
            row.innerHTML = `
                <div>
                    <div style="font-size: 0.8rem; color: var(--neon-gold);">${item.name}</div>
                    <div style="font-size: 0.68rem; color: var(--text-muted);">${pDef.label}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.8rem; color: var(--neon-green);">+${item.enhance}강</div>
                    <div style="font-size: 0.68rem; color: var(--neon-cyan);">능력치: ${enhancedStat}</div>
                </div>
            `;
        } else {
            row.innerHTML = `<span style="color: var(--text-muted);">${pDef.label} - 미착용</span>`;
        }
        list.appendChild(row);
    });

    const setBonusEl = document.getElementById("activeSetBonusText");
    if (setBonusEl) {
        const cls = CLASSES_DATA[p.classId] || CLASSES_DATA["necro"];
        if (equippedCount >= 5) {
            setBonusEl.innerHTML = `<strong>[5세트 완성]:</strong> ${cls.setName} 극의 활성화! ${cls.ultimate} 해금 및 전 스탯 +40%!`;
            setBonusEl.style.color = "var(--neon-gold)";
        } else {
            setBonusEl.innerHTML = `현재 ${equippedCount}/5 부위 착용 중 (${cls.setName})`;
            setBonusEl.style.color = "var(--text-muted)";
        }
    }
}

function renderUniqueArtifactsList() {
    const container = document.getElementById("inventoryUniqueList");
    if (!container) return;
    container.innerHTML = "";

    const p = gameState.player;

    if (!p.uniqueInventory || p.uniqueInventory.length === 0) {
        container.innerHTML = `<div style="font-size:0.75rem; color:var(--text-muted); padding:10px;">보유 중인 고유 유물이 없습니다. 차원문 보스를 격파하여 파밍하십시오.</div>`;
        return;
    }

    p.uniqueInventory.forEach(uId => {
        const u = getUnique(uId);
        if (!u) return;

        const isEquipped = p.equippedUniques && p.equippedUniques.includes(uId);

        const card = document.createElement("div");
        card.className = `hanji-card ${isEquipped ? 'active' : ''}`;
        card.style.padding = "8px";
        card.style.display = "flex";
        card.style.flexDirection = "column";
        card.style.gap = "4px";

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.8rem; color: var(--neon-gold); font-weight: bold;">${u.name}</span>
                <button class="btn-pixel ${isEquipped ? 'gold' : ''}" style="font-size: 0.65rem; padding: 2px 6px;" onclick="toggleEquipUnique(${uId})">
                    ${isEquipped ? '장착 중' : '장착'}
                </button>
            </div>
            <div style="font-size: 0.68rem; color: var(--neon-cyan);">${u.source}</div>
            <div style="font-size: 0.68rem; color: #d6c7b2; line-height: 1.3;">${u.effect}</div>
        `;

        container.appendChild(card);
    });
}

function toggleEquipUnique(uId) {
    if (!gameState.player.equippedUniques) gameState.player.equippedUniques = [];

    const idx = gameState.player.equippedUniques.indexOf(uId);
    if (idx >= 0) {
        gameState.player.equippedUniques.splice(idx, 1);
    } else {
        if (gameState.player.equippedUniques.length >= 3) {
            alert("고유 유물은 최대 3개까지만 동시 장착할 수 있습니다.");
            return;
        }
        gameState.player.equippedUniques.push(uId);
    }

    saveGameState(false);
    renderUniqueArtifactsList();
    refreshHubUI();
}

// -------------------------------------------------------------------------
// TAB: 비약 상점 (L9)
// -------------------------------------------------------------------------
function renderShop() {
    const hpCount = document.getElementById("shopHpPotionCount");
    const mpCount = document.getElementById("shopMpPotionCount");
    if (hpCount) hpCount.textContent = gameState.player.potions.hp;
    if (mpCount) mpCount.textContent = gameState.player.potions.mp;
}

function buyPotion(type) {
    const p = gameState.player;
    const price = type === "hp" ? 200 : 150;
    if (p.potions[type] >= 10) {
        alert("이 비약은 최대 10개까지만 소지할 수 있습니다.");
        return;
    }
    if (p.gold < price) {
        alert("마력석(골드)이 부족합니다!");
        return;
    }
    p.gold -= price;
    p.potions[type] += 1;
    renderShop();
    refreshHubUI();
    saveGameState(false);
}

// -------------------------------------------------------------------------
// TAB 5: 회귀 제단 & 영혼 각인 (L1, L2)
// -------------------------------------------------------------------------
function renderAltar() {
    const traitsList = document.getElementById("altarTraitsList");
    const talentsList = document.getElementById("altarTalentsList");
    const masterStatus = document.getElementById("altarMasterSoulStatus");

    if (traitsList) {
        traitsList.innerHTML = "";
        Object.entries(gameState.player.traits).forEach(([id, lv]) => {
            const t = TRAITS_DATA[id];
            if (!t) return;
            const mult = lvMul(lv);
            const val = (t.baseVal * mult).toFixed(1);

            const row = document.createElement("div");
            row.className = "btn-pixel";
            row.style.width = "100%";
            row.style.justifyContent = "space-between";
            row.style.fontSize = "0.75rem";
            row.innerHTML = `
                <span>${t.name} (Lv.${lv})</span>
                <span style="color: var(--neon-green);">${t.unit ? `+${val}${t.unit}` : `+${val}`}</span>
            `;
            traitsList.appendChild(row);
        });
    }

    if (talentsList) {
        talentsList.innerHTML = "";
        Object.entries(gameState.player.talents).forEach(([id, lv]) => {
            const t = TALENTS_DATA[id];
            if (!t) return;
            const mult = lvMul(lv);
            const val = (t.baseVal * mult).toFixed(1);

            const row = document.createElement("div");
            row.className = "btn-pixel";
            row.style.width = "100%";
            row.style.justifyContent = "space-between";
            row.style.fontSize = "0.75rem";
            row.innerHTML = `
                <span>${t.name} (Lv.${lv})</span>
                <span style="color: var(--neon-purple);">${t.unit ? `+${val}${t.unit}` : `+${val}`}</span>
            `;
            talentsList.appendChild(row);
        });
    }

    if (masterStatus) {
        if (gameState.player.masterSoulUnlocked) {
            masterStatus.innerHTML = `<strong style="color: var(--neon-gold);">🌟 영혼 각인 마스터 슬롯 개방됨!</strong>`;
        } else {
            masterStatus.textContent = "미해금 (어떤 특성이나 재능이든 최초 Lv.10 달성 시 개방)";
        }
    }
}

function openRegressionModal() {
    const modal = document.getElementById("modal-regression");
    if (!modal) return;

    const p = gameState.player;
    const traitSelect = document.getElementById("selectRegressionTrait");
    const talentSelect = document.getElementById("selectRegressionTalent");
    const relicRow = document.getElementById("inheritRelicRow");
    const relicSelect = document.getElementById("selectInheritRelic");

    // 슬롯 제한 체크 (0회차: 1칸, 1회차 이상: 2칸)
    const tSlots = 1 + (p.regressionCount >= 1 ? 1 : 0);
    const lSlots = 1 + (p.regressionCount >= 1 ? 1 : 0);

    const tFull = Object.keys(p.traits).length >= tSlots;
    const lFull = Object.keys(p.talents).length >= lSlots;

    if (traitSelect) {
        traitSelect.innerHTML = "";
        Object.entries(TRAITS_DATA).forEach(([id, t]) => {
            const curLv = p.traits[id] || 0;
            const isFullAndNew = tFull && curLv === 0;
            const isMax = curLv >= 10;
            const opt = document.createElement("option");
            opt.value = id;
            opt.disabled = isFullAndNew || isMax;
            opt.textContent = `${t.name} (Lv.${curLv} ➔ Lv.${Math.min(10, curLv + 1)})${isMax ? ' [만렙]' : isFullAndNew ? ' [슬롯가득]' : ''}`;
            traitSelect.appendChild(opt);
        });
    }

    if (talentSelect) {
        talentSelect.innerHTML = "";
        Object.entries(TALENTS_DATA).forEach(([id, t]) => {
            const curLv = p.talents[id] || 0;
            const isFullAndNew = lFull && curLv === 0;
            const isMax = curLv >= 10;
            const opt = document.createElement("option");
            opt.value = id;
            opt.disabled = isFullAndNew || isMax;
            opt.textContent = `${t.name} (Lv.${curLv} ➔ Lv.${Math.min(10, curLv + 1)})${isMax ? ' [만렙]' : isFullAndNew ? ' [슬롯가득]' : ''}`;
            talentSelect.appendChild(opt);
        });
    }

    // #36 회귀자의 회중시계 보유 시 계승 유물 선택
    if (relicRow && relicSelect) {
        if (p.uniqueInventory.includes(36)) {
            relicRow.style.display = "block";
            relicSelect.innerHTML = "";
            p.uniqueInventory.forEach(uId => {
                const u = getUnique(uId);
                if (!u) return;
                const opt = document.createElement("option");
                opt.value = uId;
                opt.textContent = u.name;
                relicSelect.appendChild(opt);
            });
        } else {
            relicRow.style.display = "none";
        }
    }

    modal.classList.add("active");
}

function closeRegressionModal() {
    const modal = document.getElementById("modal-regression");
    if (modal) modal.classList.remove("active");
}

function executeRegression() {
    const traitSelect = document.getElementById("selectRegressionTrait");
    const talentSelect = document.getElementById("selectRegressionTalent");
    const relicSelect = document.getElementById("selectInheritRelic");

    const traitId = traitSelect ? traitSelect.value : null;
    const talentId = talentSelect ? talentSelect.value : null;
    const keepRelicId = (relicSelect && gameState.player.uniqueInventory.includes(36)) ? parseInt(relicSelect.value, 10) : null;

    if (traitId) {
        const next = (gameState.player.traits[traitId] || 0) + 1;
        gameState.player.traits[traitId] = Math.min(10, next);
        if (gameState.player.traits[traitId] >= 10) gameState.player.masterSoulUnlocked = true;
    }

    if (talentId) {
        const next = (gameState.player.talents[talentId] || 0) + 1;
        gameState.player.talents[talentId] = Math.min(10, next);
        if (gameState.player.talents[talentId] >= 10) gameState.player.masterSoulUnlocked = true;
    }

    const regCount = gameState.player.regressionCount + 1;
    resetLife(gameState.player, keepRelicId);
    gameState.player.regressionCount = regCount;

    closeRegressionModal();
    saveGameState(false);
    refreshHubUI();

    alert(`💀 회귀가 완료되었습니다!
현재 회귀 차수: ${gameState.player.regressionCount}회차
새로운 생을 시작합니다.`);
}

function resetLife(p, keepUniqueId = null) {
    Object.assign(p, JSON.parse(JSON.stringify(BASE_STATS)));
    p.hp = p.maxHp;
    p.mp = p.maxMp;
    p.gold = 1500;
    p.potions = { hp: 5, mp: 5 };
    p.equippedGear = makeStarterGear(p.classId);
    p.uniqueInventory = keepUniqueId ? [keepUniqueId] : [];
    p.equippedUniques = keepUniqueId ? [keepUniqueId] : [];
    p.maxRegionUnlocked = 1;
}

function triggerDefeatRegression() {
    const defeatModal = document.getElementById("modal-defeat");
    if (defeatModal) defeatModal.classList.remove("active");
    switchScreen("screen-hub");
    openRegressionModal();
}

// =========================================================================
// 5. 실시간 횡스크롤 전투 엔진 (BATTLE ARENA)
// =========================================================================

function startGateBattle(regionId) {
    const reg = REGIONS_DATA[regionId];
    if (!reg) return;

    const s = getEffectiveStats();

    gameState.battle.active = true;
    gameState.battle.regionId = regionId;
    gameState.battle.wave = 1;
    gameState.battle.minions = [];
    gameState.battle.playerCooldowns = {};
    gameState.battle.playerShield = 0;
    gameState.battle.playerInvulnUntil = 0;
    gameState.battle.dodgeCharges = 0;
    gameState.battle.enemyStunUntil = 0;
    gameState.battle.enemyDebuffAtkUntil = 0;
    gameState.battle.playerBuffAtkUntil = 0;
    gameState.battle.reviveUsed = false;
    gameState.battle.playerAttackTimer = 0;
    gameState.battle.enemyAttackTimer = 0;
    gameState.battle.autoCastTimer = 0;
    gameState.battle.sessionDamage = 0;
    gameState.battle.sessionGold = 0;
    gameState.battle.sessionKills = 0;
    gameState.battle.sessionStartTime = performance.now();
    SoundEngine.startBgm('battle');

    gameState.player.hp = s.maxHp;
    gameState.player.mp = s.maxMp;

    // #7 아서의 해골 투구 보유 또는 네크로맨서 시작 시 아서 참전
    if (hasUnique(7)) {
        gameState.battle.minions.push({
            id: `minion_arthur_perm`,
            name: "듀라한 아서",
            atk: Math.floor(s.atk * 0.9),
            sprite: ASSET.summon("death_knight")
        });
    }

    switchScreen("screen-battle");
    setupBattleScene();
    spawnWaveMonster();
}

function setupBattleScene() {
    const reg = REGIONS_DATA[gameState.battle.regionId];
    const rId = gameState.battle.regionId;

    const viewport = document.getElementById("battleStageViewport");
    const propsLayer = document.getElementById("battlePropsLayer");

    if (viewport) {
        viewport.style.backgroundImage = `url('${ASSET.battlePano(rId)}')`;
        viewport.style.backgroundPosition = "0% center";
    }
    if (propsLayer) {
        propsLayer.style.backgroundImage = `url('${ASSET.propsPano(rId)}')`;
        propsLayer.style.backgroundPosition = "0% center";
    }

    const cls = CLASSES_DATA[gameState.player.classId] || CLASSES_DATA["necro"];
    const heroImg = document.getElementById("battleHeroActorImg");
    if (heroImg) heroImg.src = cls.sprite;

    const nameplate = document.getElementById("battleHeroNameplate");
    if (nameplate) nameplate.textContent = `${gameState.player.name} (Lv.${gameState.player.level})`;

    renderHeroMinions();
    renderBattleSkillButtons();
    updateBattleGauges();

    const titleEl = document.getElementById("battleRegionTitleText");
    if (titleEl) titleEl.textContent = `🚪 지역 ${rId}: ${reg.name}`;

    logBattleMessage(`▶ [지역 ${rId}: ${reg.name}] 차원문에 진입했습니다!`);
}

function applyWaveScroll(wave) {
    const pct = (wave - 1) * 20; // W1:0% -> W6:100%
    const viewport = document.getElementById("battleStageViewport");
    const propsLayer = document.getElementById("battlePropsLayer");
    if (viewport) viewport.style.backgroundPosition = `${pct}% center`;
    if (propsLayer) propsLayer.style.backgroundPosition = `${pct}% center`;
}

function renderHeroMinions() {
    const row = document.getElementById("heroMinionsRow");
    if (!row) return;
    row.innerHTML = "";

    gameState.battle.minions.forEach(m => {
        const img = document.createElement("img");
        img.className = "minion-unit";
        img.src = m.sprite;
        img.title = m.name;
        row.appendChild(img);
    });
}

// -------------------------------------------------------------------------
// 몬스터 스폰 (C7 비행 키 매핑)
// -------------------------------------------------------------------------
function spawnWaveMonster() {
    const reg = REGIONS_DATA[gameState.battle.regionId];
    const rId = gameState.battle.regionId;
    const waveNum = gameState.battle.wave;

    let spritePath = ASSET.monster(rId, waveNum);
    let monsterName = (reg.monsters && reg.monsters[waveNum - 1]) ? reg.monsters[waveNum - 1] : `지역 ${rId} 괴수 #${waveNum}`;
    let roleLabel = `WAVE ${waveNum}/6 · 일반 괴수`;
    let isBoss = waveNum === 6;

    if (waveNum === 5) {
        monsterName = reg.named || `지역 ${rId} 수문장`;
        roleLabel = `WAVE 5/6 · 수문장 네임드`;
    } else if (waveNum === 6) {
        monsterName = reg.boss || `지역 ${rId} 최종 보스`;
        roleLabel = `WAVE 6/6 · 지역 최종 보스`;
    }

    const s = getEffectiveStats();
    const baseEnemyHp = (800 + (rId * 450) + (waveNum * 350)) * s.enemyHpMul;
    const finalHp = Math.round(isBoss ? baseEnemyHp * 2.8 : (waveNum === 5 ? baseEnemyHp * 1.6 : baseEnemyHp));

    gameState.battle.enemy = {
        name: monsterName,
        role: roleLabel,
        sprite: spritePath,
        hp: finalHp,
        maxHp: finalHp,
        atk: 35 + (rId * 18) + (waveNum * 12),
        def: 20 + (rId * 10),
        isBoss: isBoss
    };

    // C7: FLYING_MONSTERS_MAP 키 = "지역_웨이브"
    const isFlying = !!FLYING_MONSTERS_MAP[`${rId}_${waveNum}`];

    const enemyBox = document.getElementById("enemyBattalionBox");
    if (enemyBox) enemyBox.style.bottom = isFlying ? "85px" : "16px";

    const enemySprite = document.getElementById("battleEnemySpriteImg");
    if (enemySprite) {
        enemySprite.src = spritePath;
        enemySprite.classList.toggle("floating-monster", isFlying);
    }

    const shadow = document.getElementById("battleEnemyShadow");
    if (shadow) shadow.style.opacity = isFlying ? "0.35" : "0.8";

    const roleNameEl = document.getElementById("battleEnemyRoleName");
    if (roleNameEl) {
        roleNameEl.textContent = `WAVE ${waveNum}/6 : ${monsterName}`;
        roleNameEl.style.color = isBoss ? "var(--neon-pink)" : (waveNum === 5 ? "var(--neon-gold)" : "var(--neon-cyan)");
    }

    const waveBadge = document.getElementById("battleWaveProgressBadge");
    if (waveBadge) {
        waveBadge.textContent = isBoss ? "⚠️ BOSS WAVE (최종 보스)" : roleLabel;
        waveBadge.style.borderColor = isBoss ? "var(--neon-pink)" : "var(--border-ink)";
    }

    updateEnemyHpBar();
    logBattleMessage(`⚔️ [Wave ${waveNum}] ${monsterName}이(가) 나타났습니다!`);
}

function renderBattleSkillButtons() {
    const row = document.getElementById("battleSkillsSlotsRow");
    if (!row) return;
    row.innerHTML = "";

    const p = gameState.player;
    const hotkeys = ["Q", "W", "E", "R", "SPACE"];

    p.equippedSkills.forEach((skillId, idx) => {
        const skill = findSkillById(skillId);
        if (!skill) return;

        const btn = document.createElement("div");
        btn.className = `skill-slot-btn ${idx === 4 ? 'ult-slot' : ''}`;
        btn.id = `skillSlotBtn_${idx}`;
        btn.onclick = () => useSkillSlot(idx);

        btn.innerHTML = `
            <span class="skill-hotkey-badge">${hotkeys[idx]}</span>
            <img src="${skill.vfx}" class="skill-slot-icon">
            <div class="skill-cooldown-overlay" id="skillCdOverlay_${idx}"></div>
            <div style="font-size: 0.58rem; color: var(--neon-gold); margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 58px;">
                ${skill.name.split(' ')[0]}
            </div>
        `;
        row.appendChild(btn);
    });
}

function updateBattleGauges() {
    const p = gameState.player;
    const s = getEffectiveStats();

    const hpInner = document.getElementById("battlePlayerHpBar");
    const hpText = document.getElementById("battlePlayerHpText");
    const mpInner = document.getElementById("battlePlayerMpBar");
    const mpText = document.getElementById("battlePlayerMpText");

    const shieldText = gameState.battle.playerShield > 0 ? ` (+${Math.floor(gameState.battle.playerShield)})` : '';
    if (hpInner) hpInner.style.width = `${Math.max(0, Math.min(100, (p.hp / s.maxHp) * 100))}%`;
    if (hpText) hpText.textContent = `${Math.floor(p.hp)}${shieldText} / ${s.maxHp}`;

    if (mpInner) mpInner.style.width = `${Math.max(0, Math.min(100, (p.mp / s.maxMp) * 100))}%`;
    if (mpText) mpText.textContent = `${Math.floor(p.mp)} / ${s.maxMp}`;

    const hpCount = document.getElementById("potionHpCount");
    const mpCount = document.getElementById("potionMpCount");
    if (hpCount) hpCount.textContent = `x${p.potions.hp}`;
    if (mpCount) mpCount.textContent = `x${p.potions.mp}`;
}

function updateEnemyHpBar() {
    const e = gameState.battle.enemy;
    if (!e) return;

    const hpBar = document.getElementById("battleEnemyHpBarInner");
    const hpText = document.getElementById("battleEnemyHpText");

    const pct = Math.max(0, Math.min(100, (e.hp / e.maxHp) * 100));
    if (hpBar) hpBar.style.width = `${pct}%`;
    if (hpText) hpText.textContent = `HP: ${Math.floor(e.hp)} (${pct.toFixed(0)}%)`;
}

// -------------------------------------------------------------------------
// 스킬 시전 & 자동 전투 (C3, C4 버그 해결)
// -------------------------------------------------------------------------
function getSkillCost(slotIdx) {
    const base = slotIdx === 4 ? 120 : 35;
    return Math.round(base * getEffectiveStats().mpCostMul);
}

function canCast(slotIdx) {
    const sId = gameState.player.equippedSkills[slotIdx];
    if (!sId) return false;
    const cd = gameState.battle.playerCooldowns[sId] || 0;
    return cd <= 0 && gameState.player.mp >= getSkillCost(slotIdx);
}

function useSkillSlot(slotIdx) {
    if (!gameState.battle.active || !gameState.battle.enemy) return;

    const skillId = gameState.player.equippedSkills[slotIdx];
    const skill = findSkillById(skillId);
    if (!skill) return;

    const cd = gameState.battle.playerCooldowns[skillId] || 0;
    if (cd > 0) return;

    const cost = getSkillCost(slotIdx);
    if (gameState.player.mp < cost) {
        const now = performance.now();
        if (now - gameState.battle.lastNoMpWarn > 1000) {
            gameState.battle.lastNoMpWarn = now;
            showFloatingText(document.getElementById("battleHeroActorImg"), "마나 부족!", "var(--neon-cyan)");
        }
        return;
    }

    gameState.player.mp -= cost;

    const s = getEffectiveStats();
    let baseCd = (slotIdx === 4 ? 22 : 4.5) * s.cdMul;
    if (slotIdx === 4 && hasUnique(12)) baseCd *= 0.55; // #12 고룡의 역린
    gameState.battle.playerCooldowns[skillId] = baseCd;

    executeSkillLogic(skill, slotIdx === 4);
    updateBattleGauges();
}

// -------------------------------------------------------------------------
// 스킬 3단계 시퀀스 & kind별 분기 (L5, R2)
// -------------------------------------------------------------------------
async function executeSkillLogic(skill, isUlt) {
    const e = gameState.battle.enemy;
    if (!e) return;

    const s = getEffectiveStats();
    const heroActor = document.getElementById("battleHeroActorImg");
    const enemyActor = document.getElementById("battleEnemySpriteImg");

    // 3단계 시퀀스: ① 마법진 회전 -> ② 투사체 -> ③ 폭발
    playSkillSequence(skill, isUlt);

    // 0.4초 후 타격 시점
    setTimeout(() => {
        if (!gameState.battle.active || !gameState.battle.enemy) return;

        let baseDmg = s.atk * (isUlt ? 6.5 : 2.4) * s.skillMul;
        if (e.isBoss) baseDmg *= s.bossMul;
        if (hasUnique(24)) baseDmg *= (0.5 + Math.random() * 2.5); // #24 마카오 주사위

        const isCrit = Math.random() < s.critRate;
        if (isCrit) {
            baseDmg *= s.critDmg;
            if (hasUnique(2) && Math.random() < 0.15) {
                gameState.battle.playerCooldowns = {};
                showFloatingText(heroActor, "쿨타임 즉시 초기화!", "var(--neon-gold)");
            }
        }

        let dealtDmg = Math.max(10, Math.floor(baseDmg - (e.def * 0.35)));

        // kind별 특수 효과 분기
        switch (skill.kind) {
            case "summon":
                spawnSkillMinions(skill);
                break;
            case "corpse_burst":
                if (gameState.battle.minions.length > 0) {
                    gameState.battle.minions.pop();
                    renderHeroMinions();
                    dealtDmg = Math.floor(dealtDmg * 2.5);
                    triggerCorpseExplosionVfx();
                }
                break;
            case "shield":
                gameState.battle.playerShield += Math.floor(s.maxHp * 0.35);
                showFloatingText(heroActor, `🛡️ 보호막 +${Math.floor(s.maxHp * 0.35)}`, "var(--neon-cyan)");
                break;
            case "heal":
                const healAmt = Math.floor(s.maxHp * 0.35 * s.healMul);
                const overheal = Math.max(0, (gameState.player.hp + healAmt) - s.maxHp);
                gameState.player.hp = Math.min(s.maxHp, gameState.player.hp + healAmt);
                showFloatingText(heroActor, `+${healAmt} HP`, "var(--neon-green)");
                if (overheal > 0) {
                    const holyStrike = Math.floor(overheal * 2.5);
                    e.hp -= holyStrike;
                    showFloatingText(enemyActor, `⚡ 심판 ${holyStrike}`, "var(--neon-gold)");
                }
                break;
            case "cc":
                gameState.battle.enemyStunUntil = performance.now() + 2500;
                showFloatingText(enemyActor, "💫 기절 2.5초!", "var(--neon-cyan)");
                break;
            case "debuff":
                gameState.battle.enemyDebuffAtkUntil = performance.now() + 8000;
                showFloatingText(enemyActor, "공격력 -40% 약화!", "var(--neon-purple)");
                break;
            case "buff":
                gameState.battle.playerBuffAtkUntil = performance.now() + 10000;
                showFloatingText(heroActor, "공격력 +30% 증폭!", "var(--neon-gold)");
                break;
            case "invulnerable":
                gameState.battle.playerInvulnUntil = performance.now() + 5000; // 5초 무적
                showFloatingText(heroActor, "🌟 5초간 절대 무적!", "var(--neon-gold)");
                break;
            case "parry":
            case "blink_shield":
            case "stealth":
                gameState.battle.dodgeCharges += 1;
                showFloatingText(heroActor, "1회 회피/패링 충전!", "var(--neon-cyan)");
                break;
            default:
                break;
        }

        e.hp -= dealtDmg;
        gameState.battle.sessionDamage += dealtDmg;
        if (isCrit) SoundEngine.crit(); else SoundEngine.hit();
        triggerScreenShake(isUlt);
        showFloatingText(enemyActor, `${isCrit ? 'CRIT! ' : ''}${dealtDmg.toLocaleString()}`, isCrit ? "var(--neon-pink)" : "var(--neon-gold)");
        updateEnemyHpBar();
        logBattleMessage(`⚡ [${skill.name}] 적중! ${dealtDmg.toLocaleString()} 피해!`);

        if (e.hp <= 0) onEnemyDefeated();
    }, 400);
}

function playSkillSequence(skill, isUlt) {
    SoundEngine.skill();
    const overlay = document.getElementById("battleVfxOverlay");
    if (!overlay) return;

    // 1. 마법진
    const circle = document.createElement("img");
    circle.src = skill.vfx;
    circle.style.position = "absolute";
    circle.style.left = "80px";
    circle.style.bottom = "20px";
    circle.style.width = "100px";
    circle.style.height = "100px";
    circle.style.objectFit = "contain";
    circle.style.animation = "spinIn 0.35s forwards";
    overlay.appendChild(circle);

    // 2. 투사체 / 궤적
    setTimeout(() => {
        circle.remove();
        const projectile = document.createElement("img");
        projectile.src = skill.vfx;
        projectile.style.position = "absolute";
        projectile.style.left = "160px";
        projectile.style.bottom = "45px";
        projectile.style.width = "70px";
        projectile.style.height = "70px";
        projectile.style.objectFit = "contain";
        projectile.style.transition = "transform 0.28s ease-in, opacity 0.28s";
        projectile.style.transform = "translateX(0)";
        overlay.appendChild(projectile);

        requestAnimationFrame(() => {
            projectile.style.transform = "translateX(360px) scale(1.3)";
        });

        // 3. 적 피격 폭발
        setTimeout(() => {
            projectile.remove();
            const burst = document.createElement("img");
            burst.src = skill.vfx;
            burst.style.position = "absolute";
            burst.style.right = "85px";
            burst.style.bottom = "35px";
            burst.style.width = isUlt ? "200px" : "140px";
            burst.style.height = isUlt ? "200px" : "140px";
            burst.style.objectFit = "contain";
            burst.style.animation = "burstAnim 0.4s forwards";
            overlay.appendChild(burst);
            setTimeout(() => burst.remove(), 400);
        }, 280);
    }, 180);
}

function spawnSkillMinions(skill) {
    const list = SKILL_SUMMONS[skill.id] || ['skeleton_warrior'];
    const maxM = 6 + (hasUnique(21) ? 3 : 0);

    list.forEach(key => {
        const def = SUMMON_DEFS[key];
        if (!def) return;
        if (key === 'arthur' && gameState.battle.minions.some(m => m.key === 'arthur')) return; // 아서는 중복 방지

        gameState.battle.minions.push({
            id: `minion_${Date.now()}_${Math.random()}`,
            key: key,
            name: def.name,
            atkMul: def.atkMul,
            sprite: def.sprite
        });
    });

    while (gameState.battle.minions.length > maxM) {
        gameState.battle.minions.shift();
    }
    renderHeroMinions();
}

function triggerCorpseExplosionVfx() {
    const overlay = document.getElementById("battleVfxOverlay");
    if (!overlay) return;

    const burst = document.createElement("div");
    burst.style.position = "absolute";
    burst.style.right = "80px";
    burst.style.bottom = "40px";
    burst.style.width = "180px";
    burst.style.height = "180px";
    burst.style.background = "radial-gradient(circle, rgba(255,0,85,0.85) 0%, rgba(0,0,0,0) 70%)";
    burst.style.borderRadius = "50%";
    burst.style.pointerEvents = "none";
    burst.style.animation = "minionExplode 0.5s forwards";

    overlay.appendChild(burst);
    setTimeout(() => burst.remove(), 500);
}

// -------------------------------------------------------------------------
// 일반 평타 & 적 클릭 핸들러 (L8 악용 방지)
// -------------------------------------------------------------------------
function onEnemyClick() {
    if (!gameState.battle.active || !gameState.battle.enemy) return;
    const s = getEffectiveStats();
    const interval = 1.0 / s.atkSpeed;

    // 평타 주기의 50% 이상 충전되었을 때만 앞당김 허용
    if (gameState.battle.playerAttackTimer >= interval * 0.5) {
        gameState.battle.playerAttackTimer = 0;
        playerBasicAttack();
    }
}

function playerBasicAttack() {
    const e = gameState.battle.enemy;
    if (!e || e.hp <= 0) return;

    const s = getEffectiveStats();
    let dmg = Math.floor(s.atk * (0.9 + Math.random() * 0.2));
    if (gameState.battle.playerBuffAtkUntil > performance.now()) dmg = Math.floor(dmg * 1.3);

    const isCrit = Math.random() < s.critRate;
    if (isCrit) dmg = Math.floor(dmg * s.critDmg);

    dmg = Math.max(5, dmg - Math.floor(e.def * 0.3));
    e.hp -= dmg;

    const enemySprite = document.getElementById("battleEnemySpriteImg");
    showFloatingText(enemySprite, `${isCrit ? 'CRIT! ' : ''}${dmg}`, isCrit ? "var(--neon-pink)" : "#fff");

    // 미니언 합동 공격 & 타격 모션
    if (gameState.battle.minions.length > 0) {
        let minionTotal = 0;
        document.querySelectorAll(".minion-unit").forEach(el => {
            el.style.animation = "minionStrike 0.35s ease";
            setTimeout(() => el.style.animation = "minionBob 1.6s ease-in-out infinite alternate", 350);
        });
        gameState.battle.minions.forEach(m => {
            minionTotal += Math.floor(s.atk * (m.atkMul || 0.25) * s.minionMul);
        });
        e.hp -= minionTotal;
        showFloatingText(enemySprite, `💀 +${minionTotal}`, "var(--neon-green)");
    }

    updateEnemyHpBar();
    if (e.hp <= 0) onEnemyDefeated();
}

// -------------------------------------------------------------------------
// 메인 게임 루프 (Game Loop)
// -------------------------------------------------------------------------
function gameLoop(timestamp) {
    if (!gameState.battle.lastTick) gameState.battle.lastTick = timestamp;
    const delta = (timestamp - gameState.battle.lastTick) / 1000;
    gameState.battle.lastTick = timestamp;

    if (gameState.battle.active && gameState.battle.enemy) {
        const spd = gameState.battle.speed;
        const s = getEffectiveStats();

        // 쿨타임 감소
        Object.keys(gameState.battle.playerCooldowns).forEach(k => {
            if (gameState.battle.playerCooldowns[k] > 0) {
                gameState.battle.playerCooldowns[k] -= delta * spd;
                if (gameState.battle.playerCooldowns[k] < 0) gameState.battle.playerCooldowns[k] = 0;
            }
        });
        updateCooldownOverlays();

        // 마나 자연 회복
        if (gameState.player.mp < s.maxMp) {
            gameState.player.mp += (s.mpRegen * delta * spd);
            if (gameState.player.mp > s.maxMp) gameState.player.mp = s.maxMp;
            updateBattleGauges();
        }

        // 플레이어 자동 공격
        gameState.battle.playerAttackTimer += delta * spd;
        if (gameState.battle.playerAttackTimer >= (1.0 / s.atkSpeed)) {
            gameState.battle.playerAttackTimer = 0;
            playerBasicAttack();
        }

        // 자동 전투 스킬 시전 (0.35초 간격)
        if (gameState.battle.auto) {
            gameState.battle.autoCastTimer += delta * spd;
            if (gameState.battle.autoCastTimer >= 0.35) {
                gameState.battle.autoCastTimer = 0;
                const order = [4, 0, 1, 2, 3]; // 궁극기 우선
                const readyIdx = order.find(canCast);
                if (readyIdx !== undefined) useSkillSlot(readyIdx);
            }
        }

        // 적 몬스터 공격
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

    requestAnimationFrame(gameLoop);
}

function updateCooldownOverlays() {
    for (let i = 0; i < 5; i++) {
        const sId = gameState.player.equippedSkills[i];
        const overlay = document.getElementById(`skillCdOverlay_${i}`);
        if (!overlay) continue;

        const cd = gameState.battle.playerCooldowns[sId] || 0;
        if (cd > 0) {
            overlay.style.display = "flex";
            overlay.textContent = cd.toFixed(1);
        } else {
            overlay.style.display = "none";
        }
    }
}

function executeEnemyAttack() {
    const e = gameState.battle.enemy;
    if (!e || e.hp <= 0) return;

    const now = performance.now();
    if (now < gameState.battle.enemyStunUntil) return; // 기절 중

    const heroImg = document.getElementById("battleHeroActorImg");

    // 절대 무적
    if (now < gameState.battle.playerInvulnUntil) {
        showFloatingText(heroImg, "INVULNERABLE!", "var(--neon-gold)");
        return;
    }

    // 회피/패링 충전
    if (gameState.battle.dodgeCharges > 0) {
        gameState.battle.dodgeCharges -= 1;
        showFloatingText(heroImg, "PARRIED!", "var(--neon-cyan)");
        return;
    }

    const s = getEffectiveStats();
    let dmg = Math.floor(e.atk * (0.85 + Math.random() * 0.3));
    if (now < gameState.battle.enemyDebuffAtkUntil) dmg = Math.floor(dmg * 0.6);
    dmg = Math.max(5, dmg - Math.floor(s.def * 0.35));

    // 유물 #16 원콤 방지: 최대 체력의 25% 초과 불가
    if (hasUnique(16)) {
        dmg = Math.min(dmg, Math.floor(s.maxHp * 0.25));
    }

    // 보호막 우선 흡수
    if (gameState.battle.playerShield > 0) {
        if (gameState.battle.playerShield >= dmg) {
            gameState.battle.playerShield -= dmg;
            showFloatingText(heroImg, `🛡️ -${dmg}`, "var(--neon-cyan)");
            dmg = 0;
        } else {
            dmg -= gameState.battle.playerShield;
            gameState.battle.playerShield = 0;
        }
    }

    if (dmg > 0) {
        gameState.player.hp -= dmg;
        triggerScreenShake(false);
        showFloatingText(heroImg, `-${dmg}`, "var(--neon-pink)");
    }

    // 가시 반사
    if (s.reflect > 0 && dmg > 0) {
        const refDmg = Math.floor(dmg * s.reflect);
        e.hp -= refDmg;
        showFloatingText(document.getElementById("battleEnemySpriteImg"), `🦔 ${refDmg}`, "var(--neon-pink)");
        updateEnemyHpBar();
    }

    updateBattleGauges();
    logBattleMessage(`💥 ${e.name}의 강타! 영웅이 ${dmg} 피해를 입었습니다.`);

    if (gameState.player.hp <= 0) onPlayerDefeated();
}

// -------------------------------------------------------------------------
// 승리 & 패배 & 레벨업 (L7)
// -------------------------------------------------------------------------
function gainExp(amount) {
    const p = gameState.player;
    const s = getEffectiveStats();
    p.exp += Math.round(amount * s.expMul);

    while (p.exp >= p.maxExp) {
        p.exp -= p.maxExp;
        p.level += 1;
        p.maxExp = Math.floor(p.maxExp * 1.4);
        p.maxHp += 150;
        p.maxMp += 50;
        p.baseAtk += 20;
        p.baseDef += 15;
        showFloatingText(document.getElementById("battleHeroActorImg"), "LEVEL UP!", "var(--neon-green)");
        logBattleMessage(`✨ LEVEL UP! 영웅이 Lv.${p.level}로 성장했습니다!`);
    }
}

function onEnemyDefeated() {
    const e = gameState.battle.enemy;
    gameState.battle.enemy = null;

    logBattleMessage(`🏆 ${e.name} 처치 완료!`);

    const s = getEffectiveStats();
    const earnedGold = Math.round(120 * gameState.battle.wave * gameState.battle.regionId * s.goldMul);
    const earnedExp = 80 * gameState.battle.wave;

    gameState.player.gold += earnedGold;
    gameState.battle.sessionGold = (gameState.battle.sessionGold || 0) + earnedGold;
    gameState.battle.sessionKills = (gameState.battle.sessionKills || 0) + 1;
    gainExp(earnedExp);

    // 포식자의 본능 (처치 시 회복)
    if (s.killHeal > 0) {
        gameState.player.hp = Math.min(s.maxHp, gameState.player.hp + s.maxHp * s.killHeal);
        gameState.player.mp = Math.min(s.maxMp, gameState.player.mp + s.maxMp * s.killHeal);
    }

    if (gameState.battle.wave < 6) {
        gameState.battle.wave += 1;

        // R1: 순방향 파노라마 스크롤 (0 -> 100%) & 영웅 달리기 연출
        const heroBox = document.getElementById("heroBattalionBox");
        if (heroBox) heroBox.classList.add("hero-running");
        applyWaveScroll(gameState.battle.wave);

        setTimeout(() => {
            if (heroBox) heroBox.classList.remove("hero-running");
            if (gameState.battle.active) spawnWaveMonster();
        }, 850);
    } else {
        onRegionVictory();
    }
}

function onRegionVictory() {
    gameState.battle.active = false;
    SoundEngine.levelUp();
    const rId = gameState.battle.regionId;

    if (rId >= gameState.player.maxRegionUnlocked && gameState.player.maxRegionUnlocked < 14) {
        gameState.player.maxRegionUnlocked = rId + 1;
    }

    const s = getEffectiveStats();
    const goldReward = Math.round(2500 * rId * s.goldMul);
    const expReward = 1500 * rId;

    gameState.player.gold += goldReward;
    gameState.battle.sessionGold = (gameState.battle.sessionGold || 0) + goldReward;
    gainExp(expReward);

    saveGameState(false);

    if (gameState.battle.autoNextRegion && rId < 14) {
        showFloatingText(document.body, `🏆 [지역 ${rId}] 정복 완료! 1.5초 후 다음 차원문으로 진격합니다...`, "var(--neon-gold)");
        setTimeout(() => {
            if (gameState.battle.autoNextRegion) {
                startGateBattle(rId + 1);
            }
        }, 1500);
        return;
    }

    const modal = document.getElementById("modal-victory");
    if (modal) modal.classList.add("active");

    const regNameEl = document.getElementById("victoryRegionName");
    if (regNameEl) regNameEl.textContent = `지역 ${rId}: ${REGIONS_DATA[rId].name} 완전 클리어!`;

    const goldEl = document.getElementById("lootGoldText");
    const expEl = document.getElementById("lootExpText");
    if (goldEl) goldEl.textContent = `+${goldReward.toLocaleString()} 마력석`;
    if (expEl) expEl.textContent = `+${expReward.toLocaleString()} EXP`;

    // 전리품 렌더링
    const lootGrid = document.getElementById("lootItemsGrid");
    if (lootGrid) {
        lootGrid.innerHTML = "";

        // 무작위 고유 아이템 드랍
        const unowned = UNIQUE_ITEMS_DATA.map(u => u.id).filter(id => !gameState.player.uniqueInventory.includes(id));
        if (unowned.length > 0) {
            const dropId = unowned[Math.floor(Math.random() * unowned.length)];
            gameState.player.uniqueInventory.push(dropId);
            const u = getUnique(dropId);
            const card = document.createElement("div");
            card.className = "loot-item-card";
            card.innerHTML = `
                <div style="font-size: 1.4rem;">💎</div>
                <div style="font-size: 0.65rem; color: var(--neon-gold);">${u.name}</div>
            `;
            lootGrid.appendChild(card);
        }

        // 세트 장비 드랍 (미보유 부위)
        const cls = CLASSES_DATA[gameState.player.classId] || CLASSES_DATA["necro"];
        const parts = ["ring", "armor", "helmet", "core"];
        const missingParts = parts.filter(pk => !gameState.player.equippedGear[pk]);
        if (missingParts.length > 0) {
            const dropPartKey = missingParts[0];
            const pIdx = parts.indexOf(dropPartKey);
            const setPartDef = cls.setParts ? cls.setParts[pIdx === 0 ? 0 : pIdx + 1] : null;
            if (setPartDef) {
                gameState.player.equippedGear[dropPartKey] = {
                    id: `set_${cls.id}_${dropPartKey}`,
                    name: setPartDef.name,
                    part: dropPartKey,
                    enhance: 0,
                    stat: 40 + rId * 5
                };
                const gCard = document.createElement("div");
                gCard.className = "loot-item-card";
                gCard.innerHTML = `
                    <div style="font-size: 1.4rem;">🥋</div>
                    <div style="font-size: 0.65rem; color: var(--neon-green);">${setPartDef.name}</div>
                `;
                lootGrid.appendChild(gCard);
            }
        }

        // 스킬 비급서 드랍
        const allSkillIds = [];
        Object.values(CLASSES_DATA).forEach(c => c.skills.forEach(sk => allSkillIds.push(sk.id)));
        const unlearned = allSkillIds.filter(id => !gameState.player.unlockedSkills.includes(id));
        if (unlearned.length > 0) {
            const newSkillId = unlearned[Math.floor(Math.random() * unlearned.length)];
            gameState.player.unlockedSkills.push(newSkillId);
            const newSkill = findSkillById(newSkillId);
            const sCard = document.createElement("div");
            sCard.className = "loot-item-card";
            sCard.innerHTML = `
                <div style="font-size: 1.4rem;">📜</div>
                <div style="font-size: 0.65rem; color: var(--neon-cyan);">${newSkill.name} 비급서</div>
            `;
            lootGrid.appendChild(sCard);
        }
    }

    saveGameState(false);
}

function closeVictoryModal(advanceNext = false) {
    const modal = document.getElementById("modal-victory");
    if (modal) modal.classList.remove("active");

    if (advanceNext && gameState.battle.regionId < 14) {
        startGateBattle(gameState.battle.regionId + 1);
    } else {
        switchScreen("screen-hub");
        refreshHubUI();
    }
}

function onPlayerDefeated() {
    gameState.battle.active = false;

    // #27 라시드의 모래시계 1회 부활
    if (hasUnique(27) && !gameState.battle.reviveUsed) {
        gameState.battle.reviveUsed = true;
        const s = getEffectiveStats();
        gameState.player.hp = Math.floor(s.maxHp * 0.6);
        gameState.battle.active = true;
        showFloatingText(document.getElementById("battleHeroActorImg"), "시간 회귀 부활!", "var(--neon-gold)");
        logBattleMessage("⏳ [라시드의 모래시계] 시간이 되돌려져 부활했습니다!");
        return;
    }

    const modal = document.getElementById("modal-defeat");
    if (modal) modal.classList.add("active");
}

function retreatToVillage() {
    if (confirm("전투를 중단하고 거점 마을로 후퇴하시겠습니까?")) {
        gameState.battle.active = false;
        switchScreen("screen-hub");
        refreshHubUI();
    }
}

function usePotion(type) {
    const s = getEffectiveStats();
    if (type === "hp" && gameState.player.potions.hp > 0) {
        gameState.player.potions.hp--;
        gameState.player.hp = Math.min(s.maxHp, gameState.player.hp + 600);
        showFloatingText(document.getElementById("battleHeroActorImg"), "+600 HP", "var(--neon-green)");
    } else if (type === "mp" && gameState.player.potions.mp > 0) {
        gameState.player.potions.mp--;
        gameState.player.mp = Math.min(s.maxMp, gameState.player.mp + 400);
        showFloatingText(document.getElementById("battleHeroActorImg"), "+400 MP", "var(--neon-cyan)");
    }
    updateBattleGauges();
}

function toggleBattleSpeed() {
    const speeds = [1, 2, 4, 8];
    const curIdx = speeds.indexOf(gameState.battle.speed);
    gameState.battle.speed = speeds[(curIdx + 1) % speeds.length];

    const btn = document.getElementById("btnBattleSpeed");
    if (btn) {
        btn.textContent = gameState.battle.speed === 8 ? "⚡ 8x (초고속)" : `⚡ 배속: ${gameState.battle.speed}x`;
        btn.style.color = gameState.battle.speed >= 4 ? "var(--neon-pink)" : "var(--neon-gold)";
    }
    SoundEngine.click();
}

function toggleAutoBattle() {
    gameState.battle.auto = !gameState.battle.auto;
    const btn = document.getElementById("btnAutoBattle");
    if (btn) {
        btn.textContent = `🤖 자동 전투: ${gameState.battle.auto ? 'ON' : 'OFF'}`;
        btn.style.color = gameState.battle.auto ? "var(--neon-green)" : "var(--text-muted)";
    }
}

// -------------------------------------------------------------------------
// 연출 헬퍼 함수
// -------------------------------------------------------------------------
function showFloatingText(targetEl, text, color) {
    if (!targetEl) return;
    const floater = document.createElement("div");
    floater.className = "damage-floater";
    floater.textContent = text;
    floater.style.color = color || "var(--neon-gold)";

    const rect = targetEl.getBoundingClientRect();
    floater.style.left = `${rect.left + rect.width / 2 - 20}px`;
    floater.style.top = `${rect.top - 10}px`;

    document.body.appendChild(floater);
    setTimeout(() => floater.remove(), 850);
}

function triggerScreenShake(isStrong = false) {
    const viewport = document.getElementById("battleStageViewport");
    if (!viewport) return;
    const cls = isStrong ? "screen-shake-strong" : "screen-shake";
    viewport.classList.add(cls);
    setTimeout(() => viewport.classList.remove(cls), isStrong ? 450 : 320);
}

function logBattleMessage(msg) {
    const ticker = document.getElementById("battleLogTicker");
    if (!ticker) return;

    const line = document.createElement("div");
    line.className = "battle-log-line";
    line.textContent = msg;

    ticker.appendChild(line);
    if (ticker.children.length > 5) ticker.removeChild(ticker.children[0]);
    ticker.scrollTop = ticker.scrollHeight;
}
