# Spring AI Advisors 机制实战

## 作业信息

- **日期**: 2026-08-12
- **Phase**: Phase 1（第 15/168 天）
- **对应飞书任务**: Spring AI Advisors 机制实战：RequestResponseAdvisor/链式编排/日志拦截
- **代码仓库**: [cnddb-2024/spring-ai-quickstart](https://github.com/cnddb-2024/spring-ai-quickstart)
- **提交**: `bb2cd2c` - advisor和rag基础搭建

## 作业内容

### 1. 三个自定义 CallAdvisor

| Advisor | Order | 职责 | 核心机制 |
|---------|-------|------|----------|
| `LoggingAdvisor` | HIGHEST_PRECEDENCE（最外层） | 请求/响应日志 + 耗时统计 | 前置记录 userText/model，后置记录 cost/content |
| `SensitiveWordAdvisor` | HIGHEST_PRECEDENCE+5 | 敏感词拦截护栏 | 命中后阻断 `chain.nextCall`，直接构造 ChatClientResponse 返回 |
| `TokenCountAdvisor` | HIGHEST_PRECEDENCE+10 | Token 用量估算 | 通过 `request.mutate().context()` 向下游传递，`response.mutate().context()` 回写 |

### 2. 链式编排要点

- **顺序由 `getOrder()` 决定**，而非 `defaultAdvisors()` 的添加顺序
- `ChatClientRequest` / `ChatClientResponse` 均不可变，修改 context 必须通过 `mutate().build()`
- 敏感词 Advisor 命中时不调用 `chain.nextCall()`，实现短路拦截
- 内置 `QuestionAnswerAdvisor`（order=10）与自定义 Advisor 混合编排

### 3. RAG 基础链路（同步完成）

- `RagIngestionService`：TikaDocumentReader 读取文档 → TokenTextSplitter 切分（800/200/100）→ VectorStore 写入
- `ChatController` 三个 RAG 端点：
  - `/chat/rag`：基础 QuestionAnswerAdvisor（threshold=0.5, topK=5）
  - `/chat/advanceRag`：动态元数据过滤（`type == 'spring-ai'`）
  - `/chat/rag/init`：触发文档入库

### 4. 覆盖知识点

- `CallAdvisor` 接口实现（请求前/响应后/短路）
- `AdvisorChain` 责任链模式
- `ChatClientRequest.context()` 跨 Advisor 状态传递
- `Ordered.getOrder()` 执行顺序控制
- `QuestionAnswerAdvisor` 向量检索增强
- `TokenTextSplitter` 参数调优（chunkSize/minChunkSize/overlap）

## 面试题关联

- Spring AI 的 Advisor 机制与 Spring MVC Interceptor / Servlet Filter 有何异同？（第一梯队）
- 如何在 RAG 链路中实现护栏（Guardrail）？敏感词拦截放在哪一层？（第一梯队）
- Advisor 之间如何传递状态？为什么 ChatClientRequest 设计为不可变？（第二梯队）
