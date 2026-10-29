# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

HTML_PATH = r"D:\workspace\GEMINI\project_necro\display.html"
JS_PATH = r"D:\workspace\GEMINI\project_necro\display.js"

# 1. Remove cloud layers and cloud buttons from display.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Remove #studioCloudLayer, #townCloudLayer, #battleCloudLayer lines
html = re.sub(r'\s*<!-- \[Layer 1\][^\n]*\n\s*<div id="studioCloudLayer"[^\n]*</div>', '', html)
html = re.sub(r'\s*<!-- \[Layer 1\][^\n]*\n\s*<div id="townCloudLayer"[^\n]*</div>', '', html)
html = re.sub(r'\s*<!-- \[Layer 1\][^\n]*\n\s*<div id="battleCloudLayer"[^\n]*</div>', '', html)

# Update the status bar in Section 4 to show Region-Specific 4-Frame Object Layer + Character Idle Layer (no clouds!)
old_bar_pattern = r'<!-- GIMP/Krita 다중 레이어 분리 루프 애니메이션 제어 & 실시간 상태 바 -->[\s\S]*?<button class="btn-chip active" id="btnToggleCloudScroll"[^\n]*</button>\s*</div>\s*</div>'

new_bar_html = """<!-- 지역별 고유 환경 오브젝트 4프레임 루프 제어 & 실시간 상태 바 -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; padding: 7px 12px; background: rgba(12, 18, 14, 0.9); border: 1px solid var(--neon-green);">
            <div style="font-size: 0.72rem; color: var(--text-ivory); display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="color: var(--neon-green); font-weight: bold;">🎨 [지역별 고유 오브젝트 4프레임 루프]</span>
                <span id="regionPropNameBadge" style="color: var(--neon-cyan); font-weight: bold;">🏮 1지역 오브젝트: 을지로 청사초롱 가로등 & 지하 발광 포자</span>
                <span style="color: #666;">|</span>
                <span id="foliageLoopStatusText" style="color: var(--neon-gold);">Frame 1/4 (기본 위치 · 7 FPS)</span>
                <span style="color: #666;">|</span>
                <span style="color: var(--neon-pink);">🧙 캐릭터/괴수: 2~4프레임 대기 호흡</span>
            </div>
            <div style="display: flex; gap: 6px;">
                <button class="btn-chip active" id="btnToggleFoliageLoop" style="font-size: 0.65rem; padding: 2px 8px;" onclick="toggleFoliageSwayLoop()">🌿 지역 고유 오브젝트 4프레임 모션: ON</button>
            </div>
        </div>"""

html, n_rep = re.subn(old_bar_pattern, new_bar_html, html)
print(f"Updated display.html: removed all cloud layers and updated status bar (replacements={n_rep})")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)


# 2. Update display.js to load region_obj_${rId}_f${fIdx}.png?v=3 and show each region's unique object description
with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()

start_marker = "// =========================================================================\n// 8. GIMP / Krita 다중 레이어 분리 루프 애니메이션 엔진"
idx = js.find(start_marker)
assert idx != -1, "start_marker not found in display.js"

new_js_tail = """// =========================================================================
// 8. 14대 지역별 고유 환경 오브젝트 4프레임 루프 애니메이션 엔진 (7 FPS)
//    - 구름 레이어 완전 제거 (지역 몰입감 유지)
//    - 1~14지역마다 완전히 다른 고유 전경 오브젝트(`region_obj_${rId}_f0..3.png`)가 4프레임 주기로 작동
// =========================================================================
let bgFoliageFrameIdx = 0;
let isFoliageLoopActive = true;
let foliageLoopTimer = null;
const preloadedRegionBgs = {};

const REGION_UNIQUE_PROP_NAMES = {
    1:  "🏮 [1지역 고유 오브젝트] 을지로 청사초롱 가로등 & 지하 미궁 발광 독버섯 포자",
    2:  "🌲 [2지역 고유 오브젝트] 북한산 성역 초롱불 신목(神木) & 푸른 결계 들꽃 수풀",
    3:  "⚓ [3지역 고유 오브젝트] 인천항 부두 강철 크레인 쇠사슬 & 타오르는 화염 드럼통",
    4:  "❄️ [4지역 고유 오브젝트] 설악산 대청봉 고드름 눈소나무 & 청풍 빙결정 클러스터",
    5:  "🚨 [5지역 고유 오브젝트] 평양 지하벙커 적색 회전 경보등 기둥 & 철조망 탄약고",
    6:  "⛩️ [6지역 고유 오브젝트] 도쿄 음양사 주술 부적(오후다) 도리이 기둥 & 청록 여우불",
    7:  "🐉 [7지역 고유 오브젝트] 마카오 불야성 황금 반룡 기둥 & 붉은 비단 홍등·황금 화로",
    8:  "🧊 [8지역 고유 오브젝트] 블라디보스토크 극저온 빙하 수정 기둥 & 동토의 눈보라 침엽수",
    9:  "🪸 [9지역 고유 오브젝트] 태평양 해연 발광 심해 해조류(켈프) 숲 & 심연 산호초 기둥",
    10: "🦴 [10지역 고유 오브젝트] 히말라야 만년설 고룡 거대 늑골(해골) 기둥 & 푸른 영혼 화로",
    11: "🌵 [11지역 고유 오브젝트] 타클라마칸 황금 룬 사막 오벨리스크 & 열사 선인장·고목",
    12: "🌋 [12지역 고유 오브젝트] 로키 화산 흑요석 첨탑 & 분출하는 용암 불기둥 간헐천",
    13: "🛸 [13지역 고유 오브젝트] 성층권 외계 모함 반중력 플라즈마 파일런 & 홀로그램 코어",
    14: "💎 [14지역 고유 오브젝트] 황제의 다이아몬드 차원 수정 기둥 & 진홍빛 아공간 파편"
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
        tImg.src = `assets/ui/regions/town_bg_${rId}_f${f}.png?v=3`;
        const bImg = new Image();
        bImg.src = `assets/ui/regions/battle_bg_${rId}_f${f}.png?v=3`;
        const oImg = new Image();
        oImg.src = `assets/ui/regions/region_obj_${rId}_f${f}.png?v=3`;
        preloadedRegionBgs[rId].push(tImg, bImg, oImg);
    }
}

function applyRegionSwayFrame(rId, fIdx) {
    const townView = document.getElementById('townBgView');
    if (townView) {
        townView.style.backgroundImage = `url('assets/ui/regions/town_bg_${rId}_f${fIdx}.png?v=3')`;
    }
    const battleView = document.getElementById('battleBgView');
    if (battleView) {
        battleView.style.backgroundImage = `url('assets/ui/regions/battle_bg_${rId}_f${fIdx}.png?v=3')`;
    }
    const studioStage = document.getElementById('studioStage');
    if (studioStage) {
        studioStage.style.backgroundImage = `url('assets/ui/regions/town_bg_${rId}_f${fIdx}.png?v=3')`;
    }

    // 각 지역(1~14)마다 고유한 4프레임 환경 오브젝트 오버레이 적용!
    const overlayUrl = `url('assets/ui/regions/region_obj_${rId}_f${fIdx}.png?v=3')`;
    const townFol = document.getElementById('townFoliageLayer');
    if (townFol) townFol.style.backgroundImage = overlayUrl;
    const battleFol = document.getElementById('battleFoliageLayer');
    if (battleFol) battleFol.style.backgroundImage = overlayUrl;
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

function toggleFoliageSwayLoop() {
    isFoliageLoopActive = !isFoliageLoopActive;
    const btn = document.getElementById('btnToggleFoliageLoop');
    if (btn) {
        btn.classList.toggle('active', isFoliageLoopActive);
        btn.textContent = `🌿 지역 고유 오브젝트 4프레임 모션: ${isFoliageLoopActive ? 'ON' : 'OFF'}`;
    }
}

// 초기화
window.addEventListener('DOMContentLoaded', () => {
    selectClass("necro");
    switchView("side");
    setAnimation("idle");
    animInterval = setInterval(tickAnimationFrame, 100);

    // 지역별 고유 환경 오브젝트 4프레임 루프: 초당 약 7 FPS (142ms 간격)
    foliageLoopTimer = setInterval(tickFoliage4FrameLoop, 142);

    renderRegressionUi();
    renderUniqueItems();
    renderAllSkillsGallery();
    switchRegionTheme(1);
});
"""

js = js[:idx] + new_js_tail
with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated display.js with per-region 4-frame object overlays and removed cloud scroll.")
