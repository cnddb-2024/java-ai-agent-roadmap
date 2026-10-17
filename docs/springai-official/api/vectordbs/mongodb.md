## MongoDB Atlas

This section walks you through setting up MongoDB Atlas as a vector store to use with Spring AI.

## What is MongoDB Atlas?

[MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) is the fully-managed cloud database from MongoDB available in AWS, Azure, and GCP. Atlas supports native Vector Search and full text search on your MongoDB document data.

[MongoDB Atlas Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search) allows you to store your embeddings in MongoDB documents, create vector search indexes, and perform KNN searches with an approximate nearest neighbor algorithm (Hierarchical Navigable Small Worlds). You can use the `$vectorSearch` aggregation operator in a MongoDB aggregation stage to perform a search on your vector embeddings.

## Prerequisites

- An Atlas cluster running MongoDB version 6.0.11, 7.0.2, or later. To get started with MongoDB Atlas, you can follow the instructions [here](https://www.mongodb.com/docs/atlas/getting-started/). Ensure that your IP address is included in your Atlas project’s [access list](https://www.mongodb.com/docs/atlas/security/ip-access-list/#std-label-access-list).
- A running MongoDB Atlas instance with Vector Search enabled
- Collection with vector search index configured
- Collection schema with id (string), content (string), metadata (document), and embedding (vector) fields
- Proper access permissions for index and collection operations

## Auto-configuration

There has been a significant change in the Spring AI auto-configuration, starter modules' artifact names. Please refer to the [upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html) for more information.

Spring AI provides Spring Boot auto-configuration for the MongoDB Atlas Vector Store. To enable it, add the following dependency to your project’s Maven `pom.xml` file:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-mongodb-atlas</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file:

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-mongodb-atlas'
}
```

|  | Refer to the [Dependency Management](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) section to add the Spring AI BOM to your build file. |
| --- | --- |

|  | Refer to the [Artifact Repositories](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories) section to add Maven Central and/or Snapshot Repositories to your build file. |
| --- | --- |

The vector store implementation can initialize the requisite schema for you, but you must opt-in by setting `spring.ai.vectorstore.mongodb.initialize-schema=true` in the `application.properties` file. Alternatively you can opt-out the initialization and create the index manually using the MongoDB Atlas UI, Atlas Administration API, or Atlas CLI, which can be useful if the index needs advanced mapping or additional configuration.

|  | this is a breaking change! In earlier versions of Spring AI, this schema initialization happened by default. |
| --- | --- |

Please have a look at the list of [configuration parameters](#mongodbvector-properties) for the vector store to learn about the default values and configuration options.

Additionally, you will need a configured `EmbeddingModel` bean. Refer to the [EmbeddingModel](https://docs.spring.io/spring-ai/reference/api/embeddings.html#available-implementations) section for more information.

Now you can auto-wire the `MongoDBAtlasVectorStore` as a vector store in your application:

```java
@Autowired VectorStore vectorStore;

// ...

List<Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to MongoDB Atlas
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

### Configuration Properties

To connect to MongoDB Atlas and use the `MongoDBAtlasVectorStore`, you need to provide access details for your instance. A simple configuration can be provided via Spring Boot’s `application.yml`:

```yaml
spring:
  data:
    mongodb:
      uri: <mongodb atlas connection string>
      database: <database name>
  ai:
    vectorstore:
      mongodb:
        initialize-schema: true
        collection-name: custom_vector_store
        index-name: custom_vector_index
        path-name: custom_embedding
        metadata-fields-to-filter: author,year
```

Properties starting with `spring.ai.vectorstore.mongodb.*` are used to configure the `MongoDBAtlasVectorStore`:

| Property | Description | Default Value |
| --- | --- | --- |
| `spring.ai.vectorstore.mongodb.initialize-schema` | Whether to initialize the required schema | `false` |
| `spring.ai.vectorstore.mongodb.collection-name` | The name of the collection to store the vectors | `vector_store` |
| `spring.ai.vectorstore.mongodb.index-name` | The name of the vector search index | `vector_index` |
| `spring.ai.vectorstore.mongodb.path-name` | The path where vectors are stored | `embedding` |
| `spring.ai.vectorstore.mongodb.metadata-fields-to-filter` | Comma-separated list of metadata fields that can be used for filtering | empty list |

## Manual Configuration

Instead of using the Spring Boot auto-configuration, you can manually configure the MongoDB Atlas vector store. For this you need to add the `spring-ai-mongodb-atlas-store` to your project:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mongodb-atlas-store</artifactId>
</dependency>
```

or to your Gradle `build.gradle` build file:

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-mongodb-atlas-store'
}
```

Create a `MongoTemplate` bean:

```java
@Bean
public MongoTemplate mongoTemplate() {
    return new MongoTemplate(MongoClients.create("<mongodb atlas connection string>"), "<database name>");
}
```

Then create the `MongoDBAtlasVectorStore` bean using the builder pattern:

```java
@Bean
public VectorStore vectorStore(MongoTemplate mongoTemplate, EmbeddingModel embeddingModel) {
    return MongoDBAtlasVectorStore.builder(mongoTemplate, embeddingModel)
        .collectionName("custom_vector_store")           // Optional: defaults to "vector_store"
        .vectorIndexName("custom_vector_index")          // Optional: defaults to "vector_index"
        .pathName("custom_embedding")                    // Optional: defaults to "embedding"
        .numCandidates(500)                             // Optional: defaults to 200
        .metadataFieldsToFilter(List.of("author", "year")) // Optional: defaults to empty list
        .initializeSchema(true)                         // Optional: defaults to false
        .batchingStrategy(new TokenCountBatchingStrategy()) // Optional: defaults to TokenCountBatchingStrategy
        .build();
}

// This can be any EmbeddingModel implementation
@Bean
public EmbeddingModel embeddingModel() {
    return new OpenAiEmbeddingModel(OpenAiEmbeddingOptions.builder().apiKey(System.getenv("OPENAI_API_KEY")).build());
}
```

## Metadata Filtering

You can leverage the generic, portable [metadata filters](https://docs.spring.io/spring-ai/reference/api/vectordbs.html#metadata-filters) with MongoDB Atlas as well.

For example, you can use either the text expression language:

```java
vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(5)
        .similarityThreshold(0.7)
        .filterExpression("author in ['john', 'jill'] && article_type == 'blog'").build());
```

or programmatically using the `Filter.Expression` DSL:

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(5)
        .similarityThreshold(0.7)
        .filterExpression(b.and(
                b.in("author", "john", "jill"),
                b.eq("article_type", "blog")).build()).build());
```

|  | Those (portable) filter expressions get automatically converted into the proprietary MongoDB Atlas filter expressions. |
| --- | --- |

For example, this portable filter expression:

```sql
author in ['john', 'jill'] && article_type == 'blog'
```

is converted into the proprietary MongoDB Atlas filter format:

```json
{
  "$and": [
    {
      "$or": [
        { "metadata.author": "john" },
        { "metadata.author": "jill" }
      ]
    },
    {
      "metadata.article_type": "blog"
    }
  ]
}
```

## Tutorials and Code Examples

To get started with Spring AI and MongoDB:

- See the [Getting Started guide for Spring AI Integration](https://www.mongodb.com/docs/atlas/atlas-vector-search/ai-integrations/spring-ai/#std-label-spring-ai).
- For a comprehensive code example demonstrating Retrieval Augmented Generation (RAG) with Spring AI and MongoDB, refer to this [detailed tutorial](https://www.mongodb.com/developer/languages/java/retrieval-augmented-generation-spring-ai/).

## Accessing the Native Client

The MongoDB Atlas Vector Store implementation provides access to the underlying native MongoDB client (`MongoClient`) through the `getNativeClient()` method:

```java
MongoDBAtlasVectorStore vectorStore = context.getBean(MongoDBAtlasVectorStore.class);
Optional<MongoClient> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    MongoClient client = nativeClient.get();
    // Use the native client for MongoDB-specific operations
}
```

The native client gives you access to MongoDB-specific features and operations that might not be exposed through the `VectorStore` interface.