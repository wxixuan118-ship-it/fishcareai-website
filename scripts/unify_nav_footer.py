#!/usr/bin/env python3
"""Unify the navbar and footer across all static pages.

The runtime source of truth is assets/site-compliance.js (it rewrites the
navbar and injects the footer grid on every page, including the Next.js apps
behind /species and /fish-health). This script makes the *static* HTML match
that runtime output, so first paint, no-JS crawlers and the rendered DOM all
agree. The link lists below mirror NAV_ITEMS / FOOTER_* in site-compliance.js
— keep them in sync.

Skips: the homepage (keeps its SPA nav and full footer with the badge rail),
/wiki/ (every slug 301s to /species), /fish-health/ (A/B control frozen until
2026-11-23), pages that opt out via data-global-chrome="false", redirect
stubs, and infrastructure files.

Usage: python3 scripts/unify_nav_footer.py [--apply]   (default: dry run)
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_DIRS = {'.git', 'node_modules', 'data-pipeline', 'reports', 'scripts',
             'docs', 'wiki', 'fish-health', 'admin', 'api', '.og-tmp',
             'sitemaps', '.github', '.claude'}
SKIP_FILES = {'index.html', '__forms.html', 'FishCare.html', 'tools/index.html'}

# ── Mirrors NAV_ITEMS in assets/site-compliance.js ──────────────────────────
NAV_ITEMS = [
    ('Home',          '/',                'home'),
    ('Guides',        '/guides/',         'guides'),
    ('Encyclopedia',  '/species',         'species'),
    ('Compatibility', '/compatibility/',  'compatibility'),
    ('Fish Health',   '/fish-health/',    'fish-health'),
    ('Fish ID',       '/identify/',       'identify'),
    ('About',         '/about/',          'about'),
]
NAV_APP = ('\U0001F4F1 App', '/app/')

FOOTER_EXPLORE = [
    ('All Guides', '/guides/'), ('Encyclopedia', '/species'),
    ('Compatibility Guides', '/compatibility/'), ('Fish Health', '/fish-health/'),
    ('Clownfish Health Problems', '/aquarium-fish-diseases/clownfish/'),
    ('Fish Identification', '/identify/'), ('Tank Size Calculators', '/calculators/'),
]
FOOTER_TOOLS = [
    ('Tank Size Calculator', '/tools/aquarium-size-calculator/'),
    ('Stocking Calculator', '/tools/fish-tank-stocking-calculator/'),
    ('Compatibility Checker', '/tools/fish-compatibility-checker/'),
    ('Water Parameter Checker', '/tools/water-parameter-checker/'),
    ('Betta Water Parameters', '/tools/betta-fish-water-parameters/'),
    ('Feeding Calculator', '/tools/fish-feeding-calculator/'),
    ('Substrate Calculator', '/tools/aquarium-substrate-calculator/'),
    ('Equipment Calculator', '/tools/aquarium-equipment-calculator/'),
    ('Aquarium Planner', '/tools/aquarium-planner/'),
]
FOOTER_POND_TOOLS = [
    ('Koi Pond Calculator', '/tools/koi-pond-calculator/'),
    ('Pond Stocking Calculator', '/tools/koi-pond-stocking-calculator/'),
    ('Koi Feeding Calculator', '/tools/koi-feeding-calculator/'),
    ('Pond Liner Calculator', '/tools/koi-pond-liner-calculator/'),
    ('Pond Pump Calculator', '/tools/koi-pond-pump-calculator/'),
    ('Pond Salt Calculator', '/tools/koi-pond-salt-calculator/'),
]
FOOTER_COMPANY = [
    ('About', '/about/'), ('Contact', '/contact/'), ('Privacy Policy', '/privacy/'),
    ('Terms', '/terms/'), ('Editorial Policy', '/editorial-policy/'),
    ('Resources', '/resources/'), ('Add Your Site', '/add-your-site/'),
    ('☕ Buy me a coffee', 'https://buymeacoffee.com/vikiyananw6'),
]
LEGAL_LINKS = [
    ('About', '/about/'), ('Contact', '/contact/'),
    ('Editorial Policy', '/editorial-policy/'), ('Privacy', '/privacy/'),
    ('Image Credits', '/image-credits/'), ('Add Your Site', '/add-your-site/'),
]


def section_for(rel):
    top = rel.parts[0]
    return {
        'guides': 'guides', 'species': 'species', 'compatibility': 'compatibility',
        'aquarium-fish-diseases': 'fish-health', 'about': 'about',
    }.get(top, '')


def nav_html(section):
    links = []
    for label, href, sec in NAV_ITEMS:
        act = sec == section
        cls = 'nl act' if act else 'nl'
        cur = ' aria-current="page"' if act else ''
        links.append(f'<a class="{cls}" href="{href}"{cur}>{label}</a>')
    links.append(f'<a class="nl nl-app-btn" href="{NAV_APP[1]}">{NAV_APP[0]}</a>')
    return ('<nav class="nb fishcare-global-nav" id="fishcare-global-navigation" aria-label="Main navigation">'
            '<a class="brand" href="/" aria-label="FishCare AI home">'
            '<img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36">'
            '</a>'
            '<div class="nlinks" id="fishcare-nlinks">' + ''.join(links) + '</div>'
            '<button type="button" class="hbg" aria-label="Open navigation menu"'
            ' aria-controls="fishcare-nlinks" aria-expanded="false">'
            '<span></span><span></span><span></span></button>'
            '</nav>')


def col(heading, items):
    links = ''.join(f'<a href="{h}">{l}</a>' for l, h in items)
    return f'<div class="ftcol"><h3>{heading}</h3>{links}</div>'


def footer_html():
    legal = ''.join(f'<a href="{h}">{l}</a>' for l, h in LEGAL_LINKS)
    return ('<footer class="ft">'
            '<div class="con">'
            '<div class="ftg">'
            '<div class="ftbr">'
            '<a class="logo" href="/" aria-label="FishCare AI home"><img class="fishcare-footer-logo-img"'
            ' src="/assets/fishcare-logo.svg" alt="FishCare AI" width="158" height="40" loading="lazy"></a>'
            '<p>Practical aquarium care guides, fish encyclopedia, and free tools for freshwater and saltwater fishkeepers.</p>'
            '</div>'
            + col('Explore', FOOTER_EXPLORE)
            + col('Aquarium Tools', FOOTER_TOOLS)
            + col('Koi &amp; Pond Tools', FOOTER_POND_TOOLS)
            + col('Company', FOOTER_COMPANY)
            + '</div>'
            '<div class="ftb">© 2026 EverTrend LLC. FishCare AI is a product of EverTrend LLC. All rights reserved.</div>'
            f'<nav class="legal-links" aria-label="Legal and company information">{legal}</nav>'
            '</div>'
            '</footer>')


NAV_RE = re.compile(r'<nav class="nb[^"]*"[^>]*>.*?</nav>', re.S)
FOOTER_RE = re.compile(r'<footer[^>]*>.*?</footer>', re.S)
BODY_RE = re.compile(r'<body[^>]*>')


def process(path, apply):
    t = path.read_text(errors='ignore')
    if 'http-equiv="refresh"' in t[:600]:
        return 'skip-redirect'
    if 'data-global-chrome="false"' in t[:600]:
        return 'skip-optout'
    if '<body' not in t or '</body>' not in t:
        return 'skip-nobody'
    rel = path.relative_to(ROOT)
    section = section_for(rel)
    orig = t

    # navbar: replace the first .nb nav, drop duplicates, insert if missing
    if NAV_RE.search(t):
        first = [True]
        def repl(m):
            if first[0]:
                first[0] = False
                return nav_html(section)
            return ''
        t = NAV_RE.sub(repl, t)
        nav_s = 'nav-replaced'
    else:
        t = BODY_RE.sub(lambda m: m.group(0) + '\n' + nav_html(section), t, count=1)
        nav_s = 'nav-inserted'

    # footer: replace the last <footer>, insert if missing
    foots = FOOTER_RE.findall(t)
    if foots:
        last = foots[-1]
        idx = t.rfind(last)
        t = t[:idx] + footer_html() + t[idx + len(last):]
        foot_s = 'footer-replaced'
    else:
        idx = t.rfind('</body>')
        t = t[:idx] + footer_html() + '\n' + t[idx:]
        foot_s = 'footer-inserted'

    # make sure the chrome is styled and the runtime script is loaded
    extra = []
    if 'fishcare-glass-redesign' not in t and '/assets/site-chrome.css' not in t:
        t = t.replace('</head>', '<link rel="stylesheet" href="/assets/site-chrome.css"></head>', 1)
        extra.append('chrome-css')
    if 'site-compliance.js' not in t:
        t = t.replace('</head>', '<script src="/assets/site-compliance.js" defer></script></head>', 1)
        extra.append('compliance-js')

    if t != orig and apply:
        path.write_text(t)
    return '+'.join([nav_s, foot_s] + extra)


def main():
    apply = '--apply' in sys.argv
    counts = {}
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or str(rel) in SKIP_FILES or rel.name.startswith('yandex_'):
            continue
        s = process(p, apply)
        counts[s] = counts.get(s, 0) + 1
    print('APPLIED' if apply else 'DRY RUN')
    for k in sorted(counts, key=counts.get, reverse=True):
        print(f'{counts[k]:6}  {k}')


if __name__ == '__main__':
    main()
