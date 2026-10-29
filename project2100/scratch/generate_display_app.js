const fs = require('fs');

const displayHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT 2100 - 통합 아케이드 전시 & 특성 시뮬레이터</title>
    <link rel="stylesheet" href="index.css">
    <style>
        /* Showcase Dedicated Styles */
        :root {
            --bg-deep: #07090e;
            --bg-card: #0d121d;
            --bg-card-hover: #141c2c;
            --border-neon: #1e293b;
            --neon-cyan: #00f0ff;
            --neon-pink: #ff2a6d;
            --neon-green: #05ffa1;
            --neon-gold: #facc15;
            --neon-purple: #b026ff;
        }

        body.showcase-body {
            background-color: var(--bg-deep);
            color: #e2e8f0;
            font-family: 'Pretendard', 'NeoDunggeunmo', -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(0, 240, 255, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 85% 60%, rgba(255, 42, 109, 0.04) 0%, transparent 50%),
                linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 24px 24px, 24px 24px;
        }

        /* Top Nav Header */
        .showcase-header {
            background: rgba(11, 15, 25, 0.95);
            border-bottom: 2px solid #1e293b;
            padding: 16px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(8px);
        }

        .showcase-title-group h1 {
            margin: 0;
            font-size: 1.35rem;
            color: var(--neon-cyan);
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 12px rgba(0, 240, 255, 0.5);
        }

        .showcase-title-group p {
            margin: 4px 0 0 0;
            font-size: 0.78rem;
            color: #94a3b8;
        }

        .showcase-header-nav {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-nav-tab {
            background: #141c2c;
            border: 1px solid #334155;
            color: #cbd5e1;
            padding: 7px 14px;
            font-size: 0.78rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-nav-tab:hover, .btn-nav-tab.active {
            background: #1e293b;
            color: var(--neon-cyan);
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        }

        .btn-play-game {
            background: linear-gradient(135deg, #0ea5e9, #6366f1);
            color: white !important;
            font-weight: bold;
            border: none;
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
        }

        /* Container Layout */
        .showcase-container {
            max-width: 1540px;
            margin: 24px auto;
            padding: 0 20px;
            display: flex;
            flex-direction: column;
            gap: 28px;
        }

        /* Section Card */
        .showcase-card {
            background: var(--bg-card);
            border: 1px solid var(--border-neon);
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid #1e293b;
        }

        .section-title {
            margin: 0;
            font-size: 1.15rem;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-title span.badge-num {
            background: var(--neon-cyan);
            color: #050811;
            font-size: 0.75rem;
            font-weight: 900;
            padding: 2px 8px;
            border-radius: 4px;
        }

        /* Studio Split Grid */
        .studio-grid {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 24px;
            align-items: start;
        }

        @media (max-width: 1024px) {
            .studio-grid { grid-template-columns: 1fr; }
        }

        /* Hero Stage (CRT Box) */
        .hero-stage-wrapper {
            background: #05070c;
            border: 2px solid #253349;
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 240, 255, 0.1);
        }

        .crt-scanlines {
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            pointer-events: none;
            border-radius: 10px;
            z-index: 10;
        }

        .hero-avatar-box-large {
            width: 240px;
            height: 240px;
            position: relative;
            margin: 10px 0;
            image-rendering: pixelated;
        }

        .stage-badge-status {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid #334155;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.72rem;
            color: var(--neon-cyan);
            margin-bottom: 8px;
            font-family: monospace;
            z-index: 12;
        }

        /* Animation Playback Controller */
        .stage-playback-bar {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #0c121e;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 8px 12px;
            margin-top: 12px;
            gap: 8px;
            z-index: 12;
        }

        .btn-ctrl {
            background: #1e293b;
            border: 1px solid #475569;
            color: #f1f5f9;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-ctrl:hover {
            background: #334155;
            color: var(--neon-cyan);
            border-color: var(--neon-cyan);
        }

        .frame-indicator {
            font-family: monospace;
            font-size: 0.75rem;
            color: #94a3b8;
        }

        /* Studio Controls Panel */
        .studio-controls-panel {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .control-group-title {
            font-size: 0.82rem;
            font-weight: 700;
            color: #94a3b8;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .chip-buttons-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .btn-chip {
            background: #0f172a;
            border: 1px solid #334155;
            color: #cbd5e1;
            padding: 7px 12px;
            font-size: 0.76rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .btn-chip:hover {
            background: #1e293b;
            border-color: #64748b;
        }

        .btn-chip.active {
            background: rgba(0, 240, 255, 0.15);
            border-color: var(--neon-cyan);
            color: var(--neon-cyan);
            font-weight: 700;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
        }

        /* 13 Mutations Checkbox Grid */
        .mutation-toggles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 8px;
            margin-top: 6px;
        }

        .mutation-chk-item {
            background: #0b111c;
            border: 1px solid #1e293b;
            padding: 6px 10px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.74rem;
            cursor: pointer;
            transition: all 0.15s;
            user-select: none;
        }

        .mutation-chk-item:hover {
            border-color: #475569;
            background: #121927;
        }

        .mutation-chk-item.checked {
            border-color: var(--neon-cyan);
            background: rgba(0, 240, 255, 0.08);
            color: #e0f2fe;
        }

        .mutation-chk-item input {
            cursor: pointer;
            accent-color: var(--neon-cyan);
        }

        /* Simulator Section (Slots & Synergy) */
        .simulator-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }

        @media (max-width: 1024px) {
            .simulator-layout { grid-template-columns: 1fr; }
        }

        .slots-display-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }

        .slot-display-box {
            background: #080d17;
            border: 2px dashed #223249;
            border-radius: 10px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 120px;
            text-align: center;
            position: relative;
            transition: all 0.2s;
        }

        .slot-display-box.unlocked {
            border-style: solid;
            border-color: #334155;
            background: #0d1524;
        }

        .slot-display-box.equipped {
            border-color: var(--neon-cyan);
            background: rgba(0, 240, 255, 0.05);
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
        }

        .slot-badge-num {
            position: absolute;
            top: 8px;
            left: 8px;
            font-size: 0.65rem;
            color: #64748b;
            font-weight: 700;
        }

        .slot-btn-toggle {
            position: absolute;
            top: 6px;
            right: 6px;
            background: #1e293b;
            border: 1px solid #475569;
            color: #94a3b8;
            font-size: 0.65rem;
            padding: 2px 6px;
            border-radius: 4px;
            cursor: pointer;
        }

        .slot-btn-toggle:hover {
            color: white;
            border-color: var(--neon-cyan);
        }

        .slot-content-name {
            font-size: 0.92rem;
            font-weight: 800;
            color: #f8fafc;
            margin-top: 10px;
        }

        .slot-content-part {
            font-size: 0.72rem;
            color: var(--neon-cyan);
            margin-top: 4px;
        }

        .slot-btn-unequip {
            margin-top: 8px;
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid #ef4444;
            color: #fca5a5;
            padding: 3px 8px;
            font-size: 0.68rem;
            border-radius: 4px;
            cursor: pointer;
        }

        .slot-btn-unequip:hover {
            background: #ef4444;
            color: white;
        }

        /* Active Synergies Box */
        .synergy-banner-box {
            background: #090e18;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .synergy-header {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--neon-gold);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .fusion-active-card {
            background: #111a2c;
            border: 1px solid var(--neon-cyan);
            border-radius: 8px;
            padding: 12px 14px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
            animation: glow-pulse 3s infinite alternate;
        }

        .fusion-active-card.double-fusion-2 {
            border-color: var(--neon-purple);
            box-shadow: 0 0 15px rgba(176, 38, 255, 0.25);
        }

        @keyframes glow-pulse {
            0% { box-shadow: 0 0 10px rgba(0, 240, 255, 0.15); }
            100% { box-shadow: 0 0 20px rgba(0, 240, 255, 0.35); }
        }

        .fusion-card-title {
            font-size: 0.92rem;
            font-weight: 800;
            color: #38bdf8;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 4px;
        }

        .fusion-req-tags {
            font-size: 0.7rem;
            color: #94a3b8;
            display: flex;
            gap: 6px;
            align-items: center;
            margin-bottom: 6px;
        }

        .fusion-card-desc {
            font-size: 0.78rem;
            color: #cbd5e1;
            line-height: 1.4;
        }

        /* 13 Traits Palette */
        .traits-palette-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 8px;
        }

        .trait-chip-card {
            background: #0e1524;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 10px 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            user-select: none;
        }

        .trait-chip-card:hover {
            border-color: #64748b;
            background: #141e33;
            transform: translateY(-2px);
        }

        .trait-chip-card.slotted {
            border-color: var(--neon-cyan);
            background: rgba(0, 240, 255, 0.12);
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.2);
        }

        .trait-chip-name {
            font-size: 0.82rem;
            font-weight: 700;
            color: #f1f5f9;
            margin: 4px 0 2px 0;
        }

        .trait-chip-part {
            font-size: 0.65rem;
            color: #38bdf8;
        }

        .trait-chip-cat {
            font-size: 0.6rem;
            color: #94a3b8;
            background: #1e293b;
            padding: 1px 6px;
            border-radius: 4px;
            margin-bottom: 4px;
        }

        /* 78 Fusions Matrix Section */
        .fusions-filter-bar {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }

        .search-box-wrapper {
            position: relative;
            min-width: 280px;
        }

        .search-input {
            width: 100%;
            background: #090e18;
            border: 1px solid #334155;
            color: #f1f5f9;
            padding: 8px 12px 8px 34px;
            border-radius: 6px;
            font-size: 0.82rem;
            outline: none;
            box-sizing: border-box;
        }

        .search-input:focus {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        }

        .search-icon {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
            font-size: 0.85rem;
        }

        .fusions-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 14px;
            max-height: 640px;
            overflow-y: auto;
            padding-right: 6px;
        }

        /* Custom scrollbar */
        .fusions-cards-grid::-webkit-scrollbar { width: 6px; }
        .fusions-cards-grid::-webkit-scrollbar-track { background: #070a12; }
        .fusions-cards-grid::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        .fusions-cards-grid::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

        .fusion-catalog-card {
            background: #0c1322;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s;
        }

        .fusion-catalog-card:hover {
            border-color: #475569;
            background: #111a2d;
            transform: translateY(-2px);
        }

        .fusion-catalog-card.active-match {
            border-color: var(--neon-cyan);
            background: rgba(0, 240, 255, 0.08);
            box-shadow: 0 0 14px rgba(0, 240, 255, 0.25);
        }

        .btn-test-fusion {
            margin-top: 10px;
            background: #141f35;
            border: 1px solid #2e4369;
            color: #38bdf8;
            padding: 6px 12px;
            font-size: 0.74rem;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.15s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .btn-test-fusion:hover {
            background: var(--neon-cyan);
            color: #030712;
            font-weight: 700;
            border-color: var(--neon-cyan);
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
        }

        /* Monster Gallery & Tester Section */
        .monster-showcase-grid {
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 24px;
        }

        @media (max-width: 900px) {
            .monster-showcase-grid { grid-template-columns: 1fr; }
        }

        .monster-test-stage {
            background: #05070c;
            border: 2px solid #253349;
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }

        .monster-sprite-preview-box {
            width: 140px;
            height: 140px;
            margin: 16px 0;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center bottom;
            image-rendering: pixelated;
            transform: scaleX(-1); /* monsters face left towards hero */
        }

        .monster-gallery-scroll {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 10px;
            max-height: 480px;
            overflow-y: auto;
            padding-right: 6px;
        }

        .monster-card-thumb {
            background: #0c1322;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 10px 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .monster-card-thumb:hover, .monster-card-thumb.selected {
            border-color: var(--neon-pink);
            background: rgba(255, 42, 109, 0.1);
            transform: translateY(-2px);
        }

        .monster-thumb-img {
            width: 64px;
            height: 64px;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center bottom;
            image-rendering: pixelated;
            margin-bottom: 6px;
            transform: scaleX(-1); /* Face left */
        }

        .clean-badge {
            background: #10b981;
            color: #022c22;
            font-size: 0.6rem;
            font-weight: 800;
            padding: 1px 6px;
            border-radius: 3px;
            margin-top: 2px;
        }
    </style>
</head>
<body class="showcase-body">

    <!-- Top Navigation Header -->
    <header class="showcase-header">
        <div class="showcase-title-group">
            <h1>🎮 PROJECT 2100: MASTER DISPLAY & SIMULATOR</h1>
            <p>영웅 4대 액션 · 13대 고유 신체 변이 파츠 · 78대 초월 2중 융합 매트릭스 · 괴수 갤러리 통합 제어 센터</p>
        </div>
        <div class="showcase-header-nav">
            <a href="#section-hero" class="btn-nav-tab active">👤 영웅 스튜디오</a>
            <a href="#section-slots" class="btn-nav-tab">⚡ 특성 & 시너지</a>
            <a href="#section-fusions" class="btn-nav-tab">📖 78대 융합 브라우저</a>
            <a href="#section-monsters" class="btn-nav-tab">👾 괴수 모션 갤러리</a>
            <a href="index.html" class="btn-nav-tab btn-play-game">▶ 게임 실행</a>
        </div>
    </header>

    <div class="showcase-container">

        <!-- ========================================== -->
        <!-- SECTION 1: 영웅 & 페이퍼돌 스튜디오 -->
        <!-- ========================================== -->
        <section class="showcase-card" id="section-hero">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="badge-num">01</span>
                    영웅 비주얼 & DNF 스켈레탈 4대 액션 페이퍼돌 스튜디오
                </h2>
                <span style="font-size: 0.8rem; color: #94a3b8;">무기 미착용 순수 베이스 + 독립 무기/방어구/13대 변이 파츠 오버레이</span>
            </div>

            <div class="studio-grid">
                <!-- 좌측: 대형 CRT 아바타 스테이지 -->
                <div class="hero-stage-wrapper">
                    <div class="crt-scanlines"></div>
                    <div class="stage-badge-status" id="stageStatusBadge">MALE | IDLE | FRAME 0/4</div>

                    <div class="hero-avatar-box-large" id="displayAvatarContainer">
                        <!-- 오라 이펙트 (2개 이상 장착 시 발동) -->
                        <div class="character-aura-effect" id="disp-layer-aura"></div>

                        <!-- 13대 돌연변이 파츠 레이어 (Z-Index 배치) -->
                        <div class="pixel-paperdoll-layer layer-wings" id="disp-layer-wings"></div>
                        <div class="pixel-paperdoll-layer layer-fairy_wings" id="disp-layer-fairy_wings"></div>
                        <div class="pixel-paperdoll-layer layer-tail" id="disp-layer-tail"></div>
                        <div class="pixel-paperdoll-layer layer-booster" id="disp-layer-booster"></div>
                        <div class="pixel-paperdoll-layer layer-shell" id="disp-layer-shell"></div>
                        <div class="pixel-paperdoll-layer layer-crystals" id="disp-layer-crystals"></div>
                        <div class="pixel-paperdoll-layer layer-body" id="disp-layer-body"></div>
                        <div class="pixel-paperdoll-layer layer-armor" id="disp-layer-armor"></div>
                        <div class="pixel-paperdoll-layer layer-core" id="disp-layer-core"></div>
                        <div class="pixel-paperdoll-layer layer-horns" id="disp-layer-horns"></div>
                        <div class="pixel-paperdoll-layer layer-spikes" id="disp-layer-spikes"></div>
                        <div class="pixel-paperdoll-layer layer-visor" id="disp-layer-visor"></div>
                        <div class="pixel-paperdoll-layer layer-antennae" id="disp-layer-antennae"></div>
                        <div class="pixel-paperdoll-layer layer-halo" id="disp-layer-halo"></div>
                        <div class="pixel-paperdoll-layer layer-claws" id="disp-layer-claws"></div>
                        <div class="pixel-paperdoll-layer layer-weapon" id="disp-layer-weapon"></div>
                        <div class="pixel-paperdoll-layer layer-vfx" id="disp-layer-vfx"></div>
                    </div>

                    <!-- 애니메이션 재생 제어바 -->
                    <div class="stage-playback-bar">
                        <button class="btn-ctrl" id="btnPlayPause">⏸ 일시정지</button>
                        <button class="btn-ctrl" id="btnStepFrame">⏭ 1프레임</button>
                        <span class="frame-indicator" id="playbackSpeedText">속도: 1.0x</span>
                        <div style="display:flex; gap:4px;">
                            <button class="btn-ctrl speed-btn" data-speed="0.5">0.5x</button>
                            <button class="btn-ctrl speed-btn active" data-speed="1.0">1.0x</button>
                            <button class="btn-ctrl speed-btn" data-speed="2.0">2.0x</button>
                        </div>
                    </div>
                </div>

                <!-- 우측: 컨트롤 패널 -->
                <div class="studio-controls-panel">
                    <!-- 성별 & 액션 모션 -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div>
                            <div class="control-group-title">👤 요원 성별 (Gender)</div>
                            <div class="chip-buttons-row">
                                <button class="btn-chip active" id="btnGenderMale" data-gender="male">👦 남성 요원 (Male)</button>
                                <button class="btn-chip" id="btnGenderFemale" data-gender="female">👧 여성 요원 (Female)</button>
                            </div>
                        </div>
                        <div>
                            <div class="control-group-title">🎬 액션 모션 (Skeletal Motions)</div>
                            <div class="chip-buttons-row">
                                <button class="btn-chip active" data-motion="idle">대기 (Idle - 4F)</button>
                                <button class="btn-chip" data-motion="run">달리기 (Run - 6F)</button>
                                <button class="btn-chip" data-motion="attack">공격 돌진 (Attack - 4F)</button>
                                <button class="btn-chip" data-motion="skill">필살 스킬 (Skill - 4F)</button>
                            </div>
                        </div>
                    </div>

                    <!-- 무기 & 방어구 오버레이 -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div>
                            <div class="control-group-title">⚔️ 장착 무기 (Weapon Layer)</div>
                            <div class="chip-buttons-row" id="weaponSelectorRow">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                        <div>
                            <div class="control-group-title">🛡️ 장착 방어구 (Armor Layer)</div>
                            <div class="chip-buttons-row" id="armorSelectorRow">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                    </div>

                    <!-- 오라 효과 제어 -->
                    <div>
                        <div class="control-group-title">✨ 특성 발현 오라 제어 (Aura Effect)</div>
                        <div class="chip-buttons-row">
                            <button class="btn-chip active" data-aura="auto">🔄 자동 (장착 슬롯 수 연동)</button>
                            <button class="btn-chip" data-aura="0">OFF (오라 끄기)</button>
                            <button class="btn-chip" data-aura="1">Stage 1: 청록 방사능 스월 (2특성)</button>
                            <button class="btn-chip" data-aura="2">Stage 2: 진홍 코스믹 폭주 (3특성)</button>
                        </div>
                    </div>

                    <!-- 13대 고유 신체 변이 파츠 수동 토글 -->
                    <div>
                        <div class="control-group-title" style="justify-content: space-between;">
                            <span>🧬 13대 고유 신체 변이 파츠 (13 Mutation Parts)</span>
                            <div style="display: flex; gap: 6px;">
                                <button class="btn-ctrl" id="btnSyncPartsWithSlots">🔄 슬롯 동기화</button>
                                <button class="btn-ctrl" id="btnAllPartsOn">전체 켜기</button>
                                <button class="btn-ctrl" id="btnAllPartsOff">전체 끄기</button>
                            </div>
                        </div>
                        <div class="mutation-toggles-grid" id="mutationsToggleGrid">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- SECTION 2: 3-특성 슬롯 & 실시간 시너지 엔진 -->
        <!-- ========================================== -->
        <section class="showcase-card" id="section-slots">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="badge-num">02</span>
                    3-특성 슬롯 해금 & 더블 2중 융합 시너지 엔진
                </h2>
                <span style="font-size: 0.8rem; color: #94a3b8;">1슬롯(시작) · 2슬롯(2마을 해금) · 3슬롯(3마을 해금) 및 [1+2] & [2+3] 더블 융합</span>
            </div>

            <div class="simulator-layout">
                <!-- 좌측: 슬롯 장착 및 시너지 실시간 상태 -->
                <div>
                    <div class="control-group-title">🎯 현재 장착된 특성 슬롯 (3 Slots)</div>
                    <div class="slots-display-row">
                        <!-- Slot 1 -->
                        <div class="slot-display-box unlocked equipped" id="slotCard0">
                            <span class="slot-badge-num">SLOT 1 (기본)</span>
                            <div class="slot-content-name" id="slotName0">신체 변이</div>
                            <div class="slot-content-part" id="slotPart0">흑요석 뿔 (horns)</div>
                            <button class="slot-btn-unequip" onclick="unequipSlot(0)">해제</button>
                        </div>

                        <!-- Slot 2 -->
                        <div class="slot-display-box unlocked" id="slotCard1">
                            <span class="slot-badge-num">SLOT 2</span>
                            <button class="slot-btn-toggle" id="btnToggleLock1" onclick="toggleSlotLock(1)">해금됨</button>
                            <div class="slot-content-name" id="slotName1" style="color:#64748b;">+ 빈 슬롯</div>
                            <div class="slot-content-part" id="slotPart1">특성 클릭하여 장착</div>
                        </div>

                        <!-- Slot 3 -->
                        <div class="slot-display-box unlocked" id="slotCard2">
                            <span class="slot-badge-num">SLOT 3</span>
                            <button class="slot-btn-toggle" id="btnToggleLock2" onclick="toggleSlotLock(2)">해금됨</button>
                            <div class="slot-content-name" id="slotName2" style="color:#64748b;">+ 빈 슬롯</div>
                            <div class="slot-content-part" id="slotPart2">특성 클릭하여 장착</div>
                        </div>
                    </div>

                    <!-- 실시간 융합 시너지 발동 상태 박스 -->
                    <div class="synergy-banner-box" id="synergyBannerBox">
                        <!-- Populated dynamically -->
                    </div>
                </div>

                <!-- 우측: 13대 특성 장착 팔레트 -->
                <div>
                    <div class="control-group-title" style="justify-content: space-between;">
                        <span>🧩 13대 고유 특성 칩셋 팔레트 (클릭하여 장착/해제)</span>
                        <span style="font-size: 0.7rem; color: #64748b;">각 특성마다 고유 신체 파츠 1:1 매핑</span>
                    </div>
                    <div class="traits-palette-grid" id="traitsPaletteGrid">
                        <!-- Populated dynamically -->
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- SECTION 3: 78대 초월 융합 매트릭스 브라우저 -->
        <!-- ========================================== -->
        <section class="showcase-card" id="section-fusions">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="badge-num">03</span>
                    전 78대 초월 2중 융합 매트릭스 & 원클릭 시험기
                </h2>
                <span style="font-size: 0.8rem; color: #94a3b8;">13개 특성으로 구성된 78개 (13C2) 융합 실전 엔진 전수 가동</span>
            </div>

            <!-- 검색 및 카테고리 필터 바 -->
            <div class="fusions-filter-bar">
                <div class="chip-buttons-row" id="fusionFilterChips">
                    <button class="btn-chip active" data-cat="all">전체 융합 (78)</button>
                    <button class="btn-chip" data-cat="atk">⚔️ 공격/치명타/방관</button>
                    <button class="btn-chip" data-cat="def">🛡️ 방어/보호막/경감</button>
                    <button class="btn-chip" data-cat="hit">⚡ 연타/가속/기절</button>
                    <button class="btn-chip" data-cat="skill">✨ 요정/스킬/도트</button>
                    <button class="btn-chip" data-cat="rad">☣️ 방사능/반사/부활</button>
                </div>
                <div class="search-box-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" id="fusionSearchInput" placeholder="융합명, 특성 이름, 효과 검색...">
                </div>
            </div>

            <!-- 78개 융합 카드 그리드 -->
            <div class="fusions-cards-grid" id="fusionsCardsGrid">
                <!-- Populated dynamically -->
            </div>
        </section>

        <!-- ========================================== -->
        <!-- SECTION 4: 괴수 도감 & 실시간 모션 테스터 -->
        <!-- ========================================== -->
        <section class="showcase-card" id="section-monsters">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="badge-num">04</span>
                    괴수 도감 & 실시간 액션 테스터 (모션 플립 버그 수정 & 텍스트 제거)
                </h2>
                <span style="font-size: 0.8rem; color: #94a3b8;">전 14개 지역 괴수 영웅 방향(좌측) 정렬 및 카드 뒤집힘 방지 검증</span>
            </div>

            <div class="monster-showcase-grid">
                <!-- 좌측: 선택 괴수 실시간 액션 테스트 스테이지 -->
                <div class="monster-test-stage">
                    <div style="font-size: 0.72rem; color: #94a3b8; font-family: monospace;">SELECTED MONSTER ACTION TEST</div>
                    <div class="slot-content-name" id="testMonsterName" style="color:var(--neon-pink); margin-top:4px;">그레이트 울프 [보스]</div>
                    
                    <div class="actor-card monster-card" id="demoMonsterWrapper" style="margin: 14px 0;">
                        <div class="actor-hp-container">
                            <div class="hp-label" id="demoMonsterLabel">HP: 550 / 550</div>
                            <div class="hp-bar-outer" style="width: 140px;">
                                <div class="hp-bar-inner monster-hp" id="demoMonsterHpBar" style="width: 100%;"></div>
                            </div>
                        </div>
                        <div class="monster-sprite-preview-box" id="demoMonsterSprite"></div>
                    </div>

                    <!-- 액션 테스트 버튼 -->
                    <div style="display: flex; flex-direction: column; gap: 8px; width: 100%;">
                        <button class="btn-ctrl" id="btnTestLunge" style="padding: 8px;">⚔️ 공격 돌진 (Lunge: -75px 카드 플립 없음)</button>
                        <button class="btn-ctrl" id="btnTestKnockback" style="padding: 8px;">💥 피격 넉백 (Knockback: +28px 반동)</button>
                        <button class="btn-ctrl" id="btnTestDefeat" style="padding: 8px;">💀 전투 불능 (Defeat: 90도 전도 회색화)</button>
                        <button class="btn-ctrl" id="btnTestReset" style="padding: 8px; background:#141c2c; border-color:#334155;">🔄 상태 초기화</button>
                    </div>

                    <!-- 섀도우 배트 클리닝 완료 안내 -->
                    <div style="margin-top: 14px; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 6px; padding: 8px 12px; font-size: 0.7rem; color: #6ee7b7; text-align: center;">
                        ✅ 4지역 섀도우 배트 (m_4_2) 하단 텍스트 아티팩트 제거 완료
                    </div>
                </div>

                <!-- 우측: 14개 지역 괴수 갤러리 -->
                <div>
                    <div class="control-group-title" style="justify-content: space-between;">
                        <span>👾 14개 지역 괴수 목록 (클릭하여 시험대에 올리기)</span>
                        <div class="chip-buttons-row" id="monsterRegionFilter">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                    <div class="monster-gallery-scroll" id="monsterGalleryScroll">
                        <!-- Populated dynamically -->
                    </div>
                </div>
            </div>
        </section>

    </div>

    <!-- Data & Controller Scripts -->
    <script src="display_data.js"></script>
    <script src="display.js"></script>
</body>
</html>
`;

fs.writeFileSync('display.html', displayHtml, 'utf8');
console.log('Successfully written display.html!');
