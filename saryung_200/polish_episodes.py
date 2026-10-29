"""2차 폴리싱: 한자 잔여 제거 / 닫히지 않은 따옴표 보정 / 겹친 문장·문단 제거 + 전 회차 재검증."""
import os, re, sys, json, shutil, collections

P = r"D:\workspace\GEMINI\saryung_200"
sys.path.insert(0, P); os.chdir(P)
from fix_episodes import qa_issues, is_truncated

ED = os.path.join(P, "episodes")
BK = os.path.join(P, "episodes_backup_after_fix1")
if not os.path.exists(BK):
    shutil.copytree(ED, BK)
    print("[Backup] episodes -> episodes_backup_after_fix1", flush=True)

CJK = r'\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff'

def strip_hanja(t):
    t = re.sub(rf'[{CJK}]+\(([가-힣A-Za-z ]+)\)', r'\1', t)              # 丹田(단전) -> 단전
    t = re.sub(rf'\s*\([^)\n]*[{CJK}][^)\n]*\)', '', t)                  # (次元의 裂隙), (白虎 Guild) 제거
    return t

def strip_leftover_cjk(t):
    return re.sub(rf'[{CJK}]', '', t)

def fix_quotes(t):
    out, fixed = [], 0
    for p in t.split("\n\n"):
        state = None
        for ch in p:
            if ch == '"':
                state = None if state == '"' else '"'
            elif ch == '“':
                state = '“'
            elif ch == '”':
                state = None
        if state == '"':
            p = p.rstrip() + '"'; fixed += 1
        elif state == '“':
            p = p.rstrip() + '”'; fixed += 1
        out.append(p)
    return "\n\n".join(out), fixed

def dedup(t):
    seen_p, seen_s, out, removed = set(), set(), [], 0
    for p in t.split("\n\n"):
        ps = p.strip()
        if len(ps) >= 25 and ps in seen_p:
            removed += 1; continue
        seen_p.add(ps)
        if len(ps) >= 25 and not ps.startswith('['):
            parts = re.split(r'(?<=[.!?”’"])\s+', ps)
            keep, dropped = [], 0
            for s in parts:
                k = s.strip()
                if len(k) >= 25 and not k.startswith('['):
                    if k in seen_s:
                        dropped += 1; continue
                    seen_s.add(k)
                keep.append(s)
            if dropped:
                removed += dropped
                ps = " ".join(keep)
                if not ps.strip():
                    continue
                p = ps
        out.append(p)
    return "\n\n".join(out), removed

def quote_unbalanced(t):
    n = 0
    for p in t.split("\n\n"):
        st = None
        for ch in p:
            if ch == '"': st = None if st == '"' else '"'
            elif ch == '“': st = '“'
            elif ch == '”': st = None
        n += 1 if st else 0
    return n

before = {"hanja": 0, "unbal": 0, "dup": 0}
log = {}
for i in range(1, 201):
    path = os.path.join(ED, f"ep_{i:03d}.txt")
    t = open(path, encoding="utf-8").read().strip()
    h0 = len(re.findall(rf'[{CJK}]', t)); u0 = quote_unbalanced(t)
    t = strip_hanja(t)
    left = re.findall(rf'.{{10}}[{CJK}]+.{{10}}', t)
    if left:
        log[i] = left
    t = strip_leftover_cjk(t)
    t, rm = dedup(t)
    t, qf = fix_quotes(t)
    t = re.sub(r'[ \t]+\n', '\n', t); t = re.sub(r'\n{3,}', '\n\n', t).strip()
    open(path, "w", encoding="utf-8").write(t)
    before["hanja"] += h0; before["unbal"] += u0; before["dup"] += rm

print("[Polish] hanja chars removed:", before["hanja"], "| unbalanced-quote paragraphs (before):", before["unbal"], "| duplicate sentences/paras removed:", before["dup"], flush=True)
if log:
    print("[Leftover CJK stripped bare, contexts]:", flush=True)
    for i, v in list(log.items())[:10]:
        print(f"  ep{i}: {v[:2]}", flush=True)

# ---- 전 회차 재검증 ----
eps = {i: open(os.path.join(ED, f"ep_{i:03d}.txt"), encoding="utf-8").read().strip() for i in range(1, 201)}
full = "\n".join(eps.values())
issues = {i: qa_issues(t) for i, t in eps.items()}
print("\n=== FINAL QA ===")
print("episodes:", len(eps), "| total chars:", sum(len(t) for t in eps.values()))
print("QA issues:", {i: v for i, v in issues.items() if v} or "none")
print("truncated:", [i for i, t in eps.items() if is_truncated(t)])
print("unbalanced-quote paragraphs (after):", sum(quote_unbalanced(t) for t in eps.values()))
print("CJK chars left:", len(re.findall(rf'[{CJK}]', full)), "| '**' left:", full.count("**"))
c = collections.Counter()
for t in eps.values():
    for s in set(s.strip() for s in re.split(r'(?<=[.!?”’"])\s+|\n+', t) if len(s.strip()) >= 25 and not s.strip().startswith('[')):
        c[s] += 1
print("sentences repeated across >=3 episodes:", sum(1 for k in c.values() if k >= 3))
within = 0
for t in eps.values():
    cc = collections.Counter(s.strip() for s in re.split(r'(?<=[.!?”’"])\s+|\n+', t) if len(s.strip()) >= 25 and not s.strip().startswith('['))
    within += sum(1 for k in cc.values() if k >= 2)
print("within-episode duplicate sentences left:", within)
lens = [len(t) for t in eps.values()]
print("len min/avg/max:", min(lens), sum(lens)//200, max(lens))
