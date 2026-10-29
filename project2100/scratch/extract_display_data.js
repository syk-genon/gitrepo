const fs = require('fs');
const code = fs.readFileSync('index.js', 'utf8');

function extractBlock(startMarker, endMarker) {
  const start = code.indexOf(startMarker);
  if (start === -1) return null;
  const end = code.indexOf(endMarker, start);
  if (end === -1) return null;
  return code.slice(start, end + endMarker.length);
}

// In index.js:
// const MONSTERS_DATABASE = { ... };
// const TRAIT_MUTATIONS = { ... };
// const TRAIT_PART_NAMES = { ... };
// const TRAITS_DATA = { ... };
// const FUSION_DATA = { ... };

console.log("has MONSTERS_DATABASE:", code.includes("const MONSTERS_DATABASE = {"));
console.log("has TRAIT_MUTATIONS:", code.includes("const TRAIT_MUTATIONS = {"));
console.log("has TRAIT_PART_NAMES:", code.includes("const TRAIT_PART_NAMES = {"));
console.log("has TRAITS_DATA:", code.includes("const TRAITS_DATA = {"));
console.log("has FUSION_DATA:", code.includes("const FUSION_DATA = {"));
