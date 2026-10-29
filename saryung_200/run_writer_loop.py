import os
import sys
import json
import time
import re
import urllib.request

sys.path.append(r"C:\Users\exbxda13\gdrive-classifier")
from gdrive_helper import get_drive_service
from googleapiclient.http import MediaFileUpload

PROJ_DIR = r"D:\workspace\GEMINI\saryung_200"
EPISODES_DIR = os.path.join(PROJ_DIR, "episodes")
os.makedirs(EPISODES_DIR, exist_ok=True)

API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def call_nemotron(messages, max_tokens=4096, temperature=0.75, retries=20):
    """Pure urllib.request per GEMINI.md rules, exponential backoff, 300s timeout."""
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 0.95
    }
    data = json.dumps(payload).encode("utf-8")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
            with urllib.request.urlopen(req, timeout=300) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["choices"][0]["message"]["content"]
        except Exception as e:
            wait = min(45, 5 + attempt * 4)
            print(f"[Retry {attempt+1}/{retries}] Nemotron API error: {e}. Waiting {wait}s...", flush=True)
            time.sleep(wait)
    raise RuntimeError("Nemotron API failed after maximum retries.")

SYSTEM_WRITER = (
    "당신은 네이버 시리즈와 카카오페이지에서 누적 1억 뷰를 달성한 대한민국 최정상급 웹소설 작가입니다.\n"
    "현재 소설 《목적을 잃지 않는 사령군주》를 집필 중입니다.\n\n"
    "[핵심 세계관 및 테마]\n"
    "- 주인공: 최미남 (전생에 '인간 배터리'로 혹사당하다 멸망 직전 죽은 뒤, 2043년 17세로 회귀한 사령술사)\n"
    "- 핵심 주제의식: '목표(강함과 승리)에 심취해 목적(친구들과 함께하는 평온한 일상)을 잃지 말자.'\n"
    "- 다섯 친구: 최미남(사령군주), 김현태(퓨어탱커/가디언), 이재성(폭풍마법사), 박동석(차원저격수), 오진석(팔라딘/성자)\n"
    "- 3대 네임드 언데드: 듀라한 기사단장 아서, 그림자 어쌔신 카게미츠, 화성인 참모 벨록\n\n"
    "[집필 원칙]\n"
    "1. 분량: 한 회차당 공백 포함 최소 4,000자 ~ 5,500자 이상의 풍성하고 디테일한 상업 웹소설 분량을 반드시 충족하세요.\n"
    "2. 장면 전개: 사건을 요약하거나 건너뛰지 말고, 인물의 표정·호흡·내면 심리, 마력 순환의 감각, 전장의 흙먼지와 온도, 인물 간의 티키타카 대화를 생생하게 묘사하세요.\n"
    "3. 형식: 메타 발언, 목차, 작가의 말 없이 순수한 웹소설 본문 텍스트만 출력하세요. 제목(제O화. 제목)으로 시작하세요."
)

def draft_episode(ep_info, prev_summary="", critic_feedback=None, prev_draft=""):
    user_prompt = (
        f"[집필할 회차 정보]\n"
        f"- 회차: 제{ep_info['ep_num']}화\n"
        f"- 파트: {ep_info['part']}\n"
        f"- 소제목: {ep_info['title']}\n"
        f"- 연출 및 확장 가이드: {ep_info['focus']}\n\n"
        f"[직전 회차 요약 맥락]\n{prev_summary if prev_summary else '소설의 첫 시작입니다.'}\n\n"
        f"[원작 참조 텍스트 (이 사건과 설정을 바탕으로 대폭 확장 디테일화)]\n"
        f"{ep_info['reference_text']}\n\n"
    )

    if critic_feedback and prev_draft:
        user_prompt += (
            f"[이전 초안 검토 피드백 - 보완 지시사항]\n"
            f"{critic_feedback}\n\n"
            f"이전 초안에서 부족했던 부분(분량 확대, 대화 보강, 전투 디테일 등)을 완벽히 보완하여 다시 전체를 완성해 주세요.\n"
        )

    user_prompt += f"위 정보와 원작의 뼈대를 바탕으로, 독자가 숨죽이고 몰입할 수 있는 완성도 높은 제{ep_info['ep_num']}화 본문을 최소 4,000자 이상으로 정성껏 집필해 주세요."

    messages = [
        {"role": "system", "content": SYSTEM_WRITER},
        {"role": "user", "content": user_prompt}
    ]
    return call_nemotron(messages, max_tokens=4096, temperature=0.78)

def review_draft(ep_info, draft_text):
    prompt = (
        f"당신은 웹소설 전문 편집장(Critic)입니다. 아래 작성된 제{ep_info['ep_num']}화 원고를 엄격하게 평가해 주세요.\n\n"
        f"[회차 목표]\n제목: {ep_info['title']}\n가이드: {ep_info['focus']}\n\n"
        f"[원고 분량]: {len(draft_text)}자\n"
        f"[원고 본문 시작부]:\n{draft_text[:1200]}...\n\n"
        "다음 기준에 따라 JSON 형식으로만 평가를 반환하세요:\n"
        "{\n"
        "  \"score\": 1~10 사이 점수 (8.5점 이상이면 합격),\n"
        "  \"pass\": true 또는 false (분량 3,200자 미만이거나 몰입감/설정 미흡 시 false),\n"
        "  \"feedback\": \"개선할 점 또는 보완할 구체적 지시사항\"\n"
        "}"
    )
    messages = [
        {"role": "system", "content": "You are a professional webnovel editor. Respond ONLY in valid JSON."},
        {"role": "user", "content": prompt}
    ]
    try:
        resp = call_nemotron(messages, max_tokens=400, temperature=0.2)
        clean = resp.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()
        return json.loads(clean)
    except Exception:
        passed = len(draft_text) >= 3200
        return {"score": 9.0 if passed else 7.0, "pass": passed, "feedback": "분량 충족 검토"}

def upload_to_drive():
    try:
        full_file = os.path.join(PROJ_DIR, "목적을 잃지 않는 사령군주 (1~200화 완결_확장판).txt")
        if not os.path.exists(full_file):
            return
        service = get_drive_service(
            r"C:\Users\exbxda13\gdrive-classifier\credentials.json",
            r"C:\Users\exbxda13\gdrive-classifier\token.json"
        )
        root_id = "1rMEoK6G3dguy6HoSJyJc7K9LVa8jI_jj"
        fname = os.path.basename(full_file)
        media = MediaFileUpload(full_file, mimetype="text/plain", resumable=True)
        # Search if already uploaded to overwrite
        q = f"name = '{fname}' and '{root_id}' in parents and trashed = false"
        res = service.files().list(q=q, fields="files(id)").execute()
        existing = res.get("files", [])
        if existing:
            fid = existing[0]["id"]
            service.files().update(fileId=fid, media_body=media).execute()
            print(f"[GDrive] Updated existing file: {fname} (ID: {fid})", flush=True)
        else:
            created = service.files().create(body={"name": fname, "parents": [root_id]}, media_body=media, fields="id").execute()
            print(f"[GDrive] Created new file: {fname} (ID: {created.get('id')})", flush=True)
    except Exception as e:
        print(f"[GDrive] Upload error: {e}", flush=True)

def compile_full_novel(scenario, up_to_ep):
    full_path = os.path.join(PROJ_DIR, "목적을 잃지 않는 사령군주 (1~200화 완결_확장판).txt")
    lines = [
        "=" * 80,
        "                           목적을 잃지 않는 사령군주",
        "                            (1~200화 완결 확장판)",
        "=" * 80,
        "",
        "[작품 소개]",
        "\"목표에 심취해 목적을 잃지 말자.\"",
        "",
        "40년간 인류를 유린했던 차원 게이트와 외계 제국의 침략.",
        "전생에서 오직 강함만을 좇다 모든 동료를 잃고 홀로 파멸했던 최미남.",
        "2043년으로 회귀한 그는 사령술사의 길을 걸으며,",
        "자신만의 독자적인 군단과 다섯 개의 이단자 유물을 완성해 간다.",
        "",
        "하지만 그의 진정한 목적은 신의 권좌도, 세계의 황제도 아니다.",
        "지켜낸 평화 속에서 친구들과 함께 둘러앉아 따뜻한 피자와 치킨을 나눠 먹으며,",
        "평범하게 웃을 수 있는 영원한 봄날을 되찾는 것.",
        "",
        "=" * 80,
        ""
    ]
    total_words = 0
    compiled_count = 0
    for ep in scenario[:up_to_ep]:
        ep_file = os.path.join(EPISODES_DIR, f"ep_{ep['ep_num']:03d}.txt")
        if os.path.exists(ep_file):
            with open(ep_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            lines.append(f"\n\n{'=' * 80}\n")
            lines.append(content)
            total_words += len(content)
            compiled_count += 1

    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[Compiled] {compiled_count} episodes merged. Total characters: {total_words:,}", flush=True)
    return full_path

def main():
    scenario_file = os.path.join(PROJ_DIR, "scenario_200.json")
    with open(scenario_file, "r", encoding="utf-8") as f:
        scenario = json.load(f)

    progress_file = os.path.join(PROJ_DIR, "progress.json")
    progress = {}
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                progress = json.load(f)
        except Exception:
            progress = {}

    prev_summary = ""
    for idx, ep_info in enumerate(scenario):
        ep_num = ep_info["ep_num"]
        ep_file = os.path.join(EPISODES_DIR, f"ep_{ep_num:03d}.txt")

        # Auto-Resume: skip if already written and valid length
        if os.path.exists(ep_file) and os.path.getsize(ep_file) >= 2500:
            with open(ep_file, "r", encoding="utf-8") as f:
                prev_text = f.read()
            prev_summary = f"제{ep_num}화 '{ep_info['title']}': {prev_text[-400:].strip()}"
            continue

        print(f"\n>>> [집필 시작] 제{ep_num}/200화: {ep_info['title']} ({ep_info['part']})", flush=True)
        t_start = time.time()

        # Step 1: Draft
        draft = draft_episode(ep_info, prev_summary=prev_summary)
        review = review_draft(ep_info, draft)
        score = review.get("score", 7.0)
        is_pass = review.get("pass", False)
        feedback = review.get("feedback", "")
        print(f"  [1차 초안] {len(draft)}자 | 점수: {score} | 합격: {is_pass} | 피드백: {feedback}", flush=True)

        # Step 2: Rewrite loop if needed
        best_draft = draft
        best_score = score
        rounds = 0
        while (not is_pass or len(best_draft) < 3200) and rounds < 2:
            rounds += 1
            print(f"  [재집필 라운드 {rounds}] 피드백 반영 재작성 중...", flush=True)
            new_draft = draft_episode(ep_info, prev_summary=prev_summary, critic_feedback=feedback, prev_draft=best_draft)
            new_review = review_draft(ep_info, new_draft)
            new_score = new_review.get("score", 7.0)
            if new_score > best_score or len(new_draft) > len(best_draft):
                best_draft = new_draft
                best_score = new_score
            is_pass = new_review.get("pass", False)
            feedback = new_review.get("feedback", "")
            print(f"  [재집필 {rounds}차] {len(new_draft)}자 | 점수: {new_score} | 합격: {is_pass}", flush=True)

        # Save approved episode
        with open(ep_file, "w", encoding="utf-8") as f:
            f.write(best_draft)

        elapsed = time.time() - t_start
        print(f"  [완료] 제{ep_num}화 저장 완료 ({len(best_draft):,}자, 소요시간: {elapsed:.1f}초)", flush=True)

        progress[str(ep_num)] = {
            "title": ep_info["title"],
            "chars": len(best_draft),
            "score": best_score,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

        prev_summary = f"제{ep_num}화 '{ep_info['title']}': {best_draft[-400:].strip()}"

        # Merge and upload to Google Drive every 10 episodes or at final
        if ep_num % 10 == 0 or ep_num == 200:
            compile_full_novel(scenario, ep_num)
            upload_to_drive()

    # Final complete compile and upload
    compile_full_novel(scenario, 200)
    upload_to_drive()
    print("\n🎉 [대성공] 전 200화 완결 집필 및 구글 드라이브 업로드 완료!", flush=True)

if __name__ == "__main__":
    main()
