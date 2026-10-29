const fs = require("fs");
const code = fs.readFileSync("index.js", "utf8");

// Extract FUSION_DATA
const match = code.match(/const FUSION_DATA = \{([\s\S]*?)\n\};/);
if (!match) {
  console.error("Could not find FUSION_DATA");
  process.exit(1);
}

const fData = eval("({" + match[1] + "})");
const keys = Object.keys(fData);
console.log(`Total fusions in index.js: ${keys.length}`);

keys.forEach((k, idx) => {
  const f = fData[k];
  console.log(`${idx + 1}. [${k}] ${f.name} (${f.req.join(" + ")}): ${f.description}`);
});
