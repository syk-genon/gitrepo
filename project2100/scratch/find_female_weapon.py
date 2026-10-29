from PIL import Image

def find_female_weapon():
    im = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    w, h = im.size
    pix = im.load()
    
    mask = im.copy()
    mpix = mask.load()
    
    # 1. 왼쪽 아래 마체테 칼날 (x: 0~240, y: 600~800)
    for y in range(600, 800):
        for x in range(0, 240):
            r, g, b, a = pix[x, y]
            if a > 50:
                # 다리 피부(r>200, g>150, b>120) 제외
                if not (r > 190 and g > 140 and b > 110):
                    mpix[x, y] = (255, 0, 0, 255)
                    
    # 2. 오른쪽 뒤 칼자루 (x: 350~501, y: 550~620)
    for y in range(540, 620):
        for x in range(350, w):
            r, g, b, a = pix[x, y]
            if a > 50:
                if not (r > 190 and g > 140 and b > 110):
                    mpix[x, y] = (255, 0, 0, 255)
                    
    mask.save("scratch/female_weapon_debug.png")
    print("Saved scratch/female_weapon_debug.png")

find_female_weapon()
