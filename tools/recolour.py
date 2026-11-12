"""Shift one colour range to another inside a box, keeping light and shadow.
Example (turn a yellow vehicle blue, protecting two areas):
  python recolour.py in.jpg out.jpg --hue 12 60 --to 212 --box 150 380 1760 1330 \
      --protect 605 515 905 1000 --protect 370 772 485 822
--hue: source hue range in degrees. --to: target hue. --box: x0 y0 x1 y1 area to change.
--protect: x0 y0 x1 y1 areas to leave alone (repeatable). --dark: brightness factor (default 0.8)."""
import argparse
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
p = argparse.ArgumentParser()
p.add_argument('src'); p.add_argument('dst')
p.add_argument('--hue', nargs=2, type=float, required=True)
p.add_argument('--to', type=float, required=True)
p.add_argument('--box', nargs=4, type=int)
p.add_argument('--protect', nargs=4, type=int, action='append', default=[])
p.add_argument('--dark', type=float, default=0.8)
a = p.parse_args()
rgb = Image.open(a.src).convert('RGB'); hsv = np.array(rgb.convert('HSV')).astype(float)
H = hsv[..., 0] * 360 / 255; S = hsv[..., 1]; V = hsv[..., 2]
sel = (H >= a.hue[0]) & (H <= a.hue[1]) & (S > 35) & (V > 30)
if a.box:
    yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]
    x0, y0, x1, y1 = a.box
    sel &= (xx > x0) & (xx < x1) & (yy > y0) & (yy < y1)
mask = Image.fromarray(sel.astype(np.uint8) * 255); d = ImageDraw.Draw(mask)
for r in a.protect:
    d.rectangle(tuple(r), fill=0)
mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.5))
mid = sum(a.hue) / 2
nh = (a.to + (H - mid) * 0.4) % 360
ns = np.clip(np.maximum(S, 70) * 1.05, 0, 255); nv = np.clip(V * a.dark, 0, 255)
new = Image.fromarray(np.stack([nh * 255 / 360, ns, nv], -1).astype(np.uint8), 'HSV').convert('RGB')
Image.composite(new, rgb, mask).save(a.dst, quality=94); print('saved', a.dst)
