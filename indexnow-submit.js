#!/usr/bin/env node
/**
 * Submit changed FishCare AI URLs to IndexNow.
 * Usage: node indexnow-submit.js https://www.fishcareai.com/guides/angelfish-care/
 * The key file must remain at the site root in production.
 */
const https = require('https');
const host = 'www.fishcareai.com';
const key = '7b4f8d2c9a6e41f0b3c5d7e9a1f6b8c4';
const urls = process.argv.slice(2);

if (!urls.length) {
  console.error('Provide at least one absolute URL.');
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
    console.log(`IndexNow response: ${response.statusCode}${body ? ` ${body}` : ''}`);
    process.exit(response.statusCode >= 200 && response.statusCode < 300 ? 0 : 1);
  });
});

request.on('error', error => {
  console.error(`IndexNow submission failed: ${error.message}`);
  process.exit(1);
});
request.write(payload);
request.end();
