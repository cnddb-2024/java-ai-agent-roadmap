# Skill: 融合教程生成

> 为每日飞书作业生成专属融合教程 HTML，存入路线图仓库对应作业目录，并将飞书任务评论链接指向教程。

## 适用场景

定时任务在每日维护流程中，识别当天 due 的作业任务，为每个任务生成一份个性化的融合教程。也可在用户对话中手动触发。

## 输入

| 参数 | 说明 |
|------|------|
| 飞书任务 GUID | 从飞书清单获取，用于写回评论链接 |
| 任务全称 | 飞书任务 summary，用于 HTML 顶部标题 |
| 当前 Phase | 从路线图 HTML 解析（Phase 0/1/2/3），用于标注上下文 |
| 路线图推荐参考项目 | 从路线图 HTML 中提取与该任务相关的推荐项目链接 |
| 作业日期 | YYYY-MM-DD，决定存放目录 |
| 作业目录 slug | 当天该任务在 assignments/ 下已有的目录名 |

## 规范要求

### 1. 技术栈主次

- **主线语言：Java**（LangChain4j + Spring AI 双路径，LangChain4j 优先因已掌握，Spring AI 正在补）
- **Python 仅作辅助**：SDK 写入/检索测试可展示，但不展开 RAG 链等进阶内容（那是 Python 贯穿线的事）
- 所有示例代码以 Java 视角重写

### 2. 学习时长

- HTML 顶部 Hero 区标注总预估时长，**控制在 1 小时以内（极限 1.5 小时）**
- 教程内按阶段标注分钟数（如"部署 20min / Java SDK 25min / 总结 10min"）

### 3. 文件命名

- 统一叫 `tutorial.html`，不随任务变化
- 不再出现 `qdrant-deploy-guide.html` 这种每次不同的名字

### 4. 存放位置

```
assignments/YYYY-MM-DD/<已有任务目录slug>/tutorial.html
```

- 与该任务的 `code/`、`summary.md` 平级
- 目录 slug 沿用当天飞书任务对应的已有命名

### 5. 飞书跳转

- 生成后将 **飞书云盘 URL**（非 GitHub raw URL）写入飞书任务的评论中
  - 背景：GitHub 仓库不可访问（私有/不存在/未 push）曾导致 raw URL 全部 404，已废弃此路径
  - 现方案：教程 HTML 上传到飞书云盘 `assignments/<due日期>/<slug>/tutorial.html`，与 GitHub 仓库目录结构保持一致便于溯源
- 用户正常路线：飞书任务 → 评论中的飞书云盘 URL → 点击预览/在浏览器中打开 → 完美渲染（HTML 原生执行环境）
- 不在 HTML 内写 GUID 或"作业二"这类模糊标识
- HTML 顶部标注当前 Phase 和任务全称（与飞书一致）
- 飞书云盘预览卡片为基础结构视图，点击「在浏览器中打开」可看完整效果（自定义字体/Mermaid/ECharts/CSS 全保留）

### 6. 教程来源

- 搜索互联网上的多个教程（至少 5 个来源），贴出完整链接
- 同时从路线图 HTML 中提取与该任务相关的推荐参考项目链接
- **两者地位完全平等**，都是过程素材
- 最终在 HTML 底部"教程来源"中统一列出，不区分"官方/社区/路线图"分类
- 重点产出是融合教程本身，来源只是素材

### 7. 路线图上下文

- HTML 顶部标注当前 Phase（如 Phase 1 RAG 刚需闭环）
- 标注任务全称（与飞书任务 summary 一致）
- 引用路线图中推荐的参考项目和面试题
- 呼应路线图中对应 Phase 的验收标准

### 8. HTML 技术要求

- 自包含 HTML 文件（无外部依赖）
- 使用 html-report skill 规范生成
- 文件名固定为 `tutorial.html`
- 字体使用 canvas-fonts（如 InstrumentSans + JetBrainsMono）
- 图表/图示用 Mermaid 或 ECharts
- 底部含"教程来源"章节，使用 `<ol>` 有序列表

### 8.1 代码块规范（极其重要 -- 防高亮标签泄漏）

**问题背景**：此前生成的教程使用手动 `<span class="tok-xxx">` 标签包裹代码 token 实现语法高亮。这种方式存在严重缺陷：
- LLM 生成时经常出错：span 标签未闭合、嵌套错误、属性泄漏到可见文本
- 用户复制代码时 `class="tok-str">` 等 HTML 属性残留在代码中，导致代码无法编译
- GitHub raw 视图下 span 标签暴露为可见文本

**强制规则（禁止违反）**：

1. **禁止在 `<pre><code>` 内部使用任何 `<span>` 标签做语法高亮**。代码块内容必须是纯文本，不含任何 HTML 标签（除 HTML 实体转义 `&lt;` `&gt;` `&amp;` 外）。

2. **正确的代码块写法**：
```html
<pre><code>public class WeatherTools {

    @Tool(description = "查询指定城市的实时天气")
    public WeatherResponse getWeather(String city) {
        return weatherService.query(city);
    }
}</code></pre>
```
注意：`<pre><code>` 内部是纯文本，`<` 用 `&lt;` 转义，`>` 用 `&gt;` 转义，`&` 用 `&amp;` 转义。不包裹任何 span。

3. **语法高亮通过 CSS 样式整个代码块实现**，而非逐 token 着色：
```css
pre code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  background: #1c2128;
  color: #e6edf3;
  display: block;
  padding: 16px;
  border-radius: 8px;
  white-space: pre;
  overflow-x: auto;
}
```

4. **行内代码** 使用 `<code>` 标签，同样不含 span：
```html
<p>使用 <code>@Tool</code> 注解定义工具方法。</p>
```

5. **禁止出现的模式**（生成后必须检查）：
   - `<span class="tok-` -- 旧的高亮标签前缀
   - `<span class="kw">` / `<span class="st">` / `<span class="fn">` / `<span class="ty">` / `<span class="cm">` / `<span class="an">` / `<span class="nu">` / `<span class="tag">` -- 任何手动 span 高亮
   - `class="tok-` 出现在 `<pre><code>` 内部
   - 任何未闭合的 `<span` 标签

### 8.2 HTML 实体转义规则

在 `<pre><code>` 块中，以下字符必须转义：
- `<` -> `&lt;`
- `>` -> `&gt;`
- `&` -> `&amp;`

示例 -- XML/POM 代码块：
```html
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.ai&lt;/groupId&gt;
    &lt;artifactId&gt;spring-ai-openai-spring-boot-starter&lt;/artifactId&gt;
&lt;/dependency&gt;</code></pre>
```

### 9. 幂等性检查（防重复生成，2026-08-22 重复评论事故后强化）

- **核心原则：只要某任务已有融合教程，就不再生成、不再评论**（无论 due 是否顺延、无论存放在哪个日期目录、无论在哪个会话/副本生成）。
- **前置动作（必做）**：`git pull --rebase origin main` 同步远程——不同会话的本地副本可能落后于远程，未同步会导致误判"未生成"而重复生成+重复评论（8.22 事故根因）。
- **三信号检查，任一命中即跳过**：
  1. **注册表（权威）**：读取 `.trae/tutorial_registry.json`，按**任务 guid 精确匹配**（guid 全局唯一且稳定，优先于 slug 模糊匹配）。命中即跳过，不生成、不覆盖、不追加评论，记录日志"已有教程（注册表），跳过"。文件不存在视为空注册表（首次运行自动创建）。
  2. **文件扫描**：计算该任务的 slug，扫描 `assignments/` 下**所有日期子目录**，查找是否存在 `<slug>/tutorial.html`。命中即跳过，记录日志"已有教程（文件），跳过"。
  3. **评论状态**：lark-cli task 当前仅有 `+comment` 写入、无评论读取命令（已实测确认，勿猜测子命令）。"是否已评论"以注册表中 `feishu_comment_id` 字段（飞书云盘 URL 评论）为等价记录；旧 `comment_id` 字段为废弃的 raw URL 评论历史值，**不再作为幂等依据**（同一任务允许同时存在旧 raw URL 评论 + 新飞书云盘评论，不再追加新评论以 `feishu_comment_id` 是否存在为准）。
- **slug 匹配优先级**：guid 优先；无 guid 场景（对话中手动触发）先用 summary 的 kebab-case 匹配，再按 summary 关键词模糊匹配已有目录名，视为同一任务。
- **存放路径**：新教程存入 `assignments/<当前due日期>/<slug>/tutorial.html`（用任务当前的 due 日期，不是今天日期）。
- **幂等规则总结**：同一任务（同 guid，或同 slug/summary 关键词兜底）的教程与评论**全局只产生一次**；due 顺延不触发重新生成。

### 10. 任务筛选规则

- 当天 due 的任务：优先处理，存入 `assignments/<当前due日期>/<slug>/tutorial.html`
- 逾期任务（due < TODAY 且未完成）：同样按第 9 节全局扫描判断是否已有教程
  - 任意日期目录下已有该 slug 的 `tutorial.html` -> 跳过
  - 全部没有 -> 生成并存入 `assignments/<当前due日期>/<slug>/tutorial.html`
- 已完成任务：跳过，不生成教程
- **关键变更**：不再因 due 顺延而重新生成教程。一个任务只要生成过一次教程，后续顺延/重新分配 due 时一律跳过。

### 11. Agent 校验环节（生成后必须执行，禁止跳过）

**原则**：每个 `tutorial.html` 生成后，在写入文件之前，必须经过校验。校验不通过则修复后重新校验，最多重试 2 次。仍不通过则记录错误日志，该教程标记为"生成失败"。

**校验流程**（按顺序执行，任一项失败则整体不通过）：

#### 11.1 代码块完整性校验

对文件中所有 `<pre><code>...</code></pre>` 块执行以下检查：

- **无 span 泄漏**：`<pre><code>` 内部不得出现 `<span` 标签。用正则 `<pre><code>[\s\S]*?<\/code><\/pre>` 提取每个代码块，检查内部是否含 `<span`。若含则不通过。
- **无 class 属性泄漏**：代码块内不得出现 `class="tok-`、`class="kw"`、`class="st"`、`class="fn"`、`class="ty"`、`class="cm"`、`class="an"`、`class="nu"`、`class="tag"` 等模式。
- **HTML 实体正确转义**：代码块内的 `<` 必须写作 `&lt;`，`>` 必须写作 `&gt;`（除 `</code></pre>` 闭合标签外）。检查是否存在裸露的 `<` 或 `>` 字符（如 `<dependency>` 应为 `&lt;dependency&gt;`）。
- **标签闭合平衡**：`<pre>` 与 `</pre>` 数量相等，`<code>` 与 `</code>` 数量相等。

#### 11.2 Java 代码语法校验

对代码块中的 Java 代码执行基本语法检查：

- 每个 `{` 都有对应的 `}`。
- 每个 `(` 都有对应的 `)`。
- 字符串引号成对出现（`"` 的数量为偶数）。
- 注释格式正确（`//` 单行注释不跨越代码块边界）。
- `@Annotation` 后跟合法的 Java 标识符或 `(`。

#### 11.3 HTML 结构校验

- `<!DOCTYPE html>` 存在于文件开头。
- `<html>` 和 `</html>` 标签成对。
- `<head>` 和 `</head>` 成对。
- `<body>` 和 `</body>` 成对。
- 所有 `<section>` 或 `<div>` 标签正确闭合。
- CSS 中定义了 `pre code` 的样式（字体、背景色等）。

#### 11.4 内容完整性校验

- Hero 区包含 Phase 标注和任务全称。
- Hero 区包含总预估时长。
- 底部"教程来源"章节存在，且包含至少 5 个 `<li>` 条目。
- 每个来源链接是完整的 URL（以 `http` 开头）。

#### 11.5 校验执行方式

校验通过脚本自动化执行。在生成 tutorial.html 后，运行以下检查命令：

```bash
# 检查 span 泄漏：在 pre/code 块内不应有 span 标签
python3 -c "
import re, sys
html = open(sys.argv[1]).read()
blocks = re.findall(r'<pre><code>([\s\S]*?)</code></pre>', html)
issues = []
for i, block in enumerate(blocks):
    if '<span' in block:
        issues.append(f'代码块{i+1}: 含有 <span> 标签')
    if 'class=\"tok-' in block or 'class=\"kw\"' in block or 'class=\"st\"' in block:
        issues.append(f'代码块{i+1}: 含有语法高亮 class 属性')
    # 检查裸露的 < > (非实体转义)
    stripped = block.replace('&lt;','').replace('&gt;','').replace('&amp;','')
    if '<' in stripped or '>' in stripped:
        issues.append(f'代码块{i+1}: 含有未转义的 < 或 >')
if issues:
    print('校验失败:')
    for issue in issues:
        print(f'  - {issue}')
    sys.exit(1)
else:
    print('代码块校验通过')
" <tutorial.html路径>
```

若校验失败，必须修复后重新校验。修复方式：
- 将所有 `<span class="xxx">内容</span>` 替换为纯文本 `内容`。
- 将代码块内的 `<` 替换为 `&lt;`，`>` 替换为 `&gt;`。
- 确保 `pre code` 的 CSS 样式已定义。

#### 11.6 专有名词解释抽查（第 12 节配套，禁止跳过）

- 读取 `skills/term-whitelist.md` 的「已掌握」组。
- 从教程正文中抽取最多 5 个**非白名单**专有名词，逐一检查其**首次出现处**：
  - 是否带解释（一句话人话解释）；
  - 解释是否含桥接类比（锚定 Java/Spring/MySQL/Redis 等已有知识，或按 Python 入门者深度展开）。
- 任一抽查术语首次出现处无解释或无桥接 -> 校验不通过，按第 12 节规范补写后重新校验。
- 校验通过的同时，确认教程底部「📝 术语表」小节存在且覆盖本篇解释过的非白名单术语。

### 12. 专有名词解释规范（新手友好，硬性要求）

**背景**：用户是 Java 后端转 AI Agent 的新手（8 年 Java/Spring/MySQL/Redis 经验，Python 入门中）。此前教程大量术语未解释、迫使用户自行搜索，违背"专属融合教程"的定位。

**白名单机制**（数据文件：`skills/term-whitelist.md`，随仓库版本化，用户与 agent 均可维护）：
- **已掌握组**：用户明确已懂的术语。不解释无罪，允许降低解释频率；同一篇教程至多给一次轻量提示。
- **待观察组**：教程中解释过、待用户确认掌握的术语。**仍按非白名单对待（必须解释）**，确认掌握后才移入「已掌握」组。
- 流转规则：用户作业 summary 中体现已掌握的术语，每日维护运行时移入「已掌握」组并随仓库提交。

**硬性规则**：
1. **白名单外术语首次出现必须解释，绝无例外**（含「待观察」组）。
2. 解释必须**桥接已有知识**：优先类比 Java/Spring/MySQL/Redis 生态概念，自然融入行文，禁止百科式生硬定义。示例：
   - 好：「Rerank 重排序（类似 MySQL 先用索引粗筛出 100 行，再人工精挑 10 行——粗筛快但糙，精筛慢但准）」
   - 坏：「Rerank：一种重排序技术，用于对检索结果进行重排序。」
3. Python/AI 侧术语按"入门者"深度解释（用户 Python 入门中）；Java 侧概念可直接引用白名单已掌握词。
4. 同一术语同篇只在首次出现时解释，不重复堆叠。
5. 教程底部增设「📝 术语表」小节：汇总本篇解释过的非白名单术语（术语 + 一句话解释），并将这些术语写入 `skills/term-whitelist.md`「待观察」组随仓库提交。

### 13. 框架开箱实现优先与版本标注（2026-09-03 用户要求，硬性规则）

**背景**：用户是应用层工程师，学习目标是"用好框架"，不是造轮子。此前部分教程（如引用防幻觉篇）教授手写实现，增加学习负担。原则：**开箱能做的绝不手写；实在要手写的只讲原理，不教底层逐行实现。**

**硬性规则**：

1. **教程代码主线必须优先展示框架开箱实现**。写代码前先确认 Spring AI / LangChain4j 当前版本是否提供对应能力（如 TokenTextSplitter、RewriteQueryTransformer、QueryAugmenter、ChatMemory、QuestionAnswerAdvisor、Advisor 体系等）。
2. **版本意识与检索**：搜索互联网教程时同步确认 Spring AI / LangChain4j 最新稳定版本，新版本新增的开箱实现优先采用；教程中的示例代码必须标注所依赖的框架与最低版本（如 "Spring AI 1.1+ 提供 QueryAugmenter"）。优先更好用的开箱实现并显著标明版本。
3. **手写实现仅出现在框架无对应能力的环节**，且必须同时满足两个前提：框架确实无开箱实现 + 企业对该功能的实现普遍手写（如引用溯源角标、拒答阈值判断）。出现手写环节时必须明确标注："⚠️ 框架无内置实现，以下为业界通用手写方案"。
4. 手写环节只讲清原理 + 最小可运行示例，**禁止逐行展开底层实现细节**（原理深度是面试口述层的事，不是编码作业层）。
5. **新旧做法对照**：若发现互联网旧教程使用的手写做法在新版本已有开箱替代（典型如自 Spring AI 1.x 起的 Advisor/QueryAugmenter 体系替代早期手写链路），教程需同时给出："✅ 新做法（推荐，开箱）"与"旧做法（了解即可，已被替代）"，避免用户学了已废弃的手写方式。
6. 教程来源中若引用了基于旧版本的教程，在来源条目上注明其版本时效（如 "Spring AI 1.0 时代教程，API 已变更"）。

## 执行步骤

```
0. 【同步远程】git pull --rebase origin main（防本地副本落后导致误判"未生成"）
1. 【全局幂等检查·三信号】读 .trae/tutorial_registry.json 按任务 guid 匹配；
   未命中再计算任务 slug，扫描 assignments/ 下所有日期子目录
   - 任一命中（注册表 OR assignments/*/<slug>/tutorial.html） -> 跳过该任务，
     记录日志"已有教程（注册表/文件），跳过"，不评论
   - 皆未命中 -> 继续
2. 获取飞书任务详情（summary + description）
3. 解析路线图 HTML，确定当前 Phase，提取相关推荐项目和面试题
4. 读取 skills/term-whitelist.md，区分「已掌握/待观察」术语（供第 12 节规范使用）
5. 搜索互联网教程（至少 5 个来源），同步确认 Spring AI / LangChain4j 最新稳定版本及该主题的开箱实现情况（第 13 节）
6. 融合生成 tutorial.html，按上述规范
   - 代码块使用纯文本 <pre><code>，禁止 <span> 高亮标签
   - HTML 实体正确转义（< -> &lt; 等）
   - 白名单外专有名词首次出现必须桥接式解释；底部含「📝 术语表」
   - 代码主线优先框架开箱实现并标注版本；手写仅限"框架无内置且企业普遍手写"环节并加"⚠️"标注（第 13 节）
7. 【Agent 校验】对生成的 HTML 执行第 11 节校验流程（含 11.6 术语解释抽查）
   - 校验通过 -> 继续步骤 8
   - 校验失败 -> 修复问题，重新校验（最多重试 2 次）
   - 仍失败 -> 记录错误日志，标记"生成失败"，跳过该任务
8. 存入 assignments/<due日期>/<slug>/tutorial.html（due日期≠当天时为逾期任务）
9. git add + commit + push 到路线图仓库（保留 git 流程，仓库不可访问时也不阻塞，
   写本地 commit 即可，远程 push 失败仅记录日志，不影响后续步骤 10/11）
10. 【上传飞书云盘·与 GitHub 同构】按 assignments/<due日期>/<slug>/tutorial.html
    的路径，在飞书云盘根目录创建同名层级目录：
    - 用 lark-cli drive +create-folder 逐级创建（assignments → <due日期> → <slug>）；
    - 已存在的目录跳过（可先 lark-cli drive +search --query <目录名> --doc-types folder
      或用 .trae/feishu_drive_cache.json 缓存 folder_token 复用，避免重复创建）
    - 用 lark-cli drive +upload --file <本地 tutorial.html> --name "tutorial.html"
      --folder-token <slug 目录的 folder_token> 上传
    - 返回结果中拿到 file_token 和 url（即 https://my.feishu.cn/file/<file_token>），
      立即写入 .trae/tutorial_registry.json 该 guid 条目：
      feishu_url / feishu_file_token / feishu_folder_path / raw_url_status="unavailable_github_repo_404"
11. 【评论·防重】确认注册表中该任务 guid 无 feishu_comment_id 后，单任务单命令执行
    lark-cli task +comment --task-id <guid> --content
    "📚 专属融合教程已生成（飞书云盘，可点击预览/下载）:
    <feishu_url>
    目录: assignments/<due日期>/<slug>/tutorial.html"
    （禁止 && 批量链；成功取得 comment_id 后写入注册表 feishu_comment_id 字段）
12. 【本地预览·可选，会话内可访问】集中复制今日 N 篇 HTML 到
    /workspace/今日作业教程_<TODAY>/<slug>.html，启动 nohup python3 -m http.server 8765
    & 后用 OpenPreview 工具传 command_id 和 http://localhost:8765/ 给用户；
    会话历史保留在 Trae 自动化执行历史中（以启动时间命名），会话内 URL 可长期访问
13. 将本篇新解释术语写入 skills/term-whitelist.md「待观察」组，随仓库提交
```

## 输出

| 产出 | 位置 |
|------|------|
| tutorial.html（本地） | assignments/YYYY-MM-DD/<slug>/tutorial.html |
| tutorial.html（飞书云盘） | 飞书云盘根 → assignments → YYYY-MM-DD → <slug> → tutorial.html，URL 形如 https://my.feishu.cn/file/<file_token> |
| 飞书任务评论 | 包含飞书云盘 URL，可直接点击预览/在浏览器中打开 |
| 本地预览（会话内） | http://localhost:8765/ 由 OpenPreview 暴露，会话历史保留可回看 |
