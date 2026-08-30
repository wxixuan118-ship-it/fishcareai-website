/**
 * Injects the "Share this page / Cite this page" module into the static guide
 * pages, just before </main>.
 *
 * The module gives readers a one-click way to share the page and a ready-made
 * citation plus a copy-paste HTML link — the shape of thing that earns inbound
 * links rather than asking for them.
 *
 * Idempotent: the block is wrapped in <!--sharecite:start--> / <!--sharecite:end-->
 * markers and replaced wholesale on re-run, so this is safe to run after any
 * content edit.
 *
 * Tool pages are NOT handled here. tools/aquarium-planner/ builds its body from
 * an inline script that overwrites the container on load, so its copy of this
 * module lives in that page's own render function and is baked in by
 * scripts/prerender.mjs instead.
 *
 *   npm run share-cite
 */
import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const START = '<!--sharecite:start-->';
const END = '<!--sharecite:end-->';
const SITE = 'https://www.fishcareai.com';
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const h = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const unent = (s) =>
  String(s).replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#0?39;|&apos;/g, "'").replace(/&nbsp;/g, ' ');

/**
 * @param {string} title  plain-text page title (no entities)
 * @param {string} url    absolute canonical URL
 * @param {string} noun   "guide" | "tool" — used in the heading
 */
export function shareCiteHtml(title, url, noun = 'guide') {
  const t = h(title);
  const u = h(url);
  const eu = encodeURIComponent(url);
  const et = encodeURIComponent(title);
  const embed = h(`<a href="${url}">${title}</a>`);

  return `<section class="sharecite" aria-labelledby="sharecite-heading">
  <h2 id="sharecite-heading">Share this ${noun}</h2>
  <p class="sc-hint">Found this useful? Pass it on, or cite it in your own write-up.</p>
  <div class="sc-row">
    <a class="sc-btn btn" href="https://x.com/intent/post?url=${eu}&amp;text=${et}" target="_blank" rel="noopener nofollow">Share on X</a>
    <a class="sc-btn btn" href="https://www.facebook.com/sharer/sharer.php?u=${eu}" target="_blank" rel="noopener nofollow">Facebook</a>
    <a class="sc-btn btn" href="https://www.reddit.com/submit?url=${eu}&amp;title=${et}" target="_blank" rel="noopener nofollow">Reddit</a>
    <a class="sc-btn btn" href="https://pinterest.com/pin/create/button/?url=${eu}&amp;description=${et}" target="_blank" rel="noopener nofollow">Pinterest</a>
    <button type="button" class="sc-btn" data-sc-copy="#sc-url"><span data-sc-label>Copy link</span></button>
  </div>
  <div hidden id="sc-url">${u}</div>

  <h3>Cite this page</h3>
  <div class="sc-box" id="sc-citation">FishCare AI. &ldquo;${t}.&rdquo; <em>FishCare AI</em>, ${u}.<span data-sc-accessed></span></div>
  <div class="sc-row">
    <button type="button" class="sc-btn" data-sc-copy="#sc-citation"><span data-sc-label>Copy citation</span></button>
  </div>

  <h3>Link to this page</h3>
  <div class="sc-box"><code id="sc-embed">${embed}</code></div>
  <div class="sc-row">
    <button type="button" class="sc-btn" data-sc-copy="#sc-embed"><span data-sc-label>Copy HTML</span></button>
  </div>
</section>`;
}

function ensureAssets(html) {
  let out = html;
  if (!out.includes('/assets/share-cite.css')) {
    out = out.replace('</head>', '<link rel="stylesheet" href="/assets/share-cite.css"/>\n</head>');
  }
  if (!out.includes('/assets/share-cite.js')) {
    out = out.replace('</head>', '<script defer src="/assets/share-cite.js"></script>\n</head>');
  }
  return out;
}

function pageMeta(html, file) {
  const canon = html.match(/<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)["']/i);
  const url = canon
    ? canon[1]
    : `${SITE}/${path.dirname(file).replace(/^\.\//, '')}/`.replace(/\/+$/, '/');

  // Prefer the visible H1; fall back to <title> with the brand suffix trimmed.
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  let title = h1 ? h1[1].replace(/<[^>]+>/g, '') : '';
  if (!title) {
    const t = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
    title = t ? t[1].replace(/\s*[|—-]\s*FishCare AI\s*$/i, '') : '';
  }
  return { url, title: unent(title).replace(/\s+/g, ' ').trim() };
}

const root = process.cwd();
let changed = 0;
let skipped = 0;
// fs.glob needs Node 22; this repo runs Node 20.
const dirs = await readdir(path.join(root, 'guides'), { withFileTypes: true });
const files = dirs
  .filter((d) => d.isDirectory())
  .map((d) => `guides/${d.name}/index.html`)
  .sort();

for (const rel of files) {
  const file = path.join(root, rel);
  let before;
  try {
    before = await readFile(file, 'utf8');
  } catch {
    // Directory without an index.html (e.g. guides/discus-fish-care/, which
    // 301s to the -requirements page in nginx.conf).
    skipped++;
    continue;
  }

  if (!before.includes('</main>')) {
    console.warn(`  ! ${rel} — no </main> anchor, skipped`);
    skipped++;
    continue;
  }
  const { url, title } = pageMeta(before, rel);
  if (!title) {
    console.warn(`  ! ${rel} — no title/h1 found, skipped`);
    skipped++;
    continue;
  }

  const block = `${START}\n${shareCiteHtml(title, url, 'guide')}\n${END}`;
  let after = before.includes(START)
    ? before.replace(new RegExp(esc(START) + '[\\s\\S]*?' + esc(END)), block)
    : before.replace('</main>', `${block}\n</main>`);
  after = ensureAssets(after);

  if (after !== before) {
    await writeFile(file, after, 'utf8');
    changed++;
  }
}
console.log(`Share/Cite: ${files.length} guide(s), ${changed} written, ${skipped} skipped.`);
