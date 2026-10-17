## Moderation

## Introduction

Spring AI supports OpenAI’s Moderation model, which allows you to detect potentially harmful or sensitive content in text. Follow this [guide](https://platform.openai.com/docs/guides/moderation) to for more information on OpenAI’s moderation model.

Starting from version `2.0.0-M5`, Spring AI uses the official `openai-java` SDK under the hood for all OpenAI models. The transition is expected to be seamless and there are no breaking changes for existing users of the OpenAI API properties and builders. If you find any issues, please report them to us at [Spring AI GitHub Issues](https://github.com/spring-projects/spring-ai/issues).

## Prerequisites

1. Create an OpenAI account and obtain an API key. You can sign up at the [OpenAI signup page](https://platform.openai.com/signup) and generate an API key on the [API Keys page](https://platform.openai.com/account/api-keys).
2. Add the `spring-ai-openai` dependency to your project’s build file. For more information, refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section.

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Spring AI provides Spring Boot auto-configuration for the OpenAI Moderation Model. To enable it add the following dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file:

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-openai'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

## Moderation Properties

### Connection Properties

The prefix spring.ai.openai is used as the property prefix that lets you connect to OpenAI.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.openai.base-url | The URL to connect to | [api.openai.com](https://api.openai.com/) |
| spring.ai.openai.api-key | The API Key | \- |
| spring.ai.openai.organization-id | Optionally you can specify which organization is used for an API request. | \- |
| spring.ai.openai.project-id | Optionally, you can specify which project is used for an API request. | \- |
| spring.ai.openai.timeout | Request timeout for the OpenAI client. | 60 sec. |
| spring.ai.openai.max-retries | Maximum number of retries for the OpenAI client. | 3 |
| spring.ai.openai.proxy | Proxy settings for the OpenAI client. | \- |
| spring.ai.openai.custom-headers | Custom HTTP headers to add to OpenAI client requests. | empty |
| spring.ai.openai.connection-pool-metrics-enabled | Whether to enable connection pool metrics for the underlying OkHttp client. | false |

|  | For users that belong to multiple organizations (or are accessing their projects through their legacy user API key), optionally, you can specify which organization and project is used for an API request. Usage from these API requests will count as usage for the specified organization and project. |
| --- | --- |

### Configuration Properties

|  | Enabling and disabling of the embedding auto-configurations are now configured via top level properties with the prefix `spring.ai.model.moderation`.  To enable, spring.ai.model.moderation=openai (It is enabled by default)  To disable, spring.ai.model.moderation=none (or any value which doesn’t match openai)  This change is done to allow configuration of multiple models. |
| --- | --- |

The prefix spring.ai.openai.moderation is used as the property prefix for configuring the OpenAI moderation model.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.model.moderation | Enable Moderation model | openai |
| spring.ai.openai.moderation.base-url | The URL to connect to | [api.openai.com](https://api.openai.com/) |
| spring.ai.openai.moderation.api-key | The API Key | \- |
| spring.ai.openai.moderation.organization-id | Optionally you can specify which organization is used for an API request. | \- |
| spring.ai.openai.moderation.project-id | Optionally, you can specify which project is used for an API request. | \- |
| spring.ai.openai.moderation.model | ID of the model to use for moderation. | omni-moderation-latest |

|  | You can override the common `spring.ai.openai.base-url`, `spring.ai.openai.api-key`, `spring.ai.openai.organization-id` and `spring.ai.openai.project-id` properties. The `spring.ai.openai.moderation.base-url`, `spring.ai.openai.moderation.api-key`, `spring.ai.openai.moderation.organization-id` and `spring.ai.openai.moderation.project-id` properties, if set, take precedence over the common properties. This is useful if you want to use different OpenAI accounts for different models and different model endpoints. |
| --- | --- |

|  | All properties prefixed with `spring.ai.openai.moderation` can be overridden at runtime. |
| --- | --- |

## Runtime Options

The OpenAiModerationOptions class provides the options to use when making a moderation request. On start-up, the options specified by spring.ai.openai.moderation are used, but you can override these at runtime.

For example:

```java
OpenAiModerationOptions moderationOptions = OpenAiModerationOptions.builder()
    .model("omni-moderation-latest")
    .build();

ModerationPrompt moderationPrompt = new ModerationPrompt("Text to be moderated", this.moderationOptions);
ModerationResponse response = openAiModerationModel.call(this.moderationPrompt);

// Access the moderation results
Moderation moderation = moderationResponse.getResult().getOutput();

// Print general information
System.out.println("Moderation ID: " + moderation.getId());
System.out.println("Model used: " + moderation.getModel());

// Access the moderation results (there's usually only one, but it's a list)
for (ModerationResult result : moderation.getResults()) {
    System.out.println("\nModeration Result:");
    System.out.println("Flagged: " + result.isFlagged());

    // Access categories
    Categories categories = this.result.getCategories();
    System.out.println("\nCategories:");
    System.out.println("Sexual: " + categories.isSexual());
    System.out.println("Hate: " + categories.isHate());
    System.out.println("Harassment: " + categories.isHarassment());
    System.out.println("Self-Harm: " + categories.isSelfHarm());
    System.out.println("Sexual/Minors: " + categories.isSexualMinors());
    System.out.println("Hate/Threatening: " + categories.isHateThreatening());
    System.out.println("Violence/Graphic: " + categories.isViolenceGraphic());
    System.out.println("Self-Harm/Intent: " + categories.isSelfHarmIntent());
    System.out.println("Self-Harm/Instructions: " + categories.isSelfHarmInstructions());
    System.out.println("Harassment/Threatening: " + categories.isHarassmentThreatening());
    System.out.println("Violence: " + categories.isViolence());

    // Access category scores
    CategoryScores scores = this.result.getCategoryScores();
    System.out.println("\nCategory Scores:");
    System.out.println("Sexual: " + scores.getSexual());
    System.out.println("Hate: " + scores.getHate());
    System.out.println("Harassment: " + scores.getHarassment());
    System.out.println("Self-Harm: " + scores.getSelfHarm());
    System.out.println("Sexual/Minors: " + scores.getSexualMinors());
    System.out.println("Hate/Threatening: " + scores.getHateThreatening());
    System.out.println("Violence/Graphic: " + scores.getViolenceGraphic());
    System.out.println("Self-Harm/Intent: " + scores.getSelfHarmIntent());
    System.out.println("Self-Harm/Instructions: " + scores.getSelfHarmInstructions());
    System.out.println("Harassment/Threatening: " + scores.getHarassmentThreatening());
    System.out.println("Violence: " + scores.getViolence());
}
```

## Manual Configuration

Add the `spring-ai-openai` dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-openai</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file:

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-openai'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

Next, create an OpenAiModerationModel:

```java
OpenAiModerationApi openAiModerationApi = new OpenAiModerationApi(System.getenv("OPENAI_API_KEY"));

OpenAiModerationModel openAiModerationModel = new OpenAiModerationModel(this.openAiModerationApi);

OpenAiModerationOptions moderationOptions = OpenAiModerationOptions.builder()
    .model("omni-moderation-latest")
    .build();

ModerationPrompt moderationPrompt = new ModerationPrompt("Text to be moderated", this.moderationOptions);
ModerationResponse response = this.openAiModerationModel.call(this.moderationPrompt);
```

## Customizing the HTTP Client

Spring AI uses the official `openai-java` SDK under the hood and configures its HTTP transport with a custom OkHttp client built by `SpringAiOpenAiHttpClient.Builder`. You can intercept that builder before the underlying `OkHttpClient` is created by exposing one or more `OpenAiHttpClientBuilderCustomizer` beans. Each customizer receives the same builder used by every OpenAI model (chat, embedding, image, audio, moderation), so the customization applies uniformly.

```java
@FunctionalInterface
public interface OpenAiHttpClientBuilderCustomizer {
    void customize(SpringAiOpenAiHttpClient.Builder builder);
}
```

Typical use cases include:

- registering OkHttp `Interceptor` instances (authentication, propagation headers, custom logging);
- swapping the dispatcher `ExecutorService` (for example, to route async I/O through virtual threads);
- configuring proxy, SSL, hostname verification, or the connection-pool sizing exposed by the builder.

When several customizers are present, they are applied in `@Order` / `Ordered` order, after Spring AI’s own defaults, so user code wins.

The same hook is available when wiring a model manually via the `OpenAi*Model.Builder`:

```java
var chatModel = OpenAiChatModel.builder()
    .options(OpenAiChatOptions.builder().model("gpt-4o").build())
    .httpClientBuilderCustomizer(myCustomizer)
    .build();
```

## Example Code

The `OpenAiModerationModelIT` test provides some general examples of how to use the library. You can refer to this test for more detailed usage examples.