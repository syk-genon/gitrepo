// PROJECT 2100 - Integrated Arcade Showcase & Simulator Controller (display.js)
// Works directly via file:/// protocol without CORS or backend dependencies.

(function () {
  'use strict';

  // --- 1. Global State ---
  const state = {
    gender: 'male',
    motion: 'idle',
    frame: 0,
    fps: 8,
    speed: 1.0,
    isPlaying: true,
    weapon: 'katana',
    armor: 'military',
    unlockedSlots: [true, true, true], // Start with all 3 toggleable (slot 0 base, 1&2 unlocked for easy demonstration)
    equippedTraits: ['body_mutation', 'radiation_assimilation', null],
    manualPartsMode: false,
    manualParts: {},
    manualAura: 'auto', // 'auto', '0', '1', '2'
    selectedMonsterRegion: 1,
    selectedMonster: null,
    fusionCategory: 'all',
    fusionSearchText: ''
  };

  let animTimer = null;

  const MAX_FRAMES = {
    idle: 4,
    run: 6,
    attack: 4,
    skill: 4
  };

  // Trait color mapping for all 13 actual traits in TRAITS_DATA
  const TRAIT_COLORS = {
    body_mutation: '#ff2a6d',
    energy_discharge: '#00f0ff',
    sensory_tech: '#38bdf8',
    blood_absorption: '#f43f5e',
    cellular_shield: '#10b981',
    fairy_magic: '#f472b6',
    power_overload: '#f59e0b',
    thermal_control: '#fb923c',
    ultrasonic_disruption: '#a855f7',
    berserker_madness: '#ef4444',
    radiation_assimilation: '#84cc16',
    meltdown_control: '#eab308',
    hightech_engineering: '#06b6d4'
  };

  // Categorization tags for 78 fusions
  function getFusionCategory(fId, fData) {
    const desc = fData.description || '';
    const name = fData.name || '';
    if (desc.includes('방어') || desc.includes('보호막') || desc.includes('경감') || desc.includes('피해 흡수') || desc.includes('차폐')) {
      return 'def';
    }
    if (desc.includes('연타') || desc.includes('가속') || desc.includes('기절') || desc.includes('속도') || desc.includes('쿨타임')) {
      return 'hit';
    }
    if (desc.includes('요정') || desc.includes('스킬') || desc.includes('도트') || desc.includes('마법') || desc.includes('정령') || desc.includes('시전')) {
      return 'skill';
    }
    if (desc.includes('방사능') || desc.includes('반사') || desc.includes('부활') || desc.includes('오염') || desc.includes('Rad') || desc.includes('멜트다운')) {
      return 'rad';
    }
    return 'atk';
  }

  // --- 2. Initialization ---
  window.addEventListener('DOMContentLoaded', () => {
    initHeroStudio();
    initSlotsAndPalette();
    initFusionsMatrix();
    initMonsterGallery();
    startAnimationLoop();
    updateAll();
  });

  // --- 3. Animation Loop ---
  function startAnimationLoop() {
    if (animTimer) clearInterval(animTimer);
    const intervalMs = Math.max(30, Math.round(1000 / (state.fps * state.speed)));
    animTimer = setInterval(() => {
      if (state.isPlaying) {
        state.frame = (state.frame + 1) % MAX_FRAMES[state.motion];
        renderAvatarFrame();
        updateFrameIndicator();
      }
    }, intervalMs);
  }

  function updateFrameIndicator() {
    const textEl = document.getElementById('playbackSpeedText');
    const badgeEl = document.getElementById('stageStatusBadge');
    if (textEl) {
      textEl.textContent = `프레임: ${state.frame + 1}/${MAX_FRAMES[state.motion]} | 속도: ${state.speed.toFixed(1)}x`;
    }
    if (badgeEl) {
      const gMap = {
        male: '남성 요원',
        female: '여성 요원',
        male_nemesis: '각성 네메시스(남)',
        female_nemesis: '각성 네메시스(여)'
      };
      const gName = gMap[state.gender] || '남성 요원';
      const mName = { idle: '대기', run: '달리기', attack: '공격 돌진', skill: '필살 스킬' }[state.motion];
      badgeEl.textContent = `DNF 아케이드 라이브: ${gName} [${mName} 모션 F${state.frame}]`;
    }
  }

  // --- 4. Hero Studio Controller ---
  function initHeroStudio() {
    // Gender buttons
    document.querySelectorAll('[data-gender]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('[data-gender]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.gender = btn.getAttribute('data-gender');
        renderAvatarFrame();
        updateFrameIndicator();
      });
    });

    // Motion buttons
    document.querySelectorAll('[data-motion]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('[data-motion]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.motion = btn.getAttribute('data-motion');
        state.frame = 0;
        renderAvatarFrame();
        updateFrameIndicator();
      });
    });

    // Playback control
    const btnPlayPause = document.getElementById('btnPlayPause');
    if (btnPlayPause) {
      btnPlayPause.addEventListener('click', () => {
        state.isPlaying = !state.isPlaying;
        btnPlayPause.textContent = state.isPlaying ? '⏸ 일시정지' : '▶ 재생';
        btnPlayPause.style.color = state.isPlaying ? '#f1f5f9' : '#00f0ff';
      });
    }

    const btnStepFrame = document.getElementById('btnStepFrame');
    if (btnStepFrame) {
      btnStepFrame.addEventListener('click', () => {
        state.isPlaying = false;
        if (btnPlayPause) btnPlayPause.textContent = '▶ 재생';
        state.frame = (state.frame + 1) % MAX_FRAMES[state.motion];
        renderAvatarFrame();
        updateFrameIndicator();
      });
    }

    // Speed buttons
    document.querySelectorAll('.speed-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.speed = parseFloat(btn.getAttribute('data-speed')) || 1.0;
        startAnimationLoop();
        updateFrameIndicator();
      });
    });

    // Weapon buttons population
    const weaponRow = document.getElementById('weaponSelectorRow');
    if (weaponRow && typeof DISPLAY_WEAPONS !== 'undefined') {
      weaponRow.innerHTML = '';
      DISPLAY_WEAPONS.forEach(w => {
        const btn = document.createElement('button');
        btn.className = `btn-chip ${state.weapon === w.id ? 'active' : ''}`;
        btn.textContent = w.name;
        btn.addEventListener('click', () => {
          weaponRow.querySelectorAll('.btn-chip').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          state.weapon = w.id;
          renderAvatarFrame();
        });
        weaponRow.appendChild(btn);
      });
    }

    // Armor buttons population
    const armorRow = document.getElementById('armorSelectorRow');
    if (armorRow && typeof DISPLAY_ARMORS !== 'undefined') {
      armorRow.innerHTML = '';
      DISPLAY_ARMORS.forEach(a => {
        const btn = document.createElement('button');
        btn.className = `btn-chip ${state.armor === a.id ? 'active' : ''}`;
        btn.textContent = a.name;
        btn.addEventListener('click', () => {
          armorRow.querySelectorAll('.btn-chip').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          state.armor = a.id;
          renderAvatarFrame();
        });
        armorRow.appendChild(btn);
      });
    }

    // Aura buttons
    document.querySelectorAll('[data-aura]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-aura]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.manualAura = btn.getAttribute('data-aura');
        renderAvatarFrame();
      });
    });

    // Mutation parts toggles
    const mutGrid = document.getElementById('mutationsToggleGrid');
    if (mutGrid && typeof TRAIT_PART_NAMES !== 'undefined') {
      mutGrid.innerHTML = '';
      Object.keys(TRAIT_PART_NAMES).forEach(part => {
        const btn = document.createElement('button');
        btn.className = 'btn-chip';
        btn.id = `mutToggleBtn_${part}`;
        btn.textContent = `${TRAIT_PART_NAMES[part]} (${part})`;
        btn.addEventListener('click', () => {
          state.manualPartsMode = true;
          state.manualParts[part] = !state.manualParts[part];
          btn.classList.toggle('active', state.manualParts[part]);
          renderAvatarFrame();
        });
        mutGrid.appendChild(btn);
      });
    }

    // Mutation sync buttons
    const btnSyncParts = document.getElementById('btnSyncPartsWithSlots');
    if (btnSyncParts) {
      btnSyncParts.addEventListener('click', () => {
        state.manualPartsMode = false;
        state.manualParts = {};
        syncMutationButtonsUI();
        renderAvatarFrame();
        showToast('신체 파츠가 슬롯 장착 특성과 실시간 동기화되었습니다.');
      });
    }

    const btnAllOn = document.getElementById('btnAllPartsOn');
    if (btnAllOn) {
      btnAllOn.addEventListener('click', () => {
        state.manualPartsMode = true;
        Object.keys(TRAIT_PART_NAMES).forEach(p => state.manualParts[p] = true);
        syncMutationButtonsUI();
        renderAvatarFrame();
      });
    }

    const btnAllOff = document.getElementById('btnAllPartsOff');
    if (btnAllOff) {
      btnAllOff.addEventListener('click', () => {
        state.manualPartsMode = true;
        Object.keys(TRAIT_PART_NAMES).forEach(p => state.manualParts[p] = false);
        syncMutationButtonsUI();
        renderAvatarFrame();
      });
    }
  }

  function syncMutationButtonsUI() {
    if (!TRAIT_PART_NAMES) return;
    const activeParts = getActivePartsList();
    Object.keys(TRAIT_PART_NAMES).forEach(part => {
      const btn = document.getElementById(`mutToggleBtn_${part}`);
      if (btn) {
        btn.classList.toggle('active', activeParts.includes(part));
      }
    });
  }

  function getActivePartsList() {
    if (state.manualPartsMode) {
      return Object.keys(state.manualParts).filter(p => state.manualParts[p]);
    }
    const parts = [];
    state.equippedTraits.forEach(tId => {
      if (tId && TRAIT_MUTATIONS && TRAIT_MUTATIONS[tId]) {
        parts.push(TRAIT_MUTATIONS[tId]);
      }
    });
    return parts;
  }

  // Render layered avatar frame
  function renderAvatarFrame() {
    const { gender, motion, frame, weapon, armor } = state;

    // Body
    const bodyEl = document.getElementById('disp-layer-body');
    if (bodyEl) {
      bodyEl.style.backgroundImage = `url('assets/pixel_hero/${gender}_${motion}_${frame}.png')`;
    }

    const isNemesis = gender.includes('nemesis');

    // Armor
    const armorEl = document.getElementById('disp-layer-armor');
    if (armorEl) {
      if (!isNemesis && armor && armor !== 'none') {
        const armorPrefix = gender === 'female' ? `female_${armor}` : armor;
        armorEl.style.backgroundImage = `url('assets/pixel_hero/armors/${armorPrefix}_${motion}_${frame}.png')`;
        armorEl.style.display = 'block';
      } else {
        armorEl.style.backgroundImage = 'none';
        armorEl.style.display = 'none';
      }
    }

    // Weapon
    const weaponEl = document.getElementById('disp-layer-weapon');
    if (weaponEl) {
      if (!isNemesis && weapon && weapon !== 'none') {
        weaponEl.style.backgroundImage = `url('assets/pixel_hero/weapons/${weapon}_${motion}_${frame}.png')`;
        weaponEl.style.display = 'block';
      } else {
        weaponEl.style.backgroundImage = 'none';
        weaponEl.style.display = 'none';
      }
    }

    // 13 Mutation layers
    const activeParts = getActivePartsList();
    if (typeof TRAIT_PART_NAMES !== 'undefined') {
      Object.keys(TRAIT_PART_NAMES).forEach(part => {
        const el = document.getElementById(`disp-layer-${part}`);
        if (el) {
          if (activeParts.includes(part)) {
            el.style.backgroundImage = `url('assets/pixel_hero/mutations/${part}_${motion}_${frame}.png')`;
            el.style.display = 'block';
          } else {
            el.style.backgroundImage = 'none';
            el.style.display = 'none';
          }
        }
      });
    }

    // Aura layer (matches index.css: .character-aura-effect, .aura-stage-1, .aura-stage-2)
    const auraEl = document.getElementById('disp-layer-aura');
    if (auraEl) {
      auraEl.className = 'character-aura-effect';
      let activeCount = state.equippedTraits.filter((tId, idx) => Boolean(tId && state.unlockedSlots[idx])).length;
      let effectiveStage = 0;

      if (state.manualAura === 'auto') {
        if (activeCount >= 3) effectiveStage = 2;
        else if (activeCount === 2) effectiveStage = 1;
        else effectiveStage = 0;
      } else {
        effectiveStage = parseInt(state.manualAura, 10) || 0;
      }

      if (effectiveStage === 1) {
        auraEl.classList.add('aura-stage-1');
      } else if (effectiveStage === 2) {
        auraEl.classList.add('aura-stage-2');
      }
    }
  }

  // --- 5. 3-Slot Simulator & Trait Palette ---
  function initSlotsAndPalette() {
    renderSlotsUI();
    renderPaletteUI();
    evaluateSynergies();
  }

  function renderSlotsUI() {
    for (let i = 0; i < 3; i++) {
      const card = document.getElementById(`slotCard${i}`);
      const nameEl = document.getElementById(`slotName${i}`);
      const partEl = document.getElementById(`slotPart${i}`);
      const toggleBtn = document.getElementById(`btnToggleLock${i}`);
      const unequipBtn = document.getElementById(`btnUnequip${i}`);

      if (!card || !nameEl || !partEl) continue;

      const isUnlocked = state.unlockedSlots[i];
      const traitId = state.equippedTraits[i];

      // Unlock button text
      if (toggleBtn) {
        toggleBtn.textContent = isUnlocked ? '🔓 해금됨' : '🔒 잠김';
        toggleBtn.style.color = isUnlocked ? '#00f0ff' : '#94a3b8';
        toggleBtn.style.borderColor = isUnlocked ? '#00f0ff' : '#475569';
      }

      // Slot Card state
      card.className = 'slot-display-box';
      if (!isUnlocked) {
        card.classList.add('locked');
        nameEl.textContent = '🔒 잠김';
        nameEl.style.color = '#64748b';
        partEl.textContent = i === 1 ? '2번째 마을 클리어 시 해금' : '3번째 마을 클리어 시 해금';
        if (unequipBtn) unequipBtn.style.display = 'none';
      } else {
        card.classList.add('unlocked');
        if (traitId && TRAITS_DATA[traitId]) {
          card.classList.add('equipped');
          const tData = TRAITS_DATA[traitId];
          const partId = TRAIT_MUTATIONS[traitId];
          const partName = TRAIT_PART_NAMES[partId] || partId;

          nameEl.textContent = `${tData.icon || '🧬'} ${tData.name}`;
          nameEl.style.color = TRAIT_COLORS[traitId] || '#00f0ff';
          partEl.innerHTML = `<span style="color:#facc15;">변이:</span> ${partName} (${partId})`;
          if (unequipBtn) unequipBtn.style.display = 'inline-block';
        } else {
          nameEl.textContent = '+ 빈 슬롯';
          nameEl.style.color = '#64748b';
          partEl.textContent = '특성 팔레트에서 클릭하여 장착';
          if (unequipBtn) unequipBtn.style.display = 'none';
        }
      }
    }
  }

  function renderPaletteUI() {
    const grid = document.getElementById('traitsPaletteGrid');
    if (!grid || typeof TRAITS_DATA === 'undefined') return;

    grid.innerHTML = '';
    Object.keys(TRAITS_DATA).forEach(tId => {
      const trait = TRAITS_DATA[tId];
      const isEquipped = state.equippedTraits.some((eqId, idx) => eqId === tId && state.unlockedSlots[idx]);
      const partId = TRAIT_MUTATIONS[tId];
      const partName = TRAIT_PART_NAMES[partId] || partId;

      const chip = document.createElement('div');
      chip.className = `trait-chip-card ${isEquipped ? 'slotted' : ''}`;
      chip.id = `palette_trait_${tId}`;
      chip.innerHTML = `
        <div class="trait-chip-cat">${isEquipped ? '✅ 슬롯 장착 중' : '+ 클릭하여 장착'}</div>
        <div class="trait-chip-name" style="color: ${TRAIT_COLORS[tId] || '#cbd5e1'}">
          ${trait.icon || '🧬'} ${trait.name}
        </div>
        <div class="trait-chip-part">
          파츠: <strong style="color: #facc15;">${partName} (${partId})</strong>
        </div>
      `;

      chip.addEventListener('click', () => {
        toggleEquipTrait(tId);
      });

      grid.appendChild(chip);
    });
  }

  window.toggleSlotLock = function (slotIndex) {
    state.unlockedSlots[slotIndex] = !state.unlockedSlots[slotIndex];
    if (!state.unlockedSlots[slotIndex]) {
      state.equippedTraits[slotIndex] = null;
    }
    state.manualPartsMode = false;
    updateAll();
  };

  window.unequipSlot = function (slotIndex) {
    if (!state.unlockedSlots[slotIndex]) return;
    state.equippedTraits[slotIndex] = null;
    state.manualPartsMode = false;
    updateAll();
  };

  function toggleEquipTrait(tId) {
    state.manualPartsMode = false;
    const existingIndex = state.equippedTraits.indexOf(tId);
    if (existingIndex !== -1) {
      // Unequip
      state.equippedTraits[existingIndex] = null;
      updateAll();
      showToast(`${TRAITS_DATA[tId].name} 특성을 해제했습니다.`);
      return;
    }

    // Find empty unlocked slot
    let slotToEquip = -1;
    for (let i = 0; i < 3; i++) {
      if (state.unlockedSlots[i] && !state.equippedTraits[i]) {
        slotToEquip = i;
        break;
      }
    }

    if (slotToEquip === -1) {
      showToast('⚠️ 빈 해금 슬롯이 없습니다! 슬롯을 해금하거나 기존 특성을 해제하세요.');
      return;
    }

    state.equippedTraits[slotToEquip] = tId;
    updateAll();
    showToast(`✅ [슬롯 ${slotToEquip + 1}] ${TRAITS_DATA[tId].name} 장착 완료!`);
  }

  // Evaluate Synergies according to rules:
  // 1 trait -> 1 part, single effect
  // 2 traits -> 2 parts, Stage 1 Cyan Aura, 1 dual fusion
  // 3 traits -> 3 parts, Stage 2 Crimson Aura, Double dual fusions ([1+2] & [2+3])
  function evaluateSynergies() {
    const bannerBox = document.getElementById('synergyBannerBox');
    if (!bannerBox) return;

    const activeList = [];
    state.equippedTraits.forEach((tId, idx) => {
      if (tId && state.unlockedSlots[idx]) {
        activeList.push({ id: tId, slot: idx + 1 });
      }
    });

    const count = activeList.length;

    if (count === 0) {
      bannerBox.innerHTML = `
        <div style="text-align: center; color: #64748b; font-size: 0.82rem; padding: 12px 0;">
          현재 장착된 특성이 없습니다. 우측 팔레트에서 특성을 선택해 장착하세요.
        </div>
      `;
      return;
    }

    if (count === 1) {
      const t = TRAITS_DATA[activeList[0].id];
      const part = TRAIT_MUTATIONS[activeList[0].id];
      const partName = TRAIT_PART_NAMES[part];
      bannerBox.innerHTML = `
        <div style="background: rgba(14, 165, 233, 0.08); border: 1px solid #0284c7; border-radius: 8px; padding: 12px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <strong style="color: #38bdf8; font-size: 0.88rem;">🌱 단일 특성 발현 상태 (파츠 1개 장착)</strong>
            <span style="font-size: 0.72rem; color: #94a3b8;">오라 미발현 (1/3)</span>
          </div>
          <div style="font-size: 0.78rem; color: #cbd5e1; line-height: 1.4;">
            - <strong>${t.name}</strong> 발현: 영웅 신체에 <span style="color:#facc15;">[${partName}]</span> 파츠가 생성되었습니다.<br>
            - <span style="color:#00f0ff;">2번째 슬롯</span>을 해금하고 특성을 추가 장착하면 <strong>초월 2중 융합 능력</strong> 및 <strong>1단계 청록 오라</strong>가 개화합니다!
          </div>
        </div>
      `;
      return;
    }

    if (count === 2) {
      const fData = findFusionBetween(activeList[0].id, activeList[1].id);
      bannerBox.innerHTML = `
        <div style="background: rgba(0, 240, 255, 0.08); border: 1px solid #00f0ff; border-radius: 8px; padding: 12px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <div style="display:flex; align-items:center; gap: 8px;">
              <span class="badge-num" style="background: #00f0ff; color:#05070c; font-weight:bold;">STAGE 1 AURA</span>
              <strong style="color: #00f0ff; font-size: 0.95rem;">⚡ 2특성 공명 융합 발동: ${fData ? fData.name : '미지의 융합'}</strong>
            </div>
            <span style="font-size: 0.72rem; color: #00f0ff;">청록 방사능 스월 오라 가동</span>
          </div>
          <div style="font-size: 0.8rem; color: #e2e8f0; background: rgba(0,0,0,0.4); padding: 8px 10px; border-radius: 6px; border-left: 3px solid #00f0ff;">
            ${fData ? fData.description : '특성 조합 분석 중...'}
          </div>
          <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 8px;">
            ✦ 변이 파츠 2종 동시 결착 | 3번째 특성 장착 시 <strong>더블 2중 융합([1+2] & [2+3])</strong> 및 <strong>진홍 코스믹 폭주 오라</strong>가 개방됩니다.
          </div>
        </div>
      `;
      return;
    }

    // 3 traits: Double 2-trait fusions ([1+2] & [2+3])
    const f1 = findFusionBetween(state.equippedTraits[0], state.equippedTraits[1]);
    const f2 = findFusionBetween(state.equippedTraits[1], state.equippedTraits[2]);

    bannerBox.innerHTML = `
      <div style="background: rgba(255, 42, 109, 0.1); border: 1.5px solid #ff2a6d; border-radius: 8px; padding: 12px; box-shadow: 0 0 15px rgba(255, 42, 109, 0.2);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
          <div style="display:flex; align-items:center; gap: 8px;">
            <span class="badge-num" style="background: #ff2a6d; color:#fff; font-weight:bold;">STAGE 2 MAX AURA</span>
            <strong style="color: #ff2a6d; font-size: 0.95rem;">🔥 3-특성 더블 2중 융합 동시 개화 (Twin Fusions Active)</strong>
          </div>
          <span style="font-size: 0.72rem; color: #ff5500; font-weight:bold;">진홍 코스믹 폭주 오라 가동</span>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px;">
          <!-- Fusion 1: Slot 1 + Slot 2 -->
          <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #38bdf8; border-radius: 6px; padding: 8px;">
            <div style="font-size: 0.7rem; color: #38bdf8; font-weight: bold; margin-bottom: 3px;">[1번+2번 융합] ${f1 ? f1.name : '융합 없음'}</div>
            <div style="font-size: 0.74rem; color: #cbd5e1; line-height: 1.3;">${f1 ? f1.description : '-'}</div>
          </div>
          
          <!-- Fusion 2: Slot 2 + Slot 3 -->
          <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #f43f5e; border-radius: 6px; padding: 8px;">
            <div style="font-size: 0.7rem; color: #f43f5e; font-weight: bold; margin-bottom: 3px;">[2번+3번 융합] ${f2 ? f2.name : '융합 없음'}</div>
            <div style="font-size: 0.74rem; color: #cbd5e1; line-height: 1.3;">${f2 ? f2.description : '-'}</div>
          </div>
        </div>

        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 8px; text-align: right;">
          ✦ 신체 변이 파츠 3종 전개 완료 | 영웅의 전투 능력이 궁극의 경지에 도달했습니다.
        </div>
      </div>
    `;
  }

  function findFusionBetween(idA, idB) {
    if (!idA || !idB || typeof FUSION_DATA === 'undefined') return null;
    for (const fKey in FUSION_DATA) {
      const f = FUSION_DATA[fKey];
      if (f.req && f.req.includes(idA) && f.req.includes(idB)) {
        return f;
      }
    }
    return null;
  }

  // --- 6. 78 Dual Fusions Matrix & Instant Tester ---
  function initFusionsMatrix() {
    // Filter chip buttons
    const filterRow = document.getElementById('fusionFilterChips');
    if (filterRow) {
      filterRow.querySelectorAll('.btn-chip').forEach(btn => {
        btn.addEventListener('click', () => {
          filterRow.querySelectorAll('.btn-chip').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          state.fusionCategory = btn.getAttribute('data-cat') || 'all';
          renderFusionsGrid();
        });
      });
    }

    // Search input
    const searchInput = document.getElementById('fusionSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        state.fusionSearchText = e.target.value.trim().toLowerCase();
        renderFusionsGrid();
      });
    }

    renderFusionsGrid();
  }

  function renderFusionsGrid() {
    const grid = document.getElementById('fusionsCardsGrid');
    if (!grid || typeof FUSION_DATA === 'undefined') return;

    grid.innerHTML = '';
    const fKeys = Object.keys(FUSION_DATA);

    let matchCount = 0;

    fKeys.forEach((fKey, index) => {
      const f = FUSION_DATA[fKey];
      const cat = getFusionCategory(fKey, f);

      // Category filter check
      if (state.fusionCategory !== 'all' && cat !== state.fusionCategory) {
        return;
      }

      // Search filter check
      if (state.fusionSearchText) {
        const query = state.fusionSearchText;
        const nameMatch = (f.name || '').toLowerCase().includes(query);
        const descMatch = (f.description || '').toLowerCase().includes(query);
        const req1Name = TRAITS_DATA[f.req[0]] ? TRAITS_DATA[f.req[0]].name.toLowerCase() : '';
        const req2Name = TRAITS_DATA[f.req[1]] ? TRAITS_DATA[f.req[1]].name.toLowerCase() : '';
        const reqMatch = req1Name.includes(query) || req2Name.includes(query);

        if (!nameMatch && !descMatch && !reqMatch) {
          return;
        }
      }

      matchCount++;

      const t1 = TRAITS_DATA[f.req[0]] || { name: f.req[0] };
      const t2 = TRAITS_DATA[f.req[1]] || { name: f.req[1] };
      const c1 = TRAIT_COLORS[f.req[0]] || '#38bdf8';
      const c2 = TRAIT_COLORS[f.req[1]] || '#ff2a6d';

      const activeSlot01 =
        (state.unlockedSlots[0] && state.unlockedSlots[1] &&
         ((state.equippedTraits[0] === f.req[0] && state.equippedTraits[1] === f.req[1]) ||
          (state.equippedTraits[0] === f.req[1] && state.equippedTraits[1] === f.req[0])));
      const activeSlot12 =
        (state.unlockedSlots[1] && state.unlockedSlots[2] &&
         ((state.equippedTraits[1] === f.req[0] && state.equippedTraits[2] === f.req[1]) ||
          (state.equippedTraits[1] === f.req[1] && state.equippedTraits[2] === f.req[0])));
      const isCurrentlyActive = activeSlot01 || activeSlot12;

      const card = document.createElement('div');
      card.className = `fusion-catalog-card ${isCurrentlyActive ? 'active-match' : ''}`;
      card.innerHTML = `
        <div>
          <div class="fusion-card-title">
            <span>${f.name}</span>
            <span style="font-size:0.7rem; color:#64748b;">#${index + 1}</span>
          </div>
          <div class="fusion-req-tags">
            <span class="req-chip" style="border-color:${c1}; color:${c1};">${t1.name}</span>
            <span style="color:#64748b; font-size:0.7rem;">+</span>
            <span class="req-chip" style="border-color:${c2}; color:${c2};">${t2.name}</span>
          </div>
          <div class="fusion-card-desc">
            ${f.description}
          </div>
        </div>
        <div style="display:flex; gap:6px; margin-top:10px;">
          <button class="btn-test-fusion btn-instant-2slot" style="flex:1; margin-top:0;">
            ${activeSlot01 ? '⚡ [1+2] 가동 중' : '⚡ [1+2] 장착 시험'}
          </button>
          <button class="btn-test-fusion btn-instant-3slot" style="flex:1; margin-top:0; border-color:#f43f5e; color:#fda4af;">
            ${activeSlot12 ? '🔥 [2+3] 가동 중' : '🔥 3슬롯 더블 융합'}
          </button>
        </div>
      `;

      card.querySelector('.btn-instant-2slot').addEventListener('click', (e) => {
        e.stopPropagation();
        instantSlotFusion(f.req[0], f.req[1], f.name, false);
      });

      card.querySelector('.btn-instant-3slot').addEventListener('click', (e) => {
        e.stopPropagation();
        instantSlotFusion(f.req[0], f.req[1], f.name, true);
      });

      grid.appendChild(card);
    });

    if (matchCount === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; color: #64748b; padding: 40px 0; font-size: 0.9rem;">
          검색 조건에 맞는 융합 조합이 없습니다. (검색어: "${state.fusionSearchText}")
        </div>
      `;
    }
  }

  // Instant slot fusion test (2-slot single fusion or 3-slot double fusion)
  function instantSlotFusion(req1, req2, fusionName, asDoubleFusion) {
    state.unlockedSlots[0] = true;
    state.unlockedSlots[1] = true;
    state.manualPartsMode = false;

    if (asDoubleFusion) {
      state.unlockedSlots[2] = true;
      // Keep slot 0 if it's distinct from req1/req2, otherwise pick a distinct 3rd trait so [1+2] & [2+3] both fire!
      let slot0Trait = state.equippedTraits[0];
      if (!slot0Trait || slot0Trait === req1 || slot0Trait === req2) {
        const allIds = Object.keys(TRAITS_DATA);
        slot0Trait = allIds.find(id => id !== req1 && id !== req2) || 'body_mutation';
      }
      state.equippedTraits[0] = slot0Trait;
      state.equippedTraits[1] = req1;
      state.equippedTraits[2] = req2;
    } else {
      state.equippedTraits[0] = req1;
      state.equippedTraits[1] = req2;
      state.equippedTraits[2] = null;
    }

    // Trigger visual action preview
    state.motion = asDoubleFusion ? 'skill' : 'attack';
    state.frame = 0;

    // Trigger slight flash on vfx
    const vfxEl = document.getElementById('disp-layer-vfx');
    if (vfxEl) {
      vfxEl.style.boxShadow = asDoubleFusion ? 'inset 0 0 45px #ff2a6d' : 'inset 0 0 40px #00f0ff';
      setTimeout(() => { if (vfxEl) vfxEl.style.boxShadow = 'none'; }, 600);
    }

    // Update everything
    updateAll();

    // Scroll smoothly to Hero Studio
    const studioSection = document.getElementById('section-hero');
    if (studioSection) {
      studioSection.scrollIntoView({ behavior: 'smooth' });
    }

    if (asDoubleFusion) {
      showToast(`🔥 [${fusionName}] 포함 3슬롯 더블 2중 융합([1+2] & [2+3]) 및 2단계 폭주 오라 가동!`);
    } else {
      showToast(`⚡ [${fusionName}] 2슬롯 융합 장착 완료! 파츠 2종 & 1단계 오라가 개화되었습니다.`);
    }
  }

  // --- 7. Monster Gallery & Action Tester ---
  function initMonsterGallery() {
    // Populate region buttons
    const regFilter = document.getElementById('monsterRegionFilter');
    if (regFilter && typeof MONSTERS_DATABASE !== 'undefined') {
      regFilter.innerHTML = '';
      const regions = Object.keys(MONSTERS_DATABASE).map(Number).sort((a, b) => a - b);
      regions.forEach(r => {
        const btn = document.createElement('button');
        btn.className = `btn-chip ${r === state.selectedMonsterRegion ? 'active' : ''}`;
        btn.textContent = `${r}지역`;
        btn.addEventListener('click', () => {
          regFilter.querySelectorAll('.btn-chip').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          state.selectedMonsterRegion = r;
          renderMonsterGalleryScroll();
        });
        regFilter.appendChild(btn);
      });
    }

    // Action buttons (matches index.css: .monster-motion-lunge, .monster-motion-knockback, .defeated)
    const wrapper = document.getElementById('demoMonsterWrapper');
    const spriteEl = document.getElementById('demoMonsterSprite');
    const hpBar = document.getElementById('demoMonsterHpBar');
    const label = document.getElementById('demoMonsterLabel');

    const btnLunge = document.getElementById('btnTestLunge');
    if (btnLunge) {
      btnLunge.addEventListener('click', () => {
        if (!wrapper) return;
        if (spriteEl) spriteEl.classList.remove('defeated');
        wrapper.classList.remove('monster-motion-knockback', 'monster-motion-lunge');
        void wrapper.offsetWidth; // re-flow
        wrapper.classList.add('monster-motion-lunge');
        showToast('⚔️ 공격 돌진 (Lunge): 좌측 영웅 방향 -75px 전진 (카드 뒤집힘 없음)');
      });
    }

    const btnKnockback = document.getElementById('btnTestKnockback');
    if (btnKnockback) {
      btnKnockback.addEventListener('click', () => {
        if (!wrapper) return;
        if (spriteEl) spriteEl.classList.remove('defeated');
        wrapper.classList.remove('monster-motion-lunge', 'monster-motion-knockback');
        void wrapper.offsetWidth;
        wrapper.classList.add('monster-motion-knockback');
        const maxHp = state.selectedMonster ? state.selectedMonster.hp : 550;
        const curHp = Math.round(maxHp * 0.65);
        if (hpBar) hpBar.style.width = '65%';
        if (label) label.textContent = `HP: ${curHp} / ${maxHp} (피격)`;
        showToast('💥 피격 넉백 (Knockback): 우측 +28px 반동 및 쉐이크');
      });
    }

    const btnDefeat = document.getElementById('btnTestDefeat');
    if (btnDefeat) {
      btnDefeat.addEventListener('click', () => {
        if (!wrapper) return;
        wrapper.classList.remove('monster-motion-lunge', 'monster-motion-knockback');
        if (spriteEl) spriteEl.classList.add('defeated');
        const maxHp = state.selectedMonster ? state.selectedMonster.hp : 550;
        if (hpBar) hpBar.style.width = '0%';
        if (label) label.textContent = `HP: 0 / ${maxHp} (전투 불능)`;
        showToast('💀 전투 불능 (Defeat): 90도 전도 및 그레이스케일 페이드아웃');
      });
    }

    const btnReset = document.getElementById('btnTestReset');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        if (wrapper) wrapper.classList.remove('monster-motion-lunge', 'monster-motion-knockback');
        if (spriteEl) spriteEl.classList.remove('defeated');
        if (hpBar) hpBar.style.width = '100%';
        if (label && state.selectedMonster) {
          label.textContent = `HP: ${state.selectedMonster.hp} / ${state.selectedMonster.hp}`;
        }
        showToast('🔄 괴수 액션 및 HP 상태 초기화 완료');
      });
    }

    renderMonsterGalleryScroll();

    // Default select first monster
    if (MONSTERS_DATABASE[1] && MONSTERS_DATABASE[1][0]) {
      selectMonster(MONSTERS_DATABASE[1][0]);
    }
  }

  function renderMonsterGalleryScroll() {
    const scrollEl = document.getElementById('monsterGalleryScroll');
    if (!scrollEl || typeof MONSTERS_DATABASE === 'undefined') return;

    scrollEl.innerHTML = '';
    const list = MONSTERS_DATABASE[state.selectedMonsterRegion] || [];

    list.forEach(m => {
      const card = document.createElement('div');
      const isSelected = state.selectedMonster && state.selectedMonster.name === m.name;
      card.className = `monster-card-thumb ${isSelected ? 'selected' : ''}`;
      
      const isCleanedBat = m.img && m.img.includes('m_4_2');

      card.innerHTML = `
        <div class="monster-thumb-img" style="background-image: url('${m.img}');"></div>
        <div style="font-size:0.78rem; font-weight:700; color:#f1f5f9;">${m.name}</div>
        <div style="font-size:0.65rem; color:#94a3b8; margin-top:2px;">${m.type.toUpperCase()} | HP ${m.hp}</div>
        ${isCleanedBat ? '<div class="clean-badge">✨ 텍스트 제거 완료</div>' : ''}
      `;

      card.addEventListener('click', () => {
        selectMonster(m);
        scrollEl.querySelectorAll('.monster-card-thumb').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
      });

      scrollEl.appendChild(card);
    });
  }

  function selectMonster(m) {
    state.selectedMonster = m;
    const nameEl = document.getElementById('testMonsterName');
    const spriteEl = document.getElementById('demoMonsterSprite');
    const labelEl = document.getElementById('demoMonsterLabel');
    const hpBar = document.getElementById('demoMonsterHpBar');
    const wrapper = document.getElementById('demoMonsterWrapper');

    if (nameEl) nameEl.textContent = `${m.name} [${m.type.toUpperCase()}]`;
    if (spriteEl) {
      spriteEl.style.backgroundImage = `url('${m.img}')`;
      spriteEl.classList.remove('defeated');
    }
    if (labelEl) labelEl.textContent = `HP: ${m.hp} / ${m.hp}`;
    if (hpBar) hpBar.style.width = '100%';
    if (wrapper) wrapper.classList.remove('monster-motion-lunge', 'monster-motion-knockback');
  }

  // --- 8. UI Synchronization & Toast Helper ---
  function updateAll() {
    renderAvatarFrame();
    syncMutationButtonsUI();
    renderSlotsUI();
    renderPaletteUI();
    evaluateSynergies();
    renderFusionsGrid();
  }

  function showToast(msg) {
    let toast = document.getElementById('displayToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'displayToast';
      toast.style.position = 'fixed';
      toast.style.bottom = '24px';
      toast.style.right = '24px';
      toast.style.backgroundColor = 'rgba(15, 23, 42, 0.95)';
      toast.style.color = '#00f0ff';
      toast.style.border = '1px solid #00f0ff';
      toast.style.borderRadius = '8px';
      toast.style.padding = '12px 18px';
      toast.style.fontSize = '0.82rem';
      toast.style.zIndex = '9999';
      toast.style.boxShadow = '0 0 20px rgba(0, 240, 255, 0.3)';
      toast.style.transition = 'all 0.3s ease';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';

    if (window._toastTimeout) clearTimeout(window._toastTimeout);
    window._toastTimeout = setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
    }, 2800);
  }

})();
