# -*- coding: utf-8 -*-
with open("scratch/generated_78_fusions.js", "r", encoding="utf-8") as f:
    fusions_js = f.read()

with open("index.js", "r", encoding="utf-8") as f:
    index_content = f.read()

start_marker = "const FUSION_DATA = {"
end_marker = "const REGIONS_METADATA = {"

idx_start = index_content.find(start_marker)
idx_end = index_content.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print("Markers not found!")
    exit(1)

new_content = index_content[:idx_start] + fusions_js + "\n\n" + index_content[idx_end:]

with open("index.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully replaced FUSION_DATA in index.js")
