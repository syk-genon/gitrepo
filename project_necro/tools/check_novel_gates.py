# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding="utf-8")
text = open(r"D:\workspace\GEMINI\test.txt", encoding="utf-8").read()

for kw in ["철문", "동문", "은문", "금문", "플래티넘", "다이아몬드문", "차원문", "문으로", "문을 열고", "게이트"]:
    matches = [m.start() for m in re.finditer(re.escape(kw), text)]
    print(f"=== {kw} ({len(matches)} matches) ===")
    for pos in matches[:3]:
        snippet = text[max(0, pos-60):min(len(text), pos+120)].replace("\n", " ")
        print("  ->", snippet)
