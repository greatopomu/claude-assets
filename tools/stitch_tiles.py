"""Stitch four screenshot tiles (2 x 2) of one image into the full image.
Used for the ChatGPT route when the image can't be downloaded from the browser pane.

How to capture the tiles (built-in browser, ChatGPT tab):
 1. In the page, cover the screen with a black overlay holding the image at a CSS width of
    natural_width / (screenshot_px / css_px). Measure the ratio first: compare the screenshot width with
    window.innerWidth (e.g. an 800 px screenshot of a 637 CSS px window is 1.256, so a 1122 px image is shown at 893 CSS px).
 2. Move the image to (0,0), (-dx,0), (0,-dy), (-dx,-dy) CSS px, where dx and dy are how far the image overflows the window, waiting two animation frames each time,
    and take a full-frame zoom screenshot (region 0,0,800,891) of each. The zoom tool saves lossless PNGs.
 3. Remove the overlay, then run:
    python stitch_tiles.py tl.png tr.png bl.png br.png out.png [guess_dx=321] [guess_dy=510]
The script searches around the guessed offsets for the best match."""
import sys
from PIL import Image
import numpy as np
tl, tr, bl, br, out = sys.argv[1:6]
gx = int(sys.argv[6]) if len(sys.argv) > 6 else 321
gy = int(sys.argv[7]) if len(sys.argv) > 7 else 510
T = [np.array(Image.open(p).convert('RGB')).astype(float) for p in (tl, tr, bl, br)]
h, w = T[0].shape[:2]
def best(a, b, horizontal, guess):
    res = None
    for d in range(guess - 8, guess + 9):
        if horizontal:
            e = np.abs(a[h//8:-h//8, d:] - b[h//8:-h//8, :w - d]).mean()
        else:
            e = np.abs(a[d:, w//8:-w//8] - b[:h - d, w//8:-w//8]).mean()
        if res is None or e < res[0]:
            res = (e, d)
    return res[1]
dx = best(T[0], T[1], True, gx); dy = best(T[0], T[2], False, gy)
canvas = np.zeros((h + dy, w + dx, 3))
canvas[dy:, dx:] = T[3]; canvas[dy:, :w] = T[2]; canvas[:h, dx:] = T[1]; canvas[:h, :w] = T[0]
Image.fromarray(canvas.astype(np.uint8)).save(out)
print('saved', out, 'size', (w + dx, h + dy), 'offsets', dx, dy)
