import glob
import json
import os
import re
import shutil

EP_DIR = r"D:\workspace\GEMINI\saryung_200\episodes"
BACKUP_DIR = r"D:\workspace\GEMINI\saryung_200\episodes_backup_before_de_ai"

SFX_PREFIX_RE = re.compile(
    r"(?:콰|쾅|쿠|쿵|퍼|퍽|펑|파|팍|팟|피|핑|쉬|쉭|슈|슉|치|칙|지지|지직|위|윙|우|웅|스|슥|싹|서|석|투|툭|텅|탕|챙|쨍|쩌|쩍|찌|찍|드|득|덜|달|끼|끽|삐|삑|뽀|빠|빡|으|아|크|컥|헉|하|호|후|흐|꺼|끼|캬|샤|샥|푸|푹|철|찰|촤|촥|두|둑|구|국|부|북|루|룩|수|숙|무|묵|주|죽|추|축|트|특)[가-힣]*$"
)

def split_sentences_safe(para: str):
    """Split a narrative paragraph into sentences without breaking inside quotes or brackets."""
    sents = []
    buf = []
    depth_sq = 0
    depth_dq = 0
    depth_bk = 0
    n = len(para)
    i = 0
    while i < n:
        ch = para[i]
        buf.append(ch)
        if ch == '“':
            depth_dq += 1
        elif ch == '”':
            depth_dq = max(0, depth_dq - 1)
        elif ch == '‘':
            depth_sq += 1
        elif ch == '’':
            depth_sq = max(0, depth_sq - 1)
        elif ch in '[［〈《『':
            depth_bk += 1
        elif ch in ']］〉》』':
            depth_bk = max(0, depth_bk - 1)

        if depth_dq == 0 and depth_sq == 0 and depth_bk == 0:
            if ch in '.?!' and (i + 1 == n or para[i + 1] == ' '):
                prev_str = ''.join(buf[:-1])
                if not prev_str.endswith('Lv') and not prev_str.endswith('No') and not prev_str.endswith('vs'):
                    s = ''.join(buf).strip()
                    if s:
                        sents.append(s)
                    buf = []
                    while i + 1 < n and para[i + 1] == ' ':
                        i += 1
        i += 1
    rem = ''.join(buf).strip()
    if rem:
        sents.append(rem)
    return sents

def clean_em_dashes_in_line(line: str) -> str:
    s = line.strip()
    if not s:
        return line
    leading_dash = ""
    if s.startswith("──") or s.startswith("——") or s.startswith("――"):
        leading_dash = "──"
        line = s[2:].lstrip()

    # 1. Paired em-dashes: X—Y—조사
    def repl_paired(m):
        pre = m.group(1)
        inner = m.group(2).strip()
        post = m.group(3)
        if inner.startswith('[') or inner.startswith('‘') or inner.startswith('『') or '쉴드' in inner or '포션' in inner:
            return f"{pre} {inner}{post}"
        return f"{pre}{post}"

    line = re.sub(
        r"([가-힣a-zA-Z0-9\]’”]+)\s*[—―─]{1,2}\s*([^—―─\n]{2,75}?)\s*[—―─]{1,2}\s*([은는이가을를의에로와과도만까지마저조차부터]\b|[은는이가을를의에로와과도])",
        repl_paired,
        line,
    )

    # 2. Single mid-sentence em-dashes: left — right
    def repl_single(m):
        left = m.group(1)
        right = m.group(2)
        left_word = re.findall(r"[가-힣]+$", left)
        if left_word and SFX_PREFIX_RE.search(left_word[0]) and len(left_word[0]) <= 6:
            return m.group(0)
        if right.startswith('‘') or right.startswith('『') or right.startswith('['):
            return f"{left} {right}"
        return f"{left}, {right}"

    line = re.sub(
        r"([가-힣a-zA-Z0-9\]’”\)\}])\s*[—―─]{1,2}\s*([가-힣a-zA-Z0-9\[‘『“\(])",
        repl_single,
        line,
    )

    # 3. Also catch remaining mid-sentence ` — ` surrounded by spaces in non-SFX narrative
    def repl_spaced_dash(m):
        left = m.group(1)
        right = m.group(2)
        left_word = re.findall(r"[가-힣]+$", left)
        if left_word and SFX_PREFIX_RE.search(left_word[0]) and len(left_word[0]) <= 6:
            return m.group(0)
        return f"{left}, {right}"

    line = re.sub(r"(\S)\s+[—―─]{1,2}\s+(\S)", repl_spaced_dash, line)
    line = re.sub(r"[—―─]{2,}(?=[.”\"’'\s]|$)", "……", line)

    return (leading_dash + line) if leading_dash else line

def clean_parentheticals_in_line(line: str, is_title: bool = False) -> str:
    if is_title:
        return line
    s = line.strip()
    if not s:
        return line

    is_status = (s.startswith('[') or s.startswith('［') or s.startswith('〈') or s.startswith('•') or 'Lv.' in s)
    if is_status:
        def repl_status_paren(m):
            inner = m.group(1).strip()
            lv_m = re.search(r"(Lv\.\s*\d+|최대|전직 조건[^)]*|강화[^)]*)", inner)
            if re.search(r"[A-Za-z]{3,}", inner):
                if lv_m and not re.search(r"^[A-Za-z\s/·\'\’\-]+$", inner):
                    return f"({lv_m.group(1)})"
                return ""
            return m.group(0)
        line = re.sub(r"\s*\(([^)\n]{1,65})\)", repl_status_paren, line)
        return line

    line = line.replace("deepest sector(최심부)", "최심부")
    line = line.replace("폴드론(어깨 갑옷)", "어깨 갑옷")
    line = line.replace("그리브(정강이 받이)", "정강이 받이")
    line = line.replace("건틀릿(장갑)", "건틀릿")
    line = line.replace("퀴라스(흉갑)", "흉갑")

    def repl_narrative_paren(m):
        inner = m.group(1).strip()
        if re.match(r"^\d+$", inner) and m.start() < 3:
            return m.group(0)
        return ""

    line = re.sub(r"\s*\(([^)\n]{1,65})\)", repl_narrative_paren, line)
    return line

def de_ai_sentence_transforms(text: str) -> str:
    # 1. Remove pseudo-math, backtick code lines, and English sensor logs
    text = re.sub(r"(?m)^[ \t]*`[^`\n]+`[ \t]*(?::[ \t]*[^\n]+)?\n?", "", text)
    text = text.replace("‘∫(E=mc²) × Δ(차원좌표) ÷ P(확률) = ∞’", "허공에 푸른 마력의 룬과 정교한 차원 술식이 겹겹이 맞물려 돌아갔다.")
    text = re.sub(r"(?m)^[ \t]*〈(?:Warning|Conceptual Interference)[^〉\n]+〉[ \t]*\n?", "", text)
    text = text.replace(
        "[WARNING: GRAVITY CORE OVERLOAD. SYSTEM REBOOT INITIATED. VULNERABILITY WINDOW: 3.2 SECONDS.]",
        "[경고: 중력 코어 과부하. 시스템 재기동 개시. 무방비 노출 시간: 3.2초.]",
    )
    text = text.replace("충돌점에서의 연산.\n\n충돌점에서의 연산.", "충돌점에서의 연산.")

    # 2. Specific AI filler sentences
    text = text.replace("아니, ‘깨어졌다’는 표현조차 이 비현실적인 광경 앞에서는 빈약한 단어에 불과했다. ", "")
    text = text.replace("아니, ‘깨어졌다’는 표현조차 이 비현실적인 광경 앞에서는 빈약한 단어에 불과했다.\n", "")
    text = text.replace("서울, 아니 한때 수도라 불리던 이 땅의", "한때 수도라 불리던 서울의")
    text = text.replace("고통조차 느끼지 못하는 사람처럼, 아니 고통을 느낄 겨를조차 없는 기계처럼", "고통을 느낄 겨를조차 없는 기계처럼")
    text = text.replace("전생의 동료. 아니, 전생의 ‘소모품’ 중 하나.", "전생의 동료.")
    text = text.replace("인류의 구원. 아니, 더 정확히 말하자면 인류의 멸망을 막아내고,", "인류의 멸망을 막아내고,")
    text = text.replace("차가운 호수처럼 평온했다. 아니, 평온을 넘어선 ‘절대 영도’ 그 자체였다.", "차가운 호수처럼 고요하고 서늘했다.")
    text = text.replace("소리가 아니었다. 세상이라는 캔버스가 찢어지는 비명이었다.", "세상이라는 캔버스가 찢어지는 듯한 비명이 터졌다.")

    # 3. Over-nerdy science/math TMI replacements
    sci_replacements = [
        ("닿는 모든 것의 분자 운동을 정지시켰다", "닿는 모든 것을 숨결째 얼려버렸다"),
        ("공간의 분자 운동을 정지시켜 버리는", "공간 자체를 통째로 얼려버리는"),
        ("생명체의 분자 운동 정지", "생명체의 모든 움직임 정지"),
        ("‘생명체’의 분자 운동 정지", "‘생명체’의 모든 움직임 정지"),
        ("분자 운동을 정지", "모든 움직임을 정지"),
        ("분자 운동이 정지", "모든 움직임이 정지"),
        ("분자 단위로 분해되어", "흔적도 없이 부서져"),
        ("분자 단위로 쪼개", "흔적도 없이 쪼개"),
        ("대기 중의 수분 분자 하나하나가", "대기 중의 수분이"),
        ("대기 중의 수분 분자가", "대기 중의 수분이"),
        ("공기 분자 하나가", "공기 입자 하나하나가"),
        ("영하 200도에 육박하는 이질적인 마력풍이", "살을 에는 마력 폭풍이"),
        ("영하 273.15도라는 절대 영도의 벽", "절대 영도의 벽"),
        ("절대 영도(-273.15도)", "절대 영도"),
        ("차갑던 체온이 0.5도쯤 올라가는 감각", "차갑게 식었던 몸에 온기가 도는 감각"),
        ("최적의 RPM", "최적의 회전 속도"),
        ("연산 능력 300% 오버클럭", "연산 능력 한계 돌파"),
        ("연산 효율 294%. 뇌온도 42도.", "연산 능력 한계 돌파."),
        ("소스 코드처럼", "설계도처럼"),
        ("세계의 소스 코드를", "세계의 법칙 구조를"),
        ("단일 변수 독재 공식", "절대 동결의 법칙"),
        ("다변수 순환 공식", "사령 순환의 법칙"),
        ("엔트로피를 역전시키는", "소멸을 역전시키는"),
        ("패치를 때려 박는", "법칙을 덧씌우는"),
        ("성대가 얼어붙었기 때문이다.", "성대마저 얼어붙어 있었다."),
    ]
    for old_s, new_s in sci_replacements:
        text = text.replace(old_s, new_s)

    # 4. Inline "단순한 X가 아닌 Y" -> "Y" and "단순한 X가 아니라 Y" -> "Y"
    text = re.sub(
        r"(?:단순한|그저|단순히)\s+[^.?!\n,]{1,28}[이가]\s+아닌,?\s*",
        "",
        text,
    )
    text = re.sub(
        r"(?:그것은\s+|이것은\s+)?(?:단순한|그저|단순히)\s+[^.?!\n,]{1,28}[이가]\s+아니라,?\s*",
        "",
        text,
    )
    text = re.sub(
        r"(?:단순히|그저)\s+[^.?!\n,]{1,28}뿐만\s+아니라,?\s*",
        "",
        text,
    )

    # 5. Standalone sentence "(그것은 )?(단순한|그저|단순히) ~가 아니었다/아니다."
    text = re.sub(
        r"(?:^|(?<=[.?!]\s)|(?<=\n))[^.?!\n“”]{0,25}(?:단순한|그저|단순히)\s+[^.?!\n“”]{1,40}\s*아니(?:었다|다)\.\s*",
        "",
        text,
    )

    # 6. Narrative "아니, 더 정확히 말하자면..."
    text = re.sub(
        r"(?<!“)(?<!\")아니,\s*(?:더\s+)?(?:정확히|엄밀히|솔직히|사실상)\s*(?:말하자면|말하면|보자면|따지자면)?\s*",
        "",
        text,
    )

    # 7. Didactic endings: "~것이다." and "~기 때문이었다."
    didactic_endings = [
        ("시작한 것이다.", "시작했다."),
        ("발동된 것이다.", "발동되었다."),
        ("발동한 것이다.", "발동했다."),
        ("있었던 것이다.", "있었다."),
        ("들어온 것이다.", "들어왔다."),
        ("나간 것이다.", "나갔다."),
        ("나온 것이다.", "나왔다."),
        ("온 것이다.", "왔다."),
        ("선 것이다.", "섰다."),
        ("도달한 것이다.", "도달했다."),
        ("접속한 것이다.", "접속했다."),
        ("완성된 것이다.", "완성되었다."),
        ("강타한 것이다.", "강타했다."),
        ("무력화된 것이다.", "무력화되었다."),
        ("발생한 것이다.", "발생했다."),
        ("부서진 것이다.", "부서졌다."),
        ("토해낸 것이다.", "토해냈다."),
        ("부숴버린 것이다.", "부숴버렸다."),
        ("지워진 것이다.", "지워졌다."),
        ("그리웠던 것이다.", "그리웠다."),
        ("멈춘 것이다.", "멈췄다."),
        ("마련된 것이다.", "마련되었다."),
        ("일으킨 것이다.", "일으켰다."),
        ("했던 것이다.", "했다."),
        ("였던 것이다.", "였다."),
        ("있던 것이다.", "있었다."),
        ("없던 것이다.", "없었다."),
        ("된 것이다.", "되었다."),
        ("한 것이다.", "했다."),
        ("인 것이다.", "이다."),
        ("기 때문이었다.", "탓이었다."),
        ("기 때문이다.", "탓이다."),
    ]
    for old_e, new_e in didactic_endings:
        text = text.replace(old_e, new_e)

    # Process line by line
    lines = text.splitlines()
    cleaned_lines = []
    for idx, ln in enumerate(lines):
        ln = clean_parentheticals_in_line(ln, is_title=(idx == 0))
        ln = clean_em_dashes_in_line(ln)
        if idx > 0 and '“' not in ln and '"' not in ln and not ln.strip().startswith('‘'):
            ln = re.sub(r"^아니,\s+", "", ln)
            ln = re.sub(r"(?<=[.?!])\s+아니,\s+", " ", ln)
        ln = re.sub(r" {2,}", " ", ln).strip()
        cleaned_lines.append(ln)

    # Re-group into paragraphs and split long brick lines (>= 135 chars, >= 3 sentences)
    raw_paras = [p.strip() for p in re.split(r"\n\s*\n", "\n".join(cleaned_lines)) if p.strip()]
    final_paras = []
    for idx, p in enumerate(raw_paras):
        if idx == 0:
            final_paras.append(p)
            continue
        sublines = [sl.strip() for sl in p.splitlines() if sl.strip()]
        for sl in sublines:
            if (
                not sl.startswith("“")
                and not sl.startswith('"')
                and not sl.startswith("‘")
                and not sl.startswith("[")
                and not sl.startswith("［")
                and not sl.startswith("〈")
                and not sl.startswith("※")
                and len(sl) >= 135
            ):
                sents = split_sentences_safe(sl)
                if len(sents) >= 3 or (len(sl) >= 185 and len(sents) >= 2):
                    chunk = []
                    chunk_len = 0
                    for s in sents:
                        chunk.append(s)
                        chunk_len += len(s)
                        if len(chunk) >= 2 or chunk_len >= 85:
                            final_paras.append(" ".join(chunk))
                            chunk = []
                            chunk_len = 0
                    if chunk:
                        final_paras.append(" ".join(chunk))
                    continue
            final_paras.append(sl)

    return "\n\n".join(final_paras) + "\n"

def main():
    if not os.path.exists(BACKUP_DIR):
        shutil.copytree(EP_DIR, BACKUP_DIR)
        print(f"[Backup] {EP_DIR} -> {BACKUP_DIR}")

    eps = sorted(glob.glob(os.path.join(EP_DIR, "ep_*.txt")))
    before_stats = {"단순한_아니": 0, "아니_서술": 0, "본문_괄호": 0, "설명형_대시": 0, "벽돌문단_200자": 0, "총문단": 0}
    after_stats = {"단순한_아니": 0, "아니_서술": 0, "본문_괄호": 0, "설명형_대시": 0, "벽돌문단_200자": 0, "총문단": 0}

    def measure(txt, stats):
        stats["단순한_아니"] += len(re.findall(r"(?:단순한|그저|단순히)[^.?!\n]{1,40}아니(?:었|라|다)", txt))
        for idx, ln in enumerate(txt.splitlines()):
            s = ln.strip()
            if idx == 0 or not s:
                continue
            if '“' not in s and '"' not in s and not s.startswith('‘'):
                stats["아니_서술"] += len(re.findall(r"(?:^|(?<=[.?!]\s))아니,\s", s))
            if not (s.startswith('[') or s.startswith('［') or s.startswith('〈') or s.startswith('•') or 'Lv.' in s):
                stats["본문_괄호"] += len(re.findall(r"\([^)\n]{1,65}\)", s))
                for dm in re.finditer(r"([가-힣a-zA-Z0-9\]’”\)\}])\s*[—―─]{1,2}\s*([가-힣a-zA-Z0-9\[‘『“\(])", s):
                    lw = re.findall(r"[가-힣]+$", dm.group(1))
                    if not (lw and SFX_PREFIX_RE.search(lw[0]) and len(lw[0]) <= 6) and not s.startswith("──"):
                        stats["설명형_대시"] += 1
        paras = [x.strip() for x in txt.split("\n\n") if x.strip()]
        stats["총문단"] += len(paras)
        stats["벽돌문단_200자"] += sum(
            1 for x in paras
            if len(x) >= 200 and not x.startswith("“") and not x.startswith("[") and not x.startswith("‘")
        )

    total_chars = 0
    for p in eps:
        b_path = os.path.join(BACKUP_DIR, os.path.basename(p))
        orig = open(b_path, encoding="utf-8").read()
        measure(orig, before_stats)
        polished = de_ai_sentence_transforms(orig)
        measure(polished, after_stats)
        open(p, "w", encoding="utf-8").write(polished)
        total_chars += len(polished)

    print("=== DE-AI & DE-EXPLAINER POLISH SUMMARY ===")
    for k in before_stats:
        print(f"  {k}: {before_stats[k]:,} -> {after_stats[k]:,}")
    print(f"  Total episodes: {len(eps)}, Total chars: {total_chars:,} (avg {total_chars // len(eps):,}/ep)")

    # Re-compile full novel
    from run_writer_loop import compile_full_novel
    scenario = json.load(open(r"D:\workspace\GEMINI\saryung_200\scenario_200.json", encoding="utf-8"))
    out_file = compile_full_novel(scenario, 200)
    print(f"[Compiled] {out_file}")

if __name__ == "__main__":
    main()
