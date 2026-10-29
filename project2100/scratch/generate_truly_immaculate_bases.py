from PIL import Image

def generate_truly_immaculate_bases():
    # 1. MALE
    im = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = im.size
    pix = im.load()
    out = im.copy()
    opix = out.load()
    
    # Right sword blade / scabbard: x in 355..w, y in 680..830
    for y in range(680, 830):
        for x in range(355, w):
            r, g, b, a = pix[x, y]
            if a == 0: continue
            is_skin = (r > 140 and (r - g) >= 15 and (r - b) >= 25)
            is_sandal = (y > 810)
            if not is_skin and not is_sandal:
                opix[x, y] = (0, 0, 0, 0)
                
    # Left sword hilt: x in 0..186, y in 330..620
    for y in range(320, 620):
        for x in range(0, 186):
            opix[x, y] = (0, 0, 0, 0)
            
    # Hip touchup (x: 186..195, y: 500..550): ensure clean shorts color
    for y in range(500, 550):
        for x in range(186, 195):
            r, g, b, a = opix[x, y]
            if a > 0 and r < 100 and g < 60:
                opix[x, y] = (42, 54, 84, 255)
                
    out.save("assets/pixel_hero/master_male_clean.png")
    print("Saved assets/pixel_hero/master_male_clean.png")

    # 2. FEMALE
    fim = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    fw, fh = fim.size
    fpix = fim.load()
    fout = fim.copy()
    fopix = fout.load()
    
    # Left machete blade: any pixel at x < 210, y in 580..800 is machete
    for y in range(580, 800):
        for x in range(0, 210):
            fopix[x, y] = (0, 0, 0, 0)
            
    # Between x: 210..245, y in 590..780, only keep skin
    for y in range(590, 780):
        for x in range(210, 245):
            r, g, b, a = fpix[x, y]
            if a == 0: continue
            is_skin = (r > 150 and (r - g) >= 15 and (r - b) >= 25)
            if not is_skin:
                fopix[x, y] = (0, 0, 0, 0)
                
    # Right machete handle: any pixel at x > 385, y in 530..640 is machete
    for y in range(530, 640):
        for x in range(385, fw):
            fopix[x, y] = (0, 0, 0, 0)
            
    fout.save("assets/pixel_hero/master_female_clean.png")
    print("Saved assets/pixel_hero/master_female_clean.png")

generate_truly_immaculate_bases()
