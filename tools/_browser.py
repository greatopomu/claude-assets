"""Shared helper: find a Chromium-based browser on macOS, Windows or Linux."""
import os, shutil, sys

NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
         "msedge", "microsoft-edge", "microsoft-edge-stable", "brave-browser", "brave"]
MAC = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
       "/Applications/Chromium.app/Contents/MacOS/Chromium",
       "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
       "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]
WIN_REL = [r"Google\Chrome\Application\chrome.exe", r"Microsoft\Edge\Application\msedge.exe",
           r"Chromium\Application\chrome.exe", r"BraveSoftware\Brave-Browser\Application\brave.exe"]

def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for n in NAMES:
        p = shutil.which(n)
        if p:
            return p
    if sys.platform == "darwin":
        for p in MAC:
            if os.path.exists(p):
                return p
    if os.name == "nt":
        for base in filter(None, [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"),
                                  os.environ.get("LOCALAPPDATA")]):
            for rel in WIN_REL:
                p = os.path.join(base, rel)
                if os.path.exists(p):
                    return p
    return None

def have_playwright():
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False
