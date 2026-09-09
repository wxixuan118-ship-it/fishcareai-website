const fs=require('fs'),path=require('path'),{JSDOM}=require('jsdom');
const root=process.cwd(),D='https://www.fishcareai.com',B='/guides/telescope-goldfish-care/';
const data=JSON.parse(fs.readFileSync('data-pipeline/telescope-cluster.json'));const report=[];const titles=new Set(),descs=new Set();
for(const p of data.pages){
 const u=B+(p.slug?p.slug+'/':'');const doc=new JSDOM(fs.readFileSync(path.join(root,u,'index.html'),'utf8'),{url:D+u}).window.document;let errors=[];
 for(const sel of ['title','h1','meta[name="description"]','link[rel="canonical"]','meta[name="robots"]'])if(doc.querySelectorAll(sel).length!==1)errors.push('Wrong count '+sel);
 const title=doc.title,desc=doc.querySelector('meta[name="description"]').content;
 if(title.length>60||title.length<25)errors.push('Title length '+title.length);
 if(desc.length<120||desc.length>160)errors.push('Description length '+desc.length);
 if(titles.has(title)||descs.has(desc))errors.push('Duplicate title/description');titles.add(title);descs.add(desc);
 if(doc.querySelector('link[rel="canonical"]').href!==D+u)errors.push('Canonical mismatch');
 if(doc.querySelector('meta[name="robots"]').content.includes('noindex'))errors.push('Unexpected noindex');
 const schemas=[...doc.querySelectorAll('script[type="application/ld+json"]')].map(s=>JSON.parse(s.textContent));
 if(schemas.length!==3)errors.push('Schema count');
 const faq=schemas.find(s=>s['@type']==='FAQPage').mainEntity;
 const visible=[...doc.querySelectorAll('#faq details')];
 faq.forEach((f,i)=>{if(f.name!==visible[i].querySelector('summary').textContent||f.acceptedAnswer.text!==visible[i].querySelector('p').textContent)errors.push('FAQ mismatch')});
 const ids=[...doc.querySelectorAll('[id]')].map(n=>n.id);if(new Set(ids).size!==ids.length)errors.push('Duplicate ID');
 for(const a of doc.querySelectorAll('a[href],link[rel="stylesheet"]')){
 const resolved=new URL(a.href,D+u);if(resolved.origin!==D)continue;
 let file=path.join(root,decodeURIComponent(resolved.pathname));if(resolved.pathname.endsWith('/'))file=path.join(file,'index.html');
 if(!fs.existsSync(file)){errors.push('Missing local link '+resolved.pathname);continue;}
 if(resolved.hash){const target=resolved.pathname===u?doc:new JSDOM(fs.readFileSync(file,'utf8')).window.document;if(!target.getElementById(resolved.hash.slice(1)))errors.push('Missing fragment '+a.href);}
 }
 const sitemap=new JSDOM(fs.readFileSync('sitemaps/guides.xml','utf8'),{contentType:'text/xml'}).window.document;
 if([...sitemap.querySelectorAll('loc')].filter(n=>n.textContent===D+u).length!==1)errors.push('Sitemap entry count');
 for(const tag of ['og:title','og:description','og:url','og:image'])if(!doc.querySelector(`meta[property="${tag}"]`))errors.push('Missing '+tag);
 const article=doc.querySelector('article').textContent.trim().split(/\s+/).length;
 report.push({url:D+u,titleLength:title.length,descriptionLength:desc.length,articleWords:article,errors});
}
const result={checkedAt:'2026-09-09',scope:'14 newly created local HTML pages; checks do not certify deployment, indexing, rankings, live status or Core Web Vitals.',pages:report};fs.writeFileSync('reports/telescope-seo/audit.json',JSON.stringify(result,null,2));console.log(JSON.stringify(report.filter(p=>p.errors.length),null,2));console.log('Pages:',report.length,'Errors:',report.reduce((n,p)=>n+p.errors.length,0));if(report.some(p=>p.errors.length))process.exitCode=1;
