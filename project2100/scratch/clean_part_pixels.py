# -*- coding: utf-8 -*-
"""
Precise weapon eraser for the sliced parts
- master 이미지에서 칼자루(검붉은/짙은갈색/검정)와 칼날(은백색/메탈릭) 픽셀을
  피부색(살구빛), 티셔츠(아이보리), 바지(청색)와 구분하여 정밀 투명화.
"""
from PIL import Image

def clean_part_pixels(part_img, part_name):
    im = part_img.copy()
    pix = im.load()
    w, h = im.size
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
                
            # 칼자루/코등이/칼날 색상 판정
            # 1) 어두운 가죽/목재 칼자루: (r in 40~90, g in 20~55, b in 10~40)
            # 2) 은빛 칼날/코등이: (r > 150, g > 160, b > 180) & (y > 55 or x > 38)
            # 3) 칼자루 끈/가드: (r in 20~60, g in 15~45, b in 10~35)
            
            is_skin = (r > 180 and g > 120 and b > 90 and r > g and g > b)
            is_shirt = (r > 150 and g > 140 and b > 130 and abs(r-g) < 25 and abs(g-b) < 25 and y < 62)
            is_jeans = (b > r and b > 60 and y >= 50)
            
            # 머리 영역(y < 35)은 칼이 없으므로 보존
            if y < 35:
                continue
                
            # 오른손 뒤쪽/등 뒤에 튀어나온 칼자루 제거 (x > 36 and y in 45..80)
            if (x > 38 and y > 45) and not is_skin and not is_shirt and not is_jeans:
                pix[x, y] = (0, 0, 0, 0)
                
            # 왼손 뒤쪽 칼끝 제거 (x < 15 and y > 60)
            if (x < 15 and y > 58) and not is_jeans and not is_skin:
                pix[x, y] = (0, 0, 0, 0)
                
            # 등 뒤 사선으로 걸쳐진 검은 칼집 제거 (x in 20..35, y in 42..58)
            # 피부/티셔츠/청바지가 아닌 짙은 흑갈색
            if (20 <= x <= 36 and 42 <= y <= 58) and not is_skin and not is_shirt and not is_jeans:
                # 벨트는 보존 (갈색 + 금색 버클)
                is_belt = (52 <= y <= 56 and r > 70 and g > 40)
                if not is_belt:
                    pix[x, y] = (0, 0, 0, 0)

    return im
