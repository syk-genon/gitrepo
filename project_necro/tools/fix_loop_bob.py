with open('project_necro/display.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_loop_code = """    // 4프레임 주기마다 전투장 몬스터와 영웅도 고전 16비트 특유의 2~4프레임 대기 호흡 연출
    const bossSprite = document.getElementById('battleBossSprite');
    if (bossSprite) {
        const bobY = (bgFoliageFrameIdx === 1 || bgFoliageFrameIdx === 2) ? -3 : 0;
        bossSprite.style.transform = `scaleX(-1) translateY(${bobY}px)`;
    }"""

new_loop_code = """    // 4프레임 주기마다 전투장 몬스터와 영웅도 고전 16비트 특유의 대기 호흡 연출
    const bossSprite = document.getElementById('battleBossSprite');
    if (bossSprite) {
        const meta = getWaveMonsterMeta(currentRegionId, currentGateWave);
        if (!meta.isFlying) {
            // 지상 몬스터: 발바닥을 바닥에 완벽히 고정한 채 미세한 호흡(Breathing) 연출 (붕 뜸 원천 차단)
            const breathScale = (bgFoliageFrameIdx % 2 === 1) ? 1.015 : 1.0;
            bossSprite.style.transformOrigin = 'bottom center';
            bossSprite.style.transform = `scaleX(-1) scaleY(${breathScale})`;
        }
    }"""

if old_loop_code in code:
    code = code.replace(old_loop_code, new_loop_code)
    with open('project_necro/display.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully updated tickFoliage4FrameLoop with zero-lift breathing!")
else:
    print("Warning: old_loop_code snippet not matched, checking...")
