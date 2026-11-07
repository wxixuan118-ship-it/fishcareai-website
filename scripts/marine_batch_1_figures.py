"""Charts and diagrams for build-marine-batch-1.py. Writes SVGs to assets/guides/marine/."""
from html import escape
from pathlib import Path

BG = "#0a2a42"
PANEL = "#123a56"
INK = "#ffffff"
MUTED = "#c4dbe8"
GRID = "#3b6680"
BLUE = "#1e90d6"
AMBER = "#c47a0a"
GREEN = "#1f9d7a"
FONT = "-apple-system,Segoe UI,Arial,sans-serif"


def t(x, y, s, size=22, weight=400, fill=INK, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'


def r(x, y, w, h, fill, rx=4, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def line(x1, y1, x2, y2, color=GRID, w=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"/>'


def arrow(x1, y1, x2, y2, color=MUTED):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" marker-end="url(#a)"/>'


def svg(w, h, title, desc, inner):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">\n'
        f"<title id=\"t\">{escape(title)}</title>\n<desc id=\"d\">{escape(desc)}</desc>\n"
        f'<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="{MUTED}"/></marker></defs>\n'
        f'<rect width="{w}" height="{h}" rx="20" fill="{BG}"/>\n' + "\n".join(inner) + "\n</svg>\n"
    )


def rows(items, y0, title):
    out = [t(36, 52, title, 28, 800)]
    y = y0
    for head, body in items:
        out += [r(36, y, 648, 74, PANEL, 12), t(56, y + 32, head, 22, 700), t(56, y + 60, body, 20, 400, MUTED)]
        y += 86
    return out


def quarantine_timeline():
    inner = rows([
        ("Arrival", "Match water slowly. Discard store water."),
        ("Week 1", "Check daily. Test ammonia and nitrite often."),
        ("Weeks 2–4", "Watch for spots, rubbing and fast breathing."),
        ("Weeks 4–6", "Eating and breathing normally? Keep watching."),
        ("Moving day", "Acclimate. Leave quarantine water behind."),
    ], 80, "Saltwater fish quarantine: 4–6 weeks")
    return svg(720, 520, "Saltwater fish quarantine timeline", "Five stages from arrival to moving day across a 4 to 6 week saltwater fish quarantine.", inner)


def quarantine_tank():
    inner = [
        t(36, 52, "Saltwater quarantine tank setup", 28, 800),
        r(90, 110, 540, 300, "#16597d", 6, f'stroke="{MUTED}" stroke-width="4"'),
        r(80, 96, 560, 14, MUTED, 4),
        r(110, 110, 60, 110, "#2c3e50", 6),
        r(555, 120, 16, 170, AMBER, 8),
        r(250, 372, 120, 34, "#d7dfe5", 17),
        r(250, 380, 24, 18, BG, 6),
        r(346, 380, 24, 18, BG, 6),
        r(455, 396, 44, 12, "#e8eef2", 6),
    ]
    inner += [f'<circle cx="{477 + dx}" cy="{cy}" r="{cr}" fill="#ffffff" opacity=".65"/>' for dx, cy, cr in [(-6, 380, 4), (5, 360, 5), (-3, 335, 4), (6, 305, 5), (-4, 275, 4)]]
    inner += [
        t(360, 88, "Tight lid, dim light", 20, 600, INK, "middle"),
        t(180, 170, "Filter with", 20, 600), t(180, 196, "mature media", 20, 600),
        t(545, 200, "Heater", 20, 600, INK, "end"),
        t(310, 358, "PVC hide", 20, 600, INK, "middle"),
        t(445, 345, "Air", 20, 600, INK, "end"), t(445, 370, "stone", 20, 600, INK, "end"),
        t(360, 448, "Bare bottom: no sand or rock", 22, 700, INK, "middle"),
        t(360, 480, "Separate nets and siphons, 3 ft from the display", 20, 400, MUTED, "middle"),
    ]
    return svg(720, 510, "Saltwater fish quarantine tank setup diagram", "A bare-bottom quarantine tank with a tight lid, filter with mature media, heater, PVC hide and air stone.", inner)


def ich_cycle():
    def box(x, y, name, where, time, hi=False):
        fill = GREEN if hi else PANEL
        return [r(x, y, 300, 134, fill, 14), t(x + 18, y + 38, name, 25, 800), t(x + 18, y + 72, where, 20, 400, INK if hi else MUTED), t(x + 18, y + 106, time, 20, 700)]
    inner = [t(36, 52, "Marine ich life cycle", 28, 800)]
    inner += box(36, 84, "Trophont", "Feeds under the skin", "About 3–7 days")
    inner += box(384, 84, "Protomont", "Moves onto a surface", "About 2–18 hours")
    inner += box(384, 292, "Tomont", "Protected cyst", "Most 4–8 days, up to 72")
    inner += box(36, 292, "Theront", "Swims to find a fish", "Treatment target", True)
    inner += [arrow(340, 151, 380, 151), arrow(534, 222, 534, 288), arrow(380, 359, 340, 359), arrow(186, 288, 186, 222)]
    inner += [t(36, 470, "Spots fading doesn't mean the parasite has gone.", 22, 600, MUTED)]
    return svg(720, 500, "Marine ich life cycle diagram", "Marine ich moves from trophont on the fish to protomont, tomont cyst and free-swimming theront, the main treatment target.", inner)


def ich_timing():
    x0, x1, dmax = 36, 684, 80
    sx = lambda d: x0 + (x1 - x0) * d / dmax
    data = [
        ("Trophont feeding on fish", 3, 7, "3–7 days"),
        ("Most tomonts release", 4, 8, "4–8 days"),
        ("Copper treatment minimum", 21, 42, "21–42 days"),
        ("Longest tomont release reported", 3, 72, "3–72 days"),
    ]
    inner = [t(36, 52, "Why saltwater ich treatment takes weeks", 28, 800)]
    y = 92
    for name, a, b, lab in data:
        inner += [t(36, y, f"{name}: {lab}", 21, 500), r(sx(a), y + 12, max(sx(b) - sx(a), 8), 20, BLUE, 4)]
        y += 78
    axis_y = y + 2
    inner.append(line(x0, axis_y, x1, axis_y))
    for d in range(0, 81, 20):
        inner += [line(sx(d), axis_y, sx(d), axis_y + 8), t(sx(d), axis_y + 34, str(d), 20, 400, MUTED, "middle" if 0 < d < 80 else ("start" if d == 0 else "end"))]
    inner.append(t(360, axis_y + 66, "Days (sources: UF/IFAS FA164)", 20, 400, MUTED, "middle"))
    return svg(720, axis_y + 90, "Saltwater ich treatment timing chart", "Trophonts feed for 3 to 7 days and most tomonts release in 4 to 8 days, but release has been reported up to 72 days, so copper runs at least 21 to 42 days.", inner)


def salinity_scale():
    x0, x1, lo, hi = 50, 670, 30, 38
    sx = lambda p: round(x0 + (x1 - x0) * (p - lo) / (hi - lo), 1)
    inner = [
        t(36, 52, "Reef tank salinity target", 28, 800),
        r(x0, 170, x1 - x0, 44, PANEL, 8),
        r(sx(32), 170, sx(36) - sx(32), 44, GREEN, 8),
        t((sx(32) + sx(36)) / 2, 199, "Reef range 32–36 ppt", 21, 700, INK, "middle"),
        line(sx(33.2), 118, sx(33.2), 170, INK, 3), t(sx(33.2), 106, "SG 1.025", 21, 700, INK, "middle"),
        line(sx(35), 88, sx(35), 170, INK, 3), t(sx(35) + 8, 78, "SG 1.0264", 21, 700, INK, "start"),
        t(sx(35) + 8, 106, "natural seawater", 19, 400, MUTED, "start"),
    ]
    for p, sg in [(30, "1.0226"), (32, "1.0241"), (34, "1.0256"), (36, "1.0271"), (38, "1.0286")]:
        a = "start" if p == 30 else "end" if p == 38 else "middle"
        inner += [line(sx(p), 214, sx(p), 224), t(sx(p), 252, f"{p} ppt", 20, 600, INK, a), t(sx(p), 280, sg, 19, 400, MUTED, a)]
    inner.append(t(36, 322, "SG values at 25°C, from Randy Holmes-Farley's table.", 19, 400, MUTED))
    return svg(720, 345, "Reef tank salinity scale", "Reef range 32 to 36 ppt, with SG 1.025 at about 33 ppt and natural seawater at 35 ppt, SG 1.0264.", inner)


def salinity_cycle():
    inner = rows([
        ("1. Fresh water evaporates", "Salt stays behind in the tank."),
        ("2. Salinity slowly rises", "Check it 1–3 times a week."),
        ("3. Top off with RO/DI only", "Salt water would push salinity higher."),
        ("4. Retest after mixing", "Change in small steps, not all at once."),
    ], 80, "Why reef tank salinity drifts")
    return svg(720, 430, "Why reef tank salinity drifts", "Evaporation removes fresh water, salinity rises, and topping off with RO/DI water brings it back.", inner)


def heater_bars():
    data = [(10, 50), (20, 100), (29, 145), (40, 200), (55, 275), (75, 225), (125, 375)]
    base, top, x0, step, bw = 400, 110, 56, 90, 56
    inner = [t(36, 52, "Aquarium heater watts at a 10°F rise", 28, 800), t(36, 84, "Closed lid. Estimate from this calculator.", 20, 400, MUTED)]
    for v in (100, 200, 300, 400):
        y = base - (base - top) * v / 400
        inner += [line(x0, y, 696, y, "#24506b", 1)]
    inner.append(line(x0, base, 696, base))
    for i, (g, w) in enumerate(data):
        x = x0 + 12 + i * step
        h = (base - top) * w / 400
        inner += [r(x, base - h, bw, h, BLUE, 4), t(x + bw / 2, base - h - 10, f"{w} W", 20, 700, INK, "middle"), t(x + bw / 2, base + 30, f"{g} gal", 20, 500, MUTED, "middle")]
    inner.append(t(36, 468, "Watts per gallon taper above 55 gallons.", 20, 400, MUTED))
    return svg(720, 490, "Aquarium heater calculator wattage chart", "Estimated heater watts at a 10 degree Fahrenheit rise: 10 gallons 50 W, 20 gallons 100 W, 29 gallons 145 W, 40 gallons 200 W, 55 gallons 275 W, 75 gallons 225 W, 125 gallons 375 W.", inner)


def heater_steps():
    inner = rows([
        ("1. Find the temperature rise", "78°F target − 68°F room = 10°F"),
        ("2. Multiply by tank size", "20 gal × 0.5 W × 10°F = 100 W"),
        ("3. Adjust for an open top", "Closed lid here, so no change"),
        ("4. Round up to a heater size", "One 100 W heater, or two 50 W heaters"),
    ], 80, "Aquarium heater calculation example")
    return svg(720, 430, "Aquarium heater calculation example", "A 20 gallon tank raised 10 degrees Fahrenheit above the room needs about 100 watts.", inner)


def legend(items, y):
    out, x = [], 36
    for name, color in items:
        out += [r(x, y - 16, 20, 20, color, 4), t(x + 28, y, name, 20, 500, MUTED)]
        x += 44 + len(name) * 11
    return out


def weight_bars():
    data = [(10, 83, 11), (20, 167, 25), (29, 242, 40), (40, 334, 58), (55, 459, 78), (75, 626, 140), (125, 1043, 206)]
    x0, x1, vmax = 116, 590, 1300
    sc = lambda v: (x1 - x0) * v / vmax
    inner = [t(36, 52, "Aquarium weight by tank size", 28, 800)] + legend([("Fresh water", BLUE), ("Empty glass tank", AMBER)], 92)
    y = 118
    for g, w, e in data:
        ww, we = sc(w), sc(e)
        inner += [t(36, y + 24, f"{g} gal", 21, 600), r(x0, y, ww - 2, 34, BLUE, 4), r(x0 + ww, y, max(we, 3), 34, AMBER, 4), t(x0 + ww + we + 10, y + 24, f"{w + e:,} lb", 20, 700)]
        y += 50
    inner.append(t(36, y + 22, "Before substrate, rock, equipment and stand.", 20, 400, MUTED))
    return svg(720, y + 44, "Aquarium weight calculator chart by tank size", "Water plus empty glass weight: 10 gallons 94 lb, 20 gallons 192 lb, 29 gallons 282 lb, 40 gallons 392 lb, 55 gallons 537 lb, 75 gallons 766 lb, 125 gallons 1,249 lb.", inner)


def weight_compare():
    x0, x1, vmax = 36, 684, 760
    sc = lambda v: (x1 - x0) * v / vmax
    rowsd = [("Freshwater example", [(459, BLUE), (78, AMBER), (55, GREEN)]), ("Reef example", [(470, BLUE), (78, AMBER), (165, GREEN)])]
    inner = [t(36, 52, "Where a 55 gallon tank's weight goes", 28, 800)] + legend([("Water", BLUE), ("Glass", AMBER), ("Sand and rock", GREEN)], 92)
    y = 126
    for name, seg in rowsd:
        total = sum(v for v, _ in seg)
        inner.append(t(36, y, f"{name}: {total} lb", 22, 700))
        x = x0
        for v, c in seg:
            inner.append(r(round(x, 1), y + 12, round(sc(v) - 2, 1), 40, c, 4))
            x += sc(v)
        y += 96
    inner.append(t(36, y, "Rock and sand amounts are examples. Enter your own above.", 20, 400, MUTED))
    return svg(720, y + 24, "Aquarium weight breakdown for a 55 gallon tank", "A 55 gallon freshwater example totals 592 lb and a reef example with more sand and rock totals 713 lb, with water making up most of the weight.", inner)


FIGURES = {
    "saltwater-fish-quarantine-timeline": quarantine_timeline,
    "saltwater-fish-quarantine-tank-setup": quarantine_tank,
    "saltwater-ich-treatment-life-cycle": ich_cycle,
    "saltwater-ich-treatment-timing": ich_timing,
    "reef-tank-salinity-scale": salinity_scale,
    "reef-tank-salinity-evaporation": salinity_cycle,
    "aquarium-heater-calculator-watts": heater_bars,
    "aquarium-heater-calculator-example": heater_steps,
    "aquarium-weight-calculator-by-size": weight_bars,
    "aquarium-weight-calculator-breakdown": weight_compare,
}


def write_all(root):
    outdir = Path(root) / "assets/guides/marine"
    outdir.mkdir(parents=True, exist_ok=True)
    dims = {}
    for name, fn in FIGURES.items():
        s = fn()
        (outdir / f"{name}.svg").write_text(s, encoding="utf-8")
        head = s[:200]
        w = head.split('width="')[1].split('"')[0]
        h = head.split('height="')[1].split('"')[0]
        dims[name] = (w, h)
    return dims
