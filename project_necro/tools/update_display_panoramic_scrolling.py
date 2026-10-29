# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

HTML_PATH = r"D:\workspace\GEMINI\project_necro\display.html"
JS_PATH = r"D:\workspace\GEMINI\project_necro\display.js"

# 1. Update display.html for smooth 2400px panoramic battle scrolling
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Update battleBgView style to support 2400px width with smooth transition
old_battle_box = '<div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="battleBgView">'
new_battle_box = '<div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: 2400px 100%; background-position: 0% center; background-repeat: no-repeat; image-rendering: pixelated; overflow: hidden; transition: background-position 0.95s cubic-bezier(0.22, 1, 0.36, 1);" id="battleBgView">'

if old_battle_box in html:
    html = html.replace(old_battle_box, new_battle_box, 1)

# Update battleFoliageLayer to also scroll in parallax across the 2400px strip
old_battle_fol = 'id="battleFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/region_obj_1_f0.png?v=4\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4; animation: propSmoothFloat 1.8s ease-in-out infinite alternate;"'
new_battle_fol = 'id="battleFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/nature_props_pano_1.png?v=5\'); background-size: 2400px 100%; background-position: 0% center; background-repeat: no-repeat; image-rendering: pixelated; pointer-events: none; z-index: 4; transition: background-position 0.95s cubic-bezier(0.22, 1, 0.36, 1); animation: propSmoothFloat 1.8s ease-in-out infinite alternate;"'

if old_battle_fol in html:
    html = html.replace(old_battle_fol, new_battle_fol, 1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated display.html with 2400px panoramic battle background and parallax layer.")


# 2. Update display.js to scroll background with each wave (W1 -> W6)
with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()

# Update switchRegionTheme to load battle_pano_${rId}.png and nature_props_pano_${rId}.png
old_switch_battle = """    const battleView = document.getElementById('battleBgView');
    if (battleView) {
        battleView.style.backgroundImage = `url('assets/ui/regions/battle_bg_${rId}_f${fIdx}.png?v=4')`;
    }"""

new_switch_battle = """    const battleView = document.getElementById('battleBgView');
    if (battleView) {
        battleView.style.backgroundImage = `url('assets/ui/regions/battle_pano_${rId}.png?v=5')`;
    }"""

if old_switch_battle in js:
    js = js.replace(old_switch_battle, new_switch_battle, 1)

old_battle_fol_js = """    const battleFol = document.getElementById('battleFoliageLayer');
    if (battleFol) battleFol.style.backgroundImage = overlayUrl;"""

new_battle_fol_js = """    const battleFol = document.getElementById('battleFoliageLayer');
    if (battleFol) battleFol.style.backgroundImage = `url('assets/ui/regions/nature_props_pano_${rId}.png?v=5')`;"""

if old_battle_fol_js in js:
    js = js.replace(old_battle_fol_js, new_battle_fol_js, 1)

# In setGateWave(waveNum): add panoramic scroll calculation
old_set_wave_end = """    updateGateWaveHpUI();
    renderRegionMonstersRoster(currentRegionId);
}"""

new_set_wave_end = """    updateGateWaveHpUI();
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

if old_set_wave_end in js:
    js = js.replace(old_set_wave_end, new_set_wave_end, 1)

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated display.js with 6-wave panoramic camera scrolling.")
