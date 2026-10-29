import os
from PIL import Image, ImageEnhance, ImageFilter

src_dir = r"C:\Users\exbxda13\project2100\assets\monsters"
dst_dir = r"C:\Users\exbxda13\project2100\assets\pixel_monsters"
os.makedirs(dst_dir, exist_ok=True)

def enhance_pixel_monster(src_path, dst_path):
    with Image.open(src_path) as im:
        im = im.convert("RGBA")
        
        # 1. Boost color saturation & contrast slightly to make pixel art vibrant
        r, g, b, a = im.split()
        rgb_im = Image.merge("RGB", (r, g, b))
        
        enhancer = ImageEnhance.Color(rgb_im)
        rgb_im = enhancer.enhance(1.25)
        
        enhancer_c = ImageEnhance.Contrast(rgb_im)
        rgb_im = enhancer_c.enhance(1.20)
        
        enhancer_s = ImageEnhance.Sharpness(rgb_im)
        rgb_im = enhancer_s.enhance(1.4)
        
        # 2. High-quality scale down to 64x64 (Arcade 16/32-bit high-def pixel tier)
        small_rgb = rgb_im.resize((64, 64), Image.Resampling.LANCZOS)
        small_a = a.resize((64, 64), Image.Resampling.LANCZOS)
        
        # Threshold alpha for crisp pixel edge (no muddy half-transparent halos)
        small_a = small_a.point(lambda p: 255 if p > 80 else 0)
        
        # 3. Adaptive 32-color quantization for rich pixel shading
        quantized = small_rgb.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        quantized_rgba = quantized.convert("RGBA")
        quantized_rgba.putalpha(small_a)
        
        # 4. Upscale with NEAREST NEIGHBOR to 80x80 for crisp game rendering
        final_pixel = quantized_rgba.resize((80, 80), Image.Resampling.NEAREST)
        final_pixel.save(dst_path)

count = 0
for fn in os.listdir(src_dir):
    if fn.lower().endswith(".png"):
        s_path = os.path.join(src_dir, fn)
        d_path = os.path.join(dst_dir, fn)
        enhance_pixel_monster(s_path, d_path)
        count += 1

print(f"Successfully upgraded {count} monster sprites to high-definition retro pixel art!")
