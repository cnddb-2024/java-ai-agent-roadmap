# 第一周学习笔记汇总（2026-07-31 ~ 2026-08-07）

> Phase 0 · Java Web 转 AI Agent 启蒙期
> 起始日 2026-07-29，本笔记覆盖第 3~10 天的学习内容

---

## 一、本周学习概览

本周共完成 8 个作业任务，覆盖三大学习线：

| 学习线 | 任务数 | 核心产出 |
|--------|--------|----------|
| Java AI 框架线 | 3 | LangChain4j 结构研读、Spring AI 入门、Spring AI 流式对话 |
| RAG 知识线 | 2 | RAG 核心概念笔记、Qdrant 向量数据库部署 |
| Python 基础线 | 2 | Python 语法速览、Python 数据结构实战 |
| 全局认知 | 1 | Java Web 转 AI Agent 知识体系思维导图 |

---

## 二、Java AI 框架线

### 2.1 LangChain4j 框架结构研读（07-31）

**核心收获：**

- **项目结构**：LangChain4j 是 Java 生态的 LLM 应用框架，模块化设计清晰
- **AI Services 机制**：类似 Spring Data JPA 的接口自动实现，定义接口即可获得 LLM 调用能力
- **Chat Memory**：两种实现 — ChatMemory（单会话）和 ChatMemoryStore（多会话持久化）
- **RAG 模块**：完整支持 Metadata Filtering、Query Compress（查询压缩）、Query Router（查询路由）、ReRanking（重排序）
- **Agentic 模块**：支持 Tool Use 和 Agent 编排

**实践代码：** 克隆官方仓库并跑通 QuickStart，包含多个 Config 示例（Metadata Filtering、Query Compress + Query Router、ReRanking）

**面试题关联：** Spring AI vs LangChain4j 选型（第一梯队）、ChatMemory 两种实现（第二梯队）

### 2.2 Spring AI 入门（08-01）

**核心收获：**

- **项目搭建**：Spring Boot 3.5.16 + Java 17 + Spring AI BOM 1.1.5
- **ChatClient API**：`ChatClient.Builder` 注入 → `defaultSystem()` 设置角色 prompt → `prompt().user().call().content()` 调用
- **System Prompt**：配置了角色扮演（银狼），验证 LLM 人格注入能力
- **REST 封装**：`@RestController` + `record` 请求/响应体，提供 `/api/chat` POST 接口

**与 LangChain4j 对比：** Spring AI 更偏 Spring 生态集成，ChatClient API 更简洁，Advisors 机制类似 LangChain4j 的中间件链

**代码仓库：** https://github.com/cnddb-2024/spring-ai-quickstart.git

### 2.3 Spring AI 流式对话（08-06）

**核心收获：**

- **WebFlux 依赖**：新增 `spring-boot-starter-webflux` 支持响应式编程
- **流式调用**：`chatClient.prompt().user(request.message).stream().content()` 返回 `Flux<String>`
- **SSE 接口**：`@PostMapping(produces = MediaType.TEXT_EVENT_STREAM_VALUE)` 实现逐 token 输出
- **同步 vs 流式**：`call().content()`（等完整响应）vs `stream().content()`（逐 token 返回）

---

## 三、RAG 知识线

### 3.1 RAG 核心概念学习（08-06）

**核心收获 — RAG 四大环节：**

1. **Embedding 原理**
   - 离线阶段：资料 → chunk 分割 → embedding 向量化 → 存入向量数据库
   - 本质：文字 → 高维向量，通过余弦相似度判断语义相关性
   - `cos(A, B) = (A·B) / (|A| × |B|)`

2. **向量检索（粗排）**
   - 在线阶段：用户问题向量化 → 与数据库切片计算余弦相似度 → 召回相关切片
   - 召回率高但精度有限，需后续精排

3. **重排序（精排）**
   - 对粗排 Top-K 结果用更精准的模型（如 cross-encoder）重新打分
   - 速度更慢但准确率更高

4. **生成**
   - 将检索到的 chunk 作为 context 传入 prompt
   - LLM 基于 context + question 生成回答
   - 可要求引用来源，不相关时拒绝回答（减少幻觉）

**RAG 核心价值：** 知识热更新（向量化入库即可，无需重训模型）+ 错误可追溯（通过 chunk 元数据定位）

### 3.2 Qdrant 向量数据库部署（08-07）

**核心收获：**

- **Docker 部署**：docker-compose 一键启动 Qdrant 1.19.0
- **双端口**：6333（HTTP/Dashboard）、6334（gRPC，Spring AI 默认）
- **API Key 认证**：通过环境变量注入，application.properties 已 gitignore
- **Spring AI 集成**：
  - `spring-ai-starter-vector-store-qdrant` 依赖
  - `CommonConfig.java`：VectorStore 注入 + 文档存储 + 相似性搜索 + 元数据过滤
  - `initialize-schema=true` 自动创建集合
  - 元数据过滤两种方式：文本表达式 + FilterExpressionBuilder DSL
- **Spring AI 抽象优势**：VectorStore 接口屏蔽底层细节，切换向量库只需改配置

**代码仓库：** https://github.com/cnddb-2024/spring-ai-quickstart.git（master 分支新增 Qdrant 配置）

---

## 四、Python 基础线

### 4.1 Python 语法速览（08-01）

**核心收获：**

- 动态类型语言，无需声明变量类型
- 列表 ≈ Java ArrayList，字典 ≈ HashMap，for 循环直接遍历可迭代对象
- f-string 格式化输出
- 本次覆盖到第五章（数据结构）以前，函数/类/模块后续继续

### 4.2 Python 数据结构实战（08-07）

**核心收获：**

**函数定义（第四章）：**
- `def`、默认值参数、关键字参数、`*args`、`**keywords`
- 仅限位置形参 `/`、仅限关键字形参 `*`
- Lambda 表达式、文档字符串 `__doc__`、函数注解 `__annotations__`

**数据结构（第五章）：**
- **列表**：count/index/reverse/append/sort/pop，列表实现堆栈和队列
- **列表推导式**：`[表达式 for x in ... if ...]`，嵌套推导式，zip() 并行迭代
- **元组**：不可变序列，元组打包与序列解包
- **集合**：不重复无序，集合运算（差/合/交/对称差）
- **字典**：get/del/list/sorted，字典推导式

**与 Java 对比：**
- Python 列表 ≈ ArrayList，字典 ≈ HashMap，集合 ≈ HashSet
- 列表推导式是 Python 特色，Java 需 Stream API 实现类似功能

**代码仓库：** https://github.com/cnddb-2024/python-quickstart.git（551 行练习代码）

---

## 五、全局认知

### 5.1 Java Web 转 AI Agent 知识体系思维导图（07-31，Phase0 验收项）

**五大模块认知：**

1. **RAG 全链路**
   - RAG 是 Agent 的一个工具（检索增强）
   - 链路：知识库 → 向量化 → 存储 → 查询压缩 → 查询路由 → 元数据过滤 → 重排序 → LLM 返回

2. **Agent 编排**
   - A2A 协议实现多 Agent 协作
   - 典型编排：协调 Agent 规划 → Research Agent 收集资料 → Coder Agent 编码 → Reviewer Agent 审查

3. **Function Calling**
   - 业务代码暴露函数/工具给大模型（含描述、参数）
   - LLM 决定调用哪个工具，实际运行在业务代码中
   - 结果交回 LLM 组织返回

4. **双框架（Spring AI + LangChain4j）**
   - Spring AI：Spring 生态集成，ChatClient API 简洁，Advisors 机制
   - LangChain4j：AI Services 自动实现，RAG 模块完整，Agentic 模块

5. **MCP 协议**
   - Agent 纵向调用的工具集标准
   - 用户 query → Agent 检测可用 MCP 工具 → 按传输标准传参 → MCP Server 执行

**Java Web 技能映射：** 分布式微服务技术栈 → Agent 高可用/高并发/低消耗保障，中间件 → 多 Agent 协作基础

**面试题关联：** Agent vs Workflow + 混合架构（第一梯队）、MCP vs Function Call 本质区别（第一梯队）

---

## 六、本周产出汇总

| 日期 | 任务 | 产出 | 仓库 |
|------|------|------|------|
| 07-31 | 知识体系思维导图 | notes.md + mindmap | 路线图仓库 |
| 07-31 | LangChain4j 结构研读 | QuickStart 代码 + summary | langchain4j 官方仓库 |
| 08-01 | Python 语法速览 | 练习代码 | python-quickstart |
| 08-01 | Spring AI 入门 | ChatController + pom.xml | spring-ai-quickstart |
| 08-06 | RAG 核心概念 | notes.md（纯理论） | 路线图仓库 |
| 08-06 | Spring AI 流式对话 | streamChat 接口 | spring-ai-quickstart |
| 08-07 | Python 数据结构 | 551 行练习代码 | python-quickstart |
| 08-07 | Qdrant 部署 | Docker 配置 + CommonConfig | spring-ai-quickstart |

## 七、待继续学习

- Python：面向对象编程（类/继承/多态/异常处理）
- Python：模块与包管理（pip/venv/标准库）
- Spring AI：Advisors 机制实战
- Spring AI vs LangChain4j 选型对比笔记
- RAG 知识库问答 demo 完整链路
- Function Calling 与 Tool Use 实战

---

## 八、代码仓库索引

| 仓库 | 地址 | 内容 |
|------|------|------|
| 路线图项目 | https://github.com/cnddb-2024/java-ai-agent-roadmap | 学习路线图 + 作业记录 + 雷达图 |
| Spring AI Quickstart | https://github.com/cnddb-2024/spring-ai-quickstart | Spring AI 集成代码（Chat + Qdrant） |
| Python Quickstart | https://github.com/cnddb-2024/python-quickstart | Python 基础练习代码 |
