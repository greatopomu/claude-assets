# Tools

Small, dependency-light scripts used by the skills in this repository. They need Python 3.9+ with Pillow and NumPy:

```bash
python -m pip install -r tools/requirements.txt
python tools/check_setup.py   # what works on this computer
python tools/selftest.py      # runs every tool on test images
```

Each script explains its own options at the top of the file (or run it with `-h` where supported).
`layout_check.js` is the measuring script that `check_layout.py` adds to the page while checking.
`_browser.py` is a shared helper that finds Chrome, Edge, Chromium or Brave on macOS, Windows or Linux. Set `CHROME_PATH` to choose a specific browser.
