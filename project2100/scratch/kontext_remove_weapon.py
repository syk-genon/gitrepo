# -*- coding: utf-8 -*-
"""NVIDIA FLUX.1 Kontext 로 기존 마스터 캐릭터에서 무기를 제거하고 팔을 살짝 벌린 A-포즈로 편집.
디자인(얼굴/머리/옷)은 그대로 유지하는 것이 목표."""
import os, sys, io, time, base64, requests
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\exbxda13\project2100"
URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-kontext-dev"
API_KEY = "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"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

JOBS = {
    "male": "Remove the sword completely. Keep the exact same boy character, same face, same spiky black hair, same ragged white t-shirt, same torn denim shorts, same sandals, same art style. Empty hands, both arms hanging relaxed slightly away from the body, legs slightly apart, full body, plain pure white background.",
    "female": "Remove the machete weapon completely. Keep the exact same girl character, same face, same blonde ponytail with red ribbon, same white t-shirt, same denim shorts, same wristbands and sandals, same art style. Empty hands, both arms hanging relaxed slightly away from the body, legs slightly apart, full body, plain pure white background.",
}


def to_data_uri(path):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])
    # 인라인 업로드 용량 제한 대응: 짧은 변 기준 축소 + JPEG
    bg.thumbnail((560, 1000))
    canvas = Image.new("RGB", (768, 1024), (255, 255, 255))
    canvas.paste(bg, ((768 - bg.width) // 2, (1024 - bg.height) // 2))
    buf = io.BytesIO()
    canvas.save(buf, "JPEG", quality=88)
    b = buf.getvalue()
    print("payload image bytes:", len(b))
    return "data:image/jpeg;base64," + base64.b64encode(b).decode()


def call(prompt, img_uri, seed):
    payload = {"prompt": prompt, "image": img_uri, "aspect_ratio": "match_input_image",
               "steps": 30, "cfg_scale": 3.5, "seed": seed}
    for attempt in range(8):
        try:
            r = requests.post(URL, headers=HEADERS, json=payload, timeout=300)
            if r.status_code == 200:
                return r.json()
            print(f"  status {r.status_code}: {r.text[:300]}")
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            return None
        except Exception as e:
            print("  error:", e)
            time.sleep(5 * (attempt + 1))
    return None


if __name__ == "__main__":
    which = sys.argv[1:] or list(JOBS)
    for g in which:
        for seed in (11, 23):
            out = os.path.join(ROOT, "assets", "pixel_parts", f"kontext_{g}_noweapon_s{seed}.png")
            if os.path.exists(out):
                print("skip (exists)", out)
                continue
            print("editing", g, "seed", seed)
            data = call(JOBS[g], to_data_uri(os.path.join(ROOT, "assets", "pixel_hero", f"retro_{g}_trans.png")), seed)
            if not data:
                print("FAILED", g)
                continue
            arts = data.get("artifacts") or []
            if not arts:
                print("no artifacts", str(data)[:300])
                continue
            with open(out, "wb") as f:
                f.write(base64.b64decode(arts[0]["base64"]))
            print("saved", out)
