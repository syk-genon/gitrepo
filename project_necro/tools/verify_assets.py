# -*- coding: utf-8 -*-
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = r"D:\workspace\GEMINI\project_necro"
js_files = [os.path.join(root, "display_data.js"), os.path.join(root, "display.js"), os.path.join(root, "display.html")]

missing = []
total_refs = 0
for jf in js_files:
    text = open(jf, encoding="utf-8").read()
    matches = re.findall(r'assets/[\w\./\-_]+\.(?:png|jpg)', text)
    for m in matches:
        total_refs += 1
        full_path = os.path.join(root, m.replace("/", "\\"))
        if not os.path.exists(full_path):
            missing.append((os.path.basename(jf), m))

print(f"Total asset references scanned: {total_refs}")
if missing:
    print(f"MISSING ASSETS ({len(missing)}):")
    for f, m in set(missing):
        print(f"  [{f}] -> {m}")
else:
    print("SUCCESS: ALL ASSETS VERIFIED ON DISK! Zero 404s.")
