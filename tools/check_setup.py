"""Check what this computer can do, and which parts of the guide will work.
Usage: python tools/check_setup.py"""
import importlib, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _browser import find_browser, have_playwright

def mod(name):
    try:
        m = importlib.import_module(name); return getattr(m, "__version__", "ok")
    except ImportError:
        return None

rows = []
py_ok = sys.version_info >= (3, 9)
rows.append(("Python 3.9+", py_ok, sys.version.split()[0], "Install Python 3.9 or newer."))
pil, npy = mod("PIL"), mod("numpy")
rows.append(("Pillow", bool(pil), pil or "missing", "pip install -r tools/requirements.txt"))
rows.append(("NumPy", bool(npy), npy or "missing", "pip install -r tools/requirements.txt"))
br = find_browser(); pw = have_playwright()
rows.append(("Browser for PNG export", bool(br or pw), br or ("Playwright" if pw else "none"),
             "Install Google Chrome/Edge, set CHROME_PATH, or pip install playwright && python -m playwright install chromium. Manual fallback: see the skill, Part 0."))
hf = shutil.which("higgsfield")
rows.append(("Higgsfield CLI (optional, paid)", bool(hf), hf or "not installed",
             "Optional. Without it, use stock photos or ChatGPT for images."))

print("\nPoster guide setup check\n" + "-" * 40)
for name, ok, info, fix in rows:
    print(f"[{'OK ' if ok else '-- '}] {name}: {info}")
    if not ok:
        print(f"      fix: {fix}")
core = py_ok and pil and npy
print("-" * 40)
print("Image tools (colours, contact sheet, cut-out clean-up, recolour, stitch):", "READY" if core else "NOT READY")
print("PNG export:", "READY" if (br or pw) else "MANUAL (see the skill, Part 0)")
print("Images: stock photos always work;", "Higgsfield available" if hf else "Higgsfield not available",
      "; ChatGPT route needs Claude's built-in browser (Claude desktop app) or the user downloading images.")
