from PIL import Image
import glob

def clean_bat_text():
    # 1. Clean assets/monsters/m_4_2.png
    m_path = "assets/monsters/m_4_2.png"
    im = Image.open(m_path).convert("RGBA")
    w, h = im.size
    for y in range(int(h * 0.84), h):
        for x in range(w):
            im.putpixel((x, y), (0, 0, 0, 0))
    im.save(m_path)
    print(f"Cleaned {m_path}")
    
    # 2. Clean all pixel_monsters/m_4_2_*.png
    for p in glob.glob("assets/pixel_monsters/m_4_2_*.png"):
        pim = Image.open(p).convert("RGBA")
        pw, ph = pim.size
        # Clear bottom 15%
        for y in range(int(ph * 0.85), ph):
            for x in range(pw):
                pim.putpixel((x, y), (0, 0, 0, 0))
        pim.save(p)
        print(f"Cleaned {p}")

clean_bat_text()
