## Stability AI Image Generation

Spring AI supports Stability AI’s [text to image generation model](https://platform.stability.ai/docs/api-reference#tag/v1generation).

## Prerequisites

You will need to create an API key with Stability AI to access their AI models. Follow their [Getting Started documentation](https://platform.stability.ai/docs/getting-started/authentication) to obtain your API key.

The Spring AI project defines a configuration property named `spring.ai.stabilityai.api-key` that you should set to the value of the `API Key` obtained from Stability AI.

You can set this configuration property in your `application.properties` file:

```properties
spring.ai.stabilityai.api-key=<your-stabilityai-api-key>
```

For enhanced security when handling sensitive information like API keys, you can use Spring Expression Language (SpEL) to reference a custom environment variable:

```yaml
# In application.yml
spring:
  ai:
    stabilityai:
      api-key: ${STABILITYAI_API_KEY}
```

```bash
# In your environment or .env file
export STABILITYAI_API_KEY=<your-stabilityai-api-key>
```

You can also set this configuration programmatically in your application code:

```java
// Retrieve API key from a secure source or environment variable
String apiKey = System.getenv("STABILITYAI_API_KEY");
```

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Spring AI provides Spring Boot auto-configuration for the Stability AI Image Generation Client. To enable it add the following dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-stability-ai</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file.

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-stability-ai'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

### Image Generation Properties

The prefix `spring.ai.stabilityai` is used as the property prefix that lets you connect to Stability AI.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.stabilityai.base-url | The URL to connect to | [api.stability.ai/v1](https://api.stability.ai/v1) |
| spring.ai.stabilityai.api-key | The API Key | \- |

|  | Enabling and disabling of the image auto-configurations are now configured via top level properties with the prefix `spring.ai.model.image`.  To enable, spring.ai.model.image=stabilityai (It is enabled by default)  To disable, spring.ai.model.image=none (or any value which doesn’t match stabilityai)  This change is done to allow configuration of multiple models. |
| --- | --- |

The prefix `spring.ai.stabilityai.image` is the property prefix that lets you configure the `ImageModel` implementation for Stability AI.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.stabilityai.image.enabled (Removed and no longer valid) | Enable Stability AI image model. | true |
| spring.ai.model.image | Enable Stability AI image model. | stabilityai |
| spring.ai.stabilityai.image.base-url | Optional overrides the spring.ai.openai.base-url to provide a specific url | `https://api.stability.ai/v1` |
| spring.ai.stabilityai.image.api-key | Optional overrides the spring.ai.openai.api-key to provide a specific api-key | \- |
| spring.ai.stabilityai.image.n | The number of images to be generated. Must be between 1 and 10. | 1 |
| spring.ai.stabilityai.image.model | The engine/model to use in Stability AI. The model is passed in the URL as a path parameter. | `stable-diffusion-v1-6` |
| spring.ai.stabilityai.image.width | Width of the image to generate, in pixels, in an increment divisible by 64. Engine-specific dimension validation applies. | 512 |
| spring.ai.stabilityai.image.height | Height of the image to generate, in pixels, in an increment divisible by 64. Engine-specific dimension validation applies. | 512 |
| spring.ai.stabilityai.image.response-format | The format in which the generated images are returned. Must be "application/json" or "image/png". | \- |
| spring.ai.stabilityai.image.cfg\_scale | The strictness level of the diffusion process adherence to the prompt text. Range: 0 to 35. | 7 |
| spring.ai.stabilityai.image.clip\_guidance\_preset | Pass in a style preset to guide the image model towards a particular style. This list of style presets is subject to change. | `NONE` |
| spring.ai.stabilityai.image.sampler | Which sampler to use for the diffusion process. If this value is omitted, an appropriate sampler will be automatically selected. | \- |
| spring.ai.stabilityai.image.seed | Random noise seed (omit this option or use 0 for a random seed). Valid range: 0 to 4294967295. | 0 |
| spring.ai.stabilityai.image.steps | Number of diffusion steps to run. Valid range: 10 to 50. | 30 |
| spring.ai.stabilityai.image.style\_preset | Pass in a style preset to guide the image model towards a particular style. This list of style presets is subject to change. | \- |

## Runtime Options

The [StabilityAiImageOptions.java](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-stabilityai/src/main/java/org/springframework/ai/stabilityai/api/StabilityAiImageOptions.java) provides model configurations, such as the model to use, the style, the size, etc.

On start-up, the default options can be configured with the `StabilityAiImageModel(StabilityAiApi stabilityAiApi, StabilityAiImageOptions options)` constructor. Alternatively, use the `spring.ai.stabilityai.image.*` properties described previously.

At runtime, you can override the default options by adding new, request specific, options to the `ImagePrompt` call. For example to override the Stability AI specific options such as quality and the number of images to create, use the following code example:

```java
ImageResponse response = stabilityaiImageModel.call(
        new ImagePrompt("A light cream colored mini golden doodle",
        StabilityAiImageOptions.builder()
                .stylePreset("cinematic")
                .n(4)
                .height(1024)
                .width(1024).build())

);
```

|  | In addition to the model specific [StabilityAiImageOptions](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-stabilityai/src/main/java/org/springframework/ai/stabilityai/api/StabilityAiImageOptions.java) you can use a portable [ImageOptions](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/image/ImageOptions.java) instance, created with the [ImageOptionsBuilder#builder()](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/image/ImageOptionsBuilder.java). |
| --- | --- |