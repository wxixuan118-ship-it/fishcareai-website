"""Generate telescope pages, preserving unrelated local edits. No deployment."""
from pathlib import Path
import json,html,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
D='https://www.fishcareai.com'; B='/guides/telescope-goldfish-care/'; DATE='2026-09-09'; e=html.escape
pages=json.loads((R/'data-pipeline/telescope-cluster.json').read_text())['pages']
def url(p):return B+(p['slug']+'/' if p['slug'] else '')
sources={
 'pfk':('Practical Fishkeeping: telescope-eye housing and care','https://www.practicalfishkeeping.co.uk/fishkeeping-answers/how-do-i-keep-telescope-eye-goldfish/'),
 'rspca':('RSPCA Australia: goldfish welfare and care','https://kb.rspca.org.au/categories/companion-animals/fish/how-should-i-care-for-my-goldfish'),
 'aqueon':('Aqueon: goldfish varieties, feeding and spawning','https://www.aqueon.com/resources/care-guides/goldfish'),
 'merck':('Merck Veterinary Manual: disorders and diseases of fish','https://www.merckvetmanual.com/all-other-pets/fish/disorders-and-diseases-of-fish'),
 'petmd':('PetMD: swim bladder disease, by Jessie Sanders, DVM','https://www.petmd.com/fish/conditions/respiratory/swim-bladder-disorders-fish')}
source_map={'':['pfk','rspca'],'tank-size':['pfk','rspca'],'water-parameters':['aqueon','rspca'],'feeding':['rspca','aqueon'],'lifespan':['rspca','aqueon'],'size-growth':['pfk'],'types':['aqueon','pfk'],'breeding':['aqueon'],'eye-problems':['merck','pfk'],'diseases':['merck'],'not-eating':['merck','rspca'],'swim-bladder':['petmd','merck'],'color-change':['aqueon','merck'],'tank-mates':['pfk','aqueon']}
nav=''.join(f'<a href="{url(p)}">{e(p["title"])}</a>' for p in pages)
for p in pages:
 u=url(p);title=p['title'];desc=p['desc'];faq=p['faq']
 crumbs=[('Home','/'),('Care guides','/guides/')]+([('Telescope goldfish care',B)] if p['slug'] else [])+[(title,u)]
 schema=[{'@context':'https://schema.org','@type':'Article','headline':title,'description':desc,'dateModified':DATE,'author':{'@type':'Organization','name':'FishCare AI Editorial Team','url':D+'/editorial-policy/'},'publisher':{'@type':'Organization','name':'FishCare AI','url':D},'mainEntityOfPage':D+u}, {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':D+l} for i,(n,l) in enumerate(crumbs)]},{'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}]
 sections=''.join(f'<section id="{sid}"><h2>{e(h)}</h2>{content}</section>' for sid,h,content in p['sections'])
 toc=''.join(f'<a href="#{sid}">{e(h)}</a>' for sid,h,_ in p['sections'])
 refs=''.join(f'<li><a href="{sources[k][1]}">{e(sources[k][0])}</a></li>' for k in source_map[p['slug']])
 crumb_html=' / '.join(f'<a href="{l}">{e(n)}</a>' if i<len(crumbs)-1 else f'<span aria-current="page">{e(n)}</span>' for i,(n,l) in enumerate(crumbs))
 doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{D+u}"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/goldfish-cluster.css">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{D+u}"><meta property="og:image" content="{D}/assets/encyclopedia/real/goldfish-wikimedia-real.jpg"><meta property="og:image:alt" content="Goldfish photograph representing the FishCare AI goldfish care library"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{D}/assets/encyclopedia/real/goldfish-wikimedia-real.jpg">
{''.join('<script type="application/ld+json">'+json.dumps(s)+'</script>' for s in schema)}
<style>.hero-inner{{grid-template-columns:1fr;max-width:1180px}}.hero-inner>div{{max-width:900px}}.breadcrumb{{font-size:13px}}.cluster{{display:block}}@media(max-width:760px){{aside{{order:initial}}.cluster{{display:block}}}}</style>
</head><body><a class="skip" href="#main">Skip to content</a><nav class="nav" aria-label="Main"><a class="brand" href="/">FishCare AI</a><a href="/guides/">Care guides</a><a href="/tools/">Aquarium tools</a><a href="/guides/goldfish-care/">Goldfish care</a></nav>
<header class="hero"><div class="hero-inner"><div><nav class="breadcrumb" aria-label="Breadcrumb">{crumb_html}</nav><p class="eyebrow">Telescope goldfish care library</p><h1>{e(title)}</h1><p>{e(desc)}</p></div></div></header>
<main id="main" class="layout"><article><p class="meta"><a href="/editorial-policy/">FishCare AI Editorial Team</a> · Content prepared <time datetime="{DATE}">September 9, 2026</time></p>{sections}<section id="faq"><h2>Frequently asked questions</h2>{''.join(f'<details open><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in faq)}</section><section id="sources"><h2>Sources and editorial notes</h2><ul>{refs}</ul><p class="meta">These references support general husbandry and health guidance. Telescope-specific evidence is limited for some outcomes. Planning allowances and cautious pairing assessments are editorial guidance, not guarantees for individual fish. See our <a href="/editorial-policy/">editorial policy</a>.</p></section><section id="related"><h2>Related care guides and tools</h2><div class="grid"><a href="{B}">Telescope goldfish care overview</a><a href="/wiki/black-moor-goldfish/">Black Moor goldfish profile</a><a href="/guides/goldfish-care/">General goldfish care</a><a href="/calculators/goldfish-tank-size/">Goldfish tank size calculator</a></div></section></article><aside><nav class="card toc" aria-label="On this page"><h2>On this page</h2>{toc}<a href="#faq">Frequently asked questions</a><a href="#sources">Sources and editorial notes</a></nav><nav class="card toc cluster" aria-label="Telescope care topics"><h2>Explore telescope care</h2>{nav}</nav></aside></main><footer>FishCare AI · <a href="/about/">About</a> · <a href="/editorial-policy/">Editorial policy</a> · <a href="/privacy/">Privacy</a></footer></body></html>'''
 dest=R/u.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(doc)
# Add narrow, idempotent discovery links to existing pages; do not replace content.
for f in ['guides/index.html','guides/goldfish-care/index.html','wiki/black-moor-goldfish/index.html']:
 dest=R/f;t=dest.read_text();t=re.sub(r'<!--telescope-cluster:start-->.*?<!--telescope-cluster:end-->','',t,flags=re.S)
 block=f'<!--telescope-cluster:start--><section id="telescope-care-library" style="max-width:1100px;margin:28px auto;padding:24px"><h2>Telescope goldfish care library</h2><p>Care for protruding eyes, feeding access and calm companions: <a href="{B}">telescope goldfish care guide</a>, <a href="{B}eye-problems/">eye injuries and cloudiness</a>, and <a href="{B}tank-mates/">telescope tank mates</a>.</p></section><!--telescope-cluster:end-->'
 anchor=next(a for a in ['</article>','</main>','</body>'] if a in t);dest.write_text(t.replace(anchor,block+anchor,1))
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
f=R/'sitemaps/guides.xml';root=ET.fromstring(f.read_text());known={x.find('{'+ns+'}loc').text for x in root}
for p in pages:
 if D+url(p) not in known:
  el=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(el,'{'+ns+'}loc').text=D+url(p);ET.SubElement(el,'{'+ns+'}lastmod').text=DATE
ET.indent(root);f.write_text(ET.tostring(root,encoding='unicode',xml_declaration=True))
rows=[{'keyword':k,'status':'新建（本地完成，未部署）','url':D+url(p),'path':url(p),'topic':p['title']} for p in pages for k in p['keywords']]
rows += [{'keyword':k,'status':'已有本地页面（线上状态未确认）','url':D+'/wiki/black-moor-goldfish/','path':'/wiki/black-moor-goldfish/','topic':'Black Moor Goldfish'} for k in ['black telescope goldfish','black telescope fish','black moor telescope goldfish']]
report=R/'reports/telescope-seo';report.mkdir(parents=True,exist_ok=True)
(report/'coverage.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
md='# Telescope goldfish 关键词与 URL 对照\n\n79 个关键词：76 个归并为 14 个新页面；3 个复用 Black Moor 本地已有页面。\n\n新页面仅在源码中创建，未部署；下表网址为部署后的目标地址，不表示现在已上线。Black Moor URL 的线上状态尚未确认，公开 URL 请求返回 HTTP 403，无法确认实际页面状态。已通过搜索核实的相关线上页面：[Goldfish care](https://www.fishcareai.com/guides/goldfish-care/) 和 [Goldfish tank calculator](https://www.fishcareai.com/calculators/goldfish-tank-size/)。\n\n|关键词|状态|URL|\n|---|---|---|\n'+''.join(f'|{r["keyword"]}|{r["status"]}|[{r["url"]}]({r["url"]})|\n' for r in rows)
(report/'URL-MAPPING.md').write_text(md)
trs=''.join(f'<tr><td>{e(r["keyword"])}</td><td>{e(r["status"])}</td><td><a href="{r["path"]}">{e(r["url"])}</a></td></tr>' for r in rows)
(report/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Telescope goldfish 关键词与页面审计</title><link rel="stylesheet" href="/assets/goldfish-cluster.css"></head><body><main style="max-width:1280px;margin:30px auto;padding:24px"><h1>Telescope goldfish：79 个关键词与 URL</h1><p>14 个新专题页面覆盖 76 个关键词；3 个关键词复用 Black Moor 本地页面。新页面未部署；线上状态未核验的已有 URL 已标记。表格链接打开当前环境中的页面预览。</p><p><a href="audit.json">自动化 on-page 检查结果</a> · <a href="URL-MAPPING.md">完整 URL 对照表</a></p><div class="table-wrap"><table><thead><tr><th>关键词</th><th>状态</th><th>URL / 本地预览</th></tr></thead><tbody>{trs}</tbody></table></div></main></body></html>')
print(f'Generated {len(pages)} pages; mapped {len(rows)} keywords.')
