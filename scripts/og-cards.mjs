/**
 * Generates social / SERP cards for the FishCare AI tool pages.
 *
 * Each card draws a mock of the tool's own interface — form fields, a submit
 * button, a result panel — so the image reads as "this is an interactive tool"
 * rather than the generic aquarium photo every tool page shared before.
 *
 * Two sizes per tool, because Google centre-crops thumbnails on mobile and a
 * wide card loses its headline in a square crop:
 *   1200x630   <tool>-tool-card.png          og:image / twitter:image, desktop
 *   1200x1200  <tool>-tool-card-square.png   structured data, mobile SERP
 *
 * Rendered with headless Chrome, so this runs on a workstation rather than in
 * the Docker build. Output PNGs are committed to assets/tool-cards/.
 *
 *   npm run og:cards              # all tools
 *   npm run og:cards -- planner   # one tool
 */
import { writeFile, mkdir } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const run = promisify(execFile);
const CHROME =
  process.env.CHROME_PATH ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

export const TOOLS = {
  planner: {
    out: 'aquarium-planner-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '🧭',
    title: 'Aquarium Planner',
    sub: 'Setup checklist, equipment list &amp; stocking guide — before you buy.',
    chips: ['Equipment', 'Stocking', 'Cycling'],
    fields: [
      ['Tank type', 'Freshwater'],
      ['Primary goal', 'Peaceful community'],
    ],
    input: ['Tank volume (gallons)', '20'],
    cta: 'Create Aquarium Plan',
    result: ['Flexible beginner size', '20 gallon freshwater plan'],
  },
  tank: {
    out: 'tank-size-calculator-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '📏',
    title: 'Tank Size Calculator',
    sub: 'US gallons, UK gallons and litres from your tank dimensions.',
    chips: ['Gallons', 'Litres', 'Stocking'],
    fields: [
      ['Species', 'Neon tetra'],
      ['How many fish', '12'],
    ],
    input: ['Tank length (inches)', '30'],
    cta: 'Calculate Tank Size',
    result: ['20+ gal', 'Practical minimum for 12 neon tetras'],
  },
  compat: {
    out: 'fish-compatibility-checker-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '🔬',
    title: 'Fish Compatibility Checker',
    sub: 'Test species in pairs for aggression, pH and temperature clashes.',
    chips: ['Aggression', 'pH match', 'Temperature'],
    fields: [
      ['Species A', 'Betta'],
      ['Species B', 'Neon tetra'],
    ],
    input: ['Tank volume (gallons)', '20'],
    cta: 'Check Compatibility',
    result: ['Caution', 'Fin-nipping risk in small tanks'],
  },
  water: {
    out: 'water-parameter-checker-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '💧',
    title: 'Water Parameter Checker',
    sub: 'Score pH, ammonia, nitrite and nitrate against safe ranges.',
    chips: ['pH', 'Ammonia', 'Nitrate'],
    fields: [
      ['pH', '7.4'],
      ['Ammonia (ppm)', '0.25'],
    ],
    input: ['Nitrate (ppm)', '20'],
    cta: 'Check Water Quality',
    result: ['Needs attention', 'Ammonia above safe range'],
  },
  feeding: {
    out: 'fish-feeding-calculator-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '🍽',
    title: 'Fish Feeding Calculator',
    sub: 'Portion size, food type and feeding schedule by species.',
    chips: ['Portions', 'Schedule', 'Food type'],
    fields: [
      ['Species', 'Goldfish'],
      ['Life stage', 'Adult'],
    ],
    input: ['How many fish', '4'],
    cta: 'Build Feeding Plan',
    result: ['2× daily', 'Feed only what is eaten in 60 seconds'],
  },
  size: {
    out: 'aquarium-size-calculator-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '📐',
    title: 'Aquarium Size Calculator',
    sub: 'Tank volume in gallons and litres from your inside dimensions.',
    chips: ['US gallons', 'Litres', 'Filled volume'],
    fields: [
      ['Tank shape', 'Rectangular'],
      ['Length × Width (in)', '30 × 12'],
    ],
    input: ['Height (inches)', '18'],
    cta: 'Calculate Volume',
    result: ['28.1 US gal', '106 litres · 23.4 UK gallons'],
  },
  equipment: {
    out: 'aquarium-equipment-calculator-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '⚙️',
    title: 'Aquarium Equipment Calculator',
    sub: 'Filter, heater and light sizing from your tank volume.',
    chips: ['Filter GPH', 'Heater watts', 'Lighting'],
    fields: [
      ['Tank volume (gallons)', '40'],
      ['Setup type', 'Planted freshwater'],
    ],
    input: ['Room temperature (°F)', '68'],
    cta: 'Size My Equipment',
    result: ['160+ GPH filter', '150 W heater · medium light'],
  },
  fishid: {
    out: 'fish-identification-tool-card.png',
    eyebrow: 'FREE TOOL',
    icon: '🔍',
    title: 'Fish Identification',
    sub: 'Identify a fish from a photo, then get its care requirements.',
    chips: ['Photo match', 'Species', 'Care needs'],
    fields: [
      ['Photo', 'betta-tank.jpg'],
      ['Water type', 'Freshwater'],
    ],
    input: ['Approx. size (inches)', '2.5'],
    cta: 'Identify This Fish',
    result: ['Betta splendens', 'Siamese fighting fish · 92% match'],
  },
};

const card = (t, sq = false) => `<!doctype html><meta charset="utf-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1200px;height:${sq ? 1200 : 630}px}
  body{
    font-family:-apple-system,'SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif;
    background:
      radial-gradient(900px 480px at 88% 8%, rgba(70,182,232,.30), transparent 62%),
      radial-gradient(700px 420px at 4% 96%, rgba(24,169,153,.26), transparent 60%),
      linear-gradient(160deg,#07223F 0%,#0C3160 52%,#0A2748 100%);
    color:#fff;display:flex;align-items:center;overflow:hidden;position:relative;
  }
  /* subtle waterline arcs */
  body::after{
    content:'';position:absolute;inset:0;
    background:
      radial-gradient(circle at 92% 92%, rgba(255,255,255,.05) 0 2px, transparent 3px),
      radial-gradient(circle at 12% 18%, rgba(255,255,255,.05) 0 2px, transparent 3px);
    pointer-events:none;
  }
  .wrap{display:flex;width:100%;position:relative;z-index:1;
    ${sq
      ? 'flex-direction:column;justify-content:center;padding:82px 78px;gap:40px;align-items:stretch'
      : 'padding:64px 68px;gap:52px;align-items:center'}}
  .left{${sq ? '' : 'flex:1 1 56%;'}min-width:0}
  .right{${sq ? '' : 'flex:0 0 400px'}}

  .brandrow{display:flex;align-items:center;gap:12px;margin-bottom:26px}
  .mark{width:44px;height:44px;border-radius:12px;flex:none;
    background:linear-gradient(135deg,#46B6E8,#1687C7);
    display:flex;align-items:center;justify-content:center;font-size:24px;
    box-shadow:0 8px 22px rgba(22,135,199,.45)}
  .bname{font-size:19px;font-weight:800;letter-spacing:.2px}
  .bname span{color:#7DD9FF}
  .eyebrow{margin-left:6px;font-size:12px;font-weight:800;letter-spacing:.14em;
    padding:6px 12px;border-radius:999px;color:#9BE4FF;
    background:rgba(125,217,255,.14);border:1px solid rgba(125,217,255,.32)}

  h1{font-size:${sq ? 78 : 60}px;line-height:1.04;font-weight:800;letter-spacing:-1.4px;margin-bottom:18px}
  .sub{font-size:${sq ? 27 : 22}px;line-height:1.42;color:rgba(255,255,255,.76);max-width:${sq ? 900 : 520}px;margin-bottom:30px}
  .chips{display:flex;gap:10px;flex-wrap:wrap}
  .chip{display:flex;align-items:center;gap:7px;font-size:15px;font-weight:650;
    padding:9px 15px;border-radius:999px;color:#EAF8FF;
    background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.16)}
  .tick{width:17px;height:17px;border-radius:50%;background:#27AE60;flex:none;
    display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;font-weight:900}

  /* mock tool panel */
  .panel{background:rgba(255,255,255,.97);border-radius:22px;padding:26px 24px;
    box-shadow:0 30px 70px rgba(0,0,0,.42);color:#123047}
  .ptitle{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:800;
    color:#0F3D6E;margin-bottom:18px}
  .fg{margin-bottom:14px}
  .lb{font-size:12px;font-weight:750;color:#527895;margin-bottom:6px}
  .fc{border:1.5px solid #BFE4F6;border-radius:9px;padding:11px 13px;font-size:15px;
    font-weight:650;color:#123047;background:#fff;display:flex;
    align-items:center;justify-content:space-between}
  .fc.focus{border-color:#1687C7;box-shadow:0 0 0 3px rgba(22,135,199,.16)}
  .car{color:#527895;font-size:11px}
  .btn{margin-top:18px;padding:13px;border-radius:999px;text-align:center;
    font-size:15px;font-weight:800;color:#fff;
    background:linear-gradient(135deg,#46B6E8,#6E7BF2);
    box-shadow:0 12px 26px rgba(70,182,232,.42)}
  .res{margin-top:16px;border-radius:13px;padding:14px 16px;
    background:linear-gradient(135deg,#0F3D6E,#155C98);color:#fff}
  .rn{font-size:19px;font-weight:800;margin-bottom:3px;letter-spacing:-.3px}
  .rl{font-size:12.5px;color:rgba(255,255,255,.82);line-height:1.35}
</style>
<div class="wrap">
  <div class="left">
    <div class="brandrow">
      <div class="mark">${t.icon}</div>
      <div class="bname">FishCare<span> AI</span></div>
      <div class="eyebrow">${t.eyebrow}</div>
    </div>
    <h1>${t.title}</h1>
    <div class="sub">${t.sub}</div>
    <div class="chips">
      ${t.chips.map((c) => `<div class="chip"><div class="tick">✓</div>${c}</div>`).join('')}
    </div>
  </div>
  <div class="right">
    <div class="panel">
      <div class="ptitle">${t.icon} ${t.title}</div>
      ${t.fields.map(([l, v]) => `<div class="fg"><div class="lb">${l}</div><div class="fc">${v}<span class="car">▾</span></div></div>`).join('')}
      <div class="fg"><div class="lb">${t.input[0]}</div><div class="fc focus">${t.input[1]}</div></div>
      <div class="btn">${t.cta} →</div>
      <div class="res"><div class="rn">${t.result[0]}</div><div class="rl">${t.result[1]}</div></div>
    </div>
  </div>
</div>`;

export async function build(keys, outDir, tmpDir) {
  await mkdir(tmpDir, { recursive: true });
  const made = [];
  for (const k of keys) {
    const t = TOOLS[k];
    for (const sq of [false, true]) {
      const name = sq ? t.out.replace(/\.png$/, '-square.png') : t.out;
      const html = path.join(tmpDir, `${k}${sq ? '-sq' : ''}.html`);
      const png = path.join(outDir, name);
      await writeFile(html, card(t, sq), 'utf8');
      await run(CHROME, [
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        '--force-device-scale-factor=1',
        `--window-size=1200,${sq ? 1200 : 630}`,
        `--screenshot=${png}`,
        `file://${html}`,
      ]);
      made.push(png);
      console.log('  ✓', name);
    }
  }
  return made;
}

// pathToFileURL, not `file://${argv[1]}` — the repo path contains spaces,
// which import.meta.url percent-encodes.
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const keys = process.argv[2] ? process.argv[2].split(',') : Object.keys(TOOLS);
  const unknown = keys.filter((k) => !TOOLS[k]);
  if (unknown.length) {
    console.error(`Unknown tool(s): ${unknown.join(', ')}. Known: ${Object.keys(TOOLS).join(', ')}`);
    process.exit(1);
  }
  const outDir = path.join(process.cwd(), 'assets', 'tool-cards');
  await mkdir(outDir, { recursive: true });
  await build(keys, outDir, path.join(process.cwd(), '.og-tmp'));
  console.log(`OG cards: ${keys.length} tool(s) → assets/tool-cards/`);
}
