## Provider-Native Structured Output

By default, [`.entity(…​)`](https://docs.spring.io/spring-ai/reference/api/structured-output.html) appends the JSON schema to the prompt as text instructions. That is a *response-side* approach: the model is asked to comply, and the response is parsed afterward.

The complementary approach is a *request-side* constraint: tell the model’s provider, at the API level, that the response must conform to a schema. Most modern providers support this (OpenAI’s Structured Outputs, Anthropic’s structured output extension, Gemini’s `responseSchema`, Mistral’s `response_format`).

Spring AI exposes it portably with a switch on the `EntityParamSpec` consumer:

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec.useProviderStructuredOutput());
```

What changes at the wire level:

- The system prompt no longer carries a JSON format instruction (cleaner, fewer tokens).
- The schema is sent to the provider as an API-level field.
- The provider’s runtime enforces conformance — invalid responses cannot be emitted at all.

This provides:

- **Higher reliability**: the model guarantees output conforming to the schema.
- **Cleaner prompts**: no need to append format instructions.
- **Better performance**: models can optimize for structured output internally.

## How Spring AI Detects Support

Spring AI detects native support by checking whether the model’s chat options implement the `StructuredOutputChatOptions` interface. If not, the flag is silently ignored and the call falls back to the prompt-based default.

## Supported Models

The following providers support native structured output as of Spring AI 2.0. The same `.useProviderStructuredOutput()` call works regardless of which is wired in:

- **OpenAI**: GPT-4o and later models with JSON Schema support.
- **Anthropic**: Claude 3.5 Sonnet and later models.
- **Google GenAI**: Gemini 1.5 Pro and later models.
- **Mistral AI**: Mistral Small and later models with JSON Schema support.
- **Ollama**: models with JSON Schema support (model-specific; see [Known Limitations](#_known_limitations)).

## Why It’s Off by Default

Compatibility. Older or non-supporting models would reject the request, and the prompt-based default works everywhere.

|  | Native structured output is **not enabled by default** because support varies significantly across models and providers. Enable it only when you need the stronger API-level schema enforcement it provides, and always test with your specific model version. |
| --- | --- |

## Known Limitations

Even on providers that advertise the feature, native structured output support is often *partial*  — the accepted JSON Schema surface varies. `$ref`, deeply nested arrays, `allOf`/`anyOf`/`oneOf`, regex patterns, and recursive types are common limitations. The shape drift this can cause is exactly what [`validateSchema()`](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html) is good at catching.

### Ollama: Model-Specific Instability

Not all Ollama models reliably honor the structured output schema constraint. In particular, models with a built-in reasoning or "thinking" mode (for example `qwen3:8b`, `qwen3.5:9b`, and other newer Qwen variants) may return their internal reasoning trace as plain text rather than structured JSON, causing a deserialization error in `BeanOutputConverter` such as:

```
StreamReadException: Unrecognized token 'The': was expecting (JSON String, Number, Array, Object or token 'null', 'true' or 'false')
```

If you encounter this with Ollama, try a different model (for example `llama3.1:latest`) or fall back to the default prompt-based approach. You can also combine `useProviderStructuredOutput()` with `validateSchema()` so that malformed responses are automatically retried:

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec
        .useProviderStructuredOutput()
        .validateSchema());
```

### OpenAI: No Top-Level Array Support

The OpenAI Structured Outputs API does not accept a top-level JSON array as the response schema (see the [OpenAI community discussion](https://community.openai.com/t/support-top-level-array-in-json-schema/896048)). Requesting a `List<T>` with native structured output enabled will result in an API error.

```java
// Does NOT work with OpenAI native structured output:
List<ActorsFilms> films = chatClient.prompt()
    .user("Generate filmographies for Tom Hanks and Bill Murray.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {},
            spec -> spec.useProviderStructuredOutput()); // fails with OpenAI
```

Use one of these alternatives instead:

```java
// Option 1: wrap the list in a container record
record FilmographyList(List<ActorsFilms> films) {}

FilmographyList result = chatClient.prompt()
    .user("Generate filmographies for Tom Hanks and Bill Murray.")
    .call()
    .entity(FilmographyList.class, spec -> spec.useProviderStructuredOutput());
List<ActorsFilms> films = result.films();

// Option 2: use the default prompt-based approach (no native output required)
List<ActorsFilms> films = chatClient.prompt()
    .user("Generate filmographies for Tom Hanks and Bill Murray.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {});
```

The default prompt-based flow has no such restriction — top-level arrays work fine without `useProviderStructuredOutput()`.

## Enabling Globally

`useProviderStructuredOutput()` is a per-call switch. To enable native structured output for every call on a `ChatClient`, set the `AdvisorParams.ENABLE_NATIVE_STRUCTURED_OUTPUT` advisor parameter — as a default on the builder, or per request:

```java
// Per request
ActorsFilms films = chatClient.prompt()
    .advisors(AdvisorParams.ENABLE_NATIVE_STRUCTURED_OUTPUT)
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class);

// Globally on the builder
@Bean
ChatClient chatClient(ChatClient.Builder builder) {
    return builder
        .defaultAdvisors(AdvisorParams.ENABLE_NATIVE_STRUCTURED_OUTPUT)
        .build();
}
```

## Provider Built-in JSON Mode

Independently of `useProviderStructuredOutput()`, some AI models expose dedicated configuration options to generate structured (usually JSON) output directly:

- [OpenAI Structured Outputs](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html#_structured_outputs) can ensure the model generates responses conforming strictly to your provided JSON Schema. Choose between `JSON_OBJECT` (valid JSON) or `JSON_SCHEMA` with a supplied schema (`spring.ai.openai.chat.response-format` option).
- [Ollama](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html) provides a `spring.ai.ollama.chat.format` option to specify the response format. Currently, the only accepted value is `json`.
- [Mistral AI](https://docs.spring.io/spring-ai/reference/api/chat/mistralai-chat.html) provides a `spring.ai.mistralai.chat.response-format` option. Setting it to `{ "type": "json_object" }` enables JSON mode; setting it to `{ "type": "json_schema" }` with a supplied schema enables native structured output that matches your schema.