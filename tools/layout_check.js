/* Layout checker, injected by tools/check_layout.py into ?solo=pN&check=G pages.
   It measures every piece of text on the poster and reports:
   - text overlapping other text
   - a circle edge (filled circle, ring or dashed orbit) passing within G px of text
     (text should sit clearly inside a circle or clearly outside it, never on or near its edge)
   - two circles almost touching (near-tangent edges look like a mistake: overlap clearly or keep apart)
   - an image or graphic sitting under or over text (warning: check it is intended and readable)
   - text smaller than 18 px, or closer than 40 px to the poster edge
   Results go into a hidden pre#layout-report element as JSON, and red/orange outlines are drawn on the page. */
(function () {
  const q = new URLSearchParams(location.search);
  if (!q.has('check')) return;
  const G = parseInt(q.get('check')) || 24;
  function run() {
    const P = document.querySelector('.poster') || document.body;
    const pr = P.getBoundingClientRect();
    const rel = r => ({ x: r.left - pr.left, y: r.top - pr.top, w: r.width, h: r.height });
    const name = el => (el.textContent || el.getAttribute('class') || el.tagName).trim().replace(/\s+/g, ' ').slice(0, 40);
    const issues = [];
    const add = (level, msg, boxes) => issues.push({ level, msg, boxes });
    const visible = el => { const s = getComputedStyle(el); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05; };

    // 1. text pieces (HTML only; text inside an SVG sticker belongs to the sticker)
    const texts = [];
    P.querySelectorAll('*').forEach(el => {
      if (el.closest('svg') || !visible(el)) return;
      const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
      if (!own.length) return;
      const rects = [];
      own.forEach(n => { const r = document.createRange(); r.selectNodeContents(n); [...r.getClientRects()].forEach(c => { if (c.width > 2 && c.height > 2) rects.push(rel(c)); }); });
      if (!rects.length) return;
      const fs = parseFloat(getComputedStyle(el).fontSize);
      texts.push({ el, rects, fs, label: name(el) });
    });

    // 2. circles: round HTML boxes and SVG <circle>s
    const circles = [];
    P.querySelectorAll('*').forEach(el => {
      if (!visible(el)) return;
      const b = el.getBoundingClientRect(); if (b.width < 30) return;
      let round = false;
      if (el.tagName.toLowerCase() === 'circle') round = true;
      else if (!el.closest('svg')) {
        const brs = getComputedStyle(el).borderTopLeftRadius;
        const br = brs.endsWith('%') ? parseFloat(brs) / 100 * b.width : parseFloat(brs);
        round = Math.abs(b.width - b.height) < 4 && br >= b.width * 0.45 && getComputedStyle(el).transform === 'none';
      }
      if (round && el.tagName.toLowerCase() === 'circle') {
        // true radius even when the SVG is rotated (a rotated bounding box would be too big)
        const m = el.getScreenCTM(), sv = el.ownerSVGElement.createSVGPoint();
        sv.x = el.cx.baseVal.value; sv.y = el.cy.baseVal.value; const c = sv.matrixTransform(m);
        circles.push({ el, cx: c.x - pr.left, cy: c.y - pr.top, r: el.r.baseVal.value * Math.hypot(m.a, m.b), label: name(el) });
      } else if (round) { const r = rel(b); circles.push({ el, cx: r.x + r.w / 2, cy: r.y + r.h / 2, r: r.w / 2, label: name(el) }); }
    });

    const related = (a, b) => a.contains(b) || b.contains(a) || (a.parentElement && a.parentElement.contains(b) && a.parentElement !== P) ||
      (a.closest('svg') && a.closest('svg').contains(b));
    const inter = (a, b) => Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));

    // text vs text
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const A = texts[i], B = texts[j];
      if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
      const core = r => ({ x: r.x, y: r.y + r.h * 0.14, w: r.w, h: r.h * 0.72 });  // glyphs, not the full line box
      A.rects.forEach(a => B.rects.forEach(b => { if (inter(core(a), core(b)) > 4) add('fail', `Text overlaps text: "${A.label}" / "${B.label}"`, [a, b]); }));
    }
    // circle edge near text
    texts.forEach(T => circles.forEach(C => {
      if (related(C.el, T.el)) return;
      T.rects.forEach(r => {
        const nx = Math.max(r.x, Math.min(C.cx, r.x + r.w)), ny = Math.max(r.y, Math.min(C.cy, r.y + r.h));
        const dmin = Math.hypot(nx - C.cx, ny - C.cy);
        const dmax = Math.max(...[[r.x, r.y], [r.x + r.w, r.y], [r.x, r.y + r.h], [r.x + r.w, r.y + r.h]].map(([x, y]) => Math.hypot(x - C.cx, y - C.cy)));
        if (!(dmin < C.r + G && dmax > C.r - G)) return;            // text clearly inside or clearly outside
        // is the circle edge actually visible next to this text? (e.g. hidden under an opaque footer)
        const mx = r.x + r.w / 2, my = r.y + r.h / 2, dd = Math.hypot(mx - C.cx, my - C.cy) || 1;
        const px = C.cx + (mx - C.cx) / dd * C.r + pr.left, py = C.cy + (my - C.cy) / dd * C.r + pr.top;
        const stack = document.elementsFromPoint(px, py), ci = stack.indexOf(C.el);
        if (ci < 0 && !(C.el.tagName.toLowerCase() === 'circle' && stack.includes(C.el.closest('svg')))) return;
        const covered = stack.slice(0, ci < 0 ? stack.length : ci).some(e => { const bg = getComputedStyle(e).backgroundColor; const m = bg.match(/[\d.]+/g); return m && (m.length < 4 || +m[3] > 0.9) && !/^rgba\(0, 0, 0, 0\)$/.test(bg) && e.contains(T.el); });
        if (covered) return;
        // the edge must not cross the text, and the nearest visible edge point must be G px away
        const qx = px - pr.left, qy = py - pr.top;
        const ex = Math.max(r.x - qx, 0, qx - (r.x + r.w)), ey = Math.max(r.y - qy, 0, qy - (r.y + r.h));
        if (Math.hypot(ex, ey) >= G && !(dmin < C.r && dmax > C.r)) return;
          add('fail', `Circle edge within ${G}px of text: "${T.label}" (circle: ${C.label || 'shape'})`, [r, { x: C.cx - C.r, y: C.cy - C.r, w: C.r * 2, h: C.r * 2, round: 1 }]);
      });
    }));
    // near-tangent circles
    for (let i = 0; i < circles.length; i++) for (let j = i + 1; j < circles.length; j++) {
      const A = circles[i], B = circles[j];
      if (related(A.el, B.el)) continue;
      // repeated items in a list or grid (same tag and class) keep their own rhythm
      if (A.el.tagName === B.el.tagName && A.el.getAttribute('class') === B.el.getAttribute('class') && A.el.parentElement.parentElement === B.el.parentElement.parentElement) continue;
      const d = Math.hypot(A.cx - B.cx, A.cy - B.cy), gapOut = d - (A.r + B.r), gapIn = Math.abs(A.r - B.r) - d;
      const near = (gapOut > -G && gapOut < G) || (gapIn > -G && gapIn < G && d > 2);
      if (near) add('fail', `Circles almost touching (overlap clearly or keep ${G}px apart): ${A.label || 'circle'} / ${B.label || 'circle'}`,
        [{ x: A.cx - A.r, y: A.cy - A.r, w: A.r * 2, h: A.r * 2, round: 1 }, { x: B.cx - B.r, y: B.cy - B.r, w: B.r * 2, h: B.r * 2, round: 1 }]);
    }
    // circle almost touching the straight edge of a solid panel (a footer, a band, a card)
    P.querySelectorAll('*').forEach(el => {
      if (el.closest('svg') || !visible(el)) return;
      const bg = getComputedStyle(el).backgroundColor, m = bg.match(/[\d.]+/g);
      if (!m || (m.length === 4 && +m[3] < 0.9)) return;
      const b = rel(el.getBoundingClientRect());
      if (b.w < 200 || parseFloat(getComputedStyle(el).borderTopLeftRadius) >= b.w * 0.45) return;
      circles.forEach(C => {
        if (related(C.el, el) || C.cx < b.x || C.cx > b.x + b.w) return;
        const edges = [[C.cy + C.r, b.y], [C.cy - C.r, b.y + b.h]];
        edges.forEach(([ce, pe]) => { if (Math.abs(ce - pe) < G && Math.abs(ce - pe) > 0.5)
          add('fail', `Circle edge almost touches a panel edge (${Math.round(Math.abs(ce - pe))}px): ${C.label || 'circle'} / ${el.getAttribute('class') || el.tagName}`,
            [{ x: C.cx - C.r, y: C.cy - C.r, w: C.r * 2, h: C.r * 2, round: 1 }, b]); });
      });
    });
    // images / graphics vs text
    P.querySelectorAll('img, svg').forEach(g => {
      if (!visible(g) || g.parentElement.closest('svg')) return;
      const b = rel(g.getBoundingClientRect()); if (b.w * b.h > pr.width * pr.height * 0.6 || b.w < 20) return;
      texts.forEach(T => { if (related(g, T.el)) return; T.rects.forEach(r => {
        if (inter(b, r) <= r.w * r.h * 0.05) return;
        // skip when the text sits on its own opaque panel drawn above the graphic
        const st = document.elementsFromPoint(r.x + r.w / 2 + pr.left, r.y + r.h / 2 + pr.top), gi = st.indexOf(g);
        if (st.slice(0, gi < 0 ? st.length : gi).some(e => e.contains(T.el) && e !== P && /rgb\(|rgba\([^)]*, (1|0\.9\d*)\)/.test(getComputedStyle(e).backgroundColor))) return;
        if (inter(b, r) > r.w * r.h * 0.05) add('warn', `Graphic under/over text: "${T.label}" (${g.getAttribute('class') || g.tagName})`, [r, b]); }); });
    });
    // line breaks: a short or single-word last line in running text
    texts.forEach(T => {
      if (T.el.querySelector('br') || T.rects.length < 2) return;
      const lines = {}; T.rects.forEach(r => { const k = Math.round(r.y / 6); (lines[k] = lines[k] || []).push(r); });
      const ys = Object.keys(lines).map(Number).sort((a, b) => a - b); if (ys.length < 2) return;
      const width = k => Math.max(...lines[k].map(r => r.x + r.w)) - Math.min(...lines[k].map(r => r.x));
      const last = width(ys[ys.length - 1]), full = Math.max(...ys.map(width));
      if (last < full * 0.3) add('fail', `Bad line break: last line is very short in "${T.label}" (use text-wrap: balance, rewrite or change the width)`, lines[ys[ys.length - 1]]);
    });
    // size and margins
    texts.forEach(T => {
      if (T.fs < 18) add('fail', `Text smaller than 18px (${T.fs}px): "${T.label}"`, T.rects);
      T.rects.forEach(r => { if (r.x < 40 || r.y < 40 || r.x + r.w > pr.width - 40 || r.y + r.h > pr.height - 40) add('warn', `Text within 40px of the poster edge: "${T.label}"`, [r]); });
    });

    // de-duplicate and draw
    const seen = new Set(), out = [];
    issues.forEach(i => { if (!seen.has(i.msg)) { seen.add(i.msg); out.push(i); } });
    out.forEach(i => i.boxes.forEach(b => {
      const d = document.createElement('div');
      d.style.cssText = `position:absolute;left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px;border:3px solid ${i.level === 'fail' ? '#ff1744' : '#ff9100'};${b.round ? 'border-radius:50%;' : ''}z-index:9999;pointer-events:none`;
      P.appendChild(d);
    }));
    const pre = document.createElement('pre'); pre.id = 'layout-report'; pre.style.display = 'none';
    pre.textContent = JSON.stringify(out.map(({ level, msg }) => ({ level, msg })));
    document.body.appendChild(pre);
  }
  const safe = () => { try { run(); } catch (e) {
    const pre = document.createElement('pre'); pre.id = 'layout-report'; pre.style.display = 'none';
    pre.textContent = JSON.stringify([{ level: 'fail', msg: 'Checker error: ' + e.message }]); document.body.appendChild(pre); } };
  const go = () => (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => requestAnimationFrame(() => setTimeout(safe, 50)));
  if (document.readyState === 'complete') go(); else addEventListener('load', go);
})();
