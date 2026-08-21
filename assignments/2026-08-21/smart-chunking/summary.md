# 智能切分实战

## 作业信息

- **日期**: 2026-08-21
- **Phase**: Phase 1（第 24/168 天）
- **对应飞书任务**: 智能切分实战：TokenTextSplitter / 递归字符切分 / 按标题多粒度切分对比
- **代码仓库**: [cnddb-2024/spring-ai-quickstart](https://github.com/cnddb-2024/spring-ai-quickstart)
- **提交**: `bb2cd2c` - advisor和rag基础搭建（RagIngestionService）

## 作业内容

### 1. TokenTextSplitter 实现（Spring AI 内置）

```java
TokenTextSplitter splitter = new TokenTextSplitter(
    800,   // maxChars（每块最大字符数）
    200,   // minChunkSizeChars（每块最小）
    100,   // minLengthChars（重叠大小）
    10000, // maxTokenCount（单文档最大 token）
    true,  // keepSeparator（保留分隔符）
    punctuationMarks // 分隔符列表：. , ? ! ; : " '
);
```

### 2. 参数调优理解

| 参数 | 值 | 作用 | 面试点 |
|------|-----|------|--------|
| maxChars | 800 | 每块最大字符数 | 太大：上下文散、检索精度低；太小：语义不完整 |
| minChunkSizeChars | 200 | 每块最小字符数 | 避免出现过短的碎片 chunk |
| minLengthChars（重叠） | 100 | 相邻块重叠字符数 | 防止语义在切分点被切断，提升召回连续性 |
| keepSeparator | true | 保留分隔符 | 保留标点符号，保持句子完整性 |
| 分隔符列表 | 标点符号 | 优先在句子边界切分 | 而不是在词中间切开 |

### 3. RAG 链路集成

- `RagIngestionService.initIngestDocuments()`：批量入库，TokenTextSplitter 处理 Tika 读取的文档
- `RagIngestionService.ingest(Resource)`：单文件增量入库，默认 TokenTextSplitter（默认参数）
- 流程：TikaDocumentReader → TokenTextSplitter → VectorStore.add()（自动 Embedding + 存储）

### 4. 覆盖知识点

- Spring AI `TokenTextSplitter` 核心参数调优
- 切分粒度对检索质量的影响（chunk size 与召回率/精度的权衡）
- 重叠（overlap）的作用与设计原理
- 句子边界切分 vs 固定长度切分
- RAG  ingestion 全链路：加载 → 切分 → 向量化 → 存储

## 面试题关联

- RAG 中 chunk size 设多少合适？太大或太小分别有什么问题？（第一梯队）
- 什么是 overlap（重叠）？为什么需要重叠？设多少合适？（第一梯队）
- TokenTextSplitter 和 RecursiveCharacterTextSplitter 有什么区别？适用场景？（第一梯队）
- 结构化文档（有标题层级）如何做"按标题多粒度切分"？相比固定大小切分优势在哪？（第二梯队）
