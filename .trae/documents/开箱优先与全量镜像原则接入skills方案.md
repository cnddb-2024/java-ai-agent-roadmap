# 方案：开箱优先 + 全量镜像原则接入 roadmap skills

## 一、总结

依据用户上传的《SpringAI教程产出原则-开箱优先与全量镜像.md》（2026-10-17 强制约束），精准修订 `/workspace/skills` 下相关 skill，使今后的每日定时任务（任务拆解 + 融合教程生成）强制执行：

- **原则一 开箱优先**：自研前必须先证明官方无开箱实现（当前版本镜像+jar 双证 → 更高 GA 版本；M 里程碑不算）；有开箱必用开箱，无开箱才许自研且标注"自研范围+对标对象+待官方实现后替换"；每个框架能力类任务/教程必写**立项三问**。
- **原则二 全量镜像**：Spring AI 官方文档全量镜像到仓库 `docs/springai-official/`（每页一 .md + `_manifest.txt`）；断言走三级验证链（本地镜像 → 官网抓取 → jar 实证，冲突以 jar 为准）。
- **禁止**：从未审查代码路径推断全局行为 / 凭训练记忆断言版本行为 / 把"文档没写"当"功能不存在"。
- **教程版本时效**（用户补充）：教程主线必须基于当前所用/最新 GA 版本的开箱用法，不得以过时方案为主线（其他框架同理）。
- **只对今后生效**：assignments/ 已有教程、飞书已有任务描述、term-whitelist 等历史内容一律不动。

## 二、现状分析（探索结论）

1. `/workspace` 即 roadmap 仓库工作副本（浅克隆），当前分支 `trae/agent-5QAGid`，与 `main`、`origin/main` 同指向 `fd34e01`（2026-10-14），工作树干净（仅 `.uploads/` 未跟踪）。
2. 定时任务每次 `git clone` 仓库并读取 `skills/roadmap-daily-maintainer/SKILL.md` 执行 1–9 步 → **改仓库内 skill + push 即可生效，定时任务描述本身无需修改**。
3. 现有规则差距：
   - `task-generation.md` 原则3（2026-09-03"框架开箱优先"）依据是"搜索互联网确认最新稳定版本"，无镜像/jar 实证、无 GA 与 M 里程碑区分、无立项三问、无自研标注要求。
   - `tutorial-fusion.md` 第13节（2026-09-03）同样基于互联网搜索，无全量镜像、无三级验证链、无产出前自检清单。
   - 两文件均有"手写需企业普遍手写"旧前提，与新版原则（无开箱即允许自研但须标注）不一致，需以新原则为准重写。
4. 仓库根目录无 `docs/`，`.gitignore` 不忽略 docs/ → 镜像目录无冲突。
5. 可行性已验证：代理出口访问 docs.spring.io 正常（200，0.7s/页）；node v24.1.0 + npx 可用（defuddle CLI 未装，执行时经 defuddle skill 指引用 npx 安装）；附件 `_manifest.txt` 含 112 个 reference 页面 URL（对齐 2.0.1，2026-10-17）。

## 三、修改方案（4 个 skill 文件 + 2 类新增）

### 3.1 `skills/task-generation.md`（任务拆解规则）

**改动 A：整体替换"### 3. 框架开箱优先（任务形态控制，2026-09-03 用户要求）"一节**，新文本：

```markdown
### 3. 框架开箱优先 + 全量镜像（2026-10-17 用户强制约束，替代 2026-09-03 规则）

适用范围：Spring AI / LangChain4j / Python 库 / 微服务中间件等一切框架能力。

**立项三问（框架能力类任务必写进 description，缺一不可）**：
1. 当前所用版本有什么？（证据：本地官方文档镜像 + jar 实证）
2. 更高已发布 GA 版本有什么？（M 里程碑不算，仅作路线参考）
3. 为什么不用更高版本？

**开箱判定（顺序强制）**：
1. 查当前所用版本：本地官方文档镜像 + jar 实证（javap 反编译；META-INF/spring-configuration-metadata.json 查配置键；实证须覆盖全部相关模块 jar，反例：TokenCountEstimator 在 spring-ai-commons 而非 spring-ai-model，漏扫即误判）
2. 查更高已发布 GA 版本（M 里程碑不算）
3. 有开箱 → 任务形态必须是"框架组件接入 + 参数调优"，summary/description 标注框架与版本；禁止生成手写实现任务
4. 无开箱 → 才允许自研任务，且 description 必须标注：自研范围 + 对标对象 + 待官方实现后替换

**三级验证链（所有版本/能力断言，效力递增）**：本地镜像 → 官网抓取 → jar 实证；文档与 jar 冲突以 jar 为准。

**镜像规则**：官方文档镜像位于仓库 docs/springai-official/（每页一 .md，URL 路径即文件路径；_manifest.txt 为来源清单）。拆解任务前先在镜像定位相关章节，缺页先补抓再下断言（抓取与命名规则见 tutorial-fusion.md 第 13 节）。其他框架同规则使用 docs/<framework>-official/ 目录。

**禁止**：从未审查到的代码路径推断全局行为 / 凭训练记忆断言版本特定行为 / 把"文档没写"当"功能不存在"。

自研任务仍只需"讲清原理 + 最小可运行示例"，禁止逐行底层实现（原理深度留给面试口述）。
```

**改动 B：拆解流程第 6 步**，由"先确认 Spring AI / LangChain4j 最新稳定版本的开箱实现情况（见原则3）"改为"先按原则3 完成开箱判定（镜像 + jar 实证 + 更高 GA 查证）并写好立项三问，再拆解为 G 个合适粒度的任务（≤1h/个）"。

**改动 C：任务 Description 格式**，在【相关面试题】之后追加一行：

```markdown
【立项三问】当前版本有什么: … / 更高 GA 版本有什么: … / 为什么不用更高版本: …（框架能力类任务必填；纯面试/决策日志/Python 语法类可省略）
```

### 3.2 `skills/tutorial-fusion.md`（教程生成规则）

**改动 A：整体替换"### 13. 框架开箱实现优先与版本标注（2026-09-03 用户要求，硬性规则）"一节**，新文本：

```markdown
### 13. 开箱优先与全量镜像（2026-10-17 升级为强制约束，适用一切框架）

**范围**：Spring AI / LangChain4j / Python 库 / 微服务中间件等所有教程、迁移文档、示例代码。

**原则一 开箱优先**：任何能力动手自研前，必须先证明官方没有开箱实现——
1. 查当前所用版本：本地官方文档镜像 + jar 实证（javap；META-INF/spring-configuration-metadata.json 查配置键；实证须覆盖全部相关模块 jar）
2. 查更高已发布 GA 版本（M 里程碑不算，仅作路线参考）
3. 有开箱 → 教程代码主线必须采用开箱实现，显著标注框架与版本
4. 无开箱 → 才允许自研，必须标注："⚠️ 自研范围 + 对标对象 + 待官方实现后替换"

**立项三问（框架能力类教程，写入正文开头，缺一不可）**：
当前版本有什么？/ 更高已发布 GA 版本有什么？/ 为什么不用更高版本？

**原则二 全量镜像**：
- Spring AI 官方文档（docs.spring.io/spring-ai/reference）全量镜像于仓库 docs/springai-official/：每页一个 .md，URL 路径即文件路径（.html→.md，如 api/chat/openai-chat.html → api/chat/openai-chat.md，index.html→index.md）；_manifest.txt 为来源清单，首行 # 注释记录对齐版本与抓取日期，抓取失败页以 # failed 注释追加在文件尾部
- 动手前先在镜像定位相关章节；镜像缺页 → 先补抓该页入镜像 + 更新 _manifest.txt，再下断言
- 框架版本升级后重抓全套镜像（_manifest.txt 即版本对齐凭证）
- 其他框架（LangChain4j / Python 库 / 中间件）同规则使用 docs/<framework>-official/，任务涉及章节必须先入镜像再下断言

**三级验证链（所有框架行为断言，效力递增）**：本地镜像 → 官网抓取 → jar 实证（javap + META-INF/spring-configuration-metadata.json）；文档与 jar 冲突以 jar 为准。

**版本时效（2026-10-17 用户补充）**：教程主线必须基于当前所用版本（以镜像 _manifest.txt 对齐的 GA 版本为准）的开箱用法，不得以过时方案为主线；旧版本做法仅作"了解即可"对照，其他框架同理。

**禁止**：从未审查到的代码路径推断全局行为 / 凭训练记忆断言版本特定行为 / 把"文档没写"当"功能不存在"。

**产出前自检清单（教程写入文件前逐项过，任一不过先补证再写）**：
- [ ] 涉及能力查过官方开箱实现？（当前版本：镜像 + jar 双证）
- [ ] 更高 GA 版本有对应能力吗？立项三问写了吗？
- [ ] 所有框架行为断言都过了三级验证链？
- [ ] 引用的配置键在 spring-configuration-metadata.json 实证过？
- [ ] 自研实现标注了自研范围 + 对标对象 + 替换计划？

继续有效（承接 2026-09-03 规则）：新旧做法对照（"✅ 新做法（推荐，开箱）"与"旧做法（了解即可，已被替代）"）；引用旧版本教程须在来源条目标注版本时效；手写环节只讲原理 + 最小可运行示例，禁止逐行展开底层实现。
```

**改动 B：执行步骤第 5 步**改为：

```markdown
5. 【镜像先行】先在 docs/springai-official/（或对应框架镜像目录）定位相关章节，缺页先补抓并更新 _manifest.txt（第 13 节）；再搜索互联网教程（至少 5 个来源，官方镜像对应页面须列入来源并标注对齐版本），同步确认最新 GA 版本及该主题的开箱实现情况（第 13 节）
```

**改动 C：执行步骤第 6 步**的代码主线 bullet 追加："框架能力类教程正文开头写立项三问；主线基于当前 GA 版本开箱用法，自研环节标注自研范围/对标对象/替换计划（第 13 节）"。

**改动 D：11.4 内容完整性校验**追加一条：

```markdown
- 框架能力类教程：正文开头含「立项三问」（当前版本有什么 / 更高 GA 版本有什么 / 为什么不用更高版本，三要素齐全），缺失则不通过
```

### 3.3 `skills/roadmap-daily-maintainer/SKILL.md`（主流程，最小改动）

1. frontmatter：`version: "1.1.0"` → `"1.2.0"`；`updated: "2026-09-16"` → `"2026-10-17"`。
2. 【描述规范】（步骤 6 内，全文唯一定义处）追加一句：
   "；框架能力类任务另须含【立项三问】：当前版本有什么 / 更高 GA 版本有什么（M 里程碑不算）/ 为什么不用更高版本（规则见 task-generation.md 原则3）"
3. 步骤 8.3 的来源 bullet 由"搜索互联网教程（至少5个来源），同时提取路线图中推荐的参考项目链接"改为：
   "先在本地官方文档镜像（docs/springai-official/ 等，规则见 tutorial-fusion.md 第13节）定位相关章节，缺页先补抓再下断言；再搜索互联网教程（至少5个来源，官方文档页须列入来源），同时提取路线图中推荐的参考项目链接"

### 3.4 `skills/roadmap-daily-maintainer/README.md`（一行同步）

第 7 条功能描述追加："；开箱优先 + 官方文档全量镜像三级验证（2026-10-17）"。

### 3.5 不修改

- `skills/term-whitelist.md`：术语解释控制，与实现原则无关。
- 定时任务描述：任务克隆仓库读取 SKILL.md，自动获得新规则。
- assignments/ 全部历史教程、`.trae/` 快照与注册表、飞书存量任务：过去内容不调整。

### 3.6 新增：Spring AI 官方文档全量镜像（112 页）

1. **种子清单**：将附件 `_manifest.txt`（112 个 URL）写入 `docs/springai-official/_manifest.txt`，首行加头注释：`# aligned: <实测版本，预期 2.0.1> · fetched: 2026-10-17 · pages: 112`（去除原文件 BOM）。
2. **抓取**：先加载 defuddle skill 获取 CLI 用法（`npx defuddle` / `npm i -g defuddle`）；逐页 `curl`（走代理）下载 HTML → defuddle 转为干净 markdown → 按命名规则存为 `docs/springai-official/<URL路径>.md`（如 `api/advisors.html` → `api/advisors.md`）。
3. **失败处理**：单页失败重试 1 次，仍失败则以 `# failed <url> <原因>` 追加到 `_manifest.txt` 尾部并记录日志，不中断（后续每日运行按"缺页先补抓"收敛）。
4. **版本核实**：从 getting-started/index 页核实当前 reference 对应版本号（预期 2.0.x GA），写入 manifest 头注释。

## 四、提交与推送

1. 执行前 `git ls-remote origin main` 复核远程仍为 `fd34e01`；若有推进则先 `git fetch && git rebase`。
2. `git checkout main`（三分支同点，切换无损；.uploads/ 未跟踪不受影响）。
3. 两个提交（**显式 add 指定路径，禁止 `git add .`/`-A`**，防止把 `.uploads/`、`.trae/documents/` 计划文件卷入）：
   - `git add skills/` → `feat(skills): 立项三问+开箱优先+全量镜像强制约束接入任务拆解与教程生成规则`
   - `git add docs/springai-official/` → `docs(mirror): Spring AI 官方文档全量镜像 112 页（对齐 2.0.1）+ _manifest.txt`
4. 推送：`git push https://x-access-token:<用户消息中的token>@github.com/cnddb-2024/java-ai-agent-roadmap.git main`（token 仅用于命令行，不写入任何提交文件）。

## 五、假设与决策

| 决策点 | 结论 | 依据 |
|---|---|---|
| 镜像位置 | 仓库内 `docs/springai-official/` | 定时任务每次克隆仓库，仓库是唯一持久载体；附件示例即此路径 |
| 镜像建设 | 本会话全量抓取 112 页 | 用户确认（推荐项） |
| 交付方式 | commit 到 main 并立即 push | 用户确认（推荐项） |
| 其他框架 | 章节级镜像（任务涉及章节先入镜像），不强制全量 | 用户确认 + 附件"以springai为例" |
| 教程版本 | 主线基于当前 GA 开箱用法，禁止过时方案主线 | 用户补充要求 |
| 手写前提 | 取消"企业普遍手写"旧前提，改为"无开箱即允许自研 + 强制标注" | 附件原则一第 4 条 |
| 历史内容 | 一律不动（含附件注入提示词中的"对最近教程自查"第①条亦不执行） | 用户执行要求"过去已实现的内容不做调整" |
| 立项三问豁免 | 纯面试/决策日志/Python 语法类非框架任务可省略 | 避免无意义膨胀，原则针对框架能力 |

## 六、验证步骤

1. **镜像完整性**：`find docs/springai-official -name '*.md' | wc -l` 与 manifest URL 数一致（112 − 失败数）；脚本核对每个 manifest URL 按命名规则映射的文件存在且非空；抽查 3–5 页（如 `api/advisors.md`、`api/chatclient.md`）含预期关键词。
2. **skill 修订到位**：Grep 确认 `立项三问`、`全量镜像`、`docs/springai-official`、`三级验证链` 在 task-generation.md / tutorial-fusion.md / SKILL.md 中出现；旧原则3 文本（"企业普遍手写"、"2026-09-03 用户要求"标题）已无残留冲突。
3. **一致性**：SKILL.md【描述规范】与 task-generation.md Description 格式均含立项三问且表述一致；tutorial-fusion.md 13 节与执行步骤 5/6、11.4 相互呼应。
4. **git 卫生**：`git show --stat` 两个提交仅含预期路径（skills/ 4 文件、docs/springai-official/）；`git ls-remote` 确认远程 main 已推进到新提交；`grep -r "ghp_"` 确认提交内容无 token；工作树干净（除 .uploads/ 与 .trae/documents/ 计划文件）。

## 七、明确不做的事

- 不修改 assignments/ 历史教程、不重新生成已有教程、不改飞书存量任务（幂等规则继续生效）。
- 不修改 term-whitelist.md。
- 不修改定时任务描述（克隆即得新 skill）。
- 不对过去已产出教程做两原则自查回溯（用户执行要求优先于附件注入提示词第①条）。
