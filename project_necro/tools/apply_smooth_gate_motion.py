# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

HTML_PATH = r"D:\workspace\GEMINI\project_necro\display.html"
JS_PATH = r"D:\workspace\GEMINI\project_necro\display.js"

# 1. Update display.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Add @keyframes propSmoothFloat
if "@keyframes propSmoothFloat" not in html:
    keyframe_def = """        @keyframes propSmoothFloat {
            0% { transform: translateY(0); }
            100% { transform: translateY(-3.5px); }
        }

        @keyframes minionBob {"""
    html = html.replace("        @keyframes minionBob {", keyframe_def, 1)

# Apply animation: propSmoothFloat 1.8s ease-in-out infinite alternate to the 3 foliage layer divs
html = html.replace(
    'id="studioFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/foliage_overlay_f0.png?v=3\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 3;"',
    'id="studioFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/region_obj_1_f0.png?v=4\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 3; animation: propSmoothFloat 1.8s ease-in-out infinite alternate;"'
)

html = html.replace(
    'id="townFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/foliage_overlay_f0.png?v=3\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4;"',
    'id="townFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/region_obj_1_f0.png?v=4\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4; animation: propSmoothFloat 1.8s ease-in-out infinite alternate;"'
)

html = html.replace(
    'id="battleFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/foliage_overlay_f0.png?v=3\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4;"',
    'id="battleFoliageLayer" style="position: absolute; inset: 0; background-image: url(\'assets/ui/regions/region_obj_1_f0.png?v=4\'); background-size: 100% 100%; image-rendering: pixelated; pointer-events: none; z-index: 4; animation: propSmoothFloat 1.8s ease-in-out infinite alternate;"'
)

# Also update status bar description to highlight the smooth Silver Gate-style motion
html = html.replace(
    '🌿 지역 고유 오브젝트 4프레임 모션: ON',
    '🌿 은문 스타일 부드러운 유영(Float) 모션: ON'
)
html = html.replace(
    '🌿 지역 고유 오브젝트 4프레임 모션: OFF',
    '🌿 은문 스타일 부드러운 유영(Float) 모션: OFF'
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated display.html with propSmoothFloat keyframes and smooth CSS animation.")


# 2. Update display.js
with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()

# Slow down foliageLoopTimer from 142ms to 260ms for relaxed, smooth pacing
js = js.replace("foliageLoopTimer = setInterval(tickFoliage4FrameLoop, 142);", "foliageLoopTimer = setInterval(tickFoliage4FrameLoop, 260);")

# Update cache buster to v=4
js = js.replace("?v=3", "?v=4")

# Update toggle button label text in JS toggle function
js = js.replace(
    "btn.textContent = `🌿 지역 고유 오브젝트 4프레임 모션: ${isFoliageLoopActive ? 'ON' : 'OFF'}`;",
    "btn.textContent = `🌿 은문 스타일 부드러운 유영(Float) 모션: ${isFoliageLoopActive ? 'ON' : 'OFF'}`;",
)

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated display.js with 260ms pacing and ?v=4 cache buster.")
