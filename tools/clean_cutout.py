"""Clean a generated cut-out: drop the faint halo, soften the edge slightly, trim empty space.
Usage: python clean_cutout.py in.png out.png [threshold=235]"""
import sys
from PIL import Image, ImageFilter
import numpy as np
src, dst = sys.argv[1], sys.argv[2]
thr = int(sys.argv[3]) if len(sys.argv) > 3 else 235
a = np.array(Image.open(src).convert('RGBA'))
mask = Image.fromarray(((a[:, :, 3] >= thr) * 255).astype(np.uint8))
mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
a[:, :, 3] = np.array(mask)
out = Image.fromarray(a)
out.crop(out.getbbox()).save(dst, optimize=True)
print('saved', dst, out.getbbox())
