## GemFire Vector Store

This section walks you through setting up the `GemFireVectorStore` to store document embeddings and perform similarity searches.

[GemFire](https://tanzu.vmware.com/gemfire) is a distributed, in-memory, key-value store performing read and write operations at blazingly fast speeds. It offers highly available parallel message queues, continuous availability, and an event-driven architecture you can scale dynamically without downtime. As your data size requirements increase to support high-performance, real-time apps, GemFire can easily scale linearly.

[GemFire VectorDB](https://docs.vmware.com/en/VMware-GemFire-VectorDB/1.0/gemfire-vectordb/overview.html) extends GemFire’s capabilities, serving as a versatile vector database that efficiently stores, retrieves, and performs vector similarity searches.

## Prerequisites

1. A GemFire cluster with the GemFire VectorDB extension enabled
	- [Install GemFire VectorDB extension](https://docs.vmware.com/en/VMware-GemFire-VectorDB/1.0/gemfire-vectordb/install.html)
2. An `EmbeddingModel` bean to compute the document embeddings. Refer to the [EmbeddingModel](https://docs.spring.io/spring-ai/reference/api/embeddings.html#available-implementations) section for more information. An option that runs locally on your machine is [ONNX](https://docs.spring.io/spring-ai/reference/api/embeddings/onnx.html) and the all-MiniLM-L6-v2 Sentence Transformers.

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Add the GemFire VectorStore Spring Boot starter to you project’s Maven build file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-gemfire</artifactId>
</dependency>
```

or to your Gradle `build.gradle` file

```xml
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-gemfire'
}
```

### Configuration properties

You can use the following properties in your Spring Boot configuration to further configure the `GemFireVectorStore`.

| Property | Default value |
| --- | --- |
| `spring.ai.vectorstore.gemfire.host` | localhost |
| `spring.ai.vectorstore.gemfire.port` | 8080 |
| `spring.ai.vectorstore.gemfire.initialize-schema` | `false` |
| `spring.ai.vectorstore.gemfire.index-name` | spring-ai-gemfire-store |
| `spring.ai.vectorstore.gemfire.beam-width` | 100 |
| `spring.ai.vectorstore.gemfire.max-connections` | 16 |
| `spring.ai.vectorstore.gemfire.vector-similarity-function` | COSINE |
| `spring.ai.vectorstore.gemfire.fields` | \[\] |
| `spring.ai.vectorstore.gemfire.buckets` | 0 |
| `spring.ai.vectorstore.gemfire.username` | null |
| `spring.ai.vectorstore.gemfire.password` | null |
| `spring.ai.vectorstore.gemfire.token` | null |

## Manual Configuration

To use just the `GemFireVectorStore`, without Spring Boot’s Auto-configuration add the following dependency to your project’s Maven `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-gemfire-store</artifactId>
</dependency>
```

For Gradle users, add the following to your `build.gradle` file under the dependencies block to use just the `GemFireVectorStore`:

```
dependencies {
    implementation 'org.springframework.ai:spring-ai-gemfire-store'
}
```

## Usage

Here is a sample that creates an instance of the `GemfireVectorStore` instead of using AutoConfiguration

```java
@Bean
public GemFireVectorStore vectorStore(EmbeddingModel embeddingModel) {
    return GemFireVectorStore.builder(embeddingModel)
        .host("localhost")
        .port(7071)
        .username("my-user-name")
        .password("my-password")
        .indexName("my-vector-index")
        .fields(new String[] {"country", "year", "activationDate"}) // Optional: fields for metadata filtering
        .initializeSchema(true)
        .build();
}
```

The default configuration connects to a GemFire cluster at `localhost:8080`

- In your application, create a few documents:

```java
List<Document> documents = List.of(
   new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("country", "UK", "year", 2020)),
   new Document("The World is Big and Salvation Lurks Around the Corner", Map.of()),
   new Document("You walk forward facing the past and you turn back toward the future.", Map.of("country", "NL", "year", 2023)));
```

- Add the documents to the vector store:

```java
vectorStore.add(documents);
```

- And to retrieve documents using similarity search:

```java
List<Document> results = vectorStore.similaritySearch(
   SearchRequest.builder().query("Spring").topK(5).build());
```

You should retrieve the document containing the text "Spring AI rocks!!".

You can also limit the number of results using a similarity threshold:

```java
List<Document> results = vectorStore.similaritySearch(
   SearchRequest.builder().query("Spring").topK(5)
      .similarityThreshold(0.5d).build());
```

## Metadata Filtering

You can leverage the generic, portable [metadata filters](https://docs.spring.io/spring-ai/reference/api/vectordbs.html#metadata-filters) with GemFire VectorStore as well.

For example, you can use either the text expression language:

```java
vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(5)
        .similarityThreshold(0.7)
        .filterExpression("country == 'BG' && year >= 2020").build());
```

or programmatically using the `Filter.Expression` DSL:

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(5)
        .similarityThreshold(0.7)
        .filterExpression(b.and(
                b.eq("country", "BG"),
                b.gte("year", 2020)).build()).build());
```

|  | Those (portable) filter expressions get automatically converted into the proprietary GemFire VectorDB query format. |
| --- | --- |

For example, this portable filter expression:

```sql
country == 'BG' && year >= 2020
```

is converted into the proprietary GemFire VectorDB filter format:

```
country:BG AND year:[2020 TO *]
```

The GemFire VectorStore supports a wide range of filter operations:

- **Equality**: `country == 'BG'` → `country:BG`
- **Inequality**: `city != 'Sofia'` → `city: NOT Sofia`
- **Greater Than**: `year > 2020` → `year:{2020 TO *]`
- **Greater Than or Equal**: `year >= 2020` → `year:[2020 TO *]`
- **Less Than**: `year < 2025` → `year:[* TO 2025}`
- **Less Than or Equal**: `year ⇐ 2025` → `year:[* TO 2025]`
- **IN**: `country in ['BG', 'NL']` → `country:(BG OR NL)`
- **NOT IN**: `country nin ['BG', 'NL']` → `NOT country:(BG OR NL)`
- **AND/OR**: Logical operators for combining conditions
- **Grouping**: Use parentheses for complex expressions
- **Date Filtering**: Date values in ISO 8601 format (e.g., `2024-01-07T14:29:12Z`)

|  | To use metadata filtering with GemFire VectorStore, you must specify the metadata fields that can be filtered when creating the vector store. This is done using the `fields` parameter in the builder:  ```java GemFireVectorStore.builder(embeddingModel)     .fields(new String[] {"country", "year", "activationDate"})     .build(); ```  Or via configuration properties:  ```properties spring.ai.vectorstore.gemfire.fields=country,year,activationDate ``` |
| --- | --- |