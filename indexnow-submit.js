#!/usr/bin/env node
/**
 * Submit changed FishCare AI URLs to IndexNow.
 * Usage: node indexnow-submit.js https://www.fishcareai.com/guides/angelfish-care/
 * The key file must remain at the site root in production.
 */
const https = require('https');
const { execFileSync } = require('child_process');
const host = 'www.fishcareai.com';
const key = '7b4f8d2c9a6e41f0b3c5d7e9a1f6b8c4';
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const urlArgs = args.filter(arg => arg !== '--dry-run');

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
    .map(file => file === 'index.html' ? `https://${host}/` : `https://${host}/${file.replace(/index\.html$/, '')}`);
}

const urls = urlArgs.length === 1 && urlArgs[0] === '--changed' ? changedPageUrls() : urlArgs;

if (!urls.length) {
  console.error('Provide at least one absolute URL, or use --changed after editing HTML pages.');
  process.exit(1);
}

if (urls.some(url => !url.startsWith(`https://${host}/`))) {
  console.error(`URLs must use https://${host}/`);
  process.exit(1);
}

const payload = JSON.stringify({
  host,
  key,
  keyLocation: `https://${host}/indexnow-7b4f8d2c9a6e41f0b3c5d7e9a1f6b8c4.txt`,
  urlList: urls
});

if (dryRun) {
  console.log(JSON.stringify({ dryRun: true, urlCount: urls.length, urls }, null, 2));
  process.exit(0);
}

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
  response.on('end', () => {
    console.log(JSON.stringify({
      submittedAt: new Date().toISOString(),
      status: response.statusCode,
      urlCount: urls.length,
      urls,
      response: body || null
    }, null, 2));
    process.exit(response.statusCode >= 200 && response.statusCode < 300 ? 0 : 1);
  });
});

request.on('error', error => {
  console.error(`IndexNow submission failed: ${error.message}`);
  process.exit(1);
});
request.write(payload);
request.end();
