from PIL import Image

def test_clean():
    # Male
    m = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = m.size
    mpix = m.load()
    
    # Female
    f = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    fw, fh = f.size
    fpix = f.load()
    
    # For female:
    # Handle on right: x > 360, y: 540..620.
    # What are the hand pixels?
    # Hand is skin (r>200, g>140, b>110) or wristband (r>180, g>180, b>180).
    # Handle is dark brown wood (r: 60..110, g: 30..60, b: 20..40) and silver pommel (r>150, g>150, b>150, but at x>470)
    for y in range(540, 620):
        for x in range(350, fw):
            r, g, b, a = fpix[x, y]
            if a == 0: continue
            # If it's wood handle (dark brown / black) or pommel
            is_wood = (r < 140 and g < 90 and b < 80)
            is_pommel = (x > 470 and abs(r-g) < 15 and abs(g-b) < 15)
            if is_wood or is_pommel:
                fpix[x, y] = (0, 0, 0, 0)
                
    # Blade on left: x < 250, y: 590..800
    for y in range(590, 800):
        for x in range(0, 250):
            r, g, b, a = fpix[x, y]
            if a == 0: continue
            # leg is skin: r > 200, g > 150, b > 120 and r - b > 40
            is_skin = (r > 195 and g > 145 and b > 115 and (r - b) > 35)
            # leg outline: r in 150..200, g in 90..130, b in 80..110
            is_leg_outline = (r > 140 and g > 80 and b > 70 and r > g and (r - b) > 40)
            if not is_skin and not is_leg_outline:
                fpix[x, y] = (0, 0, 0, 0)
                
    f.save("scratch/test_clean_female.png")
    print("Saved test_clean_female.png")

    # For male:
    # Hilt on left: x < 210, y: 350..620
    for y in range(350, 620):
        for x in range(0, 210):
            r, g, b, a = pix = mpix[x, y]
            if a == 0: continue
            is_skin = (r > 190 and g > 130 and b > 90 and (r - b) > 35)
            is_shirt = (r > 150 and g > 140 and b > 130 and abs(r - g) < 25 and abs(g - b) < 25)
            is_belt = (y > 510 and x > 170 and r > 80 and g > 40 and b > 25)
            is_shorts = (y > 520 and b > r and b > 60)
            is_arm_outline = (r > 120 and g > 60 and b > 50 and (r - b) > 30)
            if not is_skin and not is_shirt and not is_belt and not is_shorts and not is_arm_outline:
                mpix[x, y] = (0, 0, 0, 0)
                
    # Blade on right: x > 350, y: 680..820
    for y in range(680, 820):
        for x in range(350, w):
            r, g, b, a = mpix[x, y]
            if a == 0: continue
            is_skin = (r > 185 and g > 125 and b > 85 and (r - b) > 35)
            is_leg_outline = (r > 120 and g > 70 and b > 60 and (r - b) > 30)
            is_sandal = (y > 810)
            if not is_skin and not is_leg_outline and not is_sandal:
                mpix[x, y] = (0, 0, 0, 0)
                
    m.save("scratch/test_clean_male.png")
    print("Saved test_clean_male.png")

test_clean()
