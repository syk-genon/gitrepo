# -*- coding: utf-8 -*-
import os, sys

sys.stdout.reconfigure(encoding="utf-8")

HTML_PATH = r"D:\workspace\GEMINI\project_necro\display.html"
JS_PATH = r"D:\workspace\GEMINI\project_necro\display.js"

# 1. Update display.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# A) Upgrade #studioStage in Section 1 with layered background, scrolling clouds, and 4-frame foliage
old_studio = """                <div class="studio-stage" id="studioStage">
                    <!-- 하단 안개 바닥선 -->
                    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 45px; background: linear-gradient(to top, rgba(0,0,0,0.85), transparent); pointer-events: none; border-bottom: 2px solid rgba(255,204,0,0.2);"></div>"""

new_studio = """                <div class="studio-stage" id="studioStage" style="background-image: url('assets/ui/regions/town_bg_1_f0.png'); background-size: cover; background-position: center; image-rendering: pixelated;">
                    <!-- [Layer 0] 배경 딤 오버레이 -->
                    <div style="position: absolute; inset: 0; background: rgba(10, 7, 5, 0.42); pointer-events: none; z-index: 1;"></div>
                    <!-- [Layer 1] GIMP 분리 구름 레이어 (1px 무한 우측 타일 스크롤) -->
                    <div id="studioCloudLayer" style="position: absolute; top: 4px; left: 0; right: 0; height: 95px; background-image: url('assets/ui/regions/clouds_strip.png'); background-repeat: repeat-x; background-size: 480px 95px; image-rendering: pixelated; pointer-events: none; opacity: 0.85; z-index: 2;"></div>
                    <!-- [Layer 2] GIMP 분리 나뭇잎/수풀 4프레임 루프 레이어 (7 FPS: 기본->살짝휨->최대휨->중간복귀) -->
                    <div id="studioFoliageLayer" style="position: absolute; inset: 0; background-image: url('assets/ui/regions/foliage_overlay_f0.png'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 3;"></div>
                    <!-- 하단 안개 바닥선 -->
                    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 45px; background: linear-gradient(to top, rgba(0,0,0,0.85), transparent); pointer-events: none; border-bottom: 2px solid rgba(255,204,0,0.2); z-index: 4;"></div>"""

if "studioCloudLayer" not in html:
    assert old_studio in html, "old_studio not found in display.html"
    html = html.replace(old_studio, new_studio, 1)

# B) Upgrade Section 4 #townBgView and #battleBgView with GIMP/Krita 3-layer separation
old_sec4_stage = """        <!-- 좌/우 듀얼 인터랙티브 스테이지: [좌: 생존자 거점 마을 & 차원문 입장] ➔ [우: 차원문 내부 6웨이브 전투 스테이지] -->
        <div style="display: grid; grid-template-columns: 1fr 1.25fr; gap: 16px;">
            <!-- 좌: 생존자 거점 마을 배경 + 영웅(정면 뷰) + 클릭 가능한 차원문(Gate) 오브젝트 -->
            <div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="townBgView">"""

new_sec4_stage = """        <!-- GIMP/Krita 다중 레이어 분리 루프 애니메이션 제어 & 실시간 상태 바 -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; padding: 7px 12px; background: rgba(12, 18, 14, 0.9); border: 1px solid var(--neon-green);">
            <div style="font-size: 0.72rem; color: var(--text-ivory); display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="color: var(--neon-green); font-weight: bold;">🎨 [GIMP/Krita 3-레이어 분리 루프 엔진]</span>
                <span id="foliageLoopStatusText" style="color: var(--neon-gold);">🌿 수풀/나뭇잎 레이어: Frame 1/4 (기본 위치 · 7 FPS)</span>
                <span style="color: #666;">|</span>
                <span id="cloudScrollStatusText" style="color: var(--neon-cyan);">☁️ 구름 스크롤 레이어: +0px (1px 무한 타일 스크롤)</span>
                <span style="color: #666;">|</span>
                <span style="color: var(--neon-pink);">🧙 캐릭터/괴수 레이어: 2~4프레임 대기 호흡</span>
            </div>
            <div style="display: flex; gap: 6px;">
                <button class="btn-chip active" id="btnToggleFoliageLoop" style="font-size: 0.65rem; padding: 2px 8px;" onclick="toggleFoliageSwayLoop()">🌿 나뭇잎 4프레임 흔들림: ON</button>
                <button class="btn-chip active" id="btnToggleCloudScroll" style="font-size: 0.65rem; padding: 2px 8px;" onclick="toggleCloudScrollLoop()">☁️ 구름 1px 스크롤: ON</button>
            </div>
        </div>

        <!-- 좌/우 듀얼 인터랙티브 스테이지: [좌: 생존자 거점 마을 & 차원문 입장] ➔ [우: 차원문 내부 6웨이브 전투 스테이지] -->
        <div style="display: grid; grid-template-columns: 1fr 1.25fr; gap: 16px;">
            <!-- 좌: 생존자 거점 마을 배경 + 영웅(정면 뷰) + 클릭 가능한 차원문(Gate) 오브젝트 -->
            <div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="townBgView">
                <!-- [Layer 1] 분리된 구름 레이어 (1px씩 천천히 오른쪽으로 무한 타일 스크롤) -->
                <div id="townCloudLayer" style="position: absolute; top: 4px; left: 0; right: 0; height: 96px; background-image: url('assets/ui/regions/clouds_strip.png'); background-repeat: repeat-x; background-size: 480px 96px; image-rendering: pixelated; pointer-events: none; opacity: 0.9; z-index: 2;"></div>
                <!-- [Layer 2] 분리된 나뭇잎/수풀/풀잎 4프레임 반복 레이어 (6~8 FPS 리듬감 있는 흔들림) -->
                <div id="townFoliageLayer" style="position: absolute; inset: 0; background-image: url('assets/ui/regions/foliage_overlay_f0.png'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4;"></div>"""

if "townCloudLayer" not in html:
    assert old_sec4_stage in html, "old_sec4_stage not found in display.html"
    html = html.replace(old_sec4_stage, new_sec4_stage, 1)

old_battle_stage = """            <!-- 우: 차원문 내부 전투 전장 배경 + 6웨이브 진행 바 + 영웅(우향) vs 지역 고유 괴수(좌향 scaleX(-1)) -->
            <div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="battleBgView">"""

new_battle_stage = """            <!-- 우: 차원문 내부 전투 전장 배경 + 6웨이브 진행 바 + 영웅(우향) vs 지역 고유 괴수(좌향 scaleX(-1)) -->
            <div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="battleBgView">
                <!-- [Layer 1] 분리된 구름/전장 대기 레이어 (1px 무한 우측 스크롤) -->
                <div id="battleCloudLayer" style="position: absolute; top: 4px; left: 0; right: 0; height: 96px; background-image: url('assets/ui/regions/clouds_strip.png'); background-repeat: repeat-x; background-size: 480px 96px; image-rendering: pixelated; pointer-events: none; opacity: 0.78; z-index: 2;"></div>
                <!-- [Layer 2] 분리된 나뭇잎/수풀/풀잎 4프레임 반복 레이어 (6~8 FPS) -->
                <div id="battleFoliageLayer" style="position: absolute; inset: 0; background-image: url('assets/ui/regions/foliage_overlay_f0.png'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4;"></div>"""

if "battleCloudLayer" not in html:
    assert old_battle_stage in html, "old_battle_stage not found in display.html"
    html = html.replace(old_battle_stage, new_battle_stage, 1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated display.html with GIMP/Krita 3-layer separation DOM elements.")


# 2. Update display.js
with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()

old_js_bg_set = """    // 마을 배경 & 전투 배경 고유 이미지 적용 (1~14지역 모두 개별 에셋)
    const townView = document.getElementById('townBgView');
    if (townView) townView.style.backgroundImage = `url('${rData.town}')`;

    const battleView = document.getElementById('battleBgView');
    if (battleView) battleView.style.backgroundImage = `url('${rData.battle}')`;"""

new_js_bg_set = """    // 마을 배경 & 전투 배경 4프레임 루프 에셋 프리로드 및 초기 프레임 적용
    preloadRegion4FrameBackgrounds(rId);
    applyRegionSwayFrame(rId, bgFoliageFrameIdx);"""

if "preloadRegion4FrameBackgrounds" not in js:
    assert old_js_bg_set in js, "old_js_bg_set not found in display.js"
    js = js.replace(old_js_bg_set, new_js_bg_set, 1)

old_js_init = """// 초기화
window.addEventListener('DOMContentLoaded', () => {
    selectClass("necro");
    switchView("side");
    setAnimation("idle");
    animInterval = setInterval(tickAnimationFrame, 100);
    
    renderRegressionUi();
    renderUniqueItems();
    renderAllSkillsGallery();
    switchRegionTheme(1);
});"""

new_js_init = """// =========================================================================
// 8. GIMP / Krita 다중 레이어 분리 루프 애니메이션 엔진
//    - Layer 1 (구름 레이어): 픽셀 단위 1px씩 천천히 오른쪽으로 무한 타일 스크롤
//    - Layer 2 (나뭇잎/수풀 레이어): 4프레임 반복 (0:기본 -> 1:살짝휨 -> 2:최대휨 -> 3:중간복귀), 약 7 FPS (140ms)
//    - Layer 3 (캐릭터/몬스터 레이어): 2~4프레임 독립 정지 대기 호흡 모션
// =========================================================================
let bgFoliageFrameIdx = 0;
let isFoliageLoopActive = true;
let isCloudScrollActive = true;
let cloudScrollOffsetPx = 0;
let foliageLoopTimer = null;
let cloudScrollTimer = null;
const preloadedRegionBgs = {};

const FOLIAGE_FRAME_LABELS = [
    "Frame 1/4 (기본 위치 · 0px)",
    "Frame 2/4 (오른쪽 살짝 휨 · +1px)",
    "Frame 3/4 (최대 휨 · +2px)",
    "Frame 4/4 (돌아오는 중간 단계 · +1px)"
];

function preloadRegion4FrameBackgrounds(rId) {
    if (preloadedRegionBgs[rId]) return;
    preloadedRegionBgs[rId] = [];
    for (let f = 0; f < 4; f++) {
        const tImg = new Image();
        tImg.src = `assets/ui/regions/town_bg_${rId}_f${f}.png`;
        const bImg = new Image();
        bImg.src = `assets/ui/regions/battle_bg_${rId}_f${f}.png`;
        const oImg = new Image();
        oImg.src = `assets/ui/regions/foliage_overlay_f${f}.png`;
        preloadedRegionBgs[rId].push(tImg, bImg, oImg);
    }
}

function applyRegionSwayFrame(rId, fIdx) {
    const townView = document.getElementById('townBgView');
    if (townView) {
        townView.style.backgroundImage = `url('assets/ui/regions/town_bg_${rId}_f${fIdx}.png')`;
    }
    const battleView = document.getElementById('battleBgView');
    if (battleView) {
        battleView.style.backgroundImage = `url('assets/ui/regions/battle_bg_${rId}_f${fIdx}.png')`;
    }
    const studioStage = document.getElementById('studioStage');
    if (studioStage) {
        studioStage.style.backgroundImage = `url('assets/ui/regions/town_bg_${rId}_f${fIdx}.png')`;
    }

    const overlayUrl = `url('assets/ui/regions/foliage_overlay_f${fIdx}.png')`;
    const townFol = document.getElementById('townFoliageLayer');
    if (townFol) townFol.style.backgroundImage = overlayUrl;
    const battleFol = document.getElementById('battleFoliageLayer');
    if (battleFol) battleFol.style.backgroundImage = overlayUrl;
    const studioFol = document.getElementById('studioFoliageLayer');
    if (studioFol) studioFol.style.backgroundImage = overlayUrl;

    const statusEl = document.getElementById('foliageLoopStatusText');
    if (statusEl) {
        statusEl.textContent = `🌿 수풀/나뭇잎 레이어: ${FOLIAGE_FRAME_LABELS[fIdx]} (7 FPS)`;
    }
}

function tickFoliage4FrameLoop() {
    if (!isFoliageLoopActive) return;
    bgFoliageFrameIdx = (bgFoliageFrameIdx + 1) % 4;
    applyRegionSwayFrame(currentRegionId, bgFoliageFrameIdx);

    // 4프레임 주기마다 전투장 몬스터와 영웅도 고전 16비트 특유의 2~4프레임 대기 호흡 연출
    const bossSprite = document.getElementById('battleBossSprite');
    if (bossSprite) {
        const bobY = (bgFoliageFrameIdx === 1 || bgFoliageFrameIdx === 2) ? -3 : 0;
        bossSprite.style.transform = `scaleX(-1) translateY(${bobY}px)`;
    }
    const battleHeroImg = document.getElementById('battleHeroSpriteImg');
    if (battleHeroImg) {
        const heroBobY = (bgFoliageFrameIdx % 2 === 1) ? -2 : 0;
        battleHeroImg.style.transform = `scaleX(1) translateY(${heroBobY}px)`;
    }
}

function tickCloud1pxScroll() {
    if (!isCloudScrollActive) return;
    // 픽셀 단위로 1px씩 천천히 오른쪽으로 밀어주는 타일 스크롤 방식
    cloudScrollOffsetPx = (cloudScrollOffsetPx + 1) % 480;
    const posStr = `${cloudScrollOffsetPx}px 0px`;

    const townCloud = document.getElementById('townCloudLayer');
    if (townCloud) townCloud.style.backgroundPosition = posStr;
    const battleCloud = document.getElementById('battleCloudLayer');
    if (battleCloud) battleCloud.style.backgroundPosition = posStr;
    const studioCloud = document.getElementById('studioCloudLayer');
    if (studioCloud) studioCloud.style.backgroundPosition = posStr;

    const cloudStatus = document.getElementById('cloudScrollStatusText');
    if (cloudStatus) {
        cloudStatus.textContent = `☁️ 구름 스크롤 레이어: +${cloudScrollOffsetPx}px (1px 무한 타일 스크롤)`;
    }
}

function toggleFoliageSwayLoop() {
    isFoliageLoopActive = !isFoliageLoopActive;
    const btn = document.getElementById('btnToggleFoliageLoop');
    if (btn) {
        btn.classList.toggle('active', isFoliageLoopActive);
        btn.textContent = `🌿 나뭇잎 4프레임 흔들림: ${isFoliageLoopActive ? 'ON' : 'OFF'}`;
    }
}

function toggleCloudScrollLoop() {
    isCloudScrollActive = !isCloudScrollActive;
    const btn = document.getElementById('btnToggleCloudScroll');
    if (btn) {
        btn.classList.toggle('active', isCloudScrollActive);
        btn.textContent = `☁️ 구름 1px 스크롤: ${isCloudScrollActive ? 'ON' : 'OFF'}`;
    }
}

// 초기화
window.addEventListener('DOMContentLoaded', () => {
    selectClass("necro");
    switchView("side");
    setAnimation("idle");
    animInterval = setInterval(tickAnimationFrame, 100);

    // 1) 나뭇잎/수풀 4프레임 루프: 초당 약 7 FPS (142ms 간격)로 느긋하고 리듬감 있게 재생
    foliageLoopTimer = setInterval(tickFoliage4FrameLoop, 142);
    // 2) 구름 레이어 스크롤: 픽셀 단위로 1px씩 천천히 오른쪽으로 이동 (60ms 간격)
    cloudScrollTimer = setInterval(tickCloud1pxScroll, 60);

    renderRegressionUi();
    renderUniqueItems();
    renderAllSkillsGallery();
    switchRegionTheme(1);
});"""

if "tickFoliage4FrameLoop" not in js:
    assert old_js_init in js, "old_js_init not found in display.js"
    js = js.replace(old_js_init, new_js_init, 1)

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated display.js with 4-frame foliage loop (7 FPS) + 1px continuous cloud scroll.")
