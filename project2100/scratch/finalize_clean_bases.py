from PIL import Image

def finalize_bases():
    # Female
    fim = Image.open("scratch/perfect_female_base.png").convert("RGBA")
    # 1. Clear any remnant to the right of hand (x > 395, y: 540..640)
    for y in range(530, 640):
        for x in range(395, fim.width):
            fim.putpixel((x, y), (0, 0, 0, 0))
            
    # 2. Clear brown machete handle between hand and thigh (x: 365..395, y: 560..585)
    fpix = fim.load()
    for y in range(560, 585):
        for x in range(365, 395):
            r, g, b, a = fpix[x, y]
            if a > 0:
                # If dark brown machete wood (r < 130 and g < 70 and b < 50)
                if r < 140 and g < 80 and b < 60:
                    fpix[x, y] = (0, 0, 0, 0)
                    
    fim.save("scratch/final_clean_female.png")
    print("Saved final_clean_female.png")

    # Male
    mim = Image.open("scratch/perfect_male_base.png").convert("RGBA")
    mpix = mim.load()
    
    # 1. Clear any sword remnants at x < 180, y: 320..620
    for y in range(320, 620):
        for x in range(180):
            mim.putpixel((x, y), (0, 0, 0, 0))
            
    # 2. Natural contour for right arm / sleeve / shorts (x: 175..205, y: 350..560)
    # The sleeve cuff ends at (182, 385).
    # From y=385 to 450: elbow curves from x=182 to 176 at y=425, back to 184 at y=460.
    # Forearm from y=460 to 520: from x=184 to 186.
    # Let's fill the arm skin / outline within this natural contour!
    skin_fill = (245, 205, 185, 255)
    skin_shadow = (220, 160, 140, 255)
    skin_outline = (160, 80, 70, 255)
    
    for y in range(385, 520):
        # determine natural outer x for elbow/arm
        if y < 425:
            outer_x = int(185 - (y - 385) * (9 / 40)) # 185 -> 176
        elif y < 460:
            outer_x = int(176 + (y - 425) * (8 / 35)) # 176 -> 184
        else:
            outer_x = int(184 + (y - 460) * (4 / 60)) # 184 -> 188
            
        # find the first non-transparent pixel in this row
        first_x = None
        for x in range(outer_x, 230):
            if mpix[x, y][3] > 100:
                first_x = x
                break
                
        if first_x and first_x > outer_x:
            # draw outline at outer_x
            mpix[outer_x, y] = skin_outline
            # fill shadow/skin between outer_x+1 and first_x
            for fill_x in range(outer_x + 1, first_x):
                if fill_x < outer_x + 3:
                    mpix[fill_x, y] = skin_shadow
                else:
                    mpix[fill_x, y] = skin_fill
                    
    # Also clean up any lingering sword bits near belt/shorts (x: 165..185, y: 520..560)
    for y in range(520, 560):
        for x in range(165, 184):
            mpix[x, y] = (0, 0, 0, 0)
            
    mim.save("scratch/final_clean_male.png")
    print("Saved final_clean_male.png")

finalize_bases()
