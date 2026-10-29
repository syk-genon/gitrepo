# -*- coding: utf-8 -*-
import re, json

data_path = r"D:\workspace\GEMINI\project_necro\display_data.js"
with open(data_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update UNIQUE_ITEMS_DATA
unique_pat = re.compile(r'(\{\s*id:\s*(\d+),\s*name:\s*"[^"]+",\s*source:\s*"[^"]+",\s*icon:\s*")[^"]+("[\s\S]*?\})')
def rep_unique(m):
    item_id = m.group(2)
    return f"{m.group(1)}assets/ui/items_uniques/unique_{item_id}.png{m.group(3)}"

text = unique_pat.sub(rep_unique, text)

# 2. Update CLASSES_DATA setParts icon paths
# Find each class and its setParts
class_keys = [
    "necro", "guardian", "storm_wizard", "sniper", "priest",
    "assassin", "sword_master", "death_knight", "martial_king",
    "psionic_tactician", "berserker", "cryo_empress"
]

for ck in class_keys:
    # Match the class block
    # Within this class block, replace setParts icons
    # e.g., { part: "ring", name: "...", icon: "assets/ui/item_accessory.png", ... }
    for part in ["ring", "weapon", "armor", "helmet", "core"]:
        p_pat = re.compile(rf'("id":\s*"{ck}"[\s\S]*?part:\s*"{part}",[\s\S]*?icon:\s*")[^"]+(")')
        # Or match from class key:
        pass

# Let's do a reliable line-by-line or regex parser for classes:
# Split by "id": "..." or class definitions
lines = text.split("\n")
current_class = None
new_lines = []

for line in lines:
    # Check if a class starts
    m_cls = re.search(r'"([a-z_]+)":\s*\{', line)
    if m_cls and m_cls.group(1) in class_keys:
        current_class = m_cls.group(1)
    
    # Check set part
    m_part = re.search(r'part:\s*"([a-z]+)"', line)
    if m_part and current_class:
        part_name = m_part.group(1)
        # replace icon on this line
        line = re.sub(r'icon:\s*"assets/ui/[^"]+"', f'icon: "assets/ui/items_sets/set_{current_class}_{part_name}.png"', line)
    
    new_lines.append(line)

text = "\n".join(new_lines)

# 3. Append CLASS_PAPERDOLL_CONFIG at the bottom
paperdoll_config_code = """
// =========================================================================
// 6. 12대 직업 240x240 다중 레이어 페이퍼돌 구성 매핑 (PROJECT 2100 규격)
// =========================================================================
const CLASS_PAPERDOLL_CONFIG = {
    "necro": {
        body: "male_nemesis",
        armor: null,
        weapon: "crystal",
        mutation: "wings",
        wings: null
    },
    "guardian": {
        body: "male",
        armor: "hardlight",
        weapon: "heavy",
        mutation: "spikes",
        wings: null
    },
    "storm_wizard": {
        body: "female",
        armor: null,
        weapon: "crystal",
        mutation: "halo",
        wings: null
    },
    "sniper": {
        body: "male",
        armor: "military",
        weapon: "heavy",
        mutation: "visor",
        wings: null
    },
    "priest": {
        body: "female",
        armor: "female_hardlight",
        weapon: "crystal",
        mutation: "halo",
        wings: "fairy_wings"
    },
    "assassin": {
        body: "male",
        armor: "leather",
        weapon: "katana",
        mutation: "claws",
        wings: null
    },
    "sword_master": {
        body: "male",
        armor: "leather",
        weapon: "katana",
        mutation: "core",
        wings: null
    },
    "death_knight": {
        body: "male_nemesis",
        armor: null,
        weapon: "lava",
        mutation: "horns",
        wings: null
    },
    "martial_king": {
        body: "male",
        armor: "leather",
        weapon: "axe",
        mutation: "booster",
        wings: null
    },
    "psionic_tactician": {
        body: "male",
        armor: null,
        weapon: "crystal",
        mutation: "antennae",
        wings: null
    },
    "berserker": {
        body: "male",
        armor: "leather",
        weapon: "axe",
        mutation: "spikes",
        wings: null
    },
    "cryo_empress": {
        body: "female_nemesis",
        armor: null,
        weapon: "crystal",
        mutation: "crystals",
        wings: null
    }
};
"""

if "CLASS_PAPERDOLL_CONFIG" not in text:
    text += "\n" + paperdoll_config_code

with open(data_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated display_data.js with genuine item icons and CLASS_PAPERDOLL_CONFIG successfully!")
