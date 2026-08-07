# Qdrant 向量数据库本地部署作业

## 部署方式：Docker Compose

### 第一步：创建目录并进入

```bash
sudo mkdir -p /opt/qdrant
cd /opt/qdrant
```

### 第二步：写入 docker-compose.yml

```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
    restart: unless-stopped
```

使用 cat 一键写入：

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
    restart: unless-stopped
EOF
```

### 第三步：配置 API Key

```bash
echo "QDRANT_API_KEY=vI5zT6xO7nP7qI5xS3tN2uJ0yH4gQ6yN" > .env
```

### 第四步：启动容器

```bash
docker-compose up -d
docker-compose ps
```

## 验证部署 & Dashboard

### curl 探活

```bash
curl http://localhost:6333/
```

返回示例：

```json
{"title":"qdrant - vector search engine","version":"1.19.0","commit":"74f3e85b9473c62560006c043e13737ce6b48412"}
```

### 打开 Web Dashboard

浏览器访问 `http://localhost:6333/dashboard`，输入配好的 API Key。

## Spring AI 集成

### Maven 依赖

```xml
<!-- Spring AI Qdrant 向量存储启动器 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-qdrant</artifactId>
</dependency>

<!-- Embedding 模型 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

### application.properties 配置

```properties
spring.ai.vectorstore.qdrant.host=192.168.159.129
spring.ai.vectorstore.qdrant.port=6334
spring.ai.vectorstore.qdrant.api-key=${QDRANT_API_KEY}
spring.ai.vectorstore.qdrant.collection-name=my_collection
spring.ai.vectorstore.qdrant.use-tls=false
spring.ai.vectorstore.qdrant.initialize-schema=true
```

### 存储文档 & 相似性搜索

```java
@Autowired VectorStore vectorStore;

// 存储文档（自动 Embedding + 写入 Qdrant）
List<Document> documents = List.of(
    new Document("Spring AI 让 Java 开发者轻松集成 AI 能力",
        Map.of("author", "spring", "type", "framework")),
    new Document("Qdrant 提供高性能向量检索和元数据过滤",
        Map.of("author", "qdrant", "type", "database"))
);
vectorStore.add(documents);

// 相似性搜索
List<Document> results = vectorStore.similaritySearch(
    SearchRequest.builder()
        .query("Java AI 框架")
        .topK(5)
        .build()
);
```

### 元数据过滤

```java
// 文本表达式方式
vectorStore.similaritySearch(
    SearchRequest.builder()
        .query("向量检索")
        .filterExpression("author in ['qdrant'] && type == 'database'")
        .build()
);

// FilterExpressionBuilder DSL
FilterExpressionBuilder b = new FilterExpressionBuilder();
vectorStore.similaritySearch(
    SearchRequest.builder()
        .query("向量检索")
        .filterExpression(b.and(
            b.in("author", "qdrant"),
            b.eq("type", "database")
        ).build())
        .build()
);
```

## 关键端口说明

| 端口 | 协议 | 用途 |
|------|------|------|
| 6333 | HTTP | REST API + Dashboard |
| 6334 | gRPC | Spring AI 默认使用（高性能） |

## 代码仓库

- Spring AI 集成代码：https://github.com/cnddb-2024/spring-ai-quickstart.git
  - `pom.xml`：添加 `spring-ai-starter-vector-store-qdrant` 依赖
  - `config/CommonConfig.java`：VectorStore 注入 + 文档存储 + 相似性搜索 + 元数据过滤示例
  - `application.properties`：Qdrant 连接配置（已 gitignore，不入库）
