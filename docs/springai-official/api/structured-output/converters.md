## Output Converters

The [high-level `.entity(…​)` API](https://docs.spring.io/spring-ai/reference/api/structured-output.html) is built on top of the `StructuredOutputConverter` abstraction. Most applications never touch it directly. Reach for this lower-level API when you need to:

- parse output the built-in converters reject (for example, JSON wrapped in markdown code fences);
- produce a non-JSON format such as YAML or CSV;
- use a converter directly against the low-level [`ChatModel`](https://docs.spring.io/spring-ai/reference/api/chatmodel.html) API.

Spring AI `Structured Output Converters` convert the LLM output into a structured format. As shown in the following diagram, this approach operates around the LLM text completion endpoint:

![Structured Output Converter Architecture](https://docs.spring.io/spring-ai/reference/_images/structured-output-architecture.jpg)

The structured output converter plays a role before and after the LLM call. Before the call, the converter appends format instructions to the prompt, guiding the model to generate the desired output structure. After the call, the converter parses the model’s text output and maps it into instances of the structured type.

|  | The `StructuredOutputConverter` is a best effort to convert the model output into a structured output. The AI Model is not guaranteed to return the structured output as requested. Consider combining it with [schema validation](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html) to ensure the model output is as expected. |
| --- | --- |

|  | The `StructuredOutputConverter` is not used for LLM [Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html), as this feature inherently provides structured outputs by default. |
| --- | --- |

## Structured Output API

The `StructuredOutputConverter` interface allows you to obtain structured output, such as mapping the output to a Java class or an array of values from the text-based AI Model output. The interface definition is:

```java
public interface StructuredOutputConverter<T> extends Converter<String, T>, FormatProvider {

    /**
     * Returns the JSON schema for the structured output of an LLM call,
     * or NO_JSON_SCHEMA ("") if not available.
     */
    default String getJsonSchema() {
        return NO_JSON_SCHEMA;
    }

}
```

It combines the Spring [Converter<String, T>](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/convert/converter/Converter.html) interface and the `FormatProvider` interface:

```java
public interface FormatProvider {
    String getFormat();
}
```

The following diagram shows the data flow when using the structured output API.

![Structured Output API](https://docs.spring.io/spring-ai/reference/_images/structured-output-api.jpg)

The `FormatProvider` supplies specific formatting guidelines to the AI Model, enabling it to produce text outputs that can be converted into the designated target type `T` using the `Converter`. Here is an example of such formatting instructions:

```
Your response should be in JSON format.
The data structure for the JSON should match this Java class: java.util.HashMap
Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.
```

The format instructions are most often appended to the end of the user input using the [PromptTemplate](https://docs.spring.io/spring-ai/reference/api/prompt.html#_prompttemplate) like this:

```java
StructuredOutputConverter outputConverter = ...
String userInputTemplate = """
    ... user text input ....
    {format}
    """; // user input with a "format" placeholder.
Prompt prompt = new Prompt(
        PromptTemplate.builder()
                .template(this.userInputTemplate)
                .variables(Map.of(..., "format", this.outputConverter.getFormat())) // replace the "format" placeholder with the converter's format.
                .build().createMessage()
);
```

The `Converter<String, T>` is responsible for transforming output text from the model into instances of the specified type `T`.

### The Role of getJsonSchema()

Added in 2.0 as a default method on `StructuredOutputConverter`, `getJsonSchema()` is the bridge that lets a converter participate in [`useProviderStructuredOutput()`](https://docs.spring.io/spring-ai/reference/api/structured-output/native.html) and [`validateSchema()`](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html). Implement it to return your schema (typically by delegating to a `BeanOutputConverter`) and both switches work; leave it at the default and both switches become no-ops for that converter.

### Available Converters

Spring AI provides `AbstractConversionServiceOutputConverter`, `AbstractMessageOutputConverter`, `BeanOutputConverter`, `MapOutputConverter` and `ListOutputConverter` implementations:

![Structured Output Class Hierarchy](https://docs.spring.io/spring-ai/reference/_images/structured-output-hierarchy4.jpg)

- `AbstractConversionServiceOutputConverter<T>` - Offers a pre-configured [GenericConversionService](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/convert/support/GenericConversionService.html) for transforming LLM output into the desired format. No default `FormatProvider` implementation is provided.
- `AbstractMessageOutputConverter<T>` - Supplies a pre-configured [MessageConverter](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/jms/support/converter/MessageConverter.html) for converting LLM output into the desired format. No default `FormatProvider` implementation is provided.
- `BeanOutputConverter<T>` - Configured with a designated Java class (e.g., Bean) or a [ParameterizedTypeReference](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/ParameterizedTypeReference.html), this converter employs a `FormatProvider` implementation that directs the AI Model to produce a JSON response compliant with a `DRAFT_2020_12` JSON Schema derived from the specified Java class. Subsequently, it utilizes a `JsonMapper` to deserialize the JSON output into a Java object instance of the target class.
- `MapOutputConverter` - Extends the functionality of `AbstractMessageOutputConverter` with a `FormatProvider` implementation that guides the AI Model to generate an RFC8259 compliant JSON response. Additionally, it incorporates a converter implementation that utilizes the provided `MessageConverter` to translate the JSON payload into a `java.util.Map<String, Object>` instance.
- `ListOutputConverter` - Extends the `AbstractConversionServiceOutputConverter` and includes a `FormatProvider` implementation tailored for comma-delimited list output. The converter implementation employs the provided `ConversionService` to transform the model text output into a `java.util.List`.

## Using Converters

The following sections show how to use the available converters to generate structured outputs. Each is shown both with the high-level `ChatClient` API and the low-level `ChatModel` API.

### Bean Output Converter

The following example shows how to use `BeanOutputConverter` to generate the filmography for an actor.

The target record representing the actor’s filmography:

```java
record ActorsFilms(String actor, List<String> movies) {
}
```

Here is how to apply the `BeanOutputConverter` using the high-level, fluent `ChatClient` API:

```java
ActorsFilms actorsFilms = ChatClient.create(chatModel).prompt()
        .user(u -> u.text("Generate the filmography of 5 movies for {actor}.")
                    .param("actor", "Tom Hanks"))
        .call()
        .entity(ActorsFilms.class);
```

or using the low-level `ChatModel` API directly:

```java
BeanOutputConverter<ActorsFilms> beanOutputConverter =
    new BeanOutputConverter<>(ActorsFilms.class);

String format = this.beanOutputConverter.getFormat();

String actor = "Tom Hanks";

String template = """
        Generate the filmography of 5 movies for {actor}.
        {format}
        """;

Generation generation = chatModel.call(
    PromptTemplate.builder().template(this.template).variables(Map.of("actor", this.actor, "format", this.format)).build().create()).getResult();

ActorsFilms actorsFilms = this.beanOutputConverter.convert(this.generation.getOutput().getText());
```

#### Property Ordering in Generated Schema

The `BeanOutputConverter` supports custom property ordering in the generated JSON schema through the `@JsonPropertyOrder` annotation. This annotation allows you to specify the exact sequence in which properties should appear in the schema, regardless of their declaration order in the class or record.

For example, to ensure specific ordering of properties in the `ActorsFilms` record:

```java
@JsonPropertyOrder({"actor", "movies"})
record ActorsFilms(String actor, List<String> movies) {}
```

This annotation works with both records and regular Java classes.

#### Generic Bean Types

Use the `ParameterizedTypeReference` constructor to specify a more complex target class structure. For example, to represent a list of actors and their filmographies:

```java
List<ActorsFilms> actorsFilms = ChatClient.create(chatModel).prompt()
        .user("Generate the filmography of 5 movies for Tom Hanks and Bill Murray.")
        .call()
        .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {});
```

or using the low-level `ChatModel` API directly:

```java
BeanOutputConverter<List<ActorsFilms>> outputConverter = new BeanOutputConverter<>(
        new ParameterizedTypeReference<List<ActorsFilms>>() { });

String format = this.outputConverter.getFormat();
String template = """
        Generate the filmography of 5 movies for Tom Hanks and Bill Murray.
        {format}
        """;

Prompt prompt = PromptTemplate.builder().template(this.template).variables(Map.of("format", this.format)).build().create();

Generation generation = chatModel.call(this.prompt).getResult();

List<ActorsFilms> actorsFilms = this.outputConverter.convert(this.generation.getOutput().getText());
```

### Map Output Converter

The following snippet shows how to use `MapOutputConverter` to convert the model output to a list of numbers in a map.

```java
Map<String, Object> result = ChatClient.create(chatModel).prompt()
        .user(u -> u.text("Provide me a List of {subject}")
                    .param("subject", "an array of numbers from 1 to 9 under they key name 'numbers'"))
        .call()
        .entity(new ParameterizedTypeReference<Map<String, Object>>() {});
```

or using the low-level `ChatModel` API directly:

```java
MapOutputConverter mapOutputConverter = new MapOutputConverter();

String format = this.mapOutputConverter.getFormat();
String template = """
        Provide me a List of {subject}
        {format}
        """;

Prompt prompt = PromptTemplate.builder().template(this.template)
.variables(Map.of("subject", "an array of numbers from 1 to 9 under they key name 'numbers'", "format", this.format)).build().create();

Generation generation = chatModel.call(this.prompt).getResult();

Map<String, Object> result = this.mapOutputConverter.convert(this.generation.getOutput().getText());
```

### List Output Converter

The following snippet shows how to use `ListOutputConverter` to convert the model output into a list of ice cream flavors.

```java
List<String> flavors = ChatClient.create(chatModel).prompt()
                .user(u -> u.text("List five {subject}")
                            .param("subject", "ice cream flavors"))
                .call()
                .entity(new ListOutputConverter(new DefaultConversionService()));
```

or using the low-level `ChatModel` API directly:

```java
ListOutputConverter listOutputConverter = new ListOutputConverter(new DefaultConversionService());

String format = this.listOutputConverter.getFormat();
String template = """
        List five {subject}
        {format}
        """;

Prompt prompt = PromptTemplate.builder().template(this.template).variables(Map.of("subject", "ice cream flavors", "format", this.format)).build().create();

Generation generation = this.chatModel.call(this.prompt).getResult();

List<String> list = this.listOutputConverter.convert(this.generation.getOutput().getText());
```

## Custom Converters

The built-in `BeanOutputConverter` is strict: it expects the model’s response to be parseable JSON, full stop. But models often wrap their JSON in markdown code fences:

````text
Here's the filmography:
```json
{ "actor": "Tom Hanks", "movies": ["Forrest Gump", "Cast Away"] }
```
````

`BeanOutputConverter` will throw on the first `H` of "Here’s". The common fix is a custom converter that strips fences and extracts the JSON before delegating to the default parser:

````java
public class LenientJsonOutputConverter<T> implements StructuredOutputConverter<T> {

    private static final Pattern FENCE = Pattern.compile("```(?:json)?\\s*([\\s\\S]*?)```");

    private final BeanOutputConverter<T> delegate;

    public LenientJsonOutputConverter(Class<T> targetType) {
        this.delegate = new BeanOutputConverter<>(targetType);
    }

    @Override public String getFormat()     { return delegate.getFormat(); }
    @Override public String getJsonSchema() { return delegate.getJsonSchema(); }

    @Override
    public T convert(String source) {
        var matcher = FENCE.matcher(source);
        String json = matcher.find() ? matcher.group(1).trim() : source.trim();
        return delegate.convert(json);
    }
}
````

Pass it to `.entity(…​)` instead of a `Class`:

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(new LenientJsonOutputConverter<>(ActorsFilms.class));
```

Because this converter delegates `getJsonSchema()` to the underlying `BeanOutputConverter`, both reliability switches still work — [`validateSchema()`](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html) and [`useProviderStructuredOutput()`](https://docs.spring.io/spring-ai/reference/api/structured-output/native.html) operate against the same schema the default converter would use. See [The Role of `getJsonSchema()`](#_getjsonschema).

### Non-JSON Formats

For formats outside JSON’s reach — YAML for config generators, CSV for data extraction — implement `StructuredOutputConverter` from scratch: write your own `getFormat()` prompt and your own `convert(…​)` parser. Leave `getJsonSchema()` at its default, and both reliability switches sit out — the prompt-based path runs as it does for the built-ins.