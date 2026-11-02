# Weather Loach 页面处理方案

**给执行同事。** 这份方案推翻了原始任务「给 4 个页面加 dojo loach 别名」——原因在第 2 节。动手前请先读完第 2、3、5 节。

校准日期 2026-11-03。关键词数据来自 Google autocomplete（`hl=en gl=us`），页面状态为当日实测。

---

## 1. 一句话结论

这 4 个页面不是薄内容，问题也不是缺别名——**站内有两个泥鳅物种、三套页面在抢同一批查询**，先解决撞车，再谈改标题。

---

## 2. 为什么不能只加别名

原始判断是「weather loach 这 4 页没被收录，是因为站内没有 dojo loach 这个更常用的别名」。查下来，前半句对，后半句不完整。

真正的情况：

```
/fish-health/weather-fish-floating    →  "Weather Loach Floating at the Top? Too Warm or Short of Air"
/fish-health/weather-loach-floating   →  "Weather Loach Floating at Surface? Causes & Fast Fixes"
```

**两个不同的 URL，标题都以 "Weather Loach Floating" 开头。** 这不是别名缺失，是同题撞车。再加第三个别名 dojo loach 进去，只会让三方抢同一个查询。

---

## 3. 现状盘点

### 3.1 两个物种，不是一个

| URL 前缀 | 学名 | 中文 | 实际情况 |
|---|---|---|---|
| `/species/weather-loach` | *Misgurnus anguillicaudatus* | 东亚泥鳅 | 水族市场上的 dojo loach，就是它 |
| `/species/weather-fish` | *Misgurnus fossilis* | 欧洲泥鳅 | 欧洲原生，多国受保护，几乎不进水族贸易 |

同属不同种。但英文俗名高度重叠——"weather loach"、"weatherfish" 两边都在用，Google 不会替我们区分。

### 3.2 三套页面

每个物种各有 30 个症状页，症状清单**完全一一对应**（aggressive、black-spots、bloated … white-spots，30 个一个不差）。

此外还有 2 个页面被**静态页覆盖**了：

| slug | 来源 | 标题 |
|---|---|---|
| `weather-fish-floating` | 主仓库静态页（无 `x-powered-by: Next.js`） | Weather Loach Floating at the Top? … |
| `weather-fish-jumping` | 主仓库静态页 | Weather Loach Jumping? Pressure Changes … |

这两个是手工升级过的，标题写的是 "Weather Loach"，URL 却是 `weather-fish-*`。它们也正是 GSC 里有曝光的两个（weather-fish-jumping：128 曝光 / 2 点击 / 位置 8.15）。

### 3.3 这 4 个页面本身没问题

| 页面 | 审计分 | 正文词数 |
|---|---|---|
| weather-loach-floating | 92.7 | 756 |
| weather-loach-fuzzy-growth | 94.3 | 689 |
| weather-loach-rubbing | 92.7 | 658 |
| weather-loach-sunken-belly | 92.7 | 612 |

做过 5-gram 近重复检测，确认不是模板套壳：

```
同鱼种 不同症状   floating ~ rubbing          Jaccard  9.9%
同鱼种 不同症状   floating ~ sunken-belly     Jaccard 12.1%
同症状 不同鱼种   weather ~ zebra-loach       Jaccard 12.5%
完全无关对照      fuzzy-growth ~ white-spots  Jaccard 12.8%   ← 基线
```

最后一行是基线：两个毫无关系的页面重合度也有 12.8%，那是页头页脚侧边栏贡献的。前三行都在基线上下，**说明去掉公共外壳后几乎没有重复文本**。内容是按症状分别写的。

---

## 4. 关键词校准结果

### 4.1 别名：三选二

| 别名 | 判定 | 证据 |
|---|---|---|
| `dojo loach` | ✅ 主推 | 建议列表干净：for sale / tank size / size / tank mates / lifespan / care |
| `weather loach` | ✅ 保留 | 与 dojo 互为建议；`weather loaches (dojo loaches)` 本身就是一条建议 |
| `weather fish` / `weatherfish` | ❌ 弃用 | 同形词陷阱 |

**同形词陷阱的证据**，这条最重要：

```
"weather fish"         → weather fishers / weather fishkill ny / weather fish creek wi
"weatherfish"          → weatherfish shoes / weather fishers
"weatherfish aquarium" → (无建议)
"weather fish floating"→ (无建议)
```

输入 "weather fish"，Google 认为你在查**印第安纳州 Fishers 镇的天气**。这个词在水族语境里没有搜索行为。

> ⚠️ GSC 里 `weather-fish-jumping` 有 128 曝光、位置 8.15，看着像有需求。对照上面的建议列表，这些曝光很可能来自天气类查询的无效匹配。**不要拿这个曝光数当作保留 weather-fish 命名的理由**——这和游戏监控项目里踩过的 homonym 坑是同一个。

dojo 与 weather loach 互为建议，说明 Google 已经把两者当同义词：

```
"dojo loach floating"   → dojo loach floating upside down / weather loach floating upside down
"weather loach upside down" → dojo loach upside down / weather loach floating upside down
```

### 4.2 修饰词：比别名错得更离谱

现标题用的是 **"Floating at Surface"**。没有人这么搜。

```
"dojo loach floating"    → ① dojo loach floating upside down
                           ② dojo loach floating at top of tank
"weather loach floating" → ① weather loach floating upside down
                           ② weather loach floating top tank
                           ③ why is my weather loach floating
```

真实说法是 **floating upside down** 和 **floating at top of tank**，不是 "at surface"。

### 4.3 四个症状的需求差距很大

| 页面症状 | autocomplete | 结论 |
|---|---|---|
| floating | ✅ 两个别名下都有，且有明确修饰词 | 值得做 |
| sunken belly | ❌ 零建议 | 换说法：`dojo loach skinny` / `dojo loach skinny disease` 有建议，`loach skinny disease` 也有（clown loach / yoyo loach 变体都在） |
| rubbing | ❌ 零建议（`weather loach rubbing`、`dojo loach rubbing`、`loach rubbing on rocks` 全无） | 没有需求 |
| fuzzy growth | ❌ 零建议（`loach white fuzzy growth` 也无） | 没有需求 |

**4 个页面里只有 1 个有确切需求，1 个需要换说法，2 个没有需求。** 这是本次校准最该带走的结论。

---

## 5. 技术约束：标题现在改不动

执行前必须知道这一点，否则会在 Supabase 里白改一轮。

fish-health 页面的标题**不是存在数据库里的，是算出来的**：

```
app/fish-health/[slug]/page.tsx:72
  buildFishHealthTitle( buildSubject(species.common_name, problem.slug, problem.problem_name), … )
```

`lib/fish-health-meta.ts` 里的逻辑：标题 = `{物种名} {症状名}? Causes & Fast Fixes`，超过 60 字符就依次降级到更短的变体。

由此产生三个约束：

1. **`fish_health_content.meta_title` 和 `meta_description` 字段存在，但代码从来不读。** 改它们没有任何效果。
2. **`problems.problem_name`（"Floating at Surface"）是全物种共享的。** 改它会同时改掉所有鱼的 floating 页标题，不能为泥鳅单独改。
3. **目前唯一的按物种杠杆是 `species.common_name`**，但它一改就是该物种全部 30 页，而且 60 字符上限会把长名字截断。

所以**步骤 0 是一个代码改动**：让页面在 `meta_title` 非空时优先使用它。字段已经有了，接上即可。

---

## 6. 执行步骤

按顺序做。每步都能独立验证、独立回滚。

### 步骤 0 ｜ 打通 meta_title（代码，species-app）

仓库：`fishcareai-species-app`

在 `app/fish-health/[slug]/page.tsx` 的 `generateMetadata` 里，让 `content.meta_title` / `content.meta_description` 在非空时覆盖算出来的值；为空时保持现有行为不变。H1 同理（H1 取自同一个 `subject`）。

> 保持向后兼容：现在 60 个页面里绝大多数 `meta_title` 为空，必须一行都不变。改完后随便挑 5 个无关物种的页面比对标题，确认没动。

部署后约 **10 分钟**生效（这个 app 比静态站慢，不要以为没部署成功）。

### 步骤 1 ｜ 解决两个物种撞车（优先级最高）

这是真正的问题，比改标题值钱。

1. **给 *M. fossilis* 改名消歧义。** 把 `species.common_name` 从 **Weather Fish** 改成 **European Weatherfish**（当前值可由 `/fish-health/weather-fish-rubbing` 的标题 "Weather Fish Rubbing Against Objects?" 反推确认），并在该物种页正文写明「欧洲原生种，与水族常见的 dojo loach（*M. anguillicaudatus*）不是同一种鱼」。改完它的 30 个页面标题会自动带上 European，不再和泥鳅撞。
2. **处理两个静态页。** `fish-health/weather-fish-floating/` 和 `fish-health/weather-fish-jumping/` 在主仓库 `fishcareai-website` 里，标题写的是 "Weather Loach" 但 URL 是 `weather-fish-*`。两个选项，建议选 A：
   - **A（建议）**：既然内容写的是 dojo loach，就把这两页 301 到对应的 `/fish-health/weather-loach-floating`、`/fish-health/weather-loach-jumping`，并把内容里值得保留的部分合并过去。nginx 规则加在 `nginx.conf` 现有 clownfish 301 规则附近（第 55–59 行那一组）。
   - B：保留静态页，但把标题改成 European Weatherfish —— 不推荐，内容讲的不是那条鱼。
3. **如果 *M. fossilis* 的 30 个页面在改名后仍然零曝光**，下一轮按 `RETIRED_HEALTH_SLUGS` 的办法整体下线（见 `fishcareai-species-app/lib/consolidated.ts`，2026-10-30 和 11-02 两批都是这么做的）。这一步**本轮不做**，等观察。

### 步骤 2 ｜ 四个页面的标题校准（依赖步骤 0）

在 Supabase 的 `fish_health_content` 表里，给这 4 行写 `meta_title`（60 字符以内）：

| slug | 写入 meta_title | 字符数 |
|---|---|---|
| `weather-loach-floating` | `Dojo Loach Floating Upside Down or at the Top of Tank` | 53 |
| `weather-loach-sunken-belly` | `Dojo Loach Skinny or Sunken Belly: Skinny Disease?` | 50 |
| `weather-loach-rubbing` | `Dojo Loach Rubbing on Rocks? Causes & Fast Fixes` | 48 |
| `weather-loach-fuzzy-growth` | `Dojo Loach White Fuzzy Growth? Causes & Fast Fixes` | 50 |

同时在每页 `intro` 字段的第一句里自然带上别名，例如：

> A dojo loach (also sold as a weather loach) floating upside down or hanging at the top of the tank is …

**不改 URL、不加 301、不下线。** slug 继续用 `weather-loach-*`，改 URL 的收益不抵重定向的成本。

### 步骤 3 ｜ rubbing 与 fuzzy-growth 的处置

这两个症状在两个别名下都是零建议。本轮**照步骤 2 改完标题就停**，不要再投入扩写。

下一轮看数据：如果 60 天后仍是零曝光，并入泥鳅的 diseases 聚合页，按 `RETIRED_HEALTH_SLUGS` 下线这两个 slug。

---

## 7. 验证清单

每步做完逐条核对。

**步骤 0 之后**
- [ ] 随机 5 个无关物种的 fish-health 页，标题与改动前逐字一致
- [ ] 手工给任意一个测试页写入 `meta_title`，确认标题变了；清空后恢复原状

**步骤 1 之后**
- [ ] `/species/weather-fish` 标题含 European，正文有消歧义说明
- [ ] `/fish-health/weather-fish-floating` 与 `/fish-health/weather-loach-floating` 标题不再都以 "Weather Loach Floating" 开头
- [ ] 选 A 的话：两个静态 slug 返回 301，目标返回 200
- [ ] `/fish-health/sitemap.xml` 条数变化符合预期

**步骤 2 之后**
- [ ] 4 个页面标题为表中文字，全部 ≤60 字符，SERP 不截断
- [ ] 每页正文首句含 "dojo loach" 和 "weather loach"
- [ ] 重跑 onpage-audit，4 页均 ≥95（当前 92.7–94.3）：
      `python3 ~/.claude/skills/onpage-audit/scripts/onpage_audit.py <url> -k "dojo loach floating"`
- [ ] 提交 IndexNow（**提交前先确认每个 URL 都是 200**）：
      `node indexnow-submit.js <url> …`
- [ ] GSC 手动 Request Indexing（每天 10 条配额）

**30 / 60 天后**
- [ ] GSC 看这 4 页的曝光和查询词，确认进来的是 dojo/weather loach 查询而不是天气查询
- [ ] *M. fossilis* 30 页若仍零曝光，走下线流程

---

## 8. 风险与不做的事

**不要做**

- 不要跑 `data-pipeline/generate_compatibility_pages_v2.py`。它是坏的，跑一次会把 4148 个页面的标题回滚成旧的长标题。
- 不要在 `problems` 表里改 `problem_name` 来调标题——那是全物种共享的。
- 不要因为 `weather-fish-jumping` 有 128 曝光就保留 weather-fish 命名，见 4.1 的警告。
- 不要给这 4 页改 URL slug。

**注意**

- species-app 推送后约 10 分钟才生效，不是秒级。静态站约 1 分钟。
- 改 `species.common_name` 会同时影响该物种的 30 个 fish-health 页、species 页和所有 compatibility 页，改前先 grep 一遍影响面。
- 这 4 页内容在 Supabase，不在静态仓库；静态仓库里只有 `weather-fish-floating` 和 `weather-fish-jumping` 两个覆盖页。

**顺带发现，本方案不含，另行决定**

- 全站导航栏的 `/fish-health` 缺尾斜杠，每页吃一次 301。
- 站内 1200px 宽的 SVG 图表在手机上渲染到约 331px，字号只剩 4–5px，基本读不了。

---

## 9. 附录：校准原始数据

查询时间 2026-11-03，`suggestqueries.google.com/complete/search`，`client=firefox hl=en gl=us`。

```
dojo loach               → dojo loach / for sale / tank size / size / tank mates / lifespan / temperature / care
weather loach            → weather loach / for sale / weather loaches fish / size /
                           weather loaches (dojo loaches) / lifespan / tank size
pond loach               → pond loach / for sale / size / for sale near me / fish / lifespan / food

weather fish             → weather fishers / weather fishers indiana / weather fishkill ny /
                           weather fish creek wi / weather fishkill / weather fishersville va
weatherfish              → weatherfish / weatherfish shoes / weather fishers / weather fishkill /
                           weatherfish for sale / weatherfish size
weatherfish aquarium     → (无建议)
weather fish floating    → (无建议)
weather fish aquarium    → cold weather aquarium fish / what temperature should a fish aquarium be / …

dojo loach floating      → dojo loach floating upside down / dojo loach floating at top of tank /
                           dojo loach floating / weather loach floating upside down /
                           weather loach floating top tank / dojo loach tail floating / dojo loach keeps floating
weather loach floating   → weather loach floating upside down / weather loach floating top tank /
                           weather loach floating / dojo loach floating upside down /
                           dojo loach floating at top of tank / weather loach keeps floating /
                           why is my weather loach floating
dojo loach upside down   → dojo loach upside down / weather loach upside down /
                           dojo loach floating upside down / dojo loach laying upside down /
                           dojo loach sleeping upside down
loach floating upside down → loach floating upside down / loach swimming upside down /
                           dojo loach floating upside down / weather loach floating upside down /
                           kuhli loach floating upside down / clown loach floating upside down

dojo loach skinny        → dojo loach skinny disease / dojo loach skinny / dojo loach minimum tank size
weather loach skinny     → dojo loach skinny disease / dojo loach skinny / weather loach size
loach skinny disease     → loach skinny disease / clown loach skinny disease /
                           clown loach skinny disease treatment / yoyo loach skinny disease

dojo loach fuzzy         → (无建议)        weather loach fuzzy       → (无建议)
dojo loach white fuzzy   → (无建议)        loach white fuzzy growth  → (无建议)
dojo loach rubbing       → (无建议)        weather loach rubbing     → (无建议)
dojo loach scratching    → (无建议)        loach rubbing on rocks    → (无建议)
dojo loach sunken belly  → (无建议)        weather loach sunken belly→ (无建议)
dojo loach losing weight → (无建议)

european weatherfish     → european weatherfish / unique european weatherfish / trophy european weatherfish
misgurnus fossilis       → misgurnus fossilis / for sale / fishbase / sound
```

GSC（`reports/gsc-page-click-split-2026-09-28.xlsx`，2026-09-28 导出）里全部 weather/dojo 相关行：

```
/fish-health/weather-fish-jumping        2 clicks  128 impr  pos 8.15
/fish-health/weather-fish-bloated        1 click    87 impr  pos 6.89
/fish-health/weather-fish-not-eating     1 click    18 impr  pos 5.67
/compatibility/goldfish-and-weather-loach 1 click   18 impr  pos 10.89
/fish-health/weather-loach-fin-rot       1 click     8 impr  pos 5.38
```

查询维度里**没有任何 weather loach / dojo loach 查询**进入有点击或零点击列表——这 4 个页面当时连曝光都没有，与 GSC「已发现 - 尚未编入索引」的判定一致。
