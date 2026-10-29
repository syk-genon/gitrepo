const fs = require('fs');
const { MONSTERS_DATABASE, TRAIT_MUTATIONS, DISPLAY_WEAPONS, DISPLAY_ARMORS } = require('../display_data.js');

let missing = 0;
function check(path) {
  if (!fs.existsSync(path)) {
    console.error('MISSING FILE:', path);
    missing++;
  }
}

const motions = ['idle', 'run', 'attack', 'skill'];
const frames = { idle: 4, run: 6, attack: 4, skill: 4 };

// 1. Heroes
['male', 'female'].forEach(g => {
  motions.forEach(m => {
    for (let f = 0; f < frames[m]; f++) {
      check(`assets/pixel_hero/${g}_${m}_${f}.png`);
    }
  });
});

// 2. Weapons
DISPLAY_WEAPONS.forEach(w => {
  if (w.id === 'none') return;
  motions.forEach(m => {
    for (let f = 0; f < frames[m]; f++) {
      check(`assets/pixel_hero/weapons/${w.id}_${m}_${f}.png`);
    }
  });
});

// 3. Armors
DISPLAY_ARMORS.forEach(a => {
  if (a.id === 'none') return;
  motions.forEach(m => {
    for (let f = 0; f < frames[m]; f++) {
      check(`assets/pixel_hero/armors/${a.id}_${m}_${f}.png`);
    }
  });
});

// 4. Mutations
Object.values(TRAIT_MUTATIONS).forEach(part => {
  motions.forEach(m => {
    for (let f = 0; f < frames[m]; f++) {
      check(`assets/pixel_hero/mutations/${part}_${m}_${f}.png`);
    }
  });
});

// 5. Monsters
Object.values(MONSTERS_DATABASE).forEach(list => {
  list.forEach(m => {
    check(m.img);
  });
});

if (missing === 0) {
  console.log('SUCCESS: All 534 sprites and visual assets verified to exist on disk!');
} else {
  console.error(`FAILED: ${missing} assets missing.`);
  process.exit(1);
}
