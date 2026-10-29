# -*- coding: utf-8 -*-
with open("D:/workspace/GEMINI/project_necro/display.html", "r", encoding="utf-8") as f:
    c = f.read()

target = "<p>1단계: 12대 직업 16비트 도트 캐릭터 스튜디오 · 전 스킬 16비트 VFX · 96종 세트/고유 아이템 · 회귀 영혼 각인 시뮬레이터</p>"
replacement = target + """\n        <div style="margin-top: 10px;">
            <a href="index.html" class="btn-chip" style="text-decoration: none; color: var(--neon-gold); border-color: var(--neon-gold); font-size: 0.95rem; padding: 6px 20px; box-shadow: 0 0 16px rgba(255, 208, 0, 0.6); display: inline-block;">
                🎮 2D 도트 RPG 본 게임 플레이 (PLAY GAME) ▶
            </a>
        </div>"""

if target in c:
    c = c.replace(target, replacement, 1)
    with open("D:/workspace/GEMINI/project_necro/display.html", "w", encoding="utf-8") as f:
        f.write(c)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")
