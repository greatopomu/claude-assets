"""Export posters from an HTML page to PNG. Works on macOS, Windows and Linux.

The page must contain each poster as an element with id="p1", id="p2", ... and support
?solo=pN (show only that poster at 1:1 with no page margins). The script starts its own
temporary web server, so you don't need one running.

Usage:
  python tools/export_png.py path/to/index.html                 # all posters found (p1, p2, ...)
  python tools/export_png.py index.html --posters p1 p3 --out exports --prefix brand --size 1080x1350

Browser: uses Chrome / Edge / Chromium / Brave if found (set CHROME_PATH to choose one),
otherwise Playwright if installed (pip install playwright && python -m playwright install chromium)."""
import argparse, functools, http.server, os, re, shutil, socketserver, subprocess, sys, tempfile, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _browser import find_browser, have_playwright

ap = argparse.ArgumentParser()
ap.add_argument("html")
ap.add_argument("--posters", nargs="*")
ap.add_argument("--out", default=None)
ap.add_argument("--prefix", default="poster")
ap.add_argument("--size", default="1080x1350")
ap.add_argument("--wait", type=int, default=8000, help="ms to let fonts and images load")
a = ap.parse_args()

html = os.path.abspath(a.html)
root, page = os.path.dirname(html), os.path.basename(html)
out = os.path.abspath(a.out or os.path.join(root, "exports"))
os.makedirs(out, exist_ok=True)
W, H = (int(v) for v in a.size.lower().split("x"))
ids = a.posters or sorted(set(re.findall(r'id="(p\d+)"', open(html, encoding="utf-8").read())), key=lambda s: int(s[1:]))
if not ids:
    sys.exit("No posters found. Give each poster id=\"p1\", id=\"p2\" ... or pass --posters.")

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=root))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}/{page}"

browser = find_browser()
results = []
if browser:
    prof = tempfile.mkdtemp()
    for pid in ids:
        dst = os.path.join(out, f"{a.prefix}-{pid}.png")
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--user-data-dir={prof}",
                        f"--virtual-time-budget={a.wait}", f"--window-size={W},{H}",
                        f"--screenshot={dst}", f"{url}?solo={pid}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        results.append(dst)
    shutil.rmtree(prof, ignore_errors=True)
elif have_playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for pid in ids:
            dst = os.path.join(out, f"{a.prefix}-{pid}.png")
            pg.goto(f"{url}?solo={pid}", wait_until="networkidle")
            pg.wait_for_timeout(min(a.wait, 3000))
            pg.screenshot(path=dst)
            results.append(dst)
        b.close()
else:
    srv.shutdown()
    sys.exit("No browser found. Install Google Chrome (or Edge/Chromium), set CHROME_PATH, "
             "or: pip install playwright && python -m playwright install chromium")
srv.shutdown()

ok = True
try:
    from PIL import Image
    for r in results:
        if not os.path.exists(r):
            print("MISSING", r); ok = False; continue
        s = Image.open(r).size
        flag = "OK" if s == (W, H) else f"WRONG SIZE {s}"
        ok &= flag == "OK"
        print(flag, r)
except ImportError:
    for r in results:
        print("OK" if os.path.exists(r) else "MISSING", r)
sys.exit(0 if ok else 1)
