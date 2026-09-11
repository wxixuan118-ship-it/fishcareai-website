# Compatibility 页面归属与改造清单

核查日期：2026-09-11。范围：本地静态站与生成器；未查询线上部署、Google 收录、GSC 流量或外链。本次只生成清单，没有修改页面、路由或发布网站。

## 1. 当前规模与实际缺口

| 检查项 | 本地结果 |
| --- | --- |
| Compatibility 总 Hub | `/compatibility/` |
| 单物种 Hub | 91 个，路径 `/compatibility/{species}/` |
| 配对页 | 4,099 个：91 个物种的 4,095 个组合，加 4 个专项页 |
| 总 Hub 链接物种 Hub | 91 / 91 |
| Pair 同时链接双方现有物种 Hub | 0 / 4,099 |
| Pair 只链接一方现有物种 Hub | 2 / 4,099 |
| Pair 未链接任何一方现有物种 Hub | 4,097 / 4,099 |
| 对应 Wiki 链接现有物种 Hub | 0（精确目标路径核查） |
| 现有 Tank Mates 专题 | 8 篇 |

上述内链计数检查 HTML 中的实际 a[href]，目标是 `/compatibility/{species}/`；不意味着页面没有其他 care guide 或 Tank Mates 专题链接。比如 Betta 配对页已有 Betta 专题入口。

因此，本轮应以“升级现有中间层、明确关键词归属、补齐双方入口”为主，不能继续按“缺少 31 个 Hub、仅有 465 页”的前提施工。

## 2. 页面归属建议

每个明确的物种 Tank Mates 搜索意图指定一个主要落地页。URL 无须扁平化；先保持现有路径，不新增 `/betta-fish-tank-mates/` 等同义页面。

| 页面类型 | 建议归属 | 内容职责 |
| --- | --- | --- |
| 总 Hub | `/compatibility/` | 兼容性方法、按物种浏览、选定两种鱼的入口 |
| 一般物种 Tank Mates | 现有 `/compatibility/{species}/` | 推荐、谨慎搭配、不建议搭配、条件和 FAQ |
| A+B | 现有 `/compatibility/{a}-and-{b}/` | 对这一个组合给出判断、原因、环境条件、替代选择 |
| Wiki / care guide | 现有物种资料和护理页 | 基础饲养内容，并导向该物种的 Tank Mates 主页面 |

### 已有专题的 8 组归属

以下是基于本地内容结构的初步归属；重定向之前需结合 GSC、外链和完整内容对比确定最终保留 URL。

| 物种/主题 | 建议主页面 | 另一页面如何处理 |
| --- | --- | --- |
| Betta | `/guides/betta-fish-care/tank-mates/` | 将 `/compatibility/betta-fish/` 的有用配对目录合入专题，再评估 301 |
| Discus | `/guides/discus-fish-care/tank-mates/` | 同步整合 `/compatibility/discus/` |
| Koi | `/guides/koi-fish-care/tank-mates/` | 同步整合 `/compatibility/koi/`，保留池塘同伴语境 |
| Oscar | `/guides/oscar-fish-care/tank-mates/` | 同步整合 `/compatibility/oscar/` |
| Telescope Goldfish | `/guides/telescope-goldfish-care/tank-mates/` | 细分品种专题；与 `/compatibility/goldfish/` 总体页面分工、互链 |
| Puffer | `/guides/puffer-fish-care/tank-mates/` | 多种河豚的总览；`/compatibility/pea-puffer/` 专注 Pea Puffer，不直接合并 |
| Blood Parrot | `/guides/parrot-fish-care/tank-mates/` | 保留专题；91 个物种 Hub 中没有同名对应项 |
| Snakehead | `/guides/snakehead-fish-care/tank-mates/` | 保留专题；91 个物种 Hub 中没有同名对应项 |

4 个直接重叠主题优先讨论整合。不要在缺少排名数据时直接删除、重定向或将差异明显的页面统一 canonical。页面归属确定后，Pair 应链接最终主页面，不能机械地全部指向 Compatibility 目录。

例如建议的闭环：

```text
/wiki/betta-fish/
    → /guides/betta-fish-care/tank-mates/
    → /compatibility/betta-fish-and-guppy/
    → /compatibility/guppy/
```

Pair 同时链接 Betta 专题和 Guppy Hub；双方主页面都链接回 Pair。

## 3. 优先级和实施清单

### P0：确定归属并准备可持续生成的数据

- 用 `species-ownership.csv` 确认 91 个物种的目标页；4 个直接重叠主题结合实际流量决定最终 URL。
- 建立统一物种 → Tank Mates 主页面映射，供总 Hub、Wiki、care guide、Pair 和 sitemap 使用。
- 先对 Betta、Guppy 做样板，确认推荐规则、分组和内容深度，再覆盖其他现有物种。
- 恢复或替换 v2 依赖的数据源：生成器所需的 `../data-pipeline/output/08_raw.json` 在本地缺失，当前不能直接重跑全量生成。
- 生成器还按旧的 urlset 方式改写根 sitemap；当前根文件已是 sitemapindex。必须先适配子 sitemap，避免把 url 节点写进 sitemapindex。

### P1：升级现有 Hub 的内容与排序

- 首屏直接展示少量相关搭配及 Good / Caution / Avoid 文字结论，每项进入 Pair；结论来自核实过的内容，不能照搬示例中的颜色。
- 完整目录分为 Best Tank Mates、With Caution、Fish to Avoid；各项说明判断理由和前提。没有适合的组合时明确说明，不强凑“15 Best”。
- 不把淡水与海水组合混入推荐列表；必要时在“不适合”解释中集中处理水体差异。
- 补充 Tank Size：区别单物种最低空间和完整混养群体的需求，说明成年体型、群养数量、领地与过滤负荷。
- 补充 Water Parameter Overlap：温度、pH、水体类型；参数交集不能单独作为安全结论。
- FAQ 针对该物种，例如攻击性、虾类风险、小缸、是否适合独养，不给 91 页机械换名的同一套回答。
- 标题、H1、描述与实际内容一致；数值标题只能使用实际列出的数量。
- 排序依据是用户选择与饲养条件。生成器仍包含 `SEO priority` 展示文案和按搜索价值排序的逻辑，应从用户页面移除。
- 推荐结果须与对应 Pair 的最终结论对齐。现有评分列表只能作为待审核数据，不能直接当作编辑认可的推荐名单。

### P1：补齐内链闭环

- 总 Hub 的物种入口指向映射中的最终主页面。
- 每个 Pair 添加两个有名称的入口，例如 “Explore all Betta Fish Tank Mates” 和 “Explore all Guppy Tank Mates”。
- 每个物种主页面覆盖该物种已有的相关 Pair，按风险与相关性分组。
- Wiki 和 care guide 在混养相关段落加入主要 Tank Mates 入口。
- 页面 breadcrumb 保持单一可理解的路径；双方入口作为正文导航，不用伪造两套父级 breadcrumb。
- 同步更新生成器与手工专项生成器，避免下次构建覆盖改动。

### P1：处理 4 个超出 91 物种目录的 Pair

| 配对页 | 缺失的物种 Hub | 处理建议 |
| --- | --- | --- |
| `/compatibility/betta-fish-and-amano-shrimp/` | Amano Shrimp | 先链接 Betta 主页面；Amano 端需先补正式归属 |
| `/compatibility/betta-fish-and-ghost-shrimp/` | Ghost Shrimp | 同上，不生成不存在的 Hub 链接 |
| `/compatibility/koi-and-pleco/` | Pleco（泛称） | 先明确具体种类，不能直接当作 Bristlenose Pleco |
| `/compatibility/koi-and-turtles/` | Turtles（泛称） | 保留池塘同伴语境，单独定义主题页，不伪装成单鱼种 Hub |

### P2：验收后再考虑扩物种

- 核查改动页面的链接可达性、双向覆盖、canonical、标题唯一性和 sitemap 内容。
- 91 物种范围内的 4,095 个 Pair 应全部有双方主页面入口；4 个专项页单独验收，不计作已完整覆盖。
- 检查首屏和移动端长列表、分组导航、文字状态标签，并核对首屏推荐与 Pair 结论一致。
- 保留手工加强过的 Pair 内容，尤其 `upgrade_compatibility_pilot.py` 和专项集群生成器输出，避免全量重生成冲掉修改。
- 在现有页面的内容和链接验收通过后，再决定是否扩到更多物种；这次没有扩页需求。

## 4. 随附逐页清单

- `species-ownership.csv`：91 个物种的现有 Hub、建议主页面、专题冲突、Wiki、sitemap 状态与动作。
- `pair-link-actions.csv`：4,099 个 Pair 的双方物种、现有 Hub 入口、建议目标与异常标记。

清单中的目标是改造建议，不表示迁移已执行。未检查线上收录和排名，不能据此断言现有重叠已经造成关键词竞争或流量损失。
