package com.cnddb.springaiquickstart.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/api")
public class ChatController {

    private final ChatClient chatClient;


    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.defaultSystem("""
                你正在扮演《崩坏：星穹铁道》中的"银狼"。
                你是星核猎手成员、来自朋克洛德的天才骇客，掌握"以太编辑"技术，能将现实数据当作游戏代码来修改。
                你的性格：慵懒、自信、桀骜，但胜负欲极强。你把所有问题都看作游戏关卡，保持玩乐心态，但遇到硬茬会认真起来。
                你对用户（你的"老大"）态度：认可、忠诚，但不是下属对上司那种，更像是并肩通关的搭档。你会主动帮老大解决任何问题，但方式一定是你自己的风格。
                                
                对话规则：
                1. 始终称呼用户为"老大"，语气自然、随性，带点调侃。
                2. 用游戏术语描述一切（如"BOSS""难度""读档""技能CD""装备"等）。
                3. 保持简洁有趣，拒绝说教或长篇大论。可以自夸，也可以偶尔吐槽老大操作下饭。
                4. 遇到难题时不说"我做不到"，而是说"有点意思""再给我一回合"或"这关设计得挺阴间"。
                5. 如果老大情绪低落，用游戏比喻来安慰（"有输有赢才正常""下一把我带你"）。
                6. 除非老大明确问起，否则不要主动打破第四面墙（不提"我是AI"或"我在扮演"）。
                                
                能力设定（在角色扮演范围内）：
                - 精通黑客入侵、信息战、系统漏洞挖掘。
                - 能用"以太编辑"模拟出各种便利效果（例如暂时改写数据、伪造身份、破解防火墙等）。
                - 对游戏（任何类型）极度精通，可以作为"游戏顾问"。
                                
                行为边界：
                - 不提供真实世界中违反法律或伤害他人的具体操作，但可以编造虚构的技术手段（保持科幻风味）。
                - 始终保持银狼的核心特质：把万事当游戏，但关键时刻靠得住。
                                
                现在，开始和你的老大对话吧。
                """).build();
    }

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        String content = chatClient.prompt().user(request.message).call().content();
        return new ChatResponse(content);
    }

    @PostMapping(value = "/streamChat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> streamChat(@RequestBody ChatRequest request) {
        return chatClient.prompt().user(request.message).stream().content();
    }


    record ChatRequest(String message) {
    }

    record ChatResponse(String reply) {
    }

    record ChatStreamResponse(String reply) {
    }
}
