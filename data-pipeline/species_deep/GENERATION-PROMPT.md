# 新物种百科页生成提示词（按哥飞方法）

> 用法：把下面「提示词正文」整段交给执行的 agent，并在 `{{SPECIES_LIST}}` 处填入本批物种（每批 ≤10 个）。
> 输出落在 `data-pipeline/species_deep/<slug>.json`，用 `python3 data-pipeline/species_deep.py check|dupes|render` 校验和渲染。

---

## 提示词正文

你要为 fishcareai.com 的鱼类百科（`/species/<slug>`）新建一批物种页。这个站是新站：域名不到 6 个月，外链域名不到 100 个。哥飞的结论是"新站批量上页面必死"，所以这批页面要**每页手工精做，分批上线，看过数据再放量**，不能用模板一次性铺开。

### 本批物种
{{SPECIES_LIST}}

总名单在 `reports/species-gap-aquariumstockingcalculator-2026-10-25.csv`。来源是竞品 aquariumstockingcalculator.com 近 28 天有流量的 68 个物种页，扣掉我们已有的 8 个后，剩下 60 个：
- `type=new`：48 个，我们完全没有的物种，从这里挑出本批要做的。`batch 1 candidate` 是第一批的建议，都是大众鱼种，站内也有可以互链的页面，比如 iridescent shark ↔ bala shark、flying fox ↔ siamese/chinese algae eater。
- `type=variant`：12 个，是已有物种的品种或别称，比如 balloon molly → molly、lionhead goldfish → goldfish。**默认不单独建页**，在 `covered_by` 对应的已有页面里加一个 H2 小节，并把变种名放进 title 或 description，避免两个页面抢同一个词。只有第 0 步查出这个变种词自己的月搜量明显高、而且 SERP 前 10 名里有专门写这个变种的页面时，才单独建页。

### 第 0 步：先验证需求，不满足的直接剔除
每个物种在写之前都要过三关，并把结果记在 `reports/species-new-batch-<日期>.csv`（slug, keyword, 月搜, allintitle 数, KGR, SERP 判断, 结论）：

1. **确定主关键词**。一个关键词对应一个页面。主词用美国用户真实搜索的叫法（例如 "cherry shrimp"，不是学名），记下 Google 关键词规划师的美国月搜量。
2. **算 KGR**。KGR = allintitle 结果数 ÷ 月搜量。小于 0.25 优先做；0.25–1 可以做；大于 1 只有在 SERP 很弱时才做。
3. **看 SERP 前 10 名**。你不需要和全世界竞争，只需要和这个词前几十个结果竞争。记下前 10 名分别是谁，有几个页面是专门为这个词做的，最弱的那个页面靠什么上榜（字数、结构、有没有数据和出处）。
   - 搜索意图是"买"（for sale）或者"看图"，信息型百科页接不住，剔除。
   - 前 10 名全是 DR 70 以上、并且专门为这个词做的页面，剔除或往后排。

先把这一批里能做的物种挑出来，**排序后只写前几个**，不要为了凑数硬写。

### 第 1 步：先查重，不要和现有页面抢同一个词
- 搜一遍站内：`/species/`、`/guides/`、`/compatibility/<slug>/`、`/fish-health/fish/<slug>`、`/calculators/`。如果已经有页面在做同一个主词（比如 `/guides/` 里已有这个物种的养护长文），新页面只做"物种档案"（体型、分布、参数、混养概要），不要再写一篇养护长文，主词换成档案型叫法，避免关键词互相蚕食。
- 现有 URL 一律不改（哥飞改版第一原则）。slug 用全小写加连字符，和 compatibility、fish-health 里已经用的 slug 保持一致（例如 `cherry-shrimp`、`pea-puffer`），这样已有的链接就能直接接上。

### 第 2 步：调研，每个数字都要有出处
- 物种数据以 FishBase、Seriously Fish 为主，再用 1–2 个可信来源交叉核对（大学或研究机构、PlanetCatfish、Shrimp/Snail 专门站点等）。至少 4 条参考文献，写进 `references`，正文用 `[n]` 标注。
- 来源之间有冲突时，写出范围并注明谁给的数，不要自己编一个平均值。
- 先写出这个物种**最特别的那一点**。用户之所以专门搜这个物种，往往就是因为这一点，比如 pea puffer 只吃活食、ghost shrimp 常被当作饲料虾卖、turtles 根本不是鱼。不要套用"五个通用要点"那种模板。
- 图片只用许可证明确的图（Wikimedia Commons 等），放到 `assets/encyclopedia/real/<slug>-*.jpg`，在 caption 里写清楚授权方式。

### 第 3 步：写内容，按现有 JSON 结构
照着 `data-pipeline/species_deep/archer-fish.json` 的字段来写：`slug, keyword, common_name, scientific, title, description, h1, tag, photo, chart, facts, short_answer, intro, sections, faq, related, editorial_note, references`。

On-page 规则（哥飞的 TDK 和 H 标签规则，再加上我们自己审计踩过的坑）：
- **title**：主词放最前面，后面跟这个物种最常被搜的两个属性，例如 "Pea Puffer Care, Tank Size and Live Food Diet"。25–60 个字符（`check` 会校验），**不用冒号**（冒号会拉低审计分）。
- **description**：一句话直接回答"它要多大的缸、好不好养"，120–160 个字符（`check` 会校验），带一个具体数字。
- **intro 第一段**必须出现主关键词（`check` 会校验）。
- **h1**：只有一个，和 title 不完全相同，也不用冒号。
- **H2/H3**：层级清楚，一个 H2 讲一个子问题，每个 H2 回答一个真实的长尾搜索（缸体尺寸、水温、混养、繁殖、寿命、公母区分……）。H2 标题里主词最多出现 2–3 次，整页主词密度不超过 3%。
- **short_answer**：放在开头，40–60 词，直接给出结论和关键数字。
- 正文 1,200–2,000 词。写够为止，不要为了字数注水。
- **faq**：4–6 条，取 Google "People also ask" 和相关搜索里的真实问题。
- 和站内其他物种页的 8-gram 重复度不超过 5%（用 `species_deep.py dupes` 检查）。

### 第 4 步：内链，做成一棵树
哥飞的规则：首页是主干，子目录是枝干，内页是小枝；从首页到任何内页不超过 4 次点击，内页还要能逐级回到上级目录。
- **向下**：`/species` 总览页要列出这个新页面。别的页面能进来，谷歌才会抓到它。
- **向上**：面包屑写成"首页 → Encyclopedia → 物种"。
- **横向（同一个物种）**：`related` 里优先放同一个物种的其他页面：`/compatibility/<slug>/`、`/fish-health/fish/<slug>`、对应的 `/calculators/` 和 `/guides/`，存在哪个就放哪个，再加 2–3 个相近的物种。
- **反向**：列出现在有哪些页面应该链到这个新页面（例如 compatibility 鱼对页面里提到这个物种的地方），写进报告里，等测试期结束后统一加，**这一步先不要改 compatibility 和 fish-health 的测试页**。

### 第 5 步：上线和观察（新站放量节奏）
1. 每批不超过 10 页。`check`、`dupes` 全部通过，并且 on-page 审计 ≥ 95 分之后才 `render`。`render` 会重写 nginx.conf 里 `# BEGIN/END species deep pages` 这一段，nginx.conf 经常有其他没提交的改动，提交时只提交这一段。
2. 新页面加进 sitemap。物种 sitemap 是 app 生成的，静态覆盖页要确认能出现在某个 sitemap 里，没有就加到 `sitemaps/static.xml`。
3. 上线后在 GSC 里观察 2–3 周：有没有收录、有没有出词、有没有排名和点击。
   - 这一批大部分都收录了、出词了，再做下一批。
   - 收录差或者有收录没排名：先分析原因（词选得太难？内容不够好？内链没接上？），调整后再上下一批 10 页。
4. 每批都在 `reports/species-new-batch-<日期>.csv` 记一笔：上线日期，和 14 天、28 天后的收录、曝光、点击、排名。
5. 具体的检出、渲染、首页卡片、sitemap、图片来源和推送步骤，见同目录的 `README.md`「上线流程」。注意本地检出经常落后于 origin，要在最新的 origin/main 上做。

### 交付清单
- 第 0 步的需求验证表（包括剔除了哪些物种、为什么剔除）
- 每个物种的 `<slug>.json` 和图片
- `check`、`dupes`、审计分数的结果
- 内链清单：新增了哪些链接，哪些反向链接要等测试期结束后再加
- 下一批的建议名单
