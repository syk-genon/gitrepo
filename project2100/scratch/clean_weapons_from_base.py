from PIL import Image, ImageDraw

def clean_male_sprite():
    im = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    w, h = im.size
    
    # 칼날 및 손잡이 영역을 투명화
    pixels = im.load()
    
    # 1) 칼자루 (왼쪽 뒤) x: 0~260, y: 370~615 영역 중 칼자루/가드 부분
    # 남성 캐릭터 몸통/팔 윤곽선 외부에 튀어나온 칼자루 지우기
    for y in range(350, 615):
        for x in range(0, 260):
            # 몸통과 셔츠(x >= 170 y <= 520, x >= 240) 제외하고 튀어나온 칼자루 마스킹
            # 칼자루는 짙은 갈색(50~80, 20~40, 10~30) 및 검정 라인
            r, g, b, a = pixels[x, y]
            if a > 0:
                # 손잡이 폼멜(x <= 100, y <= 480)
                if x <= 165:
                    pixels[x, y] = (0, 0, 0, 0)
                # 칼 코등이/가드 및 허리 뒤 칼집 (x <= 230, y in range(480, 560))
                elif x <= 220 and y <= 540:
                    pixels[x, y] = (0, 0, 0, 0)
                elif x <= 265 and (520 <= y <= 610) and (x < 240 or (r < 70 and g < 60 and b < 70)):
                    # 허벅지 뒤로 튀어나온 칼자루/칼집
                    pixels[x, y] = (0, 0, 0, 0)

    # 2) 칼날 (오른쪽 아래 뻗어나온 블레이드) x: 350~591, y: 650~810
    # 오른쪽 다리/발(x: 300~440, y: 700~941)을 제외하고 칼날 지우기
    for y in range(650, 820):
        for x in range(340, w):
            r, g, b, a = pixels[x, y]
            if a > 0:
                # 종아리/발 영역 제외
                is_leg = (480 <= x <= 560 and y >= 700) or (530 <= x <= 590 and y >= 880)
                if not is_leg:
                    # 은색/검정 칼날 제거
                    pixels[x, y] = (0, 0, 0, 0)
                    
    # 허리띠 및 셔츠 뒷단 마감 (자연스러운 누더기 셔츠 실밥)
    draw = ImageDraw.Draw(im)
    # 허리 뒤쪽 부드러운 라인 보정
    im.save("scratch/clean_male.png")
    print("Saved scratch/clean_male.png")

def clean_female_sprite():
    im = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    w, h = im.size
    pixels = im.load()
    
    # 1) 왼쪽 아래 칼날 (x: 0~250, y: 600~795)
    for y in range(600, 800):
        for x in range(0, 250):
            r, g, b, a = pixels[x, y]
            if a > 0:
                # 다리 영역 제외
                is_leg = (x >= 200 and y >= 700)
                if not is_leg:
                    pixels[x, y] = (0, 0, 0, 0)

    # 2) 오른쪽 칼자루 및 등 뒤 (x: 350~501, y: 550~615)
    for y in range(540, 620):
        for x in range(360, w):
            r, g, b, a = pixels[x, y]
            if a > 0:
                pixels[x, y] = (0, 0, 0, 0)
                
    im.save("scratch/clean_female.png")
    print("Saved scratch/clean_female.png")

clean_male_sprite()
clean_female_sprite()
