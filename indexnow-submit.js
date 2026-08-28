#!/usr/bin/env node
/**
 * Submit FishCare AI URLs to IndexNow.
 *
 * Modes:
 *   node indexnow-submit.js https://www.fishcareai.com/guides/angelfish-care/   # explicit URL(s)
 *   node indexnow-submit.js --changed                                           # changed/new index.html pages (git)
 *   node indexnow-submit.js --sitemap                                           # every URL in the live sitemap index
 *   node indexnow-submit.js --sitemap https://www.fishcareai.com/sitemap.xml    # custom sitemap / sitemap index
 *
 * Flags:
 *   --dry-run   print what would be sent, submit nothing
 *
 * The key file must remain at the site root in production:
 *   https://www.fishcareai.com/indexnow-7b4f8d2c9a6e41f0b3c5d7e9a1f6b8c4.txt
 */
const https = require('https');
const { execFileSync } = require('child_process');
const host = 'www.fishcareai.com';
const key = '7b4f8d2c9a6e41f0b3c5d7e9a1f6b8c4';
const keyLocation = `https://${host}/indexnow-${key}.txt`;
const BATCH_SIZE = 10000; // IndexNow accepts at most 10,000 URLs per request
const DEFAULT_SITEMAP = `https://${host}/sitemap.xml`;

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const rest = args.filter(arg => arg !== '--dry-run');

function changedPageUrls() {
  let tracked = '';
  let untracked = '';
  try {
    tracked = execFileSync('git', ['diff', '--name-only', '--diff-filter=ACMRT', 'HEAD'], { encoding: 'utf8' });
    untracked = execFileSync('git', ['ls-files', '--others', '--exclude-standard'], { encoding: 'utf8' });
  } catch (error) {
    console.error(`Unable to read changed files: ${error.message}`);
    process.exit(1);
  }

  return [...new Set(`${tracked}\n${untracked}`.split(/\r?\n/))]
    .filter(file => file === 'index.html' || file.endsWith('/index.html'))
    .filter(file => !file.startsWith('admin/') && file !== 'thank-you/index.html')
    .map(file => file === 'index.html' ? `https://${host}/` : `https://${host}/${file.replace(/index\.html$/, '')}`);
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'FishCareAI-IndexNow/1.0' } }, response => {
      const { statusCode, headers } = response;
      if (statusCode >= 300 && statusCode < 400 && headers.location) {
        response.resume();
        resolve(fetchText(new URL(headers.location, url).toString()));
        return;
      }
      if (statusCode !== 200) {
        response.resume();
        reject(new Error(`${statusCode} for ${url}`));
        return;
      }
      let body = '';
      response.setEncoding('utf8');
      response.on('data', chunk => { body += chunk; });
      response.on('end', () => resolve(body));
    }).on('error', reject);
  });
}

const locPattern = /<(?:\w+:)?loc>\s*([^<\s]+)\s*<\/(?:\w+:)?loc>/gi;

function extractLocs(xml) {
  const found = [];
  let match;
  while ((match = locPattern.exec(xml)) !== null) {
    found.push(match[1].replace(/&amp;/g, '&').trim());
  }
  return found;
}

async function collectSitemapUrls(rootUrl) {
  const seenSitemaps = new Set();
  const pageUrls = new Set();
  const queue = [rootUrl];

  while (queue.length) {
    const current = queue.shift();
    if (seenSitemaps.has(current)) continue;
    seenSitemaps.add(current);

    let xml;
    try {
      xml = await fetchText(current);
    } catch (error) {
      console.error(`  ! skipped ${current}: ${error.message}`);
      continue;
    }

    const isIndex = /<sitemapindex[\s>]/i.test(xml);
    const locs = extractLocs(xml);
    if (isIndex) {
      console.error(`  + index ${current} -> ${locs.length} sitemaps`);
      for (const loc of locs) queue.push(loc);
    } else {
      let kept = 0;
      for (const loc of locs) {
        if (loc.startsWith(`https://${host}/`)) { pageUrls.add(loc); kept++; }
      }
      console.error(`  + sitemap ${current} -> ${kept} urls`);
    }
  }

  return [...pageUrls];
}

function submit(urls) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ host, key, keyLocation, urlList: urls });
    const request = https.request({
      hostname: 'api.indexnow.org',
      path: '/IndexNow',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, response => {
      let body = '';
      response.on('data', chunk => { body += chunk; });
      response.on('end', () => resolve({ status: response.statusCode, body: body || null }));
    });
    request.on('error', reject);
    request.write(payload);
    request.end();
  });
}

function chunk(list, size) {
  const out = [];
  for (let i = 0; i < list.length; i += size) out.push(list.slice(i, i + size));
  return out;
}

async function main() {
  let urls;

  if (rest[0] === '--sitemap') {
    const root = rest[1] || DEFAULT_SITEMAP;
    console.error(`Walking ${root} ...`);
    urls = await collectSitemapUrls(root);
  } else if (rest.length === 1 && rest[0] === '--changed') {
    urls = changedPageUrls();
  } else {
    urls = rest;
  }

  urls = [...new Set(urls)];

  if (!urls.length) {
    console.error('No URLs to submit. Provide absolute URLs, --changed, or --sitemap.');
    process.exit(1);
  }

  const bad = urls.find(url => !url.startsWith(`https://${host}/`));
  if (bad) {
    console.error(`URLs must use https://${host}/ (got ${bad})`);
    process.exit(1);
  }

  const batches = chunk(urls, BATCH_SIZE);

  if (dryRun) {
    console.log(JSON.stringify({ dryRun: true, urlCount: urls.length, batches: batches.length, sample: urls.slice(0, 20) }, null, 2));
    return;
  }

  let failed = false;
  for (let i = 0; i < batches.length; i++) {
    const { status, body } = await submit(batches[i]);
    const ok = status >= 200 && status < 300;
    if (!ok) failed = true;
    console.log(JSON.stringify({
      submittedAt: new Date().toISOString(),
      batch: `${i + 1}/${batches.length}`,
      status,
      urlCount: batches[i].length,
      response: body
    }, null, 2));
  }

  console.log(JSON.stringify({ done: true, totalUrls: urls.length, batches: batches.length }, null, 2));
  process.exit(failed ? 1 : 0);
}

main().catch(error => {
  console.error(`IndexNow submission failed: ${error.message}`);
  process.exit(1);
});
