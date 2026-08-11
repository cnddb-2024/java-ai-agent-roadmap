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

- 生成后将 GitHub raw URL 写入飞书任务的评论中
- 用户正常路线：飞书任务 → 学习链接 → 生成的专属融合教程
- 不在 HTML 内写 GUID 或"作业二"这类模糊标识
- HTML 顶部标注当前 Phase 和任务全称（与飞书一致）

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

### 9. 幂等性检查（防重复生成）

- **生成前必须检查**：目标路径 `assignments/YYYY-MM-DD/<slug>/tutorial.html` 是否已存在
- **已存在则跳过**：该任务已有融合教程，不重复生成、不覆盖、不追加评论
- **逾期任务处理**：任务 due 日期早于今天（北京时间）且未完成 → 仍视为待处理任务
  - 先检查逾期任务对应日期的目录下是否已有 `tutorial.html`
  - **已有**：跳过该任务，不重复生成
  - **没有**：正常生成，但存入该任务**原始 due 日期**对应的 `assignments/` 目录（而非今天日期）
  - 逾期任务的 `tutorial.html` 存放路径用 **due 日期**，不是当天日期
- **幂等规则总结**：同一任务（同 guid 或同 summary+due 组合）的 `tutorial.html` 只生成一次

### 10. 任务筛选规则

- 当天 due 的任务：优先处理，存入 `assignments/<TODAY>/<slug>/tutorial.html`
- 逾期任务（due < TODAY 且未完成）：检查原始 due 日期目录下是否已有教程
  - 有 -> 跳过
  - 无 -> 生成并存入 `assignments/<原始due日期>/<slug>/tutorial.html`
- 已完成任务：跳过，不生成教程

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

## 执行步骤

```
1. 【幂等检查】检查 assignments/<due日期>/<slug>/tutorial.html 是否已存在
   - 存在 → 跳过该任务，记录日志"已有教程，跳过"
   - 不存在 → 继续
2. 获取飞书任务详情（summary + description）
3. 解析路线图 HTML，确定当前 Phase，提取相关推荐项目和面试题
4. 搜索互联网教程（至少 5 个来源）
5. 融合生成 tutorial.html，按上述规范
   - 代码块使用纯文本 <pre><code>，禁止 <span> 高亮标签
   - HTML 实体正确转义（< -> &lt; 等）
6. 【Agent 校验】对生成的 HTML 执行第 11 节校验流程
   - 校验通过 -> 继续步骤 7
   - 校验失败 -> 修复问题，重新校验（最多重试 2 次）
   - 仍失败 -> 记录错误日志，标记"生成失败"，跳过该任务
7. 存入 assignments/<due日期>/<slug>/tutorial.html（due日期≠当天时为逾期任务）
8. git add + commit + push 到路线图仓库
9. 获取 GitHub raw URL
10. lark-cli task +comment 将 raw URL 写入飞书任务评论
```

## 输出

| 产出 | 位置 |
|------|------|
| tutorial.html | assignments/YYYY-MM-DD/<slug>/tutorial.html |
| 飞书任务评论 | 包含 GitHub raw URL，可直接点击查看 |
