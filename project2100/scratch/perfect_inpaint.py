from PIL import Image, ImageFilter

def inpaint_image(orig_path, clean_path, female=False):
    orig = Image.open(orig_path).convert("RGBA")
    clean = Image.open(clean_path).convert("RGBA")
    w, h = orig.size
    
    opix = orig.load()
    cpix = clean.load()
    
    # Identify transparent holes that are INSIDE the character's bounding silhouette
    # In female:
    # 1. Thigh gap around x: 220..270, y: 680..750 (the machete blade behind leg)
    # 2. Left hip/denim area behind hand x: 340..440, y: 540..610
    
    # We can perform nearest-neighbor or horizontal/vertical interpolation from valid neighboring body pixels
    final = clean.copy()
    fpix = final.load()
    
    if female:
        # Patch 1: thigh gap (x: 215..260, y: 690..760)
        # Interpolate skin from x + 5 (inside the leg)
        for y in range(690, 760):
            # find rightmost skin pixel in leg
            rx = None
            for x in range(250, 220, -1):
                if fpix[x, y][3] > 100:
                    rx = x
                    break
            if rx:
                # leg width is roughly 25-30px, interpolate curve
                target_left = int(228 + (y - 690) * 0.18)
                for x in range(target_left, rx):
                    if fpix[x, y][3] == 0:
                        # use color from rx
                        c = fpix[rx, y]
                        fpix[x, y] = c
                        
        # Patch 2: behind left hip / hand (x: 340..430, y: 540..610)
        for y in range(540, 610):
            # check denim shorts color at x: 320, y
            ref_c = fpix[330, y]
            if ref_c[3] > 100:
                # fill across to hand boundary
                for x in range(330, 410):
                    if fpix[x, y][3] == 0:
                        fpix[x, y] = ref_c
                        
    else: # Male
        # Patch 1: knee/calf gap (x: 330..375, y: 680..740)
        for y in range(680, 740):
            # find skin color at x: 330, y
            ref_c = fpix[330, y]
            if ref_c[3] > 100:
                # calf contour
                max_x = int(368 - (y - 680) * 0.3)
                for x in range(330, max_x):
                    if fpix[x, y][3] == 0:
                        fpix[x, y] = ref_c
                        
        # Patch 2: waist / shirt / shorts gap (x: 160..215, y: 460..580)
        for y in range(460, 580):
            # ref from inside torso (x: 230, y)
            ref_c = fpix[230, y]
            if ref_c[3] > 100:
                min_x = 185 if y > 530 else 170
                for x in range(min_x, 230):
                    if fpix[x, y][3] == 0:
                        fpix[x, y] = ref_c
                        
    return final

m_inp = inpaint_image("assets/pixel_hero/retro_male_trans.png", "scratch/clean_male_master.png", female=False)
m_inp.save("scratch/master_male_seamless.png")

f_inp = inpaint_image("assets/pixel_hero/retro_female_trans.png", "scratch/clean_female_master.png", female=True)
f_inp.save("scratch/master_female_seamless.png")
print("Saved master_male_seamless.png and master_female_seamless.png")
