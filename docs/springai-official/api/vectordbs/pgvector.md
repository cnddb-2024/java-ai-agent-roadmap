## PGvector

This section walks you through setting up the PGvector `VectorStore` to store document embeddings and perform similarity searches.

[PGvector](https://github.com/pgvector/pgvector) is an open-source extension for PostgreSQL that enables storing and searching over machine learning-generated embeddings. It provides different capabilities that let users identify both exact and approximate nearest neighbors. It is designed to work seamlessly with other PostgreSQL features, including indexing and querying.

## Prerequisites

First you need access to PostgreSQL instance with enabled `vector`, `hstore` and `uuid-ossp` extensions.

|  | You can run a PGvector database as a Spring Boot dev service via [Docker Compose](https://docs.spring.io/spring-ai/reference/api/docker-compose.html) or [Testcontainers](https://docs.spring.io/spring-ai/reference/api/testcontainers.html). In alternative, the [setup local Postgres/PGVector](#_run_postgres_pgvector_db_locally) appendix shows how to set up a DB locally with a Docker container. |
| --- | --- |

On startup with the schema initialization feature explicitly enabled, the `PgVectorStore` will attempt to install the required database extensions and create the required `vector_store` table with an index if not existing.

Optionally, you can do this manually like so:

```
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS vector_store (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    content text,
    metadata json,
    embedding vector(1536) // 1536 is the default embedding dimension
);

CREATE INDEX ON vector_store USING HNSW (embedding vector_cosine_ops);
```

|  | replace the `1536` with the actual embedding dimension if you are using a different dimension. PGvector supports at most 2000 dimensions for HNSW indexes. |
| --- | --- |

Next, if required, an API key for the [EmbeddingModel](https://docs.spring.io/spring-ai/reference/api/embeddings.html#available-implementations) to generate the embeddings stored by the `PgVectorStore`.

## Auto-Configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Then add the PgVectorStore boot starter dependency to your project:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-pgvector</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file.

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-pgvector'
}
```

The vector store implementation can initialize the required schema for you, but you must opt-in by specifying the `initializeSchema` boolean in the appropriate constructor or by setting `…​initialize-schema=true` in the `application.properties` file.

|  | This is a breaking change! In earlier versions of Spring AI, this schema initialization happened by default. |
| --- | --- |

The Vector Store also requires an `EmbeddingModel` instance to calculate embeddings for the documents. You can pick one of the available [EmbeddingModel Implementations](https://docs.spring.io/spring-ai/reference/api/embeddings.html#available-implementations).

For example, to use the [OpenAI EmbeddingModel](https://docs.spring.io/spring-ai/reference/api/embeddings/openai-embeddings.html), add the following dependency to your project:

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

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. Refer to the [Artifact Repositories](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories) section to add Maven Central and/or Snapshot Repositories to your build file. |
| --- | --- |

To connect to and configure the `PgVectorStore`, you need to provide access details for your instance. A simple configuration can be provided via Spring Boot’s `application.yml`.

```
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/postgres
    username: postgres
    password: postgres
  ai:
    vectorstore:
      pgvector:
        index-type: HNSW
        distance-type: COSINE_DISTANCE
        dimensions: 1536
        max-document-batch-size: 10000 # Optional: Maximum number of documents per batch
```

|  | If you run PGvector as a Spring Boot dev service via [Docker Compose](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose) or [Testcontainers](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.testcontainers), you don’t need to configure URL, username and password since they are autoconfigured by Spring Boot. |
| --- | --- |

|  | Check the list of [configuration parameters](#pgvector-properties) to learn about the default values and configuration options. |
| --- | --- |

Now you can auto-wire the `VectorStore` in your application and use it

```java
@Autowired VectorStore vectorStore;

// ...

List<Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to PGVector
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = this.vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

### Configuration properties

You can use the following properties in your Spring Boot configuration to customize the PGVector vector store.

| Property | Description | Default value |
| --- | --- | --- |
| `spring.ai.vectorstore.pgvector.index-type` | Nearest neighbor search index type. Options are `NONE` - exact nearest neighbor search, `IVFFlat` - index divides vectors into lists, and then searches a subset of those lists that are closest to the query vector. It has faster build times and uses less memory than HNSW, but has lower query performance (in terms of speed-recall tradeoff). `HNSW` - creates a multilayer graph. It has slower build times and uses more memory than IVFFlat, but has better query performance (in terms of speed-recall tradeoff). There’s no training step like IVFFlat, so the index can be created without any data in the table. | HNSW |
| `spring.ai.vectorstore.pgvector.distance-type` | Search distance type. Defaults to `COSINE_DISTANCE`. But if vectors are normalized to length 1, you can use `EUCLIDEAN_DISTANCE` or `NEGATIVE_INNER_PRODUCT` for best performance. | COSINE\_DISTANCE |
| `spring.ai.vectorstore.pgvector.dimensions` | Embeddings dimension. If not specified explicitly the PgVectorStore will retrieve the dimensions form the provided `EmbeddingModel`. Dimensions are set to the embedding column the on table creation. If you change the dimensions your would have to re-create the vector\_store table as well. | \- |
| `spring.ai.vectorstore.pgvector.remove-existing-vector-store-table` | Deletes the existing `vector_store` table on start up. | false |
| `spring.ai.vectorstore.pgvector.initialize-schema` | Whether to initialize the required schema | false |
| `spring.ai.vectorstore.pgvector.schema-name` | Vector store schema name | `public` |
| `spring.ai.vectorstore.pgvector.table-name` | Vector store table name | `vector_store` |
| `spring.ai.vectorstore.pgvector.schema-validation` | Enables schema and table name validation to ensure they are valid and existing objects. | false |
| `spring.ai.vectorstore.pgvector.max-document-batch-size` | Maximum number of documents to process in a single batch. | 10000 |

|  | If you configure a custom schema and/or table name, consider enabling schema validation by setting `spring.ai.vectorstore.pgvector.schema-validation=true`. This ensures the correctness of the names and reduces the risk of SQL injection attacks. |
| --- | --- |

## Metadata filtering

You can leverage the generic, portable [metadata filters](https://docs.spring.io/spring-ai/reference/api/vectordbs.html#_metadata_filters) with the PgVector store.

For example, you can use either the text expression language:

```java
vectorStore.similaritySearch(
    SearchRequest.builder()
    .query("The World")
    .topK(TOP_K)
    .similarityThreshold(SIMILARITY_THRESHOLD)
    .filterExpression("author in ['john', 'jill'] && article_type == 'blog'").build());
```

or programmatically using the `Filter.Expression` DSL:

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.similaritySearch(SearchRequest.builder()
    .query("The World")
    .topK(TOP_K)
    .similarityThreshold(SIMILARITY_THRESHOLD)
    .filterExpression(b.and(
        b.in("author","john", "jill"),
        b.eq("article_type", "blog")).build()).build());
```

|  | These filter expressions are converted into PostgreSQL JSON path expressions for efficient metadata filtering. |
| --- | --- |

## Manual Configuration

Instead of using the Spring Boot auto-configuration, you can manually configure the `PgVectorStore`. For this you need to add the PostgreSQL connection and `JdbcTemplate` auto-configuration dependencies to your project:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>

<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>

<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-pgvector-store</artifactId>
</dependency>
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

To configure PgVector in your application, you can use the following setup:

```java
@Bean
public VectorStore vectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel) {
    return PgVectorStore.builder(jdbcTemplate, embeddingModel)
        .dimensions(1536)                    // Optional: defaults to model dimensions or 1536
        .distanceType(COSINE_DISTANCE)       // Optional: defaults to COSINE_DISTANCE
        .indexType(HNSW)                     // Optional: defaults to HNSW
        .initializeSchema(true)              // Optional: defaults to false
        .schemaName("public")                // Optional: defaults to "public"
        .vectorTableName("vector_store")     // Optional: defaults to "vector_store"
        .maxDocumentBatchSize(10000)         // Optional: defaults to 10000
        .build();
}
```

## Run Postgres & PGVector DB locally

```
docker run -it --rm --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres pgvector/pgvector
```

You can connect to this server like this:

```
psql -U postgres -h localhost -p 5432
```

## Accessing the Native Client

The PGVector Store implementation provides access to the underlying native JDBC client (`JdbcTemplate`) through the `getNativeClient()` method:

```java
PgVectorStore vectorStore = context.getBean(PgVectorStore.class);
Optional<JdbcTemplate> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    JdbcTemplate jdbc = nativeClient.get();
    // Use the native client for PostgreSQL-specific operations
}
```

The native client gives you access to PostgreSQL-specific features and operations that might not be exposed through the `VectorStore` interface.