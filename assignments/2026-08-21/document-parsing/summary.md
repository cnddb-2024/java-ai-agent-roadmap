# 文档解析实战

## 作业信息

- **日期**: 2026-08-21
- **Phase**: Phase 1（第 24/168 天）
- **对应飞书任务**: 文档解析实战：Apache PDFBox + Apache POI 抽取 PDF/Word/Markdown 纯文本与表格
- **代码仓库**: [cnddb-2024/spring-ai-quickstart](https://github.com/cnddb-2024/spring-ai-quickstart)
- **提交**: `7430f82` - 文档解析器

## 作业内容

### 1. 解析器架构

```
utils/
├── DocumentParser.java     # 统一入口：按扩展名分发（PDF/DOCX/MD）
├── ExtractPdfUtil.java     # PDFBox 抽取纯文本
└── ExtractDocxUtil.java    # POI 抽取段落 + 表格（表格转 Markdown）
```

### 2. 核心实现要点

| 模块 | 技术 | 关键点 |
|------|------|--------|
| `DocumentParser` | 策略模式 | `switch` 按扩展名分发，返回 `ParsedDocument(source, text)` record |
| `ExtractPdfUtil` | Apache PDFBox | `PDFTextStripper.setSortByPosition(true)` 按物理位置排序，避免列混乱 |
| `ExtractDocxUtil` | Apache POI | 遍历 `BodyElement`，区分 PARAGRAPH / TABLE；段落追加双换行 |
| 表格转 Markdown | POI XWPFTable | 逐行逐单元格拼接 `| cell |`，首行后加 `|---|` 分隔线；`\n` 转空格、`\|` 转义 |

### 3. 设计亮点

- **表格转 Markdown**：注释明确说明了动机——"行列结构对检索和 LLM 都是最友好的形态，单元格文本完整、语义紧凑，比线性化成一串句子召回质量高得多"。这是 RAG 文档解析的关键决策，面试能讲清楚 why 加分很多
- **格式扩展性**：DocumentParser 的 switch 分发模式易于后续新增 PPT/Excel 等格式
- **record 返回值**：Java 17+ record 封装解析结果，不可变且语义清晰

### 4. 覆盖知识点

- Apache PDFBox 文本抽取（`PDFTextStripper`、按位置排序）
- Apache POI XWPF 文档解析（段落、表格遍历）
- Markdown 表格格式化与转义
- 策略模式 + 工具类静态方法
- 多格式统一入口封装

## 面试题关联

- RAG 中为什么要把表格转成 Markdown 而不是直接提取文本？对检索质量有什么影响？（第一梯队）
- PDF 解析有哪些常见坑？列布局、页眉页脚、图片中的文字如何处理？（第二梯队）
- 不同文档格式（PDF/Word/Markdown/HTML）的解析策略有何差异？（第二梯队）
