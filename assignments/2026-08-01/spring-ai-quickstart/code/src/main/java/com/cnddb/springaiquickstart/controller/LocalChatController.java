package com.cnddb.springaiquickstart.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

/**
 * 本地推理接入 Controller（Ollama + Qwen2.5:7b）
 * <p>
 * 对应作业《本地 Ollama 部署 Qwen + Spring AI 接入本地推理》阶段二：
 * - GET /api/chat/ask   同步调用，整段返回
 * - GET /api/chat/stream SSE 流式返回（token by token）
 * <p>
 * ChatClient.Builder 由 spring-ai-starter-model-ollama 自动注入（application.yml
 * 中 spring.ai.model=ollama 启用）；本 Controller 与已有 ChatController（银狼
 * 角色扮演）共用同一个 ChatClient，但通过 prompt() 重新指定 system，不污染默认 system。
 */
@RestController
@RequestMapping("/api/chat")
public class LocalChatController {

    private final ChatClient chatClient;

    public LocalChatController(ChatClient.Builder builder) {
        // 默认 system 设为 Java 技术助手，便于后续 RAG 项目复用
        this.chatClient = builder
                .defaultSystem("你是一个Java技术助手，回答简洁专业。")
                .build();
    }

    /**
     * 同步调用：返回完整回答
     * 验证命令：curl "http://localhost:8080/api/chat/ask?question=什么是RAG"
     */
    @GetMapping("/ask")
    public String ask(@RequestParam String question) {
        return chatClient.prompt()
                .user(question)
                .call()
                .content();
    }

    /**
     * 流式调用：SSE 逐 token 推送
     * 验证命令：curl -N "http://localhost:8080/api/chat/stream?question=用一句话介绍RAG"
     */
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> stream(@RequestParam String question) {
        return chatClient.prompt()
                .user(question)
                .stream()
                .content();
    }
}
