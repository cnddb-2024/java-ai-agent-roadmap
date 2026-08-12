# Spring AI Tool Calling 实战

## 作业信息

- **日期**: 2026-08-12
- **Phase**: Phase 1（第 15/168 天）
- **对应飞书任务**: Spring AI Tool Calling 实战：@Tool注解/FunctionCallback/工具注册与调用demo
- **代码仓库**: [cnddb-2024/spring-ai-quickstart](https://github.com/cnddb-2024/spring-ai-quickstart)
- **提交**: `ec615ee` - tool再回顾

## 作业内容

### 1. 两种工具定义方式对比

| 方式 | 类 | 适用场景 | 示例 |
|------|-----|----------|------|
| `@Tool` 注解 | `WeatherTools`, `DateTimeTools` | 业务方法直接暴露，简单直观 | `@Tool(description="查询天气")` + `@ToolParam` |
| `Function<I,O>` + `FunctionToolCallback` | `MockWeatherService` | 需要强类型输入输出 record，兼容传统函数式 | `FunctionToolCallback.builder().inputType(Request.class)` |

### 2. 三种工具注册层级

- **全局注册**：`ChatClient.Builder.defaultTools(weatherTools, dateTimeTools)` — 所有请求可用
- **Provider 注册**：`MethodToolCallbackProvider.builder().toolObjects(...)` — 批量扫描 `@Tool` 方法
- **请求级注册**：`chatClient.prompt().tools(new WeatherTools(), new DateTimeTools())` — 单次请求临时挂载，支持并行调用

### 3. 工具实现细节

**WeatherTools**：
- `@Tool(name="getCurrentWeather", description="根据城市名称查询实时天气")`
- `@ToolParam(required=false)` 标注可选参数 unit
- `returnDirect=true` 的使用场景注释说明（结构化数据直接返回，跳过模型二次润色）

**DateTimeTools**：
- `getCurrentDateTime()` 无参数工具，通过 `LocaleContextHolder` 获取时区
- `plusMinutes(long minutes)` 带参工具

**MockWeatherService**（Function 模式）：
- `record Request(String location, Unit unit)` / `record Response(double temp, Unit unit, String condition)`
- Spring AI 自动将 record schema 转换为 JSON Schema 供模型理解

### 4. 覆盖知识点

- `@Tool` / `@ToolParam` 注解驱动
- `FunctionToolCallback` 编程式注册
- `MethodToolCallbackProvider` 批量扫描
- `defaultTools` vs 请求级 `tools()` 三层注册
- 工具描述（description）对模型决策的关键作用
- JSON Schema 自动生成（record → tool schema）

## 面试题关联

- Spring AI 的 @Tool 注解与 FunctionCallback 两种方式有何区别？如何选择？（第一梯队）
- Function Calling 的底层原理：模型如何决定调用哪个工具？JSON Schema 如何生成？（第一梯队）
- 工具注册的三个层级（全局/Provider/请求级）各自的适用场景？（第二梯队）
- `returnDirect=true` 的作用是什么？什么场景下使用？（第二梯队）
