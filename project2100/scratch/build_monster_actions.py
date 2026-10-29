import os
from PIL import Image, ImageEnhance, ImageDraw, ImageOps

monsters_dir = r"C:\Users\exbxda13\project2100\assets\pixel_monsters"

def process_monster(base_filename):
    filepath = os.path.join(monsters_dir, base_filename)
    if not os.path.exists(filepath):
        return

    name_without_ext = os.path.splitext(base_filename)[0]
    # Skip if it's already an action sprite
    if any(suffix in name_without_ext for suffix in ["_idle", "_attack", "_hit"]):
        return

    try:
        with Image.open(filepath) as im:
            base_im = im.convert("RGBA")
            w, h = base_im.size

            # =========================================================
            # 1. IDLE FRAMES (0, 1, 2, 3) - 16-Bit Classic Breathing
            # =========================================================
            # Frame 0: Base
            base_im.save(os.path.join(monsters_dir, f"{name_without_ext}_idle_0.png"))

            # Frame 1: Inhale rise (-2px up)
            f1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            f1.paste(base_im, (0, -2), base_im)
            f1.save(os.path.join(monsters_dir, f"{name_without_ext}_idle_1.png"))

            # Frame 2: Squash & stretch peak (Slightly taller & narrower, -3px up)
            # Resize image portion
            scaled_h = int(h * 1.05)
            scaled_w = max(1, int(w * 0.96))
            stretched = base_im.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)
            f2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            # align to bottom
            ox = (w - scaled_w) // 2
            oy = h - scaled_h - 2
            f2.paste(stretched, (ox, oy), stretched)
            f2.save(os.path.join(monsters_dir, f"{name_without_ext}_idle_2.png"))

            # Frame 3: Settle (+1px down)
            f3 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            f3.paste(base_im, (0, 1), base_im)
            f3.save(os.path.join(monsters_dir, f"{name_without_ext}_idle_3.png"))

            # =========================================================
            # 2. ATTACK POSE (Lunge thrust + claw claws energy)
            # =========================================================
            # Lean forward (+6px right in monster's facing direction)
            atk_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            # Stretch horizontally for lunge
            lunge_w = int(w * 1.08)
            lunge_stretched = base_im.resize((lunge_w, h), Image.Resampling.NEAREST)
            atk_im.paste(lunge_stretched, (4, -2), lunge_stretched)
            
            # Draw 16-bit arcade scratch/swipe claw marks on the attack front
            d = ImageDraw.Draw(atk_im)
            # Claw marks (bright yellow/red slash energy)
            cl_x = w - 12
            cl_y = h // 2
            d.line([(cl_x - 14, cl_y - 12), (cl_x + 6, cl_y + 4)], fill=(255, 60, 40, 240), width=2)
            d.line([(cl_x - 12, cl_y - 2), (cl_x + 8, cl_y + 14)], fill=(255, 230, 60, 240), width=2)
            d.line([(cl_x - 16, cl_y + 6), (cl_x + 4, cl_y + 20)], fill=(255, 120, 40, 240), width=2)
            d.point((cl_x + 6, cl_y + 4), fill=(255, 255, 255, 255))
            d.point((cl_x + 8, cl_y + 14), fill=(255, 255, 255, 255))
            atk_im.save(os.path.join(monsters_dir, f"{name_without_ext}_attack.png"))

            # =========================================================
            # 3. HIT / FLINCH POSE (Knockback recoil + hit sparks)
            # =========================================================
            hit_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            # Recoil back (-5px) and slightly up (-3px)
            # Apply slight white/red tint for hit flash
            r, g, b, a = base_im.split()
            # Boost brightness for flash
            rgb = Image.merge("RGB", (r, g, b))
            enhancer = ImageEnhance.Brightness(rgb)
            flash_rgb = enhancer.enhance(1.4)
            flash_im = flash_rgb.convert("RGBA")
            flash_im.putalpha(a)
            
            hit_im.paste(flash_im, (-5, -3), flash_im)
            
            # Hit impact sparks on monster center
            dh = ImageDraw.Draw(hit_im)
            sp_x = w // 2 - 4
            sp_y = h // 2
            # 16-bit Star impact burst
            dh.line([(sp_x - 8, sp_y), (sp_x + 8, sp_y)], fill=(255, 255, 100, 255), width=2)
            dh.line([(sp_x, sp_y - 8), (sp_x, sp_y + 8)], fill=(255, 255, 100, 255), width=2)
            dh.point((sp_x, sp_y), fill=(255, 255, 255, 255))
            dh.point((sp_x - 4, sp_y - 4), fill=(255, 80, 50, 255))
            dh.point((sp_x + 4, sp_y + 4), fill=(255, 80, 50, 255))
            dh.point((sp_x + 4, sp_y - 4), fill=(255, 80, 50, 255))
            dh.point((sp_x - 4, sp_y + 4), fill=(255, 80, 50, 255))
            
            hit_im.save(os.path.join(monsters_dir, f"{name_without_ext}_hit.png"))

    except Exception as e:
        print(f"Error processing {base_filename}: {e}")

if __name__ == "__main__":
    count = 0
    all_files = [f for f in os.listdir(monsters_dir) if f.startswith("m_") and f.endswith(".png") and not any(k in f for k in ["_idle", "_attack", "_hit"])]
    print(f"Generating multi-frame action sprites for {len(all_files)} monsters...")
    for fn in all_files:
        process_monster(fn)
        count += 1
    print(f"Successfully created 16-bit multi-frame action sprites for {count} monsters!")
