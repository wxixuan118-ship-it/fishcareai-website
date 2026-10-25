# 物种百科新增方案

为 `/species/<slug>` 补充竞品有流量、我们还没有的物种页。每页都是手工调研、带引用的静态页，由 `data-pipeline/species_deep.py` 渲染，nginx 优先返回静态页，物种 app 的数据库不动。

## 文件

| 文件 | 用途 |
|---|---|
| `data-pipeline/species_deep/GENERATION-PROMPT.md` | 每一批的执行提示词：需求验证、查重、调研、写作规则、内链、上线节奏 |
| `data-pipeline/species_deep/<slug>.json` | 页面内容（改内容只改 JSON，然后重新 render，不要直接改 HTML） |
| `reports/species-gap-aquariumstockingcalculator-2026-10-25.csv` | 总名单：竞品近 28 天有流量的 68 个物种页，扣掉我们已有的 8 个，剩下 48 个新物种（`new`）和 12 个已有物种的变种（`variant`） |
| `reports/species-new-batch-2026-10-25.csv` | 第一轮 10 个候选的需求验证结果和上线状态 |

## 方法（哥飞）

- **新站不批量上页面。** 每批最多 10 页，每页手工精做，上线后观察 2–3 周的收录和出词，再决定下一批的数量。
- **一个关键词一个页面。** 12 个变种（如 balloon molly、lionhead goldfish）默认并进已有页面，写成一个 H2 小节，不单独建页。只有变种词自己的搜索量明显更高、SERP 前 10 名有专门写它的页面时，才单独建页。
- **先验证需求再写。** 看美国月搜量、KGR（allintitle ÷ 月搜量）和 SERP 前 10 名，不值得做的直接剔除。
- **内链按树形结构。** 首页 → 物种总览 → 物种页，面包屑能逐级回去；每个新页面至少有一个相近的已有物种页链过来。

## 进度

| 批次 | 上线 | 物种 | 提交 |
|---|---|---|---|
| 已有物种重写 | 2026-10-25 | 20 个与竞品重叠的物种（archer fish、bolivian ram 等） | `25cb97a40` |
| 第 1 批 | 2026-10-25 | iridescent shark、mudskipper、motoro stingray | `d0c490d7f` |
| 第 2 批 | 2026-10-25 | flying fox、golden orfe、altum angelfish、orange chromide、demasoni | `d70fc2984` |
| 暂缓 | — | ruby tetra、royal acara（需求低） | — |

目前共 28 个深度物种页，首页 `#species-profiles` 区全部列出。

**下一步：**
1. 补第 1、2 批 8 个页面的美国月搜量和 allintitle，填进 `species-new-batch-2026-10-25.csv`。
2. 2026-11-08 前后看第一次 GSC 数据，2026-11-22 前后看第二次：收录、曝光、点击、排名，记进同一个表。
3. 收录和出词正常，就从总名单里按需求验证结果挑下一批（每批 ≤10 个）；不正常就先找原因再继续。
4. 12 个变种逐个并进对应的已有页面。

## 上线流程

本地 main 经常落后于 origin，工作区里也常有没提交的改动，所以**不要在本地检出里渲染和推送**。

1. 在临时目录检出最新的 origin/main：`git worktree add --detach <临时目录> origin/main`。页面的页脚是从 origin 的模板页复制的，必须在最新版本上渲染。
2. 在这个检出里写 `<slug>.json`，图片放到 `assets/encyclopedia/real/<slug>-wikimedia-real.jpg`。用原图宽度，不要放大到 1600 px。
3. 运行 `python3 data-pipeline/species_deep.py check <slug...>`，再运行 `dupes`，和其他页面的重复度要低于 5%。
4. 运行 `python3 data-pipeline/species_deep.py render <slug...>`。它只重新生成指定的页面，nginx 的 species deep 路由段会自动更新。
5. 用 on-page 审计检查，目标 ≥95：`python3 ~/.claude/skills/onpage-audit/scripts/onpage_audit.py species/<slug>/index.html -k "<主词>" --url https://www.fishcareai.com/species/<slug>`。
6. 补齐这几处：
   - 从相近的已有深度页 JSON 的 `related` 加一条链接，然后重新 render 那一页。
   - 首页 `#species-profiles` 按字母顺序加卡片。首页里这一区有两份（静态版和 JS 模板版），两份都要加，同时把区块描述里的物种数量改掉。
   - `sitemaps/static.xml` 加一条。app 生成的物种 sitemap 不会包含新 slug。
   - `image-credits/index.html` 加图片来源。
7. 提交后推送到 origin/main。AnySites 大约 1 分钟自动部署，部署后用 `curl "https://www.fishcareai.com/species/<slug>?v=$RANDOM"` 确认线上已生效。

## 踩过的坑

- **图片要人工看一遍。** Wikimedia 上按学名搜到的图可能认错了种（flying fox 第一次选的图就是），也可能是糊的。要选能看清这个物种识别特征的图。
- **首页物种区的样式。** 新版首页的样式表里没有 `.g4` 和 `.card` 的规则，所以 `#species-profiles` 自带一段限定在本区的 `<style>`。改布局时要保留它，否则卡片会变成一长列纯文字。
- **不要编数字。** 来源没给的数字（比如 altum 的缸体容积）可以按来源里的其他数据推算，但要在页面上写明是我们自己的建议。来源之间有冲突时，把两边的数都写出来。
- **测试期的页面。** compatibility 和 fish-health 正在做 A/B 测试，测试期内只链到总览页，不链到具体的鱼对页或症状页。
