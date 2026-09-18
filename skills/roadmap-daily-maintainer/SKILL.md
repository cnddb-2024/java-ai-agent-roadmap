---
name: roadmap-daily-maintainer
description: "Java AI Agent 转型学习计划的每日无人值守维护：拉取路线图仓库、飞书鉴权、更新反馈层(HTML/雷达图)、滑动窗口任务规划与拆解、融合教程生成、写回与兜底。当用户要求执行该学习计划每日维护或为其设置定时任务时使用。"
version: "1.1.0"
author: "user"
created: "2026-08-17"
updated: "2026-09-16"
---

# Java AI Agent 转型学习计划 · 每日无人值守维护提示词

你是一个无人值守的定时任务执行体。每次运行需独立完成以下流程。各步骤独立降级（某步非致命失败时写日志后继续下一步）；但飞书鉴权为硬性前置——若飞书不可用，本次运行直接终止并报警（飞书必须可用，由本人监督），不进入后续步骤。全部中文输出。沙箱时间为UTC，用北京时间：TZ=Asia/Shanghai date +%Y-%m-%d。

1. 拉取仓库
   git clone roadmap-repo && cd roadmap-repo

2. 创建日志目录
   mkdir -p .trae/logs

3. 初始化时间与阶段（仅计算一次，全程复用）
   TODAY=$(TZ=Asia/Shanghai date +%Y-%m-%d)
   DAY_NUM=$(python3 -c "from datetime import datetime; print((datetime.strptime('$TODAY','%Y-%m-%d')-datetime(2026,7,29)).days+1)")
   PHASE=$(python3 -c "d=$DAY_NUM; print(0 if d<=14 else 1+(d-15)//42)")
   TODAY_TS=$(python3 -c "from datetime import datetime,timezone; print(int(datetime.strptime('$TODAY','%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())*1000)")
   TOMORROW_TS=$((TODAY_TS + 86400000))
   DAY_AFTER_TS=$((TODAY_TS + 172800000))
   # 后续步骤一律直接引用上述 TODAY / DAY_NUM / PHASE / TODAY_TS / TOMORROW_TS / DAY_AFTER_TS，禁止重复计算或复用历史值。

4. 飞书鉴权
   lark-cli auth status --as user 检查飞书token状态。若失败，用 RequestAuthorization 请求 trae-remote-official:lark::feishu 授权后重试。若仍失败，则本次运行直接终止并报警（飞书必须可用，由本人监督），不再继续执行后续步骤。

5. 更新反馈层（改 HTML + charts.js）
   5.1 使用【初始化】已算出的 TODAY / DAY_NUM / PHASE（Phase0:第1-14天, Phase1:第15-56天, Phase2:第57-98天...）更新 java-ai-agent-roadmap.html 中 id="today-marker" 的div，用sed正则替换天数。格式：当前：Phase X · 第 N/168 天
   5.2 更新 assets/charts.js 中 window.__RADAR_GAP__.me 数组（7维）。me值只有在飞书任务completed=true时才推进，根据已完成任务对应的知识维度递增。
   5.3 更新 assets/charts.js 中 window.__RADAR_DAILY__ 数组（6维），基于assignments/目录中最近7天作业完成情况。

6. 采集飞书任务状态 + 扫描作业（飞书为硬依赖，此步骤不保存 snapshot）
   6.1 lark-cli task tasklists list --as user 查找清单"Java AI Agent 转型学习计划"，获取其 tasklist_guid。（可将上次成功的 guid 缓存于 .trae/feishu_cache.json 复用，但以本次名称查找结果为准；仅当名称查找失败且无缓存时才报错终止。）
   6.2 lark-cli task tasklists tasks --as user --tasklist-guid <guid> --page-size 100 --page-all --format json 列出所有任务。记录每个任务的guid/summary/due.timestamp/completed_at。
   6.3 扫描 assignments/ 目录，记录作业完成情况。
   6.4 读取 .trae/snapshot.json（旧快照），与飞书当前状态对比，记录以下diff结果（不修改snapshot.json）：
        - 新完成任务NEW_DONE：旧快照中completed=false但飞书completed_at≠"0"的任务。记录guid和summary。
        - 消失任务VANISHED：旧快照中存在但飞书中不存在的任务。将summary加入excluded.json的excluded_titles。
        - 新出现任务NEW_APPEARED：飞书中存在但旧快照中没有的任务。记录guid、summary、飞书created_at。
        - 若snapshot.json不存在或为空，NEW_DONE为空列表。
   6.5 补写学习指引：飞书中 description 为空的任务，按【描述规范】补写后用 lark-cli task tasks patch --as user --task-guid <guid> --data '{"task":{"description":"<内容>"},"update_fields":["description"]}' 更新。

   【描述规范】（6.5 与 7.3.7 共用，全文只此一处定义）
   description 内容格式为：学习目标 / 知识点 / 学习资源 / 验收标准 / 相关面试题；其中"相关面试题"从路线图面试体系中匹配。

   重要：步骤6不保存snapshot.json，snapshot将在步骤7结束后统一保存。

7. 滑动窗口任务规划 + 路线图自动拆解（依赖飞书，飞书为硬依赖）
   核心原则：飞书清单中始终保持恰好9个活跃未完成任务（今天3个、明天3个、后天3个）处于窗口内，按created_at从旧到新排序分配。已完成的任务保留在飞书中（用于雷达图统计），但不参与窗口。窗口外多余的活跃任务一律【冻结不删】，保留在飞书中存档。
   每日窗口锚定原则（极重要，防止窗口不滚动）：无论任务是否完成、是否新增，每次运行都必须用【初始化】已算出的 TODAY_TS / TOMORROW_TS / DAY_AFTER_TS 把窗口内前9个活跃未完成任务（冻结任务不参与）的 due 无条件重写（patch）为 今天/明天/后天。绝不允许沿用历史 due 日期。
   重要：任务补充直接从路线图 HTML 拆解。读取 skills/task-generation.md 中的 Skill 规范执行任务拆解。
   时间戳（已在【初始化】阶段计算，全程复用，禁止此处重复计算）：TODAY_TS / TOMORROW_TS / DAY_AFTER_TS 直接使用【初始化】的值。due格式：{"timestamp":"<ts>","is_all_day":true}
   created_at排序规则（统一，极重要，全文只此一条）：
        - 窗口排序一律以 .trae/snapshot.json 中的 created_at 为准，不使用飞书API返回的created_at作为排序依据。
        - 若某任务在 snapshot 中缺 created_at：用 lark-cli task tasks get --as user --task-guid <guid> 获取一次，并写回 snapshot（同时作为 7.7 的 created_at 来源）。
        - 仅 NEW_APPEARED（飞书有、旧快照无）的 created_at 以飞书API值为兜底，且同样写回 snapshot。
        - 排序规则全程只此一条，其余步骤不再另述。

   7.1 统计飞书中所有未完成（completed_at="0"）且未冻结（frozen=false）的任务数量 N。计算需要补充的任务数 G = max(0, 9 - N)。说明：冻结任务不计入 N、不参与窗口，仅作存档保留（见7.2/7.5）。
   7.2 若 G=0（当前已有≥9个活跃未完成任务，无需补充新任务）：不拆解新任务。将飞书中所有活跃未完成任务（completed_at="0" 且 frozen=false）按 snapshot 中 created_at 排序：
        - 取前9个作为窗口；第10个及以后：标记为冻结（snapshot 中 frozen=true 并清除其 due），保留在飞书中不删除。
        - 对这9个窗口任务执行【窗口锚定】：前3个due=【初始化】的 TODAY_TS、中3个=TOMORROW_TS、后3个=DAY_AFTER_TS，用 patch 无条件重写 due。
        执行窗口锚定后，继续 7.6 → 7.7。
   7.3 若 G>0（当前活跃未完成任务不足9个，需要补充 G 个）：先解冻：若存在冻结任务，将最旧的 min(G, 冻结数) 个解冻（snapshot 中 frozen=false），计入可复用任务；剩余 G' = G - 解冻数。读取 skills/task-generation.md 中的 Skill 规范，执行以下拆解流程（仅拆解剩余的 G' 个新任务）：
        7.3.1 确定当前 Phase：直接使用【初始化】已算出的 PHASE，勿重复计算。
        7.3.2 解析 java-ai-agent-roadmap.html 中该 Phase 的"核心内容"列表和"验收标准"。
        7.3.3 读取 snapshot.json，收集所有已存在任务的 summary（已完成 + 未完成 + 冻结）。
        7.3.4 对比 Phase 核心内容与已存在任务，找出尚未覆盖的知识点。
        7.3.5 将未覆盖知识点按 task-generation.md 规范拆解为 G' 个新任务（粒度控制：≤1h/个，禁止内容爆满）。
        7.3.6 如果当前 Phase 核心内容已全部拆解完毕但仍不足 G' 个：检查该 Phase 验收标准是否已全部满足，若已满足则进入下一 Phase；从下一 Phase 核心内容中拆解剩余任务；如果下一 Phase 也不存在或路线图已到末尾，创建多少算多少，不凑数。
        7.3.7 每个新任务编写 description：严格按【描述规范】（见步骤6【描述规范】）编写，从路线图面试体系匹配相关面试题。
        7.3.8 贯穿线任务穿插：每 3-4 个 Phase 核心任务后，穿插一个 Python 补齐或技术决策日志任务（见 task-generation.md 贯穿线规则）。
   7.4 汇总所有活跃未完成任务 = 飞书 completed_at="0" 且 frozen=false 的任务（含本次解冻的） + 新拆解的任务。按 created_at 从旧到新排序（新拆解任务的 created_at 设为当前时间戳，排在已有任务之后）。
   7.5 取前9个活跃未完成任务（按 created_at 排序）执行【窗口锚定】：前3个due=【初始化】的 TODAY_TS、中3个=TOMORROW_TS、后3个=DAY_AFTER_TS。
        - 窗口任务中已在飞书的：用 lark-cli task tasks patch --as user --task-guid <guid> --data '{"task":{"due":{"timestamp":"<ts>","is_all_day":true}},"update_fields":["due"]}' 用【初始化】的日期重写 due。
        - 窗口任务中新拆解的：用 lark-cli task tasks create --as user 创建到飞书（description有特殊字符时用 cat file.json | lark-cli task tasks create --as user --data - 传入），创建后用 lark-cli task tasklists task-add 加入清单。
        - 活跃未完成任务中排在第10个及以后的：标记为冻结（snapshot 中 frozen=true 并清除 due），保留在飞书中不删除。
        - 若活跃未完成任务不足9个：全部放入飞书，按顺序分配due（前3今天/中3明天/后3后天），不足部分不补充。
        重要：窗口锚定使用的 TODAY_TS/TOMORROW_TS/DAY_AFTER_TS 已在【初始化】计算，禁止重复计算或复用历史日期。
   7.6 excluded.json中的标题不得复活。
   7.7 保存 snapshot.json（在所有飞书操作完成后统一保存）：
        - 包含当前飞书清单中的所有任务（含已完成、未完成、冻结）。
        - 每个任务：guid/summary/due(YYYY-MM-DD)/created_at/completed(bool)/frozen(bool)。
        - completed：飞书 completed_at≠"0" 则为 true。
        - created_at：已在旧 snapshot 中的用旧值；NEW_APPEARED 用飞书API值；新拆解用步骤7.3设定的时间戳；快照缺失则按需 lark-cli task tasks get 获取（见 created_at 统一规则）。
        - due：用飞书返回的 due.timestamp 转换为 YYYY-MM-DD（冻结任务可为空）。
        - frozen：冻结任务为 true，其余 false。

8. 融合教程生成（依赖飞书+路线图）
   读取 roadmap-repo/skills/tutorial-fusion.md 中的 Skill 规范，为需要处理的任务生成专属融合教程。（详细融合规则见该 Skill 文件，主提示词不再复述）
   8.1 确定待处理任务列表（合并两类）：当天due任务：步骤7中due设为今天的3个任务（正常情况）；逾期未完成任务：飞书中 completed_at="0" 且 due 日期早于 TODAY 的任务。合并去重后得到待处理列表（通常3-6个）。
   8.2 对每个待处理任务执行全局幂等检查（极其重要：只要某任务已有融合教程，就不再生成，无论due是否顺延）：
        前置（必做）：git pull --rebase origin main 同步远程（如远程不可访问则跳过，仅本地比对，不阻塞后续流程）。
        三信号检查，任一命中即跳过：
        - 信号①注册表（权威）：读 .trae/tutorial_registry.json，按任务 guid 精确匹配（guid 全局唯一且稳定，优先于 slug 模糊匹配）。注册表记录每个已生成教程任务的 summary/slug/tutorial_path/raw_url(已废弃)/feishu_url/feishu_file_token/feishu_comment_id/generated_at。文件不存在视为空注册表（首次运行自动创建）。
        - 信号②文件：计算该任务的slug（先按summary关键词匹配assignments目录中已有的子目录名，若无匹配则用summary的kebab-case），全局扫描 assignments/ 下所有日期子目录，查找 <slug>/ 目录下是否存在任一 *.html（即 assignments/*/<slug>/*.html 任意一个存在，兼容历史 tutorial.html 与现行 <任务全称>.html 命名，文件名规则见 tutorial-fusion.md 第3节）。
        - 信号③评论状态：lark-cli task 当前仅有 +comment 写入、无评论读取命令（已实测确认，勿再猜测子命令）。"是否已评论"以注册表中的 feishu_comment_id 字段（飞书云盘 URL 评论）为等价记录；旧 comment_id 字段为废弃 raw URL 评论历史值，不再作为幂等依据。
        - 命中任一信号 -> 跳过，记录日志"任务<summary>已有教程（注册表/文件），跳过生成"，不重复生成、不覆盖、不追加评论。
        - 三信号皆未命中 -> 继续生成。
        - 新教程存入 assignments/<当前due日期>/<slug>/<任务全称>.html（文件名取HTML标题/任务全称，清洗规则见 tutorial-fusion.md 第3节；用任务当前的due日期，不是今天日期）。
        - 关键：due顺延不触发重新生成；注册表或 assignments 树中已有该任务记录/教程的，后续顺延/重新分配due时一律跳过。
   8.3 对需要生成教程的每个任务，按 tutorial-fusion.md 规范执行：
        - 获取飞书任务详情（summary + description）
        - 解析 java-ai-agent-roadmap.html 确定当前 Phase，提取相关推荐项目链接和面试题
        - 搜索互联网教程（至少5个来源），同时提取路线图中推荐的参考项目链接
        - 读取 skills/term-whitelist.md 区分"已掌握/待观察"术语，按 tutorial-fusion.md 第12节规范：白名单外专有名词首次出现必须桥接式解释（类比 Java/Spring/MySQL/Redis 已有知识），教程底部附术语表
        - 按 tutorial-fusion.md 规范融合生成 <任务全称>.html（标题即文件名，见该 skill 第3节）：主线语言 Java（LangChain4j + Spring AI），Python 仅辅助；顶部标注总预估时长（≤1小时，极限1.5小时）；顶部标注 Phase 和任务全称；底部"教程来源"列出所有来源链接（互联网+路线图推荐项目，地位平等）；自包含 HTML，使用 html-report skill 规范。
        - 存入 assignments/<当前due日期>/<slug>/<任务全称>.html
   8.4 教程生成完成后，本地提交一次（远程不可访问时跳过 push，仅本地 commit）：git add assignments/ && git commit -m "feat(tutorial): <TODAY> 生成<N>篇融合教程" && git push || 记录日志"远程 push 失败，本地已 commit"。
   8.5 【上传飞书云盘·与 GitHub 同构路径】对每个新生成教程的任务：
        - 用 lark-cli drive +create-folder 逐级创建 assignments → <当前due日期> → <slug> 三层目录（已存在则跳过，可读 .trae/feishu_drive_cache.json 缓存 folder_token 复用）。
        - 用 lark-cli drive +upload --file <本地 <任务全称>.html> --name "<任务全称>.html" --folder-token <slug 目录的 folder_token> 上传。
        - 拿到返回的 file_token 和 url（形如 https://my.feishu.cn/file/<file_token>），立即写入 .trae/tutorial_registry.json 该 guid 条目：
          feishu_url / feishu_file_token / feishu_folder_path / raw_url_status="unavailable_github_repo_404"。
        - 上传完成后立即提交注册表：git add .trae/tutorial_registry.json && git commit -m "chore(registry): <TODAY> 教程注册表更新" && git push || 记录日志。
   8.6 【评论·防重】对每个新生成教程的任务，单任务单命令执行 lark-cli task +comment --task-id <guid> --content：
        评论格式："📚 专属融合教程已生成（飞书云盘，可点击预览/下载）:
                   <feishu_url>
                   目录: assignments/<当前due日期>/<slug>/<任务全称>.html"
        幂等与防重（2026-08-22 重复评论事故修复，硬性规则）：
        - 发送前必查注册表：该任务 guid 已有 feishu_comment_id 记录 -> 禁止再次发送。
        - 单任务单命令：+comment 逐条执行，禁止 && 批量链；返回结果中取得 comment_id 才算成功。输出不完整/超时时，先用 --dry-run 核对参数并重查注册表，禁止盲目重发。
        - 评论成功后立即将 feishu_comment_id 写入 .trae/tutorial_registry.json 对应 guid 条目，单独 commit + push 注册表。
        - 已跳过（8.2 命中）的任务一律不评论。
        - 注意：旧的 raw URL 评论无法删除（lark-cli task 无评论删除命令），保留即可；用户看到新评论（含飞书云盘 URL）后优先使用新评论。
   8.7 【本地预览·可选，会话内可访问】全部教程生成并上传完成后，集中复制今日 N 篇 HTML 到 /workspace/今日作业教程_<TODAY>/<任务全称>.html，启动 nohup python3 -m http.server 8765 & 后用 OpenPreview 工具传 command_id 和 http://localhost:8765/ 给用户；将 URL 作为本次会话答案返回（Trae 自动化会话历史以启动时间命名，会话内 URL 可长期回看）。
   8.8 若某任务的教程生成失败，记录错误日志，继续处理下一个任务，不中断整体流程。

9. 写回与兜底
   9.1 写入 .trae/logs/YYYY-MM-DD.log，记录每步执行结果、N值、G值、新增/删除(冻结)/顺延的任务列表、教程生成情况（生成/跳过/失败，含幂等命中信号：注册表/文件）、新拆解任务列表（如有）、注册表变更明细。
   9.2 所有步骤完成后，统一提交剩余变更（snapshot.json、excluded.json、日志、HTML/JS 等）：git add . && git commit -m "chore(daily): <TODAY> 每日维护" && git push main || 记录日志"远程 push 失败，本地已 commit"。时序：8.4 的本地 commit 必须先于 8.5（上传飞书云盘不依赖 git push）；8.6 评论需 8.5 已上传取得的 feishu_url；9.2 的 push 在最后，覆盖其余全部变更。
   9.3 汇报本次运行结果。
