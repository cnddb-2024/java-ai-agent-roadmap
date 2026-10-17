## Getting Started with Model Context Protocol (MCP)

The Model Context Protocol (MCP) standardizes how AI applications interact with external tools and resources.

Spring joined the MCP ecosystem early as a key contributor, helping to develop and maintain the [official MCP Java SDK](https://github.com/modelcontextprotocol/java-sdk) that serves as the foundation for Java-based MCP implementations. Building on this contribution, Spring AI provides MCP support through Boot Starters and annotations, making it easy to build both MCP servers and clients.

## Introduction Video

**[Introduction to Model Context Protocol (MCP) - YouTube](https://www.youtube.com/watch?v=FLpS7OfD5-s)**

Start here for an introductory overview of the Model Context Protocol, explaining core concepts and architecture.

## Complete Tutorial and Source Code

**📖 Blog Tutorial:** [Connect Your AI to Everything](https://spring.io/blog/2025/09/16/spring-ai-mcp-intro-blog)

**💻 Complete Source Code:** [MCP Weather Example Repository](https://github.com/tzolov/spring-ai-mcp-blogpost)

The tutorial covers the essentials of MCP development with Spring AI, including advanced features, and deployment patterns. All code examples below are taken from this tutorial.

## Quick Start

The fastest way to get started is with Spring AI’s annotation-based approach. The following examples are from the blog tutorial:

### Simple MCP Server

```java
@Service
public class WeatherService {

    @McpTool(description = "Get current temperature for a location")
    public String getTemperature(
            @McpToolParam(description = "City name", required = true) String city) {
        return String.format("Current temperature in %s: 22°C", city);
    }
}
```

Add the dependency and configure:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server-webmvc</artifactId>
</dependency>
```

```properties
spring.ai.mcp.server.protocol=STREAMABLE
```

### Simple MCP Client

```java
@Bean
public CommandLineRunner demo(ChatClient chatClient, ToolCallbackProvider mcpTools) {
    return args -> {
        String response = chatClient
            .prompt("What's the weather like in Paris?")
            .tools(mcpTools)
            .call()
            .content();
        System.out.println(response);
    };
}
```

Add the dependency and configure:

```xml
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

```yaml
spring:
  ai:
    mcp:
      client:
        streamable-http:
          connections:
            weather-server:
              url: http://localhost:8080
```

## Learning Resources

### Implementation Video

A video walkthrough of Spring AI’s MCP integration, covering both server and client implementations.