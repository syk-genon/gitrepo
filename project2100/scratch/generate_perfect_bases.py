from PIL import Image

def generate_perfect_bases():
    # 1. Male
    im = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = im.size
    pix = im.load()
    out = im.copy()
    opix = out.load()
    
    # Sword blade / scabbard on right: x in 355..w, y in 680..830
    for y in range(680, 830):
        for x in range(355, w):
            r, g, b, a = pix[x, y]
            if a == 0: continue
            # Skin has r > 140, r > g, and r - b > 25
            is_skin = (r > 140 and (r - g) >= 15 and (r - b) >= 25)
            # Sandal strap
            is_sandal = (y > 810)
            if not is_skin and not is_sandal:
                opix[x, y] = (0, 0, 0, 0)
                
    # Sword hilt on left: x in 0..180, y in 330..620
    # Everything at x < 172 is 100% sword
    for y in range(330, 620):
        for x in range(0, 172):
            opix[x, y] = (0, 0, 0, 0)
            
    # Touching points at x: 172..205, y: 480..580
    for y in range(480, 580):
        for x in range(172, 205):
            r, g, b, a = pix[x, y]
            if a == 0: continue
            is_sword = (abs(r - g) < 20 and abs(g - b) < 20 and r < 140) or (r < 110 and g < 60 and b < 50)
            if is_sword:
                # Replace with shorts or belt
                if y > 530:
                    opix[x, y] = (42, 54, 84, 255)
                else:
                    opix[x, y] = (95, 45, 35, 255)
                    
    out.save("scratch/master_male_clean.png")
    print("Saved master_male_clean.png")

    # 2. Female
    fim = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    fw, fh = fim.size
    fpix = fim.load()
    fout = fim.copy()
    fopix = fout.load()
    
    # Left machete blade: x in 0..250, y in 590..800
    for y in range(590, 800):
        for x in range(0, 250):
            r, g, b, a = fpix[x, y]
            if a == 0: continue
            is_skin = (r > 150 and (r - g) >= 15 and (r - b) >= 25)
            if not is_skin:
                fopix[x, y] = (0, 0, 0, 0)
                
    # Right machete handle: x in 375..fw, y in 530..640
    for y in range(530, 640):
        for x in range(375, fw):
            r, g, b, a = fpix[x, y]
            if a == 0: continue
            is_skin = (r > 150 and (r - g) >= 15 and (r - b) >= 25)
            is_wristband = (r > 180 and g > 180 and b > 170 and x < 395)
            if not is_skin and not is_wristband:
                fopix[x, y] = (0, 0, 0, 0)
                
    fout.save("scratch/master_female_clean.png")
    print("Saved master_female_clean.png")

generate_perfect_bases()
