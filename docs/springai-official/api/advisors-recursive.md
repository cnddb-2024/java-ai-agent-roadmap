## Recursive Advisors

## What is a Recursive Advisor?

![Advisors Recursive](https://docs.spring.io/spring-ai/reference/_images/advisors-recursive.png)

Advisors Recursive

Recursive advisors are a special type of advisor that can loop through the downstream advisor chain multiple times. This pattern is useful when you need to repeatedly call the LLM until a certain condition is met, such as:

- Executing tool calls in a loop until no more tools need to be called
- Validating structured output and retrying if validation fails
- Implementing evaluation logic with modifications to the request
- Implementing retry logic with modifications to the request

The `CallAdvisorChain.copy(CallAdvisor after)` method is the key utility that enables recursive advisor patterns. It creates a new advisor chain that contains only the advisors that come after the specified advisor in the original chain and allows the recursive advisor to call this sub-chain as needed. This approach ensures that:

- The recursive advisor can loop through the remaining advisors in the chain
- Other advisors in the chain can observe and intercept each iteration
- The advisor chain maintains proper ordering and observability
- The recursive advisor doesn’t re-execute advisors that came before it

## Built-in Recursive Advisors

Spring AI ships two built-in recursive advisors that demonstrate this pattern.

### ToolCallingAdvisor

`ToolCallingAdvisor` implements the tool calling loop as part of the advisor chain rather than relying on per-`ChatModel` internal execution. It is auto-registered by `DefaultChatClient` whenever tools are present and is the default mechanism through which `ChatClient` drives tool-augmented conversations.

Highlights:

- Loops through the advisor chain until the `ToolExecutionEligibilityChecker` reports no more tool calls.
- Uses `callAdvisorChain.copy(this)` to create a sub-chain for recursive calls — other advisors can observe and intercept every iteration.
- Supports return-direct: when a tool’s result has `returnDirect = true`, the advisor breaks the loop and returns the tool result to the caller without sending it back to the LLM.
- Implements the `ToolAdvisor` marker interface, which `DefaultChatClient` uses to enforce the single-tool-advisor invariant — custom subclasses register transparently as replacements.
- Accumulates token usage across every iteration of the loop, so the final `ChatResponse` reports the cumulative usage of all model calls rather than only the last one (see [Cumulative Usage Across Multi-Step Flows](https://docs.spring.io/spring-ai/reference/api/usage-handling.html#_cumulative_usage_across_multi_step_flows)).

Short example:

```java
var toolCallingAdvisor = ToolCallingAdvisor.builder()
    .toolCallingManager(toolCallingManager)
    .advisorOrder(BaseAdvisor.HIGHEST_PRECEDENCE + 300)
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(toolCallingAdvisor)
    .build();
```

For the full builder API, hook methods, configuration options, memory-advisor ordering interactions, user-controlled execution patterns, and the custom-subclass extension pattern, see [`ToolCallingAdvisor`](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html).

For the conceptual overview of how the tool loop fits into the broader tool calling architecture, see [Tool Calling: The Tool Calling Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop).

For a concrete subclass that uses \`ToolCallingAdvisor’s extension hooks to implement progressive tool disclosure, see [Tool Search Tool](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html).

### StructuredOutputValidationAdvisor

`StructuredOutputValidationAdvisor` validates the structured JSON output against a JSON schema and retries the call if validation fails, up to a configurable number of attempts.

Key features:

- Derives a JSON schema from the expected output type, or accepts a pre-supplied schema string.
- Validates the LLM response against the schema.
- Retries the call when validation fails (default: up to 3 attempts).
- Augments the prompt with the validation error message on retry attempts to help the model self-correct.
- Uses `callAdvisorChain.copy(this)` to create a sub-chain for recursive calls.
- Accumulates token usage across every validation attempt, so the returned `ChatResponse` reports the cumulative usage of all retries rather than only the final attempt (see [Cumulative Usage Across Multi-Step Flows](https://docs.spring.io/spring-ai/reference/api/usage-handling.html#_cumulative_usage_across_multi_step_flows)).
- Optionally supports a custom `JsonMapper`.

The advisor can be configured via `outputType` (schema derived automatically) or `outputJsonSchema` (pre-supplied schema string); the two options are mutually exclusive.

Example with `outputType`:

```java
var validationAdvisor = StructuredOutputValidationAdvisor.builder()
    .outputType(MyResponseType.class)
    .maxRepeatAttempts(3)
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(validationAdvisor)
    .build();
```

Example with a pre-supplied JSON schema:

```java
var validationAdvisor = StructuredOutputValidationAdvisor.builder()
    .outputJsonSchema(myConverter.getJsonSchema())
    .build();
```

Alternatively, enable schema validation directly on an `entity()` call without configuring the advisor manually, via the `EntityParamSpec` consumer:

```java
ActorFilms actorFilms = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorFilms.class, spec -> spec.validateSchema());
```

See [Schema Validation & Self-Correction](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html) for the high-level usage.

## Accumulating Token Usage in Custom Recursive Advisors

A recursive advisor performs more than one model call per invocation, so it must accumulate the token usage of every call to report a correct cumulative total; otherwise only the last call’s usage is visible to the caller. Spring AI provides `org.springframework.ai.chat.client.advisor.UsageAccumulator` to make this straightforward. Create one instance per `adviseCall` invocation (or per stream subscription, inside a `Flux.defer`, to keep it subscription-local), fold each round’s response in with `addRoundResponse(…​)`, and stamp the cumulative total onto the final response with `applyAccumulatedUsage(…​)`:

```java
UsageAccumulator usage = new UsageAccumulator();
ChatClientResponse response;
do {
    response = callAdvisorChain.copy(this).nextCall(request);
    usage.addRoundResponse(response.chatResponse());
    // ... decide whether to loop again ...
}
while (loopAgain);
return usage.applyAccumulatedUsage(response);
```

The underlying token math lives in `org.springframework.ai.support.UsageCalculator` (`accumulateResponseUsage` and `withUsage`), which `UsageAccumulator` wraps.