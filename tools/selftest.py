"""Self-test: checks every tool works on this computer, using made-up test images.
Usage: python tools/selftest.py      (takes about 30 seconds)"""
import os, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
try:
    from PIL import Image, ImageDraw
    import numpy as np
except ImportError:
    sys.exit("Pillow/NumPy missing. Run: pip install -r tools/requirements.txt")
tmp = tempfile.mkdtemp(prefix="poster-selftest-")
def run(*args):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()
results = []
def check(name, ok, detail=""):
    results.append(ok); print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

# 1 sample_colours: image with a known colour
im = Image.new("RGB", (300, 300), "white"); ImageDraw.Draw(im).rectangle((0, 0, 200, 300), fill=(79, 192, 37))
im.save(f"{tmp}/logo.png")
code, out = run(f"{HERE}/sample_colours.py", f"{tmp}/logo.png", "3")
check("sample_colours", code == 0 and "#4fc025" in out.lower(), out.splitlines()[0] if out else "")

# 2 clean_cutout: subject plus a faint halo
a = np.zeros((300, 300, 4), np.uint8); a[..., :3] = 120; a[50:250, 50:250, 3] = 60; a[100:200, 100:200, 3] = 255
Image.fromarray(a).save(f"{tmp}/cut.png")
code, out = run(f"{HERE}/clean_cutout.py", f"{tmp}/cut.png", f"{tmp}/cut_clean.png")
ok = code == 0 and os.path.exists(f"{tmp}/cut_clean.png") and Image.open(f"{tmp}/cut_clean.png").size[0] < 130
check("clean_cutout", ok, out[-60:])

# 3 stitch_tiles: cut a known image into 4 overlapping tiles, stitch back
rng = np.random.default_rng(1); big = (rng.random((1400, 1122, 3)) * 255).astype(np.uint8)
dx, dy = 322, 509
for n, (x, y) in zip(("tl", "tr", "bl", "br"), ((0, 0), (dx, 0), (0, dy), (dx, dy))):
    Image.fromarray(big[y:y + 891, x:x + 800]).save(f"{tmp}/{n}.png")
code, out = run(f"{HERE}/stitch_tiles.py", *[f"{tmp}/{n}.png" for n in ("tl", "tr", "bl", "br")], f"{tmp}/stitched.png")
ok = code == 0 and np.array_equal(np.array(Image.open(f"{tmp}/stitched.png")), big)
check("stitch_tiles", ok, out[-60:])

# 4 recolour: yellow block becomes blue
im = Image.new("RGB", (200, 200), (240, 180, 30)); im.save(f"{tmp}/yellow.jpg", quality=95)
code, out = run(f"{HERE}/recolour.py", f"{tmp}/yellow.jpg", f"{tmp}/blue.jpg", "--hue", "20", "60", "--to", "212")
r, g, b = Image.open(f"{tmp}/blue.jpg").convert("RGB").getpixel((100, 100))
check("recolour", code == 0 and b > r and b > g, f"centre pixel {r},{g},{b}")

# 5 contact_sheet
code, out = run(f"{HERE}/contact_sheet.py", f"{tmp}/sheet.png", f"{tmp}/logo.png", f"{tmp}/blue.jpg", "--cols", "2")
check("contact_sheet", code == 0 and os.path.exists(f"{tmp}/sheet.png"))

# 6 export_png: export the starter template's two posters
page = os.path.join(tmp, "page.html")
open(page, "w").write("""<!doctype html><html><head><style>*{margin:0}body{background:#000}.poster{width:1080px;height:1350px;position:relative}
#p1{background:linear-gradient(#1f3a5f,#0d1d33)}#p2{background:#f2b134}h2{font:800 120px sans-serif;color:#fff;padding:60px}</style></head>
<body><section class="poster" id="p1"><h2>One</h2></section><section class="poster" id="p2"><h2>Two</h2></section>
<script>const s=new URLSearchParams(location.search).get('solo');if(s)document.querySelectorAll('.poster').forEach(p=>{if(p.id!==s)p.remove()})</script></body></html>""")
code, out = run(f"{HERE}/export_png.py", page, "--out", f"{tmp}/exports", "--prefix", "test")
check("export_png", code == 0 and out.count("OK") >= 2, out.replace("\n", " | ")[:160])

print("-" * 40)
print("ALL PASSED" if all(results) else f"{results.count(False)} FAILED. Run tools/check_setup.py for fixes.")
print("Test files:", tmp)
sys.exit(0 if all(results) else 1)
