const fs=require('fs'),path=require('path');const {JSDOM}=require(process.cwd()+'/node_modules/jsdom');const root=process.cwd(),D='https://www.fishcareai.com', img=D+'/assets/encyclopedia/real/goldfish-wikimedia-real.jpg';const rows=JSON.parse(fs.readFileSync('reports/goldfish-seo/coverage.json'));let results=[];
for(const url of [...new Set(rows.map(r=>r.url))]){
 const file=path.join(root,url,'index.html');if(!fs.existsSync(file)){results.push({url,errors:['Missing file']});continue}let raw=fs.readFileSync(file,'utf8'),dom=new JSDOM(raw),doc=dom.window.document;
 const errors=[],warnings=[];for(const [sel,count] of [['h1',1],['title',1],['meta[name="description"]',1],['link[rel="canonical"]',1],['meta[name="robots"]',1]])if(doc.querySelectorAll(sel).length!==count)errors.push(sel+' count');
 const canonical=doc.querySelector('link[rel="canonical"]')?.href;if(canonical!==D+url)errors.push('canonical mismatch '+canonical);
 const desc=doc.querySelector('meta[name="description"]')?.content||'';if(doc.title.length>65||doc.title.length<20)warnings.push('title length '+doc.title.length);if(desc.length<100||desc.length>170)warnings.push('description length '+desc.length);
 for(const s of doc.querySelectorAll('script[type="application/ld+json"]'))try{JSON.parse(s.textContent)}catch{errors.push('Invalid JSON-LD')}
 const ids=[...doc.querySelectorAll('[id]')].map(n=>n.id);if(new Set(ids).size!==ids.length)errors.push('Duplicate IDs');
 for(const a of doc.querySelectorAll('a[href^="#"]'))if(a.hash.length>1&&!doc.getElementById(a.hash.slice(1)))warnings.push('Broken fragment '+a.hash);
 for(const a of doc.querySelectorAll('a[href^="/"]')){const h=a.getAttribute('href').split(/[?#]/)[0];if(!fs.existsSync(path.join(root,h))&&!h.startsWith('/species')&&!h.startsWith('/fish-health'))warnings.push('Missing local link '+h)}
 for(const im of doc.querySelectorAll('img'))if(!im.hasAttribute('alt'))errors.push('Image missing alt');
 results.push({url,title:doc.title,descriptionLength:desc.length,errors,warnings:[...new Set(warnings)]});dom.window.close();
}
fs.writeFileSync('reports/goldfish-seo/audit.json',JSON.stringify({checkedAt:'2026-09-09',scope:'Local on-page HTML checks; not a ranking, live redirect or Core Web Vitals certification',pages:results},null,2));console.log(JSON.stringify(results.filter(x=>x.errors.length||x.warnings.length),null,2));console.log('Pages checked:',results.length,'Errors:',results.reduce((s,r)=>s+r.errors.length,0));
