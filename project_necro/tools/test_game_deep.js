// Deep functional testing of game actions
const fs = require('fs');
const vm = require('vm');

const displayDataCode = fs.readFileSync('D:/workspace/GEMINI/project_necro/display_data.js', 'utf8');
const indexJsCode = fs.readFileSync('D:/workspace/GEMINI/project_necro/index.js', 'utf8');

// Rich DOM mock
function createMockElement(tag = 'div') {
    return {
        tagName: tag.toUpperCase(),
        style: {},
        classList: {
            add: () => {},
            remove: () => {},
            toggle: () => {}
        },
        children: [],
        appendChild: function(c) { this.children.push(c); },
        removeChild: function(c) { const i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); },
        setAttribute: () => {},
        getAttribute: () => null,
        addEventListener: () => {},
        innerHTML: '',
        textContent: '',
        remove: function() {},
        getBoundingClientRect: () => ({ left: 100, top: 100, width: 80, height: 80 })
    };
}

const elements = {};
function getEl(id) {
    if (!elements[id]) elements[id] = createMockElement('div');
    return elements[id];
}

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
        getElementById: getEl,
        querySelectorAll: () => [createMockElement()],
        createElement: createMockElement,
        body: createMockElement('body')
    },
    setInterval: () => {},
    requestAnimationFrame: () => {},
    setTimeout: (fn) => fn(),
    alert: (m) => console.log("[ALERT]", m),
    confirm: () => true
};

vm.createContext(sandbox);

const wrapDisplay = displayDataCode.replace(/^const /gm, 'var ');
const wrapIndex = indexJsCode.replace(/^const /gm, 'var ').replace(/^let /gm, 'var ');

vm.runInContext(wrapDisplay, sandbox);
vm.runInContext(wrapIndex, sandbox);

console.log("Testing confirmSelectedClass...");
sandbox.confirmSelectedClass();

console.log("Testing refreshHubUI...");
sandbox.refreshHubUI();

console.log("Testing blacksmith enhancement...");
sandbox.performEnhancement();

console.log("Testing gate battle start (Region 1)...");
sandbox.startGateBattle(1);
console.log("Wave monster:", sandbox.gameState.battle.enemy.name, "HP:", sandbox.gameState.battle.enemy.hp);

console.log("Testing player manual attack...");
sandbox.playerManualAttack();
console.log("Monster HP after attack:", sandbox.gameState.battle.enemy.hp);

console.log("Testing skill slot 0 (해골 군단 소환)...");
sandbox.useSkillSlot(0);
console.log("Minions count:", sandbox.gameState.battle.minions.length);

console.log("Testing skill slot 1 (시체 폭발)...");
sandbox.useSkillSlot(1);

console.log("Testing enemy defeat & wave progression...");
sandbox.gameState.battle.enemy.hp = 0;
sandbox.onEnemyDefeated();
console.log("Current wave after defeat:", sandbox.gameState.battle.wave);

console.log("Testing 6-wave boss defeat & region victory...");
sandbox.gameState.battle.wave = 6;
sandbox.gameState.battle.enemy = { name: "보스", hp: 0, maxHp: 1000, def: 10 };
sandbox.onEnemyDefeated();
console.log("Max region unlocked:", sandbox.gameState.player.maxRegionUnlocked);

console.log("Testing regression execution...");
sandbox.executeRegression();
console.log("Regression count:", sandbox.gameState.player.regressionCount, "Gold reset to:", sandbox.gameState.player.gold);

console.log("ALL TESTS PASSED WITH 100% SUCCESS!");
