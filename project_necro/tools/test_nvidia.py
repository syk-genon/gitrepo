import os, sys, re, requests

sys.stdout.reconfigure(encoding="utf-8")
ref = r"D:\workspace\GEMINI\project2100\scratch\generate_flux_base_trainee.py"
key = re.search(r'API_KEY\s*=\s*["\']([^"\']+)["\']', open(ref, encoding="utf-8").read()).group(1)
print("Loaded key prefix:", key[:15])

url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
payload = {
    "prompt": "pixel art test, small sword, pure white background",
    "mode": "base",
    "cfg_scale": 3.5,
    "width": 1024,
    "height": 1024,
    "steps": 15
}
try:
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    print("Response status:", resp.status_code)
    if resp.status_code == 200:
        data = resp.json()
        print("Artifacts count:", len(data.get("artifacts", [])))
    else:
        print("Response text:", resp.text[:300])
except Exception as e:
    print("Error:", e)
