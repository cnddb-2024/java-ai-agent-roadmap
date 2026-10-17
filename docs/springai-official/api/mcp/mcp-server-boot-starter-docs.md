## MCP Server Boot Starter

[Model Context Protocol (MCP) Servers](https://modelcontextprotocol.io/docs/learn/server-concepts) are programs that expose specific capabilities to AI applications through standardized protocol interfaces. Each server provides focused functionality for a particular domain.

The Spring AI MCP Server Boot Starters provide auto-configuration for setting up [MCP Servers](https://modelcontextprotocol.io/docs/learn/server-concepts) in Spring Boot applications. They enable seamless integration of MCP server capabilities with Spring Boot’s auto-configuration system.

The MCP Server Boot Starters offer:

- Automatic configuration of MCP server components, including tools, resources, and prompts
- Support for different MCP protocol versions, including STDIO, SSE, Streamable-HTTP, and stateless servers
- Support for both synchronous and asynchronous operation modes
- Multiple transport layer options
- Flexible tool, resource, and prompt specification
- Change notification capabilities
- [Annotation-based server development](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html) with automatic bean scanning and registration

|  | The HTTP-based server transports (SSE, Streamable-HTTP, and Stateless) expose an unauthenticated JSON-RPC endpoint by default. The starters do not apply any authentication or authorization on their own, so any client that can reach the endpoint can list and invoke every registered tool, resource, and prompt. Before exposing an MCP server beyond localhost, you must place a security boundary in front of it. See [Securing the MCP Server](#securing-the-mcp-server) for details.  This does not apply to the `STDIO` transport, which runs in-process and is not network-accessible. |
| --- | --- |

## MCP Server Boot Starters

MCP Servers support multiple protocol and transport mechanisms. Use the dedicated starter and the correct `spring.ai.mcp.server.protocol` property to configure your server:

### STDIO

| Server Type | Dependency | Property |
| --- | --- | --- |
| [Standard Input/Output (STDIO)](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html) | `spring-ai-starter-mcp-server` | `spring.ai.mcp.server.stdio=true` |

### WebMVC

| Server Type | Dependency | Property |
| --- | --- | --- |
| [SSE WebMVC](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#%3Cem%3Esse_webmvc_server) \_(deprecated since 2.0.0, use STREAMABLE instead) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=SSE` |
| [Streamable-HTTP WebMVC](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html#_streamable_http_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| [Stateless WebMVC](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html#_stateless_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STATELESS` |

### WebFlux (Reactive)

| Server Type | Dependency | Property |
| --- | --- | --- |
| [SSE WebFlux](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#%3Cem%3Esse_webflux_server) \_(deprecated since 2.0.0, use STREAMABLE instead) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=SSE` |
| [Streamable-HTTP WebFlux](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html#_streamable_http_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| [Stateless WebFlux](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html#_stateless_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STATELESS` |

## Server Capabilities

Depending on the server and transport types, MCP Servers can support various capabilities, such as:

- **Tools** - Allows servers to expose tools that can be invoked by language models
- **Resources** - Provides a standardized way for servers to expose resources to clients
- **Prompts** - Provides a standardized way for servers to expose prompt templates to clients
- **Utility/Completions** - Provides a standardized way for servers to offer argument autocompletion suggestions for prompts and resource URIs
- **Utility/Logging** - Provides a standardized way for servers to send structured log messages to clients
- **Utility/Progress** - Optional progress tracking for long-running operations through notification messages
- **Utility/Ping** - Optional health check mechanism for the server to report its status

All capabilities are enabled by default. Disabling a capability will prevent the server from registering and exposing the corresponding features to clients.

## Server Protocols

MCP provides several protocol types including:

- [**STDIO**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html) - In process (e.g. server runs inside the host application) protocol. Communication is over standard in and standard out. To enable the `STDIO` set `spring.ai.mcp.server.stdio=true`.
- [**SSE**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#_sse_webmvc_server) - Server-sent events protocol for real-time updates. The server operates as an independent process that can handle multiple client connections.
- [**Streamable-HTTP**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html) - The [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#streamable-http) allows MCP servers to operate as independent processes that can handle multiple client connections using HTTP POST and GET requests, with optional Server-Sent Events (SSE) streaming for multiple server messages. It replaces the SSE transport. To enable the `STREAMABLE` protocol, set `spring.ai.mcp.server.protocol=STREAMABLE`.
- [**Stateless**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html) - Stateless MCP servers are designed for simplified deployments where session state is not maintained between requests. They are ideal for microservices architectures and cloud-native deployments. To enable the `STATELESS` protocol, set `spring.ai.mcp.server.protocol=STATELESS`.

## Securing the MCP Server

The MCP server transports are intentionally authentication-agnostic: the auto-configuration wires up the endpoint but does not enforce authentication or authorization. As with any other Spring web endpoint, securing an HTTP-based MCP server (SSE, Streamable-HTTP, or Stateless) is the responsibility of a dedicated security layer that you add in front of it — it is not provided by the transport. Examples of security libraries are Spring Security and [MCP Security](https://github.com/spring-ai-community/mcp-security)

|  | With the default configuration the MCP endpoint (`POST /mcp` by default) accepts all requests, allowing any network-accessible client to enumerate and invoke your registered tools, resources, and prompts without credentials. Treat the registration of a tool, resource, or prompt as a decision to expose it, and secure the endpoint before deploying beyond localhost. |
| --- | --- |

## Sync/Async Server API Options

The MCP Server API supports imperative (i.e. synchronous) and reactive (e.g. asynchronous) programming models.

- **Synchronous Server** - The default server type implemented using `McpSyncServer`. It is designed for straightforward request-response patterns in your applications. To enable this server type, set `spring.ai.mcp.server.type=SYNC` in your configuration. When activated, it automatically handles the configuration of synchronous tool specifications.

**NOTE:** The SYNC server will register only synchronous MCP annotated methods. Asynchronous methods will be ignored.

- **Asynchronous Server** - The asynchronous server implementation uses `McpAsyncServer` and is optimized for non-blocking operations. To enable this server type, configure your application with `spring.ai.mcp.server.type=ASYNC`. This server type automatically sets up asynchronous tool specifications with built-in Project Reactor support.

**NOTE:** The ASYNC server will register only asynchronous MCP annotated methods. Synchronous methods will be ignored.

## MCP Server Annotations

The MCP Server Boot Starters provide comprehensive support for annotation-based server development, allowing you to create MCP servers using declarative Java annotations instead of manual configuration.

### Key Annotations

- **[@McpTool](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcptool)** - Mark methods as MCP tools with automatic JSON schema generation
- **[@McpResource](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcpresource)** - Provide access to resources via URI templates
- **[@McpPrompt](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcpprompt)** - Generate prompt messages for AI interactions
- **[@McpComplete](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcpcomplete)** - Provide auto-completion functionality for prompts

### Special Parameters

The annotation system supports [special parameter types](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-special-params.html) that provide additional context:

- **`McpMeta`** - Access metadata from MCP requests
- **`@McpProgressToken`** - Receive progress tokens for long-running operations
- **`McpSyncServerExchange`/`McpAsyncServerExchange`** - Full server context for advanced operations
- **`McpTransportContext`** - Lightweight context for stateless operations
- **`CallToolRequest`** - Dynamic schema support for flexible tools

### Simple Example

```java
@Component
public class CalculatorTools {

    @McpTool(name = "add", description = "Add two numbers together")
    public int add(
            @McpToolParam(description = "First number", required = true) int a,
            @McpToolParam(description = "Second number", required = true) int b) {
        return a + b;
    }

    @McpResource(uri = "config://{key}", name = "Configuration")
    public String getConfig(String key) {
        return configData.get(key);
    }
}
```

### Adding data to McpTransportContext

By default, the `McpTransportContext` is empty (`McpTransportContext.EMPTY`). This is by design, to keep the MCP server transport-agnostic.

If you need transport-specific metadata (for example, HTTP headers, remote host, etc) in your tools, configure a `TransportContextExtractor` on your transport provider.

For WebMVC:

```java
@Bean
public WebMvcStreamableServerTransportProvider transport() {
    return WebMvcStreamableServerTransportProvider.builder()
        .contextExtractor(serverRequest -> {
            String authorization = serverRequest.headers().firstHeader("Authorization");
            return McpTransportContext.create(Map.of("authorization", authorization));
        })
        .build();
}
```

For WebFlux (reactive):

```java
@Bean
public WebFluxStreamableServerTransportProvider transport() {
    return WebFluxStreamableServerTransportProvider.builder()
        .contextExtractor(serverRequest -> {
            String authorization = serverRequest.headers().firstHeader("Authorization");
            return McpTransportContext.create(Map.of("authorization", authorization));
        })
        .build();
}
```

Once configured, access the context via `McpSyncRequestContext` (or `McpAsyncRequestContext`) in your tool.

```java
@McpTool
public String accessProtectedResource(McpSyncRequestContext requestContext) {
    McpTransportContext context = requestContext.transportContext();
    String authorization = (String) context.get("authorization");

    return "Successfully accessed protected resource.";
}
```

### Auto-Configuration

With Spring Boot auto-configuration, annotated beans are automatically detected and registered:

```java
@SpringBootApplication
public class McpServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }
}
```

The auto-configuration will:

### Configuration Properties

Configure the server annotation scanner:

```yaml
spring:
  ai:
    mcp:
      server:
        type: SYNC  # or ASYNC
        annotation-scanner:
          enabled: true
```

## Example Applications

- [Weather Server (SSE WebFlux)](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/starter-webflux-server) - Spring AI MCP Server Boot Starter with WebFlux transport
- [Weather Server (STDIO)](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/starter-stdio-server) - Spring AI MCP Server Boot Starter with STDIO transport
- [Weather Server Manual Configuration](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/manual-webflux-server) - Spring AI MCP Server Boot Starter that doesn’t use auto-configuration but uses the Java SDK to configure the server manually
- Streamable-HTTP WebFlux/WebMVC Example - TODO
- Stateless WebFlux/WebMVC Example - TODO

## Additional Resources

- [MCP Server Annotations](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html) - Declarative server development with annotations
- [Special Parameters](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-special-params.html) - Advanced parameter injection and context access
- [MCP Annotations Examples](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-examples.html) - Comprehensive examples and use cases
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification)
- [Spring Boot Auto-configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration)