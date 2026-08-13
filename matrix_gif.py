#!/usr/bin/env python3
"""Generate a blurred Matrix-style falling binary code GIF for GitHub."""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1000, 280
FONT_SIZE = 18
FONT = ImageFont.truetype(
    "/usr/local/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSansMono-Bold.ttf",
    FONT_SIZE,
)
CHAR_W = FONT.getbbox("0")[2] + 1
STEP = FONT_SIZE + 4            # vertical distance between characters
COL_W = CHAR_W + 2
N_COLS = W // COL_W

rng = random.Random(7)

drops = []
for _ in range(N_COLS):
    drops.append({
        "y": rng.randint(-H, 0),
        "speed": rng.randint(2, 6),
        "len": rng.randint(6, 22),
    })

frames = []
N_FRAMES = 42

for _ in range(N_FRAMES):
    img = Image.new("RGB", (W, H), (2, 6, 3))
    d = ImageDraw.Draw(img)
    for c in range(N_COLS):
        drop = drops[c]
        x = c * COL_W
        head_y = drop["y"]
        L = drop["len"]
        for k in range(L):
            y = head_y - k * STEP
            if y < -FONT_SIZE or y > H:
                continue
            t = k / L
            if k == 0:
                color = (190, 255, 205)          # bright whitish-green head
            else:
                g = int(190 * (1 - t)) + 6
                color = (0, g, 0)
            ch = rng.choice("01")
            d.text((x, y), ch, font=FONT, fill=color)
        drop["y"] += drop["speed"]
        if drop["y"] - L * STEP > H + 40:
            drop["y"] = rng.randint(-H // 2, -10)
            drop["speed"] = rng.randint(2, 6)
            drop["len"] = rng.randint(6, 22)

    img = img.filter(ImageFilter.GaussianBlur(1.1))
    frames.append(img)

frames[0].save(
    "/home/user/matrix_rain.gif",
    save_all=True,
    append_images=frames[1:],
    duration=90,
    loop=0,
    optimize=True,
)
print("GIF written")
