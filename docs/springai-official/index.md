## Introduction

![Integration Problem](https://docs.spring.io/spring-ai/reference/_images/spring_ai_logo_with_text.svg)

The `Spring AI` project aims to streamline the development of applications that incorporate artificial intelligence functionality without unnecessary complexity.

The project draws inspiration from notable Python projects, such as LangChain and LlamaIndex, but Spring AI is not a direct port of those projects. The project was founded with the belief that the next wave of Generative AI applications will not be only for Python developers but will be ubiquitous across many programming languages.

|  | Spring AI addresses the fundamental challenge of AI integration: `Connecting your enterprise Data and APIs with AI Models`. |
| --- | --- |

Spring AI provides abstractions that serve as the foundation for developing AI applications. These abstractions have multiple implementations, enabling easy component swapping with minimal code changes.

Spring AI provides the following features:

- Portable API support across AI providers for Chat, text-to-image, and Embedding models. Both synchronous and streaming API options are supported. Access to model-specific features is also available.
- Support for all major [AI Model providers](https://docs.spring.io/spring-ai/reference/api/index.html) such as Anthropic, OpenAI, Microsoft, Amazon, Google, and Ollama. Supported model types include:
- [Structured Outputs](https://docs.spring.io/spring-ai/reference/api/structured-output.html) - Mapping of AI Model output to POJOs.
- Support for all major [Vector Database providers](https://docs.spring.io/spring-ai/reference/api/vectordbs.html) such as Apache Cassandra, Azure Vector Search, Chroma, Elasticsearch, GemFire, MariaDB, Milvus, MongoDB Atlas, Neo4j, OpenSearch, Oracle, PostgreSQL/PGVector, Pinecone, Qdrant, Redis, Typesense and Weaviate.
- Portable API across Vector Store providers, including a novel SQL-like metadata filter API.
- [Tools/Function Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) - Permits the model to request the execution of client-side tools and functions, thereby accessing necessary real-time information as required and taking action.
- [Observability](https://docs.spring.io/spring-ai/reference/observability/index.html) - Provides insights into AI-related operations.
- Document ingestion [ETL framework](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html) for Data Engineering.
- [AI Model Evaluation](https://docs.spring.io/spring-ai/reference/api/testing.html) - Utilities to help evaluate generated content and protect against hallucinated response.
- [MCP (Model Context Protocol)](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-overview.html) - Seamless integration for building AI applications that consume MCP servers or expose Spring-based services to the AI ecosystem.
- Spring Boot Auto Configuration and Starters for AI Models and Vector Stores.
- [ChatClient API](https://docs.spring.io/spring-ai/reference/api/chatclient.html) - Fluent API for communicating with AI Chat Models, idiomatically similar to the WebClient and RestClient APIs.
- [Advisors API](https://docs.spring.io/spring-ai/reference/api/advisors.html) - Encapsulates recurring Generative AI patterns, transforms data sent to and from Language Models (LLMs), and provides portability across various models and use cases.
- Support for [Chat Conversation Memory](https://docs.spring.io/spring-ai/reference/api/chatclient.html#_chat_memory) and [Retrieval Augmented Generation (RAG)](https://docs.spring.io/spring-ai/reference/api/chatclient.html#_retrieval_augmented_generation).

This feature set lets you implement common use cases, such as “Q&A over your documentation” or “Chat with your documentation.”

The [concepts section](https://docs.spring.io/spring-ai/reference/concepts.html) provides a high-level overview of AI concepts and their representation in Spring AI.

The [Getting Started](https://docs.spring.io/spring-ai/reference/getting-started.html) section shows you how to create your first AI application. Subsequent sections delve into each component and common use cases with a code-focused approach.