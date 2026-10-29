import urllib.request
import json

API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def test_chat(model_name):
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": "안녕하세요! 한 문장으로 인사해 주세요."}],
        "temperature": 0.7,
        "max_tokens": 100
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[{model_name}] Success:", data["choices"][0]["message"]["content"])
            return True
    except Exception as e:
        print(f"[{model_name}] Error:", e)
        return False

test_chat("nvidia/nemotron-3-ultra-550b-a55b")
