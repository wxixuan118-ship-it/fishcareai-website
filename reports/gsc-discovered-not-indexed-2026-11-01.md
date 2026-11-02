# GSC「已发现 - 尚未编入索引」82 页处置 — 2026-11-01

导出文件：`fishcareai.com-Coverage-Drilldown-2026-11-01 (1).xlsx`（82 URL，全部「上次抓取日期」为空 = Google 从未抓取）。
趋势：08-18 峰值 335 → 10-23 的 82，方向是对的。

## 根因：不是页面质量，是抓取预算

sitemap 已知 URL 总量 **12,466**：

| sitemap | URL 数 |
|---|---|
| fish-health（species app） | 7,750 |
| compatibility-1 + -2 | 4,151 |
| species | 257 |
| guides | 188 |
| static | 98 |
| wiki + identify | 22 |

抽样全部返回 200、`robots: index,follow`、canonical 自指 —— 技术上没有任何问题。
决定性证据是**它们在 sitemap 里的位置**：

- 20 个 fish-health URL 落在 7,750 条的第 **7,050–7,723** 位 → **最后 9%**。
- 45 个 compatibility URL 中 36 个落在 4,151 条的 67% 之后，最远到 99.1%。

Google 从上往下抓，抓到约 91–97% 就停。所以逐页「修内容」没用，**必须把 URL 总量降下来**。

## 结构性大头：872 个跨水体组合页（21% 的 compatibility 集群）

compatibility 是 91 物种全组合（4,060 对 + 91 hub）。其中 **11 个海水种**（lionfish、blue tang、yellow tang、
watchman goby、percula clownfish、foxface rabbitfish、flame angelfish、firefish goby、royal gramma、
coral beauty、pajama cardinalfish）× **80 个淡水种** = **872 页生物学上不可能的组合**。

这些页面自己就写着 0/100：

> ❌ One of these is a marine species and the other is not; they cannot share one aquarium.

没有人会搜 "can lionfish and zebra loach live together"。本次 82 页里有 **27 页**正属于这一类 —— Google
精准地跳过了垃圾。删掉这 872 页，compatibility 抓取预算每页提升 ~27%。

保留 54 个海水×海水组合（狮子鱼+小丑鱼、倒吊+神仙 等是真实海缸问题）。

## 82 页分类（明细见同名 .csv）

| 处置 | 页数 | 对象 |
|---|---|---|
| **404 删除** | 27 | 跨水体 compatibility（连带清理全部 872 页） |
| **unpublish** | 7 | 冷门物种 fish-health（~700 词模板，无 diseases hub 承接） |
| **扩写后重提** | 4 | goldfish-care/{breeding,spots-colour,swim-bladder}、telescope-goldfish-care/eye-problems（460–535 词，低于门槛） |
| **直接重提索引** | 16 | 2 个 calculators + 11 个 1,000–1,500 词 guides 子页 + 3 个海水×海水 compatibility |
| **保留不动** | 28 | 15 个淡水 compatibility（threadfin rainbowfish 为主）+ 13 个常见物种 fish-health；清完垃圾页后自然会被抓到 |

## 顺带发现的问题

`/aquarium-fish-diseases/` 有 **133 个 hub 目录，只有 7 个进了 sitemap**。进了的那 7 个是 1,766–2,530 词、
16–22 个锚点的完整页；剩下 **126 个是 <400 词的空壳**（如 tropheus-cichlid-diseases 仅 315 词、0 锚点、
0 条指向 /fish-health/ 的链接）。不进 sitemap 是对的，但这说明**合并方案只做了 4 个小丑鱼物种就停了**。

真正的长期解法是把 clownfish 那套 301 合并模式推广开：冷门物种的 ~30 个症状页 301 到
`/aquarium-fish-diseases/<species>-diseases/#<anchor>`，前提是先把 hub 写到 2,000 词。
190 个冷门物种 × 30 页 → 190 页，站点 URL 从 12,466 降到约 6,900，抓取预算翻倍。这是独立项目，不在本次范围。

## 执行清单

1. `reports/compatibility-cross-water-delete-2026-11-01.txt` — 872 个待删 URL
   删目录 → 重建 11 个海水 hub + 80 个淡水 hub 的 tank-mate 列表（去掉跨水体行）→ 重生成
   `sitemaps/compatibility-1.xml` / `-2.xml` → 更新 `sitemap.xml` lastmod
2. `reports/gsc-discovered-not-indexed-2026-11-01-unpublish.sql` — 在 species-app 的 Supabase SQL editor 执行
3. 扩写 4 个薄页 → 跑 `/onpage-audit` 到 95+
4. 16 个页面走 IndexNow + GSC Request Indexing
5. 重跑 `scripts/build-feed.py`
