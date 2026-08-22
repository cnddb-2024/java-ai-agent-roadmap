# Embedding 模型选型与接入实战

## 作业信息

- **日期**: 2026-08-22
- **Phase**: Phase 1（第 25/168 天）
- **对应飞书任务**: Embedding 模型选型与接入实战：bge-large-zh / text-embedding-3 / m3e 对比 + Spring AI 接入
- **代码仓库**: [cnddb-2024/spring-ai-quickstart](https://github.com/cnddb-2024/spring-ai-quickstart)
- **提交**:
  - `91296d0` - 准备 3 份真实文档 + 一键跑出 A/B 的 Recall@5 对比
  - `3929617` - rag初始化，使用ollama向量模型

---

## 一、接入实现

### 技术选型：Ollama 本地向量模型（禁用云端 API）

`pom.xml` 关键变化——启用 Ollama starter、注释掉 OpenAI starter：

```xml
<!-- 使用本地 Ollama 向量模型（部署成本低） -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-ollama</artifactId>
</dependency>

<!-- 云端 OpenAI（已注释，需付 API 费用） -->
<!--<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>-->
```

### Embedding Model 装配（ChatClientConfig）

```java
@Bean
@Primary
public EmbeddingModel primaryEmbeddingModel(@Qualifier("ollamaEmbeddingModel") EmbeddingModel ollamaEmbeddingModel) {
    return ollamaEmbeddingModel;
}
```

- 通过 `@Qualifier("ollamaEmbeddingModel")` 注入 Spring AI 自动装配的 Ollama 本地 embedding 模型
- `@Primary` 确保 graph 全局使用本地 embedding，而非云端
- 搭配 Qdrant 向量库 + `spring-ai-starter-vector-store-qdrant`

### 向量化入库链路（RagIngestionService）

- 资源加载：`PathMatchingResourcePatternResolver` 读取 classpath 下全部文档（简历 PDF / 技术方案 docx / Markdown 手册）
- 文档解析：`DocumentParser.parse(filename, is)` 新增流式重载，按扩展名分发 PDF(PDFBox)/DOCX(POI markdown 表格)/MD
- 切分：`TokenTextSplitter(800/200/100)` 按约 800 字符 + 100 重叠
- 向量化 + 存储：`vectorStore.add(chunks)`，Embedding 由 Ollama 本地模型自动完成

### A/B 评测（RetrievalEvalTest）

配合 3 份真实文档 + 一批检索问题，一键跑出不同 embedding 模型的 Recall@5 对比，为选型提供数字依据。

---

## 二、选型四步法（面试话术）

对应「RAG 完整链路 + Chunking 策略」的 Embedding 选型追问，强调"换模型要全量重建向量库"的迁移成本意识。

> 主要考虑四步：
>
> 1. **中文评测**：看中文评测体系下的检索和语义相似度得分，中文场景必须看中文跑分
> 2. **维度/存储成本**：不同维度会影响 HNSW 索引内存占用
> 3. **上下文长度**：切分块 chunk 的 token 大小要跟随向量模型支持的上下文长度走。bge-m3 支持 8192 token，bge-large-zh-v1.5 只有 512 token
> 4. **部署成本**：OpenAI text-embedding-3 这类要付 API 费用，本地部署则不需要
>
> 向量模型选型决策非常重要，因为**换模型涉及全量重建向量库**。

---

## 三、混合检索对向量质量的要求（面试话术）

对应「混合检索 + Rerank」追问向量质量：

> 混合检索指的是稠密检索和稀疏检索。**稠密向量对精确的东西查询定位很弱，它只管语义**；而稀疏可以精确匹配一个字都不差。这就需要给稠密向量搭配 BM25 稀疏检索（算法）的原因。而 **bge-m3 原生支持双模**（稠密 + 稀疏），可以减少一路模型。

---

## 四、维度降维（MRL，面试话术）

> 维度降维指优化向量的存储成本和计算成本。text-embedding-3 这类 **MRL（Matryoshka Representation Learning）模型可以智能截断**。MRL 是一种让模型主动学习向量如何有效截断的技术，它把向量语义中最重要信息集中到低维，高维放补充信息和细节，**前 N 维已是一个高质量语义表达**。降维可有效在性能与效率间找平衡。
>
> **对比**：
> - MRL 模型是智能截断、传统模型是粗暴截断
> - MRL 模型降维后仍保留不错语义、传统模型直接丢失大量有效信息
> - 原因：MRL 对前缀低维向量进行优化，传统模型未做优化训练
>
> **如何降维**（通过 dimensions 参数）三个场景：
> 1. 数据库只支持 1024 → 把 text-embedding-3 降到 1024
> 2. 极致性价比 → 尝试降到 512 或 256
> 3. 优化 → 先用全量维度测试，再逐步降低维度，寻找最佳平衡点

---

## 五、量化结果话术

呼应路线图验收标准「RAG 评测三层指标」，用数字说服面试官：

> 对这两个模型的选型，我们用 20 道中文评测题，Recall@5 分别得到 X% 与 Y%，最终 bge 获胜；同时本地部署成本还低，节省 API 成本 Z 元。

> **注意**：X%、Y%、Z 为占位，pending 用 `RetrievalEvalTest` 跑出真实数字后填入，面试说单时必须有真实可讲的数字。

---

## 面试题关联

- Embedding 模型选型四要素（中文评测/维度/上下文长度/部署成本）？（第一梯队）
- 换 embedding 模型为什么要全量重建向量库？（第一梯队）
- 稠密向量与稀疏向量（BM25）各自的弱点与互补点？（第一梯队）
- Matryoshka 降维的原理与三种降维场景？（第二梯队）

---

## 教程来源

- [Embedding 模型选型与接入实战 融合教程](./tutorial.html)