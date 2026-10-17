## ElevenLabs Text-to-Speech (TTS)

## Introduction

ElevenLabs provides natural-sounding speech synthesis software using deep learning. Its AI audio models generate realistic, versatile, and contextually-aware speech, voices, and sound effects across 32 languages. The ElevenLabs Text-to-Speech API enables users to bring any book, article, PDF, newsletter, or text to life with ultra-realistic AI narration.

## Prerequisites

1. Create an ElevenLabs account and obtain an API key. You can sign up at the [ElevenLabs signup page](https://elevenlabs.io/sign-up). Your API key can be found on your profile page after logging in.
2. Add the `spring-ai-elevenlabs` dependency to your project’s build file. For more information, refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section.

## Auto-configuration

Spring AI provides Spring Boot auto-configuration for the ElevenLabs Text-to-Speech Client. To enable it, add the following dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-elevenlabs</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file:

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-elevenlabs'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

## Speech Properties

### Connection Properties

The prefix `spring.ai.elevenlabs` is used as the property prefix for **all** ElevenLabs related configurations (both connection and TTS specific settings). This is defined in `ElevenLabsConnectionProperties`.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.elevenlabs.base-url | The base URL for the ElevenLabs API. | [api.elevenlabs.io](https://api.elevenlabs.io/) |
| spring.ai.elevenlabs.api-key | Your ElevenLabs API key. | \- |

### Configuration Properties

|  | Enabling and disabling of the audio speech auto-configurations are now configured via top level properties with the prefix `spring.ai.model.audio.speech`.  To enable, spring.ai.model.audio.speech=elevenlabs (It is enabled by default)  To disable, spring.ai.model.audio.speech=none (or any value which doesn’t match elevenlabs)  This change is done to allow configuration of multiple models. |
| --- | --- |

The prefix `spring.ai.elevenlabs.tts` is used as the property prefix to configure the ElevenLabs Text-to-Speech client, specifically. This is defined in `ElevenLabsSpeechProperties`.

| Property | Description | Default |
| --- | --- | --- |
| spring.ai.model.audio.speech | Enable Audio Speech Model | elevenlabs |
| spring.ai.elevenlabs.tts.model-id | The ID of the model to use. | eleven\_turbo\_v2\_5 |
| spring.ai.elevenlabs.tts.voice-id | The ID of the voice to use. This is the **voice ID**, not the voice name. | 9BWtsMINqrJLrRacOk9x |
| spring.ai.elevenlabs.tts.output-format | The output format for the generated audio. See [Output Formats](#output-formats) below. | mp3\_22050\_32 |

|  | The base URL and API key can also be configured **specifically** for TTS using `spring.ai.elevenlabs.tts.base-url` and `spring.ai.elevenlabs.tts.api-key`. However, it is generally recommended to use the global `spring.ai.elevenlabs` prefix for simplicity, unless you have a specific reason to use different credentials for different ElevenLabs services. The more specific `tts` properties will override the global ones. |
| --- | --- |

|  | All properties prefixed with `spring.ai.elevenlabs.tts` can be overridden at runtime. |
| --- | --- |

| Enum Value | Description |
| --- | --- |
| MP3\_22050\_32 | MP3, 22.05 kHz, 32 kbps |
| MP3\_44100\_32 | MP3, 44.1 kHz, 32 kbps |
| MP3\_44100\_64 | MP3, 44.1 kHz, 64 kbps |
| MP3\_44100\_96 | MP3, 44.1 kHz, 96 kbps |
| MP3\_44100\_128 | MP3, 44.1 kHz, 128 kbps |
| MP3\_44100\_192 | MP3, 44.1 kHz, 192 kbps |
| PCM\_8000 | PCM, 8 kHz |
| PCM\_16000 | PCM, 16 kHz |
| PCM\_22050 | PCM, 22.05 kHz |
| PCM\_24000 | PCM, 24 kHz |
| PCM\_44100 | PCM, 44.1 kHz |
| PCM\_48000 | PCM, 48 kHz |
| ULAW\_8000 | µ-law, 8 kHz |
| ALAW\_8000 | A-law, 8 kHz |
| OPUS\_48000\_32 | Opus, 48 kHz, 32 kbps |
| OPUS\_48000\_64 | Opus, 48 kHz, 64 kbps |
| OPUS\_48000\_96 | Opus, 48 kHz, 96 kbps |
| OPUS\_48000\_128 | Opus, 48 kHz, 128 kbps |
| OPUS\_48000\_192 | Opus, 48 kHz, 192 kbps |

## Runtime Options

The `ElevenLabsTextToSpeechOptions` class provides options to use when making a text-to-speech request. On start-up, the options specified by `spring.ai.elevenlabs.tts` are used, but you can override these at runtime. The following options are available:

- `modelId`: The ID of the model to use.
- `voiceId`: The ID of the voice to use.
- `outputFormat`: The output format of the generated audio.
- `voiceSettings`: An object containing voice settings such as `stability`, `similarityBoost`, `style`, `useSpeakerBoost`, and `speed`.
- `enableLogging`: A boolean to enable or disable logging.
- `languageCode`: The language code of the input text (e.g., "en" for English).
- `pronunciationDictionaryLocators`: A list of pronunciation dictionary locators.
- `seed`: A seed for random number generation, for reproducibility.
- `previousText`: Text before the main text, for context in multi-turn conversations.
- `nextText`: Text after the main text, for context in multi-turn conversations.
- `previousRequestIds`: Request IDs from previous turns in a conversation.
- `nextRequestIds`: Request IDs for subsequent turns in a conversation.
- `applyTextNormalization`: Apply text normalization ("auto", "on", or "off").
- `applyLanguageTextNormalization`: Apply language text normalization.

For example:

```java
ElevenLabsTextToSpeechOptions speechOptions = ElevenLabsTextToSpeechOptions.builder()
    .model("eleven_multilingual_v2")
    .voiceId("your_voice_id")
    .outputFormat(ElevenLabsApi.OutputFormat.MP3_44100_128.getValue())
    .build();

TextToSpeechPrompt speechPrompt = new TextToSpeechPrompt("Hello, this is a text-to-speech example.", speechOptions);
TextToSpeechResponse response = elevenLabsTextToSpeechModel.call(speechPrompt);
```

### Using Voice Settings

You can customize the voice output by providing `VoiceSettings` in the options. This allows you to control properties like stability and similarity.

```java
var voiceSettings = new ElevenLabsApi.SpeechRequest.VoiceSettings(0.75f, 0.75f, 0.0f, true);

ElevenLabsTextToSpeechOptions speechOptions = ElevenLabsTextToSpeechOptions.builder()
    .model("eleven_multilingual_v2")
    .voiceId("your_voice_id")
    .voiceSettings(voiceSettings)
    .build();

TextToSpeechPrompt speechPrompt = new TextToSpeechPrompt("This is a test with custom voice settings!", speechOptions);
TextToSpeechResponse response = elevenLabsTextToSpeechModel.call(speechPrompt);
```

## Manual Configuration

Add the `spring-ai-elevenlabs` dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-elevenlabs</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file:

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-elevenlabs'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

Next, create an `ElevenLabsTextToSpeechModel`:

```java
ElevenLabsApi elevenLabsApi = ElevenLabsApi.builder()
        .apiKey(System.getenv("ELEVEN_LABS_API_KEY"))
        .build();

ElevenLabsTextToSpeechModel elevenLabsTextToSpeechModel = ElevenLabsTextToSpeechModel.builder()
    .elevenLabsApi(elevenLabsApi)
    .options(ElevenLabsTextToSpeechOptions.builder()
        .model("eleven_turbo_v2_5")
        .voiceId("your_voice_id") // e.g. "9BWtsMINqrJLrRacOk9x"
        .outputFormat("mp3_44100_128")
        .build())
    .build();

// The call will use the default options configured above.
TextToSpeechPrompt speechPrompt = new TextToSpeechPrompt("Hello, this is a text-to-speech example.");
TextToSpeechResponse response = elevenLabsTextToSpeechModel.call(speechPrompt);

byte[] responseAsBytes = response.getResult().getOutput();
```

## Streaming Real-time Audio

The ElevenLabs Speech API supports real-time audio streaming using chunk transfer encoding. This allows audio playback to begin before the entire audio file is generated.

```java
ElevenLabsApi elevenLabsApi = ElevenLabsApi.builder()
        .apiKey(System.getenv("ELEVEN_LABS_API_KEY"))
        .build();

ElevenLabsTextToSpeechModel elevenLabsTextToSpeechModel = ElevenLabsTextToSpeechModel.builder()
    .elevenLabsApi(elevenLabsApi)
    .build();

ElevenLabsTextToSpeechOptions streamingOptions = ElevenLabsTextToSpeechOptions.builder()
    .model("eleven_turbo_v2_5")
    .voiceId("your_voice_id")
    .outputFormat("mp3_44100_128")
    .build();

TextToSpeechPrompt speechPrompt = new TextToSpeechPrompt("Today is a wonderful day to build something people love!", streamingOptions);

Flux<TextToSpeechResponse> responseStream = elevenLabsTextToSpeechModel.stream(speechPrompt);

// Process the stream, e.g., play the audio chunks
responseStream.subscribe(speechResponse -> {
    byte[] audioChunk = speechResponse.getResult().getOutput();
    // Play the audioChunk
});
```

## Voices API

The ElevenLabs Voices API allows you to retrieve information about available voices, their settings, and default voice settings. You can use this API to discover the \`voiceId\`s to use in your speech requests.

To use the Voices API, you’ll need to create an instance of `ElevenLabsVoicesApi`:

```java
ElevenLabsVoicesApi voicesApi = ElevenLabsVoicesApi.builder()
        .apiKey(System.getenv("ELEVEN_LABS_API_KEY"))
        .build();
```

You can then use the following methods:

- `getVoices()`: Retrieves a list of all available voices.
- `getDefaultVoiceSettings()`: Gets the default settings for voices.
- `getVoiceSettings(String voiceId)`: Returns the settings for a specific voice.
- `getVoice(String voiceId)`: Returns metadata about a specific voice.

Example:

```java
// Get all voices
ResponseEntity<ElevenLabsVoicesApi.Voices> voicesResponse = voicesApi.getVoices();
List<ElevenLabsVoicesApi.Voice> voices = voicesResponse.getBody().voices();

// Get default voice settings
ResponseEntity<ElevenLabsVoicesApi.VoiceSettings> defaultSettingsResponse = voicesApi.getDefaultVoiceSettings();
ElevenLabsVoicesApi.VoiceSettings defaultSettings = defaultSettingsResponse.getBody();

// Get settings for a specific voice
ResponseEntity<ElevenLabsVoicesApi.VoiceSettings> voiceSettingsResponse = voicesApi.getVoiceSettings(voiceId);
ElevenLabsVoicesApi.VoiceSettings voiceSettings = voiceSettingsResponse.getBody();

// Get details for a specific voice
ResponseEntity<ElevenLabsVoicesApi.Voice> voiceDetailsResponse = voicesApi.getVoice(voiceId);
ElevenLabsVoicesApi.Voice voiceDetails = voiceDetailsResponse.getBody();
```

## Example Code

- The [ElevenLabsTextToSpeechModelIT.java](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-elevenlabs/src/test/java/org/springframework/ai/elevenlabs/ElevenLabsTextToSpeechModelIT.java) test provides some general examples of how to use the library.
- The [ElevenLabsApiIT.java](https://github.com/spring-projects/spring-ai/blob/main/models/spring-ai-elevenlabs/src/test/java/org/springframework/ai/elevenlabs/api/ElevenLabsApiIT.java) test provides examples of using the low-level `ElevenLabsApi`.