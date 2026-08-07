# 学习指引：RAG 核心概念学习：Embedding/向量检索/Chunking/重排序 原理笔记

> 来源：飞书任务，任务日期 2026-08-06（已标记完成但未提交作业，补充提交）
> 飞书任务 GUID：53707db7-8956-4530-aacd-359c9284a9bb

## 学习目标

掌握 RAG（Retrieval-Augmented Generation）的核心原理与四大关键环节，理解企业级 AI 知识库的架构基础。

## 知识点

- **Embedding 原理**：文本向量化、离线阶段 chunk 分割与向量存储、余弦相似度语义判断
- **向量检索**：query 向量化、与向量数据库内切片的余弦相似度计算、粗排检索
- **重排序（Reranking）**：精排筛选、score 模型应用、去除看似相关实则无关的数据
- **生成**：切片 + 用户问题传入 LLM、引用资料回答、不相关则不回答
- **RAG 核心价值**：知识热更新（直接向量化入库）、错误可追溯（定位到 chunk 元数据）

## 学习资源

- RAG 概念综述：https://research.ibm.com/blog/retrieval-augmented-generation-RAG
- Embedding 原理详解：https://platform.openai.com/docs/guides/embeddings
- 向量检索与重排序：https://qdrant.tech/documentation/
- 作业项目仓库：https://github.com/cnddb-2024/spring-ai-quickstart.git

## 验收标准

- 理解 Embedding 将文字转化为高维向量的原理
- 掌握向量检索中余弦相似度判断语义相关性的机制
- 理解粗排（向量检索）与精排（重排序）的两阶段流程
- 能解释 RAG 作为企业 AI 知识库最佳实践的两个核心原因

## 相关面试题

- RAG 的完整流程是什么？每个阶段的作用？（第一梯队）
- 向量检索为什么需要重排序？粗排和精排的区别？（第一梯队）
- RAG 相比直接微调 LLM 的优势是什么？（第二梯队）
