const fs = require('fs');

const html = fs.readFileSync('display.html', 'utf8');
const js = fs.readFileSync('display.js', 'utf8');

const idRegex = /getElementById\(['"]([^'"]+)['"]\)/g;
const ids = new Set();
let match;
while ((match = idRegex.exec(js)) !== null) {
  ids.add(match[1]);
}

console.log('Total unique IDs accessed in display.js:', ids.size);
let missing = 0;
ids.forEach(id => {
  // Ignore dynamic IDs or toast
  if (id === 'displayToast' || id.startsWith('mutToggleBtn_')) return;
  if (!html.includes(`id="${id}"`)) {
    console.error('MISSING ID in HTML:', id);
    missing++;
  } else {
    // console.log('Found ID:', id);
  }
});

if (missing === 0) {
  console.log('SUCCESS: All element IDs referenced in display.js exist in display.html!');
} else {
  console.error(`FAILED: ${missing} IDs missing.`);
  process.exit(1);
}
