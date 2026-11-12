"""List the main saturated colours in a logo or poster (to find the real brand hexes).
Usage: python sample_colours.py image.png [top=15]"""
import sys, collections
from PIL import Image
import numpy as np
im = np.array(Image.open(sys.argv[1]).convert('RGB'))[::2, ::2].reshape(-1, 3).astype(int)
top = int(sys.argv[2]) if len(sys.argv) > 2 else 15
sat = im.max(1) - im.min(1) > 40
q = (im[sat] // 6) * 6
c = collections.Counter(map(tuple, q))
for (r, g, b), n in c.most_common(top):
    near = im[sat][(np.abs(im[sat] - [r, g, b]).max(1) <= 8)]
    m = near.mean(0).astype(int)
    print('#%02x%02x%02x' % tuple(m), n)
