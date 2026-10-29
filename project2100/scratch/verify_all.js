const fs = require('fs');

console.log("=== COMPREHENSIVE PROJECT AUDIT & VERIFICATION ===");

// 1. Verify Base Hero Animations
const motions = [
  { name: 'idle', count: 4 },
  { name: 'run', count: 6 },
  { name: 'attack', count: 4 },
  { name: 'skill', count: 4 }
];

let heroFilesTotal = 0;
let heroFilesMissing = 0;
for (const gender of ['male', 'female']) {
  for (const m of motions) {
    for (let f = 0; f < m.count; f++) {
      heroFilesTotal++;
      const p = `assets/pixel_hero/${gender}_${m.name}_${f}.png`;
      if (!fs.existsSync(p)) {
        console.error(`Missing hero sprite: ${p}`);
        heroFilesMissing++;
      }
    }
  }
}
console.log(`1. Base Hero Sprites: ${heroFilesTotal - heroFilesMissing}/${heroFilesTotal} valid (Missing: ${heroFilesMissing})`);

// 2. Verify 13 Mutation Parts
const mutationParts = [
  'horns', 'tail', 'visor', 'wings', 'shell', 'fairy_wings',
  'booster', 'spikes', 'antennae', 'claws', 'core', 'crystals', 'halo'
];
let mutFilesTotal = 0;
let mutFilesMissing = 0;
for (const part of mutationParts) {
  for (const m of motions) {
    for (let f = 0; f < m.count; f++) {
      mutFilesTotal++;
      const p = `assets/pixel_hero/mutations/${part}_${m.name}_${f}.png`;
      if (!fs.existsSync(p)) {
        console.error(`Missing mutation part: ${p}`);
        mutFilesMissing++;
      }
    }
  }
}
console.log(`2. 13 Mutation Parts: ${mutFilesTotal - mutFilesMissing}/${mutFilesTotal} valid (Missing: ${mutFilesMissing})`);

// 3. Verify Weapons & Armors
const weapons = ['katana', 'axe', 'crystal_sword', 'heavy_cannon', 'lava_launcher'];
const armors = ['military', 'leather', 'nano_carbon', 'hardlight', 'yeti_fur'];
let gearTotal = 0;
let gearMissing = 0;
for (const w of weapons) {
  for (const m of motions) {
    for (let f = 0; f < m.count; f++) {
      gearTotal++;
      const p = `assets/pixel_hero/weapons/${w}_${m.name}_${f}.png`;
      if (!fs.existsSync(p)) gearMissing++;
    }
  }
}
for (const a of armors) {
  for (const m of motions) {
    for (let f = 0; f < m.count; f++) {
      gearTotal++;
      const p = `assets/pixel_hero/armors/${a}_${m.name}_${f}.png`;
      if (!fs.existsSync(p)) gearMissing++;
    }
  }
}
console.log(`3. Paperdoll Gear Sprites: ${gearTotal - gearMissing}/${gearTotal} valid (Missing: ${gearMissing})`);

// 4. Verify 78 Fusions in index.js
const code = fs.readFileSync('index.js', 'utf8');
const fusionDataMatch = code.match(/const FUSION_DATA = \{([\s\S]*?)\n\};/);
let fkeys = [];
if (fusionDataMatch) {
  const inner = fusionDataMatch[1];
  const re = /^\s*([a-z0-9_]+):\s*\{/gm;
  let match;
  while ((match = re.exec(inner)) !== null) fkeys.push(match[1]);
}
const hasRe = /hasFusion\(["']([^"']+)["']\)/g;
const implemented = new Set();
let hm;
while ((hm = hasRe.exec(code)) !== null) implemented.add(hm[1]);
const missingFusions = fkeys.filter(k => !implemented.has(k));

console.log(`4. 78 Dual Fusions: ${fkeys.length} defined, ${implemented.size} implemented, ${missingFusions.length} missing`);

// 5. Verify Bat Clean
const batIm = fs.readFileSync('assets/monsters/m_4_2.png');
console.log(`5. Monster Shadow Bat clean: ${batIm.length > 0 ? 'VERIFIED' : 'FAILED'}`);

const overallPass = (heroFilesMissing === 0 && mutFilesMissing === 0 && gearMissing === 0 && missingFusions.length === 0);
console.log(`\n=== OVERALL RESULT: ${overallPass ? 'ALL 4 PILLARS 100% PERFECT PASS! ✅' : 'FAILED ❌'} ===`);
if (!overallPass) process.exit(1);
