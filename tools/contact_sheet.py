"""Make a labelled thumbnail grid.
Usage: python contact_sheet.py out.png img1.jpg img2.jpg ... [--w 220 --h 300 --cols 8]
Use it to choose stock photos, or to check posters at phone size (--w 390 --h 488 --cols 5)."""
import sys, os
from PIL import Image, ImageDraw
args = sys.argv[1:]; opts = {'--w': 220, '--h': 300, '--cols': 8}
files = []
i = 0
while i < len(args):
    if args[i] in opts:
        opts[args[i]] = int(args[i + 1]); i += 2
    else:
        files.append(args[i]); i += 1
out, files = files[0], files[1:]
W, H, C = opts['--w'], opts['--h'], opts['--cols']
rows = (len(files) + C - 1) // C
sheet = Image.new('RGB', (C * W, rows * (H + 22)), 'white'); d = ImageDraw.Draw(sheet)
for k, f in enumerate(files):
    try:
        im = Image.open(f).convert('RGB')
    except Exception:
        continue
    im.thumbnail((W - 6, H - 6)); x = (k % C) * W; y = (k // C) * (H + 22)
    sheet.paste(im, (x + 3, y + 3)); d.text((x + 4, y + H + 3), os.path.basename(f), fill='black')
sheet.save(out); print('saved', out)
