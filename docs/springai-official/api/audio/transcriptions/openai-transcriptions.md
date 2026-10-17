## OpenAI Transcriptions

Spring AI supports [OpenAI’s Transcription model](https://platform.openai.com/docs/api-reference/audio/createTranscription).

Starting from version `2.0.0-M5`, Spring AI uses the official `openai-java` SDK under the hood for all OpenAI models. The transition is expected to be seamless and there are no breaking changes for existing users of the OpenAI API properties and builders. If you find any issues, please report them to us at [Spring AI GitHub Issues](https://github.com/spring-projects/spring-ai/issues).

## Prerequisites

You will need to create an API key with OpenAI to access ChatGPT models. Create an account at [OpenAI signup page](https://platform.openai.com/signup) and generate the token on the [API Keys page](https://platform.openai.com/account/api-keys). The Spring AI project defines a configuration property named `spring.ai.openai.api-key` that you should set to the value of the `API Key` obtained from openai.com. Exporting an environment variable is one way to set that configuration property:

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Spring AI provides Spring Boot auto-configuration for the OpenAI Transcription Client. To enable it add the following dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file.

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-openai'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

### Transcription Properties

#### Connection Properties

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

#### Configuration Properties

|  | Enabling and disabling of the audio transcription auto-configurations are now configured via top level properties with the prefix `spring.ai.model.audio.transcription`.  To enable, spring.ai.model.audio.transcription=openai (It is enabled by default)  To disable, spring.ai.model.audio.transcription=none (or any value which doesn’t match openai)  This change is done to allow configuration of multiple models. |
| --- | --- |

The prefix `spring.ai.openai.audio.transcription` is used as the property prefix that lets you configure the retry mechanism for the OpenAI transcription model.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.model.audio.transcription | Enable OpenAI Audio Transcription Model | openai |
| spring.ai.openai.audio.transcription.base-url | The URL to connect to | [api.openai.com](https://api.openai.com/) |
| spring.ai.openai.audio.transcription.api-key | The API Key | \- |
| spring.ai.openai.audio.transcription.organization-id | Optionally you can specify which organization used for an API request. | \- |
| spring.ai.openai.audio.transcription.project-id | Optionally, you can specify which project is used for an API request. | \- |
| spring.ai.openai.audio.transcription.model | ID of the model to use for transcription. Available models: `gpt-4o-transcribe` (speech-to-text powered by GPT-4o), `gpt-4o-mini-transcribe` (speech-to-text powered by GPT-4o mini), `gpt-4o-transcribe-diarize` (speaker diarization), or `whisper-1` (general-purpose speech recognition model, default). | whisper-1 |
| spring.ai.openai.audio.transcription.response-format | The format of the transcript output: `json`, `text`, `srt`, `verbose_json`, `vtt`, or `diarized_json` (speaker-labeled segments, requires `gpt-4o-transcribe-diarize`). | text |
| spring.ai.openai.audio.transcription.prompt | An optional text to guide the model’s style or continue a previous audio segment. The prompt should match the audio language. |  |
| spring.ai.openai.audio.transcription.language | The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency. |  |
| spring.ai.openai.audio.transcription.temperature | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit. | 0 |
| spring.ai.openai.audio.transcription.timestamp-granularities | The timestamp granularities to populate for this transcription. response\_format must be set to `verbose_json` to use timestamp granularities. Either or both of these options are supported: `word`, or `segment`. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. | segment |
| spring.ai.openai.audio.transcription.known-speaker-names | Speaker names (up to 4), positionally matched with `known-speaker-references`. Only used with `gpt-4o-transcribe-diarize`. |  |
| spring.ai.openai.audio.transcription.known-speaker-references | Audio samples (as data URLs, e.g. `data:audio/wav;base64,…​`) of the known speakers, positionally matched with `known-speaker-names`. Only used with `gpt-4o-transcribe-diarize`. |  |
| spring.ai.openai.audio.transcription.chunking-strategy | Controls how the audio is chunked. Only `auto` is supported through this property; use `OpenAiAudioTranscriptionOptions.Builder` programmatically for voice-activity-detection tuning. Not supported by `whisper-1`. |  |
| spring.ai.openai.audio.transcription.diarized-json-workaround-enabled | Whether to work around a known OpenAI Java SDK bug ([openai-java#802](https://github.com/openai/openai-java/issues/802)) that misclassifies `diarized_json` responses. See [`diarized_json` SDK Workaround](#diarized-json-workaround). | true |

|  | You can override the common `spring.ai.openai.base-url`, `spring.ai.openai.api-key`, `spring.ai.openai.organization-id` and `spring.ai.openai.project-id` properties. The `spring.ai.openai.audio.transcription.base-url`, `spring.ai.openai.audio.transcription.api-key`, `spring.ai.openai.audio.transcription.organization-id` and `spring.ai.openai.audio.transcription.project-id` properties if set take precedence over the common properties. This is useful if you want to use different OpenAI accounts for different models and different model endpoints. |
| --- | --- |

|  | All properties prefixed with `spring.ai.openai.audio.transcription` can be overridden at runtime. |
| --- | --- |

## Runtime Options

The `OpenAiAudioTranscriptionOptions` class provides the options to use when making a transcription. On start-up, the options specified by `spring.ai.openai.audio.transcription` are used but you can override these at runtime.

For example:

```java
OpenAiAudioTranscriptionOptions transcriptionOptions = OpenAiAudioTranscriptionOptions.builder()
    .language("en")
    .prompt("Ask not this, but ask that")
    .temperature(0f)
    .responseFormat(AudioResponseFormat.VTT)
    .build();
AudioTranscriptionPrompt transcriptionRequest = new AudioTranscriptionPrompt(audioFile, transcriptionOptions);
AudioTranscriptionResponse response = openAiTranscriptionModel.call(transcriptionRequest);
```

### Response Metadata

For `verbose_json` and `diarized_json`, `response.getMetadata()` is an `OpenAiAudioTranscriptionResponseMetadata` exposing `getDuration()`, `getLanguage()`, `getUsage()`, `getSegments()` and `getWords()` in addition to the transcribed text. These are `null`/empty for other response formats.

### diarized\_json SDK Workaround

The OpenAI Java SDK (as of `4.42.0`) misclassifies `diarized_json` responses, which would otherwise surface the raw JSON payload as the transcript text ([openai-java#802](https://github.com/openai/openai-java/issues/802)). Spring AI detects this and recovers the clean text, speaker segments and usage automatically. `duration` stays unavailable for this format since the API doesn’t return it. Disable the workaround with `OpenAiAudioTranscriptionOptions.Builder#diarizedJsonWorkaroundEnabled(false)` or `spring.ai.openai.audio.transcription.diarized-json-workaround-enabled=false`.

## Manual Configuration

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

Next, create a `OpenAiAudioTranscriptionModel`

```java
var transcriptionOptions = OpenAiAudioTranscriptionOptions.builder()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .responseFormat(AudioResponseFormat.TEXT)
    .temperature(0f)
    .build();

var openAiAudioTranscriptionModel = OpenAiAudioTranscriptionModel.builder()
    .options(transcriptionOptions)
    .build();

var audioFile = new FileSystemResource("/path/to/your/resource/speech/jfk.flac");

AudioTranscriptionPrompt transcriptionRequest = new AudioTranscriptionPrompt(audioFile, transcriptionOptions);
AudioTranscriptionResponse response = openAiAudioTranscriptionModel.call(transcriptionRequest);
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