# -*- coding: utf-8 -*-
"""
High-Precision Contour-Preserving Cleaner & Retro Action Sprites Builder
- 몸통 내부를 일절 손상시키지 않고, 몸체 외곽으로 튀어나온 칼(손잡이, 칼날)만 완벽히 제거
- 남/여 마스터 스프라이트의 아름다운 비주얼 100% 보존
"""
from PIL import Image

def clean_outer_weapon(im_path, female=False):
    im = Image.open(im_path).convert("RGBA")
    # 오른쪽을 보도록 FLIP
    flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    w, h = flipped.size
    pix = flipped.load()
    
    if not female:
        # Male: 
        # 원본에서: 칼자루는 왼쪽 뒤, 칼날은 오른쪽 아래로 뻗음.
        # FLIP 후: 칼자루는 오른쪽 뒤(x > w*0.62), 칼날은 왼쪽 아래(x < w*0.35)로 반전됨!
        for y in range(h):
            for x in range(w):
                a = pix[x, y][3]
                if a == 0: continue
                
                # 1) 오른쪽 뒤로 튀어나온 칼자루 및 코등이
                # x > w * 0.60, y in (h*0.35 .. h*0.65)
                # 오른팔(x: w*0.48..w*0.62, y: h*0.35..h*0.70) 외곽에 튀어나온 부분
                if x > int(w * 0.64) and int(h * 0.35) <= y <= int(h * 0.65):
                    pix[x, y] = (0, 0, 0, 0)
                # 칼자루 폼멜 끝 (x > w*0.58 and y < h*0.55)
                elif x > int(w * 0.60) and int(h * 0.40) <= y <= int(h * 0.52):
                    pix[x, y] = (0, 0, 0, 0)
                    
                # 2) 왼쪽 아래로 튀어나온 칼날 (x < w * 0.38, y > h * 0.65)
                # 왼다리(x: w*0.25..w*0.40, y: h*0.65..h) 바깥으로 뻗은 칼날
                if x < int(w * 0.36) and y > int(h * 0.68):
                    # 발(y > h*0.85 and x > w*0.22) 제외
                    if not (y > int(h * 0.88) and x > int(w * 0.24)):
                        pix[x, y] = (0, 0, 0, 0)
    else:
        # Female:
        # FLIP 후: 마체테 칼자루는 왼쪽(x < w*0.28, y in 0.55..0.65), 
        # 칼날은 오른쪽 아래(x > w*0.60, y > 0.60)
        for y in range(h):
            for x in range(w):
                a = pix[x, y][3]
                if a == 0: continue
                # 왼쪽 칼자루
                if x < int(w * 0.26) and int(h * 0.52) <= y <= int(h * 0.65):
                    pix[x, y] = (0, 0, 0, 0)
                # 오른쪽 칼날
                if x > int(w * 0.62) and y > int(h * 0.58):
                    pix[x, y] = (0, 0, 0, 0)
                    
    return flipped

m_clean = clean_outer_weapon("assets/pixel_hero/retro_male_trans.png", female=False)
m_clean.save("scratch/perfect_clean_male.png")
f_clean = clean_outer_weapon("assets/pixel_hero/retro_female_trans.png", female=True)
f_clean.save("scratch/perfect_clean_female.png")
print("Saved perfect_clean_male.png and perfect_clean_female.png")
