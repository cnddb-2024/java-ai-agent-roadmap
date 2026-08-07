# 任务完成总结

在 Spring AI quickstart 项目中新增 ChatClient 流式对话接口，实现 SSE 实时流式输出。

技术实现：
- 新增 `spring-boot-starter-webflux` 依赖，支持响应式编程
- ChatController 新增 `/api/streamChat` POST 接口，返回 `Flux<String>`
- 使用 `chatClient.prompt().user(request.message).stream().content()` 实现流式调用
- 设置 `produces = MediaType.TEXT_EVENT_STREAM_VALUE` 确保响应类型为 SSE
- 原有 `/api/chat` 同步接口（`call().content()`）保持不变

核心对比：
- 同步调用：`call().content()` — 等待完整响应后一次性返回
- 流式调用：`stream().content()` — 逐 token 返回 `Flux<String>`，前端实时渲染

项目基于 Spring Boot 3.5.16 + Java 17 + Spring AI BOM 1.1.5，ChatClient 注入银狼角色 system prompt，提供同步和流式两种对话模式。

注：application.yml 未入库（含 API Key），需通过环境变量配置 OPENAI_API_KEY 和 base-url。
