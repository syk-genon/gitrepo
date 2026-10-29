from PIL import Image

def build_perfect_male_master():
    orig = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = orig.size
    pix = orig.load()
    out = orig.copy()
    opix = out.load()
    
    # 1. Right sword blade / scabbard (x: 350..w, y: 680..830)
    # The calf has skin (r>180, g>120, b>80, r-b>35)
    # Sandal strap at y>810
    for y in range(680, 830):
        for x in range(350, w):
            r, g, b, a = pix[x, y]
            if a == 0: continue
            is_skin = (r > 175 and g > 115 and b > 75 and (r - b) > 30)
            is_sandal = (y > 810 and r > 40 and g > 20 and b > 15)
            if not is_skin and not is_sandal:
                opix[x, y] = (0, 0, 0, 0)
                
    # 2. Left sword hilt (x: 0..170, y: 340..600)
    # At x < 170, y in 340..600, it's 100% sword!
    for y in range(330, 600):
        for x in range(0, 172):
            opix[x, y] = (0, 0, 0, 0)
            
    # 3. For x: 172..200, y: 480..580:
    # Here was the tsuba (guard) and pommel base touching the shirt/shorts.
    # Sword guard is dark metallic / gold: r < 120 and g < 70 and b < 50
    # or brass ornament r: 180..220, g: 140..170, b: 30..60 (very low blue!)
    for y in range(480, 580):
        for x in range(172, 205):
            r, g, b, a = pix[x, y]
            if a == 0: continue
            is_sword_guard = (r < 110 and g < 60 and b < 50) or (r > 160 and g > 120 and b < 80)
            if is_sword_guard:
                # Replace with denim shorts or belt
                if y > 530:
                    opix[x, y] = (38, 48, 75, 255) # denim blue
                else:
                    opix[x, y] = (95, 45, 35, 255) # leather belt brown
                    
    out.save("scratch/master_male_clean_perfect.png")
    print("Saved master_male_clean_perfect.png")

build_perfect_male_master()
