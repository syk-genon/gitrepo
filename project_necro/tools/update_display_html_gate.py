# -*- coding: utf-8 -*-
import os

html_path = r"D:\workspace\GEMINI\project_necro\display.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

start_marker = "<!-- 섹션 4: 지역별 맞춤 [생존자 거점 마을 + 전투 전장 배경] 라이브 프리뷰 -->"
end_marker = "<!-- 회귀 실행 선택 모달 창 -->"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)
assert start_idx != -1 and end_idx != -1

new_section_html = """<!-- 섹션 4: 14대 작전 지역 [생존자 마을 거점 ➔ 6대 차원문(Gate) 진입 ➔ 6웨이브(84종 괴수) 실전 시뮬레이터] -->
    <section class="showcase-card">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px dashed var(--border-wood-light); padding-bottom: 8px; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <div>
                <span style="font-size: 1.25rem; color: var(--neon-gold);">🚪 14대 지역별 [마을 차원문(Gate) 진입 ➔ 6웨이브(84종 괴수) 전투] 시뮬레이터</span>
                <span id="currentRegionTitle" style="font-size: 0.85rem; color: var(--neon-cyan); margin-left: 10px;"></span>
            </div>
            <div style="display: flex; gap: 6px; align-items: center;">
                <span id="currentGateBadge" style="font-size: 0.75rem; padding: 3px 10px; border: 2px solid var(--neon-gold); background: rgba(0,0,0,0.8); color: var(--neon-gold);">🚪 철문 (Iron Gate)</span>
            </div>
        </div>

        <!-- 6대 차원문(Gate) 등급별 필터/요약 바 -->
        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; padding: 8px 10px; background: rgba(10, 7, 5, 0.75); border: 1px solid var(--border-wood);">
            <span style="font-size: 0.74rem; color: var(--neon-gold); align-self: center; margin-right: 4px;">🔑 차원문 등급 체계:</span>
            <span style="font-size: 0.7rem; color: #a8b4c4; padding: 2px 7px; border: 1px solid #a8b4c4; background: rgba(168,180,196,0.1);">🚪 철문 (1지역)</span>
            <span style="font-size: 0.7rem; color: #e69650; padding: 2px 7px; border: 1px solid #e69650; background: rgba(230,150,80,0.1);">🚪 동문 (3·5지역)</span>
            <span style="font-size: 0.7rem; color: #00f0ff; padding: 2px 7px; border: 1px solid #00f0ff; background: rgba(0,240,255,0.1);">🚪 은문 (2·4·6지역)</span>
            <span style="font-size: 0.7rem; color: #ffd000; padding: 2px 7px; border: 1px solid #ffd000; background: rgba(255,208,0,0.1);">🚪 금문 (7·8·11·13지역)</span>
            <span style="font-size: 0.7rem; color: #c850ff; padding: 2px 7px; border: 1px solid #c850ff; background: rgba(200,80,255,0.1);">🚪 플래티넘문 (9·10·12지역)</span>
            <span style="font-size: 0.7rem; color: #ff2a6d; padding: 2px 7px; border: 1px solid #ff2a6d; background: rgba(255,42,109,0.15);">🚪 다이아몬드문 (14지역 종언)</span>
        </div>

        <!-- 1~14지역 선택 칩스 -->
        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px;" id="regionSelectorTabs">
            <button class="btn-chip active" data-region="1" onclick="switchRegionTheme(1)">1. 서울 을지로 [철문]</button>
            <button class="btn-chip" data-region="2" onclick="switchRegionTheme(2)">2. 북한산 성역 [은문]</button>
            <button class="btn-chip" data-region="3" onclick="switchRegionTheme(3)">3. 인천항 부두 [동문]</button>
            <button class="btn-chip" data-region="4" onclick="switchRegionTheme(4)">4. 설악산 대청봉 [은문]</button>
            <button class="btn-chip" data-region="5" onclick="switchRegionTheme(5)">5. 평양 지하벙커 [동문]</button>
            <button class="btn-chip" data-region="6" onclick="switchRegionTheme(6)">6. 도쿄 음양사 [은문]</button>
            <button class="btn-chip" data-region="7" onclick="switchRegionTheme(7)">7. 마카오 불야성 [금문]</button>
            <button class="btn-chip" data-region="8" onclick="switchRegionTheme(8)">8. 블라디보스토크 [금문]</button>
            <button class="btn-chip" data-region="9" onclick="switchRegionTheme(9)">9. 태평양 해연 [플래티넘문]</button>
            <button class="btn-chip" data-region="10" onclick="switchRegionTheme(10)">10. 히말라야 묘지 [플래티넘문]</button>
            <button class="btn-chip" data-region="11" onclick="switchRegionTheme(11)">11. 시베리아·사막 [금문]</button>
            <button class="btn-chip" data-region="12" onclick="switchRegionTheme(12)">12. 라인강·로키산 [플래티넘문]</button>
            <button class="btn-chip" data-region="13" onclick="switchRegionTheme(13)">13. 성층권 모함 [금문]</button>
            <button class="btn-chip" data-region="14" onclick="switchRegionTheme(14)">14. 성층권 결전 [다이아몬드문]</button>
        </div>

        <!-- 선택된 문(Gate) 고유 환경 특성 & 획득 가능 신체 특성 & 드랍 보너스 정보창 -->
        <div class="hanji-card" style="margin-bottom: 14px; padding: 10px 14px; border-color: var(--border-brass);">
            <div style="display: grid; grid-template-columns: 1.3fr 1fr 1fr; gap: 12px; align-items: center;">
                <div>
                    <div style="font-size: 0.78rem; color: var(--neon-gold); margin-bottom: 3px;" id="gateFeatureTitle">🚪 차원문 특성 & 전장 배경 해설</div>
                    <div style="font-size: 0.72rem; color: var(--text-ivory); line-height: 1.35;" id="gateFeatureDesc"></div>
                </div>
                <div style="background: rgba(0,0,0,0.55); padding: 7px 10px; border-left: 3px solid var(--neon-green);">
                    <div style="font-size: 0.68rem; color: var(--text-muted);">🧬 해당 차원문 각성 특성 (Trait) & 환경 기믹</div>
                    <div style="font-size: 0.76rem; color: var(--neon-green); margin-top: 2px; font-weight: bold;" id="gateRegionTrait"></div>
                    <div style="font-size: 0.68rem; color: var(--neon-cyan); margin-top: 3px;" id="gateEnvModifier"></div>
                </div>
                <div style="background: rgba(0,0,0,0.55); padding: 7px 10px; border-left: 3px solid var(--neon-gold);">
                    <div style="font-size: 0.68rem; color: var(--text-muted);">🎁 차원문 등급 클리어 보상 배율</div>
                    <div style="font-size: 0.74rem; color: var(--neon-gold); margin-top: 2px;" id="gateDropBonus"></div>
                    <div style="font-size: 0.68rem; color: var(--neon-pink); margin-top: 3px;" id="gateBossSummary"></div>
                </div>
            </div>
        </div>

        <!-- 좌/우 듀얼 인터랙티브 스테이지: [좌: 생존자 거점 마을 & 차원문 입장] ➔ [우: 차원문 내부 6웨이브 전투 스테이지] -->
        <div style="display: grid; grid-template-columns: 1fr 1.25fr; gap: 16px;">
            <!-- 좌: 생존자 거점 마을 배경 + 영웅(정면 뷰) + 클릭 가능한 차원문(Gate) 오브젝트 -->
            <div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="townBgView">
                <!-- 상단 배지 -->
                <div style="position: absolute; top: 10px; left: 10px; background: rgba(10, 7, 5, 0.9); border: 2px solid var(--border-ink); padding: 4px 10px; font-size: 0.74rem; color: var(--neon-gold); z-index: 10;">
                    🏘️ 생존자 안전 거점 (정면 대기 뷰)
                </div>
                <div id="townStatusBadge" style="position: absolute; top: 10px; right: 10px; background: rgba(0, 255, 170, 0.18); border: 1px solid var(--neon-green); padding: 3px 8px; font-size: 0.68rem; color: var(--neon-green); z-index: 10;">
                    🟢 마을 대기 중 (문을 클릭해 입장)
                </div>

                <!-- 마을 내 영웅 아바타 (정면/대기 도트) -->
                <div id="townHeroActor" style="position: absolute; bottom: 18px; left: 36px; width: 110px; height: 110px; transition: all 0.55s cubic-bezier(0.25, 1, 0.5, 1); z-index: 8; text-align: center;">
                    <img id="townHeroImg" src="assets/agents/agent_male_nemesis.png" style="width: 96px; height: 96px; object-fit: contain; image-rendering: pixelated; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.9));">
                    <div style="font-size: 0.65rem; color: #fff; background: rgba(0,0,0,0.8); border: 1px solid var(--neon-gold); padding: 1px 5px; display: inline-block; margin-top: -6px;">사령군주 (마을)</div>
                </div>

                <!-- 우측 차원문(Gate) 클릭 오브젝트 -->
                <div id="townGatePortalObj" onclick="enterRegionGate()" title="클릭하여 차원문 내부 던전으로 진입!" style="position: absolute; bottom: 14px; right: 26px; width: 145px; height: 175px; cursor: pointer; z-index: 9; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; transition: transform 0.2s;">
                    <div id="townGateGlow" style="position: absolute; inset: 10px; border-radius: 50%; filter: blur(16px); opacity: 0.65; pointer-events: none;"></div>
                    <img id="townGateSprite" src="assets/ui/gates/gate_iron.png" style="width: 135px; height: 150px; object-fit: contain; image-rendering: pixelated; position: relative; z-index: 2; animation: minionBob 1.6s ease-in-out infinite alternate;">
                    <button class="btn-chip" id="btnEnterGateAction" style="position: relative; z-index: 3; margin-top: -6px; font-size: 0.7rem; padding: 3px 10px; background: #120b07; color: var(--neon-gold); border-color: var(--neon-gold); box-shadow: 0 0 12px rgba(255, 208, 0, 0.6);">
                        🚪 차원문 진입 ▶
                    </button>
                </div>
            </div>

            <!-- 우: 차원문 내부 전투 전장 배경 + 6웨이브 진행 바 + 영웅(우향) vs 지역 고유 괴수(좌향 scaleX(-1)) -->
            <div style="height: 290px; border: 3px solid var(--border-ink); position: relative; background-size: cover; background-position: center; image-rendering: pixelated; overflow: hidden;" id="battleBgView">
                <!-- 차원문 워프 플래시 오버레이 -->
                <div id="gatePortalFlashOverlay" style="position: absolute; inset: 0; background: radial-gradient(circle, rgba(0,240,255,0.85), rgba(0,0,0,0.95)); opacity: 0; pointer-events: none; transition: opacity 0.35s; z-index: 30; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.15rem; text-shadow: 0 0 12px var(--neon-cyan);">
                    🌀 차원문 워프 진입 중...
                </div>

                <!-- 상단 웨이브 헤더 및 컨트롤 -->
                <div style="position: absolute; top: 8px; left: 10px; right: 10px; display: flex; justify-content: space-between; align-items: center; z-index: 15;">
                    <div style="background: rgba(10, 7, 5, 0.9); border: 2px solid var(--border-ink); padding: 4px 10px; font-size: 0.74rem; color: var(--neon-pink);">
                        ⚔️ <span id="battleStageWaveBadge">WAVE 1/6 (일반 괴수)</span> : <strong id="battleBossName" style="color: var(--neon-gold);"></strong>
                    </div>
                    <div style="display: flex; gap: 4px;">
                        <button class="btn-chip" style="font-size: 0.66rem; padding: 3px 8px; color: var(--neon-green); border-color: var(--neon-green);" onclick="attackGateWaveMonster()">⚡ 타격/스킬 처치</button>
                        <button class="btn-chip" style="font-size: 0.66rem; padding: 3px 8px; color: var(--neon-cyan); border-color: var(--neon-cyan);" onclick="nextGateWave()">⏭️ 다음 웨이브</button>
                        <button class="btn-chip" style="font-size: 0.66rem; padding: 3px 8px; color: var(--text-muted);" onclick="returnToTownFromGate()">🏘️ 마을 귀환</button>
                    </div>
                </div>

                <!-- 웨이브 1~6 단계 선택 미니 탭 -->
                <div id="gateWaveStepsBar" style="position: absolute; top: 42px; left: 10px; display: flex; gap: 4px; z-index: 15;">
                    <button class="btn-chip active" data-wave="1" style="font-size:0.62rem; padding:2px 6px;" onclick="setGateWave(1)">W1.척후</button>
                    <button class="btn-chip" data-wave="2" style="font-size:0.62rem; padding:2px 6px;" onclick="setGateWave(2)">W2.주력</button>
                    <button class="btn-chip" data-wave="3" style="font-size:0.62rem; padding:2px 6px;" onclick="setGateWave(3)">W3.강습</button>
                    <button class="btn-chip" data-wave="4" style="font-size:0.62rem; padding:2px 6px;" onclick="setGateWave(4)">W4.정예</button>
                    <button class="btn-chip" data-wave="5" style="font-size:0.62rem; padding:2px 6px; color:var(--neon-cyan);" onclick="setGateWave(5)">W5.수문장</button>
                    <button class="btn-chip" data-wave="6" style="font-size:0.62rem; padding:2px 6px; color:var(--neon-pink);" onclick="setGateWave(6)">W6.보스</button>
                </div>

                <!-- 좌측: 차원문 진입 완료 영웅(우향 Facing Right) & 입구 포털 잔상 -->
                <div id="battleHeroPartyBox" style="position: absolute; bottom: 16px; left: 22px; display: flex; align-items: flex-end; gap: 6px; z-index: 12; opacity: 0.45; transition: all 0.35s;">
                    <img id="battleEntranceGateMini" src="assets/ui/gates/gate_iron.png" style="width: 64px; height: 74px; object-fit: contain; image-rendering: pixelated; opacity: 0.85;">
                    <div style="text-align: center;">
                        <img id="battleHeroSpriteImg" src="assets/agents/agent_male_nemesis.png" style="width: 105px; height: 105px; object-fit: contain; image-rendering: pixelated; transform: scaleX(1); filter: drop-shadow(0 0 10px rgba(0,255,170,0.6));">
                        <div id="battleHeroStatusTag" style="font-size: 0.62rem; background: rgba(0,0,0,0.85); color: var(--neon-green); border: 1px solid var(--neon-green); padding: 1px 5px;">차원문 입장 대기</div>
                    </div>
                </div>

                <!-- 중앙: 전투 VFX 폭발 레이어 -->
                <div id="gateBattleVfxLayer" style="position: absolute; inset: 0; pointer-events: none; z-index: 20;"></div>

                <!-- 우측: 해당 차원문 웨이브 몬스터 (좌향 scaleX(-1)) + 체력바 -->
                <div id="battleMonsterContainer" style="position: absolute; bottom: 16px; right: 32px; display: flex; flex-direction: column; align-items: center; z-index: 14;">
                    <div style="background: rgba(10,7,5,0.9); border: 1px solid var(--border-ink); padding: 2px 8px; margin-bottom: 4px; text-align: center; min-width: 145px;">
                        <div id="battleMonsterRoleTag" style="font-size: 0.62rem; color: var(--neon-cyan);">WAVE 1 · 지역 고유 괴수</div>
                        <div style="width: 100%; height: 8px; background: #220a0a; border: 1px solid #000; margin-top: 2px; overflow: hidden;">
                            <div id="battleMonsterHpBar" style="width: 100%; height: 100%; background: linear-gradient(90deg, #ff2a6d, #ffcc00); transition: width 0.2s;"></div>
                        </div>
                        <div id="battleMonsterHpText" style="font-size: 0.6rem; color: #fff; margin-top: 1px;">HP: 100%</div>
                    </div>
                    <div id="battleBossSprite" onclick="attackGateWaveMonster()" title="클릭하여 몬스터 타격!" style="width: 138px; height: 138px; cursor: pointer; background-repeat: no-repeat; background-position: center bottom; background-size: contain; transform: scaleX(-1); image-rendering: pixelated; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.9)); transition: transform 0.15s, filter 0.15s;"></div>
                </div>

                <!-- 하단 전투 로그 바 -->
                <div id="gateBattleLogBar" style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(8, 6, 4, 0.88); border-top: 1px solid var(--border-wood); padding: 4px 10px; font-size: 0.68rem; color: var(--neon-gold); z-index: 18;">
                    ▶ 좌측 마을 화면의 [🚪 차원문]을 클릭하면 영웅이 문을 통과해 6웨이브 던전 전투에 돌입합니다!
                </div>
            </div>
        </div>

        <!-- 해당 차원문(지역) 출현 6종 고유 몬스터 패밀리 도감 (일반 4종 + 5웨이브 수문장 + 6웨이브 보스) -->
        <div style="margin-top: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.86rem; color: var(--neon-gold);">👾 현재 차원문 출현 괴수 라인업 (클릭 시 해당 웨이브 즉시 스폰 · 전 14개 지역 × 6종 = 84종 고유 도트):</span>
                <span style="font-size: 0.72rem; color: var(--neon-cyan);" id="regionRosterSummary">Wave 1~4 일반 괴수 · Wave 5 수문장 · Wave 6 보스</span>
            </div>
            <div id="regionMonstersRosterGrid" style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px;"></div>
        </div>
    </section>

    """

updated_html = html[:start_idx] + new_section_html + html[end_idx:]
with open(html_path, "w", encoding="utf-8") as f:
    f.write(updated_html)
print("Successfully updated Section 4 in display.html")
