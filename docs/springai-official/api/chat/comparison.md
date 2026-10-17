## Chat Models Comparison

This table compares various Chat Models supported by Spring AI, detailing their capabilities:

- [Multimodality](https://docs.spring.io/spring-ai/reference/api/multimodality.html): The types of input the model can process (e.g., text, image, audio, video).
- [Tools/Function Calling](https://docs.spring.io/spring-ai/reference/api/tools.html): Whether the model supports function calling or tool use.
- Streaming: If the model offers streaming responses.
- Retry: Support for retry mechanisms.
- [Observability](https://docs.spring.io/spring-ai/reference/observability/index.html): Features for monitoring and debugging.
- [Built-in JSON](https://docs.spring.io/spring-ai/reference/api/structured-output/native.html#_provider_built_in_json_mode): Native support for JSON output.
- Local deployment: Whether the model can be run locally.
- OpenAI API Compatibility: If the model is compatible with OpenAI’s API.

| Provider | Multimodality | Tools/Functions | Streaming | Retry | Observability | Built-in JSON | Local | OpenAI API Compatible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Anthropic Claude](https://docs.spring.io/spring-ai/reference/api/chat/anthropic-chat.html) | text, pdf, image |  |  |  |  |  |  |  |
| [DeepSeek (OpenAI-proxy)](https://docs.spring.io/spring-ai/reference/api/chat/deepseek-chat.html) | text |  |  |  |  |  |  |  |
| [Google GenAI](https://docs.spring.io/spring-ai/reference/api/chat/google-genai-chat.html) | text, pdf, image, audio, video |  |  |  |  |  |  |  |
| [Groq (OpenAI-proxy)](https://docs.spring.io/spring-ai/reference/api/chat/groq-chat.html) | text, image |  |  |  |  |  |  |  |
| [Mistral AI](https://docs.spring.io/spring-ai/reference/api/chat/mistralai-chat.html) | text, image, audio |  |  |  |  |  |  |  |
| [MiniMax (Anthropic-proxy)](https://docs.spring.io/spring-ai/reference/api/chat/minimax-chat.html) | text, image |  |  |  |  |  |  |  |
| [NVIDIA (OpenAI-proxy)](https://docs.spring.io/spring-ai/reference/api/chat/nvidia-chat.html) | text, image |  |  |  |  |  |  |  |
| [Ollama](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html) | text, image |  |  |  |  |  |  |  |
| [OpenAI](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html) | In: text, image, audio Out: text, audio |  |  |  |  |  |  |  |
| [Perplexity (OpenAI-proxy)](https://docs.spring.io/spring-ai/reference/api/chat/perplexity-chat.html) | text |  |  |  |  |  |  |  |
| [Amazon Bedrock Converse](https://docs.spring.io/spring-ai/reference/api/chat/bedrock-converse.html) | text, image, video, docs (pdf, html, md, docx …) |  |  |  |  |  |  |  |