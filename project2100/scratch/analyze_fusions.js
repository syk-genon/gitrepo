const fs = require("fs");
const code = fs.readFileSync("index.js", "utf8");

// Extract FUSION_DATA keys
const fusionDataMatch = code.match(/const FUSION_DATA = \{([\s\S]*?)\n\};/);
let fkeys = [];
if (fusionDataMatch) {
  const inner = fusionDataMatch[1];
  const re = /^\s*([a-z0-9_]+):\s*\{/gm;
  let match;
  while ((match = re.exec(inner)) !== null) {
    fkeys.push(match[1]);
  }
}
console.log(`Defined fusions in FUSION_DATA: ${fkeys.length}`);

// Extract all hasFusion("...")
const hasRe = /hasFusion\(["']([^"']+)["']\)/g;
const implemented = new Set();
let hm;
while ((hm = hasRe.exec(code)) !== null) {
  implemented.add(hm[1]);
}
console.log(`Implemented in hasFusion logic: ${implemented.size}`);

const missing = fkeys.filter(k => !implemented.has(k));
console.log(`Missing fusions (${missing.length}):`, missing);

const dead = [...implemented].filter(k => !fkeys.includes(k));
console.log(`Dead/legacy fusions (${dead.length}):`, dead);
