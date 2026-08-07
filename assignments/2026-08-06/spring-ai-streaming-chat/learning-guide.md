# 学习指引：Spring AI 集成 OpenAI API：完成 ChatClient 流式对话调用 demo

> 来源：飞书任务，任务日期 2026-08-06（已标记完成但未提交作业，补充提交）
> 飞书任务 GUID：0e1d9f3a-2b30-4d4f-8484-a3446c30cfb8

## 学习目标

在已搭建的 Spring AI 项目基础上，新增 ChatClient 流式对话接口，实现 SSE（Server-Sent Events）实时流式输出。

## 知识点

- ChatClient 流式 API：`stream()` 方法与 `Flux<String>` 返回类型
- Spring WebFlux 响应式编程：`spring-boot-starter-webflux` 依赖
- SSE 协议：`MediaType.TEXT_EVENT_STREAM_VALUE` 内容类型
- Reactor `Flux` 响应式流：逐 token 返回生成内容
- 同步调用 vs 流式调用对比：`call().content()` vs `stream().content()`

## 学习资源

- Spring AI ChatClient 文档：https://docs.spring.io/spring-ai/reference/api/chatclient.html
- Spring WebFlux 文档：https://docs.spring.io/spring-framework/reference/web/webflux.html
- 作业项目仓库：https://github.com/cnddb-2024/spring-ai-quickstart.git

## 验收标准

- 新增 `/api/streamChat` 接口，返回 `Flux<String>`
- 使用 `MediaType.TEXT_EVENT_STREAM_VALUE` 实现 SSE 流式输出
- 添加 `spring-boot-starter-webflux` 依赖支持响应式
- 原有 `/api/chat` 同步接口保持可用

## 相关面试题

- ChatClient 的 `call()` 和 `stream()` 有什么区别？（第一梯队）
- SSE 流式输出的原理是什么？为什么 LLM 需要流式返回？（第一梯队）
- Spring WebFlux 和 Spring MVC 能否共存？（第二梯队）
