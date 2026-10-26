# On-page audit：20 个和竞品重叠的物种页

- 日期：2026-10-24
- 工具：`onpage-audit`（44 项检查，满分 100），审计线上 `https://www.fishcareai.com/species/<slug>`
- 主关键词 = 物种名；副关键词 = 竞品在该物种上的排名词（见 `competitor-aquariumstockingcalculator-species-keyword-gap-2026-10-24.md`）

## 分数

| 分数 | 页面 | 主词 | 关键词密度 | 正文字数 | 副关键词出现次数 |
|---|---|---|---|---|---|
| 83.8 | archer-fish | archer fish | 5.07% 🔴 | 434 | clouded archer fish：0 |
| 83.8 | badis | badis | 5.03% 🔴 | 537 | black tiger badis：0 |
| 84.6 | bolivian-ram | bolivian ram | 6.03% 🔴 | 464 | bolivian ram care sheet：0 |
| 84.6 | zebra-loach | zebra loach | 5.63% 🔴 | 462 | zebra loach tank mates：0 |
| 85.8 | fairy-cichlid | fairy cichlid | 6.45% 🔴 | 496 | tank size for fairy cichlid：0 |
| 86.2 | honey-gourami | honey gourami | 6.73% 🔴 | 505 | red honey gourami：0 |
| 86.9 | forktail-blue-eye | forktail blue eye | 6.61% 🔴 | 545 | blue eye rainbowfish：0 |
| 86.9 | molly | molly | 2.21% 🟢 | 587 | balloon molly：0 |
| 87.3 | blind-cave-tetra | blind cave tetra | 8.45% 🔴 | 497 | mexican tetra：1 |
| 87.3 | congo-tetra | congo tetra | 6.01% 🔴 | 499 | congo tetra care：0 |
| 87.3 | emerald-catfish | emerald catfish | 6.61% 🔴 | 454 | emerald cory catfish：0 |
| 87.3 | four-eyed-fish | four eyed fish | 8.17% 🔴 | 514 | anableps：12 |
| 87.3 | keyhole-cichlid | keyhole cichlid | 5.43% 🔴 | 479 | keyhole cichlids：1 |
| 87.3 | peacock-spiny-eel | peacock spiny eel | 8.97% 🔴 | 468 | peacock eel size：0 |
| 87.3 | three-spot-gourami | three spot gourami | 7.73% 🔴 | 466 | 3 spot gourami：0 |
| 88.5 | bristlenose-pleco | bristlenose pleco | 5.38% 🔴 | 520 | bristle nose pleco care：0 |
| 88.5 | upside-down-catfish | upside down catfish | 7.80% 🔴 | 500 | upside down catfish difficulty：0 |
| 90.0 | goldfish | goldfish | 2.25% 🟢 | 666 | lionhead goldfish：0 |
| 90.0 | pristella-tetra | pristella tetra | 4.40% 🔴 | 545 | glofish pristella：0 |
| 92.7 | betta-fish | betta fish | 4.53% 🔴 | 662 | female betta fish：0 |

分数集中在 84–93。所有页面都用同一个模板，所以分数接近，扣分项也几乎相同。改模板比逐页改更划算。

注：molly 用主词 "molly fish" 时只得 58.1，因为 title 是 "Molly Care Guide"，没有 "molly fish"。上表是用 "molly" 重跑的结果。

## 模板级问题（按影响排序）

### 1. "Species Related to X" 区块是空的（19/20 页）
H2 存在，但下面没有任何物种链接，只有 betta-fish 有 3 个。正文内链只有 4 个，都指向 hub 页（All Care Guides / Encyclopedia），没有同属或同类物种的互链。审计中的 "Internal links present" 有 19 页是 🟡。
→ 修复：用数据库里的同科、同属或同类数据把这个区块填上，每页 4–6 个相邻物种链接。这一项在 SEO 上收益最大，审计分数只反映了一部分。

### 2. 关键词密度 4.4%–9.0%（17/20 页 🔴，扣 4 分）
原因是模板结构：9 个 H2 都写成 "X Overview / X Scientific Classification / X Natural Habitat…"。物种名重复太多，正文又只有约 500 字，比例就被拉高了。
→ 修复：H2 改成 "Overview"、"Tank Size & Setup"、"Tank Mates" 这种不带物种名的写法，或只保留 1–2 个 H2 带物种名。不需要删正文。

### 3. 正文字数 434–545（18/20 页 🟡，扣 4 分）
只有 goldfish（666）和 betta-fish（662）超过 600 字。
→ 修复：新增 **"X Tank Size"** 和 **"X Tank Mates"** 两个 H2，大约能加 150–200 字，同时覆盖竞品的 "tank size for X" 和 "X compatible with Y" 两类词。

### 4. 话题集中度 41%–68%（16 页 🟡、4 页 🔴）
Classification、Interesting Facts、Related 这些 H2 会稀释大纲。"care" 这个词只出现在 title，没有出现在 H2 里。
→ 修复：同第 2 条。H2 改成以护理意图为主（Tank Size / Water Parameters / Diet / Tank Mates / Breeding），Classification 降成 Quick Facts 里的一行。

### 5. Meta description 太短（12/20 页低于 120 字符）
bolivian-ram（64）、honey-gourami（77）、fairy-cichlid（82）、emerald-catfish（84）、zebra-loach（87）最短。
→ 修复：统一用 "Complete X (*学名*) care guide — tank size, water parameters, diet, and compatibility…" 这个模板，bristlenose、goldfish、pristella 已经在用，长度约 140 字符。

### 6. Title 太短（7/20 页低于 25 字符）
molly（16）、badis（16）、goldfish（19）、archer-fish（22）、zebra-loach（22）、bolivian-ram（23）、fairy-cichlid（24）。
→ 修复：改成 "X Care Guide: Tank Size, Tank Mates & Diet" 这类格式，同时补上竞品的修饰词（care sheet / tank size）。

### 可以忽略的扣分项
- **"8 placeholder hrefs"**（20/20 🔴）：其实是目录里的 `#overview`、`#habitat` 这类页内锚点，不是死链，不用改。
- **响应时间 911–1243 ms**（20/20 🟡）：反代 + Next.js 冷启动导致，`proxy_cache` 命中后会更快。
- **图片没有 lazy-load / webp**、**没有外链**：各扣 0.5 分，优先级低。

## 数据准确性问题（审计工具不检查，但影响 "tank size" 类关键词）

Quick Facts 里的数据有明显错误。如果按上面的建议新增 "Tank Size" H2，这些数字会直接出现在正文和摘要里，必须先修：

| 页面 | 现在的值 | 问题 |
|---|---|---|
| bolivian-ram | 最小鱼缸 20 L（5 gal） | 太小，常见建议 ≥30 gal |
| congo-tetra | 20 L（5 gal） | 太小，群游鱼，常见建议 ≥30 gal |
| honey-gourami | 20 L（5 gal） | 偏小，常见建议 ≥10 gal |
| archer-fish | 26 gal，Care level：Beginner | 鱼缸太小（常见建议 ≥55 gal，半咸水），难度应为中级或以上 |
| four-eyed-fish | 20 gal，Beginner | 半咸水大型鱼缸，难度应为高级 |
| emerald-catfish | 13 gal | 群居底栖鱼，常见建议 ≥20 gal |
| 多个页面 | 体长 "5-6"、寿命 "5"，没有单位 | 缺 cm/年；很多页面寿命都是 "5"，像是默认填充值 |
| 18/20 页 | Care level 全是 Beginner | 可疑，可能是默认值 |

## 建议顺序

1. 修 Quick Facts 数据（鱼缸大小、单位、难度），先修上表这几页，再排查全部 258 页的默认值。
2. 模板：填充 Related Species 区块。
3. 模板：H2 改为护理意图结构，新增 Tank Size / Tank Mates 两段（同时解决密度、字数、集中度三项扣分）。
4. 逐页：补 title 和 description，加入竞品修饰词和别名（mexican tetra、emerald cory、3 spot gourami、peacock eel 等）。
5. 改完后用同一组关键词重跑审计，对比分数变化。

物种页由 anysites 上的 Next.js 应用从数据库渲染，第 1–4 步都要在那边或数据库里改，不在本仓库。

---

## 修复结果（2026-10-25）

20 个页面全部按 writer skill 流程重写，改为静态覆盖页：内容在 `data-pipeline/species_deep/<slug>.json`，由 `python3 data-pipeline/species_deep.py render` 生成 `species/<slug>/index.html` 和 `assets/species-deep/<slug>-care-chart.svg`，并重新生成 `nginx.conf` 里的 `# BEGIN/END species deep pages` 区块。机制与 fish-health deep test 相同：nginx 的精确匹配优先于反代到 species app。数据库没有改动。

| 页面 | 修复前 | 修复后（本地） | 关键词密度 | 正文字数 |
|---|---|---|---|---|
| bolivian-ram | 84.6 | 98.4 | 2.40% | 2003 |
| fairy-cichlid | 85.8 | 98.4 | 2.32% | 1896 |
| keyhole-cichlid | 87.3 | 98.4 | 2.57% | 1559 |
| three-spot-gourami | 87.3 | 98.4 | 2.60% | 1499 |
| upside-down-catfish | 88.5 | 98.4 | 2.90% | 1446 |
| zebra-loach | 84.6 | 98.4 | 1.45% | 1383 |
| bristlenose-pleco | 88.5 | 98.4 | 2.58% | 1318 |
| pristella-tetra | 90.0 | 98.4 | 2.86% | 1328 |
| emerald-catfish | 87.3 | 98.4 | 2.23% | 1343 |
| blind-cave-tetra | 87.3 | 98.4 | 2.65% | 1469 |
| honey-gourami | 86.2 | 98.4 | 2.46% | 1384 |
| goldfish | 90.0 | 98.4 | 2.72% | 1470 |
| archer-fish | 83.8 | 98.4 | 2.52% | 1507 |
| peacock-spiny-eel | 87.3 | 98.4 | 2.33% | 1285 |
| molly | 86.9 | 98.4 | 2.80% | 1357 |
| betta-fish | 92.7 | 98.4 | 2.14% | 1497 |
| badis | 83.8 | 98.4 | 2.51% | 1434 |
| forktail-blue-eye | 86.9 | 98.4 | 2.68% | 1345 |
| congo-tetra | 87.3 | 98.4 | 2.54% | 1262 |
| four-eyed-fish | 87.3 | 98.4 | 2.94% | 1532 |

本地审计没有响应时间和 robots.txt 两项（不计分）；上线后要重跑线上审计。剩下的 2 分扣在话题集中度（各页 55–67%，🟡），属于"关键词 + 自然语言 H2"的取舍，没有为了刷分去堆关键词。

**每页包含：** 真实照片（头图和正文各一张）、按页面数据生成的护理图表 SVG、3–6 条参考文献（FishBase、Seriously Fish、同行评审论文的 DOI 都已核对）、FAQ + Article + BreadcrumbList 结构化数据、Related Species 内链（全部链接都校验过存在）。

**重复度：** 正文 8 词 shingle，与其他 19 页的重合最高 1.26%（目标 <5%）。与已有的 goldfish、betta、molly、bristlenose 护理指南重合均为 0%。

**首页入口：** `index.html` 新增 `#species-profiles` 区块，20 张卡片链接到这些页面。首页的静态 HTML 和 SPA 模板字符串两处都加了。

**修正的数据错误：** archer fish 原来是 26 gal、Beginner，改为约 114 gal、半咸水；four-eyed fish 原来是 20 gal、Beginner，改为 60 × 18 in 浅缸；Congo tetra 和 Bolivian ram 原来是 5 gal，改为 48 in 和 36 × 18 in；其余页面都按来源补上了单位和范围。

### 未完成 / 需要跟进
- **图片清晰度：** goldfish（250 px）、bristlenose-pleco（330 px）两张照片太小，放大后会模糊；betta 已换成 900 px 的图。需要从 Wikimedia Commons 下载 CC 授权的大图替换。
- **重复物种页：** `/species/x-ray-tetra` 和 `/species/pristella-tetra` 是同一个物种；`/species/forktail-rainbowfish` 很可能和 `/species/forktail-blue-eye` 是同一个物种。建议合并并做 301。
- **数据库：** 其余 238 个物种页的 Quick Facts 仍可能有同类错误（默认 Beginner、缺单位），本次没有改数据库。
- **上线：** 需要部署本仓库（nginx 镜像）后，在线上重跑审计确认分数。
