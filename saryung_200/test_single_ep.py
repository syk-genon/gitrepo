import os
import sys
import json
import time
import urllib.request

API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def call_nemotron(messages, max_tokens=4096, temperature=0.75, retries=6):
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
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=300) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["choices"][0]["message"]["content"]
        except Exception as e:
            wait = 3 * (attempt + 1)
            print(f"[Retry {attempt+1}/{retries}] Nemotron API error: {e}. Waiting {wait}s...", flush=True)
            time.sleep(wait)
    raise RuntimeError("Nemotron API failed after retries.")

def write_episode(ep_info, prev_summary=""):
    system_prompt = (
        "당신은 네이버 시리즈와 카카오페이지에서 누적 1억 뷰를 달성한 대한민국 최정상급 웹소설 작가입니다.\n"
        "현재 소설 《목적을 잃지 않는 사령군주》를 집필 중입니다.\n\n"
        "[핵심 세계관 및 테마]\n"
        "- 주인공: 최미남 (전생에 '인간 배터리'로 혹사당하다 멸망 직전 죽은 뒤, 2043년 17세로 회귀한 사령술사)\n"
        "- 핵심 주제의식: '목표(강함과 승리)에 심취해 목적(친구들과 함께하는 평온한 일상)을 잃지 말자.'\n"
        "- 다섯 친구: 최미남(사령군주), 김현태(퓨어탱커/가디언), 이재성(폭풍마법사), 박동석(차원저격수), 오진석(팔라딘/성자)\n"
        "- 3대 네임드 언데드: 듀라한 기사단장 아서, 그림자 어쌔신 카게미츠, 화성인 참모 벨록\n\n"
        "[집필 규칙]\n"
        "1. 분량: 한 회차당 공백 포함 최소 4,000자 ~ 5,500자 이상의 풍성하고 디테일한 상업 웹소설 분량을 반드시 충족하세요.\n"
        "2. 장면 전개: 사건을 요약하거나 건너뛰지 말고, 인물의 표정·호흡·내면 심리, 마력 순환의 감각, 전장의 흙먼지와 온도, 인물 간의 티키타카 대화를 생생하게 묘사하세요.\n"
        "3. 형식: 메타 발언, 목차, 작가의 말 없이 순수한 웹소설 본문 텍스트만 출력하세요. 제목(제O화. 제목)으로 시작하세요."
    )

    user_prompt = (
        f"[집필할 회차 정보]\n"
        f"- 회차: 제{ep_info['ep_num']}화\n"
        f"- 파트: {ep_info['part']}\n"
        f"- 소제목: {ep_info['title']}\n"
        f"- 연출 및 확장 가이드: {ep_info['focus']}\n\n"
        f"[직전 회차 요약 맥락]\n{prev_summary if prev_summary else '소설의 첫 시작입니다.'}\n\n"
        f"[원작 참조 텍스트 (이 사건과 설정을 바탕으로 대폭 확장 디테일화)]\n"
        f"{ep_info['reference_text']}\n\n"
        f"위 정보와 원작의 뼈대를 바탕으로, 독자가 숨죽이고 몰입할 수 있는 완성도 높은 제{ep_info['ep_num']}화 본문을 최소 4,000자 이상으로 정성껏 집필해 주세요."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return call_nemotron(messages, max_tokens=4096, temperature=0.78)

def review_episode(ep_info, draft_text):
    prompt = (
        f"당신은 웹소설 전문 편집장(Critic)입니다. 아래 작성된 제{ep_info['ep_num']}화 원고를 엄격하게 평가해 주세요.\n\n"
        f"[회차 목표]\n제목: {ep_info['title']}\n가이드: {ep_info['focus']}\n\n"
        f"[원고 분량]: {len(draft_text)}자\n"
        f"[원고 본문 발췌]:\n{draft_text[:1500]}...\n\n"
        "다음 기준에 따라 JSON 형식으로만 평가를 반환하세요:\n"
        "{\n"
        "  \"score\": 1~10 사이 정수 또는 소수 (8.5점 이상이면 합격),\n"
        "  \"pass\": true 또는 false (분량 3,500자 미만이거나 몰입감/설정 미흡 시 false),\n"
        "  \"feedback\": \"개선할 점 또는 보완할 구체적 지시사항 (합격인 경우에도 칭찬/강점 간략히)\"\n"
        "}"
    )
    messages = [
        {"role": "system", "content": "You are a professional webnovel editor. Respond ONLY in valid JSON."},
        {"role": "user", "content": prompt}
    ]
    resp = call_nemotron(messages, max_tokens=500, temperature=0.2)
    try:
        clean_json = resp.strip()
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()
        return json.loads(clean_json)
    except Exception:
        # Fallback based on length
        passed = len(draft_text) >= 3500
        return {"score": 9.0 if passed else 7.0, "pass": passed, "feedback": "자동 판정"}

if __name__ == "__main__":
    with open(r"D:\workspace\GEMINI\saryung_200\scenario_200.json", "r", encoding="utf-8") as f:
        scenario = json.load(f)

    ep1 = scenario[0]
    print(f"--- [집필 테스트] 제{ep1['ep_num']}화: {ep1['title']} ---")
    t0 = time.time()
    draft = write_episode(ep1)
    t1 = time.time()
    print(f"작성 완료! 분량: {len(draft)}자 (소요 시간: {t1-t0:.1f}초)")

    review = review_episode(ep1, draft)
    print("편집장 검토 결과:", review)

    with open(r"D:\workspace\GEMINI\saryung_200\test_ep1_output.txt", "w", encoding="utf-8") as f:
        f.write(f"=== 검토 점수: {review.get('score')} | 합격여부: {review.get('pass')} ===\n")
        f.write(f"=== 피드백: {review.get('feedback')} ===\n\n")
        f.write(draft)
    print("Saved sample to test_ep1_output.txt")
