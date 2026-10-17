## Groq Chat

[Groq](https://groq.com/) is an extremely fast, LPU™ based, AI Inference Engine that support various [AI Models](https://console.groq.com/docs/models), supports `Tool/Function Calling` and exposes a `OpenAI API` compatible endpoint.

Spring AI integrates with the [Groq](https://groq.com/) by reusing the existing [OpenAI](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html) client. For this you need to obtain a [Groq Api Key](https://console.groq.com/keys), set the base-url to [api.groq.com/openai/v1](https://api.groq.com/openai/v1) and select one of the provided [Groq models](https://console.groq.com/docs/models).

![spring ai groq integration](https://docs.spring.io/spring-ai/reference/_images/spring-ai-groq-integration.jpg)

|  | The Groq API is not fully compatible with the OpenAI API. Be aware for the following [compatibility constrains](https://console.groq.com/docs/openai). Additionally, currently Groq doesn’t support multimodal messages. |
| --- | --- |

Check the [GroqWithOpenAiChatModelIT.java](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-openai/src/test/java/org/springframework/ai/openai/chat/proxy/GroqWithOpenAiChatModelIT.java) tests for examples of using Groq with Spring AI.

## Prerequisites

- **Create an API Key**: Visit [here](https://console.groq.com/keys) to create an API Key. The Spring AI project defines a configuration property named `spring.ai.openai.api-key` that you should set to the value of the `API Key` obtained from groq.com.
- **Set the Groq URL**: You have to set the `spring.ai.openai.base-url` property to `https://api.groq.com/openai/v1`.
- **Select a Groq Model**: Use the `spring.ai.openai.chat.model=<model name>` property to select from the available [Groq Models](https://console.groq.com/docs/models).

You can set these configuration properties in your `application.properties` file:

```properties
spring.ai.openai.api-key=<your-groq-api-key>
spring.ai.openai.base-url=https://api.groq.com/openai/v1
spring.ai.openai.chat.model=llama3-70b-8192
```

For enhanced security when handling sensitive information like API keys, you can use Spring Expression Language (SpEL) to reference custom environment variables:

```yaml
# In application.yml
spring:
  ai:
    openai:
      api-key: ${GROQ_API_KEY}
      base-url: ${GROQ_BASE_URL}
      chat:
        model: ${GROQ_MODEL}
```

```bash
# In your environment or .env file
export GROQ_API_KEY=<your-groq-api-key>
export GROQ_BASE_URL=https://api.groq.com/openai/v1
export GROQ_MODEL=llama3-70b-8192
```

You can also set these configurations programmatically in your application code:

```java
// Retrieve configuration from secure sources or environment variables
String apiKey = System.getenv("GROQ_API_KEY");
String baseUrl = System.getenv("GROQ_BASE_URL");
String model = System.getenv("GROQ_MODEL");
```

### Add Repositories and BOM

Spring AI artifacts are published in Maven Central and Spring Snapshot repositories. Refer to the [Artifact Repositories](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories) section to add these repositories to your build system.

To help with dependency management, Spring AI provides a BOM (bill of materials) to ensure that a consistent version of Spring AI is used throughout the entire project. Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build system.

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Spring AI provides Spring Boot auto-configuration for the OpenAI Chat Client. To enable it add the following dependency to your project’s Maven `pom.xml` or Gradle `build.gradle` build files:

- Maven
- Gradle

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-openai'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

### Chat Properties

#### Retry Properties

The prefix `spring.ai.retry` is used as the property prefix that lets you configure the retry mechanism for the OpenAI chat model.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.retry.max-attempts | Maximum number of retry attempts. | 10 |
| spring.ai.retry.backoff.initial-interval | Initial sleep duration for the exponential backoff policy. | 2 sec. |
| spring.ai.retry.backoff.multiplier | Backoff interval multiplier. | 5 |
| spring.ai.retry.backoff.max-interval | Maximum backoff duration. | 3 min. |
| spring.ai.retry.on-client-errors | If false, throw a NonTransientAiException, and do not attempt retry for `4xx` client error codes | false |
| spring.ai.retry.exclude-on-http-codes | List of HTTP status codes that should not trigger a retry (e.g. to throw NonTransientAiException). | empty |
| spring.ai.retry.on-http-codes | List of HTTP status codes that should trigger a retry (e.g. to throw TransientAiException). | empty |

#### Connection Properties

The prefix `spring.ai.openai` is used as the property prefix that lets you connect to OpenAI.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.openai.base-url | The URL to connect to. Must be set to `https://api.groq.com/openai/v1` | \- |
| spring.ai.openai.api-key | The Groq API Key | \- |

#### Configuration Properties

|  | Enabling and disabling of the chat auto-configurations are now configured via top level properties with the prefix `spring.ai.model.chat`.  To enable, spring.ai.model.chat=openai (It is enabled by default)  To disable, spring.ai.model.chat=none (or any value which doesn’t match openai)  This change is done to allow configuration of multiple models. |
| --- | --- |

The prefix `spring.ai.openai.chat` is the property prefix that lets you configure the chat model implementation for OpenAI.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.openai.chat.enabled (Removed and no longer valid) | Enable OpenAI chat model. | true |
| spring.ai.openai.chat | Enable OpenAI chat model. | openai |
| spring.ai.openai.chat.base-url | Optional overrides the spring.ai.openai.base-url to provide chat specific url. Must be set to `https://api.groq.com/openai/v1` | \- |
| spring.ai.openai.chat.api-key | Optional overrides the spring.ai.openai.api-key to provide chat specific api-key | \- |
| spring.ai.openai.chat.model | The [available model](https://console.groq.com/docs/models) names are `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`, `gemma2-9b-it`. | \- |
| spring.ai.openai.chat.temperature | The sampling temperature to use that controls the apparent creativity of generated completions. Higher values will make output more random while lower values will make results more focused and deterministic. It is not recommended to modify temperature and top\_p for the same completions request as the interaction of these two settings is difficult to predict. | 0.8 |
| spring.ai.openai.chat.frequency-penalty | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model’s likelihood to repeat the same line verbatim. | 0.0f |
| spring.ai.openai.chat.max-tokens | The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model’s context length. | \- |
| spring.ai.openai.chat.n | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs. | 1 |
| spring.ai.openai.chat.presence-penalty | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model’s likelihood to talk about new topics. | \- |
| spring.ai.openai.chat.response-format | An object specifying the format that the model must output. Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is valid JSON. | \- |
| spring.ai.openai.chat.seed | This feature is in Beta. If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. | \- |
| spring.ai.openai.chat.stop | Up to 4 sequences where the API will stop generating further tokens. | \- |
| spring.ai.openai.chat.top-p | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or temperature but not both. | \- |
| spring.ai.openai.chat.tools | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. | \- |
| spring.ai.openai.chat.tool-choice | Controls which (if any) function is called by the model. none means the model will not call a function and instead generates a message. auto means the model can pick between generating a message or calling a function. Specifying a particular function via {"type: "function", "function": {"name": "my\_function"}} forces the model to call that function. none is the default when no functions are present. auto is the default if functions are present. | \- |
| spring.ai.openai.chat.user | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. | \- |
| spring.ai.openai.chat.stream-usage | (For streaming only) Set to add an additional chunk with token usage statistics for the entire request. The `choices` field for this chunk is an empty array and all other chunks will also include a usage field, but with a null value. | false |
| spring.ai.openai.chat.tool-callbacks | Tool Callbacks to register with the ChatModel. | \- |

|  | All properties prefixed with `spring.ai.openai.chat` can be overridden at runtime by adding a request specific [Runtime Options](#chat-options) to the `Prompt` call. |
| --- | --- |

## Runtime Options

The [OpenAiChatOptions.java](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-openai/src/main/java/org/springframework/ai/openai/OpenAiChatOptions.java) provides model configurations, such as the model to use, the temperature, the frequency penalty, etc.

On start-up, the default options can be configured with the `OpenAiChatModel(api, options)` constructor or the `spring.ai.openai.chat.*` properties.

At run-time you can override the default options by adding new, request specific, options to the `Prompt` call. For example to override the default model and temperature for a specific request:

```java
ChatResponse response = chatModel.call(
    new Prompt(
        "Generate the names of 5 famous pirates.",
        OpenAiChatOptions.builder()
            .model("mixtral-8x7b-32768")
            .temperature(0.4)
        .build()
    ));
```

|  | In addition to the model specific [OpenAiChatOptions](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-openai/src/main/java/org/springframework/ai/openai/OpenAiChatOptions.java) you can use a portable [ChatOptions](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/chat/prompt/ChatOptions.java) instance, created with the [ChatOptions#builder()](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/chat/prompt/DefaultChatOptionsBuilder.java). |
| --- | --- |

## Tool Calling

Groq supports [tool calling](https://console.groq.com/docs/tool-use) when the selected model supports it. Spring AI handles the tool execution loop.

|  | Check the [supported models](https://console.groq.com/docs/tool-use). |
| --- | --- |

For most applications, use `ChatClient` with the auto-registered `ToolCallingAdvisor` — see [Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html). For low-level control where you drive the loop yourself, see [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html).

## Multimodal

|  | Currently the Groq API doesn’t support media content. |
| --- | --- |

## Sample Controller

[Create](https://start.spring.io/) a new Spring Boot project and add the `spring-ai-starter-model-openai` to your pom (or gradle) dependencies.

Add a `application.properties` file, under the `src/main/resources` directory, to enable and configure the OpenAi chat model:

```application.properties
spring.ai.openai.api-key=<GROQ_API_KEY>
spring.ai.openai.base-url=https://api.groq.com/openai/v1
spring.ai.openai.chat.model=llama3-70b-8192
spring.ai.openai.chat.temperature=0.7
```

|  | replace the `api-key` with your OpenAI credentials. |
| --- | --- |

This will create a `OpenAiChatModel` implementation that you can inject into your class. Here is an example of a simple `@Controller` class that uses the chat model for text generations.

```java
@RestController
public class ChatController {

    private final OpenAiChatModel chatModel;

    @Autowired
    public ChatController(OpenAiChatModel chatModel) {
        this.chatModel = chatModel;
    }

    @GetMapping("/ai/generate")
    public Map generate(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
        return Map.of("generation", this.chatModel.call(message));
    }

    @GetMapping("/ai/generateStream")
    public Flux<ChatResponse> generateStream(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
        Prompt prompt = new Prompt(new UserMessage(message));
        return this.chatModel.stream(prompt);
    }
}
```

## Manual Configuration

The [OpenAiChatModel](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-openai/src/main/java/org/springframework/ai/openai/OpenAiChatModel.java) implements the `ChatModel` and `StreamingChatModel` and uses the [\[low-level-api\]](#low-level-api) to connect to the OpenAI service.

Add the `spring-ai-openai` dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-openai</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file.

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-openai'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

Next, create a `OpenAiChatModel` and use it for text generations:

```java
var chatModel = OpenAiChatModel.builder()
    .options(OpenAiChatOptions.builder()
        .baseUrl("https://api.groq.com/openai/v1")
        .apiKey(System.getenv("GROQ_API_KEY"))
        .model("llama3-70b-8192")
        .temperature(0.4)
        .maxTokens(200)
        .build())
    .build();

ChatResponse response = this.chatModel.call(
    new Prompt("Generate the names of 5 famous pirates."));

// Or with streaming responses
Flux<ChatResponse> response = this.chatModel.stream(
    new Prompt("Generate the names of 5 famous pirates."));
```

The `OpenAiChatOptions` provides the configuration information for the chat requests. The `OpenAiChatOptions.Builder` is fluent options builder.