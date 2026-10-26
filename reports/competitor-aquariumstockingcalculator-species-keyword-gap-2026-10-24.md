# 竞品关键词差距：aquariumstockingcalculator.com 物种页

- 日期：2026-10-24
- 数据源：竞品近 28 天自然流量页面明细（截至 2026-10-20），共 70 个 URL，每个页面取一个排名词
- 对比对象：fishcareai.com 线上 `/species/`（站点地图共 258 个物种页）

## 背景

- 竞品约 75% 的流量来自首页（约 830），物种页每页都不到 50，很多词已经标成 "Lost"。
- 这些词都是低量长尾，适合拿来补我们页面里缺的词，不值得为它们单独建页。

## 一、模板层面（一处改动，覆盖全部物种页）

竞品的 70 个词里有 12 个是 **"tank size for X"** 格式。我们的物种页 H2 都是固定 9 段（Overview / Scientific Classification / Natural Habitat / Appearance & Size / Behavior & Temperament / Water Requirements / Interesting Facts / Species Related / Related Species & Guides），**没有单独的 "Tank Size" 段**。比如 fairy cichlid、keyhole cichlid 页面里 "gallon" 一次都没出现。

建议：

- 增加 **H2 "X Tank Size"**，第一句直接给答案，例如 "Fairy cichlids need at least 30 gallons…"
- 增加 **"Care Level / Difficulty"** 字段（对应 "upside down catfish difficulty"、"humphead glassfish difficulty"）

注：物种页是 anysites 上的 Next.js 应用从数据库渲染的（见 `nginx.conf` 的 `/species` 反代），不在本仓库，模板要去那边改。

## 二、和竞品重叠的 20 个页面，可以补的词

| 我们的页面 | 竞品排名词 | 我们页面现状 → 建议补充 |
|---|---|---|
| bolivian-ram | bolivian ram care sheet | 没有 "care sheet" → 加进 title/描述 |
| fairy-cichlid | tank size for fairy cichlid | 没写加仑数；缺别名 lyretail（*N. brichardi*） |
| keyhole-cichlid | keyhole cichlids, tank size | 缺加仑数 |
| three-spot-gourami | 3 spot gourami | 没有数字写法；缺变种名 blue / opaline gourami |
| upside-down-catfish | upside down catfish difficulty | 页面没有 "difficulty" 这个词 |
| zebra-loach | zebra loach + barilius 混养 | 没有 "tank mates" 段 |
| bristlenose-pleco | bristle nose pleco care、longfin、super red | 没有 "bristle nose" 拼法；缺变种 longfin / super red / albino |
| pristella-tetra | glofish pristella、能否与 black skirt tetra 混养 | 缺 GloFish 变种；缺 black skirt 混养（可链到混养配对页） |
| emerald-catfish | emerald cory catfish | 缺 "emerald cory" 和 *Corydoras splendens*（旧学名，现为 *Brochis splendens*，页面已有 Brochis） |
| **blind-cave-tetra** | **mexican tetra** | "mexican tetra" 只出现 1 次 → 放进 title/H1（同为 *Astyanax mexicanus*） |
| honey-gourami | red honey gourami、red robin gourami | 两个变种名都没有 |
| goldfish | lionhead goldfish | 没有 lionhead / oranda 变种段 |
| archer-fish | clouded archer fish | 缺 "clouded" |
| peacock-spiny-eel | peacock eel size | 没有 "peacock eel" 简称；体长没用英寸写 |
| molly | balloon molly | 没有 "balloon" |
| betta-fish | female betta fish | 只出现 1 次 → 加一段 female / sorority |
| badis | black tiger badis | 缺这个变种 |
| forktail-blue-eye | blue eye rainbowfish | 缺这个通用叫法 |
| congo-tetra | congo tetra | 已经覆盖 |
| four-eyed-fish | four eyed grouper | 这是另一种鱼，不用管 |

## 三、我们没有的 48 个物种

搜索意图较明确、值得以后补的（主观判断，无搜索量数据）：iridescent shark、flying fox、goliath tiger fish、mudskipper、motoro stingray、altum angelfish、demasoni、lionhead goldfish、royal acara、ruby tetra、golden orfe、golden cobra snakehead、fly river turtle。

其余是小众品种（L 编号异形、danionella 等），优先级低。

如果建新页，可以先从 **iridescent shark、motoro stingray、flying fox** 开始：都是大众鱼种，而且分别能和现有的 bala shark、rainbow shark、siamese/chinese algae eater 页面互相内链。

## 附：竞品 URL → 排名词

| 竞品 slug | 排名词 |
|---|---|
| （首页） | aquarium fish calculator |
| calculators | aquarium water change calculator |
| calculators/volume | fish tank volume calculator |
| bolivian-ram | bolivian ram care sheet |
| flying-fox | flying fox fish carachteristics |
| goliath-tiger-fish | goliath tiger fish |
| iridescent-shark | iridescent sharks |
| mudskipper | where do mudskippers live |
| agassizs-dwarf-cichlid | tank size for agassizs dwarf cichlid |
| altum-angelfish | altum angelfish |
| aurora-cichlid | tank size for aurora cichlid |
| balloon-molly | balloon molly |
| black-morpho-tetra | tetra morpho black |
| black-tiger-badis | black tiger badis |
| blue-moon-danio | blue moon danio |
| blue-panaque-l239 | l239 |
| blue-tail-borneo-sucker | borneo loach |
| brevis-shelldweller | tank size for brevis cichlid |
| bulgarian-green-seal-point-angelfish | green seal bulgarian angelfish |
| chinese-high-fin-banded-shark | chinese high fin banded shark |
| clouded-archerfish | clouded archer fish |
| congo-tetra | congo tetra |
| cururu-stingray | freshwater stingray care guide |
| danionella-cerebrum | danionella cerebrum fisch |
| demasoni | demasoni cichlid aquarium |
| egyptian-mouthbrooder | tank size for egyptian mouth brooder |
| emerald-green-corydoras | emerald cory catfish |
| fairy-cichlid | tank size for fairy cichlid |
| fangs-puffer | puffer fang |
| female-betta | female betta fish |
| fenestratum-cichlid | tank size for fenestratus |
| five-bar-cichlid | tank size for five barred lamprologus |
| fly-river-turtle | fly river turtle |
| four-eyed-fish | four eyed grouper |
| freshwater-frogfish | minium tank gallo for frogfish |
| glofish-pristella | do pristilla tetras get along with skirt tetra |
| golden-cobra-snakehead | golden snakehead fish |
| golden-orfe | golden orfe |
| hairy-puffer | hairy puffer fish puffed up |
| hovering-zebra-loach | hovering loach |
| humphead-glassfish | humphead glassfish difficulty |
| indian-mud-moray-eel | how to take care of indian mud eel |
| kansu-loach | kansu loach |
| keyhole-cichlid | keyhole cichlids |
| king-tiger-plec-l066 | pleco l066 king tiger |
| lampeye | lamp eye tetra |
| lionhead-goldfish | lionhead goldfish |
| longfin-bristlenose-pleco | bristle nose pleco care |
| malawi-hawk | malawi hawk female cichlid |
| mexican-tetra | mexican tetra |
| motoro-stingray | motoro stingray |
| mottled-bichir | mottled bichir (polypterus weeksii) |
| needle-nose-gar | needlefish, needlenose gar, asian needle gar |
| neon-blue-rasbora | blue neon rasbora |
| nichols-mouthbrooder | tank size for south african mouthbrooder |
| orange-chromide | orange chromide |
| orange-venezuelan-cory | orange venezuelan cory no orange color on dark substrate |
| peacock-eel | peacock eel size |
| rainbow-shiner | rainbow shiner |
| rainbow-stiphodon-goby | stiphodon ornatus rainbow how many in a group so they feel happy |
| red-honey-gourami | red robin gourami |
| red-neon-blue-eye-rainbow | blue eye rainbowfish |
| royal-acara | royal acara |
| ruby-tetra | ruby tetras |
| super-red-bristlenose-pleco | super red bristlenose pleco |
| t-bar-cichlid | tank size for t bar cichlid |
| three-spot-gourami | 3 spot gourami |
| upside-down-catfish | upside down catfish difficulty |
| vulcan-cory | vulcan cory |
| west-african-lungfish | lungfish aquarium |
| zebra-loach | zebra loaches compatbel with barillius? |
