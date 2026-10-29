const fs = require('fs');

const fileChecks = [
  'assets/pixel_hero/weapons/katana_idle_0.png',
  'assets/pixel_hero/weapons/axe_idle_0.png',
  'assets/pixel_hero/weapons/crystal_sword_idle_0.png',
  'assets/pixel_hero/weapons/heavy_cannon_idle_0.png',
  'assets/pixel_hero/weapons/lava_launcher_idle_0.png',
  'assets/pixel_hero/armors/military_idle_0.png',
  'assets/pixel_hero/armors/leather_idle_0.png',
  'assets/pixel_hero/armors/nano_carbon_idle_0.png',
  'assets/pixel_hero/armors/hardlight_idle_0.png',
  'assets/pixel_hero/armors/yeti_fur_idle_0.png',
  'assets/pixel_hero/female_nemesis_idle_0.png',
  'assets/pixel_hero/male_nemesis_idle_0.png',
  'assets/pixel_hero/female_idle_0.png',
  'assets/pixel_hero/male_idle_0.png',
  'assets/pixel_vfx/vfx_slash_arc.png',
  'assets/pixel_vfx/vfx_axe_spin.png',
  'assets/pixel_vfx/vfx_laser_bolt.png',
  'assets/pixel_vfx/vfx_hit_burst.png',
  'assets/pixel_vfx/vfx_nemesis_burst.png',
  'assets/pixel_monsters/m_1_1_idle_0.png',
  'assets/pixel_monsters/m_1_1_attack.png',
  'assets/pixel_monsters/m_1_1_hit.png',
  'assets/pixel_monsters/m_14_boss_idle_0.png',
  'assets/pixel_monsters/m_14_boss_attack.png',
  'assets/pixel_monsters/m_14_boss_hit.png'
];

let allExist = true;
fileChecks.forEach(p => {
  const exists = fs.existsSync(p);
  console.log(`[File ${p}]: ${exists ? 'EXISTS' : 'MISSING'}`);
  if (!exists) allExist = false;
});

console.log('Asset Verification:', allExist ? 'ALL ASSETS READY ✅' : 'SOME ASSETS MISSING ❌');
