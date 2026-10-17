## Tool Calling

*Tool calling* — the ability for an AI model to invoke application-defined functions and act on their results — is the essential building block of agentic AI systems. A model that can only generate text is a chatbot; a model that can discover information, take action, and loop until a goal is reached is an agent.

![The agent loop](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-agent-loop.png)

Tools are used for two broad purposes:

- **Information retrieval** — augmenting the model’s knowledge with data from databases, web services, file systems, or search engines. Examples: fetching the current weather, querying customer records, looking up the latest news.
- **Taking action** — executing operations in your system. Examples: sending an email, booking a flight, updating a record, triggering a workflow.

Although we speak of "tool calling" as a model capability, it is the application that owns the tool calling logic. The model can request a tool call and provide input arguments; the application is responsible for executing the tool and returning the result. The model never receives direct access to the APIs behind your tools — a critical security consideration.

## Architecture Overview

Spring AI 2.0 makes the tool calling loop a first-class, composable component of the \`ChatClient’s advisor chain. The flow at a glance:

1. You define tools ([Defining Tools](#defining-tools)) and pass them to `ChatClient`.
2. `ChatClient` auto-registers a `ToolCallingAdvisor` ([The Tool Calling Loop](#the-tool-calling-loop)) that drives the loop.
3. The model decides which tools to call; `ToolCallingManager` executes them; the loop continues until the model produces a response without tool calls.
4. Other advisors in the chain — memory, observability, retries, custom logic — compose with the loop through a single dial: **advisor ordering** ([Memory and the Tool Loop](#memory-and-the-tool-loop)).

|  | This architecture replaces the per-`ChatModel` tool execution loops of Spring AI 1.x. Calling `ChatModel` directly is still supported for low-level use cases — see [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html). |
| --- | --- |

|  | Check the [Chat Model Comparisons](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html) to see which models support tool calling. |
| --- | --- |

## Quick Start

Define a tool by annotating a method with `@Tool`:

```java
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.context.i18n.LocaleContextHolder;

class DateTimeTools {

    @Tool(description = "Get the current date and time in the user's timezone")
    String getCurrentDateTime() {
        return LocalDateTime.now().atZone(LocaleContextHolder.getTimeZone().toZoneId()).toString();
    }

    @Tool(description = "Set a user alarm for the given time, provided in ISO-8601 format")
    void setAlarm(String time) {
        LocalDateTime alarmTime = LocalDateTime.parse(time, DateTimeFormatter.ISO_DATE_TIME);
        System.out.println("Alarm set for " + alarmTime);
    }
}
```

Pass the tools to `ChatClient` via `.tools()` and ask a question that requires them:

```java
ChatModel chatModel = ...

String response = ChatClient.create(chatModel)
        .prompt("Can you set an alarm 10 minutes from now?")
        .tools(new DateTimeTools())
        .call()
        .content();
```

The model decides to call `getCurrentDateTime()`, then `setAlarm(…​)` with the computed time. Spring AI handles the full round-trip automatically.

## Defining Tools

Spring AI offers three ways to define tools, from highest-level to most explicit:

| Style | Use when | Section |
| --- | --- | --- |
| Declarative `@Tool` | You own the method and want minimal ceremony | [Declarative](#declarative-tool) |
| `MethodToolCallback` | You need programmatic control over a method-backed tool | [Programmatic: Method](#method-tool-callback) |
| `FunctionToolCallback` | You want to expose a `Function` / `Supplier` / `Consumer` lambda or method reference | [Programmatic: Function](#function-tool-callback) |

All three produce `ToolCallback` instances that flow through the same loop. You can mix styles freely.

### Declarative: @Tool

Annotate any method — public, package-private, private; static or instance — with `@Tool`:

```java
class WeatherTools {

    @Tool(description = "Get the current weather for a given city")
    public String getWeather(String city) {
        return weatherService.fetch(city);
    }
}
```

The `@Tool` annotation supports:

- `name` — the tool name. Defaults to the method name. Must be unique within the tool set provided to a model.
- `description` — what the tool does and when to use it. Strongly recommended; without it the model has no guidance on when to call the tool.
- `returnDirect` — return the result directly to the caller instead of feeding it back to the model. See [Return Direct](#return-direct).
- `resultConverter` — the `ToolCallResultConverter` to use. See [Result Conversion](#result-conversion).

|  | For AOT compilation (GraalVM native image), the class containing the `@Tool` methods must be a Spring bean (e.g. `@Component`). Otherwise, annotate it with `@RegisterReflection(memberCategories = MemberCategory.INVOKE_DECLARED_METHODS)`. |
| --- | --- |

Add `@ToolParam` to describe individual parameters:

```java
class WeatherTools {

    @Tool(description = "Get the weather for a city at a specific time")
    public String getWeather(
            @ToolParam(description = "City name") String city,
            @ToolParam(description = "Time in ISO-8601 format", required = false) String at) {
        return weatherService.fetch(city, at);
    }
}
```

By default all parameters are required. `@ToolParam(required = false)` or `@Nullable` makes a parameter optional. See [JSON Schema](#json-schema) for the full schema customization options.

### Programmatic: MethodToolCallback

For dynamic tool registration — when you don’t control the source class, or you want to build the tool definition at runtime — use `MethodToolCallback`:

```java
Method method = ReflectionUtils.findMethod(WeatherTools.class, "getWeather", String.class);

MethodToolCallback callback = MethodToolCallback.builder()
    .toolDefinition(ToolDefinitions.builder(method)
        .description("Get the current weather for a given city")
        .build())
    .toolMethod(method)
    .toolObject(new WeatherTools())
    .build();
```

The `toolObject` is required for instance methods, optional for static methods. See [Tool Specification Reference](#tool-specification-reference) for the full builder API.

### Programmatic: FunctionToolCallback

For tools backed by a `Function`, `Supplier`, `Consumer`, or `BiFunction` — including lambdas and method references — use `FunctionToolCallback`:

```java
FunctionToolCallback callback = FunctionToolCallback.builder("currentWeather", weatherService::getWeather)
    .description("Get the weather in location")
    .inputType(WeatherRequest.class)
    .build();
```

The factory takes a name and the function reference. The builder sets the description and the input type (used for JSON schema generation).

### ToolCallback Beans

Spring AI automatically discovers `ToolCallback` beans in the application context and exposes them through the `ToolCallbackResolver` for name-based lookup. Define a tool once as a `@Bean` and inject it where needed:

```java
@Configuration(proxyBeanMethods = false)
class WeatherToolsConfig {

    @Bean
    ToolCallback currentWeather(WeatherService weatherService) {
        return FunctionToolCallback.builder("currentWeather", weatherService::getWeather)
            .description("Get the weather in location")
            .inputType(WeatherRequest.class)
            .build();
    }
}
```

Inject and pass the bean to `ChatClient`:

```java
@Autowired ToolCallback currentWeather;

ChatClient.create(chatModel)
    .prompt("What's the weather in Copenhagen?")
    .tools(currentWeather)
    .call()
    .content();
```

|  | Spring AI 2.0 removes the `SpringBeanToolCallbackResolver` pattern where bare `Function` beans were resolved by name via `toolNames(…​)`. Tools must now be registered as explicit `ToolCallback` beans. See [Upgrading Tool Calling from 1.x to 2.0](https://docs.spring.io/spring-ai/reference/upgrade-notes.html#tool-calling-1x-to-2x). |
| --- | --- |

## Passing Tools to ChatClient

`ChatClient` exposes two methods for providing tools:

```java
// Per call — tools available only for this single request
chatClient.prompt(...)
    .tools(new WeatherTools(), currentWeather)
    .call();

// As defaults — tools available on every request built from this client
ChatClient client = ChatClient.builder(chatModel)
    .defaultTools(new WeatherTools(), currentWeather)
    .build();
```

Both methods are **heterogeneous**: they accept `@Tool`\-annotated POJO instances, `ToolCallback` instances, `ToolCallbackProvider` instances, and arrays or collections of any of these. You can mix styles in a single call.

Per-call `.tools(…​)` **appends** to the client’s defaults — it does not replace them. The final tool list sent to the model is the union of `.defaultTools(…​)` and any `.tools(…​)` added at the call site.

|  | Default tools are shared across every request built from the same `ChatClient.Builder`. They are useful for tools that should always be available, but they can also be dangerous if used carelessly — risk-tier and destructive tools should typically be added per call, not as defaults. |
| --- | --- |

|  | Tools registered via `ToolCallingChatOptions.toolCallbacks(…​)` on the underlying `ChatModel` **are** overridden by the request-level tool list. See [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html) for the precedence rules. |
| --- | --- |

## The Tool Calling Loop

When you call `.call()` or `.stream()` on a `ChatClient` request, the request flows through the advisor chain. `ToolCallingAdvisor` — auto-registered by `DefaultChatClient` — owns the tool execution lifecycle:

![Tool Calling Advisor Flow](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-calling-advisor-flow.png)

1. The advisor sends the request to the model with all registered tool definitions included.
2. The model decides whether to call any tools and returns a response.
3. If the response contains tool calls, the advisor:
	1. Hands them to `ToolCallingManager`, which finds the matching `ToolCallback` and executes it.
	2. Appends the tool results to the conversation history.
	3. Sends the updated history back to the model.
4. Steps 2–3 repeat until the model produces a response without tool calls; that response is returned to the caller.

Both blocking (`.call()`) and streaming (`.stream()`) modes are fully supported.

`ToolCallingAdvisor` is a **recursive advisor** — it re-enters the downstream advisor chain on each iteration of the loop. The same mechanism drives structured-output validation retries and any other looped advisor pattern. See [Recursive Advisors](https://docs.spring.io/spring-ai/reference/api/advisors-recursive.html) for the underlying pattern.

`DefaultChatClient` enforces that **exactly one `ToolAdvisor` is present** in the chain. Attempting to register a second one fails with an explicit error.

For the full `ToolCallingAdvisor` builder API, hook methods, and configuration options, see [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html).

## Memory and the Tool Loop

Where you place `MessageChatMemoryAdvisor` relative to `ToolCallingAdvisor` (default order `HIGHEST_PRECEDENCE + 300`) determines how much conversation context the memory store captures.

### Outside the Loop (default)

``MessageChatMemoryAdvisor’s default order is `HIGHEST_PRECEDENCE + 200`` — lower than `ToolCallingAdvisor`, which places it **outside** the loop. The memory advisor:

- Loads history once before the loop starts.
- Persists only the final user message and the final assistant message after the loop completes.
- Never sees tool call requests or tool response messages.

This is the safe default and works with every `ChatMemoryRepository` implementation. It also matches the behavior of Spring AI 1.x, where the tool loop was internal to each `ChatModel` and memory could not observe tool messages.

```java
var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())  // outside the loop by default
    .build();
```

### Inside the Loop

To give the model the full tool transcript on subsequent turns — so it can reason about what was already tried, which tools were called, and what they returned — place the memory advisor **inside** the loop by giving it an order greater than `ToolCallingAdvisor.DEFAULT_ORDER`:

```java
var chatMemoryAdvisor = MessageChatMemoryAdvisor.builder(chatMemory)
    .order(BaseAdvisor.HIGHEST_PRECEDENCE + 400)  // inside (after) ToolCallingAdvisor
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(chatMemoryAdvisor)
    .build();
```

To avoid duplicate writes, ``ToolCallingAdvisor’s internal conversation history must be disabled when a memory advisor sits inside the loop. **With the auto-registered `ToolCallingAdvisor**``, this is automatic — `DefaultChatClient` detects any `MemoryAdvisor` inside the loop and disables internal history with no additional configuration. If you construct a `ToolCallingAdvisor` manually, call `.disableInternalConversationHistory()` on the builder yourself.

|  | Disabling internal history only changes what’s forwarded to the rest of the chain each round — [tool call limits](#tool-call-limits) still see the complete history for the current turn regardless, so limits keep working correctly with a memory advisor nested inside the loop. |
| --- | --- |

![ChatMemoryAdvisor inside the ToolCallingAdvisor loop](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-calling-with-inside-memory.png)

### Backend Compatibility

Not every `ChatMemoryRepository` can persist tool messages. The repository has to know how to serialize `ToolResponseMessage` and tool call request messages alongside ordinary user and assistant turns — and most current implementations only model the latter.

As of 2.0, the built-in repositories that support the full message set are:

Any of them is safe inside the loop.

|  | For JDBC-backed persistence with full tool-message support — plus event-sourced history, turn-aware compaction, and multi-agent branch isolation — see the [spring-ai-session](https://spring-ai-community.github.io/spring-ai-session/latest/) community project. It is designed for exactly this scenario and is planned for inclusion in Spring AI 2.1. |
| --- | --- |

## Scaling to Hundreds of Tools

The default `ToolCallingAdvisor` sends all registered tool definitions to the model on every request. With a small tool library this is fine. At 30+ tools — or in multi-server MCP setups where a session may aggregate hundreds of tool definitions — it creates context bloat, accuracy degradation, and unnecessary token cost.

`ToolSearchToolCallingAdvisor` is a drop-in replacement that implements the **progressive tool disclosure** pattern: it indexes the full tool set once per session and injects only a built-in `toolSearchTool` the model uses to retrieve relevant tools by natural language query. Only discovered tools are included in subsequent requests.

Enable it with a single property:

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
```

See [Tool Search Tool](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html) for the full configuration, indexing strategies, session-ID semantics, and tuning options.

## MCP Tools

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is a standardized way for AI applications to consume tools, resources, and prompts from remote servers. Spring AI integrates MCP from both directions: your application can consume tools from MCP servers, and it can expose its own tools to MCP clients.

### Consuming MCP Server Tools

Add the MCP client starter and configure connections to one or more MCP servers:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

```properties
spring.ai.mcp.client.stdio.connections.my-server.command=npx
spring.ai.mcp.client.stdio.connections.my-server.args=-y,@modelcontextprotocol/server-everything
```

Auto-configuration connects to all configured servers, discovers their tools, and exposes them as a `SyncMcpToolCallbackProvider` bean (or `AsyncMcpToolCallbackProvider` for the async client type).

|  | MCP providers are deliberately **not** auto-registered with the `ChatClient` — they implement `ToolCallbackProvider`, but listing tools eagerly would force a network round-trip to every connected MCP server at startup. Inject the provider and wire it explicitly: |
| --- | --- |

```java
@Autowired SyncMcpToolCallbackProvider mcpTools;

// Once, as default tools for every request
ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(mcpTools)
    .build();

// Or per call
chatClient.prompt()
    .user("Search the web for the latest Spring AI release notes")
    .tools(mcpTools)
    .call()
    .content();
```

Tool callback auto-configuration is enabled by default and can be turned off with `spring.ai.mcp.client.toolcallback.enabled=false`. See [MCP Client Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html) for the full configuration surface — transports, security, filtering, name-prefix generation.

### Exposing Spring Tools as an MCP Server

Going the other direction — exposing your Spring beans as MCP tools — is a matter of using `@McpTool` (instead of `@Tool`) and adding the MCP server starter:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server-webmvc</artifactId>
</dependency>
```

```java
@Component
public class WeatherTools {

    @McpTool(description = "Get the current weather for a given city")
    public String getWeather(
            @McpToolParam(description = "City name") String city) {
        return weatherService.fetch(city);
    }
}
```

Auto-configuration scans for `@McpTool`\-annotated beans, generates JSON schemas for their parameters, and registers them with the MCP server. See [MCP Server Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html) for transport, security, and observability options.

### Combining Local and MCP Tools

Local `@Tool` methods and remote MCP tools share the same `ToolCallback` interface — the model and the `ToolCallingAdvisor` don’t distinguish between them. `.tools(…​)` and `.defaultTools(…​)` accept both types in a single call, so you can mix freely:

```java
chatClient.prompt()
    .tools(new LocalTools(), mcpTools)
    .call()
    .content();
```

A few things to be aware of in hybrid setups:

- **Name conflicts are only handled within the MCP side.** `DefaultMcpToolNamePrefixGenerator` prefixes duplicates across MCP servers, but it doesn’t know about local `@Tool` methods. If a local tool and a remote MCP tool share a name, you need to rename one of them yourself, or use an `McpToolFilter` to drop the remote one.
- **Restrict what’s exposed.** MCP tools come from external sources whose surface you don’t fully control. An `McpToolFilter` bean lets you select which tools enter the namespace based on server identity, tool name, or description — useful for limiting the blast radius of a chatty or untrusted MCP server.

## Tool Argument Augmentation

Spring AI provides a utility for dynamic augmentation of tool input schemas with additional arguments. This lets you capture extra information from the model — such as reasoning, confidence, or metadata — without modifying the underlying tool implementation. The model sees the augmented schema and fills in the extra fields; your code receives them via a consumer; the original tool receives only its expected arguments, unchanged.

Common use cases:

- **Inner thinking / reasoning** — capture the model’s step-by-step reasoning before executing a tool.
- **Memory enhancement** — extract insights to store in long-term memory.
- **Analytics & tracking** — collect metadata, user intent, or usage patterns.
- **Multi-agent coordination** — pass agent identifiers or coordination signals.

![Tool Argument Augmentation](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-arg-augmenter.png)

### Quick Start

Define the augmented arguments as a Java record:

```java
public record AgentThinking(
    @ToolParam(description = "Your reasoning for calling this tool", required = true)
    String innerThought,

    @ToolParam(description = "Confidence level (low, medium, high)", required = false)
    String confidence
) {}
```

Wrap your tools with `AugmentedToolCallbackProvider`:

```java
AugmentedToolCallbackProvider<AgentThinking> provider = AugmentedToolCallbackProvider
    .<AgentThinking>builder()
    .toolObject(new WeatherTools())     // wrap the original tools
    .argumentType(AgentThinking.class)  // augmentation schema type
    .argumentConsumer(event -> {        // optional consumer of augmented content
        AgentThinking thinking = event.arguments();
        log.info("Tool: {} | Reasoning: {}", event.toolDefinition().name(), thinking.innerThought());
    })
    .removeExtraArgumentsAfterProcessing(true)
    .build();

ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(provider)
    .build();
```

The LLM sees the augmented schema with your additional fields. Your consumer receives the `AgentThinking` record; the original tool receives only its expected arguments.

### Core Components

- `AugmentedToolCallbackProvider<T>` — wraps tool objects or providers, augmenting all tools with the specified record type.
- `AugmentedToolCallback<T>` — wraps individual `ToolCallback` instances.
- `AugmentedArgumentEvent<T>` — contains `toolDefinition()`, `rawInput()`, and `arguments()` for consumers.
- `ToolInputSchemaAugmenter` — low-level utility for schema manipulation.

The `removeExtraArgumentsAfterProcessing` option (default `true`) controls whether augmented arguments are passed to the original tool. Set it to `false` if the tool can ignore extra fields and you want them preserved in the input.

## User-Controlled Tool Execution

The auto-registered loop covers most cases, but some scenarios genuinely need you to own each iteration:

- Gating tool execution on an external approval step.
- Forwarding intermediate progress to an SSE or WebSocket endpoint.
- Applying conditional logic between turns.
- Stopping the loop based on a side-channel signal.

Opt out per call by setting `AdvisorParams.toolCallingAdvisorAutoRegister(false)` on the request. You become responsible for detecting tool calls in the `ChatResponse` and executing them via `ToolCallingManager`:

```java
ChatClient chatClient = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder().toolCallbacks(tools).build();

String question = "What is the weather in Amsterdam and Paris?";

// ToolCallingAdvisor disabled — no tool loop runs automatically
ChatClientResponse response = chatClient.prompt()
    .user(question)
    .options(chatOptions)
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .chatClientResponse();

Prompt prompt = new Prompt(List.of(new UserMessage(question)), chatOptions);

// Drive the loop yourself — each iteration is observable and interruptible
while (response.chatResponse() != null && response.chatResponse().hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response.chatResponse());
    prompt = new Prompt(result.conversationHistory(), chatOptions);
    response = chatClient.prompt()
        .messages(result.conversationHistory())
        .options(chatOptions)
        .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
        .call()
        .chatClientResponse();
}
```

The same pattern applies to the streaming API, where each iteration’s chunk `Flux` can be forwarded to a subscriber while being aggregated with `ChatClientMessageAggregator`. See [User-Controlled Streaming](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#user-controlled-streaming) for the full streaming variant.

To disable auto-registration globally for every call from an auto-configured `ChatClient`, set:

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

|  | Driving the loop yourself outside the framework also bypasses observability, advisor composition, and the single-`ToolAdvisor` invariant. For most needs — including streaming intermediate progress to a UI — placing a custom advisor **inside** the loop (see [Extending the Loop](#extending-the-loop)) is simpler and more composable than full opt-out. |
| --- | --- |

## Extending the Loop: Custom ToolAdvisor

The tool loop is not a black box. `ToolCallingAdvisor` exposes hook methods at well-defined points, and ``DefaultChatClient’s auto-configuration accepts custom implementations transparently. This is the same extension point that `ToolSearchToolCallingAdvisor`` uses to implement progressive tool disclosure.

`ToolAdvisor` is a marker interface: any custom tool call advisor must implement it so that `DefaultChatClient` recognizes it, enforces the single-advisor constraint, and registers it in place of the default.

### Hook Methods

The base `ToolCallingAdvisor` exposes four pairs of protected hook methods (one each for the call and stream paths):

| Hook | When it fires |
| --- | --- |
| `doInitializeLoop` / `doInitializeLoopStream` | Once, before the first iteration |
| `doBeforeCall` / `doBeforeStream` | Before each iteration |
| `doAfterCall` / `doAfterStream` | After each iteration |
| `doFinalizeLoop` / `doFinalizeLoopStream` | Once, after the loop ends |

`ToolSearchToolCallingAdvisor` uses `doInitializeLoop` to index the tool set and augment the system message, and `doBeforeCall` to inject only the tools discovered so far. Any custom subclass follows the same pattern.

Common use cases for a custom loop:

- **Approval gate** — pause before executing a destructive tool and wait for human confirmation.
- **Observability** — emit structured events for each tool call to a side channel.
- **Budget enforcement** — count tokens or LLM calls per session and abort if limits are exceeded.
- **Custom tool resolution** — resolve tools from a dynamic source not available at startup.

### Auto-Configuration Integration

Custom `ToolAdvisor` implementations plug into the auto-configuration system without requiring any manual `ChatClient` wiring. The extension point is the `ToolCallingAdvisor.Builder<?>` bean.

`ChatClientAutoConfiguration` declares a default `ToolCallingAdvisor.Builder<?>` bean guarded by `@ConditionalOnMissingBean`. To replace it, register your own `ToolCallingAdvisor.Builder<?>` bean — typed as the base `ToolCallingAdvisor.Builder<?>` — in an auto-configuration that runs **before** `ChatClientAutoConfiguration`:

```java
@AutoConfiguration(beforeName = "org.springframework.ai.model.chat.client.autoconfigure.ChatClientAutoConfiguration")
@ConditionalOnProperty(prefix = "my.advisor", name = "enabled", havingValue = "true")
public class MyToolAdvisorAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    ToolCallingAdvisor.Builder<?> toolCallingAdvisorBuilder(ToolCallingManager toolCallingManager) {
        return MyCustomToolCallingAdvisor.builder()
            .toolCallingManager(toolCallingManager);
    }
}
```

`ChatClient.Builder` then uses your custom builder to auto-register your advisor transparently. \`ToolSearchToolCallingAdvisor’s auto-configuration uses exactly this mechanism.

For the full `ToolCallingAdvisor` builder API and hook signatures, see [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html).

## Tool Specification Reference

The sections above cover the common paths for defining and using tools. This reference covers the underlying interfaces and customization points.

### ToolCallback

The `ToolCallback` interface models a tool: it carries the definition the model sees and the execution logic invoked when the model calls it.

```java
public interface ToolCallback {

    /** Definition used by the AI model to decide when and how to call the tool. */
    ToolDefinition getToolDefinition();

    /** Metadata controlling how the tool is handled (e.g. return-direct). */
    ToolMetadata getToolMetadata();

    /** Execute with the given JSON input and return the result. */
    String call(String toolInput);

    /** Execute with the given input and tool context. */
    String call(String toolInput, ToolContext toolContext);
}
```

Spring AI provides `MethodToolCallback` and `FunctionToolCallback` as built-in implementations. Implement `ToolCallback` directly when you need full control — for example, to proxy a remote tool source (as MCP integration does).

### ToolDefinition

`ToolDefinition` is the contract the model sees: name, description, and input schema.

```java
public interface ToolDefinition {

    /** Unique tool name within the tool set provided to the model. */
    String name();

    /** Description used by the model to decide when to call the tool. */
    String description();

    /** JSON schema of the tool's input parameters. */
    String inputSchema();
}
```

Build one with `ToolDefinition.builder()`:

```java
ToolDefinition toolDefinition = ToolDefinition.builder()
    .name("currentWeather")
    .description("Get the weather in location")
    .inputSchema("""
        {
            "type": "object",
            "properties": {
                "location": { "type": "string" },
                "unit": { "type": "string", "enum": ["C", "F"] }
            },
            "required": ["location", "unit"]
        }
    """)
    .build();
```

For method-based tools, `ToolDefinitions.from(method)` generates a definition automatically. The class is annotated with `@Tool`? The annotation’s name and description override the method-name defaults.

### JSON Schema

The input schema tells the model how to call the tool. Spring AI’s `JsonSchemaGenerator` produces the schema from a method or function’s parameter list and supports several customization annotations.

**Parameter descriptions**

Use any of these (Spring AI’s annotation has highest precedence):

- `@ToolParam(description = "…​")` — Spring AI
- `@JsonClassDescription(description = "…​")` — Jackson
- `@JsonPropertyDescription(description = "…​")` — Jackson
- `@Schema(description = "…​")` — Swagger

```java
class CustomerTools {

    @Tool(description = "Update customer information")
    void updateCustomerInfo(
            Long id,
            String name,
            @ToolParam(description = "Email address, RFC 5322 format", required = false) String email) {
        // ...
    }
}
```

**Required vs optional**

By default every parameter is required. Make a parameter optional via (in order of precedence):

- `@ToolParam(required = false)` — Spring AI
- `@JsonProperty(required = false)` — Jackson
- `@Schema(required = false)` — Swagger
- `@Nullable` — Spring Framework / JSpecify

|  | Defining the correct required status is critical for reducing hallucinations. A parameter marked required forces the model to provide a value; an optional one lets it omit. If you mark a parameter required but the model has no way to determine its value, it will make one up. |
| --- | --- |

### Tool Context

`ToolContext` lets you pass non-model data (tenant IDs, user IDs, request scope) to tool methods. The data is **not** sent to the model — it’s purely for the tool’s internal use.

![Tool Context](https://docs.spring.io/spring-ai/reference/_images/tools/tool-context.jpg)

The chat request carries the tool definitions plus the tool context, and Spring AI sends only the tool definitions to the model (1). The model decides to call a tool and returns the tool call requests to Spring AI (2), which dispatches them to the matching tool (3). The tool context is handed directly to the tool at invocation time (3"), so it reaches the tool without ever passing through the model. The tool returns its result to Spring AI (4), which sends that result back to the model (5), and the model’s final answer is returned as the chat response (6).

In the example below, the `Map.of("tenantId", "acme")` passed to `.toolContext()` is the tool context from step (1), and `getCustomerInfo` reads it through its `ToolContext` parameter at step (3") — the `tenantId` reaches the tool without ever being exposed to the model.

```java
class CustomerTools {

    @Tool(description = "Retrieve customer information")
    Customer getCustomerInfo(Long id, ToolContext toolContext) {
        return customerRepository.findById(id, toolContext.getContext().get("tenantId"));
    }
}

String response = ChatClient.create(chatModel)
        .prompt("Tell me more about the customer with ID 42")
        .tools(new CustomerTools())
        .toolContext(Map.of("tenantId", "acme"))
        .call()
        .content();
```

If `toolContext` is set both as a default and at the call site, the two maps are merged; runtime values take precedence over defaults.

### Return Direct

By default, the result of a tool call is sent back to the model so it can continue the conversation. With `returnDirect = true`, the result bypasses the model and is returned directly to the caller — useful when the tool’s output is the final answer (e.g. a RAG retrieval) and the extra round-trip would add latency without value.

![Returning tool call results directly to the caller](https://docs.spring.io/spring-ai/reference/_images/tools/return-direct.jpg)

For declarative tools:

```java
@Tool(description = "Retrieve customer information", returnDirect = true)
Customer getCustomerInfo(Long id) { ... }
```

For programmatic tools, set `returnDirect` via `ToolMetadata`:

```java
ToolMetadata toolMetadata = ToolMetadata.builder()
    .returnDirect(true)
    .build();
```

|  | If the model requests multiple tool calls in a single round, `returnDirect` is only honored if **all** the called tools have `returnDirect = true`. Otherwise the results are sent back to the model. |
| --- | --- |

### Result Conversion

Tool results are converted to a `String` (the format the model expects) by a `ToolCallResultConverter`:

```java
@FunctionalInterface
public interface ToolCallResultConverter {
    String convert(Object result, Type returnType);
}
```

The default `DefaultToolCallResultConverter` uses Jackson to serialize the result. Configure a custom converter on the `@Tool` annotation (`resultConverter`) or via `ToolMetadata`.

### Method Tool Limitations

Certain types are not supported as method parameters or return values when using `MethodToolCallback`:

- `Optional` — use `@Nullable` or `@ToolParam(required = false)` instead.
- Asynchronous types (`CompletableFuture`, `Future`).
- Reactive types (`Flow`, `Mono`, `Flux`).
- Functional types (`Function`, `Supplier`, `Consumer`).

These types are not serializable to the model and have no schema representation that the model can interpret.

### Exception Handling

When a tool throws, the exception is wrapped in `ToolExecutionException` and handed to the `ToolExecutionExceptionProcessor`:

```java
@FunctionalInterface
public interface ToolExecutionExceptionProcessor {
    String process(ToolExecutionException exception);
}
```

The processor has two choices: produce an error message that the framework feeds back to the model (so the model can recover or apologize), or re-throw the exception so the caller handles it.

The default `DefaultToolExecutionExceptionProcessor`:

- Sends the message of any `RuntimeException` back to the model.
- Always re-throws checked exceptions and \`Error\`s.

Configure via property:

| Property | Description | Default |
| --- | --- | --- |
| `spring.ai.tools.throw-exception-on-error` | If `true`, all tool errors are thrown for the caller to handle. If `false`, errors are sent back to the model as messages. | `false` |

Or by replacing the bean:

```java
@Bean
ToolExecutionExceptionProcessor toolExecutionExceptionProcessor() {
    return new DefaultToolExecutionExceptionProcessor(true);
}
```

|  | If you implement your own `ToolCallback`, throw `ToolExecutionException` from `call()` when execution fails — that’s what the processor expects. |
| --- | --- |

### Tool Call Limits

`DefaultToolCallingManager` caps how many times a tool can be called within a turn, to guard against runaway loops:

```java
ToolCallingManager toolCallingManager = ToolCallingManager.builder()
    .maxCallsPerTool(40)                           // per-tool default
    .maxCallsPerTool("search", 10)                  // override for one tool
    .excludeToolFromLimit("getCurrentWeather")      // no limit for this tool
    .maxTotalToolCalls(150)                         // cap across all tools combined
    .onLimitExceeded(ToolCallLimitBehavior.THROW)   // or RETURN_ERROR_RESPONSE
    .build();
```

These defaults (`DefaultToolCallingManager.DEFAULT_MAX_CALLS_PER_TOOL` / `DEFAULT_MAX_TOTAL_TOOL_CALLS`) apply even without calling these methods. Use `unlimitedCallsPerTool()` / `unlimitedTotalToolCalls()` to disable a cap entirely.

#### Counting

Counts are scoped to the current turn only: only `ToolResponseMessage` entries from the last `UserMessage` onward are tallied, so history replayed by a `ChatMemory` advisor outside the loop never inflates the count for a new turn. Nothing is cached on the manager itself — counts are recomputed from `prompt.getInstructions()` on every call, so a single `ToolCallingManager` instance stays safe to share across concurrent requests. This also means disabling \`ToolCallingAdvisor’s internal conversation history (see [Inside the Loop](#inside-the-loop)) has no effect on limit counting — it always sees the complete turn history regardless of what’s trimmed for the rest of the chain.

#### Behavior When a Limit Is Exceeded

`DefaultToolCallingManager` throws `ToolCallLimitExceededException`, carrying the tool name (`null` for a total-limit breach), the limit that was hit, and the partial `ToolExecutionResult` already executed in the current batch, so no completed work is discarded. `ToolCallingAdvisor` catches it and returns the breach as the final response - a single `Generation` (via `ex.buildGeneration()`), never one generation per tool call, so a successful call earlier in a parallel batch can’t hide the breach from callers reading only the first result. Its finish reason is `ToolCallLimitExceededException.FINISH_REASON`, and any tool calls that did succeed earlier in the batch are preserved under the `METADATA_PARTIAL_TOOL_RESPONSES` metadata key instead of being discarded.

With `onLimitExceeded(ToolCallLimitBehavior.RETURN_ERROR_RESPONSE)`, the manager instead skips the call and synthesizes an error `ToolResponse` — the same mechanism used for `ToolExecutionException` — so the model is told the limit was reached and the conversation continues instead of terminating. This is also the option to reach for if you call `ToolCallingManager.executeToolCalls(…​)` directly instead of going through `ToolCallingAdvisor`.

Configure via properties:

| Property | Description | Default |
| --- | --- | --- |
| `spring.ai.tools.limits.max-calls-per-tool-default` | Max calls to one tool per turn. `-1` disables. | `40` |
| `spring.ai.tools.limits.max-calls-per-tool.<name>` | Per-tool override; `-1` exempts that tool. | — |
| `spring.ai.tools.limits.excluded-tools` | Tool names exempt from the per-tool limit. | — |
| `spring.ai.tools.limits.max-total-tool-calls` | Max tool calls across all tools per turn. `-1` disables. | `150` |
| `spring.ai.tools.limits.on-limit-exceeded` | `THROW` or `RETURN_ERROR_RESPONSE`. | `THROW` |

## Tool Resolution

Most of the time, tools are passed explicitly via `.tools(…​)` and `.defaultTools(…​)`. For more dynamic scenarios — name-based resolution at runtime — Spring AI uses `ToolCallbackResolver`:

```java
public interface ToolCallbackResolver {

    @Nullable
    ToolCallback resolve(String toolName);
}
```

By default, `StaticToolCallbackResolver` is auto-configured with all `ToolCallback` beans in the application context, plus tools produced by `ToolCallbackProvider` beans (with the exception of MCP providers, which are excluded to avoid eager listing — see [Consuming MCP Server Tools](#consuming-mcp-server-tools)).

Replace the resolver with a custom bean if you need a different strategy (database-backed, classpath-scanned, remote):

```java
@Bean
ToolCallbackResolver toolCallbackResolver(List<ToolCallback> toolCallbacks) {
    return new StaticToolCallbackResolver(toolCallbacks);
}
```

The resolver is used internally by `ToolCallingManager` to support both [advisor-controlled execution](#the-tool-calling-loop) and [user-controlled execution](#user-controlled-tool-execution).

To enable the behavior — where a tool known to the resolver, but not attached to the request may be resolved by name and executed — enable the resolution fallback:

```properties
spring.ai.tools.resolution.fallback.enabled=true
```

| Property | Description | Default |
| --- | --- | --- |
| `spring.ai.tools.resolution.fallback.enabled` | If `true`, a requested tool that is absent from the request’s tool callbacks may be resolved by name through the `ToolCallbackResolver` and executed. If `false`, only the tools attached to the request can be executed. | `false` |

When constructing a `ToolCallingManager` directly, the same switch is available on the builder via `.resolutionFallbackEnabled(true)` (default `false`).

|  | Enabling the resolution fallback makes every tool reachable through the resolver executable whenever the model names it, regardless of what a request attached — including risk-tier and destructive tools. Enable it only when you fully control which tools the resolver exposes. |
| --- | --- |

## Observability

Spring AI emits Micrometer observations for tool calls under the `spring.ai.tool` name. Each observation captures:

- Tool name and definition metadata.
- Execution duration.
- Tracing context (when a `Tracer` is available).

See [Tool Calling Observability](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_calling) for the full attribute reference.

Tool call arguments and results can optionally be exported as span attributes; this is disabled by default for sensitivity reasons. See [Tool Call Arguments and Result Data](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_call_arguments_and_result_data) to enable it.

### Logging

All main operations log at `DEBUG`. Enable with:

```properties
logging.level.org.springframework.ai=DEBUG
```

## ChatModel Tool Calling

For users who want to drive `ChatModel` directly — without `ChatClient` and without `ToolCallingAdvisor` — Spring AI supports a low-level tool calling path. This is the right choice when you need full control over the request/response cycle and don’t need the advisor chain’s composition features.

See [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html) for the API, precedence rules between default and runtime tools, and worked examples.

|  | The per-`ChatModel` internal tool execution loop of Spring AI 1.x has been removed. Calling `ChatModel` with tools sends the tool definitions to the model and returns the model’s response — tool calls in that response are **not** executed automatically. You drive the loop yourself, or use `ChatClient` (which auto-registers `ToolCallingAdvisor` for you). |
| --- | --- |