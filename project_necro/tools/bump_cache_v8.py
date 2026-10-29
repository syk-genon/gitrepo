# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['project_necro/display.html', 'project_necro/display.js', 'project_necro/display_data.js']:
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('?v=7', '?v=8')
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Bumped cache buster to ?v=8 in {fn}")
