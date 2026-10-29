from PIL import Image

def mirror_arm_and_patch():
    # 1. MALE
    m = Image.open("scratch/perfect_male_base.png").convert("RGBA")
    
    # Left arm (viewer's right): x: 340..420, y: 410..600
    # Let's crop it from the original retro_male_trans.png
    orig_m = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    # Left arm is at x: 330..430, y: 410..650 in orig_m
    left_arm = orig_m.crop((340, 410, 430, 650))
    # Flip it horizontally
    mirrored_arm = left_arm.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Paste onto viewer's left arm position (x: 155..245, y: 410..650)
    # But only where alpha > 0 and only on the left side (x < 225)
    w, h = m.size
    mpix = m.load()
    arm_pix = mirrored_arm.load()
    aw, ah = mirrored_arm.size
    
    # The boy's right shoulder joint is at y=400, x=190
    paste_x = 155
    paste_y = 405
    
    # Clear the left area where the cut was: x: 150..220, y: 350..620
    # First restore clean shirt/body from orig_m for x > 210
    for y in range(350, 620):
        for x in range(0, 195):
            mpix[x, y] = (0, 0, 0, 0)
            
    # Paste the mirrored arm onto canvas under torso
    arm_canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    arm_canvas.paste(mirrored_arm, (paste_x, paste_y))
    
    # Composite: arm_canvas behind body!
    # Where m has alpha > 100 and x > 195, m takes priority. Where m is transparent at x: 155..210, arm_canvas fills!
    final_m = Image.alpha_composite(arm_canvas, m)
    final_m.save("scratch/mirrored_clean_male.png")
    print("Saved mirrored_clean_male.png")

    # 2. FEMALE
    f = Image.open("scratch/final_clean_female.png").convert("RGBA")
    fpix = f.load()
    # Fill the tiny hand gap at x: 365..380, y: 570..595 with skin/shorts color
    # Between shorts hem (y: 570) and fingers (y: 595)
    for y in range(565, 595):
        for x in range(365, 385):
            if fpix[x, y][3] == 0:
                # if upper part, fill denim; if lower part, fill skin
                if y < 575:
                    fpix[x, y] = (45, 68, 105, 255) # denim
                else:
                    fpix[x, y] = (250, 210, 190, 255) # skin
                    
    f.save("scratch/mirrored_clean_female.png")
    print("Saved mirrored_clean_female.png")

mirror_arm_and_patch()
