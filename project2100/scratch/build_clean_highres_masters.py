# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance
from collections import deque

def get_exterior_transparent_mask(pix, w, h, extra_seeds=None):
    ext = [[False] * h for _ in range(w)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if pix[x, y][3] == 0 and not ext[x][y]:
                ext[x][y] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if pix[x, y][3] == 0 and not ext[x][y]:
                ext[x][y] = True
                q.append((x, y))
    if extra_seeds:
        for sx, sy in extra_seeds:
            if 0 <= sx < w and 0 <= sy < h and pix[sx, sy][3] == 0 and not ext[sx][sy]:
                ext[sx][sy] = True
                q.append((sx, sy))
    while q:
        cx, cy = q.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and not ext[nx][ny] and pix[nx, ny][3] == 0:
                ext[nx][ny] = True
                q.append((nx, ny))
    return ext

def clean_exterior_white_bg(im, is_male=True, extra_seeds=None):
    w, h = im.size
    pix = im.load()
    visited = [[False] * h for _ in range(w)]
    q = deque()

    def is_protected_interior(x, y):
        nx = x / float(w)
        ny = y / float(h)
        if is_male:
            # Protect Male's white shirt interior (so flood-fill never enters shirt via sleeve)
            if 0.31 <= nx <= 0.68 and 0.32 <= ny <= 0.54:
                return True
            # Protect Male's eyes
            if 0.32 <= nx <= 0.65 and 0.20 <= ny <= 0.30:
                return True
        else:
            # Protect Female's white blouse, eyes, wristbands, and ankle wraps
            if 0.36 <= nx <= 0.78 and 0.26 <= ny <= 0.48:
                return True
            if 0.35 <= nx <= 0.70 and 0.14 <= ny <= 0.25:
                return True
            # Wristbands & ankle wraps
            if (0.71 <= nx <= 0.83 and 0.51 <= ny <= 0.59) or (0.36 <= nx <= 0.44 and 0.54 <= ny <= 0.61):
                return True
            if (0.58 <= nx <= 0.70 and 0.84 <= ny <= 0.93) or (0.37 <= nx <= 0.50 and 0.90 <= ny <= 0.96):
                return True
        return False

    def is_bg_pixel(x, y):
        r, g, b, a = pix[x, y]
        if a < 215:
            return not is_protected_interior(x, y)
        if is_protected_interior(x, y):
            return False
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        sat = max(r, g, b) - min(r, g, b)
        if lum > 214 and sat < 28:
            return True
        if lum > 228 and sat < 42:
            return True
        if is_male and y < int(h * 0.33) and lum > 130 and sat < 55:
            return True
        return False

    for x in range(w):
        for y in (0, h - 1):
            if is_bg_pixel(x, y):
                visited[x][y] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visited[x][y] and is_bg_pixel(x, y):
                visited[x][y] = True
                q.append((x, y))
    if extra_seeds:
        for sx, sy in extra_seeds:
            for dy in range(-6, 7):
                for dx in range(-6, 7):
                    nx, ny = sx + dx, sy + dy
                    if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny] and is_bg_pixel(nx, ny):
                        visited[nx][ny] = True
                        q.append((nx, ny))

    while q:
        cx, cy = q.popleft()
        pix[cx, cy] = (0, 0, 0, 0)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                if is_bg_pixel(nx, ny):
                    visited[nx][ny] = True
                    q.append((nx, ny))

    edge_trim = []
    for y in range(h):
        for x in range(w):
            if visited[x][y] or pix[x, y][3] == 0 or is_protected_interior(x, y):
                continue
            touches_ext = False
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or visited[nx][ny]:
                    touches_ext = True
                    break
            if touches_ext:
                r, g, b, a = pix[x, y]
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                sat = max(r, g, b) - min(r, g, b)
                if (lum > 195 and sat < 35) or (is_male and y < int(h * 0.33) and lum > 105 and sat < 45):
                    edge_trim.append((x, y))
    for x, y in edge_trim:
        pix[x, y] = (0, 0, 0, 0)
        visited[x][y] = True

    return im, visited

def build_clean_highres_masters():
    # 1. MALE (591x941)
    m = Image.open("assets/pixel_hero/retro_male_trans.png").convert("RGBA")
    mw, mh = m.size
    mp = m.load()
    out_m = m.copy()
    omp = out_m.load()

    ext_m0 = get_exterior_transparent_mask(omp, mw, mh, extra_seeds=[(260, 750)])
    for y in range(mh):
        for x in range(mw):
            if omp[x, y][3] < 250 and not ext_m0[x][y]:
                r, g, b, a = omp[x, y]
                omp[x, y] = (255, 255, 255, 255) if a == 0 else (r, g, b, 255)

    for y in range(340, 492):
        cut_x = 165
        for x in range(192, 40, -1):
            if mp[x, y][3] <= 30:
                cut_x = x
                break
        for x in range(0, cut_x + 1):
            omp[x, y] = (0, 0, 0, 0)

    for y in range(492, 615):
        if y < 522:
            border_x = int(178 + (y - 492) * (14 / 30.0))
        else:
            border_x = int(192 - (y - 522) * (16 / 93.0))
        for x in range(0, border_x):
            omp[x, y] = (0, 0, 0, 0)

    for y in range(615, 705):
        for x in range(248, 276):
            r, g, b, a = omp[x, y]
            if a == 0:
                continue
            if not (b > r + 12 and y < 650):
                omp[x, y] = (0, 0, 0, 0)

    for y in range(682, 815):
        leg_max_x = 365
        for x in range(320, 405):
            r, g, b, a = mp[x, y]
            if a > 50 and r > 140 and (r - b) >= 18:
                leg_max_x = x
        for x in range(leg_max_x + 5, mw):
            omp[x, y] = (0, 0, 0, 0)
    for y in range(665, 682):
        for x in range(383, mw):
            omp[x, y] = (0, 0, 0, 0)

    out_m, _ = clean_exterior_white_bg(out_m, is_male=True, extra_seeds=[(260, 720), (260, 820)])
    out_m.save("assets/pixel_hero/master_male_clean.png")

    # 2. FEMALE (501x956)
    f = Image.open("assets/pixel_hero/retro_female_trans.png").convert("RGBA")
    fw, fh = f.size
    fp = f.load()
    out_f = f.copy()
    ofp = out_f.load()

    ext_f0 = get_exterior_transparent_mask(ofp, fw, fh, extra_seeds=[(278, 700), (355, 460)])
    for y in range(fh):
        for x in range(fw):
            if ofp[x, y][3] < 250 and not ext_f0[x][y]:
                r, g, b, a = ofp[x, y]
                ofp[x, y] = (255, 252, 245, 255) if a == 0 else (r, g, b, 255)

    for y in range(585, 790):
        for x in range(0, 245):
            r, g, b, a = fp[x, y]
            if a == 0:
                continue
            if x < 212:
                ofp[x, y] = (0, 0, 0, 0)
            else:
                is_skin = (r > 145 and (r - b) >= 18 and g > 85)
                if not is_skin:
                    ofp[x, y] = (0, 0, 0, 0)

    for y in range(570, 645):
        for x in range(260, 298):
            r, g, b, a = fp[x, y]
            if a == 0:
                continue
            if not (r > 165 and g > 105 and (r - b) > 20) and not (b > r + 10 and y < 602):
                ofp[x, y] = (0, 0, 0, 0)

    for y in range(525, 615):
        for x in range(348, fw):
            r, g, b, a = fp[x, y]
            if a == 0:
                continue
            if x > 412:
                ofp[x, y] = (0, 0, 0, 0)
            elif y >= 555:
                is_skin = (r > 150 and g > 90 and (r - b) >= 20)
                is_band = (y <= 564 and r > 145 and g > 135 and b > 120)
                is_shorts = (x <= 362 and b > r)
                if not (is_skin or is_band or is_shorts):
                    ofp[x, y] = (0, 0, 0, 0)

    for y in range(600, 685):
        for x in range(210, 360):
            r, g, b, a = ofp[x, y]
            if a == 0:
                continue
            if r < 125 and g < 85 and b < 80:
                ofp[x, y] = (0, 0, 0, 0)

    for y in range(900, fh):
        for x in range(0, fw):
            r, g, b, a = ofp[x, y]
            if a == 0:
                continue
            if r > 205 and g > 205 and b > 205 and abs(r - b) < 15:
                ofp[x, y] = (0, 0, 0, 0)

    out_f, _ = clean_exterior_white_bg(out_f, is_male=False, extra_seeds=[(275, 650), (275, 750), (275, 850), (355, 450), (208, 460)])
    out_f.save("assets/pixel_hero/master_female_clean.png")
    print("Built spotless high-res master_male_clean.png and master_female_clean.png!")

if __name__ == "__main__":
    build_clean_highres_masters()
