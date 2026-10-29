const fs = require('fs');

const code = fs.readFileSync('index.js', 'utf8');

// Extract the 5 data blocks from index.js
const pStart = code.indexOf('const MONSTERS_DATABASE = {');
const pEnd = code.indexOf('const REGIONS_METADATA = {');

if (pStart === -1 || pEnd === -1) {
  console.error("Could not find start or end of data blocks!");
  process.exit(1);
}

const dataCode = code.slice(pStart, pEnd).trim();

// Add export / global assign for display
const fullDisplayData = `// PROJECT 2100 - Display Data Extracted from index.js
${dataCode}

// Weapon and Armor Definitions
const DISPLAY_WEAPONS = [
  { id: "none", name: "맨손 / 빈손 (Bare Hands)" },
  { id: "katana", name: "카타나 (Katana)" },
  { id: "axe", name: "전투 도끼 (Axe)" },
  { id: "crystal_sword", name: "크리스탈 소드 (Crystal Sword)" },
  { id: "heavy_cannon", name: "중기관포 (Heavy Cannon)" },
  { id: "lava_launcher", name: "용암 런처 (Lava Launcher)" }
];

const DISPLAY_ARMORS = [
  { id: "none", name: "기본 낡은 셔츠 & 반바지 (Ragged Clothes)" },
  { id: "military", name: "조선 군복 (Joseon Military)" },
  { id: "leather", name: "납 차폐 가죽 코트 (Shielded Leather)" },
  { id: "nano_carbon", name: "나노 카본 외골격 (Nano Carbon)" },
  { id: "hardlight", name: "중성자 하드라이트 슈트 (Hardlight)" },
  { id: "yeti_fur", name: "빅풋 예티 퍼 코트 (Yeti Fur)" }
];

if (typeof module !== 'undefined') {
  module.exports = { MONSTERS_DATABASE, TRAIT_MUTATIONS, TRAIT_PART_NAMES, TRAITS_DATA, FUSION_DATA, DISPLAY_WEAPONS, DISPLAY_ARMORS };
}
`;

fs.writeFileSync('display_data.js', fullDisplayData, 'utf8');
console.log('Successfully generated display_data.js! Length:', fullDisplayData.length);
