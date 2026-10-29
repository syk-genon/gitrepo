// Test script to check index.js functions and references
const fs = require('fs');
const vm = require('vm');

const displayDataCode = fs.readFileSync('D:/workspace/GEMINI/project_necro/display_data.js', 'utf8');
const indexJsCode = fs.readFileSync('D:/workspace/GEMINI/project_necro/index.js', 'utf8');

const sandbox = {
    console: console,
    localStorage: {
        getItem: () => null,
        setItem: () => {},
        removeItem: () => {}
    },
    window: {
        addEventListener: () => {}
    },
    document: {
        getElementById: () => null,
        querySelectorAll: () => [],
        createElement: () => ({ style: {}, classList: { add: () => {}, remove: () => {} }, appendChild: () => {} }),
        body: { appendChild: () => {} }
    },
    setInterval: () => {},
    requestAnimationFrame: () => {},
    alert: () => {},
    confirm: () => true
};

vm.createContext(sandbox);

// Convert `const ` to `var ` so they bind to the global sandbox in vm
const wrapDisplay = displayDataCode.replace(/^const /gm, 'var ');
const wrapIndex = indexJsCode.replace(/^const /gm, 'var ').replace(/^let /gm, 'var ');

try {
    vm.runInContext(wrapDisplay, sandbox);
    console.log("display_data.js evaluated successfully.");
    vm.runInContext(wrapIndex, sandbox);
    console.log("index.js evaluated successfully.");
    console.log("CLASSES_DATA length:", Object.keys(sandbox.CLASSES_DATA).length);
    console.log("REGIONS_DATA length:", Object.keys(sandbox.REGIONS_DATA).length);
    console.log("UNIQUE_ITEMS_DATA length:", Object.keys(sandbox.UNIQUE_ITEMS_DATA).length);
    console.log("Initial player class:", sandbox.gameState.player.classId);
    console.log("Combat Power calculated:", sandbox.calculateCombatPower());
} catch (e) {
    console.error("Test failed:", e);
    process.exit(1);
}
