from PIL import Image, ImageDraw

def analyze_weapon(path, out_mask_path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    print(f"Analyzing {path} ({w}x{h})...")
    # Save a thumbnail with grid for precise bounding box detection
    grid_im = im.copy()
    from PIL import ImageDraw
    draw = ImageDraw.Draw(grid_im)
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill=(255, 0, 0, 100))
        draw.text((x+2, 10), str(x), fill=(255, 0, 0, 255))
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill=(0, 255, 0, 100))
        draw.text((10, y+2), str(y), fill=(0, 255, 0, 255))
    grid_im.save(out_mask_path)
    print(f"Saved {out_mask_path}")

analyze_weapon("assets/pixel_hero/retro_male_trans.png", "scratch/grid_male.png")
analyze_weapon("assets/pixel_hero/retro_female_trans.png", "scratch/grid_female.png")
