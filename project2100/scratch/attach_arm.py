from PIL import Image

def attach_mirrored_arm():
    base = Image.open("assets/pixel_hero/master_male_clean.png").convert("RGBA")
    w, h = base.size
    
    # Crop the pristine left arm from base (x: 345..435, y: 410..630)
    left_arm = base.crop((345, 410, 435, 630))
    mirrored = left_arm.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Hand / arm width is 90, height is 220
    # The right shoulder sleeve ends at x=200, y=410
    # We position the mirrored arm so the shoulder connects smoothly
    arm_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    arm_layer.paste(mirrored, (155, 410))
    
    # We composite the mirrored arm BEHIND the torso/sleeve/shorts
    # So base is on top, arm_layer is behind
    final = Image.alpha_composite(arm_layer, base)
    
    # Clean up any leftover pixels outside the character silhouette on the left (x < 155)
    fpix = final.load()
    for y in range(320, 650):
        for x in range(0, 155):
            fpix[x, y] = (0, 0, 0, 0)
            
    final.save("assets/pixel_hero/master_male_clean.png")
    print("Saved final assets/pixel_hero/master_male_clean.png with seamless arm!")

attach_mirrored_arm()
