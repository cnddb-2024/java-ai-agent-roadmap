# AGENTS.md — 仓库开发规则

对本仓库工作的所有 AI Agent 会话与人生效。2026-11-03 由用户确定。

## Git 工作流

1. **直接在 main 分支开发**
   - 不创建 feature/agent 分支，不提 PR，不搞合并流程。
   - 会话若被工具（如 Trae）自动切到 `trae/agent-*` 临时分支：先 `git checkout main && git pull --ff-only` 对齐后再动工。
2. **提交与推送**
   - 完成后直接提交到 main 并 `git push origin main`（快进推送）；远程不可访问时保留本地 commit 并记日志（既有惯例）。
   - 暂存必须显式 `git add <具体路径>`，**禁止 `git add .` / `git add -A`**，防止 `.uploads/`、`.trae/documents/` 计划草稿、会话临时文件误入提交。
3. **分支清理**
   - 仓库长期只保留 main 一个分支。若仍产生了 `trae/agent-*` 临时分支，工作收尾时删除：本地 `git branch -d <分支>`、远程 `git push origin --delete <分支>`，并 `git branch -dr` 清理残留跟踪引用。
   - 删除前用 `git diff main <分支> --name-status` 确认无有价值内容遗漏（`.trae*` 会话产物可忽略）。

## 提交信息

- 沿用仓库既有风格：`feat(tutorial):` / `chore(daily):` / `chore(weekly):` / `refactor(phase):` 等前缀 + 中文描述。
