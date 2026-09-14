# 专有名词白名单（融合教程术语解释控制表）

> 配套 `skills/tutorial-fusion.md` 第 12 节使用。随仓库版本化，用户与 agent 均可维护。
> 最后更新：2026-08-27

## 使用规则

1. **已掌握组**：用户明确已懂的术语。生成教程时**不强制解释**（不解释无罪），允许降低解释频率；同一篇教程至多给一次轻量提示。
2. **待观察组**：教程中解释过、待用户确认掌握的术语。**仍按非白名单对待——首次出现必须解释**。
3. **白名单外**（两组皆不在）：首次出现**必须解释，绝无例外**，且必须与已有知识桥接（类比 Java/Spring/MySQL/Redis 生态），自然融入行文，禁止百科式生硬定义。
4. **流转规则**：用户作业 summary 中体现已掌握的「待观察」术语，每日维护运行时移入「已掌握」组并随仓库提交；每篇教程新解释的术语自动进入「待观察」组。
5. 用户背景锚点：8 年 Java 后端（Spring/MySQL/Redis 熟练），Python 入门中，AI Agent 领域新手。

## 已掌握（无需每次解释）

### 后端基础（职业背景，直接使用）

Java, Spring Boot, Spring MVC, Spring 全家桶常见注解（@Autowired/@Service/@Controller 等）, MyBatis, MySQL, Redis, Maven, Gradle, Git, GitHub, RESTful API, JSON, HTTP/HTTPS, MVC, Bean, 依赖注入（DI/IoC）, AOP, 连接池, 索引, 事务, CRUD, JDBC, 单元测试（JUnit/Mockito）, 日志（SLF4J/Logback）, Linux 基础命令, Docker 基础, 面向对象（封装/继承/多态）, 设计模式（单例/工厂/策略等常见）

### AI/LLM 侧（已完成对应作业，2026-07-31 ~ 2026-08-22）

大语言模型（LLM）, Prompt（提示词）, Token, API Key, 流式输出（SSE）, RAG 基本概念（检索增强生成）, Function Calling / Tool Calling（函数调用/工具调用）, LangChain4j 基础（AiServices/@Tool）, Spring AI 基础（ChatClient/ChatModel）, Spring AI Advisor, Spring AI 可观测性（Micrometer/Actuator）, 文档解析（PDFBox/POI/Spring AI ETL）, 文本切分（Chunking/智能切分）, Embedding 基础与选型, 向量数据库基础概念, pgvector 基础, Ollama 本地部署, Python 基础语法/数据结构/OOP/模块包（入门级已练）

## 待观察（解释过或即将学到，仍必须解释）

BM25, RRF（倒数排序融合）, 混合检索, Rerank（重排序）, 上下文组装, Token 预算控制, Lost-in-the-Middle, 引用溯源, Faithfulness（忠实度）, 幻觉/防幻觉, Recall@K, nDCG, LLM-as-Judge, RAG 评测, Milvus, Qdrant, Elasticsearch, tsvector, 全文检索, 向量相似度（余弦/欧氏）, 温度参数（Temperature）, 微调（Fine-tuning）, Agent, ReAct, MCP, 多模态, 知识库问答, 技术决策日志（ADR）, Bi-Encoder（双编码器）, Cross-Encoder（交叉编码器）, ScoringModel（评分模型）, ReRankingContentAggregator（重排序内容聚合器）, relevance_score（相关性分数）, ONNX Runtime, QueryAugmenter（查询增强器）, ContextualQueryAugmenter, ContentInjector（内容注入器）, ContentAggregator（内容聚合器）, CompressionQueryTransformer（查询压缩器）, OpenAI 兼容接口, requests/Session（Python HTTP 客户端）, iter_lines, 瞬时错误/永久错误, 指数退避（backoff）, jitter（抖动）, tenacity, 金标集（golden set）, MRR, 分级相关性, RAGAS, Answer Relevancy, Context Precision/Recall, 自一致性（self-consistency）, A/B 对比实验, 结构化输出, 原子陈述（Atomic Statements）, 拒答（Refusal）, 阈值切点, Grounding（接地/依据约束）, DDD 分层, Maven 多模块, CI 门禁（Quality Gate）, Testcontainers, Profile 分层配置, DataFrame, Series, NaN 缺失值, 向量化（Vectorization）, split-apply-combine, transform（广播聚合）, pivot_table（数据透视表）, Simple/MADR 模板, 成本红线（Cost Threshold）, P95 延迟, 加权决策矩阵, 撤销条件

## 维护记录

- 2026-08-22：初始版本。后端基础按职业背景录入；AI 侧按 07-31~08-22 已完成作业录入；待观察组为 Phase1 剩余任务及 Phase2 预计涉及术语。
- 2026-08-23：新增 Rerank / 上下文组装两篇教程解释的 12 个术语至待观察组（Bi-Encoder、Cross-Encoder、ScoringModel、ReRankingContentAggregator、relevance_score、ONNX Runtime、QueryAugmenter、ContextualQueryAugmenter、ContentInjector、ContentAggregator、CompressionQueryTransformer 等）。
- 2026-08-27：新增当日三篇教程解释的 20 个术语至待观察组。引用与防幻觉篇：结构化输出、原子陈述、拒答、阈值切点、Grounding；RAG 评测篇：金标集、MRR、分级相关性、RAGAS、Answer Relevancy、Context Precision/Recall、自一致性、A/B 对比实验；Python requests 篇：OpenAI 兼容接口、requests/Session、iter_lines、瞬时错误/永久错误、指数退避、jitter、tenacity。
- 2026-09-15：新增当日三篇教程解释的 17 个术语至待观察组。生产级工程化篇：DDD 分层、Maven 多模块、CI 门禁、Testcontainers、Profile 分层配置；pandas 篇：DataFrame、Series、NaN 缺失值、向量化、split-apply-combine、transform、pivot_table；Rerank 决策日志篇：Simple/MADR 模板、成本红线、P95 延迟、加权决策矩阵、撤销条件。
