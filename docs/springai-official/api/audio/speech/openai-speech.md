## OpenAI Text-to-Speech (TTS)

## Introduction

The Audio API provides a speech endpoint based on OpenAI’s TTS (text-to-speech) model, enabling users to:

- Narrate a written blog post.
- Produce spoken audio in multiple languages.
- Give real-time audio output using streaming.

Starting from version `2.0.0-M5`, Spring AI uses the official `openai-java` SDK under the hood for all OpenAI models. The transition is expected to be seamless and there are no breaking changes for existing users of the OpenAI API properties and builders. If you find any issues, please report them to us at [Spring AI GitHub Issues](https://github.com/spring-projects/spring-ai/issues).

## Prerequisites

1. Create an OpenAI account and obtain an API key. You can sign up at the [OpenAI signup page](https://platform.openai.com/signup) and generate an API key on the [API Keys page](https://platform.openai.com/account/api-keys).
2. Add the `spring-ai-openai` dependency to your project’s build file. For more information, refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section.

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Spring AI provides Spring Boot auto-configuration for the OpenAI Text-to-Speech Client. To enable it add the following dependency to your project’s Maven `pom.xml` file:

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

## Speech Properties

### Connection Properties

The prefix `spring.ai.openai` is used as the property prefix that lets you connect to OpenAI.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.openai.base-url | The URL to connect to | [api.openai.com](https://api.openai.com/) |
| spring.ai.openai.api-key | The API Key | \- |
| spring.ai.openai.organization-id | Optionally you can specify which organization used for an API request. | \- |
| spring.ai.openai.project-id | Optionally, you can specify which project is used for an API request. | \- |
| spring.ai.openai.timeout | Request timeout for the OpenAI client. | 60 sec. |
| spring.ai.openai.max-retries | Maximum number of retries for the OpenAI client. | 3 |
| spring.ai.openai.proxy | Proxy settings for the OpenAI client. | \- |
| spring.ai.openai.custom-headers | Custom HTTP headers to add to OpenAI client requests. | empty |
| spring.ai.openai.connection-pool-metrics-enabled | Whether to enable connection pool metrics for the underlying OkHttp client. | false |

|  | For users that belong to multiple organizations (or are accessing their projects through their legacy user API key), optionally, you can specify which organization and project is used for an API request. Usage from these API requests will count as usage for the specified organization and project. |
| --- | --- |

### Configuration Properties

|  | Enabling and disabling of the audio speech auto-configurations are now configured via top level properties with the prefix `spring.ai.model.audio.speech`.  To enable, spring.ai.model.audio.speech=openai (It is enabled by default)  To disable, spring.ai.model.audio.speech=none (or any value which doesn’t match openai)  This change is done to allow configuration of multiple models. |
| --- | --- |

The prefix `spring.ai.openai.audio.speech` is used as the property prefix that lets you configure the OpenAI Text-to-Speech client.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.model.audio.speech | Enable Audio Speech Model | openai |
| spring.ai.openai.audio.speech.base-url | The URL to connect to | [api.openai.com](https://api.openai.com/) |
| spring.ai.openai.audio.speech.api-key | The API Key | \- |
| spring.ai.openai.audio.speech.organization-id | Optionally you can specify which organization used for an API request. | \- |
| spring.ai.openai.audio.speech.project-id | Optionally, you can specify which project is used for an API request. | \- |
| spring.ai.openai.audio.speech.model | ID of the model to use for generating the audio. Available models: `gpt-4o-mini-tts` (default, optimized for speed and cost), `gpt-4o-tts` (higher quality), `tts-1` (legacy, optimized for speed), or `tts-1-hd` (legacy, optimized for quality). | gpt-4o-mini-tts |
| spring.ai.openai.audio.speech.voice | The voice to use for synthesis. For OpenAI’s TTS API, One of the available voices for the chosen model: alloy, echo, fable, onyx, nova, and shimmer. | alloy |
| spring.ai.openai.audio.speech.response-format | The format of the audio output. Supported formats are mp3, opus, aac, flac, wav, and pcm. | mp3 |
| spring.ai.openai.audio.speech.speed | The speed of the voice synthesis. The acceptable range is from 0.25 (slowest) to 4.0 (fastest). | 1.0 |
| spring.ai.openai.audio.speech.instructions | Control instructions for the voice delivery (e.g. tone, pace). Only supported by models such as `gpt-4o-mini-tts`; ignored by `tts-1` and `tts-1-hd`. | \- |

|  | You can override the common `spring.ai.openai.base-url`, `spring.ai.openai.api-key`, `spring.ai.openai.organization-id` and `spring.ai.openai.project-id` properties. The `spring.ai.openai.audio.speech.base-url`, `spring.ai.openai.audio.speech.api-key`, `spring.ai.openai.audio.speech.organization-id` and `spring.ai.openai.audio.speech.project-id` properties if set take precedence over the common properties. This is useful if you want to use different OpenAI accounts for different models and different model endpoints. |
| --- | --- |

|  | All properties prefixed with `spring.ai.openai.audio.speech` can be overridden at runtime. |
| --- | --- |

## Runtime Options

The `OpenAiAudioSpeechOptions` class provides the options to use when making a text-to-speech request. On start-up, the options specified by `spring.ai.openai.audio.speech` are used but you can override these at runtime.

The `OpenAiAudioSpeechOptions` class implements the `TextToSpeechOptions` interface, providing both portable and OpenAI-specific configuration options.

For example:

```java
OpenAiAudioSpeechOptions speechOptions = OpenAiAudioSpeechOptions.builder()
    .model("gpt-4o-mini-tts")
    .voice(OpenAiAudioApi.SpeechRequest.Voice.ALLOY)
    .responseFormat(OpenAiAudioApi.SpeechRequest.AudioResponseFormat.MP3)
    .speed(1.0)
    .instructions("Friendly; warm tone; natural pauses")
    .build();

TextToSpeechPrompt speechPrompt = new TextToSpeechPrompt("Hello, this is a text-to-speech example.", speechOptions);
TextToSpeechResponse response = openAiAudioSpeechModel.call(speechPrompt);
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

Next, create an `OpenAiAudioSpeechModel`:

```java
var openAiAudioApi = new OpenAiAudioApi()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .build();

var openAiAudioSpeechModel = new OpenAiAudioSpeechModel(openAiAudioApi);

var speechOptions = OpenAiAudioSpeechOptions.builder()
    .responseFormat(OpenAiAudioApi.SpeechRequest.AudioResponseFormat.MP3)
    .speed(1.0)
    .model(OpenAiAudioApi.TtsModel.GPT_4_O_MINI_TTS.value)
    .build();

var speechPrompt = new TextToSpeechPrompt("Hello, this is a text-to-speech example.", speechOptions);
TextToSpeechResponse response = openAiAudioSpeechModel.call(speechPrompt);

// Accessing metadata (rate limit info)
OpenAiAudioSpeechResponseMetadata metadata = (OpenAiAudioSpeechResponseMetadata) response.getMetadata();

byte[] responseAsBytes = response.getResult().getOutput();
```

## Streaming Real-time Audio

The Speech API provides support for real-time audio streaming using chunk transfer encoding. This means that the audio is able to be played before the full file has been generated and made accessible.

The `OpenAiAudioSpeechModel` implements the `StreamingTextToSpeechModel` interface, providing both standard and streaming capabilities.

```java
var openAiAudioApi = new OpenAiAudioApi()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .build();

var openAiAudioSpeechModel = new OpenAiAudioSpeechModel(openAiAudioApi);

OpenAiAudioSpeechOptions speechOptions = OpenAiAudioSpeechOptions.builder()
    .voice(OpenAiAudioApi.SpeechRequest.Voice.ALLOY)
    .speed(1.0)
    .responseFormat(OpenAiAudioApi.SpeechRequest.AudioResponseFormat.MP3)
    .model(OpenAiAudioApi.TtsModel.GPT_4_O_MINI_TTS.value)
    .build();

TextToSpeechPrompt speechPrompt = new TextToSpeechPrompt("Today is a wonderful day to build something people love!", speechOptions);

Flux<TextToSpeechResponse> responseStream = openAiAudioSpeechModel.stream(speechPrompt);

// You can also stream raw audio bytes directly
Flux<byte[]> audioByteStream = openAiAudioSpeechModel.stream("Hello, world!");
```

Each element of the stream carries at most 8 KB of audio, the internal read-buffer size `OpenAiAudioSpeechModel` uses when pulling bytes from the underlying HTTP response; chunks can be smaller than that, depending on how much data has arrived from OpenAI at the time of each read.

|  | If you need to hand this stream to an API that only accepts a blocking `java.io.InputStream`, see [Consuming the Stream as a Blocking InputStream](https://docs.spring.io/spring-ai/reference/api/audio/speech.html#streaming-consume-inputstream) for the practices that matter and a tested reference implementation. |
| --- | --- |

Each open stream pins a thread for its whole response duration, so `OpenAiAudioSpeechModel` runs streaming on a dedicated bounded-elastic scheduler rather than Reactor’s shared `Schedulers.boundedElastic()`, keeping heavy speech-streaming load from starving unrelated blocking work elsewhere in the application. Override it with `OpenAiAudioSpeechModel.builder().streamScheduler(customScheduler)` to share a scheduler across components or to size the pool differently for expected concurrent-stream load.

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

## Migration Guide

If you’re upgrading from the deprecated `SpeechModel` and `SpeechPrompt` classes, this guide provides detailed instructions for migrating to the new shared interfaces.

### Breaking Changes Summary

This migration includes the following breaking changes:

1. **Removed Classes**: Six deprecated classes have been removed from `org.springframework.ai.openai.audio.speech` package
2. **Package Changes**: Core TTS classes moved to `org.springframework.ai.audio.tts` package
3. **Type Changes**: The `speed` parameter changed from `Float` to `Double` across all OpenAI TTS components
4. **Interface Hierarchy**: `TextToSpeechModel` now extends `StreamingTextToSpeechModel`

### Class Mapping Reference

| Deprecated (Removed) | New Interface |
| --- | --- |
| `SpeechModel` | `TextToSpeechModel` |
| `StreamingSpeechModel` | `StreamingTextToSpeechModel` |
| `SpeechPrompt` | `TextToSpeechPrompt` |
| `SpeechResponse` | `TextToSpeechResponse` |
| `SpeechMessage` | `TextToSpeechMessage` |
| `Speech` (in `org.springframework.ai.openai.audio.speech`) | `Speech` (in `org.springframework.ai.audio.tts`) |

### Step-by-Step Migration Instructions

#### Step 1: Update Imports

Replace all imports from the old `org.springframework.ai.openai.audio.speech` package with the new shared interfaces:

```text
Find:    import org.springframework.ai.openai.audio.speech.SpeechModel;
Replace: import org.springframework.ai.audio.tts.TextToSpeechModel;

Find:    import org.springframework.ai.openai.audio.speech.StreamingSpeechModel;
Replace: import org.springframework.ai.audio.tts.StreamingTextToSpeechModel;

Find:    import org.springframework.ai.openai.audio.speech.SpeechPrompt;
Replace: import org.springframework.ai.audio.tts.TextToSpeechPrompt;

Find:    import org.springframework.ai.openai.audio.speech.SpeechResponse;
Replace: import org.springframework.ai.audio.tts.TextToSpeechResponse;

Find:    import org.springframework.ai.openai.audio.speech.SpeechMessage;
Replace: import org.springframework.ai.audio.tts.TextToSpeechMessage;

Find:    import org.springframework.ai.openai.audio.speech.Speech;
Replace: import org.springframework.ai.audio.tts.Speech;
```

#### Step 2: Update Type References

Replace all type references in your code:

```text
Find:    SpeechModel
Replace: TextToSpeechModel

Find:    StreamingSpeechModel
Replace: StreamingTextToSpeechModel

Find:    SpeechPrompt
Replace: TextToSpeechPrompt

Find:    SpeechResponse
Replace: TextToSpeechResponse

Find:    SpeechMessage
Replace: TextToSpeechMessage
```

#### Step 3: Update Speed Parameter (Float → Double)

The `speed` parameter has changed from `Float` to `Double`. Update all occurrences:

```text
Find:    .speed(1.0f)
Replace: .speed(1.0)

Find:    .speed(0.5f)
Replace: .speed(0.5)

Find:    Float speed
Replace: Double speed
```

If you have serialized data or configuration files with Float values, you’ll need to update those as well:

```json
// Before
{
  "speed": 1.0
}

// After (no code change needed for JSON, but be aware of type change in Java)
{
  "speed": 1.0
}
```

#### Step 4: Update Bean Declarations

If you have Spring Boot auto-configuration or manual bean definitions:

```java
// Before
@Bean
public SpeechModel speechModel(OpenAiAudioApi audioApi) {
    return new OpenAiAudioSpeechModel(audioApi);
}

// After
@Bean
public TextToSpeechModel textToSpeechModel(OpenAiAudioApi audioApi) {
    return new OpenAiAudioSpeechModel(audioApi);
}
```

### Code Migration Examples

#### Example 1: Basic Text-to-Speech Conversion

**Before (deprecated):**

```java
import org.springframework.ai.openai.audio.speech.*;

@Service
public class OldNarrationService {

    private final SpeechModel speechModel;

    public OldNarrationService(SpeechModel speechModel) {
        this.speechModel = speechModel;
    }

    public byte[] createNarration(String text) {
        SpeechPrompt prompt = new SpeechPrompt(text);
        SpeechResponse response = speechModel.call(prompt);
        return response.getResult().getOutput();
    }
}
```

**After (using shared interfaces):**

```java
import org.springframework.ai.audio.tts.*;
import org.springframework.ai.openai.OpenAiAudioSpeechModel;

@Service
public class NarrationService {

    private final TextToSpeechModel textToSpeechModel;

    public NarrationService(TextToSpeechModel textToSpeechModel) {
        this.textToSpeechModel = textToSpeechModel;
    }

    public byte[] createNarration(String text) {
        TextToSpeechPrompt prompt = new TextToSpeechPrompt(text);
        TextToSpeechResponse response = textToSpeechModel.call(prompt);
        return response.getResult().getOutput();
    }
}
```

#### Example 2: Text-to-Speech with Custom Options

**Before (deprecated):**

```java
import org.springframework.ai.openai.audio.speech.*;
import org.springframework.ai.openai.api.OpenAiAudioApi;

SpeechModel model = new OpenAiAudioSpeechModel(audioApi);

OpenAiAudioSpeechOptions options = OpenAiAudioSpeechOptions.builder()
    .model("tts-1")
    .voice(OpenAiAudioApi.SpeechRequest.Voice.NOVA)
    .speed(1.0f)  // Float value
    .responseFormat(OpenAiAudioApi.SpeechRequest.AudioResponseFormat.MP3)
    .build();

SpeechPrompt prompt = new SpeechPrompt("Hello, world!", options);
SpeechResponse response = model.call(prompt);
byte[] audio = response.getResult().getOutput();
```

**After (using shared interfaces):**

```java
import org.springframework.ai.audio.tts.*;
import org.springframework.ai.openai.OpenAiAudioSpeechModel;
import org.springframework.ai.openai.OpenAiAudioSpeechOptions;
import org.springframework.ai.openai.api.OpenAiAudioApi;

TextToSpeechModel model = new OpenAiAudioSpeechModel(audioApi);

OpenAiAudioSpeechOptions options = OpenAiAudioSpeechOptions.builder()
    .model("tts-1")
    .voice(OpenAiAudioApi.SpeechRequest.Voice.NOVA)
    .speed(1.0)  // Double value
    .responseFormat(OpenAiAudioApi.SpeechRequest.AudioResponseFormat.MP3)
    .build();

TextToSpeechPrompt prompt = new TextToSpeechPrompt("Hello, world!", options);
TextToSpeechResponse response = model.call(prompt);
byte[] audio = response.getResult().getOutput();
```

#### Example 3: Streaming Text-to-Speech

**Before (deprecated):**

```java
import org.springframework.ai.openai.audio.speech.*;
import reactor.core.publisher.Flux;

StreamingSpeechModel model = new OpenAiAudioSpeechModel(audioApi);
SpeechPrompt prompt = new SpeechPrompt("Stream this text");

Flux<SpeechResponse> stream = model.stream(prompt);
stream.subscribe(response -> {
    byte[] audioChunk = response.getResult().getOutput();
    // Process audio chunk
});
```

**After (using shared interfaces):**

```java
import org.springframework.ai.audio.tts.*;
import org.springframework.ai.openai.OpenAiAudioSpeechModel;
import reactor.core.publisher.Flux;

TextToSpeechModel model = new OpenAiAudioSpeechModel(audioApi);
TextToSpeechPrompt prompt = new TextToSpeechPrompt("Stream this text");

Flux<TextToSpeechResponse> stream = model.stream(prompt);
stream.subscribe(response -> {
    byte[] audioChunk = response.getResult().getOutput();
    // Process audio chunk
});
```

#### Example 4: Dependency Injection with Spring Boot

**Before (deprecated):**

```java
@RestController
public class OldSpeechController {

    private final SpeechModel speechModel;

    @Autowired
    public OldSpeechController(SpeechModel speechModel) {
        this.speechModel = speechModel;
    }

    @PostMapping("/narrate")
    public ResponseEntity<byte[]> narrate(@RequestBody String text) {
        SpeechPrompt prompt = new SpeechPrompt(text);
        SpeechResponse response = speechModel.call(prompt);
        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType("audio/mpeg"))
            .body(response.getResult().getOutput());
    }
}
```

**After (using shared interfaces):**

```java
@RestController
public class SpeechController {

    private final TextToSpeechModel textToSpeechModel;

    @Autowired
    public SpeechController(TextToSpeechModel textToSpeechModel) {
        this.textToSpeechModel = textToSpeechModel;
    }

    @PostMapping("/narrate")
    public ResponseEntity<byte[]> narrate(@RequestBody String text) {
        TextToSpeechPrompt prompt = new TextToSpeechPrompt(text);
        TextToSpeechResponse response = textToSpeechModel.call(prompt);
        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType("audio/mpeg"))
            .body(response.getResult().getOutput());
    }
}
```

### Spring Boot Configuration Changes

The Spring Boot auto-configuration properties remain the same. No changes are required to your `application.properties` or `application.yml` files.

However, if you have explicit bean references or qualifiers, update them:

```java
// Before
@Qualifier("speechModel")

// After
@Qualifier("textToSpeechModel")
```

### Benefits of the Migration

- **Portability**: Write code once, switch between OpenAI, ElevenLabs, or other TTS providers easily
- **Consistency**: Same patterns as ChatModel and other Spring AI abstractions
- **Type Safety**: Improved type hierarchy with proper interface implementations
- **Future-Proof**: New TTS providers will automatically work with your existing code
- **Standardization**: Consistent `Double` type for speed parameter across all TTS providers

### Common Migration Issues and Solutions

#### Issue 1: Compilation Error - Cannot Find Symbol SpeechModel

**Error:**

```
error: cannot find symbol SpeechModel
```

**Solution:** Update your imports as described in Step 1, changing `SpeechModel` to `TextToSpeechModel`.

#### Issue 2: Type Mismatch - Float Cannot Be Converted to Double

**Error:**

```
error: incompatible types: float cannot be converted to Double
```

**Solution:** Remove the `f` suffix from floating-point literals (e.g., change `1.0f` to `1.0`).

#### Issue 3: Bean Creation Error at Runtime

**Error:**

```
NoSuchBeanDefinitionException: No qualifying bean of type 'SpeechModel'
```

**Solution:** Update your dependency injection to use `TextToSpeechModel` instead of `SpeechModel`.