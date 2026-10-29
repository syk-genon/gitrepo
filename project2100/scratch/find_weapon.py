from PIL import Image

def find_weapon_coords():
    # 원본 male
    im = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = im.size
    pix = im.load()
    
    # 칼자루(hilt)는 x: 0~240, y: 350~610 사이에 있음
    # 피부와 티셔츠의 색상 범위를 벗어난 칼 부품들
    hilt_pixels = []
    for y in range(350, 610):
        for x in range(0, 260):
            r, g, b, a = pix[x, y]
            if a > 50:
                # 셔츠(r>180, g>170, b>160) 및 피부(r>200, g>140) 제외
                if r < 140 and g < 100:
                    hilt_pixels.append((x, y))
                    
    print(f"Detected {len(hilt_pixels)} hilt pixels")
    # 마스크 이미지 저장
    mask = im.copy()
    mpix = mask.load()
    for (x, y) in hilt_pixels:
        mpix[x, y] = (255, 0, 0, 255)
    mask.save("scratch/hilt_debug.png")
    print("Saved scratch/hilt_debug.png")

find_weapon_coords()
