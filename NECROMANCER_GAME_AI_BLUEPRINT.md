# 💀 《목적을 잃지 않는 사령군주》 2D 도트 RPG 개발 마스터 블루프린트 (타 AI 전달용 지침서 v3.0 완결판)

> **문서 목적**: 본 문서는 웹소설 **《목적을 잃지 않는 사령군주》**에 등장하는 **모든 직업(12대 클래스)·모든 스킬(80종+)·대규모 세트/고유 아이템(96종+)**과 **회귀(Regression) 영혼 각인 시스템**을 바탕으로, **`PROJECT 2100`과 동일한 아키텍처·그래픽 스타일·9-Slice 전통 창살 UI·리소스 파이프라인**을 갖춘 게임을 제작하기 위해 **다른 AI 코딩 어시스턴트에게 그대로 복사해 전달할 수 있도록 작성된 마스터 지침서(Master Prompt & Technical Spec)**입니다.

---

## 📋 1. AI 어시스턴트 최우선 강제 룰셋 (`GEMINI.md` / System Prompt용)

다른 AI에게 작업을 시작시킬 때 아래 규칙을 프로젝트 루트의 `GEMINI.md`로 저장하거나 첫 프롬프트로 주입하십시오.

### 1.1 핵심 그래픽 & 아키텍처 절대 규칙
| 항목 | 강제 규격 상세 |
| :--- | :--- |
| **비주얼 테마** | **조선 전통 목판·한지·전통 창살(`亞`/완자문) + 황동 두석(놋쇠 장식) + 다크 판타지(사령 청록·절대영도 시안·성역 황금·그림자 보라·광전사 진홍) 네온**이 결합된 16비트 레트로 도트 스타일 (*Forager* / *Dungreed* 스타일의 통통 튀는 픽셀 보더 + `NeoDunggeunmo` 굵은 도트 폰트) |
| **리소스 포맷** | **SVG(벡터) 전면 금지**. 모든 캐릭터 파츠, 몬스터, 소환수, 배경, 아이콘, VFX, UI 프레임은 **`image-rendering: pixelated`가 적용된 2D 비트맵(PNG/JPG)**으로만 제작 |
| **주인공 듀얼 뷰 (Dual View)** | 1) **전투 씬(횡스크롤)**: 주인공(12대 직업)과 아군 소환수/용병은 무조건 **왼쪽→오른쪽(Facing Right)**을 바라보며 조립 (`오른팔` 전면 Z-index 상단, `왼팔` 몸통 뒤 Z-index 하단 배치)<br>2) **비전투 씬(마을/거점/스튜디오)**: 주인공은 **정면(Front View)** 대칭 구도로 조립 |
| **적 몬스터 방향** | 모든 적 괴수·외계군 스프라이트는 기본 우향 도트로 생성하되, **전투 화면 및 도감에서는 `transform: scaleX(-1)`을 적용해 오른쪽→왼쪽(주인공 방향)**을 바라보도록 통일 |
| **단일 파츠 + 18프레임 다중 레이어 페이퍼돌** | AI 이미지 생성 시 깨지기 쉬운 스프라이트 시트(Sprite Sheet) 생성을 금지함. `PROJECT 2100`의 검증된 **`240×240` 다중 레이어 페이퍼돌(`body`, `armor`, `helmet`, `weapon`, `wings/cape`, `aura`) + 6부위 스켈레탈 분할(`head`, `torso`, `f_arm`, `b_arm`, `l_leg`, `r_leg`)** 구조를 사용하여 대기(4F)·달리기(6F)·공격(4F)·스킬(4F) 모션 시 손 위치(`hx, hy`)와 무기가 1px 오차 없이 함께 움직이도록 구현 |
| **전시관 우선 검증 (`display.html`)** | 본 게임(`index.html`)을 수정하기 전에 반드시 **독립된 전시관/시뮬레이터(`display.html`)**를 먼저 구축하여 12대 직업 외형 조립, 전 스킬(72종) 다단계 연출 & 실제 부하 소환, 12종 신화 세트(60종) & 36종 고유 아이템, 회귀 특성/재능(Lv.1~10 영혼 각인) 시뮬레이터, 지역별 마을/전투 배경, 9-Slice 창살 UI를 시각적으로 검증받을 것 |

### 1.2 🚨 [절대 금지 / 꼼수 차단 규칙 (Anti-Shortcut Guardrails)]
> **⚠️ 아래 5가지 꼼수(Shortcut) 중 하나라도 발생하면 즉시 작업 실패로 간주한다:**
> 1. **단순 도형(네모 박스·졸라맨·단순 원) 생성 절대 금지**: `PIL.ImageDraw`의 기본 `rectangle`, `line`, `ellipse` 몇 줄로 대충 그린 **단색 네모 상자 아이템 아이콘(`[■]`), 졸라맨(Stick-figure) 소환수, 단순 동그라미 스킬 VFX**를 만드는 행위를 전면 금지한다.
> 2. **NVIDIA NIM API (`flux.1-dev` / `flux.1-kontext-dev`) & 2x 슈퍼샘플링 파이프라인 필수 사용**: 모든 주요 에셋(캐릭터 베이스, 소환수 7종, 지역 배경, 보스, 핵심 아이콘)은 반드시 **[섹션 8.1]의 NVIDIA Flux API 스크립트**와 **[섹션 8.2]의 `2x 슈퍼샘플링 + 베지어 곡선(draw_bezier_tube) + 16비트 명암(apply_16bit_shading) + 2px 먹선 외곽선(MaxFilter)` 엔진**으로 제작해야 한다.
> 3. **배경 미제거 통짜 이미지 사용 금지**: 흰색/검정색 배경이 남아 있는 비투명 이미지를 그대로 띄우거나, 파츠 레이어 조립 없이 통짜 일러스트 1장만 위아래로 흔드는 행위를 금지한다.
> 4. **정적 1장짜리 스킬 이펙트 금지**: 모든 72종 스킬은 각각 고유한 에셋을 가져야 하며, 시전 시 **`① 바닥 마법진 회전 ➡️ ② 투사체 비행 / 참격 궤적 ➡️ ③ 피격 폭발(Hit Burst) + 화면 역경직(Screen Shake) + 데미지 플로팅`**의 다단계 시퀀스로 작동해야 한다.
> 5. **소환 스킬의 실제 부하 도열 필수**: `해골 군단 소환`, `군단장 아서`, `진 블리자드(빙룡)`, `그림자 분신술`, `수호 천사령` 등 소환 스킬 발동 시 단순히 이펙트만 번쩍이고 끝나는 것이 아니라, **주인공 뒤편/상공 대열에 실제 고퀄리티 도트 부하 유닛들이 스폰되어 숨쉬기(Bobbing)·일제 돌격·시체 폭발(부하 희생 광역 자폭)을 수행**해야 한다.

---

## 🎨 2. 아트 디렉팅 & 컬러 팔레트 & 9-Slice 전통 창살 UI 규격

### 2.1 컬러 팔레트 (CSS `:root` 변수 규격)
```css
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/NeoDunggeunmo.css');

:root {
    /* 조선 고목판 & 음영 한지 베이스 */
    --bg-wood-dark: #0c0908;        /* 칠흑에 가까운 탄화 목판 배경 */
    --bg-wood-panel: #18120e;       /* 기본 목판 패널 내부 */
    --bg-hanji-dark: #231b15;       /* 어두운 고서 한지 슬롯 배경 */
    --bg-hanji-card: #2c221a;       /* 카드 본문 배경 */

    /* 목판 & 황동 두석 테두리 */
    --border-ink: #050403;          /* 3~4px 픽셀 외곽선용 먹색 */
    --border-wood: #543b28;         /* 깎아낸 전통 나무 프레임 */
    --border-wood-light: #7e5a3e;   /* 나무 상단 하이라이트 */
    --border-brass: #d4a338;        /* 황동 장석(두석) 포인트 */

    /* 직업별 & 등급별 네온 포인트 컬러 */
    --neon-gold: #ffd000;           /* 프리스트/권왕 / 만렙 영혼 각인 / 신화 세트 */
    --neon-cyan: #00f0ff;           /* 가디언/소드마스터/빙설여제 / 절대영도 */
    --neon-green: #00ffaa;          /* 네크로맨서/스나이퍼 / 사령 영혼불 */
    --neon-purple: #c850ff;         /* 어쌔신/사이오닉/데스나이트 / 심연 마력 */
    --neon-pink: #ff2a6d;           /* 버서커/시체폭발 / 치명타 / 보스 경고 */

    --text-ivory: #f5ede2;          /* 한지 위 미색 본문 */
    --text-muted: #b8a692;          /* 보조 설명 텍스트 */
    --font-pixel: 'NeoDunggeunmo', monospace, sans-serif;
}
```

### 2.2 전통 창살(`亞`/완자문) 9-Slice UI 테두리 구현 방식
단순한 CSS 단색 선(`border: 2px solid`)을 절대 사용하지 말고, **9-Slice용 전통 목판·창살 이미지 2종**을 생성하여 Python `PIL`로 여백 없이 크롭한 뒤 CSS `border-image`로 모든 패널과 버튼에 적용합니다.

1. **메인 대청 패널 프레임 (`assets/ui/ui_joseon_frame_cropped.png`)**:
   - `border: 26px solid transparent; border-image: url('assets/ui/ui_joseon_frame_cropped.png') 135 160 135 160 fill / 26px 32px / 0 round;`
2. **소형 한지 족자/창살 카드 프레임 (`assets/ui/ui_hanji_card_cropped.png`)**:
   - `border: 14px solid transparent; border-image: url('assets/ui/ui_hanji_card_cropped.png') 155 155 155 155 fill / 14px / 0 round;`

---

## ⚔️ 3. 소설 등장 전 직업 총망라: [12대 플레이어블 클래스] & 수학적 밸런스 설계

소설 《목적을 잃지 않는 사령군주》에 등장하는 주역 5인방, 3대 군단장, 세계 10왕(十王), 외계 제국 장군들의 전투 스타일을 전부 플레이어블화하여 **총 12개 직업**을 제공합니다. 플레이어는 시작 시 또는 회귀 시마다 원하는 직업을 자유롭게 선택할 수 있습니다.

### 3.1 12대 플레이어블 클래스 전체 일람 및 밸런스 기준표

> **⚖️ 직업 간 황금 밸런스 공식 (Standardized Combat Power Formula)**
> 특정 직업(사령술사 등)만 독주하지 않도록 모든 직업의 초당 기대 화력(Effective DPS)과 생존력(Effective HP)을 아래 표준 공식으로 정규화합니다.
> - **물리/마법 딜러형**: $\text{DPS} = \text{주스탯} \times 4.5 \times (1 + \text{치명타율} \times \text{치명타피해}) \times \text{공격속도}$
> - **소환사형 (네크로맨서/사이오닉)**: $\text{본체 DPS (40\%)} + \sum \text{소환수 DPS (60\%)} = \text{딜러형 100\% 화력과 동등}$ (단, 보스 광역기에 소환수가 파괴될 위험을 감수하는 대신 고점 시너지 부여)
> - **탱커/브루저형 (가디언/권왕/버서커)**: 기본 공격 계수는 딜러의 60%이나, **`[방어력(DEF) 또는 최대 체력(HP) 비례 추가 피해]`** 및 **`[피격 반사/광폭화 증폭]`**을 합산하면 딜러와 동등한 클리어 타임 보장!
> - **서포터/성역형 (프리스트)**: 회복 스킬 사용 시 **`[초과 회복량(Overheal)의 250~500%가 신성 고정 피해 벼락으로 전환]`**되어 솔로 플레이에서도 딜러급 폭딜 보장!

| 번호 | 직업명 (영문 ID) | 소설 원작 모델 | 주스탯 / 보조스탯 | 고유 전투 메커니즘 & 플레이 스타일 |
| :---: | :--- | :--- | :---: | :--- |
| **01** | **💀 네크로맨서**<br>`necromancer` | **최미남**<br>*(사령군주)* | **INT (마력)**<br>MP (최대마나) | • 적 처치 시 해골·네임드 군단 부활 + 한빙 마법 군중제어<br>• 소환수 물량전과 **`[시체 폭발]`** 연쇄 반응으로 화면 장악 |
| **02** | **🛡️ 아이기스 가디언**<br>`guardian` | **김현태 · 박태준**<br>*(제1방패여단)* | **DEF (방어력)**<br>HP (최대체력) | • 절대 깨지지 않는 다중 보호막과 도발·철벽 방진<br>• **방어력(DEF)과 누적 방어량에 비례**해 대지 강타 및 가시 반사 폭딜 |
| **03** | **⚡ 스톰 위저드**<br>`storm_wizard` | **이재성 · 아르카나**<br>*(마도포병/마도왕)* | **INT (마력)**<br>CDR (쿨감) | • 뇌전·화염·비전 마법 및 마도포 일제 사격<br>• 스킬 연속 시전 시 **`[마력 동조망 과충전]`** 스택이 쌓여 마법 범위 2배 폭발 |
| **04** | **🎯 팬텀 스나이퍼**<br>`sniper` | **박동석 · 강민우**<br>*(특수저격대)* | **AGI (민첩)**<br>CRIT (치명타) | • 최장거리 대구경 마도 저격총 & 공간 굴절 탄환<br>• 공격속도는 느리지만 **단일 탄환에 방어관통 100% + 확정 치명타 헤드샷** |
| **05** | **✨ 하이 프리스트**<br>`priest` | **오진석 · 엘레나**<br>*(성역의무단/성녀)* | **WIS (신성력)**<br>HP (최대체력) | • 상시 유지되는 황금 성역(Sanctuary) 장판으로 초당 회복 & 상태이상 정화<br>• **초과 회복량(Overheal)이 즉시 적에게 떨어지는 성광 심판 벼락**으로 변환 |
| **06** | **🗡️ 섀도우 어쌔신**<br>`assassin` | **카게미츠 · 시렌**<br>*(그림자 암살자)* | **AGI (민첩)**<br>EVA (회피율) | • 초고속 쌍검 난무·그림자 은신·맹독 및 출혈 중첩<br>• 회피 시 생성되는 **그림자 분신 3기가 본체의 모든 참격을 복제** |
| **07** | **🐉 소드마스터 (검왕)**<br>`sword_master` | **백도훈 · 지크프리트**<br>*(세계 10왕 검왕/철혈왕)* | **STR (무력)**<br>CRIT (치명타) | • 화면을 가르는 검기(오러 블레이드)와 발도술 카운터<br>• 적의 공격 타이밍에 맞춰 **`[일섬 패링]`** 성공 시 쿨타임 초기화 및 3배 반격 |
| **08** | **⚔️ 데스나이트**<br>`death_knight` | **듀라한 아서**<br>*(제1군단장)* | **STR (무력)**<br>LIFESTEAL (흡혈) | • 칠흑의 대검과 흑염 갑주를 두른 흡혈 중장갑 기사<br>• 스킬 사용 시 마나 대신 **체력을 소모해 흑염 피해 2.5배 증폭 + 적중 시 대량 흡혈** |
| **09** | **👊 권왕 무투가**<br>`martial_king` | **진무극 · 보리스**<br>*(곤륜 권왕/강철거인)* | **STR (무력)**<br>DEF (방어력) | • 맨주먹 투기와 금강불괴 강철 육체로 적진을 부수는 인파이터<br>• 기본 공격 3타마다 **`[내공 파쇄 충격파]`**가 터지며 보스 슈퍼아머 강제 파괴 |
| **10** | **🔮 사이오닉 마도사**<br>`psionic_tactician` | **벨록 · 대음양사**<br>*(제3군단장/음양사)* | **INT (마력)**<br>WIS (신성/정신력) | • 중력장 왜곡·외계 포탑/부적 식신 전개·적군 정신 해킹<br>• 적 몬스터를 일시적으로 **해킹(세뇌)하여 아군 편에서 자폭/교란**시키는 전략가 |
| **11** | **🪓 그래비티 버서커**<br>`berserker` | **볼가르 · 라시드**<br>*(외계 대장군/사막왕)* | **STR (무력)**<br>HP (잃은 체력) | • 쌍수 중력 도끼와 황금 곡도를 휘두르는 광전사<br>• **현재 체력이 낮을수록 공격속도와 피해량이 최대 +300% 폭증**하며 5초 불사 보유 |
| **12** | **❄️ 크라이오 엠프레스**<br>`cryo_empress` | **나탈리야 로마노바**<br>*(세계 10왕 빙여제)* | **INT (마력)**<br>FROST (빙결치) | • 순수 절대영도 냉기 마법의 극치를 다루는 빙설 여제<br>• 적에게 `[동상]` 중첩을 쌓아 **완전 빙결(Frozen) 상태인 적에게 입히는 피해 3배** |

---

## 🔥 4. 전 스킬 완전 개방 시스템 (총 72종 직업 스킬 + 크로스 스킬 장착 규칙)

> **💡 핵심 시스템: "모든 스킬을 자유롭게 사용 가능!" (`Cross-Class Skill Mastery`)**
> 1. 플레이어는 기본적으로 **액티브 스킬 슬롯 4칸 + 궁극기 슬롯 1칸(총 5칸)**을 가집니다.
> 2. 현재 선택한 직업의 전용 스킬 6종은 기본 해금되며, **타 직업의 스킬도 던전 보스 드랍 `[고대 스킬 비급서]` 또는 `[회귀 기억 계승]`을 통해 도감에 영구 해금**하여 슬롯에 자유롭게 섞어 장착할 수 있습니다!
>    - 예: **가디언**이 네크로맨서의 `[시체 폭발]`과 프리스트의 `[성역 전개]`를 동시에 장착하여 불사 자폭 탱커 빌드 구축 가능!
>    - 예: **소드마스터**가 어쌔신의 `[그림자 분신술]`과 스나이퍼의 `[약점 포착]`을 장착하여 분신 4명이 동시에 `[청룡참]`을 날리는 빌드 구축 가능!
> 3. **직업 밸런스 보정**: 본래 직업과 일치하는 주력 스킬은 **`[직업 정통성 보너스: 최종 위력 +25%, 마나 소모 -20%]`**를 받으며, 타 직업 스킬을 가져와 쓸 때는 기본 위력(100%)으로 작동하되 특정 **고유(Unique) 아이템** 착용 시 타 직업 스킬도 정통성 보너스를 받도록 설계합니다.

### 4.1 12대 직업별 핵심 스킬 트리 전체 명세표 (직업당 6종 = 총 72종)

| 직업 | ① 기본/패시브 코어 | ② 주력 딜링기 A | ③ 주력 딜링기 B | ④ 기동/방어/유틸기 | ⑤ 상급 결전기 | ⑥ 🌟 5세트 각성 궁극기 |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **01. 네크로맨서** | `해골 군단 소환`<br>(처치 시 자동 부활) | `시체 폭발`<br>(사체 연쇄 암흑폭발) | `본 스피어`<br>(관통 뼈창 5연사) | `본 아머 & 망자 걸음`<br>(뼈방패+유령 이동) | `군단장 소환: 아서`<br>(듀라한 흑염 돌격) | **`[진(眞) 블리자드]`**<br>(칠흑 얼음창 전장 초토화) |
| **02. 가디언** | `아이기스의 철벽`<br>(방어력 비례 반사) | `방패 돌진 강타`<br>(전방 기절+밀치기) | `대지 분쇄(어스퀘이크)`<br>(방어력 250% 충격파) | `연대 방진 결속`<br>(최대체력 50% 보호막) | `도발의 포효`<br>(적 공격력 40% 강탈) | **`[절대 방벽: 아이기스 노바]`**<br>(무적 성채+방어력 500% 폭발) |
| **03. 스톰 위저드** | `마력 동조망`<br>(스킬 3회마다 과충전) | `체인 라이트닝`<br>(적 8기 연쇄 뇌전) | `헬파이어 메테오`<br>(고열 운석 낙하) | `점멸(블링크) & 마나실드`<br>(순간이동+마나방벽) | `마도포 300문 일제사격`<br>(전방 융단폭격) | **`[템페스트 아크 노바]`**<br>(성층권 뇌전 폭풍 증발) |
| **04. 팬텀 스나이퍼** | `매의 눈(약점 포착)`<br>(거리 비례 치명타+) | `대구경 관통 저격`<br>(일직선 전원 관통) | `폭발 크레모아 & 탄막`<br>(후방 도약+지뢰 매설) | `고스트 카모플라주`<br>(은신+다음 탄환 3배) | `동력 코어 정밀 파괴`<br>(보스 방어력 0화+스턴) | **`[50km 공간 굴절 저격]`**<br>(차원 왜곡 확정 즉사급 탄환) |
| **05. 하이 프리스트** | `오버힐 심판 전환`<br>(초과회복->성광 벼락) | `홀리 라이트닝`<br>(치유+주변 성광 타격) | `정화의 성염`<br>(디버프 제거+지속화상) | `천상의 축복 방벽`<br>(공방 +40% 오라) | `구원의 빛기둥`<br>(아군 전체 즉시 완치) | **`[대성역: 천벌의 빛기둥]`**<br>(전원 불사+신성 고정피해 폭격) |
| **06. 섀도우 어쌔신** | `맹독과 출혈 각인`<br>(타격 시 도트 중첩) | `그림자 습격(섀도우 스탭)`<br>(적 배후 순간 베기) | `흑도 난무(블레이드 댄스)`<br>(무적 판정 12연참) | `그림자 분신술`<br>(공격 복제 분신 2기) | `혈독 폭살진`<br>(중첩된 출혈/독 일제폭발) | **`[차원 무음 참수]`**<br>(시간 정지+100개 환영 일제참수) |
| **07. 소드마스터** | `검기 발현(오러 블레이드)`<br>(사거리/관통력 2배) | `발도: 섬광일섬`<br>(초고속 전방 화면 베기) | `질풍노도 5연참`<br>(검기 폭풍 연속 발사) | `심안 패링(흘려내기)`<br>(피격 무효+3배 카운터) | `청룡참(Blue Dragon)`<br>(푸른 용 형상 거대 검기) | **`[만검귀종: 진(眞) 청룡참]`**<br>(하늘을 가르는 천 개의 신검) |
| **08. 데스나이트** | `피의 갈증(블러드 서스트)`<br>(피해량 25% 체력흡수) | `흑염 대검 베기`<br>(체력 소모 암흑화염 참격) | `죽음의 손아귀`<br>(원거리 적 강제 그랩) | `망자의 갑주`<br>(받는 피해 지연+흡혈2배) | `단두대 처형(길로틴)`<br>(체력 30% 이하 적 즉사급) | **`[아발론의 흑염 단두대]`**<br>(듀라한 군세 돌격+차원 양단) |
| **09. 권왕 무투가** | `금강불괴(강철 피부)`<br>(피격 경직 완전 면역) | `파쇄권(붕권)`<br>(방어 무시 단거리 펀치) | `폭풍 연환격`<br>(초당 15타 주먹 난타) | `순보 & 내공 폭발`<br>(주변 적 넉백+공속증폭) | `패왕 열파참`<br>(대지를 가르는 주먹 기공파) | **`[일격필살: 태산파쇄격]`**<br>(우주적 투기 주먹으로 전장 함몰) |
| **10. 사이오닉 마도사** | `전술 연산 알고리즘`<br>(적 패턴 예측 회피+) | `중력장 압축(그래비티 웰)`<br>(적들을 한 점으로 블랙홀 흡입) | `음양 오행 부적진`<br>(5속성 연쇄 폭발 결계) | `사이오닉 해킹(세뇌)`<br>(적 2기를 아군으로 변절) | `외계 강습 드론 호출`<br>(레이저 포탑 4기 전개) | **`[궤도 모함 해킹: 플라즈마 폭격]`**<br>(적 함대 주포를 역조작해 초토화) |
| **11. 버서커** | `광전사의 피`<br>(잃은 체력 1%당 공+3%) | `중력 도끼 휠윈드`<br>(이동하며 360도 회전참) | `사막의 혈풍참`<br>(모래폭풍 출혈 검기) | `불사 광란(언다잉 레이지)`<br>(5초간 체력 1 이하 불사) | `거인 학살자의 도약`<br>(공중 도약 후 대지 찍기) | **`[라그나로크: 중력 붕괴]`**<br>(체력 1로 전환 후 1000% 광역 파멸) |
| **12. 크라이오 엠프레스** | `절대영도의 한기`<br>(주변 적 이속/공속 -40%) | `아이스 스피어 개틀링`<br>(고드름 20연속 사격) | `프로스트 노바 & 빙벽`<br>(즉시 동결+얼음 성벽) | `얼음 여왕의 보석화`<br>(3초간 무적 얼음 결정) | `글래시어 폴(빙하 낙하)`<br>(거대 빙산 추락 공격) | **`[절대영도: 다이아몬드 더스트]`**<br>(전장 전체 영구 동결 후 유리처럼 분쇄) |

---

## 💎 5. 대규모 아이템 도감: [12직업 5부작 신화 세트(60종)] & [고유(Unique) 아이템(36종)]

다른 AI가 풍부한 파밍과 빌드 구성을 구현할 수 있도록 **총 96종의 핵심 세트/고유 아이템 데이터**를 명세합니다.

### 5.1 12대 직업별 [5부작 신화 세트 아이템] 총람 (12세트 × 5부위 = 60종)

| 직업 | 세트 명칭 | ① 반지 (1세트) | ② 주무기 (2세트) | ③ 갑옷 (3세트) | ④ 투구 (4세트) | ⑤ 코어 (5세트 완성) | 5세트 완성 핵심 효과 |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01. 네크로맨서** | **이단자의 유물** | 이단자의 뼈가락지 | 심연의 척추 지팡이 | 이단자의 늑골 갑옷 | 이단자의 두개골 투구 | 이단자의 심장석 | 소환수 자아 개안 + `[진 블리자드]` 해금 |
| **02. 가디언** | **아이기스 용철** | 거인의 강철 인장 | 용철의 대방패 | 불굴의 성채 두정갑 | 아이기스 청룡 투구 | 대지의 용철 심장핵 | 방어력 100% 공격 전환 + `[아이기스 노바]` |
| **03. 스톰 위저드** | **제네바 마도왕** | 동조망 에테르 반지 | 아르카나의 뇌전 보주 | 성운의 대마도 로브 | 대현자의 황금 서클릿 | 태초의 마력 폭풍핵 | 마나 소모 0 + 스킬 2연발 + `[아크 노바]` |
| **04. 스나이퍼** | **팬텀 호크아이** | 무음의 탄도 반지 | 강두호제 대구경 마도총 | 고스트 스텔스 코트 | 사신의 외안경(사탕) | 아공간 굴절 코어 | 거리 비례 피해 3배 + `[50km 공간 굴절 저격]` |
| **05. 프리스트** | **대성역 사도** | 성녀의 눈물 반지 | 구원의 백금 석장 | 심판관의 황금 성의 | 광휘의 천사 면류관 | 태초의 성흔 코어 | 초과회복 500% 딜 전환 + `[천벌의 빛기둥]` |
| **06. 어쌔신** | **그림자 군주** | 칠흑의 암살 가락지 | 카게미츠의 요도 쌍검 | 차원 은신 야행복 | 무음의 복면 두건 | 그림자 여왕의 심장 | 분신 3기 상시 유지 + `[차원 무음 참수]` |
| **07. 소드마스터** | **설악 청룡검왕** | 검선의 매듭 반지 | 백도훈의 청룡 신검 | 설악 운무 도포 | 검왕의 백발 관모 | 검기(劍氣)의 극의 단전 | 모든 공격 검기 나감 + `[만검귀종: 진 청룡참]` |
| **08. 데스나이트** | **아발론 단두대** | 망자의 서약 반지 | 아서의 흑염 대검 | 아발론 칠흑 판금갑 | 타오르는 듀라한 투구 | 불멸 기사의 어둠 성배 | 체력 소모기 피해 3배 + `[아발론 흑염 단두대]` |
| **09. 권왕 무투가** | **곤륜 무신(武神)** | 금강 투기 반지 | 보리스의 아다만티움 너클 | 무신의 호포 무도복 | 투신의 붉은 머리띠 | 내공의 등화 코어 | 공속 한계 돌파 + 슈퍼아머 파괴 + `[태산파쇄격]` |
| **10. 사이오닉** | **화성 이단참모** | 텔레파시 증폭 링 | 벨록의 홀로그램 제어봉 | 반중력 연구원 로브 | 사이오닉 연산 고글 | 화성 제국의 금기 코어 | 세뇌 가능 적 수 +3 & `[궤도 모함 플라즈마 폭격]` |
| **11. 버서커** | **사막의 중력왕** | 피의 갈망 반지 | 볼가르의 중력 쌍도끼 | 사막왕의 황금 견갑 | 광전사의 뿔투구 | 폭주하는 베히모스 핵 | 불사 지속시간 +5초 & `[라그나로크: 중력 붕괴]` |
| **12. 크라이오** | **시베리아 빙여제** | 영구동토의 얼음반지 | 나탈리야의 빙정 홀 | 설원 황실의 백색 코트 | 빙여제의 수정 티아라 | 히말라야 빙룡의 용옥 | 빙결 면역 적도 강제 동결 + `[다이아몬드 더스트]` |

---

### 5.2 빌드 체인저 [고유(Unique) 아이템 36종 도감] (드랍·대장간·암시장 획득)
플레이어가 세트 아이템 일부를 포기하더라도 섞어 쓰거나, **보조 장신구/특수 유물 슬롯**에 장착해 **타 직업 스킬 연동 및 기상천외한 시너지 빌드**를 만들 수 있는 고유 아이템 36종입니다.

#### (A) 무기·전투 메커니즘 변형 고유 아이템 (1~12번)
| 번호 | 고유 아이템명 | 소설 출처 / 획득처 | 고유 특수 옵션 (Unique Effect) |
| :---: | :--- | :--- | :--- |
| **01** | **🔨 강두호 장인의 담금질 망치** | 1지역 을지로 대장간 | 착용 중인 방어구·방패의 **기본 방어력 수치를 2.0배**로 증폭 |
| **02** | **🍬 박동석의 딸기맛 각성 사탕** | 2지역 북한산 캠프 | 치명타 적중 시 15% 확률로 **모든 스킬 쿨타임 즉시 초기화** + 3초간 공속 +50% |
| **03** | **🐉 백도훈의 부러진 청룡 목검** | 4지역 설악산 대청봉 | 직업 무관 기본 공격 5회마다 **`[삼할 청룡참]`** 검기 자동 발사 (모든 스탯 합산 계수) |
| **04** | **🪽 타락한 성녀의 검은 성서** | 12지역 라인강 방어선 | 모든 치유/회복 스킬이 체력 회복 대신 **400% 위력의 암흑 저주 폭발**로 전환 |
| **05** | **❄️ 시베리아 빙여제의 수정구** | 11지역 시베리아 요새 | 모든 직업의 공격 속성이 **[냉기]**로 변환되며, 빙결된 적 대상 최종 피해 **+85%** |
| **06** | **⚙️ 보리스의 아다만티움 외골격** | 8지역 블라디보스토크 | 이동속도 -15% 대신 **최대 체력 +100% 및 모든 공격에 최대 체력 15% 물리 피해 추가** |
| **07** | **💀 아서의 말없는 해골 투구** | 2지역 은문 보스전 | 네크로맨서가 아니어도 **제1군단장 `듀라한 아서`가 상시 호위 기사로 동반 참전** |
| **08** | **🥷 카게미츠의 그림자 수리검** | 6지역 양재동/도쿄 | 모든 투사체 스킬(뼈창, 화살, 저격탄, 고드름)의 **발사 개수가 +3개 추가**됨 |
| **09** | **📡 벨록의 전술 해킹 단말기** | 13지역 금문 외계모함 | **타 직업 스킬을 슬롯에 장착해도 `[직업 정통성 보너스(+25% 위력)]`를 동일하게 적용** |
| **10** | **🌋 로키산맥 베히모스의 용암심장** | 12지역 로키산맥 화산 | 주변에 초당 공격력 300%의 화염 오라 발생 + 냉기 스킬이 **[융해(증기 폭발)]**로 2배 피해 |
| **11** | **🦑 심해 크라켄의 흡착 촉수** | 9지역 태평양 해연 | 공격 적중 시 적들을 주인공 전방으로 끌어당기며 입힌 피해의 **12%를 체력/마나로 흡수** |
| **12** | **🐉 히말라야 고룡의 역린** | 10지역 고룡 묘지 | 궁극기(5번 슬롯)의 재사용 대기시간 **-45% 감소** 및 궁극기 시전 중 완전 무적 |

#### (B) 방어·생존·경제·회귀 시너지 고유 아이템 (13~24번)
| 번호 | 고유 아이템명 | 소설 출처 / 획득처 | 고유 특수 옵션 (Unique Effect) |
| :---: | :--- | :--- | :--- |
| **13** | **💍 인천항 거상의 황금 반지** | 1지역 블랙마켓 (10화) | 마력석(골드) 획득량 **+100%**, 보유 골드 1,000당 최종 피해량 +5% (최대 +150%) |
| **14** | **🍕 10주년 약속의 피자 박스** | 14지역 평화의 서울 | 다섯 친구 지원 스킬 호출 쿨타임 **-50%**, 호출 시 주인공 체력/마나 50% 즉시 회복 |
| **15** | **🍗 한밤의 치킨과 소주잔** | 3부 서울 휴식처 (89화) | 보스 웨이브 진입 시 **20초간 공격력·방어력·치명타 피해 +60% 만찬 버프** 발동 |
| **16** | **🛡️ 박태준 부단장의 특전 방탄복** | 5지역 수도권 사령부 | 한 번에 최대 체력의 25%를 초과하는 피해를 입지 않음 (**원콤/즉사 완전 방지**) |
| **17** | **🔥 서유나 대위의 마력 과열 코어** | 5지역 마도포병단 | 마나 소모량이 2배가 되는 대신 **모든 마법 및 포격 스킬 최종 피해량 +90%** |
| **18** | **🔭 강민우 관측수의 레이저 표적기** | 5지역 특수저격대 | 화면에 등장한 보스에게 자동으로 `[표적]` 마크 부여 (표적 대상 치명타 확률 +40%) |
| **19** | **📿 이수아 수석사제의 묵주** | 5지역 성역의무단 | 보호막이 유지되는 동안 **모든 상태이상 면역 및 스킬 쿨타임 회복 속도 +35%** |
| **20** | **🧪 한지윤 박사의 정제 마력 영약** | 판교 마도공학 연구소 | 전투 중 장착된 **[특성(Trait)]의 적용 레벨을 임시로 +2레벨 상승**시킴 |
| **21** | **📜 강태식 협회장의 S급 임명장** | 대한헌터협회 본부 | 아군 소환수 및 용병의 최대 소환 개체수 제한 **+3기 증가** |
| **22** | **🕶️ 윤서연 차관의 기밀 블랙박스** | 국방부 특임차관실 | 네임드 및 보스 처치 시 **아이템을 2번 드랍(더블 루팅)**할 확률 50% |
| **23** | **🕷️ 아라크네의 맹독 갑피** | 1지역 지하철 미궁 보스 | 피격 시 공격자에게 5초간 최대 체력 20%를 깎는 **치명적 신경독** 자동 전염 |
| **24** | **🎲 마카오 용왕의 속임수 주사위** | 7지역 마카오 카지노 | 모든 공격 피해량이 **50% ~ 300% 사이에서 랜덤**하게 터지며, 777이 뜨면 7배 피해! |

#### (C) 10왕 & 외계 제국 초월 고유 유물 (25~36번)
| 번호 | 고유 아이템명 | 소설 출처 / 획득처 | 고유 특수 옵션 (Unique Effect) |
| :---: | :--- | :--- | :--- |
| **25** | **⚡ 뇌제 마커스의 번개 창끝** | 12지역 북미 연맹 | 이동 거리에 비례해 전하가 충전되며 다음 스킬에 **연쇄 뇌격(공격력 600%)** 추가 |
| **26** | **⚔️ 철혈왕 지크프리트의 대검 파편** | 12지역 라인강 기적 | 체력이 50% 이상일 때 모든 공격에 **방어 무시 고정 피해 +40%** 추가 |
| **27** | **🏜️ 사막왕 라시드의 유리 모래시계** | 11지역 타클라마칸 | 사망에 이르는 피해를 입으면 **시간을 4초 전으로 되돌려 체력과 위치를 복구** (전투당 1회) |
| **28** | **👊 권왕 진무극의 곤륜 옥패** | 11지역 곤륜 특구 | 무기 장착을 해제(맨손)하면 **기본 공격력과 공격속도가 3.0배로 폭증** |
| **29** | **🔮 마도왕 아르카나의 무한 수정구** | 스위스 제네바 마도탑 | 마나가 100%로 고정되며, **최대 마나 수치의 200%만큼 영구 마법 보호막** 생성 |
| **30** | **🛸 타르코스 사령관의 중력 제어기** | 13지역 금문 함교 | 화면 내 모든 적의 이동속도와 투사체 속도를 **70% 둔화**시키는 역중력장 전개 |
| **31** | **🪓 대장군 볼가르의 행성 파쇄추** | 14지역 성층권 결전 | 공격속도가 30% 감소하는 대신 **모든 공격이 범위 폭발(스플래시) 및 확정 치명타**로 적중 |
| **32** | **🌑 그림자 여왕 시렌의 아공간 망토** | 14지역 성층권 결전 | 3초마다 1초씩 **차원 은신(타겟팅 해제 및 무적)** 상태로 자동 진입 |
| **33** | **👑 외계 황제의 부서진 왕관** | 14지역 최종 보스 드랍 | **모든 직업의 5부작 세트 요구 조건을 `-1` 감소**시킴 (4부위만 입어도 5세트 효과 발동!) |
| **34** | **🧬 이단자 벨록의 기억 결정체** | 13지역 벨록의 선물 | 전투 획득 경험치 **+200%** 및 스킬 마법서 드랍률 3배 증가 |
| **35** | **💎 다이아몬드 게이트의 차원 파편** | 14지역 성층권 균열 | 장착된 **모든 액티브 스킬이 25% 확률로 쿨타임 없이 연속 2회 발동** |
| **36** | **🕰️ 회귀자의 태엽 회중시계** | 1화 회귀 시작 유물 | **회귀(Regression) 실행 시 보유 중인 고유(Unique) 아이템 중 1개를 다음 회차로 계승** 가능! |

---

## 🔄 6. 핵심 성장 루프: [회귀(Regression) & 특성·재능 Lv.1~10 & 영혼 각인] 시스템

소설 제1화 *"멸망, 그리고 회귀"*의 테마를 게임의 핵심 메타 성장 시스템으로 구현합니다. **다른 AI가 수학 공식과 슬롯 로직을 오차 없이 코딩할 수 있도록 아래 명세를 100% 준수**하게 하십시오.

### 6.1 회귀(Regression) 핵심 규칙 요약표
| 구분 | 회귀 시 소멸(초기화)되는 항목 | 회귀 시 영구 유지 및 확장되는 항목 |
| :---: | :--- | :--- |
| **초기화 vs 유지** | • 보유 골드 및 마력석(Mana Stone) **전량 소멸 (0원)**<br>• 인벤토리 내 모든 장비·세트 아이템·고유 아이템 **전량 소멸** *(단, 36번 고유 유물 '회귀자의 시계' 보유 시 1개 계승 예외)*<br>• 현재 캐릭터 레벨(Lv.1로 초기화) 및 지역 진행도 초기화 | • **현재 장착 중인 [특성(Trait)] 및 [재능(Talent)]과 그 레벨(Lv.1~10)**<br>• **영혼에 각인된 만렙(Lv.10) 특성 및 재능 목록**<br>• 해금된 추가 특성칸 / 재능칸 / **영혼 각인 전용칸**<br>• 도감에 해금된 **12대 직업 및 72종 크로스 스킬 마법서 목록** |

### 6.2 슬롯 해금 및 중복 선택 레벨업 규칙 (`1 + 0.5*(Lv-1)` 공식)
1. **초기 슬롯 및 최초 회귀 보너스**:
   - **게임 최초 시작 시 (0회귀)**: 기본 `[특성 슬롯 1칸]` + 기본 `[재능 슬롯 1칸]` 보유.
   - **최초 회귀 실행 시 (1회귀 달성)**: **보상으로 `[특성 슬롯 +1칸]`, `[재능 슬롯 +1칸]`이 영구 확장**됩니다! (즉, 1회귀부터는 특성 2칸 + 재능 2칸 보유)
   - 회귀를 진행할 때마다 플레이어는 **특성 1개와 재능 1개를 추가로 선택하여 장착**합니다.
2. **동일 특성/재능 중복 선택 시 레벨업 및 `1.5배(+50%p)` 효율 공식**:
   - 회귀 보상으로 특성이나 재능을 선택할 때, **이미 착용 중인 것과 동일한 특성/재능을 선택하면 슬롯을 추가로 차지하지 않고 1칸만 유지한 채 해당 특성/재능의 레벨(Lv)이 `+1` 상승**합니다.
   - **레벨별 수치 증가 공식** (1레벨 기본 수치를 $B$라고 할 때, 레벨당 기본 수치의 $+50\%$씩 선형 증가):
     $$\text{Value}(\text{Lv}) = B \times \bigl(1 + 0.5 \times (\text{Lv} - 1)\bigr)$$
   - **예시 (`마나 회복 속도 +10%` 특성)**:
     - **Lv.1**: $10\% \times 1.0 = \mathbf{10\%}$
     - **Lv.2**: $10\% \times 1.5 = \mathbf{15\%}$ (1.5배)
     - **Lv.3**: $10\% \times 2.0 = \mathbf{20\%}$ (2.0배)
     - **Lv.4**: $10\% \times 2.5 = \mathbf{25\%}$ ...
     - **Lv.10 (만렙)**: $10\% \times 5.5 = \mathbf{55\%}$ (5.5배)
3. **🌟 만렙(Lv.10) 달성 & [영혼 각인 전용 재능칸 (Soul Engraved Slot)] 규칙**:
   - 모든 특성과 재능의 최대 레벨은 **Lv.10(만렙)**이며, 만렙에 도달하는 순간 **주인공의 영혼에 새겨지게(Soul Engraved)** 됩니다.
   - **최초 만렙 달성 특전**: 플레이어가 최초로 어떤 특성이나 재능 하나를 Lv.10(만렙)으로 달성하는 순간, **특수 슬롯인 `[🌟 영혼 각인 전용 재능칸 (Master Soul Slot)]`이 1칸 추가로 생성**됩니다!
   - **전용칸 장착 제한 규칙**: 이 `[영혼 각인 전용칸]`에는 Lv.1~9짜리 일반 특성/재능은 절대 넣을 수 없으며, **오직 Lv.10(만렙)을 달성해 영혼에 새겨진 특성 또는 재능만 장착**할 수 있습니다.

---

## 🚀 7. 다른 AI에게 그대로 복사해서 붙여넣을 [초기 실행 프롬프트]

다른 AI에게 첫 지시를 내릴 때 아래 블록을 그대로 복사해서 전달하십시오:

```markdown
너는 지금부터 웹소설 《목적을 잃지 않는 사령군주》를 원작으로 하는 2D 레트로 도트 RPG 웹 게임을 제작한다.
첨부된 `NECROMANCER_GAME_AI_BLUEPRINT.md` 문서의 모든 기술 규칙과 아트 디렉팅, 12대 직업/72종 스킬/96종 아이템/회귀 영혼 각인 밸런스 수치, 그리고 [섹션 8]의 NVIDIA NIM API(`flux.1-dev` / `flux.1-kontext-dev`) 생성 파이프라인 및 `PROJECT 2100` 240x240 다중 레이어 스켈레탈 엔진을 100% 준수하라.

### 🚨 최우선 절대 경고 (꼼수/지름길 절대 금지)
1. **PIL 기본 도형(단색 네모 상자, 졸라맨, 단순 원)으로 에셋을 때우는 행위를 절대 금지**한다. 만약 기존 폴더에 5KB 미만의 저해상도 더미 파일이 있다면 전량 덮어써서 고해상도 도트로 재생성하라.
2. **이미지 생성 시 반드시 [섹션 8.1]의 NVIDIA NIM REST API (`flux.1-dev` / `flux.1-kontext-dev`)**와 **[섹션 8.2]의 `2x 슈퍼샘플링 + 베지어 곡선(draw_bezier_tube) + 16비트 명암(apply_16bit_shading) + 2px 먹선 외곽선(MaxFilter)` 파이프라인**을 사용하라.
3. 흰색/검정색 배경이 안 지워진 통짜 캐릭터 이미지를 띄우지 말고, `remove_solid_bg_floodfill()`로 투명화 후 `240x240` 다중 레이어 페이퍼돌(`body`, `armor`, `helmet`, `weapon`, `wings`, `aura`)로 조립하라.

### [1단계 작업 지시: 전시관(`display.html`) 및 통합 시뮬레이터 우선 구축]
본 게임(`index.html`)을 만들기 전에, 모든 그래픽 에셋과 UI 테두리, 12대 직업 조립, 전 스킬(72종) 다단계 연출 및 실제 부하 소환, 12종 신화 세트 & 36종 고유 아이템, 회귀 시스템을 한눈에 검증할 수 있는 **전시관 및 시뮬레이터(`display.html`, `display.js`, `display_data.js`)**를 완벽히 구축하라.

1. **테마 & 9-Slice 전통 창살 UI 프레임**:
   - 폰트는 `NeoDunggeunmo`를 사용하고, 단순한 CSS 실선 테두리 대신 **조선 전통 목판/한지 + 전통 창살(`亞`/완자문) + 황동 두석 + 네온**이 결합된 9-Slice 비트맵 프레임(`ui_joseon_frame_cropped.png`, `ui_hanji_card_cropped.png`)을 모든 카드와 모달창에 `border-image`로 적용하라.
2. **섹션 01 (12대 플레이어블 직업 & 다중 레이어 페이퍼돌 & 실제 부하 소환 스튜디오)**:
   - 플레이어가 소설에 등장하는 **12대 직업(①네크로맨서 ②아이기스 가디언 ③스톰 위저드 ④팬텀 스나이퍼 ⑤하이 프리스트 ⑥섀도우 어쌔신 ⑦소드마스터 ⑧데스나이트 ⑨권왕 무투가 ⑩사이오닉 마도사 ⑪그래비티 버서커 ⑫크라이오 엠프레스)**을 모두 선택·전환할 수 있게 하라.
   - **[섹션 8.2]의 18프레임 스켈레탈 모션(`idle` 4F, `run` 6F, `attack` 4F, `skill` 4F)**과 손 좌표(`hx, hy`) 동기화를 통해 무기·갑옷·5세트 외형이 자연스럽게 움직이게 하라.
   - **[섹션 8.3]의 실제 부하 군단 도열 & 협공 시스템**: `해골 군단 소환`, `듀라한 아서`, `진 블리자드(빙룡)`, `그림자 분신술`, `수호 천사령` 시전 시 주인공 뒤편/상공에 **고퀄리티 도트 부하 유닛들이 실제로 소환되어 도열**하고, `[군단 일제 돌격]` 시 함께 공격하며, `[시체 폭발]` 시 소환된 해골 부하가 적진에서 화려하게 자폭하도록 구현하라.
3. **섹션 02 (회귀(Regression) & 특성·재능 Lv.1~10 & [영혼 각인 전용칸] 시뮬레이터)**:
   - `[🔄 회귀 실행]` 버튼을 누르면 보유 골드와 장착 아이템이 전량 소멸하는 대신 특성/재능을 선택할 수 있는 시뮬레이터를 구현하라.
   - **최초 1회귀 시 특성칸 +1개, 재능칸 +1개가 영구 확장**되게 하라.
   - 동일 특성/재능 중복 선택 시 슬롯을 추가 차지하지 않고 **레벨(Lv)이 오르며, 기본 효과의 `1 + 0.5 * (Lv - 1)`배(Lv.1=1.0배, Lv.2=1.5배, Lv.3=2.0배 ... Lv.10=5.5배)** 효율이 실시간 계산되게 하라.
   - **Lv.10(만렙) 달성 시 '영혼에 각인'**되며, **최초로 만렙 달성 시 `[🌟 영혼 각인 전용 재능칸]`이 1칸 추가 해금**되어 오직 만렙(Lv.10) 특성/재능만 그 칸에 장착할 수 있도록 구현하라.
4. **섹션 03 & 04 (전 스킬 72종 5대 아키타입 연출 도감 & 1~14지역 84종 적 괴수 도감)**:
   - 72종 전 스킬을 **[섹션 8.3]의 5대 연출 아키타입(마법진 회전 ➡️ 투사체 비행/참격 궤적 ➡️ 타격 폭발 + 역경직)**으로 구현하고, 1~14지역 84종 몬스터(`assets/monsters/m_{1..14}_{1..4|named|boss}.png`, `scaleX(-1)` 좌향 반전) 액션 스테이지를 구현하라.
5. **섹션 05 (지역별 맞춤 [생존자 거점 마을 + 전투 전장 배경] 및 인게임 UI 프리뷰어)**:
   - 지역별 고유 마을 배경(`town_bg`)과 전투 배경(`battle_bg`)을 즉시 전환하며 볼 수 있게 구현하라.
```

---

## 🛠️ 8. [타 AI 실패 방지용] 하드코어 기술 구현 명세 (NVIDIA Flux API · 240x240 스켈레탈 빌더 · 5대 스킬 시퀀스 · 84종 몬스터)

> **🚨 중요**: 다른 AI가 기존 `PROJECT 2100`의 소스코드를 직접 보지 못하거나 내장 이미지 생성기 쿼터 제한(429)을 만나더라도 단 한 번의 시행착오나 퀄리티 저하 없이 완벽한 도트 에셋과 게임을 만들 수 있도록, 아래 **5대 핵심 엔지니어링 파이프라인**을 100% 그대로 구현하게 하십시오.

---

### 8.1 NVIDIA NIM REST API (`flux.1-dev` / `flux.1-kontext-dev`) 생성 & 투명화 파이프라인 (`tools/nvidia_asset_pipeline.py`)

내장 `image-generator` 도구 대신, `PROJECT 2100`에서 검증된 **NVIDIA NIM API**를 순수 Python `requests`로 직접 호출하여 고해상도 2D 도트/치비 마스터 에셋(캐릭터 베이스, 소환수 7종, 주요 보스, 배경)을 생성합니다.
- **API Key 자동 로드**: 워크스페이스 내 `D:\workspace\GEMINI\project2100\scratch\generate_flux_base_trainee.py` (또는 환경변수 `NVIDIA_API_KEY`)에서 검증된 키를 자동으로 읽어옵니다.
- **필수 준수 규칙**: 타임아웃 **300초**, `429/500/502/503/504` 발생 시 **최대 8회 지수 백오프 재시도**, **파일 크기가 8KB 이상인 정상 파일만 스킵하는 스마트 이어쓰기(Auto-Resume)**, 생성 직후 **네 모서리 Flood-fill 투명화 + 2px 먹선 외곽선(`MaxFilter(5)`)** 자동 적용.

```python
# -*- coding: utf-8 -*-
import os, re, sys, io, time, base64, requests
from collections import deque
from PIL import Image, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

FLUX_DEV_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
FLUX_KONTEXT_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-kontext-dev"

def load_nvidia_api_key():
    """환경변수 또는 project2100의 검증된 스크립트에서 NVIDIA API 키를 자동 추출"""
    if os.environ.get("NVIDIA_API_KEY"):
        return os.environ["NVIDIA_API_KEY"]
    ref_script = r"D:\workspace\GEMINI\project2100\scratch\generate_flux_base_trainee.py"
    if os.path.exists(ref_script):
        text = open(ref_script, encoding="utf-8").read()
        m = re.search(r'API_KEY\s*=\s*["\']([^"\']+)["\']', text)
        if m:
            return m.group(1)
    raise RuntimeError("NVIDIA_API_KEY not found!")

def remove_solid_bg_floodfill(img, tolerance=32):
    """네 모서리에서 시작하여 흰색/단색 배경을 투명(Alpha=0)으로 제거하고 알파 바운딩 박스로 크롭"""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    bg_r, bg_g, bg_b, _ = px[0, 0]
    visited = [[False] * h for _ in range(w)]
    queue = deque(corners)

    while queue:
        x, y = queue.popleft()
        if x < 0 or x >= w or y < 0 or y >= h or visited[x][y]:
            continue
        visited[x][y] = True
        r, g, b, a = px[x, y]
        if (abs(r - bg_r) <= tolerance and abs(g - bg_g) <= tolerance and abs(b - bg_b) <= tolerance) or (r > 240 and g > 240 and b > 240):
            px[x, y] = (0, 0, 0, 0)
            queue.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img

def add_fast_anime_outline(im, outline_color=(20, 16, 26, 255), size=5):
    """모든 스프라이트/아이콘 외곽에 깔끔한 2px 다크 먹선 테두리(Outline)를 입히는 핵심 함수"""
    r, g, b, a = im.split()
    a_solid = a.point(lambda p: 255 if p > 125 else 0)
    im_solid = Image.merge("RGBA", (r, g, b, a_solid))
    dilated_a = a_solid.filter(ImageFilter.MaxFilter(size))
    outline_layer = Image.new("RGBA", im.size, outline_color)
    outline_layer.putalpha(dilated_a)
    return Image.alpha_composite(outline_layer, im_solid)

def generate_flux_sprite(prompt, out_path, canvas_size=(240, 240), seed=1004, is_bg=False):
    """
    1) Auto-Resume: 이미 8KB 이상의 정상 에셋이 존재하면 건너뜀 (5KB 미만 더미 파일은 강제 재생성)
    2) 8회 자동 재시도(Backoff) 및 300초 타임아웃 적용
    3) 캐릭터/소환수/아이콘은 배경 투명화 후 정방형 캔버스 중앙 정렬 & 외곽선 마감
    """
    if os.path.exists(out_path) and os.path.getsize(out_path) > 8192:
        print(f"[SKIP - Valid Asset Exists] {out_path}")
        return True

    api_key = load_nvidia_api_key()
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    payload = {
        "prompt": prompt,
        "mode": "base",
        "cfg_scale": 3.8,
        "width": 1024,
        "height": 768 if is_bg else 1024,
        "seed": seed,
        "steps": 28
    }

    for attempt in range(8):
        try:
            resp = requests.post(FLUX_DEV_URL, headers=headers, json=payload, timeout=300)
            if resp.status_code == 200:
                arts = resp.json().get("artifacts", [])
                if arts and arts[0].get("base64"):
                    raw_im = Image.open(io.BytesIO(base64.b64decode(arts[0]["base64"])))
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    if is_bg:
                        raw_im.convert("RGB").save(out_path, "PNG")
                    else:
                        clean_im = remove_solid_bg_floodfill(raw_im)
                        cw, ch = canvas_size
                        clean_im.thumbnail((int(cw * 0.85), int(ch * 0.85)), Image.Resampling.LANCZOS)
                        canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
                        canvas.paste(clean_im, ((cw - clean_im.width) // 2, ch - clean_im.height - 6), clean_im)
                        canvas = add_fast_anime_outline(canvas, size=5)
                        canvas.save(out_path, "PNG")
                    print(f"[SAVED] {out_path}")
                    return True
            if resp.status_code in (429, 500, 502, 503, 504):
                wait_s = 6 * (attempt + 1)
                print(f"[RETRY {attempt+1}/8] HTTP {resp.status_code}, waiting {wait_s}s...")
                time.sleep(wait_s)
                continue
            print(f"[ERROR] HTTP {resp.status_code}: {resp.text[:200]}")
            return False
        except Exception as e:
            time.sleep(6 * (attempt + 1))
    return False
```

#### (A) 소환수 부하 군단 7종 & 대표 클래스 NVIDIA Flux 표준 프롬프트 테이블
소환수 및 클래스 마스터 스프라이트를 생성할 때 아래 프롬프트 규격을 사용하여 **메이플스토리/던전앤파이터/아크나이츠 풍의 선명한 2.5등신 SD 치비 도트/셀셰이딩 아트워크(우향 전투 자세, 순백색 배경)**로 뽑아내야 합니다:

| 에셋 파일명 | NVIDIA Flux 생성 프롬프트 (`pure solid white background` 필수) |
| :--- | :--- |
| `assets/summons/minion_skeleton_warrior.png` | `"2D game sprite asset, cute chibi undead skeleton warrior soldier facing right, glowing emerald green soul fire in eye sockets, wearing dark iron shoulder armor, holding a rune bone sword and weathered round shield, MapleStory and Dungeon Fighter chibi pixel art style, bold dark outlines, full body, pure solid white background"` |
| `assets/summons/minion_skeleton_archer.png` | `"2D game sprite asset, cute chibi undead skeleton archer facing right, wearing tattered purple hood and quiver on back, drawing a glowing cyan ghost-arrow on a bone recurve bow, MapleStory chibi pixel art style, bold dark outlines, full body, pure solid white background"` |
| `assets/summons/minion_skeleton_mage.png` | `"2D game sprite asset, cute chibi undead lich skeleton mage facing right, wearing ornate dark necromancer robe with gold trim, holding a skull staff radiating neon green and purple magic flames, MapleStory chibi pixel art style, bold dark outlines, full body, pure solid white background"` |
| `assets/summons/minion_death_knight.png` | `"2D game sprite asset, cute chibi Dullahan Death Knight Commander Arthur facing right, black abyssal full-plate armor with glowing crimson runes, horned dark helm, wielding a massive black-flame greatsword, MapleStory chibi pixel art style, bold dark outlines, full body, pure solid white background"` |
| `assets/summons/minion_frost_dragon.png` | `"2D game boss summon sprite asset, majestic chibi Frost Bone Dragon spirit facing right, translucent crystalline ice wings, glowing cyan dragon eyes, breathing diamond ice mist, MapleStory pixel art style, bold dark outlines, full body, pure solid white background"` |
| `assets/summons/minion_shadow_clone.png` | `"2D game sprite asset, cute chibi shadow ninja assassin clone facing right, shrouded in dark purple smoke aura, glowing crimson eyes, dual-wielding wicked shadow daggers, MapleStory chibi pixel art style, bold dark outlines, full body, pure solid white background"` |
| `assets/summons/minion_holy_guardian.png` | `"2D game sprite asset, cute chibi celestial valkyrie guardian spirit facing right, glowing golden angel wings and halo, shining white-gold paladin armor, holding an ornate Aegis greatshield, MapleStory chibi pixel art style, bold dark outlines, full body, pure solid white background"` |

---

### 8.2 `PROJECT 2100` 검증 완료: 240×240 다중 레이어 스켈레탈 페이퍼돌 & 2x 슈퍼샘플링 베지어/16비트 명암 엔진

`project2100/scratch/build_all_flawless_assets.py`에서 검증된 **핵심 절차적 고해상도 도트 렌더링 알고리즘**입니다. 무기(60종 세트 무기 + 고유 무기), 갑옷(몸통 컨투어 매핑), 날개/오라/뿔 파츠, 그리고 96종 아이템 아이콘과 72종 스킬 VFX를 생성할 때 **단순 사각형/직선 도형 대신 반드시 아래 4대 함수(`draw_bezier_tube`, `apply_16bit_shading`, `rotate_smooth_hd`, `get_hand_pos_and_angle`)**를 사용하여 2배 슈퍼샘플링(`SS=2`) 후 축소(`LANCZOS`) + `add_fast_anime_outline`으로 마감해야 합니다.

```python
import math
from PIL import Image, ImageDraw, ImageFilter

SCALE = 2
CANVAS_W, CANVAS_H = 240, 240
OUTLINE = (20, 16, 26, 255)

# 4대 모션 18프레임 스켈레탈 키프레임 정의 (idle 4F, run 6F, attack 4F, skill 4F)
MOTION_CONFIGS = {
    "idle": [
        dict(dx=0, dy=0, head_lean=0, torso_lean=0, fa_swing=0, ba_swing=0, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=0, dy=-1, head_lean=0, torso_lean=0, fa_swing=4, ba_swing=-4, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=0, dy=-2, head_lean=0, torso_lean=0, fa_swing=7, ba_swing=-7, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=0, dy=-1, head_lean=0, torso_lean=0, fa_swing=4, ba_swing=-4, ll_swing=0, rl_swing=0, ll_dy=0, rl_dy=0, vfx=None),
    ],
    "run": [
        dict(dx=2, dy=1, head_lean=4, torso_lean=6, fa_swing=28, ba_swing=-24, ll_swing=-22, rl_swing=22, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=3, dy=2, head_lean=5, torso_lean=8, fa_swing=14, ba_swing=-12, ll_swing=-10, rl_swing=12, ll_dy=-1, rl_dy=0, vfx=None),
        dict(dx=2, dy=-3, head_lean=3, torso_lean=5, fa_swing=-4, ba_swing=4, ll_swing=4, rl_swing=-4, ll_dy=-2, rl_dy=-2, vfx=None),
        dict(dx=2, dy=1, head_lean=4, torso_lean=6, fa_swing=-22, ba_swing=28, ll_swing=22, rl_swing=-22, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=3, dy=2, head_lean=5, torso_lean=8, fa_swing=-10, ba_swing=14, ll_swing=12, rl_swing=-10, ll_dy=0, rl_dy=-1, vfx=None),
        dict(dx=2, dy=-3, head_lean=3, torso_lean=5, fa_swing=4, ba_swing=-4, ll_swing=-4, rl_swing=4, ll_dy=-2, rl_dy=-2, vfx=None),
    ],
    "attack": [
        dict(dx=-4, dy=1, head_lean=-5, torso_lean=-8, fa_swing=-38, ba_swing=20, ll_swing=-12, rl_swing=14, ll_dy=0, rl_dy=0, vfx=None),
        dict(dx=8, dy=0, head_lean=6, torso_lean=10, fa_swing=68, ba_swing=-25, ll_swing=-18, rl_swing=22, ll_dy=0, rl_dy=0, vfx="slash"),
        dict(dx=10, dy=0, head_lean=5, torso_lean=8, fa_swing=52, ba_swing=-18, ll_swing=-14, rl_swing=18, ll_dy=0, rl_dy=0, vfx="pierce"),
        dict(dx=2, dy=0, head_lean=2, torso_lean=3, fa_swing=12, ba_swing=-6, ll_swing=-4, rl_swing=4, ll_dy=0, rl_dy=0, vfx=None),
    ],
    "skill": [
        dict(dx=-1, dy=4, head_lean=4, torso_lean=6, fa_swing=-28, ba_swing=-15, ll_swing=-10, rl_swing=12, ll_dy=-3, rl_dy=-3, vfx="charge"),
        dict(dx=5, dy=-14, head_lean=-4, torso_lean=-4, fa_swing=105, ba_swing=-30, ll_swing=-16, rl_swing=18, ll_dy=-2, rl_dy=-1, vfx="upper"),
        dict(dx=7, dy=-17, head_lean=4, torso_lean=6, fa_swing=78, ba_swing=-20, ll_swing=-20, rl_swing=22, ll_dy=-2, rl_dy=-2, vfx="burst"),
        dict(dx=4, dy=3, head_lean=6, torso_lean=8, fa_swing=32, ba_swing=-15, ll_swing=-12, rl_swing=16, ll_dy=-2, rl_dy=-2, vfx="slam"),
    ]
}

def draw_bezier_tube(d, p0, p1, p2, p3, r_start, r_end, col_dark, col_main, col_hi, steps=36):
    """두께감과 3단 입체 명암(암부·중간톤·하이라이트)을 가진 곡선 튜브 렌더링 (뿔, 날개, 갈비뼈, 대검, 지팡이 제작 필수 함수)"""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3)*p0[0] + 3*(mt**2)*t*p1[0] + 3*mt*(t**2)*p2[0] + (t**3)*p3[0]
        y = (mt**3)*p0[1] + 3*(mt**2)*t*p1[1] + 3*mt*(t**2)*p2[1] + (t**3)*p3[1]
        r = r_start + (r_end - r_start) * t
        pts.append((x, y, r))
    for x, y, r in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=col_dark)
    for x, y, r in pts:
        rm = max(1.0, r * 0.82)
        d.ellipse([x - rm, y - rm - r*0.08, x + rm, y + rm - r*0.08], fill=col_main)
    for x, y, r in pts[2:-2]:
        rh = max(0.8, r * 0.42)
        d.ellipse([x - rh, y - r*0.55 - rh, x + rh, y - r*0.55 + rh], fill=col_hi)

def apply_16bit_shading(im, preserve_glow=True):
    """좌상단 베벨 하이라이트(1.24배)와 우하단 음영(0.72배)을 자동 계산하여 16비트 도트 입체감을 부여하는 함수"""
    w, h = im.size
    src = im.load()
    out = im.copy()
    dst = out.load()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = src[x, y]
            if a == 0 or (r < 40 and g < 35 and b < 45) or (preserve_glow and r > 240 and g > 240 and b > 240):
                continue
            tl_empty = src[x - 1, y - 1][3] == 0
            br_empty = src[x + 1, y + 1][3] == 0
            if tl_empty and not br_empty:
                dst[x, y] = (min(255, int(r * 1.24) + 14), min(255, int(g * 1.24) + 14), min(255, int(b * 1.24) + 14), a)
            elif br_empty and not tl_empty:
                dst[x, y] = (int(r * 0.72), int(g * 0.72), int(b * 0.76), a)
    return out

def rotate_smooth_hd(img, pivot, deg):
    """회전 시 검은색 테두리 번짐(Black Halo)을 완벽히 방지하는 RGB 팽창 후 BICUBIC 회전 함수"""
    if deg == 0:
        return img
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    dilated_rgb = rgb.filter(ImageFilter.MaxFilter(5))
    padded_rgb = Image.composite(rgb, dilated_rgb, a.point(lambda p: 255 if p > 10 else 0))
    pr, pg, pb = padded_rgb.split()
    rot_r = pr.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot)
    rot_g = pg.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot)
    rot_b = pb.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot)
    rot_a = a.rotate(deg, resample=Image.Resampling.BICUBIC, center=pivot).point(lambda p: 255 if p > 125 else 0)
    return Image.merge("RGBA", (rot_r, rot_g, rot_b, rot_a))

def get_hand_pos_and_angle(cfg):
    """현재 프레임(cfg)의 오른손 그립 정확한 픽셀 좌표(hx, hy)와 무기 회전각(blade_deg) 반환"""
    dx, dy, fa_swing = cfg["dx"], cfg["dy"], cfg["fa_swing"]
    sx, sy = (53 + dx) * SCALE, (61 + dy) * SCALE
    rad = math.radians(fa_swing)
    hx = sx + int(21 * SCALE * math.sin(rad))
    hy = sy + int(21 * SCALE * math.cos(rad))
    return hx, hy, fa_swing - 22
```

> **💡 핵심 활용 지침**: 워크스페이스 내 `D:\workspace\GEMINI\project2100\assets\pixel_hero\` 폴더에는 이미 위 파이프라인으로 완벽히 구워진 `male_{idle|run|attack|skill}_{0..5}.png`, `female_*`, `male_nemesis_*`, `armors/*`, `weapons/*`, `mutations/*` (총 576장의 240×240 투명 레이어 PNG)가 존재합니다! 이를 베이스 레이어로 적극 활용하고, 12대 직업별 전용 무기·갑옷·투구·오라 레이어를 추가로 입혀 조립하십시오.

---

### 8.3 72종 전 스킬 고유 메커니즘 & 다단계 시각 연출 (방어막·무적·패링·점멸·은신·치유·소환·공격 완전 분기)

스킬을 단순히 적 타격용 단일 공격기로 통일하는 행위를 금지하며, 스킬 명칭과 본래 역할에 부합하도록 **아래 9대 메커니즘 아키타입(Archetype)**으로 엄격히 분기하여 시각 연출과 수치 판정을 분리해야 합니다:

| 아키타입 코드 | 대표 스킬 | 대상 (Target) 및 다단계 시각·수치 메커니즘 |
| :--- | :--- | :--- |
| **`SHIELD`**<br>(보호막/임시체력) | • `점멸 & 마나실드` (`storm_4`)<br>• `연대 방진 결속` (`guard_4`)<br>• `천상의 축복 방벽` (`priest_4`)<br>• `본 아머 & 망자 걸음` (`necro_4`)<br>• `망자의 갑주` (`dk_4`) | **시전자 본체(`self`) 전개 (적 타격 0)**:<br>• 영웅 본체에 푸른 마나실드 육각 돔 또는 성스러운 황금 방벽(`border: 3px solid #00f0ff/#ffd000, box-shadow: 0 0 30px`) 2.5초간 형성<br>• 영웅 머리 위에 **`[🔷 MANA SHIELD +24,000]`** 또는 **`[🛡️ CITADEL SHIELD +32,000]`** 플로팅 상승<br>• `storm_4`는 발동 즉시 후방으로 순간이동(점멸)하여 3초간 회피율 +75% 획득 |
| **`INVULNERABLE`**<br>& **`PARRY`**<br>(무적/패링/반격) | • `아이기스 노바` (`guard_ult`)<br>• `얼음 여왕의 보석화` (`cryo_4`)<br>• `불사 광란` (`ber_4`)<br>• `심안 패링` (`sm_4`)<br>• `흑도 난무` (`as_3`) | **영웅 전신 무적 판정**:<br>• 영웅 본체가 순수 다이아몬드 결정 또는 눈부신 황금빛(`filter: brightness(2.2) drop-shadow(...)`)으로 발광<br>• 영웅 머리 위에 **`[🌟 10s INVINCIBLE]`** 또는 **`[💎 ICE JEWEL 3s]`** 팝업 (모든 피해 100% 무효화 및 마력 급속 충전)<br>• `sm_4` 심안 패링은 피격 완전 무효화 후 **즉시 적진에 `[⚔️ 300% PARRY COUNTER 84,000]`** 반격 폭발 작렬! |
| **`STEALTH`**<br>& **`BLINK`**<br>(은신/회피/기동) | • `고스트 카모플라주` (`snip_4`)<br>• `순보 & 내공 폭발` (`mk_4`)<br>• `그림자 습격` (`as_2`) | **영웅 반투명화 & 타겟팅 면역**:<br>• 영웅 스프라이트가 투명도 35%(`opacity: 0.35`)로 변하며 보라빛 그림자 잔상 형성<br>• 영웅 머리 위에 **`[🕶️ STEALTH ON & CRIT +300%]`** 팝업 + 적 보스 타겟팅 즉시 해제 |
| **`HEAL`**<br>& **`OVERHEAL`**<br>(치유/정화/심판) | • `구원의 빛기둥` (`priest_5`)<br>• `정화의 성염` (`priest_3`)<br>• `홀리 라이트닝` (`priest_2`)<br>• `피의 갈증` (`dk_1`) | **생명력 회복 & 오버힐 벼락**:<br>• 하늘에서 황금 빛기둥이 꽂히며 영웅 머리 위에 **`[💚 FULL HEAL +50,000]`** 녹색 텍스트 상승 및 디버프 완전 정화<br>• 체력이 100%일 때 추가 치유량은 즉시 적진으로 꺾이며 **`[⚡ OVERHEAL JUDGMENT]`** 신성 벼락으로 변환 작렬 |
| **`BUFF`**<br>(스탯/오라 강화) | • `아이기스의 철벽` (`guard_1`)<br>• `금강불괴` (`mk_1`)<br>• `마력 동조망` (`storm_1`)<br>• `검기 발현` (`sm_1`)<br>• `광전사의 피` (`ber_1`) | **스탯 비례 전투력 폭증**:<br>• 영웅 발밑에 기공 오라 회전 + 머리 위에 **`[🥋 VAJRA BODY! DEF +100%]`**, **`[🛡️ DEF +80% & THORN ON]`**, **`[⚡ OVERCHARGE! MP 0]`** 팝업<br>• 피격 경직 완전 면역 및 지속시간 동안 평타 검기/가시 반사 부여 |
| **`SUMMON`**<br>(군단/영체 소환) | • `해골 군단 소환` (`necro_1`)<br>• `군단장 소환: 아서` (`necro_5`)<br>• `그림자 분신술` (`as_4`)<br>• `외계 강습 드론` (`psi_5`)<br>• `수호 천사령` (`priest_ult`) | **영웅 뒤편 실제 도열 및 협공**:<br>• 영웅 뒤편(`#heroMinionsContainer`) 및 상공에 고퀄리티 도트 부하 유닛(`minion_*.png`) 솟아오름<br>• 영웅 머리 위에 **`[💀 SUMMONED! +3 MINIONS]`** 팝업<br>• `[⚔️ 군단 일제 돌격]` 시 뒤편 부하들이 일제히 전방 돌진 사격 |
| **`CORPSE_BURST`**<br>(시체 폭발 연계) | • `시체 폭발` (`necro_2`)<br>• `혈독 폭살진` (`as_5`) | **부하/혈기 적진 돌진 자폭**:<br>• 소환된 부하 중 1기가 붉은 섬광과 함께 적진으로 돌진하여 팽창 후 **`[💀 CORPSE BURST!]`** 대폭발! |
| **`PROJECTILE_BARRAGE`**<br>(관통 투사체) | • `본 스피어` (`necro_3`)<br>• `대구경 관통 저격` (`snip_2`)<br>• `아이스 스피어 개틀링` (`cryo_2`) | **적진 관통 다단히트**:<br>• 영웅 손끝에서 적 타격존까지 초고속 비행하는 도트 투사체 3~20발 + 관통 스파크 연속 작렬 |
| **`AOE_CATACLYSM`**<br>(전장 초토화 결전기) | • `[진(眞) 블리자드]` (`necro_ult`)<br>• `[만검귀종: 진 청룡참]` (`sm_ult`)<br>• `[50km 공간 굴절 저격]` (`snip_ult`)<br>• `[다이아몬드 더스트]` (`cryo_ult`) | **화면 전체 지진 & 결전 컷인**:<br>• 무대 암전 + 거대 칠흑 빙창/천 개의 신검/플라즈마 폭격 쏟아짐 + 초대형 **`[💥 CRITICAL]`** 폭발 데미지 |

---

### 8.4 에셋 디렉토리 구조 & 파일명 매핑 절대 규격 (404 깨짐 방지)

코드(`display_data.js`, `display.js`, `game.js`)에서 이미지 경로를 참조할 때 단 1건의 `404 File Not Found`도 발생하지 않도록 아래 경로 규칙을 엄격히 통일하십시오:

1. **적 괴수 (84종 — `project2100/assets/monsters/`에서 복사 완료)**:
   - ❌ 잘못된 경로: `assets/monsters/region1_6.png` (**절대 사용 금지!**)
   - ✅ **정확한 실제 경로**:
     - 1~4웨이브 일반 괴수: `assets/monsters/m_${regionNum}_1.png` ~ `assets/monsters/m_${regionNum}_4.png`
     - 5웨이브 수문장(Named): `assets/monsters/m_${regionNum}_named.png`
     - 6웨이브 지역 보스(Boss): **`assets/monsters/m_${regionNum}_boss.png`** (예: 1지역 보스 아라크네 = `assets/monsters/m_1_boss.png`)
2. **영웅 다중 레이어 페이퍼돌 (`project2100/assets/pixel_hero/` 연동)**:
   - 베이스 바디: `assets/pixel_hero/${gender}_${motion}_${frame}.png` (`gender`: `male` / `female` / `male_nemesis` / `female_nemesis`, `motion`: `idle` / `run` / `attack` / `skill`, `frame`: `0..5`)
   - 갑옷 레이어: `assets/pixel_hero/armors/${armor}_${motion}_${frame}.png`
   - 무기 레이어: `assets/pixel_hero/weapons/${weapon}_${motion}_${frame}.png`
   - 변이/세트 파츠 레이어: `assets/pixel_hero/mutations/${part}_${motion}_${frame}.png` (`horns`, `wings`, `fairy_wings`, `halo`, `crystals`, `spikes`, `core`, `tail`, `claws`, `booster`, `visor`, `shell`, `antennae`)
3. **소환수 부하 군단 (7종)**:
   - `assets/summons/minion_skeleton_warrior.png` (해골 전사)
   - `assets/summons/minion_skeleton_archer.png` (해골 궁병)
   - `assets/summons/minion_skeleton_mage.png` (해골 술사)
   - `assets/summons/minion_death_knight.png` (데스나이트 아서)
   - `assets/summons/minion_frost_dragon.png` (빙룡 영체)
   - `assets/summons/minion_shadow_clone.png` (그림자 분신)
   - `assets/summons/minion_holy_guardian.png` (수호 천사령)
4. **스킬 VFX (72종) & 타격 이펙트**:
   - 직업별 스킬 VFX: `assets/pixel_vfx/skills/vfx_${skillId}.png`
   - 공통 아케이드 타격/참격 VFX (`project2100/assets/pixel_vfx/`에서 복사): `vfx_slash_arc.png`, `vfx_axe_spin.png`, `vfx_laser_bolt.png`, `vfx_nemesis_burst.png`, `vfx_hit_burst.png`

---

### 8.5 14대 지역 × 6종 = [총 84종 적 괴수 도감] 및 스탯 스케일링 공식
모든 지역(1~14지역)은 **총 6웨이브**로 구성되며, **1~4웨이브는 일반 괴수(Normal 4종), 5웨이브는 정예 수문장(Named 1종), 6웨이브는 지역 보스(Boss 1종)**가 등장합니다.

#### (A) 지역 및 웨이브별 몬스터 스탯 자동 스케일링 수식
```javascript
function getMonsterStats(regionNum, waveNum, type) {
    // 지역당 지수 성장 + 웨이브 선형 성장
    const regionScale = Math.pow(1.45, regionNum - 1);
    const waveScale = 1 + (waveNum - 1) * 0.18;
    const typeMult = type === "boss" ? { hp: 6.5, atk: 2.2, def: 1.8, gold: 10 }
                   : type === "named" ? { hp: 3.0, atk: 1.5, def: 1.3, gold: 4 }
                   : { hp: 1.0, atk: 1.0, def: 1.0, gold: 1 };

    return {
        maxHp: Math.round(120 * regionScale * waveScale * typeMult.hp),
        atk:   Math.round(15  * regionScale * waveScale * typeMult.atk),
        def:   Math.round(5   * regionScale * waveScale * typeMult.def),
        rewardGold: Math.round(25 * regionScale * typeMult.gold),
        dropRateSetOrUnique: type === "boss" ? 0.35 : (type === "named" ? 0.12 : 0.02)
    };
}
```

#### (B) 6대 차원문(Gate) 등급별 환경 기믹(`assets/ui/gates/gate_*.png`) 및 1~14지역 전체 몬스터·배경 라인업 명세 (총 84종)
- **차원문 입장 메커니즘**: 플레이어는 마을 거점(`town_bg_{1..14}.png`)에서 각 지역의 고유 **차원문 오브젝트(`gate_iron.png`, `gate_bronze.png`, `gate_silver.png`, `gate_gold.png`, `gate_platinum.png`, `gate_diamond.png`)**를 클릭해 문을 통과하며, 각 문마다 **고유 전장 배경(`battle_bg_{1..14}.png`), 환경 특성(Modifier), 공명 신체 특성(Trait), 6웨이브 몬스터 패밀리(`m_{1..14}_{1..4|named|boss}.png`)**가 다르게 적용됩니다.

| 지역 | 차원문 등급 & 에셋 | 공명 특성 & 환경 기믹 | 일반 괴수 1~4 (`m_N_1..4`) | 5웨이브 수문장 (`m_N_named`) | 6웨이브 지역 보스 (`m_N_boss`) |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1. 지하철 미궁** | **🚪 철문**<br>`gate_iron.png` | `🌀 마력 호흡`<br>지하 탁기 · 맹독 포자 | 지하철 감염 쥐 / 동공 구울 / 녹슨 철도 해골 / 맹독 거미줄 유충 | **미궁의 도살자 오거** | **🕷️ 철갑과 맹독의 여왕 아라크네** |
| **2. 북한산 은문** | **🚪 은문**<br>`gate_silver.png` | `💀 사령의 권능`<br>은빛 마력 한기 (+30% 마나) | 은빛 침엽수 늑대 / 고대 제단 해골병 / 결계 망령 술사 / 흑요석 가고일 | **흑요석의 수호 골렘** | **🏇 단두대의 기사 듀라한 아서** |
| **3. 인천항 부두** | **🚪 동문**<br>`gate_bronze.png` | `🩸 포식자의 본능`<br>중장갑 요새화 (적 방어+20%) | 밀수단 단검 조폭 / 부두 개조 사냥개 / 컨테이너 마도 포수 / 암시장 주술사 | **제4부두 행동대장 크로우** | **⚓ 카르텔 마도 중장갑 파괴자** |
| **4. 설악산 대청봉** | **🚪 은문**<br>`gate_silver.png` | `🦅 매의 눈`<br>설원 검기 한파 | 설산 빙결 멧돼지 / 대청봉 설인(예티) / 설악검문 수련 무사 / 청풍 검기 환영 | **설악검문 수제자 최강현** | **🐉 세계 10왕 ‘검왕’ 백도훈 (삼할 시험)** |
| **5. 평양 지하벙커** | **🚪 동문**<br>`gate_bronze.png` | `🛡️ 육체의 기억`<br>지하 요새 지뢰밭 | 휴전선 지뢰 거미 / 북측 강화 보병 / 지하 벙커 화염방사병 / 생체 실험 키메라 | **친위대장 강철 골렘** | **🤖 지하 50m 아다만티움 거신병** |
| **6. 양재동·도쿄** | **🚪 은문**<br>`gate_silver.png` | `🌙 잔상 보법`<br>음양사 주술 결계 | 열도 하급 닌자 / 그림자 까마귀 요괴 / 종이 식신(시키가미) / 주술 원령 무사 | **어둠의 칼날 카게미츠** | **👹 도쿄 본가 대음양사 아베노** |
| **7. 마카오 불야성** | **🚪 금문**<br>`gate_gold.png` | `✨ 성역의 은총`<br>황금 과부하 역장 (치명타+50%) | 카지노 흑복 경호원 / 삼합회 쌍도끼 집행자 / 불야성 혈마법사 / 황금 룰렛 골렘 | **삼합회 부두목 혈귀** | **🐲 마카오 삼합회 수장 흑룡 용왕** |
| **8. 블라디보스토크** | **🚪 금문**<br>`gate_gold.png` | `🦔 불굴의 가시`<br>극저온 해저 동토 | 동토의 불곰 변이체 / 해저 기지 전투 잠수부 / 극저온 냉기 드론 / 아다만티움 사이보그 | **신디케이트 부관 이반** | **🦾 해저 요새의 거인 ‘강철의 보리스’** |
| **9. 태평양 해연** | **🚪 플래티넘문**<br>`gate_platinum.png` | `🌀 심해 마력 동조`<br>초고압 심연 중력 왜곡 | 심해 발광 아귀 괴수 / 해연 소라게 골렘 / 수압 파쇄 세이렌 / 심연 촉수 기생체 | **해연의 수문장 리바이어던** | **🦑 심해의 지배자 크라켄 골렘** |
| **10. 히말라야 묘지** | **🚪 플래티넘문**<br>`gate_platinum.png` | `❄️ 극한의 심장`<br>해발 8천m 절대영도 | 해발 8천 설산 망령 / 얼어붙은 등반가 구울 / 빙룡 뼈조각 와이번 / 만년설 빙하 골렘 | **고룡 묘지 수호 거신병** | **🦴 태고의 재앙 ‘서리 본 드래곤’** |
| **11. 시베리아·사막** | **🚪 금문**<br>`gate_gold.png` | `⚔️ 학살자의 투기`<br>열사 모래폭풍 & 혹한 | 동토의 서리 늑대기병 / 타클라마칸 모래 전갈 / 유리 사막 아누비스 / 열사 폭풍 정령 | **모래지옥 친위장 사하라** | **🦂 타클라마칸 사막 여왕 유리 스콜피온** |
| **12. 라인강·로키** | **🚪 플래티넘문**<br>`gate_platinum.png` | `🛡️ 대지의 용철`<br>화산 마그마 분출 지대 | 라인강 타락 마수병 / 유럽 침공 키메라 / 로키산맥 화염 임프 / 마그마 암석 거인 | **마수 군단장 벨제부브** | **🌋 북미 대재앙 ‘용암 베히모스’** |
| **13. 성층권 금문** | **🚪 금문**<br>`gate_gold.png` | `🛸 제3군단장 해킹망`<br>외계 모함 반중력장 | 화성 제국 강습 보병 / 반중력 플라즈마 드론 / 사이오닉 심문관 / 외계 중장갑 센추리온 | **이단자 참모 벨록 (구출전)** | **🛸 금문 외계 선봉 사령관 타르코스** |
| **14. 다이아몬드 게이트** | **🚪 다이아몬드문**<br>`gate_diamond.png` | `👑 사령군주의 종언`<br>황제의 절대 권역 (영혼각인 2배) | 황실 친위대 결사병 / 아공간 암살 팬텀 / 성층권 궤도 폭격기 / 차원 파쇄 거신 | **대장군 볼가르 & 여왕 시렌** | **👑 외계 제국 절대자 ‘무감정의 황제’** |

#### (C) 14대 작전 지역별 고유 16비트 환경 오브젝트 4프레임 모션 규격 (`region_obj_{1..14}_f{0..3}.png`)
어색하게 떠다니던 전체 공통 구름 레이어를 완전히 제거하고, **14대 지역마다 고유한 세계관 설정과 전장 테마에 100% 부합하는 16비트 레트로 환경 오브젝트**를 배치했습니다. 특히 과도한 픽셀 뒤틀림 대신 **은문(Silver Gate)과 동일한 부드러운 사인파 곡선(`ease-in-out` 1.8s)의 유영(Float) 애니메이션 및 절반 이하의 극미세 1px 변위**를 결합하여 흔들림이 훨씬 차분하고 자연스럽게 구동됩니다 ([build_all_14_region_objects.py](file:///D:/workspace/GEMINI/project_necro/tools/build_all_14_region_objects.py)):

| 지역 번호 및 테마 | 고유 전경 환경 오브젝트 구성 (`region_obj_N_f0..3.png`) | 4프레임 애니메이션 모션 기믹 |
| :--- | :--- | :--- |
| **1. 서울 을지로 (지하철·한옥시장)** | 을지로 청사초롱 가로등 & 지하 미궁 발광 보라색 독버섯 포자 | 청사초롱 붉은/푸른 비단등 살랑임 + 화로 불꽃 타오름 |
| **2. 북한산 성역 (신목 결계)** | 북한산 성역 초롱불 신목(神木) & 푸른 결계 룬스톤·수풀 | 신목 가지 잎사귀 흔들림 + 결계 룬스톤 발광 |
| **3. 인천항 부두 (밀수 카르텔)** | 인천항 부두 강철 크레인 쇠사슬 & 타오르는 화염 드럼통 | 크레인 쇠사슬 흔들림 + 기름 드럼통 픽셀 화염 일렁임 |
| **4. 설악산 대청봉 (설원 검문)** | 설악산 고드름 눈소나무 & 청풍 빙결정 클러스터 | 눈 덮인 솔잎 흔들림 + 청색 빙결정 프리즘 반사 |
| **5. 평양 지하벙커 (철통 요새)** | 지하벙커 방벽 기둥 & 적색 회전 경보등·철조망 탄약고 | **적색 회전 경보등(Beacon) 4단계 점멸 펄스** |
| **6. 도쿄 음양사 (신사 결계)** | 붉은 도리이 기둥 & 흩날리는 오후다(부적)·청록 여우불 | 흰색 부적 종이 펄럭임 + 청록색 여우불 부유 |
| **7. 마카오 불야성 (카지노 카르텔)** | 황금 반룡 기둥 & 붉은 비단 홍등·황금 화로 | 비단 홍등 흔들림 + 황금 화로 불꽃 타오름 |
| **8. 블라디보스토크 (해저 동토)** | 극저온 빙하 수정 기둥 & 동토의 눈보라 침엽수 | 동토 침엽수 가지 흔들림 + 빙하 표면 냉기 맥동 |
| **9. 태평양 해연 (심해 심연)** | 발광 심해 해조류(보라 켈프) 숲 & 튜브 산호초 기둥 | **해류에 맞춰 좌우로 부드럽게 넘실거리는 켈프 파동** |
| **10. 히말라야 묘지 (서리 본드래곤)** | 만년설 고룡 거대 늑골(해골) 기둥 & 푸른 영혼 화로 | 고룡 갈비뼈 고드름 반사 + 푸른 영혼불(Soul Fire) 일렁임 |
| **11. 시베리아·사막 (타클라마칸)** | 황금 룬 사막 오벨리스크 & 열사 선인장·메마른 고목 | 오벨리스크 고대 룬문자 황금빛 점멸 펄스 |
| **12. 라인강·로키산 (용암 마그마)** | 흑요석 화산 첨탑 & 분출하는 용암 불기둥 간헐천 | **주황색 용암 균열과 마그마 불꽃의 4단계 팽창/수축** |
| **13. 성층권 모함 (외계 결전)** | 반중력 플라즈마 파일런 & 부유하는 보라색 수정 코어 | **중력을 거스르고 상하로 부유(Levitation)하는 차원 파편** |
| **14. 다이아몬드 게이트 (종언)** | 황제의 다이아몬드 차원 수정 기둥 & 진홍빛 아공간 아크 | **크리스탈 코어의 회전 및 번개 방전(Plasma Arc) 맥동** |

#### (D) 차원문 내부 100% 순수 자연 2400px 와이드 파노라마 & 6웨이브 전진 스크롤링 엔진
- **설정 준수 (Pure Wild Nature Only)**: 차원문 내부 던전은 인공물·현대 건축물·철골이 전혀 존재하지 않는 **100% 순수 원시 자연 환경(석회 동굴, 신목 원시림, 해안 갯바위, 설산 빙벽, 심해 해구, 화산 마그마 등)**으로 구성됩니다.
- **2400px 와이드 파노라마 전장 (`battle_pano_{1..14}.png`) & 시차 패럴랙스 오브젝트 (`nature_props_pano_{1..14}.png`)**:
  - 1회용 단칸 배경 대신 **6개 웨이브(W1~W6) 전투 구간이 하나로 이어진 2400×360 와이드 파노라마 스트립**을 구축합니다.
- **웨이브 진행 시 카메라 스크롤 메커니즘**:
  - `Wave 1(척후)`: 입구 구역 (`background-position: 0%`)
  - `Wave 2(주력)`: 외곽 통로 (`background-position: 20%`)
  - `Wave 3(강습)`: 중심 구역 (`background-position: 40%`)
  - `Wave 4(정예)`: 위험 지대 (`background-position: 60%`)
  - `Wave 5(수문장)`: 결계 문턱 (`background-position: 80%`)
  - `Wave 6(보스)`: 최심부 보스 둥지 (`background-position: 100%`)
  - 몬스터 처치 및 다음 웨이브 진입 시, **영웅이 전진 보행 모션을 취하며 카메라가 0.95초 부드러운 가감속(`cubic-bezier(0.22, 1, 0.36, 1)`)으로 오른쪽 심층 구역으로 스크롤**되는 오락실/던전앤파이터식 횡스크롤 연출을 구현합니다.

---

### 8.4 인게임 실시간 전투 엔진 & `localStorage` 세이브 스키마 (`game.js` 핵심 규격)

1. **실시간 전투 루프 (`requestAnimationFrame`, 60FPS)**:
   - **아군 진영(좌측)**: 주인공 본체 + 소환수(최대 4~7기)가 우향(`Facing Right`)으로 서서 전진 및 공격.
   - **적군 진영(우측)**: 웨이브당 3~5마리의 몬스터가 좌향(`scaleX(-1)`)으로 스폰되어 접근.
   - **스킬 슬롯(1~4번 액티브 + 5번 궁극기 + F1~F4 다섯 친구 지원 호출)**:
     - 자동 전투(Auto-Cast) 토글과 수동 클릭을 모두 지원.
     - 데미지 플로팅 텍스트(일반: 흰색, 치명타: `--neon-gold` 크기 1.5배, 시체폭발/출혈: `--neon-pink`, 빙결: `--neon-cyan`, 오버힐 심판: 황금 번개)를 캔버스/DOM 위에 팝업 연출.
2. **영구 세이브 데이터 스키마 (`localStorage.getItem('NECRO_RPG_SAVE_V1')`)**:
   - 플레이어가 브라우저를 새로고침해도 현재 회차의 장비·골드와 회귀 메타 데이터(회귀 횟수, 특성/재능 Lv.1~10, 영혼 각인 슬롯)가 완벽히 보존되어야 합니다.

```javascript
const DEFAULT_SAVE_SCHEMA = {
    version: "3.0",
    currentClass: "necromancer",     // 12대 직업 중 현재 선택된 직업 ID
    player: {
        level: 1, exp: 0, gold: 500, manaStones: 50,
        currentRegion: 1, unlockedRegion: 1,
        equippedSet: { ring: null, weapon: null, armor: null, helmet: null, core: null },
        equippedUniques: [null, null], // 고유(Unique) 아이템 특수 슬롯 2칸
        equippedSkills: ["necro_1", "necro_2", "necro_3", "necro_4", "necro_ult"],
        inventory: []                  // 획득한 장비 보관함 (최대 30칸, 회귀 시 초기화)
    },
    regression: {
        count: 0,
        maxTraitSlots: 1,              // 1회귀 달성 시 2로 영구 증가
        maxTalentSlots: 1,             // 1회귀 달성 시 2로 영구 증가
        hasSoulEngravedSlot: false,    // 최초 Lv.10 달성 시 true로 영구 해금
        ownedTraits: { "trait_mana_flow": 1 },
        ownedTalents: { "talent_exp_surge": 1 },
        soulEngravedIds: [],           // Lv.10 도달 특성/재능 ID 배열
        equippedTraits: ["trait_mana_flow"],
        equippedTalents: ["talent_exp_surge"],
        equippedSoulSlot: null,        // 오직 soulEngravedIds 내 항목만 장착 가능
        unlockedCrossSkills: []        // 비급서/회귀로 영구 해금된 타 직업 스킬 ID 목록
    }
};
```
