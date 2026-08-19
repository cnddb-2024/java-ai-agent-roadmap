# roadmap-daily-maintainer

`Java AI Agent 转型学习计划` 的每日无人值守维护 **Skill**。

把原来一大段提示词提炼成一个标准 CodeBuddy Skill（`SKILL.md`），这样定时任务的描述只需一句话：**「从仓库获取该 skill，然后执行」**，无需在任务里重复整段指令。

## 这个 Skill 做什么
1. 拉取路线图仓库 `roadmap-repo`
2. 初始化时间与阶段（只算一次，全程复用）
3. 飞书鉴权（硬前置，不可用即终止）
4. 更新反馈层（`java-ai-agent-roadmap.html` + `charts.js` 雷达图）
5. 采集飞书任务状态 + 扫描作业
6. 滑动窗口任务规划（始终保持 9 个活跃任务：今天3/明天3/后天3，每天锚定滚动；窗口外任务冻结不删）
7. 融合教程生成（幂等：文件或飞书评论已存在则跳过）
8. 写回与兜底（日志 + git push）

> 完整指令见 `SKILL.md`，由 Skill 正文承载，本 README 不重复。

## 安装（放入 CodeBuddy skills 目录）
```bash
# 方式 A：直接拷贝到本地 skills 目录
cp -r roadmap-daily-maintainer ~/.codebuddy/skills/

# 方式 B：运行时从本仓库克隆后读取 SKILL.md（推荐用于自动化，见下）
git clone https://github.com/<your-github-username>/roadmap-daily-maintainer.git
cat roadmap-daily-maintainer/SKILL.md   # 让 agent 严格按其指令执行
```

## 注册为每日自动化任务（精简版描述）
创建定时任务时，`--prompt` 只需写：

> 从仓库 `https://github.com/<your-github-username>/roadmap-daily-maintainer` 克隆最新版，读取其中的 `SKILL.md`，严格按其指令执行「Java AI Agent 转型学习计划」的每日无人值守维护流程（先 `git clone roadmap-repo`，再按 SKILL.md 的 1–9 步执行；运行时需具备 `lark-cli`、git、python3 与飞书凭证）。

对应调度命令（在已启用 cron 的环境中执行）：
```bash
./scripts/scheduler-api.sh create \
  --name "Java AI Agent 学习计划·每日维护" \
  --cron "0 0 8 * * *" \
  --frequency-type "daily" \
  --prompt "从仓库 https://github.com/<your-github-username>/roadmap-daily-maintainer 克隆最新版，读取其中的 SKILL.md，严格按其指令执行「Java AI Agent 转型学习计划」的每日无人值守维护流程（先 git clone roadmap-repo，再按 SKILL.md 的 1–9 步执行；运行时需具备 lark-cli、git、python3 与飞书凭证）。" \
  --timeout 1800 \
  --retry-count 3
```

## 前置依赖（运行环境需具备）
- `git`、`python3`
- `lark-cli` 及已登录的飞书用户凭证（trae-remote-official:lark::feishu）
- 可访问的 `roadmap-repo`（含 `skills/task-generation.md`、`skills/tutorial-fusion.md`）
- GitHub 只读权限（自动化任务克隆本 skill 仓库用）
