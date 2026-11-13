# Claude Assets

Skills and tools to use with Claude (Claude Code, the Claude desktop app or claude.ai). Everything here is free to use.

- **Skills** are written instructions that teach Claude a whole job, start to finish.
- **Tools** are small scripts that skills use, and that you can also run on their own.

## Skills

| Skill | What it does |
|---|---|
| [poster-design](skills/poster-design/SKILL.md) | Designs campaign posters like a senior graphic designer. Each poster is built in HTML/CSS/SVG with real layering, gradients, shapes and light; photos come from stock sites, ChatGPT or Higgsfield; every poster is checked at phone size and exported to PNG. |

## Tools

| Tool | What it does |
|---|---|
| [check_setup.py](tools/check_setup.py) | Shows what your computer can run, and how to fix anything missing. |
| [selftest.py](tools/selftest.py) | Tests every tool on sample images. |
| [remove_bg.swift](tools/remove_bg.swift) | Removes a photo's background on a Mac, using the built-in subject lifting. |
| [check_layout.py](tools/check_layout.py) | Checks HTML posters for clashing text, crowded circles, bad line breaks and tiny text, and outlines each problem. |
| [export_png.py](tools/export_png.py) | Exports HTML posters to PNG (macOS, Windows, Linux). |
| [sample_colours.py](tools/sample_colours.py) | Finds the main brand colours in a logo or flyer. |
| [contact_sheet.py](tools/contact_sheet.py) | Makes a thumbnail grid of images. |
| [clean_cutout.py](tools/clean_cutout.py) | Cleans the edges of AI-generated cut-outs. |
| [recolour.py](tools/recolour.py) | Changes one colour to another inside an area of a photo. |
| [stitch_tiles.py](tools/stitch_tiles.py) | Joins four screenshot tiles into one image. |

## How to use a skill

**Easiest (any Claude chat that can browse or run code):** paste the link in your message.

> Use the poster-design skill from https://github.com/greatopomu/claude-assets to design 5 Instagram posters for [brand]. Here's their website: [link].

**Claude Code (install once):**

```bash
git clone --depth 1 https://github.com/greatopomu/claude-assets.git ~/claude-assets
mkdir -p ~/.claude/skills && cp -r ~/claude-assets/skills/poster-design ~/.claude/skills/
```

Then ask for posters as normal. Claude finds the tools in `~/claude-assets/tools`.

**No internet access in your chat?** Download the repository with GitHub's green **Code → Download ZIP** button, then attach `skills/poster-design/SKILL.md` to your chat.

## Set up the tools

Requirements:
- Python 3.9 or newer
- Pillow and NumPy
- For PNG export: Google Chrome, Edge, Chromium or Brave (or Playwright)

```bash
python -m pip install -r tools/requirements.txt
python tools/check_setup.py
python tools/selftest.py
```

The self-test should end with `ALL PASSED`.
