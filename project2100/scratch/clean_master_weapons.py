from PIL import Image

def clean_male():
    im = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = im.size
    pix = im.load()
    out = im.copy()
    opix = out.load()
    
    # 1. Left hilt (x < 220, y: 350..620)
    for y in range(350, 620):
        for x in range(0, 220):
            r, g, b, a = pix[x, y]
            if a < 20: continue
            
            # x < 165: completely sword, no body parts
            if x < 165:
                opix[x, y] = (0, 0, 0, 0)
                continue
                
            # x: 165..220: check if skin or shirt
            is_skin = (r > 190 and g > 130 and b > 90 and (r - b) > 40)
            is_shirt = (r > 140 and g > 130 and b > 120 and abs(r - g) < 30 and abs(g - b) < 30)
            is_wristband = (y > 550 and x > 185 and r > 70 and g > 40 and b > 30 and r > g)
            
            if not is_skin and not is_shirt and not is_wristband:
                opix[x, y] = (0, 0, 0, 0)

    # 2. Right scabbard & blade (x: 350..w, y: 680..840)
    for y in range(680, 840):
        for x in range(340, w):
            r, g, b, a = pix[x, y]
            if a < 20: continue
            
            is_skin = (r > 180 and g > 125 and b > 85 and (r - b) > 35)
            # Sandals strap
            is_sandal = (y > 830 and r > 50 and g > 30 and b > 20)
            
            if not is_skin and not is_sandal:
                opix[x, y] = (0, 0, 0, 0)
                
    out.save("scratch/clean_male_master.png")
    print("Saved scratch/clean_male_master.png")

def clean_female():
    im = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    w, h = im.size
    pix = im.load()
    out = im.copy()
    opix = out.load()
    
    # 1. Bottom-left machete blade (x: 0..260, y: 590..800)
    for y in range(590, 800):
        for x in range(0, 260):
            r, g, b, a = pix[x, y]
            if a < 20: continue
            
            is_skin = (r > 190 and g > 140 and b > 110 and (r - b) > 35)
            if not is_skin:
                opix[x, y] = (0, 0, 0, 0)
                
    # 2. Right machete handle (x: 340..w, y: 530..630)
    for y in range(530, 630):
        for x in range(340, w):
            r, g, b, a = pix[x, y]
            if a < 20: continue
            
            is_skin = (r > 190 and g > 140 and b > 110 and (r - b) > 35)
            is_wristband = (r > 180 and g > 180 and b > 170)
            if not is_skin and not is_wristband:
                opix[x, y] = (0, 0, 0, 0)
                
    out.save("scratch/clean_female_master.png")
    print("Saved scratch/clean_female_master.png")

if __name__ == "__main__":
    clean_male()
    clean_female()
