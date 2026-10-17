## Docker Compose

Spring AI provides Spring Boot auto-configuration for establishing a connection to a model service or vector store running via Docker Compose. To enable it, add the following dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-spring-boot-docker-compose</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file.

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-spring-boot-docker-compose'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

## Service Connections

The following service connection factories are provided in the `spring-ai-spring-boot-docker-compose` module:

| Connection Details | Matched on |
| --- | --- |
| `AwsOpenSearchConnectionDetails` | Containers named `localstack/localstack` |
| `ChromaConnectionDetails` | Containers named `chromadb/chroma`, `ghcr.io/chroma-core/chroma` |
| `MilvusServiceClientConnectionDetails` | Containers named `milvusdb/milvus` |
| `OllamaConnectionDetails` | Containers named `ollama/ollama` |
| `OpenSearchConnectionDetails` | Containers named `opensearchproject/opensearch` |
| `QdrantConnectionDetails` | Containers named `qdrant/qdrant` |
| `TypesenseConnectionDetails` | Containers named `typesense/typesense` |
| `WeaviateConnectionDetails` | Containers named `semitechnologies/weaviate`, `cr.weaviate.io/semitechnologies/weaviate` |
| `McpSseClientConnectionDetails` | Containers named `docker/mcp-gateway` |

More service connections are provided by the spring boot module `spring-boot-docker-compose`. Refer to the [Docker Compose Support](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose) documentation page for the full list.