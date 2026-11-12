---
name: poster-design
description: Design campaign posters (Instagram, stories, print) the way a senior graphic designer would. Build each poster in HTML/CSS/SVG with real layering, gradients, shapes and light, use photos only as ingredients (stock, ChatGPT or Higgsfield), check every poster at full and phone size, and export PNGs. Use when someone asks for posters, flyers, social graphics or a campaign set for a brand.
---

# Campaign Poster Design

**For the user:** send one message, for example:

> Use the poster-design skill from https://github.com/greatopomu/claude-assets to design 5 Instagram posters for [brand]. Here's their website / old flyer: [link or file].

That's it. Claude asks for anything else it needs.

**For Claude:** this file tells you how to run the whole job. Follow it from start to finish. Keep the user's effort low: ask once, then work.

---

## Part 0: Setup (do this first, quietly)

The helper tools live in the same repository, in `tools/`. Paths below like `tools/export_png.py` are relative to the repository root.

1. **Get the tools.** If you can run commands and the repo isn't already on this computer:
   `git clone --depth 1 https://github.com/greatopomu/claude-assets.git`
   If git isn't available, download https://github.com/greatopomu/claude-assets/archive/refs/heads/main.zip and unzip it.
2. **Install and check:**
   `python -m pip install -r tools/requirements.txt`
   then `python tools/check_setup.py`. It reports what works on this computer. To prove every tool works, run `python tools/selftest.py`.
3. **Start from the template:** copy `skills/poster-design/template/index.html` into the project folder. It already has the brand tokens, the preview page (Fit / Phone / 100%) and the `?solo=pN` export mode.

**Fallbacks.** Tell the user plainly which of these applies.

| If this is missing | Do this instead |
|---|---|
| No way to run code (a plain chat) | Build the posters as one HTML file (or an artifact) using the template. To export, the user opens the file in Chrome, adds `?solo=p1` to the address, opens DevTools (F12 / Cmd+Opt+I) → Command menu (Ctrl/Cmd+Shift+P) → "Capture full size screenshot". Repeat for each poster. |
| Python works but no browser is found | Install Google Chrome or Edge, set `CHROME_PATH` to a Chromium-based browser, or run `pip install playwright` then `python -m playwright install chromium`. Otherwise use the manual export above. |
| No Higgsfield CLI or credits | Use stock photos (Route A) or ChatGPT (Route B). |
| No built-in browser (Claude desktop) for ChatGPT | Ask the user to generate the image in ChatGPT and download it, then share the file. |
| Can't download from the internet | Ask the user to download the chosen stock photos and share them. |

The image tools are optional helpers. If one can't run, do the same step another way (for example, choose photos by eye) and carry on.

---

## What you are making

Designed campaign posters that look like a senior graphic designer made them. They are not AI images with text on top.

- Build every poster in **HTML, CSS and SVG**, then export it as **PNG** with a headless browser (`tools/export_png.py`).
- Images (people, products, places) are **ingredients only**. You get them from one of three routes (Part 4). An image tool never makes the finished poster.
- Each brand gets **its own look**. The method stays the same; the art direction is chosen fresh every time. Never reuse another brand's layouts.

---

## Part 1: Ask first (one message, only what's missing)

Read the user's message and any files or links. Then send **one short message** with only the questions you still need answered. Offer a sensible default for each one, so the user can reply "defaults are fine".

Ask about these, in this order, skipping anything already answered:

1. **Brand basics:** name, what it sells, city or country, who the customers are.
2. **Brand assets:** logo file, brand colours (or a website or flyer you can sample them from), and any brand fonts.
3. **Size and use:** default 1080 × 1350 for Instagram. Other options: 1080 × 1080, 1080 × 1920 stories, A4 or A3 print.
4. **How many posters, and what each should say:** for example services, offers, an event, or "your choice".
5. **Must-include details:** prices, dates, phone number, address, website or call to action. Anything not given is marked as a placeholder.
6. **People rules:** default is the rules in Part 6.
7. **Images:** default is to use whatever is available, in this order: stock photos (free), ChatGPT in the built-in browser (free, limited), then Higgsfield (paid credits). Ask whether paid credits may be used.
8. **Where to save:** default is a new folder named after the brand.

Don't ask about design choices such as style, layout or effects. Those are your job. You'll show the direction in Part 2.

---

## Part 2: Plan, then show one checkpoint

Do all of this yourself, then show the user **one short plan** to approve.

1. **Sample the brand colours** from their files with a script (`tools/sample_colours.py`); don't guess. Plan to redraw the logo as clean SVG, never a blurry crop.
2. **Research the category:** how 3 or 4 leading brands advertise (layout, type, imagery, tone), including one local competitor. Borrow the thinking, never the assets. Save notes and sources in `RESEARCH.md`.
3. **Collect local truth:** real places, everyday habits, words people actually use, and regional details. Examples of regional details: the usual vehicle colour in that state, or local dress.
4. **Choose the art direction:** pick one option per row of the table in Part 3, to fit this brand and audience. Also choose the fonts (Google Fonts) and how the colours are used: which leads, which is the accent, and what the backgrounds are.
5. **Write the poster ideas:** for each poster, one idea, a headline under 8 words, one supporting line that leads with what the customer gets, a call to action, the image needed, and its story element. No two posters share a layout or story element.

**Checkpoint, the only one before building.** Show the user:
- the colours
- the art direction in 2 or 3 lines
- the fonts
- the list of posters with their headlines

Ask "Go ahead, or change anything?" Keep it short.

---

## Part 3: Art direction choices

Choose per brand. Different brands should differ on several rows.

| Choice | Options |
|---|---|
| Light | dark and moody · bright and airy · earthy mid-tones · black and white plus one colour |
| Colour use | one colour leads with an accent · duotone photos · bold colour blocks · neutral with a brand accent |
| Type | heavy grotesk · condensed and tall · round geometric · editorial serif plus sans · handwritten accent |
| Shapes | organic blobs and waves · hard geometric angles · thin lines and grids · cut paper · circles and arcs |
| Photo treatment | cut-out on shapes · full-bleed with a colour overlay · photo inside a shape · wide photo band · tinted · collage |
| Texture and light | glows and light trails · flat and clean · grain · halftone dots · soft shadows only |
| Layout | headline top, image below · split screen · image centred, type around it · type-led · diagonal · grid of panels |
| Story element | app or interface card · sticker or badge · ticket or receipt · map or route · big number or chart · quote · before and after |

Don't default to dark backgrounds with glowing accents. Use them only when the brand calls for it.

---

## Part 4: Getting images (three routes)

Use the route that fits each poster. Check every image against the people rules (Part 6) before using it. Record sources and licences in `RESEARCH.md`.

**A. Stock photos** (Pexels, Unsplash, Pixabay). Free, real people and places.
- Search with several local queries.
- Compare 20 to 30 thumbnails on one contact sheet (`tools/contact_sheet.py`).
- Reject photos with:
  - the wrong place or people
  - a rules breach
  - readable number plates or private details
  - damage or mess that undercuts the message
  - no space for text
- Download 1600 to 2000 px wide.
- Fix local details if needed. `tools/recolour.py` changes one colour inside an area.
- Let the photo's shape decide the layout: portrait photos work full-bleed; landscape photos work as a band or inside a frame.

**B. ChatGPT in the built-in browser.** Free; best for full scenes.
- The user must be signed in. Type a detailed prompt: subject, clothing that follows the rules, setting, light, "portrait 4:5, no text, no logos".
- To change one detail, stay in the same ChatGPT chat: "Same image, change only …".
- **Limit:** the free plan allows about 3 images a day.
- **Getting the file out:** ChatGPT's download doesn't work from the browser pane.
  - Best: ask the user to click download and tell you the file name.
  - Fallback: show the image full-screen at its real size, capture it in 2 × 2 screenshot tiles and join them with `tools/stitch_tiles.py`.

**C. Higgsfield.** Paid credits; best for cut-outs.
- Check the balance and price first (`higgsfield account status`, `higgsfield generate cost …`).
- GPT Image 2.6 with `--background transparent` gives cut-outs. Use medium quality for people and low for objects. The basic plan runs about 4 jobs at once.
- Clean the faint glow around each cut-out with `tools/clean_cutout.py`.
- To change one detail of an image, pass it back with `--image` and describe only the change.

**Every image prompt** states: the subject and action, clothing that follows the people rules, lighting that matches the poster's mood, framing, "photorealistic, no text, no logos, no watermark", and space left for type when it's a full scene.

---

## Part 5: Building the posters

**Set up first** (start from `skills/poster-design/template/index.html`):
- one `index.html` with colour tokens, fonts and the logo as an SVG symbol
- a shared sign-off (logo plus call-to-action style) that fits the art direction
- a preview page showing every poster at true ratio, scaled to fit, with Fit / Phone (390 px wide) / 100% buttons
- a `?solo=pN` mode for export
- serve the folder from a local server (not `file://`) and open it in the browser pane

**Every poster:**
- **One idea:** headline, supporting line, call to action.
- **At least four layers,** with at least one element crossing in front of the subject.
- **A story element** that shows the product working, such as a realistic app card, ticket, tracker, map or badge.
- **Custom shapes, gradients and light,** not template boxes.
- **Vary the signature effects** across the set while keeping the shared system.

**Design principles (non-negotiable).** These are the mistakes that make a poster look machine-made. Plan for them while building, not only at the end.
- **Breathing space.** Text gets at least 24 px of clear space (40 px is better) from every shape edge, ring, line, badge and image. A circle or ring must never run along, through or close to text.
- **No near-misses.** Two elements either overlap clearly and on purpose (by a quarter of the smaller one or more), or sit well apart. Edges that almost touch, or line up by accident, look like a mistake. Examples: a product top lined up with the top of the circle behind it, or a sticker grazing a box corner.
- **Circles meet panels clearly.** A circle that runs into a footer or band either stops well short of it (24 px or more) or goes clearly under it (40 px or more). It never just grazes the edge.
- **Clear packaging.** Check every cut-out on the poster's real background colour, not only on white and black. Leftover backdrop, jagged edges and solid "frosted" areas only show up on the actual colour.
- **Fewer decorations.** Each extra ring, outline or leaf is one more thing that can crowd the text. If it doesn't add meaning, leave it out.
- **Visual hierarchy.** Decide the reading order: (1) headline or product, (2) supporting line, (3) story element, (4) sign-off. Size, weight and colour must follow that order. Only one thing shouts.
- **Pairing and grouping.** Every icon sits right next to the one thing it labels, with equal spacing in every pair. Each contact detail gets its own icon: WhatsApp next to the number, Instagram next to the handle. Group related items under one small heading ("Order now", "Available in"). Separate unrelated groups with clear space.
- **Alignment.**
  - One left margin for the logo, headline, body and footer.
  - Footer blocks align to the top, so their small headings share a line.
  - Rows and columns of badges have even, measured spacing.
- **Line breaks.**
  - Running text never ends on a single short word. Use `text-wrap: balance` on headlines and body text, then read each line.
  - A break should fall between phrases, not inside one ("over oats, / guinea corn" is wrong; "over / oats, guinea corn and soy pulp" is right).
  - Headlines break by meaning, with a `<br>` where you choose.
- **One name per thing.** Use the same product or flavour names, ingredient lists and claims on every poster in the set. Before you publish, list every claim (such as "no added sugar" or "100% natural") for the client to confirm.
- **The footer is designed too.** It gets the same care as the hero: hierarchy, pairing, alignment and at least 36 px of padding.

**Technique menu** (choose per poster; don't use them all):
- **Depth:**
  - layer order: background → texture → glow or colour fields → shapes → subject → foreground element → story element → overlay for legibility → type → sign-off
  - a foreground line, shape or card crossing the subject
  - a subject breaking out of its card or frame
  - a card placed behind the subject so a hand overlaps it
- **Light and colour:**
  - a blurred radial glow behind the subject
  - rim light asked for in the image prompt to match the poster
  - light trails (an SVG path drawn twice: blurred glow plus sharp core)
  - outline or neon type using stacked `filter: drop-shadow` (not `text-shadow`)
  - a brand-colour overlay on photos: clear on the subject, solid behind the text
  - re-grading an image (day to night, warmer) with a script
- **Shape and texture:**
  - blobs or waves with a thin accent line
  - curved or angled photo edges
  - faded grids, dots or patterns
  - rings and rays
  - circular badges with text on a path (`<textPath>` with `textLength`)
- **Type:**
  - one heavy display face and one clean text face
  - headline leading 0.85 to 0.92, slightly tight tracking with no touching letters
  - one key word in the accent colour or on a colour block
  - clear space under descenders (g, j, y)

---

## Part 6: People rules (default)

Use these unless the user gives others.

- **Women:** no trousers; long sleeves; loose fit with no visible bra lines or undergarment outlines; no cleavage; no earrings, makeup or painted nails. Hair may be uncovered.
- **Men:** no dreadlocks; neat hair.
- **Everyone:** people who fit the brand's place and audience, in real local settings.
- **Write the rules into every image prompt, then check the result.** Zoom in on ears, sleeves, necklines and fit. AI images often add tiny stud earrings even when told not to; retouch or edit them out.

---

## Part 7: Check before showing (three gates, every time)

Nothing reaches the user until it has passed all three gates. Fix, re-render and re-run the gates until they're clean.

**Gate 1: automatic layout check.** Run `python tools/check_layout.py <project>/index.html`. It measures the real page and lists:
- text overlapping text;
- circle edges or rings near or through text;
- circles that almost touch;
- graphics under text;
- bad line breaks;
- text that is too small or too close to the edge.

It also saves each poster with the problems outlined in red (must fix) or orange (check it is intended), in `<project>/checks/`.
- Fix every red item.
- Look at every orange one and decide.
- Re-run until there is no red.
- Chain the export to the check so a red result stops it: `python tools/check_layout.py index.html && python tools/export_png.py index.html ...`.

**Gate 2: your own look.** Render each poster at 1:1 and on a phone-size contact sheet (390 px wide). Check:
- **Text:** nothing clipped, no descenders hitting the next block, no letters touching, no text over a busy part of the image.
- **Minimum sizes at 1080 px wide:** headline about 100 px, body about 30 px, small labels 18 to 19 px.
- **Images:** no cards covering faces or key details; no halos around cut-outs.
- **People:** every person passes Part 6.
- **The set:** reads as one campaign, no two posters feel like copies, each headline reads in about 2 seconds at phone size.
- **Part 5's design principles,** one by one.

**Gate 3: independent design review.** Hand the PNGs to a separate reviewer: a subagent (the Agent or Task tool), or a fresh chat if there is no subagent tool. The reviewer must not see your plan or notes. A reviewer who knows your intentions sees what you meant, not what is there.
- Paste the reviewer brief below, with the file paths filled in.
- Fix every MUST FIX and SHOULD FIX, or write down why you didn't.
- Run gates 1 and 2 again on what changed. If the changes were big, run gate 3 again too.

> **Reviewer brief.** You are a senior art director reviewing [N] [platform] posters ([W]×[H]) for [brand]. Someone else designed them. Find every flaw before the client sees them. Be strict and specific. Don't praise, and don't redesign from scratch. Open each file: [paths]. Also judge each one at phone size (390 px wide).
>
> Check:
> 1. **Breathing space:** anything touching, nearly touching or awkwardly tangent, or crowding text.
> 2. **Visual hierarchy:** one clear focal point and an obvious reading order.
> 3. **Grouping and pairing:** every icon clearly belongs to its label; related items are grouped.
> 4. **Alignment and margins:** shared margins, even gutters, nothing almost-aligned.
> 5. **Typography:** line breaks, touching letters, descenders, sizes at phone size.
> 6. **Legibility and contrast.**
> 7. **Consistency across the set.**
> 8. **Copy:** typos, AI-sounding phrases, risky claims.
> 9. **Product and image quality:** edges, halos, cropping, shadows.
> 10. **Anything else an art director would send back.**
>
> For each poster, list findings with: severity (MUST FIX / SHOULD FIX / NITPICK), location (with approximate pixel coordinates), what is wrong, and the concrete fix. Then list set-wide issues.

Then show the user the preview page in the browser pane, with a short note on each poster, what the review found and what you fixed.

**Common problems:**

| Problem | Fix |
|---|---|
| Images missing in the browser pane | Serve the folder from a local server, not `file://`. |
| An effect that uses an image file does nothing | Bake the effect into the image with a script. |
| Odd boxes or colours in a poster | A class name clashes with the preview page. Prefix poster classes. |
| Glow turns letters into blobs | Use stacked `drop-shadow` on stroked text. |
| Text unreadable over a bright photo | Move the text into the overlay area; don't weaken the overlay. |
| A ring or circle edge runs close to text | Shrink or move the circle so the text is clearly inside or clearly outside it, or remove the ring. |
| An icon could belong to two things | Give each detail its own icon, pair them tightly and separate the pairs. |
| A paragraph ends on one word | Add `text-wrap: balance`, change the width, or rewrite. |

---

## Part 8: Finish

- **Export** only after the three gates in Part 7 pass, and only when the user is happy, or straight away if they asked for PNGs. Run `python tools/export_png.py <project>/index.html --prefix <brand> --size <WxH>`. It starts its own local server, renders every `?solo=` poster to `<project>/exports/` and checks each file's size.
- **Send the files,** with a list of every placeholder (prices, times, numbers) that the client must confirm.
- **Save local facts** the user gives you (for example "taxis here are painted blue") in your project notes, and apply them to every poster they affect.

---

## Tools (in the repository's `tools/` folder)

| File | Purpose |
|---|---|
| `tools/check_setup.py` | Reports what this computer can do, and how to fix gaps. |
| `tools/selftest.py` | Runs every tool on test images and reports PASS or FAIL. |
| `tools/sample_colours.py` | Lists the main colours in a logo or poster. |
| `tools/contact_sheet.py` | Thumbnail grid for choosing photos or checking phone size. |
| `tools/clean_cutout.py` | Removes the faint glow around generated cut-outs. |
| `tools/stitch_tiles.py` | Joins four screenshot tiles into one image (ChatGPT route). |
| `tools/recolour.py` | Changes one colour to another inside an area. |
| `tools/check_layout.py` | Gate 1: finds clashes, near-misses, bad line breaks and tiny text, and saves outlined screenshots. |
| `tools/export_png.py` | Exports `?solo=pN` posters to PNG on macOS, Windows or Linux. |

All tools need Python 3.9+ with Pillow and NumPy (`tools/requirements.txt`). PNG export also needs Chrome, Edge, Chromium or Brave, or Playwright.
