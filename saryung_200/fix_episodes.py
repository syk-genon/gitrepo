"""
152화 끊김 복구 + 코드 기반 검수(QA) + 후처리 + 합본/드라이브 업로드.
- 순수 urllib(run_writer_loop.call_nemotron 재사용: 20회 재시도, 300초 타임아웃)
- Auto-Resume: fix_state.json 에 완료 회차 기록, 재실행 시 이어서 진행
"""
import os, re, sys, json, time, shutil, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJ = r"D:\workspace\GEMINI\saryung_200"
sys.path.insert(0, PROJ)
os.chdir(PROJ)

from run_writer_loop import call_nemotron, SYSTEM_WRITER, compile_full_novel, upload_to_drive, EPISODES_DIR

BACKUP = os.path.join(PROJ, "episodes_backup_before_fix")
STATE = os.path.join(PROJ, "fix_state.json")
TERMS = '.!?”’"\'…」』'

# ---------------------------------------------------------------- QA (코드 기반)
def is_truncated(t):
    t = t.rstrip()
    if t.endswith("[소설 완결]"):
        return False
    return t[-1] not in TERMS

def trim_to_last_sentence(t):
    t = t.rstrip()
    idx = max(t.rfind(c) for c in TERMS)
    return t[: idx + 1] if idx > 0 else t

def qa_issues(t):
    issues = []
    if is_truncated(t): issues.append("truncated")
    if len(t) < 4000: issues.append(f"short({len(t)})")
    if "**" in t: issues.append("markdown**")
    if re.search(r'\([\u4e00-\u9fff\u3040-\u30ff][^)]*\)', t): issues.append("hanja_paren")
    if re.search(r'\((?:[A-Za-z][A-Za-z ,\'\-:&]{3,})\)', t): issues.append("english_paren")
    return issues

# ---------------------------------------------------------------- 후처리
def clean_text(t):
    SB = "\u0000SCENE\u0000"
    t = re.sub(r'^\s*(\*\s*){3,}\s*$', SB, t, flags=re.M)      # 장면 구분선 보호
    t = re.sub(r'^\s*[-]{3,}\s*$', SB, t, flags=re.M)
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t, flags=re.S)         # **bold**
    t = t.replace("**", "")
    t = re.sub(r'(?<!\*)\*(?!\s)([^*\n]+?)(?<!\s)\*(?!\*)', r'‘\1’', t)  # *생각* -> ‘생각’
    t = t.replace("*", "")
    t = re.sub(r'\s*\([\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff・·\s,]+\)', '', t)          # 한자 병기
    t = re.sub(r'\s*\((?:[A-Za-z][A-Za-z ,\'\-:&]{3,})\)', '', t)                          # 영어 병기(Lv.1 등은 유지)
    t = re.sub(r'\s*[‘\'"]?벨제뷔트[’\'"]?', '', t)                                       # 원작에 없는 황제 이름
    t = t.replace("여섯 명(미남 포함)", "다섯 명")
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    t = t.replace(SB, "\n※ ※ ※\n")
    return t.strip()

# ---------------------------------------------------------------- 이어쓰기
def continue_episode(ep_info, base_text, nxt_title):
    tail = base_text[-2200:]
    short = len(base_text) < 4000
    want = "1,400~2,000자" if short else "900~1,600자"
    prompt = (
        f"[회차] 제{ep_info['ep_num']}화 '{ep_info['title']}' ({ep_info['part']})\n"
        f"[연출 가이드] {ep_info['focus']}\n"
        f"[다음 화 제목] {nxt_title}\n\n"
        f"아래는 이 회차 본문의 마지막 부분입니다. 출력 한도 때문에 이 지점에서 원고가 끊겼습니다.\n"
        f"-----\n{tail}\n-----\n\n"
        f"위 마지막 문장 바로 다음부터 이어서 써서 이 회차를 완결하세요.\n"
        f"- 분량: {want}\n"
        f"- 앞 내용을 반복하거나 요약하지 말고, 끊긴 지점에서 자연스럽게 이어지는 새 문장만 쓰세요.\n"
        f"- 마지막은 장면이 매듭지어지고 다음 화에 대한 궁금증(훅)이 남도록 마무리하세요.\n"
        f"- 한자 병기, 영어 병기, 마크다운(**, #), 제목, 해설, 메타 발언은 쓰지 마세요. 순수 본문만 출력하세요."
    )
    msgs = [{"role": "system", "content": SYSTEM_WRITER}, {"role": "user", "content": prompt}]
    return call_nemotron(msgs, max_tokens=4096, temperature=0.7)

def fix_one(ep_num, scenario):
    path = os.path.join(EPISODES_DIR, f"ep_{ep_num:03d}.txt")
    text = open(path, encoding="utf-8").read().strip()
    info = scenario[ep_num - 1]
    nxt = scenario[ep_num]["title"] if ep_num < len(scenario) else "(완결)"

    need_cont = is_truncated(text) or len(text) < 4000
    if need_cont:
        base = trim_to_last_sentence(text) if is_truncated(text) else text
        for attempt in range(4):
            add = continue_episode(info, base, nxt).strip()
            add = re.sub(r'^제\d+화[^\n]*\n+', '', add)          # 모델이 제목을 다시 붙인 경우
            add = clean_text(add)
            if add and not is_truncated(add):
                break
        else:
            add = trim_to_last_sentence(add)                       # 끝내 못 맞추면 마지막 완결 문장까지만
        text = base.rstrip() + ("\n\n" if not base.endswith("\n") else "") + add

    text = clean_text(text)
    issues = qa_issues(text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return ep_num, len(text), need_cont, issues

def main():
    scenario = json.load(open(os.path.join(PROJ, "scenario_200.json"), encoding="utf-8"))
    if not os.path.exists(BACKUP):
        shutil.copytree(EPISODES_DIR, BACKUP)
        print("[Backup] episodes -> episodes_backup_before_fix", flush=True)

    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    todo = [i for i in range(1, 201) if str(i) not in state]
    print(f"[Resume] done={len(state)} todo={len(todo)}", flush=True)

    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(fix_one, i, scenario): i for i in todo}
        for fut in as_completed(futs):
            i = futs[fut]
            try:
                ep_num, n, cont, issues = fut.result()
            except Exception as e:
                print(f"[FAIL] ep{i}: {e}", flush=True)
                continue
            with lock:
                state[str(ep_num)] = {"chars": n, "continued": cont, "issues": issues}
                json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"[OK] ep{ep_num} {n}자 continued={cont} issues={issues}", flush=True)

    failed = [i for i in range(1, 201) if str(i) not in state]
    print(f"\n[Done] fixed={len(state)} failed={failed}", flush=True)
    if not failed:
        compile_full_novel(scenario, 200)
        upload_to_drive()

if __name__ == "__main__":
    main()
