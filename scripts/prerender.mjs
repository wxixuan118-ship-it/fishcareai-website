/**
 * Build-time SEO prerender for JS-shell pages.
 *
 * A few pages (currently only /tools/aquarium-planner/) render their entire
 * body from an inline <script> that expands template literals like ${longSeo}
 * into an empty <div id="page-tools">. A crawler that does not execute JS sees
 * ~120 words (nav + footer) instead of the ~1,500-word guide that is actually
 * in the file.
 *
 * This script loads each target page in jsdom, lets its own inline script run
 * (initSite() reads window.location.pathname and renders the matching view),
 * extracts the rendered container HTML, and bakes it back into the static file
 * between <!--prerender:start--> / <!--prerender:end--> markers. The shipped
 * page then contains the full content on first byte; when the browser runs the
 * page script it re-renders the same container with full interactivity.
 *
 * Idempotent: re-running replaces the block between the markers.
 * Run standalone with `npm run prerender`, or as part of `npm run build`.
 */
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { JSDOM } from 'jsdom';

const root = process.cwd();
const START = '<!--prerender:start-->';
const END = '<!--prerender:end-->';
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/**
 * containerId  – the <div id="..."> the page script renders into
 * emptyAnchor  – exact static markup of that div before any prerender pass
 */
const TARGETS = [
  {
    file: 'tools/aquarium-planner/index.html',
    url: 'https://www.fishcareai.com/tools/aquarium-planner/',
    containerId: 'page-tools',
    emptyAnchor: '<div id="page-tools" class="hide"></div>',
  },
];

async function renderContainer(html, url, containerId) {
  const dom = new JSDOM(html, {
    url,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    // Only inline scripts run; external/defer scripts and other subresources
    // are not fetched (jsdom default), which is what we want for a content snapshot.
    beforeParse(window) {
      window.scrollTo = () => {};
    },
  });
  // The page script's initSite() IIFE runs synchronously during parse; this tick
  // is just belt-and-braces for any queued microtasks.
  await new Promise((r) => setTimeout(r, 30));

  const el = dom.window.document.getElementById(containerId);
  if (!el) throw new Error(`#${containerId} not found after render`);

  el.querySelectorAll('script').forEach((n) => n.remove());

  const h1s = el.querySelectorAll('h1');
  if (h1s.length > 1) {
    console.warn(`  ! ${h1s.length} <h1> in rendered output; demoting all but the first to <h2>`);
    [...h1s].slice(1).forEach((h) => {
      const h2 = dom.window.document.createElement('h2');
      for (const a of h.attributes) h2.setAttribute(a.name, a.value);
      h2.innerHTML = h.innerHTML;
      h.replaceWith(h2);
    });
  }

  const out = el.innerHTML.trim();
  dom.window.close();
  return out;
}

function inject(html, rendered, { containerId, emptyAnchor }) {
  if (html.includes(START)) {
    return html.replace(
      new RegExp(esc(START) + '[\\s\\S]*?' + esc(END)),
      `${START}\n${rendered}\n${END}`,
    );
  }
  if (!html.includes(emptyAnchor)) {
    throw new Error(
      `neither the ${START} marker nor the expected empty anchor ` +
        `\`${emptyAnchor}\` was found — page structure changed, update TARGETS`,
    );
  }
  return html.replace(
    emptyAnchor,
    `<div id="${containerId}">\n${START}\n${rendered}\n${END}\n</div>`,
  );
}

let changed = 0;
for (const target of TARGETS) {
  const file = path.join(root, target.file);
  const before = await readFile(file, 'utf8');
  const rendered = await renderContainer(before, target.url, target.containerId);
  const after = inject(before, rendered, target);

  const words = rendered.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().split(' ').filter(Boolean).length;
  if (after === before) {
    console.log(`  = ${target.file} (${words} words, unchanged)`);
  } else {
    await writeFile(file, after, 'utf8');
    changed++;
    console.log(`  ✓ ${target.file} (${words} words prerendered)`);
  }
}
console.log(`Prerender: ${TARGETS.length} target(s), ${changed} written.`);
