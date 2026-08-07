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
- 代码块带语法高亮颜色标注
- 底部含"教程来源"章节，使用 `<ol>` 有序列表

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
  - 有 → 跳过
  - 无 → 生成并存入 `assignments/<原始due日期>/<slug>/tutorial.html`
- 已完成任务：跳过，不生成教程

## 执行步骤

```
1. 【幂等检查】检查 assignments/<due日期>/<slug>/tutorial.html 是否已存在
   - 存在 → 跳过该任务，记录日志"已有教程，跳过"
   - 不存在 → 继续
2. 获取飞书任务详情（summary + description）
3. 解析路线图 HTML，确定当前 Phase，提取相关推荐项目和面试题
4. 搜索互联网教程（至少 5 个来源）
5. 融合生成 tutorial.html，按上述规范
6. 存入 assignments/<due日期>/<slug>/tutorial.html（due日期≠当天时为逾期任务）
7. git add + commit + push 到路线图仓库
8. 获取 GitHub raw URL
9. lark-cli task +comment 将 raw URL 写入飞书任务评论
```

## 输出

| 产出 | 位置 |
|------|------|
| tutorial.html | assignments/YYYY-MM-DD/<slug>/tutorial.html |
| 飞书任务评论 | 包含 GitHub raw URL，可直接点击查看 |
