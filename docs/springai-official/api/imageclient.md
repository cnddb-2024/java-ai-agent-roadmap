## Image Model API

The `Spring Image Model API` is designed to be a simple and portable interface for interacting with various [AI Models](https://docs.spring.io/spring-ai/reference/concepts.html#_models) specialized in image generation, allowing developers to switch between different image-related models with minimal code changes. This design aligns with Spring’s philosophy of modularity and interchangeability, ensuring developers can quickly adapt their applications to different AI capabilities related to image processing.

Additionally, with the support of companion classes like `ImagePrompt` for input encapsulation and `ImageResponse` for output handling, the Image Model API unifies the communication with AI Models dedicated to image generation. It manages the complexity of request preparation and response parsing, offering a direct and simplified API interaction for image-generation functionalities.

The Spring Image Model API is built on top of the Spring AI `Generic Model API`, providing image-specific abstractions and implementations.

## API Overview

This section provides a guide to the Spring Image Model API interface and associated classes.

## Image Model

Here is the [ImageModel](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/image/ImageModel.java) interface definition:

```java
@FunctionalInterface
public interface ImageModel extends Model<ImagePrompt, ImageResponse> {

    ImageResponse call(ImagePrompt request);

}
```

### ImagePrompt

The [ImagePrompt](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/image/ImagePrompt.java) is a `ModelRequest` that encapsulates a list of [ImageMessage](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/image/ImageMessage.java) objects and optional model request options. The following listing shows a truncated version of the `ImagePrompt` class, excluding constructors and other utility methods:

```java
public class ImagePrompt implements ModelRequest<List<ImageMessage>> {

    private final List<ImageMessage> messages;

    private ImageOptions imageModelOptions;

    @Override
    public List<ImageMessage> getInstructions() {...}

    @Override
    public ImageOptions getOptions() {...}

    // constructors and utility methods omitted
}
```

#### ImageMessage

The `ImageMessage` class encapsulates the text to use and the weight that the text should have in influencing the generated image. For models that support weights, they can be positive or negative.

```java
public class ImageMessage {

    private String text;

    private Float weight;

    public String getText() {...}

    public Float getWeight() {...}

   // constructors and utility methods omitted
}
```

#### ImageOptions

Represents the options that can be passed to the Image generation model. The `ImageOptions` interface extends the `ModelOptions` interface and is used to define few portable options that can be passed to the AI model.

The `ImageOptions` interface is defined as follows:

```java
public interface ImageOptions extends ModelOptions {

    Integer getN();

    String getModel();

    Integer getWidth();

    Integer getHeight();

    String getResponseFormat(); // openai - url or base64 : stability ai byte[] or base64

}
```

Additionally, every model specific ImageModel implementation can have its own options that can be passed to the AI model. For example, the OpenAI Image Generation model has its own options like `quality`, `style`, etc.

This is a powerful feature that allows developers to use model specific options when starting the application and then override them at runtime using the `ImagePrompt`.

### ImageResponse

The structure of the `ImageResponse` class is as follows:

```java
public class ImageResponse implements ModelResponse<ImageGeneration> {

    private final ImageResponseMetadata imageResponseMetadata;

    private final List<ImageGeneration> imageGenerations;

    @Override
    public ImageGeneration getResult() {
        // get the first result
    }

    @Override
    public List<ImageGeneration> getResults() {...}

    @Override
    public ImageResponseMetadata getMetadata() {...}

    // other methods omitted

}
```

The [ImageResponse](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-model/src/main/java/org/springframework/ai/image/ImageResponse.java) class holds the AI Model’s output, with each `ImageGeneration` instance containing one of potentially multiple outputs resulting from a single prompt.

The `ImageResponse` class also carries a `ImageResponseMetadata` object holding metadata about the AI Model’s response.

### ImageGeneration

```java
public class ImageGeneration implements ModelResult<Image> {

    private ImageGenerationMetadata imageGenerationMetadata;

    private Image image;

    @Override
    public Image getOutput() {...}

    @Override
    public ImageGenerationMetadata getMetadata() {...}

    // other methods omitted

}
```