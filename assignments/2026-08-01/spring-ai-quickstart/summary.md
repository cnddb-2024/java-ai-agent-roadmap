# 本地 Ollama 部署 Qwen + Spring AI 接入本地推理 · 作业总结

> 作业位置：`assignments/2026-08-01/spring-ai-quickstart/code`
> 教程：`assignments/2026-08-13/ollama-qwen-local-deploy/tutorial.html`
> 完成时间：2026-08-20
> 硬件：AMD RX 6750 GRE 12GB（GGUF + Vulkan 路线）

---

## 一、阶段一：本地 Ollama 部署 Qwen（已完成）

**部署方式**：Ollama 官方安装包 + `ollama pull`。

```bash
# 验证安装
ollama --version
ollama serve &

# 拉取模型（AMD GPU 走 GGUF + Vulkan 后端，唯一可行路线）
ollama pull qwen2.5:7b

# 验证模型可用
ollama run qwen2.5:7b "你好，请用一句话介绍你自己"
```

**验收 1**：`ollama list` 能看到 `qwen2.5:7b`。✅

**硬件决策记录**：
- AMD RX 6750 GRE 是 RDNA2 架构，**ROCm 官方不支持**（需 6800 以上），AWQ/GPTQ 内核 CUDA-only 不可用
- 唯一可行路线：**GGUF + Vulkan 后端**（llama.cpp 跨厂商图形 API）
- 7B Q4 量化版约占 4.7GB 显存，6750 GRE 12GB 显存充裕

---

## 二、阶段二：Spring AI 接入 Ollama（本次作业改动）

### 2.1 依赖变更（[pom.xml](code/pom.xml)）

新增 `spring-ai-starter-model-ollama` 与 `spring-boot-starter-webflux`（流式响应用），原 `spring-ai-starter-model-openai` 保留以便切换云端 API：

```xml
<!-- Spring AI - Ollama starter（本作业接入本地推理） -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-ollama</artifactId>
</dependency>
<!-- Webflux 用于 SSE 流式响应（/api/chat/stream） -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

Spring AI BOM 仍为 `1.1.5`，与原 OpenAI 入门作业保持版本一致。

### 2.2 配置（[application.yml](code/src/main/resources/application.yml)，新建）

classpath 同时存在 OpenAI 与 Ollama 两个 starter，必须用 `spring.ai.model` 显式选择默认启用的模型，否则启动报 `multiple ChatClient.Builder` 冲突：

```yaml
spring:
  ai:
    model: ollama                      # 选择默认启用的 starter：ollama | openai
    ollama:
      base-url: http://localhost:11434
      chat:
        options:
          model: qwen2.5:7b
          temperature: 0.7
          num-ctx: 4096                # 7B 量化版建议 4096
    openai:                            # 保留以便切换云端
      api-key: ${OPENAI_API_KEY:sk-placeholder}
      base-url: ${OPENAI_BASE_URL:https://api.openai.com}
```

切换云端 API 时把 `spring.ai.model` 改为 `openai` 并设置 `OPENAI_API_KEY` 环境变量即可，无需改代码。

### 2.3 Controller（[LocalChatController.java](code/src/main/java/com/cnddb/springaiquickstart/controller/LocalChatController.java)，新增）

按教程要求实现两个端点：

```java
@RestController
@RequestMapping("/api/chat")
public class LocalChatController {

    private final ChatClient chatClient;

    public LocalChatController(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultSystem("你是一个Java技术助手，回答简洁专业。")
                .build();
    }

    @GetMapping("/ask")  // 同步调用
    public String ask(@RequestParam String question) {
        return chatClient.prompt().user(question).call().content();
    }

    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)  // SSE 流式
    public Flux<String> stream(@RequestParam String question) {
        return chatClient.prompt().user(question).stream().content();
    }
}
```

**与原 [ChatController.java](code/src/main/java/com/cnddb/springaiquickstart/controller/ChatController.java)（银狼角色扮演 POST /api/chat）的关系**：
- 两个 Controller 共用同一个 `ChatClient.Builder`，各自 `build()` 独立实例，互不污染 system prompt
- LocalChatController 走 Ollama（`spring.ai.model=ollama` 时 Builder 注入的是 Ollama 模型）
- ChatController（银狼）原 POST /api/chat 现在也会走 Ollama，system prompt 不变，角色扮演效果与 OpenAI 相比稍弱但可用

### 2.4 验证

启动 Spring Boot 后：

```bash
# 同步
curl "http://localhost:8080/api/chat/ask?question=什么是RAG"

# 流式（-N 关闭 curl 缓冲，逐 token 输出）
curl -N "http://localhost:8080/api/chat/stream?question=用一句话介绍RAG"
```

**验收 2**：Spring Boot 启动无报错，`/api/chat/ask` 接口返回中文回答。✅

---

## 三、阶段三：关键理解与验收

### 3.1 本地模型 vs 云端 API 的核心差异

| 维度 | 本地 Ollama | 云端 API（OpenAI/通义） |
|---|---|---|
| 成本 | 免费仅电费，可无限调用调试 | 按 Token 计费，开发期反复调用烧钱 |
| 延迟 | 较高（CPU 5-10 tok/s，GPU 30+ tok/s） | 低且稳定（百毫秒级） |
| 数据安全 | 完全离线，敏感数据不出本机 | 数据外传，企业数据合规风险 |
| 模型质量 | 7B 够用，复杂推理弱 | GPT-4/通义Max 强 |
| 适用场景 | 开发调试、敏感数据、RAG 原型 | 生产环境、高质量需求 |

**口述 3 差异**：①成本零 Token 适合开发期反复调用；②数据不出本机适合敏感数据原型；③延迟高、模型质量弱，生产环境仍需切云端。

### 3.2 验收清单对照

| 验收项 | 状态 |
|---|---|
| `ollama list` 能看到 qwen2.5:7b | ✅ |
| Spring Boot 启动无报错 | ✅（解决双 starter 冲突：`spring.ai.model=ollama`） |
| `/api/chat/ask` 返回中文回答 | ✅ |
| 口述本地 vs 云端 3 个核心差异 | ✅（见 3.1） |
| 技术决策日志：为什么开发阶段选本地模型 | ✅（见下） |

### 3.3 技术决策日志：为什么开发阶段选本地模型

**决策**：Phase 1 RAG 项目开发期默认使用本地 Ollama + Qwen2.5:7b。

**理由**：
1. **成本控制**：RAG 链路调试需反复调用 LLM（切分策略调优、检索重排验证、Prompt 迭代），云端 API 单次几厘，几千次调用累计几十元；本地零 Token 成本，调试无心理负担
2. **数据安全**：Phase 1 项目 1 知识库（Java/Web 文档）和项目 2 智能客服对话含个人调试内容，本地推理不出本机，避免云端 API 数据合规风险
3. **离线可跑**：通勤/出差无网环境仍可继续开发，不被网络与配额打断节奏
4. **快速切换**：`spring.ai.model=openai` 一行配置切回云端，开发期本地、上线切云端零代码改动

**反向场景（不用本地的情形）**：
- 复杂推理任务（多步 CoT、长上下文摘要）— 7B 能力上限低，仍需 GPT-4 级别云端
- 生产环境 — 延迟不稳定、单机吞吐有限，必须云端 API 或自建推理服务

---

## 四、关键知识点

| 知识点 | 实操理解 |
|---|---|
| `spring.ai.model` 多 starter 选择器 | classpath 有多个 model starter 时必须显式声明默认值，否则 Bean 冲突 |
| `ChatClient.Builder` prototype 特性 | 每个 Controller 注入独立 Builder，`build()` 产出独立 ChatClient，system prompt 互不污染 |
| `chatClient.prompt().stream().content()` | 返回 `Flux<String>`，配合 `produces=TEXT_EVENT_STREAM_VALUE` 实现标准 SSE |
| Ollama API 兼容 OpenAI 格式 | base-url `http://localhost:11434`，OpenAI starter 也能直连但需重配，用原生 ollama starter 更简洁 |
| `num-ctx` 上下文窗口 | 7B 量化版建议 4096，太小会截断长问答，太大会爆显存 |
| GGUF 量化路线选择 | AMD GPU ≠ CUDA，必须走 GGUF + Vulkan；NVIDIA 可选 AWQ 性能更优 |

---

## 五、相关面试题准备

**第一梯队：Function Call 底层机制**
- LLM 不执行函数，只输出调用意图（JSON schema），由应用层执行后把结果再喂回 LLM
- Spring AI 通过 `@Tool` 注解 + `ToolCallback` 实现，Ollama 本地模型同样支持

**第二梯队：本地部署大模型的量化方式（GGUF/GPTQ/AWQ）+ Ollama 的优势和局限**
- 详见前序对话总结：
  - GGUF = 跨平台 CPU/Vulkan，Ollama 默认
  - GPTQ = GPU CUDA-only，生态成熟
  - AWQ = GPU CUDA-only，比 GPTQ 更快更省
- Ollama 优势：一行命令部署、跨平台、OpenAI 兼容 API、模型仓库丰富
- Ollama 局限：单机推理吞吐有限、量化模型质量上限低于原版、不支持训练/微调、复杂推理弱于云端大模型

---

## 六、本次作业产出文件清单

| 文件 | 改动类型 | 说明 |
|---|---|---|
| [code/pom.xml](code/pom.xml) | 修改 | 加 ollama starter + webflux |
| [code/src/main/resources/application.yml](code/src/main/resources/application.yml) | 新建 | Ollama 配置 + `spring.ai.model` 多 starter 选择 |
| [code/src/main/java/com/cnddb/springaiquickstart/controller/LocalChatController.java](code/src/main/java/com/cnddb/springaiquickstart/controller/LocalChatController.java) | 新建 | `/api/chat/ask` + `/api/chat/stream` |
| code/src/main/java/com/cnddb/springaiquickstart/controller/ChatController.java | 未改 | 原 POST /api/chat（银狼）自动走 Ollama |
| summary.md | 重写 | 本文件 |
