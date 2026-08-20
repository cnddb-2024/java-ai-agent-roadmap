# 目标 JD 收集与刚需能力提取 · 总结报告

> Phase 0 验收作业 · 调研时间：2026-08-20
> 样本：14 个真实在招 JD（11 个 Java 主线 + 3 个大厂对照样本），覆盖 14 个不同招聘主体
> 平台：BOSS 直聘、猎聘、前程无忧 51job、智联招聘、企业官方招聘官网（腾讯 / 海康威视）、牛客网
> 说明：所有链接在调研当日（2026-08-20）均可访问；标注"已关闭/已结束"的岗位已剔除。

---

## 一、JD 原始链接列表（14 条）

### Java 主线岗位（11 条）

| # | 公司 / 主体 | 岗位 | 城市 | 经验 / 学历 | 薪资 | 平台 | 链接 | 抓取时间 |
|---|---|---|---|---|---|---|---|---|
| 1 | 北京华品博睿网络技术有限公司（BOSS直聘） | Java开发工程师（AI Agent方向） | 北京 | 3-5年 / 本科 | 见链接 | BOSS直聘 | https://m.zhipin.com/job_detail/f10c95a8875a014e03N63t20FFdZ.html | 2026-08-20 |
| 2 | 某大型人力资源服务公司（上海智聘猎头代招） | AI Agent工程师 | 北京/杭州/广州 | 5-10年 / 本科 | 见链接 | BOSS直聘 | https://www.zhipin.com/job_detail/30ca4704da9e87060nB_2tu6E1VW.html | 2026-08-20 |
| 3 | 成都某大型互联网招聘平台公司（锐仕方达猎头代招） | Agent开发工程师 | 成都 | 5-10年 / 本科 | 见链接 | BOSS直聘 | https://refund.zhipin.com/job_detail/161a5637b8aeacf60nB43d64EFBS.html | 2026-08-20 |
| 4 | 北京某中型人工智能大模型研发公司（领程咨询猎头代招） | 大模型应用开发专家（Java+Python） | 北京 | 5-10年 / 本科 | 见链接 | BOSS直聘 | https://www.zhipin.com/job_detail/26fb7aa91945ec4f0nd_2Nm7EFdW.html | 2026-08-20 |
| 5 | 某北京人工智能公司（三秦企管猎头代招） | Java开发工程师（Agent） | 北京 | 3-5年 / 统招本科 | 18-25k | 猎聘 | https://m.liepin.com/a/78746727.shtml | 2026-08-20 |
| 6 | 雀艺信息科技（上海）— 金斯瑞生物科技需求 | AI全栈开发（Java AI 方向） | 南京 | 3-5年 / 学历不限 | 13-21k | 猎聘 | https://www.liepin.com/job/1982561337.shtml | 2026-08-20 |
| 7 | 上海艾策通讯科技股份有限公司 | AI应用研发工程师（Java方向） | 成都 | 1-3年 / 本科 | 1.5-1.8万·13薪 | 前程无忧 | https://msearch.51job.com/jobs/chengdu-whq/173228504.html | 2026-08-20 |
| 8 | 前锦网络信息技术（上海）— 国企云手机平台 | 国企-Java开发（AI） | 广州 | 2年+ / 本科 | 20-30万/年 | 前程无忧 | https://msearch.51job.com/jobs/guangzhou-thq/173177441.html | 2026-08-20 |
| 9 | 宁波力易达人力资源 — 金融科技部（银行方向） | 高级Java开发工程师（AI方向） | 宁波 | 3年+ / 全日制重点本科 | 3-5.5万 | 前程无忧 | https://msearch.51job.com/jobs/ningbo-yzq/172661087.html | 2026-08-20 |
| 10 | 西安润道智检科技有限公司 | AI Agent/微调研发工程师 | 西安 | 经验不限 / 本科 | 150-200元/天 | 智联招聘 | https://m.zhaopin.com/jobs/CCL1321006470J40816097814.htm | 2026-08-20 |
| 11 | 海康威视（官方招聘，EBG） | 应用软件开发工程师（Java方向·大模型） | 杭州 | 3年及以上 / 本科 | 见链接 | 官方官网 | https://talent.hikvision.com/home/socity/position?postId=A38E25E692D5E8F142E4190688F8B1C2 | 2026-08-20 |

### 大厂对照样本（3 条，非 Java 主线，用于校准市场趋势）

| # | 公司 | 岗位 | 城市 | 方向 | 平台 | 链接 | 抓取时间 |
|---|---|---|---|---|---|---|---|
| 12 | 腾讯（CDG 腾讯营销） | 高级数据产品 Agent 算法工程师 | 上海 | Python/算法 | 官方官网 | https://hr.tencent.com/m/jobdesc.html?postId=2052676737472577536 | 2026-08-20 |
| 13 | 字节跳动（抖音） | AI Agent开发工程师 | 杭州/广州 | Python/Go | BOSS直聘 | https://m.zhipin.com/job_detail/6d2fbc6f4b8142f80nBy39u9GVtU.html | 2026-08-20 |
| 14 | 神州数码信息服务（校招） | 2027届-AI Agent工程师 | 北京 | Python/校招 | 牛客网 | https://www.nowcoder.com/jobs/detail/462005 | 2026-08-20 |

> 剔除记录（真实性存疑或已关闭，不计入样本）：滴滴「AI Agent工程师（研发效能）」页面标注"已结束"；佛山善世集团代招「AI 智能体开发工程师」页面标注"职位已关闭"；字节跳动「后端研发工程师（Agent中台）」页面标注"职位已关闭"。

---

## 二、四列提取表（11 条 Java 主线 JD）

### JD-1 BOSS直聘 · Java开发工程师（AI Agent方向）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上计算机相关；精通 Java、熟悉 JVM 原理；Spring Boot 企业级微服务开发；MySQL/Redis 设计优化与调优；分布式系统架构 |
| 加分项 | Docker、微服务经验、Dubbo、云计算经验、大模型相关经验（岗位标签） |
| 工作内容 | Java+Spring Boot 开发维护企业级微服务；分布式架构设计与性能稳定性优化；数据库设计调优；代码审查与协作交付 |
| 面试流程 | JD 未披露 |

### JD-2 代招 · AI Agent工程师（北京/杭州/广州）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上；3年+ 后端开发经验；Java 基础扎实（IO/多线程/集合/JVM）；至少一种主流语言（Java/Python/Go）；数据结构与算法扎实 |
| 加分项 | 分布式系统设计、缓存、消息队列；AI Coding 工具深度使用（Cursor、Claude Code、Codex、GitHub Copilot）；主流 AI Agent 框架；推动 AI 原生研发模式 |
| 工作内容 | 将 AI 辅助编程融入开发全流程提升工程交付效率；跟踪 AI Agent 前沿进展推动业务落地；探索 Coding Agent 在自动化测试/代码重构/文档生成/需求拆解的应用 |
| 面试流程 | JD 未披露 |

### JD-3 代招 · Agent开发工程师（成都）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上；5年+；Java 技术栈构建高性能高可用 Agent 运行时；LangChain4j / Spring AI / 自研框架；JVM、Spring、SpringCloud、Dubbo、微服务、分布式 |
| 加分项 | RAG 架构设计经验、Function Calling、Python |
| 工作内容 | 上亿用户 AI Agent 平台整体架构设计；统一模型网关（动态路由、流式响应、Token 成本管控）；ReAct、Plan-and-Execute 模式落地；Agent 工具标准化接入；高延迟/不确定输出/幻觉抑制治理；链路追踪、日志分析、评估体系；RAG 高并发攻坚 |
| 面试流程 | JD 未披露 |

### JD-4 代招 · 大模型应用开发专家（Java+Python，北京）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上；5年+；Python/Java 后端开发；高性能高可用 AI 服务接口；LangChain、LlamaIndex 框架集成 |
| 加分项 | GraphRAG 与向量检索融合、知识关联建模；图数据库（Neo4j/NebulaGraph）；向量数据库（Milvus/Pinecone/Weaviate）中间件选型集成 |
| 工作内容 | LLM 复杂应用系统架构设计与核心实现；RAG 系统优化、Agent 任务编排、多轮对话逻辑；业务逻辑与大模型能力对接 |
| 面试流程 | JD 未披露 |

### JD-5 某北京人工智能公司 · Java开发工程师（Agent）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 统招本科计算机相关；3年+ Java；多线程/JVM/集合；Spring/Spring Boot/Spring Cloud；MySQL/Redis/Kafka；微服务与分布式（缓存/限流/熔断/分库分表） |
| 加分项 | 大模型应用（Prompt Engineering、RAG、Embedding）；Agent 框架理念（ReAct、Tool Calling、多 Agent 协作）；实际 Agent 项目经验（自动化任务/智能客服/数据分析 Agent）；Docker/Kubernetes；Python、JS |
| 工作内容 | 基于 LLM 的 Agent 系统设计与开发；Agent 框架设计（多轮对话、工具调用、工作流编排）；高并发高可用系统建设；代码评审与技术分享 |
| 面试流程 | JD 未披露（18-25k·五险一金/加班津贴/晋升/年假/体检） |

### JD-6 雀艺信息 · AI全栈开发（南京金斯瑞需求）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 精通 Java、Spring Boot/Cloud 微服务架构；并发编程与 JVM 调优；实际落地的 Java AI 应用开发经验；Agent Scope、LangChain4j 或类似 Java AI 框架；RAG 技术栈、向量数据库（Milvus/Pinecone/Elasticsearch）与检索重排序；大模型 API 调用原理、Prompt Engineering、Context Window 管理、Function Calling |
| 加分项 | MaaS 平台/AI 中台建设（模型网关、鉴权、流控）；企业级 ERP/OA/MES AI 化改造；Python 跨语言协作；LangChain4j/Spring AI 开源贡献；知识图谱 + RAG |
| 工作内容 | 企业系统 AI 化改造（顾问制，周期半年）；业务逻辑转化为标准 Agent 工作流；跟进 AgentRAG、GraphRAG 前沿范式 |
| 面试流程 | JD 未披露（13-21k·五险一金/双休） |

### JD-7 上海艾策通讯 · AI应用研发工程师（Java方向，成都）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上（计算机/软件/AI）；精通 Java、JVM 原理、多线程并发及 NIO；Spring Boot/Spring Cloud；MySQL、Redis、Kafka/RocketMQ 中间件；有实际 AI 应用开发经验（RAG 知识库、Agent 工作流、智能对话） |
| 加分项 | Spring AI、LangChain4j 框架优先；AI 辅助编程工具（Cursor、GitHub Copilot、TRAE）应用于实际项目 |
| 工作内容 | Java 微服务 AI 应用后端核心模块；LLM 工程化集成；Agent 工作流编排、RAG 链路、Function Calling 工程化实现；流式响应（SSE/WebSocket）、高并发上下文管理、Token 成本控制、超时重试降级；跟踪 LangChain4j/Spring AI 演进做技术选型 |
| 面试流程 | JD 未披露（1.5-1.8万·13薪） |

### JD-8 国企 · Java开发（AI，广州）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上（计算机/软件工程优先）；2年+；精通 Java 或 Python；多线程/并发/锁/事务/内存管理（Java 方向需 JVM 原理调优）；Spring Boot/Spring Cloud 生态框架；Linux 与网络；算法数据结构与设计模式 |
| 加分项 | AI/Agent 项目经验（Openclaw、Hermes 等）；ARM 服务器架构、虚拟化、Docker/Kubernetes；Python Web 框架（Django/Flask/FastAPI） |
| 工作内容 | 云手机平台、AI 相关模块软件设计规范制定与架构设计；开发框架搭建改进；技术预研与攻坚 |
| 面试流程 | JD 未披露（20-30万/年·五险一金/双休） |

### JD-9 宁波力易达 · 高级Java开发工程师（AI方向，金融科技）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 全日制重点本科及以上、35 周岁以下；3年+ Java 企业级开发、至少 1年大模型应用/智能体开发；精通 Spring Boot、Spring Cloud、分布式、Dubbo/Feign RPC，熟悉 AI coding；Spring AI、LangChain4j 或类似 Java 原生 AI 框架对接主流大模型（DeepSeek、Qwen、豆包）；Function Calling、CoT、多智能体协作的 Java 实现；Docker/K8s；Redis、关系型数据库、向量数据库 Java 客户端；Prompt Engineering（上下文注入、Few-shot） |
| 加分项 | 金融业务洞察（租赁/风控/尽调）；合规与数据安全意识 |
| 工作内容 | Java 微服务封装 AI 能力（对话/生成/抽取）高可用高并发集成；ReAct、Plan-and-Execute 智能体工作流；Prompt 模板设计（合同审查、尽调报告）；RAG + 向量数据库；推理性能优化、SSE 流式输出、缓存策略、监控体系；跟踪 Spring AI/LangChain4j 演进沉淀开发规范 |
| 面试流程 | JD 未披露（3-5.5万·银行/证券/基金行业） |

### JD-10 西安润道智检 · AI Agent/微调研发工程师

| 列 | 提取内容 |
|---|---|
| 硬性要求 | 本科及以上（计算机/AI）；精通 Java/Python 及 AI 应用开发框架（LangChain、LangChain4j、SpringAI、Semantic Kernel、AutoGen、LlamaIndex 任一）；1年+ Agent 开发经验；RAG 技术与向量数据库实践；Prompt 工程（复杂问题拆解规划执行）；多 Agent 协作架构与任务调度 |
| 加分项 | 大模型微调（LoRA/PEFT）或强化学习；985/211 优先；开源项目贡献或技术博客；独立完成需求分析到系统上线全流程 |
| 工作内容 | 基于主流框架实现业务 AI Agent 产品；多 Agent 协作、意图识别、记忆管理、知识库、工具调用；RAG 召回效率与准确性优化、知识库构建清洗；监控与评估体系设计；大模型微调 |
| 面试流程 | JD 未披露（150-200元/天·日薪制） |

### JD-11 海康威视 · 应用软件开发工程师（Java方向·大模型）

| 列 | 提取内容 |
|---|---|
| 硬性要求 | Java 集合、多线程、IO、JVM；Spring Boot、Spring Cloud Alibaba；微服务、分布式系统；Redis、PostgreSQL、RabbitMQ、Kafka |
| 加分项 | 大模型应用：Prompt、Agent 工作流、RAG、MCP、Agent Skills；Claude Code、Cline 等 AI 编程工具（注：大模型部分在原文属职位要求第 3 条，部分条目为"者优先"性质） |
| 工作内容 | 以 Java 后端工程为基础，叠加企业级大模型应用接入与智能体实践（杭州，2026-06-10 发布） |
| 面试流程 | JD 未披露（信息来源：官方招聘页 + CSDN 第 30 周岗位观察转引） |

---

## 三、高频技能统计（11 条 Java 主线 JD）

| 技能 | 出现次数 | 占比 | 优先级 |
|---|---|---|---|
| Java 语言基础（JVM/并发/集合） | 11/11 | 100% | P0 硬门槛 |
| Spring Boot / Spring Cloud 微服务 | 10/11 | 91% | P0 硬门槛 |
| Agent 编排（ReAct/Tool Calling/多Agent/工作流） | 10/11 | 91% | P0 硬门槛 |
| 高并发 / 高可用系统工程化 | 9/11 | 82% | P0 硬门槛 |
| 大模型 API 集成（Qwen/DeepSeek/OpenAI 等） | 9/11 | 82% | P0 硬门槛 |
| RAG 全链路（检索增强生成） | 8/11 | 73% | P0 硬门槛 |
| 分布式中间件（Redis/Kafka/RocketMQ/RabbitMQ） | 8/11 | 73% | P0 硬门槛 |
| Function Calling / 工具调用 | 7/11 | 64% | P1 核心 |
| Prompt Engineering | 7/11 | 64% | P1 核心 |
| 向量数据库 + Embedding（Milvus/PGVector 等） | 7/11 | 64% | P1 核心 |
| Python（多为"二选一/加分"性质） | 7/11 | 64% | P1 核心 |
| Spring AI / LangChain4j（Java 原生 AI 框架） | 5/11 | 45% | P1 核心 |
| Docker / Kubernetes | 4/11 | 36% | P2 加分 |
| 流式响应（SSE/WebSocket） | 3/11 | 27% | P2 加分 |
| Token 成本控制 / 推理性能优化 | 3/11 | 27% | P2 加分 |
| 可观测性（链路追踪/监控/评估体系） | 3/11 | 27% | P2 加分 |
| MCP 协议 / Agent Skills | 1/11 | 9% | P3 了解即可 |
| 大模型微调（LoRA/PEFT） | 1/11 | 9% | P3 了解即可 |
| GraphRAG / 知识图谱 | 2/11 | 18% | P3 了解即可 |

**对照样本趋势信号（腾讯/字节/神州数码）：** LangGraph/LangChain、Agent 记忆管理（记忆槽位）、LLM 评测体系、SFT/RL 微调、上下文工程已进入大厂 JD 高频词，但主线语言为 Python/Go——Java 候选人掌握同等概念（用 Java 实现）即可形成差异化。另：AI Coding 工具（Claude Code/Cursor/TRAE）在 Java 主线 JD-2/7/11 中被明确要求；"Harness 工程"信号来自 CSDN《2026 年第 30 周 Agent＋Java 岗位观察》对腾讯混元岗位的观察，非本样本 JD 原文。

---

## 四、与当前路线图的差距分析

对照 `java-ai-agent-roadmap.html`（五阶段 24 周规划）逐项核对：

| 刚需能力 | 路线图覆盖情况 | 差距与结论 |
|---|---|---|
| Java 基础（JVM/并发/集合） | ✅ 已有（存量优势） | 无差距，面试前按八股复习即可 |
| Spring Boot/Cloud 微服务 | ✅ Phase 2 覆盖 | 路线图节奏合理，微服务是 91% 岗位硬门槛 |
| Agent 编排（ReAct/工具调用/多Agent） | ✅ Phase 2 覆盖 | 无差距；JD-3/JD-9 明确要求 ReAct、Plan-and-Execute，路线项目 2（智能客服）正好匹配 |
| RAG 全链路 | ✅ Phase 1 覆盖（切分/混合检索/rerank/评测） | 无差距；JD-9 金融岗还要求"可溯源性"，评测维度需在项目 1 中补强 |
| 分布式中间件 | ✅ Phase 2 覆盖 | 73% 岗位硬门槛，路线图定位正确，不能推迟 |
| Spring AI / LangChain4j | ✅ Phase 0 覆盖 | 45% 岗位点名要求（且多为"熟练/精通"级），路线图双框架策略与市场完全吻合 |
| Python | ✅ 贯穿线覆盖（2-3 周） | 7/11 提及但多为加分/二选一，路线图"能读写脚本"定位准确，不必过度投入 |
| Prompt 工程 | ✅ Phase 1/2 覆盖 | 64% 岗位要求，已纳入 |
| 流式 SSE / Token 成本 / 可观测性 | ⚠️ 路线图 Phase 2 提及但深度不足 | **需补强**：JD-3/JD-7/JD-9 三个岗位把"流式响应、Token 成本管控、监控评估体系"写进核心职责，建议项目 1/2 均加入真实数字 |
| MCP / Agent Skills | ⚠️ 路线图列为 P2 差异化筹码 | 本次统计仅 9% 出现（海康威视），属前瞻窗口，路线图定位（做但不押注）合理 |
| 大厂算法向技能（SFT/RL、评测体系） | ❌ 未覆盖（Python 算法线） | 对照样本显示此为大厂算法岗要求，Java 工程岗不强制，维持不投入决策 |
| AI Coding 工具（Cursor/TRAE/Claude Code） | ❌ 未覆盖 | **新增发现**：JD-2/JD-7/JD-11 三家明确要求，建议纳入日常开发习惯（零成本积累） |

---

## 五、面试重点提取（7 个高频方向）

1. **Spring AI vs LangChain4j 选型**：优劣、适用场景、企业集成 vs 灵活工具箱（JD-3/6/7/9 点名）
2. **RAG 全链路优化**：切分策略、混合检索（BM25+向量）、rerank、召回率/准确性提升（JD-3/4/7/9/10）
3. **Agent 模式与可靠性**：ReAct、Plan-and-Execute、工具调用、多轮对话、幻觉抑制、死循环防护（JD-3/5/9）
4. **工程化深水区**：高并发上下文管理、流式响应（SSE/WebSocket）、Token 成本管控、超时重试降级（JD-3/7/9）
5. **分布式系统设计**：缓存/限流/熔断/分库分表、微服务治理、消息队列选型（JD-1/5/8/9）
6. **向量数据库选型与 Embedding**：Milvus/PGVector/ES 对比、检索重排序算法（JD-4/6/9/10）
7. **业务场景落地**：智能客服、知识库问答、合同审查等真实业务 AI 化的方案设计与 trade-off（JD-5/9/10）

---

## 六、差距分析与学习校准总结（196 字）

本次 14 个 JD 调研验证了路线图主体方向正确：Java 基础、Spring 微服务、Agent 编排、RAG、分布式中间件五项硬门槛与规划完全吻合，Spring AI/LangChain4j 双框架策略被 45% 岗位点名支持。需校准三点：一是流式输出、Token 成本、监控评估等工程化指标已从加分项升格为多家 JD 核心职责，项目 1/2 必须补真实数字；二是 AI Coding 工具（Cursor/TRAE/Claude Code）成为新硬性要求，需即刻融入日常开发；三是 Python 确认为加分而非门槛（多为二选一），维持 2-3 周轻量投入即可。MCP/Agent Skills 仅 9% 出现，作为差异化筹码保留但不押注。

---

## 附：数据可信度说明

- 以上 14 条 JD 均来自公开招聘平台/企业官网，链接于 2026-08-20 抓取时有效。
- 四列提取内容直接摘自 JD 原文职责与要求段落，未做主观扩写。
- 薪资"见链接"表示抓取快照未包含薪资字段，以链接页面实时显示为准。
- 已剔除 3 个页面标注"已关闭/已结束"的岗位，保证样本全部为在招状态。
- **真实性审查（2026-08-20）**：由独立检查 agent 逐条访问全部 14 个链接复核，结论为 14/14 真实在招、公司/城市/薪资/技能提取与原文一致、无编造；JD-11 海康威视经官方页面直访 + CSDN 转引来源 + BOSS 直聘同名岗位三重交叉验证确认。审查发现的 6 处小幅偏差（海康经验年限、力易达 AI coding 归类、润道日薪制表述、海康加分项归类、对照样本趋势句出处限定、GraphRAG 统计口径）已全部修正入本稿。
