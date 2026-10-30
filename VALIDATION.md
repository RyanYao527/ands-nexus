# v0.4.6 验证摘要

Owner 已明确选择 **Codex 首发支持**，保留 Claude 安装说明并披露当前 DeepSeek 配置行为未通过。该范围选择不改变原失败判定，也不把其他 Claude 配置列为已测试。

## 发布来源

基线为 `d1bbbbc000f4054c49e484dbc471e317314b2089`。先引入 H 冻结快照的四份交接文件，清单 SHA256 为 `c7d2f99eab0b9492785619266c4acaae2247983f7d5f244101851d1a293fc7dc`，69 份源文件逐项核验一致。随后根据本次实际首答失败补充回复来源、复盘事实依据、提案标识和返回状态规则；最终包并非原 H 的逐字副本。安装包及仓库中的首跑示例保持相同。

H 历史核心行为：12 场景 × 2 次共 24 项通过，包含 8 次留出试跑；两条四步链另行通过。这些是历史合成测试，不是本次重新执行，也不是所有模型或客户端的兼容保证。

## 本次检查

| 检查 | 状态 |
|---|---|
| Windows PowerShell 5.1 / PowerShell Core 包检查 | `test_validate_release.ps1` 与 `validate_release.ps1` 均通过；包含模板、writeback 回归、清单与扫描；外部 quick_validate 未提供，明确 SKIP |
| ZIP 安装、升级、回退及引用一致性 | 双 PowerShell、Windows Git Bash 各测 Codex / Claude Code，共六组通过；备份在扫描目录外，无嵌套且恢复的 v0.4.5 文件哈希一致；未实测原生 macOS/Linux |
| Codex 四步合成首跑与新会话交接 | Codex CLI 0.163.0 的四个独立新会话通过，实际读取冻结包；最后任务卡模板修正后的 ANDS-T 单次兼容复测通过，版本覆盖见下文 |
| revise / unfilled / stop / CI 与 Gate 3 分离 | 首次修正后的四项聚焦首答通过；停止不继续、缺回复不自授权、CI 不替代 Gate 3。该组不是最终包同源重跑 |
| Claude Code 安装说明与合成练习 | 安装说明及隔离安装通过；现有 Claude Code 2.1.304 + deepseek-flash 配置行为未通过：在新确认后仍停留 Gate，未生成所请求的 Lessons。不是 Anthropic 模型验证；其他 Claude 配置未实测 |
| 独立发布复核与发布执行 | Codex 首发范围下独立复核通过；[PR #1](https://github.com/RyanYao527/ands-nexus/pull/1) 记录合并及对应 CI。主线 CI、tag 与附件校验的实际执行记录见 [Release 正文](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.6) |

安装路径依据：[Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)、[Claude Code](https://code.claude.com/docs/en/skills)。其他工具仅提供手动加载方式，不宣称全部实测。

本地检查曾因新增官方文档 URL 和中文否定表述而失败。扫描器现只剥离两个完整官方文档地址，仍检测同行其他地址和私有路径；新增正例及四种反例通过。否定表述改用既有 Non-Scope 格式，未放宽集成能力声明检查。

本次保留首轮及修后首答中的失败：无当前回复时错误推进；Lessons 补写未经记录支持的轮次和发现时间；未标注的时间端点假设；新 Gate 产物的返回 State 仍停留在 ANDS-T。对应修正后只复测相关路径，原输出及结论不覆盖。各版本结果如下，不将多轮通过结果拼成同源矩阵。

精度修正后的 Claude 定点链：ANDS-T 与 Gate 通过，但 Gate 生成的 Next Prompt 含有陈旧的回复时间说明。下一会话将其置于新填写的 `confirm` 之上，未产生 Lessons，且改变了当前回复的来源表述。该失败保持失败；不能把安装通过或 CI 通过当作此配置的行为通过。Owner 已将该配置排除在本次首发支持范围之外，保留安装说明和失败披露。

### 本次行为覆盖的版本来源

- `9ffd50a`：Codex 的 revise / unfilled / stop / CI 与 Gate 3 分离四项聚焦通过。Claude 本轮发现的问题及原答保留。
- `43cff23`（ZIP `89e4589f…44b21b6`）：Codex Intake → ANDS-T → Gate → Lessons 四步首答通过；每步新建会话，下一输入为上一步完整 Next Prompt，仅替换 Owner 回复。读源、回复来源、六段、13 字段、Gate 缺口和无业务写入均有记录。
- `da5c9be`（ZIP `2213da3c…62ad2c0c`）：仅修改任务卡 Input 的来源精度提示，其余 40 个包文件不变。Codex 重放同一 ANDS-T 输入的兼容检查通过；Claude 重放同一输入后端点修复通过，随后新 Gate 通过、新 Lessons 失败。

这组记录是有限发布检查与受影响路径复测，不是最终包同源完整矩阵，也不是 Q25 验收。所有原输入、原答、实际命令、退出码、读取文件与哈希及失败判据保留在项目发布证据包。

## 保留的限制

- H 有 7 项篇幅比例性下降；后续简洁性补充口径仍有失败及待复核，旧分不改，本版不声明全部解决。
- Q25 的完整行为矩阵、五份新 Owner 抽查与只读 helper 不属于本次发布验收。
- Next Prompt 仍需用户手动复制和填写当前回复；模型可能遗漏字段或偏离格式。
- CI / 包检查通过不等于当前任务的 Gate 3 获得人类批准；示例、模拟回复不能替代实际批准。
- 暂无真人使用反馈；合成首跑不证明供应商能力、生产就绪、团队采用效果或长期收益。
