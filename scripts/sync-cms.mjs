import {readFile,writeFile,mkdir} from 'node:fs/promises';
import path from 'node:path';

const root=process.cwd();
const url=(process.env.SUPABASE_URL||'').replace(/\/$/,'');
const key=(process.env.SUPABASE_SECRET_KEY||process.env.SUPABASE_SERVICE_ROLE_KEY||'').trim();
const dryRun=process.env.CMS_DRY_RUN==='1';
if(!url||!key){console.log('CMS sync skipped: Supabase build variables are not configured.');process.exit(0)}

const response=await fetch(`${url}/rest/v1/cms_pages?site_id=eq.fishcareai&status=eq.published&select=*`,{headers:{apikey:key,Authorization:`Bearer ${key}`}});
if(!response.ok)throw new Error(`CMS fetch failed (${response.status}): ${await response.text()}`);
const pages=await response.json();
const encode=value=>String(value||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const safeBody=html=>String(html||'').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'').replace(/<iframe\b[^>]*>[\s\S]*?<\/iframe>/gi,'').replace(/\son[a-z]+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)/gi,'').replace(/<h1(\b[^>]*)>/gi,'<h2$1>').replace(/<\/h1>/gi,'</h2>');

function fallback(page){return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${encode(page.title)}</title><meta name="description" content="${encode(page.description)}"><link rel="canonical" href="${encode(page.canonical)}"><link rel="stylesheet" href="/assets/fishcare-glass-redesign.css"></head><body><header class="site-header"><a href="/">FishCare AI</a></header><main><section class="guide-hero"><h1>${encode(page.h1)}</h1></section><article class="con guide-content">${safeBody(page.body_html)}</article></main></body></html>`}
function patch(html,page){
  html=html.replace(/<title[^>]*>[\s\S]*?<\/title>/i,`<title>${encode(page.title)}</title>`);
  if(/<meta[^>]+name=["']description["'][^>]*>/i.test(html))html=html.replace(/<meta[^>]+name=["']description["'][^>]*>/i,`<meta name="description" content="${encode(page.description)}">`);else html=html.replace('</head>',`<meta name="description" content="${encode(page.description)}">\n</head>`);
  if(/<link[^>]+rel=["']canonical["'][^>]*>/i.test(html))html=html.replace(/<link[^>]+rel=["']canonical["'][^>]*>/i,`<link rel="canonical" href="${encode(page.canonical)}">`);else html=html.replace('</head>',`<link rel="canonical" href="${encode(page.canonical)}">\n</head>`);
  if(/<h1\b/i.test(html))html=html.replace(/<h1([^>]*)>[\s\S]*?<\/h1>/i,`<h1$1>${encode(page.h1)}</h1>`);
  const body=safeBody(page.body_html);if(/<article\b/i.test(html))html=html.replace(/(<article\b[^>]*>)[\s\S]*?(<\/article>)/i,`$1\n${body}\n$2`);else html=html.replace(/(<main\b[^>]*>)[\s\S]*?(<\/main>)/i,`$1\n<h1>${encode(page.h1)}</h1>\n${body}\n$2`);
  const schemas=(Array.isArray(page.schema_json)?page.schema_json:[]).map(item=>`<script type="application/ld+json">${JSON.stringify(item)}</script>`).join('\n');html=html.replace(/<script[^>]+type=["']application\/ld\+json["'][^>]*>[\s\S]*?<\/script>\s*/gi,'');return html.replace('</head>',`${schemas}\n</head>`)
}

let updated=0,created=0;
for(const page of pages){const file=path.join(root,'guides',page.slug,'index.html');let html;try{html=await readFile(file,'utf8');updated++}catch{html=fallback(page);created++}if(/data-cms-sync=["']off["']/i.test(html)){console.log(`CMS sync skipped for protected page: ${page.slug}`);continue}const output=patch(html,page);if(!dryRun){await mkdir(path.dirname(file),{recursive:true});await writeFile(file,output,'utf8')}}
console.log(`CMS sync: ${pages.length} published pages (${updated} updated, ${created} created)${dryRun?' [dry run]':''}.`);
