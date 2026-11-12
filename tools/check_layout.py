"""Check posters for layout mistakes before anyone sees them.

Finds: text overlapping text, circle edges and rings passing too close to text,
circles that almost touch, graphics sitting under text, text that is too small,
and text too close to the poster edge. Saves a copy of each poster with the problems
outlined (red = must fix, orange = check it is intended).

The page needs posters with id="p1", id="p2" ... and the ?solo=pN mode (as in the template).
The checker script is added to the page on the fly, so nothing in your HTML changes.

Usage:
  python tools/check_layout.py path/to/index.html                      # all posters
  python tools/check_layout.py index.html --posters p1 p3 --gap 24 --size 1080x1350 --shots checks

Exit code 0 = no red problems, 1 = red problems found."""
import argparse, functools, html as htmlmod, http.server, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _browser import find_browser, have_playwright

ap = argparse.ArgumentParser()
ap.add_argument("html")
ap.add_argument("--posters", nargs="*")
ap.add_argument("--gap", type=int, default=24, help="minimum clear space in px between text and circle edges")
ap.add_argument("--size", default="1080x1350")
ap.add_argument("--shots", default=None, help="folder for annotated screenshots (default <html dir>/checks)")
ap.add_argument("--wait", type=int, default=8000)
a = ap.parse_args()

html = os.path.abspath(a.html)
root, page = os.path.dirname(html), os.path.basename(html)
shots = os.path.abspath(a.shots or os.path.join(root, "checks"))
os.makedirs(shots, exist_ok=True)
W, H = (int(v) for v in a.size.lower().split("x"))
src = open(html, encoding="utf-8").read()
ids = a.posters or sorted(set(re.findall(r'id="(p\d+)"', src)), key=lambda s: int(s[1:]))
if not ids:
    sys.exit('No posters found. Give each poster id="p1", id="p2" ... or pass --posters.')
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "layout_check.js"), encoding="utf-8").read()

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_GET(self):
        if self.path.split("?")[0].lstrip("/") == page:
            body = src.replace("</body>", f"<script>{JS}</script></body>").encode("utf-8")
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        else:
            super().do_GET()

srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Handler, directory=root))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/{page}"

def parse(dom):
    m = ([None] + list(re.finditer(r'<pre id="layout-report"[^>]*>(.*?)</pre>', dom, re.S)))[-1]
    return json.loads(htmlmod.unescape(m.group(1))) if m else None

reports = {}
browser = find_browser()
if browser:
    prof = tempfile.mkdtemp()
    base = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--user-data-dir={prof}", f"--virtual-time-budget={a.wait}", f"--window-size={W},{H}"]
    for pid in ids:
        u = f"{url}?solo={pid}&check={a.gap}"
        for attempt in range(3):   # web fonts sometimes arrive late; try again
            dom = subprocess.run(base + ["--dump-dom", u], capture_output=True, text=True, timeout=180).stdout
            reports[pid] = parse(dom)
            if reports[pid] is not None:
                break
        subprocess.run(base + [f"--screenshot={os.path.join(shots, pid + '-check.png')}", u],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    shutil.rmtree(prof, ignore_errors=True)
elif have_playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for pid in ids:
            pg.goto(f"{url}?solo={pid}&check={a.gap}", wait_until="networkidle")
            pg.wait_for_selector("#layout-report", state="attached", timeout=15000)
            reports[pid] = parse(pg.content())
            pg.screenshot(path=os.path.join(shots, pid + "-check.png"))
        b.close()
else:
    srv.shutdown()
    sys.exit("No browser found. Install Google Chrome (or Edge/Chromium), set CHROME_PATH, "
             "or: pip install playwright && python -m playwright install chromium")
srv.shutdown()

fails = 0
for pid in ids:
    r = reports.get(pid)
    if r is None:
        print(f"{pid}: checker did not finish (raise --wait?)"); fails += 1; continue
    f = [i for i in r if i["level"] == "fail"]; w = [i for i in r if i["level"] == "warn"]
    fails += len(f)
    print(f"{pid}: {len(f)} to fix, {len(w)} to look at  ->  {os.path.join(shots, pid + '-check.png')}")
    for i in f: print("   FIX  ", i["msg"])
    for i in w: print("   LOOK ", i["msg"])
sys.exit(1 if fails else 0)
