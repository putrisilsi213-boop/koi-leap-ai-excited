#!/usr/bin/env python3
"""Koi Leap — round 3 artwork generator (drawn from scratch with PIL).

Giant rainbow koi leaping over a neon city at dusk, orange astronaut
riding on its back. 1024x1024, vivid saturated colors, high contrast.
No external assets — every pixel is drawn by this script.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
random.seed(20261116)

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")

# ---------- dusk sky: vertical gradient deep purple -> magenta -> orange ----------
top = (24, 8, 64)
mid = (122, 20, 110)
low = (255, 94, 40)
for y in range(H):
    t = y / H
    if t < 0.55:
        k = t / 0.55
        c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
    else:
        k = (t - 0.55) / 0.45
        c = tuple(int(mid[i] + (low[i] - mid[i]) * k) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# ---------- stars ----------
for _ in range(220):
    x, y = random.randint(0, W - 1), random.randint(0, int(H * 0.45))
    r = random.choice([1, 1, 2])
    a = random.randint(120, 255)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

# ---------- low sun (glowing disc on the horizon) ----------
sun_cx, sun_cy, sun_r = 760, 640, 90
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, a in [(260, 28), (200, 50), (150, 90)]:
    gd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r],
               fill=(255, 170, 60, a))
gd.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
           fill=(255, 214, 120, 255))
img = Image.alpha_composite(img.convert("RGBA"), glow)
d = ImageDraw.Draw(img, "RGBA")

# ---------- neon city skyline (two layers: far + near) ----------
def skyline(y_base, h_min, h_max, color, win_colors, seed):
    rnd = random.Random(seed)
    x = -10
    while x < W + 10:
        bw = rnd.randint(46, 110)
        bh = rnd.randint(h_min, h_max)
        d.rectangle([x, y_base - bh, x + bw, y_base], fill=color)
        # antenna on some towers
        if rnd.random() < 0.35:
            d.line([x + bw // 2, y_base - bh, x + bw // 2, y_base - bh - 26],
                   fill=(255, 60, 90, 255), width=3)
            d.ellipse([x + bw // 2 - 4, y_base - bh - 32, x + bw // 2 + 4,
                       y_base - bh - 24], fill=(255, 60, 90, 255))
        # lit windows
        for wy in range(y_base - bh + 12, y_base - 10, 18):
            for wx in range(x + 8, x + bw - 8, 16):
                if rnd.random() < 0.5:
                    wc = rnd.choice(win_colors)
                    d.rectangle([wx, wy, wx + 8, wy + 10], fill=wc)
        x += bw + rnd.randint(2, 14)

skyline(880, 120, 260, (38, 16, 68, 255),
        [(255, 220, 120, 255), (120, 240, 255, 255)], seed=7)
skyline(880, 180, 380, (16, 8, 40, 255),
        [(255, 90, 180, 255), (80, 255, 210, 255), (255, 230, 90, 255)],
        seed=21)

# neon sign strips along the skyline base
for x0, col in [(40, (255, 40, 140)), (330, (40, 255, 220)),
                (620, (255, 200, 40)), (880, (160, 90, 255))]:
    d.rectangle([x0, 868, x0 + 130, 876], fill=col + (255,))

# ---------- water at the bottom with neon reflections ----------
d.rectangle([0, 880, W, H], fill=(10, 10, 46, 255))
for _ in range(160):
    x = random.randint(0, W - 1)
    y = random.randint(884, H - 4)
    ln = random.randint(14, 60)
    col = random.choice([(255, 90, 180), (60, 255, 220), (255, 200, 60),
                         (140, 120, 255)])
    d.line([(x, y), (x + ln, y)], fill=col + (random.randint(90, 200),),
           width=2)

# ---------- the rainbow koi: big leaping arc across the sky ----------
# Body built from overlapping rainbow segments along a curved spine.
spine = []
for i in range(61):
    t = i / 60.0
    x = 120 + t * 800
    # arc: rises from bottom-left, peaks mid-sky, dives to bottom-right
    y = 830 - 560 * math.sin(math.pi * t) ** 0.9
    spine.append((x, y))

rainbow = [(255, 0, 60), (255, 120, 0), (255, 220, 0), (40, 220, 80),
           (0, 170, 255), (120, 80, 255), (255, 60, 200)]
band_w = 26
for i, (x, y) in enumerate(spine):
    frac = i / 60.0
    ci = min(int(frac * len(rainbow)), len(rainbow) - 1)
    c = rainbow[ci]
    # body thickness swells mid-body, tapers at head/tail
    thick = 34 + 58 * math.sin(math.pi * frac) ** 0.8
    d.ellipse([x - band_w, y - thick, x + band_w, y + thick],
              fill=c + (255,))
    d.ellipse([x - band_w, y - thick, x + band_w, y + thick],
              outline=(255, 255, 255, 90), width=2)

# belly highlight (lighter stripe along the lower edge of the body)
for i, (x, y) in enumerate(spine):
    thick = 34 + 58 * math.sin(math.pi * (i / 60.0)) ** 0.8
    d.ellipse([x - 12, y + thick * 0.45, x + 12, y + thick * 0.85],
              fill=(255, 255, 255, 70))

# head (right end) with big eye and whiskers
hx, hy = spine[-1]
d.ellipse([hx - 26, hy - 66, hx + 66, hy + 66], fill=(255, 60, 200, 255))
d.ellipse([hx - 26, hy - 66, hx + 66, hy + 66], outline=(255, 255, 255, 160),
          width=3)
d.ellipse([hx + 18, hy - 34, hx + 52, hy], fill=(255, 255, 255, 255))
d.ellipse([hx + 28, hy - 26, hx + 48, hy - 6], fill=(10, 10, 30, 255))
d.ellipse([hx + 33, hy - 22, hx + 41, hy - 14], fill=(255, 255, 255, 255))
# whiskers
for dy in (-18, 6):
    d.line([hx + 52, hy + dy, hx + 130, hy + dy - 26],
           fill=(255, 240, 200, 230), width=4)
    d.line([hx + 52, hy + dy + 8, hx + 122, hy + dy + 30],
           fill=(255, 240, 200, 230), width=4)

# tail (left end): flowing forked fins
tx, ty = spine[0]
for sgn, col in [(1, (255, 0, 80)), (-1, (255, 120, 0))]:
    pts = [(tx, ty),
           (tx - 150, ty + sgn * 130),
           (tx - 90, ty + sgn * 60),
           (tx - 170, ty + sgn * 30)]
    d.polygon(pts, fill=col + (235,))
    d.line(pts + [pts[0]], fill=(255, 255, 255, 120), width=3)

# dorsal fin spikes along the top of the arc
for i in range(6, 55, 8):
    x, y = spine[i]
    thick = 34 + 58 * math.sin(math.pi * (i / 60.0)) ** 0.8
    d.polygon([(x - 18, y - thick + 6), (x + 18, y - thick + 6),
               (x, y - thick - 52)], fill=(255, 255, 255, 200))

# ---------- orange astronaut riding on the koi's back (near the peak) ----------
ax, ay = spine[26]  # near the top of the arc
# suit body
d.rounded_rectangle([ax - 34, ay - 118, ax + 34, ay - 34], radius=18,
                    fill=(255, 110, 20, 255), outline=(255, 255, 255, 220),
                    width=3)
# chest panel + buttons
d.rectangle([ax - 20, ay - 104, ax + 20, ay - 72], fill=(20, 30, 60, 255))
for bx, bc in [(-10, (0, 255, 220)), (0, (255, 220, 0)), (10, (255, 60, 120))]:
    d.ellipse([ax + bx - 5, ay - 96, ax + bx + 5, ay - 86], fill=bc + (255,))
# backpack
d.rounded_rectangle([ax + 34, ay - 116, ax + 62, ay - 44], radius=10,
                    fill=(230, 80, 10, 255), outline=(255, 255, 255, 200),
                    width=2)
d.rectangle([ax + 40, ay - 108, ax + 56, ay - 92], fill=(0, 255, 220, 255))
# helmet
d.ellipse([ax - 34, ay - 176, ax + 34, ay - 108], fill=(255, 130, 40, 255),
          outline=(255, 255, 255, 255), width=4)
d.ellipse([ax - 22, ay - 164, ax + 22, ay - 122], fill=(120, 230, 255, 255))
d.ellipse([ax - 10, ay - 158, ax + 6, ay - 142], fill=(255, 255, 255, 220))
# arms: one waving up, one gripping the koi
d.line([ax - 30, ay - 108, ax - 78, ay - 168], fill=(255, 110, 20, 255),
       width=16)
d.line([ax - 78, ay - 168, ax - 66, ay - 196], fill=(255, 110, 20, 255),
       width=14)
d.ellipse([ax - 84, ay - 202, ax - 58, ay - 178], fill=(255, 255, 255, 255))
d.line([ax + 30, ay - 108, ax + 58, ay - 62], fill=(255, 110, 20, 255),
       width=16)
# legs straddling the koi
d.line([ax - 20, ay - 36, ax - 46, ay + 8], fill=(255, 110, 20, 255),
       width=18)
d.line([ax + 20, ay - 36, ax + 48, ay + 6], fill=(255, 110, 20, 255),
       width=18)
d.ellipse([ax - 56, ay - 2, ax - 34, ay + 18], fill=(255, 255, 255, 255))
d.ellipse([ax + 38, ay - 4, ax + 60, ay + 16], fill=(255, 255, 255, 255))
# tether line trailing behind
d.line([ax + 56, ay - 60, ax + 150, ay - 130], fill=(255, 255, 255, 160),
       width=3)

# ---------- splash where the koi's tail leaves the water ----------
for _ in range(90):
    x = 60 + random.randint(-40, 160)
    y = 880 - random.randint(0, 90)
    r = random.randint(2, 7)
    d.ellipse([x - r, y - r, x + r, y + r],
              fill=(180, 240, 255, random.randint(140, 255)))
d.arc([40, 800, 320, 960], start=200, end=340, fill=(255, 255, 255, 200),
      width=5)

# ---------- vignette + slight blur for a painted feel ----------
img = img.convert("RGB")
img = img.filter(ImageFilter.GaussianBlur(0.6))
img.save("entry.jpg", "JPEG", quality=92)
print("saved entry.jpg", img.size)
