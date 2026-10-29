import os, sys, json, time, base64, requests
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

INVOKE_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}

prompt = (
    "2D mobile game character sprite asset, cute anime chibi survivor hero, "
    "wearing ragged worn off-white short-sleeve cotton t-shirt, ragged frayed denim shorts, "
    "bare skin arms, bare legs, wearing simple worn traveler boots, "
    "standing neutral A-pose combat stance, clean pure solid white background, "
    "high quality vector style cell shaded 2D game art, clean dark outlines, "
    "chibi 2.5 heads tall proportions, MapleStory and Arknights chibi aesthetic, full body, crisp details"
)

payload = {
    "prompt": prompt,
    "mode": "base",
    "cfg_scale": 3.8,
    "width": 1024,
    "height": 1024,
    "seed": 1004,
    "steps": 28
}

print("Invoking NVIDIA Flux 1-dev to generate high quality base trainee sprite...")
resp = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=120)
print("Status code:", resp.status_code)

if resp.status_code == 200:
    data = resp.json()
    artifacts = data.get("artifacts", [])
    if artifacts:
        b64_str = artifacts[0].get("base64")
        raw_bytes = base64.b64decode(b64_str)
        out_raw = r"C:\Users\exbxda13\project2100\assets\pixel_parts\flux_ragged_hero_raw.png"
        with open(out_raw, "wb") as f:
            f.write(raw_bytes)
        print(f"Saved raw Flux generation to {out_raw} ({len(raw_bytes)} bytes)")
    else:
        print("No artifacts returned:", data)
else:
    print("Error:", resp.text)
