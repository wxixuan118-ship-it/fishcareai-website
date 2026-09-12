"""
Shared template for the /tank-sizes/ experiment pages.

The information architecture (section order, headings pattern, schema) is
identical across pages so it can later be scaled into a programmatic Tank Size
system. All prose, data and recommendations live in the per-page content
modules (content_55.py, content_50.py, content_100.py) and must be unique.
"""

import json
import html as _html

SITE = "https://www.fishcareai.com"

# ── Shared CSS (page-specific classes prefixed ts- to avoid the glass sheet's
#    !important overrides on .card/.callout/.toc etc.) ──────────────────────
CSS = r"""
:root{--p:#1B5E8B;--pd:#0F3D5E;--bg:#F0F7FF;--tx:#1A2B3C;--mu:#5A7A94;--bd:#D0E4F0;--ink:#EAFBFF;--ink-muted:rgba(220,246,255,.74);--line:rgba(125,235,255,.2);--cyan:#7DEBFF;--coral:#FF6B78;--mint:#39F2C5}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--p);text-decoration:none}
a:hover{text-decoration:underline}
.con{max-width:1140px;margin:0 auto;padding:0 22px}
.nb{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.97);border-bottom:1px solid var(--bd);padding:0 22px;height:64px;display:flex;align-items:center;justify-content:space-between}
.brand img{height:36px;width:auto;display:block}
.nlinks{display:flex;gap:2px}
.nl{padding:7px 13px;border-radius:8px;font-weight:500;font-size:.86rem;color:var(--mu)}
.hero{position:relative;background:linear-gradient(135deg,#051C2A,#0F3D5E,#1B5E8B);padding:44px 22px 42px;color:#fff}
.breadcrumb ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;padding:0;margin:0 0 16px;font-size:.84rem}
.breadcrumb li{color:rgba(234,251,255,.72)}
.breadcrumb li+li::before{content:"/";margin-right:6px;color:rgba(125,235,255,.4)}
.breadcrumb a{color:var(--cyan)}
.hero .tag{display:inline-block;padding:4px 12px;border-radius:999px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;background:rgba(255,255,255,.14);color:#fff;margin-bottom:12px}
.hero h1{font-size:clamp(1.75rem,4vw,2.65rem);font-weight:800;line-height:1.15;margin:0 0 14px;max-width:900px;color:#fff}
.hero .lead{max-width:840px}
.hero .lead p{font-size:1.04rem;line-height:1.7;color:rgba(234,251,255,.84)!important;margin:0 0 .8rem}
.hero .lead p:last-child{margin-bottom:0}
.ts-meta{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:18px;font-size:.8rem;color:rgba(234,251,255,.62)}
.ts-layout{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:28px;max-width:1140px;margin:28px auto 56px;padding:0 22px}
.ts-layout>article{min-width:0;max-width:100%}
@media(max-width:940px){.ts-layout{grid-template-columns:1fr}.ts-side{display:none}}
.ts-card{background:linear-gradient(145deg,rgba(11,62,93,.74),rgba(7,35,56,.56));border:1px solid var(--line);border-radius:24px;padding:28px 30px;margin-bottom:22px;box-shadow:0 28px 90px rgba(0,10,22,.36);backdrop-filter:blur(18px) saturate(1.25);color:var(--ink)}
@media(max-width:640px){.ts-card{padding:22px 18px;border-radius:20px}}
.ts-card h2{font-size:1.42rem;font-weight:800;line-height:1.25;margin:0 0 14px;padding-bottom:12px;border-bottom:1px solid var(--line);color:#fff}
.ts-card h3{font-size:1.08rem;font-weight:700;margin:20px 0 8px;color:#fff}
.ts-card p{margin:0 0 .9rem;font-size:.98rem;line-height:1.75;color:var(--ink-muted)}
.ts-card p:last-child{margin-bottom:0}
.ts-card ul,.ts-card ol{margin:6px 0 14px 20px}
.ts-card li{margin-bottom:6px;line-height:1.65;color:var(--ink-muted)}
.ts-card a{color:var(--cyan)}
.ts-card strong{color:#fff}
.glance-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:14px}
.stat{background:rgba(4,22,36,.55);border:1px solid rgba(125,235,255,.16);border-radius:16px;padding:14px 16px}
.stat .lbl{font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:rgba(220,246,255,.62)}
.stat .val{font-size:1.1rem;font-weight:800;color:#fff;margin-top:4px;line-height:1.3}
.stat .sub{font-size:.78rem;color:rgba(220,246,255,.62);margin-top:3px;line-height:1.4}
.tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px 0 10px;border-radius:14px;border:1px solid rgba(125,235,255,.14)}
.ts-table{width:100%;border-collapse:collapse;font-size:.9rem;min-width:520px}
.ts-table th,.ts-table td{padding:10px 12px;text-align:left;vertical-align:top;border-bottom:1px solid rgba(125,235,255,.12)}
.ts-table th{background:rgba(37,215,255,.12);color:#fff;font-weight:700}
.ts-table tr:last-child td{border-bottom:none}
.ts-table td{color:var(--ink-muted)}
.ts-table td:first-child{color:#fff;font-weight:600}
.ts-note{border-left:3px solid var(--cyan);background:rgba(37,215,255,.08);padding:12px 16px;border-radius:0 12px 12px 0;margin:14px 0;font-size:.92rem;color:var(--ink-muted)}
.ts-note p{font-size:.92rem;margin-bottom:.5rem}
.ts-warn{border-left-color:var(--coral);background:rgba(255,107,120,.1)}
.fig{margin:18px 0 6px}
.fig img{width:100%;height:auto;display:block;max-width:760px;margin:0 auto}
.fig figcaption{font-size:.82rem;color:rgba(220,246,255,.62);margin-top:8px;text-align:center;line-height:1.5}
.calc{background:rgba(4,22,36,.55);border:1px solid rgba(125,235,255,.16);border-radius:16px;padding:16px 18px;margin:12px 0;font-size:.92rem}
.calc-row{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px dashed rgba(125,235,255,.14);color:var(--ink-muted)}
.calc-row:last-child{border-bottom:none;font-weight:800;color:#fff}
.calc-row span:last-child{white-space:nowrap;color:#fff}
.fish-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin-top:14px}
.fish{background:rgba(4,22,36,.5);border:1px solid rgba(125,235,255,.16);border-radius:18px;padding:16px 18px}
.fish h3{margin:0 0 8px;font-size:1.02rem}
.fish dl{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;font-size:.82rem;margin:0 0 10px}
.fish dt{color:rgba(220,246,255,.6)}
.fish dd{margin:0;color:#EAFBFF}
.fish p{font-size:.88rem;margin:0;line-height:1.6}
.idea{border:1px solid rgba(125,235,255,.18);border-radius:18px;padding:18px 20px;margin-bottom:14px;background:rgba(4,22,36,.45)}
.idea h3{margin:0 0 4px;font-size:1.08rem}
.idea .tagline{font-size:.86rem;color:var(--cyan);margin-bottom:10px}
.zones{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin:10px 0 12px}
.zone{background:rgba(125,235,255,.07);border-radius:12px;padding:10px 12px;font-size:.86rem;color:var(--ink)}
.zone b{display:block;font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:rgba(220,246,255,.6);margin-bottom:3px}
.idea p{font-size:.9rem;margin-bottom:.6rem}
.avoid-item{display:grid;grid-template-columns:28px 1fr;gap:12px;padding:13px 0;border-bottom:1px solid rgba(125,235,255,.12)}
.avoid-item:last-child{border-bottom:none}
.avoid-x{color:var(--coral);font-weight:800;font-size:1.1rem;line-height:1.3}
.avoid-item h3{margin:0 0 4px;font-size:1rem}
.avoid-item p{font-size:.9rem;margin-bottom:.35rem}
.avoid-item .alt{font-size:.84rem;color:var(--mint)!important}
.steps{counter-reset:s;list-style:none;margin:0 0 6px!important;padding:0}
.steps li{counter-increment:s;position:relative;padding-left:46px;margin-bottom:14px}
.steps li::before{content:counter(s);position:absolute;left:0;top:0;width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#1ECFF7,#7C3AED);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.9rem}
.steps li strong{display:block;margin-bottom:2px;color:#fff}
.equip h3{display:flex;align-items:center;gap:8px}
.equip h3 span{font-size:1.1rem}
.procon{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}
@media(max-width:640px){.procon{grid-template-columns:1fr}}
.procon>div{background:rgba(4,22,36,.5);border-radius:16px;padding:16px 18px;border:1px solid rgba(125,235,255,.14)}
.procon h3{margin:0 0 8px}
.procon ul{margin:0 0 0 18px}
.procon li{font-size:.92rem}
.cta-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:11px 20px;font-weight:700;font-size:.9rem;text-decoration:none;border-radius:999px;background:linear-gradient(135deg,#1ECFF7,#7C3AED);color:#fff}
.btn:hover{text-decoration:none}
.btn-ghost{background:rgba(255,255,255,.08)!important;border:1px solid rgba(125,235,255,.35)!important;color:#EAFBFF!important;box-shadow:none!important}
.plan-box{position:relative;overflow:hidden;background:radial-gradient(circle at 18% 20%,rgba(37,215,255,.32),transparent 40%),radial-gradient(circle at 82% 82%,rgba(139,92,246,.36),transparent 42%),linear-gradient(135deg,#052236,#0A4E73);border:1px solid rgba(125,235,255,.38);border-radius:24px;padding:38px 32px;margin-bottom:22px;text-align:center;box-shadow:0 30px 90px rgba(0,10,22,.5)}
.plan-box h2{border:0;font-size:1.65rem;margin:0 0 10px;padding:0;color:#fff}
.plan-box p{max-width:640px;margin:0 auto 6px;font-size:1.02rem;color:rgba(234,251,255,.84)}
.plan-box .cta-row{justify-content:center;margin-top:22px}
.plan-box .btn{padding:13px 24px;font-size:.95rem}
.faq details{border-bottom:1px solid rgba(125,235,255,.12);padding:12px 0}
.faq details:last-child{border-bottom:none}
.faq summary{font-weight:700;cursor:pointer;list-style:none;position:relative;padding-right:28px;font-size:.98rem;color:#fff}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'+';position:absolute;right:2px;top:-2px;color:var(--cyan);font-size:1.25rem}
.faq details[open] summary::after{content:'−'}
.faq details p{margin:10px 0 0;font-size:.93rem}
.cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:12px}
.cmp-card{display:block;background:rgba(4,22,36,.5);border:1px solid rgba(125,235,255,.18);border-radius:18px;padding:18px;color:var(--ink);transition:transform .18s,border-color .18s}
.cmp-card:hover{border-color:rgba(125,235,255,.5);transform:translateY(-3px);text-decoration:none}
.cmp-card .g{font-size:1.35rem;font-weight:800;color:var(--cyan)}
.cmp-card .d{font-size:.78rem;color:rgba(220,246,255,.6);margin-bottom:6px}
.cmp-card p{font-size:.88rem;margin:0}
.ts-side{position:sticky;top:84px;align-self:start}
.side-card{background:linear-gradient(145deg,rgba(11,62,93,.74),rgba(7,35,56,.56));border:1px solid var(--line);border-radius:20px;padding:18px 20px;margin-bottom:16px;box-shadow:0 20px 60px rgba(0,10,22,.3);color:var(--ink)}
.side-card h2{font-size:.76rem;text-transform:uppercase;letter-spacing:.07em;color:rgba(220,246,255,.7);margin:0 0 10px}
.ts-toc a{display:block;padding:6px 0;font-size:.84rem;border-bottom:1px solid rgba(125,235,255,.1);color:rgba(234,251,255,.84)}
.ts-toc a:last-child{border-bottom:none}
.ts-toc a:hover{color:#fff;text-decoration:none}
.qf{width:100%;border-collapse:collapse;font-size:.82rem}
.qf td{padding:6px 0;border-bottom:1px solid rgba(125,235,255,.1);color:var(--ink-muted)}
.qf td:last-child{text-align:right;font-weight:700;color:#fff}
.qf tr:last-child td{border-bottom:none}
.side-cta{background:linear-gradient(135deg,#0A4E73,#3B2A8C);text-align:center}
.side-cta h3{color:#fff;font-size:1rem;margin:0 0 6px}
.side-cta p{font-size:.84rem;color:rgba(234,251,255,.8);margin:0 0 14px}
.ft{background:#0F3D5E;padding:28px 22px;margin-top:40px;text-align:center}
.ftb{color:rgba(255,255,255,.5);font-size:.78rem}
"""

NAV_HTML = """<nav class="nb" aria-label="Main navigation">
  <a class="brand" href="/" aria-label="FishCare AI home"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/guides/">Guides</a>
    <a class="nl" href="/tools/">Tools</a>
    <a class="nl" href="/species">Encyclopedia</a>
    <a class="nl" href="/fish-health/">Fish Diseases</a>
    <a class="nl" href="/tanks/">Tank Sizes</a>
    <a class="nl" href="/about/">About</a>
  </div>
</nav>"""

FOOTER_HTML = """<footer class="ft">
  <div class="ftb">© 2026 EverTrend LLC. FishCare AI is a product of EverTrend LLC. All rights reserved.</div>
  <nav class="legal-links" aria-label="Legal and company information"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a><a href="/image-credits/">Image Credits</a><a href="/add-your-site/">Add Your Site</a></nav>
</footer>"""

SECTIONS = [
    ("glance", "At a glance"),
    ("dimensions", "Dimensions"),
    ("weight", "Weight"),
    ("stocking", "How many fish?"),
    ("best-fish", "Best fish"),
    ("stocking-ideas", "Stocking ideas"),
    ("avoid", "Fish to avoid"),
    ("setup", "Setup steps"),
    ("equipment", "Equipment"),
    ("water", "Water parameters"),
    ("maintenance", "Maintenance"),
    ("right-for-you", "Is it right for you?"),
    ("faq", "FAQ"),
    ("compare", "Compare sizes"),
    ("methodology", "How we recommend"),
]


def esc(s):
    return _html.escape(s, quote=True)


def strip_tags(s):
    import re
    s = re.sub(r"<[^>]+>", "", s)
    return _html.unescape(" ".join(s.split()))


def inch_cm(v):
    return f"{v:g} in ({round(v * 2.54):g} cm)"


# ── Size visualisation SVG ────────────────────────────────────────────────────
def diagram_svg(g, L, W, H, label):
    """Oblique projection of an L×W×H box with dimension callouts, in the
    FishCare cyan/violet palette. Dimensions in inches; cm computed."""
    Lcm, Wcm, Hcm = round(L * 2.54), round(W * 2.54), round(H * 2.54)
    # Scale: longest run fits ~560px wide inside a 760×400 viewBox.
    dx, dy = 0.55, 0.32           # receding-edge direction for depth
    span = L + W * dx
    s = 500 / span
    ox, oy = 96, 300              # front-bottom-left corner
    fl, fh = L * s, H * s         # front face size
    wx, wy = W * s * dx, W * s * dy
    # Front face corners
    A = (ox, oy); B = (ox + fl, oy); C = (ox + fl, oy - fh); D = (ox, oy - fh)
    # Back face (offset by depth)
    A2 = (A[0] + wx, A[1] - wy); B2 = (B[0] + wx, B[1] - wy)
    C2 = (C[0] + wx, C[1] - wy); D2 = (D[0] + wx, D[1] - wy)
    water_y = oy - fh * 0.86
    water_y2 = water_y - wy
    def pt(p): return f"{p[0]:.1f},{p[1]:.1f}"
    tid = f"ts-diagram-title-{g}"
    did = f"ts-diagram-desc-{g}"
    return f"""<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{tid} {did}">
<title id="{tid}">{g} gallon fish tank dimensions diagram: {L:g} × {W:g} × {H:g} inches ({Lcm} × {Wcm} × {Hcm} cm)</title>
<desc id="{did}">Simple 3D outline of a {label} showing length {L:g} in ({Lcm} cm), width {W:g} in ({Wcm} cm) and height {H:g} in ({Hcm} cm), with the water line drawn near the top of the glass.</desc>
<defs>
<linearGradient id="glass-{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25D7FF" stop-opacity=".18"/><stop offset="1" stop-color="#8B5CF6" stop-opacity=".22"/></linearGradient>
<linearGradient id="water-{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25D7FF" stop-opacity=".42"/><stop offset="1" stop-color="#0B6FA4" stop-opacity=".55"/></linearGradient>
</defs>
<g stroke="#7DEBFF" stroke-width="1.6" stroke-linejoin="round" fill="none">
<polygon points="{pt(D)} {pt(D2)} {pt(C2)} {pt(C)}" fill="url(#glass-{g})" opacity=".9"/>
<polygon points="{pt(B)} {pt(B2)} {pt(C2)} {pt(C)}" fill="url(#glass-{g})" opacity=".75"/>
<polygon points="{ox:.1f},{water_y:.1f} {ox + fl:.1f},{water_y:.1f} {B[0]:.1f},{oy:.1f} {ox:.1f},{oy:.1f}" fill="url(#water-{g})" stroke="none"/>
<polygon points="{B[0]:.1f},{water_y:.1f} {B2[0]:.1f},{water_y2:.1f} {B2[0]:.1f},{A2[1]:.1f} {B[0]:.1f},{oy:.1f}" fill="url(#water-{g})" stroke="none" opacity=".7"/>
<polygon points="{pt(A)} {pt(B)} {pt(C)} {pt(D)}" fill="none"/>
<line x1="{ox:.1f}" y1="{water_y:.1f}" x2="{ox + fl:.1f}" y2="{water_y:.1f}" stroke="#39F2C5" stroke-dasharray="5 4" stroke-width="1.2"/>
<line x1="{D[0]:.1f}" y1="{D[1]:.1f}" x2="{D2[0]:.1f}" y2="{D2[1]:.1f}"/>
<line x1="{C[0]:.1f}" y1="{C[1]:.1f}" x2="{C2[0]:.1f}" y2="{C2[1]:.1f}"/>
<line x1="{B[0]:.1f}" y1="{B[1]:.1f}" x2="{B2[0]:.1f}" y2="{B2[1]:.1f}"/>
<line x1="{D2[0]:.1f}" y1="{D2[1]:.1f}" x2="{C2[0]:.1f}" y2="{C2[1]:.1f}"/>
<line x1="{C2[0]:.1f}" y1="{C2[1]:.1f}" x2="{B2[0]:.1f}" y2="{B2[1]:.1f}"/>
</g>
<g stroke="rgba(234,251,255,.55)" stroke-width="1" fill="none">
<line x1="{ox:.1f}" y1="{oy + 34:.1f}" x2="{ox + fl:.1f}" y2="{oy + 34:.1f}"/>
<line x1="{ox:.1f}" y1="{oy + 26:.1f}" x2="{ox:.1f}" y2="{oy + 42:.1f}"/>
<line x1="{ox + fl:.1f}" y1="{oy + 26:.1f}" x2="{ox + fl:.1f}" y2="{oy + 42:.1f}"/>
<line x1="{ox - 34:.1f}" y1="{oy:.1f}" x2="{ox - 34:.1f}" y2="{oy - fh:.1f}"/>
<line x1="{ox - 42:.1f}" y1="{oy:.1f}" x2="{ox - 26:.1f}" y2="{oy:.1f}"/>
<line x1="{ox - 42:.1f}" y1="{oy - fh:.1f}" x2="{ox - 26:.1f}" y2="{oy - fh:.1f}"/>
<line x1="{B[0] + 26:.1f}" y1="{B[1] + 14:.1f}" x2="{B2[0] + 26:.1f}" y2="{B2[1] + 14:.1f}"/>
</g>
<g font-family="-apple-system,'Segoe UI',Arial,sans-serif" fill="#EAFBFF" font-size="19" font-weight="700" text-anchor="middle">
<text x="{ox + fl / 2:.1f}" y="{oy + 62:.1f}">Length {L:g} in <tspan fill="rgba(234,251,255,.65)" font-weight="500">({Lcm} cm)</tspan></text>
<text transform="translate({ox - 56:.1f},{oy - fh / 2:.1f}) rotate(-90)">Height {H:g} in <tspan fill="rgba(234,251,255,.65)" font-weight="500">({Hcm} cm)</tspan></text>
<text x="{B2[0] + 14:.1f}" y="{(B[1] + B2[1]) / 2 + 24:.1f}" text-anchor="start">Width {W:g} in <tspan fill="rgba(234,251,255,.65)" font-weight="500">({Wcm} cm)</tspan></text>
<text x="{ox + fl / 2:.1f}" y="{oy - fh - 22:.1f}" font-size="15" fill="rgba(234,251,255,.7)" font-weight="600">{esc(label)} — typical dimensions, not a manufacturer specification</text>
</g>
</svg>"""


# ── Section renderers ─────────────────────────────────────────────────────────
def render_glance(p):
    tiles = "".join(
        f'<div class="stat"><div class="lbl">{esc(l)}</div><div class="val">{v}</div>'
        + (f'<div class="sub">{n}</div>' if n else "") + "</div>"
        for l, v, n in p["glance"]
    )
    return f"""<section class="ts-card" id="glance">
<h2>{p['gallons']} Gallon Fish Tank at a Glance</h2>
<div class="glance-grid">{tiles}</div>
<div class="ts-note">{p['glance_note']}</div>
</section>"""


def render_dimensions(p):
    rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
        for r in p["dimensions_rows"]
    )
    d = p["diagram"]
    g = p["gallons"]
    Lcm, Wcm, Hcm = (round(d[k] * 2.54) for k in ("l", "w", "h"))
    alt = (f"{g} gallon fish tank dimensions diagram: {d['l']} x {d['w']} x {d['h']} inches "
           f"({Lcm} x {Wcm} x {Hcm} cm) length, width and height")
    svg = (f'<img src="/assets/tank-sizes/{p["slug"]}-dimensions.svg" alt="{esc(alt)}" '
           f'width="800" height="400" loading="lazy" decoding="async"/>')
    return f"""<section class="ts-card" id="dimensions">
<h2>{p['gallons']} Gallon Fish Tank Dimensions</h2>
{p['dimensions_intro_html']}
<div class="tbl-wrap"><table class="ts-table">
<thead><tr><th>Tank type</th><th>Length</th><th>Width (front to back)</th><th>Height</th><th>Best for</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<figure class="fig">{svg}<figcaption>{d['caption']}</figcaption></figure>
{p['dimensions_after_html']}
</section>"""


def render_weight(p):
    rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in p["weight_rows"]
    )
    calc = "".join(
        f'<div class="calc-row"><span>{a}</span><span>{b}</span></div>' for a, b in p["weight_calc"]
    )
    return f"""<section class="ts-card" id="weight">
<h2>How Much Does a {p['gallons']} Gallon Fish Tank Weigh?</h2>
{p['weight_intro_html']}
<div class="tbl-wrap"><table class="ts-table">
<thead><tr><th>Component</th><th>Estimated weight</th><th>Basis</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<h3>Example calculation</h3>
<div class="calc">{calc}</div>
{p['weight_after_html']}
<div class="ts-note ts-warn">{p['weight_safety_html']}</div>
</section>"""


def render_stocking(p):
    return f"""<section class="ts-card" id="stocking">
<h2>How Many Fish Can Live in a {p['gallons']} Gallon Tank?</h2>
{p['stocking_html']}
<div class="cta-row"><a class="btn" href="/tools/aquarium-planner/">Plan Your Aquarium →</a></div>
</section>"""


def render_best_fish(p):
    cards = ""
    for f in p["best_fish"]:
        name = f'<a href="{f["url"]}">{esc(f["name"])}</a>' if f.get("url") else esc(f["name"])
        cards += f"""<article class="fish"><h3>{name}</h3>
<dl><dt>Adult size</dt><dd>{f['adult']}</dd><dt>Group</dt><dd>{f['group']}</dd><dt>Temperament</dt><dd>{f['temperament']}</dd><dt>Zone</dt><dd>{f['zone']}</dd></dl>
<p>{f['why']}</p></article>"""
    return f"""<section class="ts-card" id="best-fish">
<h2>Best Fish for a {p['gallons']} Gallon Tank</h2>
{p['best_fish_intro_html']}
<div class="fish-grid">{cards}</div>
{p.get('best_fish_after_html', '')}
</section>"""


def render_ideas(p):
    items = ""
    for i in p["ideas"]:
        zones = "".join(f'<div class="zone"><b>{esc(z)}</b>{v}</div>' for z, v in i["zones"])
        items += f"""<article class="idea"><h3>{esc(i['title'])}</h3><div class="tagline">{esc(i['tagline'])}</div>
<div class="zones">{zones}</div>
<p><strong>Why it works:</strong> {i['why']}</p>
<p><strong>Watch for:</strong> {i['watch']}</p></article>"""
    return f"""<section class="ts-card" id="stocking-ideas">
<h2>{p['gallons']} Gallon Fish Tank Stocking Ideas</h2>
{p['ideas_intro_html']}
{items}
<div class="ts-note">{p['ideas_disclaimer_html']}</div>
<div class="cta-row"><a class="btn" href="/tools/fish-compatibility-checker/">Check Fish Compatibility →</a></div>
</section>"""


def render_avoid(p):
    items = ""
    for a in p["avoid"]:
        name = f'<a href="{a["url"]}">{esc(a["name"])}</a>' if a.get("url") else esc(a["name"])
        items += f"""<div class="avoid-item"><div class="avoid-x">✕</div><div><h3>{name}</h3><p>{a['why']}</p><p class="alt">{a['better']}</p></div></div>"""
    return f"""<section class="ts-card" id="avoid">
<h2>Fish That Are Not Suitable for a {p['gallons']} Gallon Tank</h2>
{p['avoid_intro_html']}
{items}
{p.get('avoid_after_html', '')}
</section>"""


def render_setup(p):
    steps = "".join(f"<li><strong>{esc(t)}</strong>{h}</li>" for t, h in p["setup_steps"])
    return f"""<section class="ts-card" id="setup">
<h2>How to Set Up a {p['gallons']} Gallon Fish Tank</h2>
{p['setup_intro_html']}
<ol class="steps">{steps}</ol>
</section>"""


def render_equipment(p):
    e = p["equipment"]
    return f"""<section class="ts-card equip" id="equipment">
<h2>Equipment for a {p['gallons']} Gallon Aquarium</h2>
{p['equipment_intro_html']}
<h3><span>🌀</span>Filter</h3>{e['filter']}
<h3><span>🌡️</span>Heater</h3>{e['heater']}
<div class="cta-row"><a class="btn btn-ghost" href="/tools/aquarium-equipment-calculator/">Size filter, heater &amp; light for your tank →</a></div>
<h3><span>💡</span>Lighting</h3>{e['lighting']}
<h3><span>🪨</span>Substrate</h3>{e['substrate']}
<div class="cta-row"><a class="btn btn-ghost" href="/tools/aquarium-substrate-calculator/">Aquarium substrate calculator →</a></div>
<h3><span>🪵</span>Stand</h3>{e['stand']}
</section>"""


def render_water(p):
    return f"""<section class="ts-card" id="water">
<h2>Water Parameters for a {p['gallons']} Gallon Aquarium</h2>
{p['water_html']}
<div class="cta-row"><a class="btn" href="/tools/water-parameter-checker/">Check Your Water Parameters →</a></div>
</section>"""


def render_maintenance(p):
    return f"""<section class="ts-card" id="maintenance">
<h2>{p['gallons']} Gallon Fish Tank Maintenance</h2>
{p['maintenance_html']}
</section>"""


def render_right(p):
    pros = "".join(f"<li>{x}</li>" for x in p["pros"])
    cons = "".join(f"<li>{x}</li>" for x in p["cons"])
    return f"""<section class="ts-card" id="right-for-you">
<h2>Is a {p['gallons']} Gallon Fish Tank Right for You?</h2>
{p['right_intro_html']}
<div class="procon"><div><h3>✅ Advantages</h3><ul>{pros}</ul></div><div><h3>⚠️ Considerations</h3><ul>{cons}</ul></div></div>
{p['right_verdict_html']}
</section>"""


def render_plan(p):
    g = p["gallons"]
    return f"""<section class="plan-box" id="plan" aria-labelledby="plan-h">
<h2 id="plan-h">Plan Your {g} Gallon Aquarium</h2>
<p>Not sure which fish can live together in your {g}-gallon tank? Build your aquarium and check stocking, compatibility and care requirements before adding fish.</p>
<div class="cta-row">
<a class="btn" href="/tools/aquarium-planner/">Open Aquarium Planner</a>
<a class="btn" href="/tools/fish-compatibility-checker/">Check Compatibility</a>
<a class="btn btn-ghost" href="/tools/aquarium-size-calculator/">Calculate Tank Size</a>
</div>
</section>"""


def render_faq(p):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in p["faqs"])
    return f"""<section class="ts-card faq" id="faq">
<h2>{p['gallons']} Gallon Fish Tank FAQ</h2>
{items}
</section>"""


def render_compare(p):
    cards = "".join(
        f'<a class="cmp-card" href="{c["url"]}"><div class="g">{esc(c["title"])}</div><div class="d">{esc(c["dims"])}</div><p>{c["html"]}</p></a>'
        for c in p["compare"]
    )
    return f"""<section class="ts-card" id="compare">
<h2>Compare Other Aquarium Sizes</h2>
{p['compare_intro_html']}
<div class="cmp">{cards}</div>
<p style="margin-top:14px">Browse every size in the <a href="/tanks/">fish tank size guide</a>, or enter your own dimensions in the <a href="/tools/aquarium-size-calculator/">aquarium size calculator</a>.</p>
</section>"""


def render_methodology(p):
    return f"""<section class="ts-card" id="methodology">
<h2>How FishCare AI Makes Tank Recommendations</h2>
<p>The species, group sizes and stocking combinations on this page are based on the same factors the <a href="/tools/aquarium-planner/">Aquarium Planner</a> and <a href="/tools/fish-compatibility-checker/">Fish Compatibility Checker</a> weigh for every species in our database:</p>
<ul>
<li><strong>Adult size</strong> — we plan around the fish an animal becomes, not the juvenile sold in stores.</li>
<li><strong>Swimming behaviour</strong> — cruising, hovering and darting species need different lengths and depths.</li>
<li><strong>Territorial requirements</strong> — cichlids and some catfish claim floor space that has to exist in the footprint.</li>
<li><strong>Schooling needs</strong> — shoaling species are counted as groups, never as individuals.</li>
<li><strong>Bioload</strong> — body mass, diet and messiness drive the filtration and water-change budget.</li>
<li><strong>Aquarium footprint</strong> — length, width and surface area, not just gallons.</li>
<li><strong>Compatibility</strong> — temperament, size difference and fin-nipping risk between species.</li>
<li><strong>Water requirements</strong> — temperature, pH and hardness overlap across every fish in a combination.</li>
</ul>
<p>{p['methodology_note_html']}</p>
<p>Dimensions and empty weights are typical figures for the size class, not specifications for any particular product; filled weights are estimates built from the assumptions shown. Husbandry ranges are general guidance drawn from mainstream aquarium practice and our <a href="/editorial-policy/">editorial policy</a>, not veterinary or scientific advice. Individual fish, tank layouts and local water vary — check any plan against your own parameters before buying fish.</p>
</section>"""


def render_sidebar(p):
    toc = "".join(f'<a href="#{i}">{esc(t)}</a>' for i, t in SECTIONS)
    facts = "".join(f"<tr><td>{esc(a)}</td><td>{b}</td></tr>" for a, b in p["sidebar_facts"])
    return f"""<aside class="ts-side">
<div class="side-card"><h2>On this page</h2><nav class="ts-toc" aria-label="Page sections">{toc}</nav></div>
<div class="side-card"><h2>Quick facts</h2><table class="qf">{facts}</table></div>
<div class="side-card side-cta"><h3>Plan this tank</h3><p>Pick fish, check compatibility and get a cycling checklist for a {p['gallons']}-gallon setup.</p><a class="btn" href="/tools/aquarium-planner/">Open Aquarium Planner</a></div>
</aside>"""


# ── Structured data ───────────────────────────────────────────────────────────
def schema_blocks(p):
    url = f"{SITE}/tank-sizes/{p['slug']}/"
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Tank Sizes", "item": f"{SITE}/tanks/"},
            {"@type": "ListItem", "position": 3, "name": f"{p['gallons']} Gallon Fish Tank", "item": url},
        ],
    }
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["h1"],
        "description": p["meta_description"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": p["date_published"],
        "dateModified": p["date_modified"],
        "author": {"@type": "Organization", "name": "FishCare AI Editorial Team", "url": f"{SITE}/about/"},
        "publisher": {
            "@type": "Organization",
            "name": "FishCare AI",
            "url": f"{SITE}/",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/fishcare-logo.svg"},
        },
        "about": {"@type": "Thing", "name": f"{p['gallons']} gallon fish tank"},
        "isPartOf": {"@type": "WebSite", "name": "FishCare AI", "url": f"{SITE}/"},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faqs"]
        ],
    }
    def block(o):
        return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>"
    return "\n".join(block(o) for o in (breadcrumb, article, faq))


# ── Page assembly ─────────────────────────────────────────────────────────────
def render_page(p):
    url = f"{SITE}/tank-sizes/{p['slug']}/"
    g = p["gallons"]
    body = "\n".join([
        render_glance(p),
        render_dimensions(p),
        render_weight(p),
        render_stocking(p),
        render_best_fish(p),
        render_ideas(p),
        render_avoid(p),
        render_setup(p),
        render_equipment(p),
        render_water(p),
        render_maintenance(p),
        render_right(p),
        render_plan(p),
        render_faq(p),
        render_compare(p),
        render_methodology(p),
    ])
    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="utf-8"/>
<meta name="apple-itunes-app" content="app-id=6793299571">
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['meta_description'])}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{url}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="FishCare AI"/>
<meta property="og:title" content="{esc(p['title'])}"/>
<meta property="og:description" content="{esc(p['meta_description'])}"/>
<meta property="og:url" content="{url}"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{esc(p['title'])}"/>
<meta name="twitter:description" content="{esc(p['meta_description'])}"/>
{schema_blocks(p)}
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260823-screenshot"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260824-dark-fix"></script>
</head>
<body>
{NAV_HTML}
<main>
<header class="hero">
  <div class="con">
    <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/tanks/">Tank Sizes</a></li><li><span aria-current="page">{g} Gallon Fish Tank</span></li></ol></nav>
    <div class="tag">Tank Size Guide</div>
    <h1>{esc(p['h1'])}</h1>
    <div class="lead">{p['intro_html']}</div>
    <div class="ts-meta"><span>By FishCare AI Editorial Team</span><span>Updated {p['date_modified_human']}</span><span>{p['read_time']} min read</span></div>
  </div>
</header>
<div class="ts-layout">
<article>
{body}
</article>
{render_sidebar(p)}
</div>
</main>
{FOOTER_HTML}
</body>
</html>
"""
