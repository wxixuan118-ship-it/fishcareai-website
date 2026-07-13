# FishCare AI Tools MVP PRD

版本：MVP v1  
日期：2026-07-06  
阶段：第一阶段，1–2 个月，SEO 流量优先，无需 LLM  
范围：官网 Tools 模块新增 5 个免费工具，并移除 AI Assistant

## 1. 背景

FishCare AI 官网目前已经具备鱼类百科、care guide、搜索入口和基础工具能力。下一阶段的核心目标不是继续大量发文章，而是通过“高搜索需求 + 高实用性 + 低开发复杂度”的免费工具获取自然搜索流量，并提高用户停留时间、页面互动率和后续 App 转化。

第一阶段不使用 LLM，所有工具基于结构化规则、公式、阈值和本地物种数据库完成计算。这样可以降低开发成本、避免 AI 成本、提升响应速度，也更适合做 SEO landing page。

## 2. 产品目标

### 2.1 业务目标

- 建立 FishCare AI 的“实用鱼缸工具中心”定位。
- 用免费工具承接高频关键词流量，例如 tank size calculator、fish compatibility checker、water parameter checker、fish feeding calculator、aquarium planner。
- 提升 Tools 页面访问深度和用户互动。
- 为后续 App 积累功能验证、用户需求和数据埋点。

### 2.2 用户目标

- 新手可以快速知道鱼缸大小是否合适。
- 用户可以判断不同鱼能不能混养。
- 用户可以根据水质读数判断风险。
- 用户可以控制喂食量，减少水质恶化。
- 用户可以在买鱼前获得基础鱼缸配置建议。

## 3. MVP 功能范围

本版本包含 5 个免费工具：

1. Tank Size Calculator
2. Compatibility Checker
3. Water Parameter Checker
4. Feeding Calculator
5. Aquarium Planner

本版本明确不包含：

- AI Assistant / LLM 问答
- 用户登录
- 云端保存鱼缸档案
- 图片识别
- 付费订阅
- 多鱼缸长期追踪
- 医疗诊断类结论

## 4. 目标用户

### 4.1 新手养鱼用户

刚买鱼或准备买鱼，需要知道鱼缸大小、换水、喂食和设备基础。

### 4.2 已有鱼缸但频繁出问题的用户

常见问题包括鱼死亡、水浑、鱼浮头、藻类爆发、喂食过量、混养打架。

### 4.3 准备扩缸或新增鱼种的用户

需要提前确认鱼的成年体型、攻击性、水温、pH、群居需求和空间需求。

## 5. 用户故事

### Tank Size Calculator

- 作为新手用户，我想输入鱼的种类和数量，快速知道至少需要多大的鱼缸。
- 作为准备扩缸的用户，我想看到“最低尺寸”和“更安全尺寸”，避免买太小。

### Compatibility Checker

- 作为社区缸用户，我想选择多种鱼，判断它们是否能一起养。
- 作为买鱼前用户，我想知道风险原因，例如温度不匹配、pH 不匹配、攻击性强。

### Water Parameter Checker

- 作为鱼状态异常的用户，我想输入 ammonia、nitrite、nitrate、pH、温度和硬度，知道水质是否危险。
- 作为维护鱼缸的用户，我想获得明确行动建议，例如换水、增加打氧、停止喂食。

### Feeding Calculator

- 作为新手用户，我想知道每天喂几次、每次喂多少，避免过量。
- 作为多鱼缸用户，我想根据鱼种和数量获得更保守的喂食建议。

### Aquarium Planner

- 作为准备开缸的用户，我想输入鱼缸类型、容量和目标，得到基础设备和 stocking 建议。
- 作为计划养海水、虾缸或金鱼缸的用户，我想看到不同类型鱼缸的关键差异。

## 6. 功能需求

### 6.1 Tank Size Calculator

输入：

- Species
- Number of animals
- Tank style：standard rectangle、long swimming tank、tall tank、nano tank

输出：

- Practical minimum gallons
- Recommended upgrade gallons
- Temperature target
- Group plan
- Setup note

核心逻辑：

- 每个物种维护 adult size、activity factor、minimum gallons、temperature、group rule。
- 计算结果取“物种最低缸体要求”和“成年尺寸 × 数量 × 活动系数”的较大值。
- 输出结果向上取整到接近的 5 gallons。

验收标准：

- 用户选择 Betta + 1 条，结果不低于 5 gallons。
- 用户选择 Goldfish + 1 条，结果不低于 20 gallons。
- 用户改变数量后结果能更新。
- 输出必须包含“推荐更安全尺寸”，而不是只给最低尺寸。

### 6.2 Compatibility Checker

输入：

- 多选鱼种

输出：

- 每一对鱼的兼容状态：Compatible、Use Caution、Not Compatible
- 风险解释

核心逻辑：

- 检查温度区间是否重叠。
- 检查 pH 区间是否重叠。
- 检查攻击性等级。
- 对 Betta 等特殊物种设置强规则。

验收标准：

- 少于 2 个物种时不能运行检查。
- Betta 与高风险混养应给出 Not Compatible 或 Use Caution。
- 温度或 pH 完全不重叠时必须提示 Not Compatible。

### 6.3 Water Parameter Checker

输入：

- pH
- Ammonia
- Nitrite
- Nitrate
- Temperature
- GH

输出：

- Overall health score
- 每个参数的 Good / Warning / Danger 状态
- 对危险参数给出行动建议

核心逻辑：

- Ammonia 和 Nitrite 权重最高，安全目标必须是 0 ppm。
- 若 ammonia 或 nitrite 危险，总分上限降低。
- 根据参数区间给出状态和建议。

验收标准：

- Ammonia > 0 必须提示 Warning 或 Danger。
- Nitrite > 0 必须提示 Warning 或 Danger。
- 危险结果必须展示“Act Now”类提示。

### 6.4 Feeding Calculator

输入：

- Species / animal type
- Number of animals
- Meals per day

输出：

- 每天喂食次数
- 每餐建议进食时间窗口
- 推荐食物类型
- 剩余食物处理规则

核心逻辑：

- 根据物种体型、数量和每日餐数给出保守喂食时间。
- 对 shrimp、snail、goldfish 给出不同食物类型。
- 默认强调“吃完为准，不以固定克数为准”。

验收标准：

- 输出必须包含“remove leftovers”或等价剩食处理建议。
- Goldfish、Shrimp、Snail 必须有不同的食物建议。
- 用户修改餐数后输出会变化。

### 6.5 Aquarium Planner

输入：

- Tank type：Freshwater、Saltwater、Shrimp tank、Goldfish tank
- Experience level
- Primary goal
- Tank volume

输出：

- Tank capacity label
- Equipment checklist
- Stocking recommendation
- Cycling warning
- Setup priority

核心逻辑：

- 根据 tank type 输出不同设备清单。
- 小缸给出保守 stocking 提醒。
- 所有类型都必须提醒 cycling 完成后再放生物。

验收标准：

- Saltwater 输出必须包含 marine salt mix 或 refractometer 类提示。
- Shrimp tank 输出必须包含 sponge filter 或 shrimp-safe minerals 类提示。
- Goldfish tank 输出必须强调 oversized filtration 或大水体。
- 所有结果必须包含 ammonia/nitrite 归零后再放鱼的提醒。

## 7. 页面与信息架构

### 7.1 Tools 主页面

页面标题：Aquarium Tool Center  
副标题：5 free, no-LLM calculators built for SEO traffic and everyday aquarium planning.

Tab：

- Tank Size
- Compatibility
- Water Parameters
- Feeding
- Aquarium Planner

页面底部：

- 引导用户阅读 care guides
- 可链接到 Guides / Encyclopedia

### 7.2 首页入口

首页 Free Tools 区块展示 5 个工具卡片，每张卡片包含：

- 工具名称
- 一句话价值描述
- Open Tool 按钮

### 7.3 Footer 入口

Footer Tools 列表展示 5 个工具链接。

## 8. SEO 需求

### 8.1 目标关键词

- tank size calculator
- fish tank size calculator
- aquarium size calculator
- fish compatibility checker
- aquarium fish compatibility chart
- water parameter checker
- aquarium water test calculator
- fish feeding calculator
- how much to feed fish
- aquarium planner
- fish tank planner

### 8.2 页面内容要求

- 每个工具的 H2 使用完整关键词。
- 工具说明首段直接回答用户能得到什么。
- 工具结果页/状态区提供可读文本，不只显示数字。
- 内链到相关 care guide。
- 保留免费工具定位，降低跳出率。

## 9. 数据与规则库

MVP 阶段使用前端本地结构化数据：

- fish profile：name、adult size、activity、minimum tank、temperature、group rule
- compatibility data：pH range、temperature range、aggression level
- water parameter thresholds
- food type rules
- planner equipment rules

后续 App 阶段可迁移到后端数据库。

## 10. 埋点指标

建议记录以下事件：

- tool_opened：用户打开某个工具
- tool_calculated：用户点击计算
- tool_species_selected：用户选择物种
- tool_result_viewed：用户看到结果
- guide_clicked_from_tool：从工具点击进入文章
- newsletter_signup_from_tool：从工具页订阅

核心指标：

- Tools 页面访问量
- 每个工具的点击率
- 每个工具的完成率
- 工具页平均停留时间
- 从工具到 guide 的点击率
- SEO CTR

第一阶段目标：

- Search Console CTR 首个目标：2%
- 工具完成率目标：30%+
- Tools 页面平均停留时间：60 秒+

## 11. 风险与限制

- 规则工具不能替代兽医或专业诊断。
- 不同品系、年龄、鱼缸过滤能力会影响真实结果。
- Compatibility Checker 只能做风险判断，不能保证绝对安全。
- Water Parameter Checker 依赖用户测试读数准确性。
- Feeding Calculator 应避免给精确克数，以免误导。

## 12. 后续版本

### v1.1

- 为每个工具创建独立 SEO landing page。
- 增加更多鱼种、虾、螺、海水鱼规则。
- 增加结果分享链接。
- 增加“保存我的鱼缸计划”邮箱收集。

### v2 App 版本

- 用户鱼缸档案
- 多鱼缸管理
- 水质记录曲线
- 换水和喂食提醒
- 图片识别鱼病 / 藻类
- AI 问答与个性化建议
- 社区案例库

## 13. MVP 发布验收清单

- Tools 页面不再出现 AI Assistant。
- 首页工具区显示 5 个工具。
- Footer 显示 5 个工具。
- 每个工具都可以打开并计算。
- Water Parameter Checker 无脚本错误。
- 移动端 Tab 可横向滚动或正常换行。
- GA 已能追踪页面访问。
- 结果文案避免医疗诊断承诺。

