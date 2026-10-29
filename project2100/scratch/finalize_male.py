from PIL import Image

def finalize_male():
    im = Image.open("scratch/master_male_clean_perfect.png").convert("RGBA")
    pix = im.load()
    
    # 1. Fill calf contour (y: 695..740)
    for y in range(695, 740):
        # find the inner skin edge at x=340
        ref_c = pix[340, y]
        # outer edge of calf smoothly curves from x=375 down to 365
        outer_x = int(374 - (y - 695) * 0.2)
        for x in range(340, outer_x):
            if pix[x, y][3] == 0:
                pix[x, y] = (248, 208, 180, 255)
        # outline at outer_x
        pix[outer_x, y] = (140, 60, 50, 255)
        
    # 2. Fix hip patch at x: 172..195, y: 490..545
    # Replace the dark brown with blue denim shorts matching (45, 60, 90, 255)
    for y in range(490, 545):
        for x in range(165, 195):
            r, g, b, a = pix[x, y]
            if a > 0:
                # if brown patch
                if r > 60 and g < 60 and b < 50:
                    pix[x, y] = (42, 54, 84, 255)
                    
    im.save("scratch/master_male_flawless.png")
    print("Saved master_male_flawless.png")

finalize_male()
