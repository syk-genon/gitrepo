// Test trait slots, fusions, parts, and unlocking logic
const fs = require('fs');

// Simple DOM mock
const dummyEl = {
  classList: { add: () => {}, remove: () => {}, contains: () => false },
  style: {},
  appendChild: () => {},
  innerHTML: '',
  textContent: '',
  dataset: {},
  parentNode: { appendChild: () => {} }
};
global.document = {
  getElementById: (id) => dummyEl,
  createElement: (tag) => dummyEl,
  querySelector: (sel) => dummyEl,
  querySelectorAll: (sel) => []
};
global.window = {};
global.alert = (msg) => console.log("[ALERT]", msg);

// Read index.js content and eval the data and helper functions
const content = fs.readFileSync('index.js', 'utf8');

// Test running in node VM
const vm = require('vm');
const context = {
  console,
  document: global.document,
  window: global.window,
  alert: global.alert,
  Image: function() { return { src: '', onerror: null }; },
  setInterval: () => 1,
  clearInterval: () => {},
  setTimeout: (fn) => fn(),
  Math,
  Date,
  JSON,
  Array,
  Object,
  Set,
  parseInt
};
vm.createContext(context);
const testRunner = `
console.log("=== Initial STATE ===");
console.log("unlockedTraitSlots:", STATE.unlockedTraitSlots);
console.log("equippedTraits:", STATE.equippedTraits);
console.log("ownedTraits:", STATE.ownedTraits);
console.log("activeParts:", getActiveMutationParts());
console.log("auraStage:", getActiveAuraStage());
console.log("activeFusions:", STATE.activeFusions);

console.log("\\n=== Testing Equip into Full Slots ===");
STATE.ownedTraits.push("blood_absorption");
equipTrait("blood_absorption"); // should fail because only 1 slot open and already occupied
console.log("equippedTraits after failed equip:", STATE.equippedTraits);

console.log("\\n=== Testing Region 2 Unlock ===");
STATE.unlockedTraitSlots = 2;
equipTrait("blood_absorption");
console.log("equippedTraits after slot 2 equip:", STATE.equippedTraits);
console.log("activeParts:", getActiveMutationParts());
console.log("auraStage:", getActiveAuraStage());
console.log("activeFusions:", STATE.activeFusions);

console.log("\\n=== Testing Region 3 Unlock & 3rd Trait ===");
STATE.unlockedTraitSlots = 3;
STATE.ownedTraits.push("cellular_shield");
equipTrait("cellular_shield");
console.log("equippedTraits after slot 3 equip:", STATE.equippedTraits);
console.log("activeParts:", getActiveMutationParts());
console.log("auraStage:", getActiveAuraStage());
console.log("activeFusions:", STATE.activeFusions);

console.log("\\n=== Testing 3-trait Ultimate Fusion ===");
unequipTraitSlot(0);
unequipTraitSlot(1);
unequipTraitSlot(2);
console.log("Equipped after clear:", STATE.equippedTraits);
STATE.ownedTraits.push("energy_discharge", "thermal_control", "meltdown_control");
equipTrait("energy_discharge");
equipTrait("thermal_control");
equipTrait("meltdown_control");
console.log("Equipped traits:", STATE.equippedTraits);
console.log("activeParts:", getActiveMutationParts());
console.log("auraStage:", getActiveAuraStage());
console.log("activeFusions:", STATE.activeFusions);

console.log("\\n=== Exhaustive 78 Pair Verification ===");
const traitKeys = Object.keys(TRAITS_DATA);
console.log("Total Traits count:", traitKeys.length);
let foundPairs = 0;
for (let i = 0; i < traitKeys.length; i++) {
  for (let j = i + 1; j < traitKeys.length; j++) {
    const f = getPairFusion(traitKeys[i], traitKeys[j]);
    if (!f) {
      throw new Error("Missing fusion pair for " + traitKeys[i] + " + " + traitKeys[j]);
    }
    foundPairs++;
  }
}
console.log("Exhaustive test verified all " + foundPairs + "/78 pairs successfully!");

console.log("\\nALL TESTS PASSED SUCCESSFULLY!");
`;

vm.runInContext(content + "\n" + testRunner, context);
