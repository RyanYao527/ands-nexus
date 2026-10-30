# ANDS Nexus

把 AI 协作中的任务、责任人、检查和复盘写清楚。`ands-nexus` 是一套可安装的 skill、参考资料和模板，适合已经使用 AI agent、希望先跑通一个小型协作流程的团队。

**当前正式版：v0.4.6。** 从 [START-HERE](START-HERE.md) 开始，完成一次约 10 分钟的虚构任务练习。

## 快速开始

1. **下载指定版本**：[v0.4.6 Release](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.6) · [安装包](https://github.com/RyanYao527/ands-nexus/releases/download/v0.4.6/ands-nexus-v0.4.6.zip) · [SHA256SUMS.txt](https://github.com/RyanYao527/ands-nexus/releases/download/v0.4.6/SHA256SUMS.txt)。不要用 `main` 代替发布版本。
2. **安装并启用**：按 [安装说明](START-HERE.md#2-安装) 把解压后的 `ands-nexus/` 放到对应目录。已有目录先移到 skills 扫描目录之外备份，再复制到新空目录。
3. **完成 4 步练习**：[任务梳理 → ANDS-T 任务卡 → Track + Gate 检查 → Lessons 草稿](START-HERE.md#4-完成一次四步练习guided-workflow-first-run)。每步由你确认后再继续。
4. **反馈问题**：到 [GitHub Issues](https://github.com/RyanYao527/ands-nexus/issues/new) 提交版本、runtime、步骤、预期、实际和脱敏复现。

| 使用工具 | 用户级安装目录 | 显式调用 |
|---|---|---|
| Codex | `~/.agents/skills/ands-nexus/` | `$ands-nexus` |
| Claude Code | `~/.claude/skills/ands-nexus/` | `/ands-nexus` |
| 其他工具 | 手动加载 `SKILL.md` 和所需路由资料 | 使用自然语言请求 |

目录与调用方式依据 [Codex 官方说明](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)和 [Claude Code 官方说明](https://code.claude.com/docs/en/skills)。If you are not using Codex，请选择上表中的 Claude Code 或手动加载方式。Windows PowerShell 和 macOS/Linux 的可复制安装命令均在 [START-HERE](START-HERE.md)。

## 可以用它做什么

- 把模糊需求写成有目标、约束、验收标准和责任人的 ANDS-T。
- 按风险选择 Quick / Standard / Enterprise Track，并区分机器检查与人的验收。
- 明确 AI PM、执行、验证、治理和知识回写的分工。
- 用 30 天小型试点、复盘和可复用 Lessons 改善团队协作。

需要更完整的例子时，查看 [示例索引](examples/INDEX.md)、[引导式首跑](examples/guided-workflow-first-run-v0.4.md)或[简短首跑](examples/first-run-prompt-packet-v0.3.1.md)。根目录 `examples/` 便于浏览；skill 内 `ands-nexus/examples/` 提供 `SKILL.md` 路由所需的安装副本。

## v0.4.6 的证据与限制

本版整理学员入口、安装与反馈说明，承接 H 轮历史交接基线。**H 轮历史记录是核心项 24/24、两条多轮链通过；同时旧 7 题出现比例性下降，简洁性仍未收尾。** 历史结果不能替代本次验证，也不能表示所有问题已解决。

| 验证项 | v0.4.6 状态 |
|---|---|
| 本地发布与模板验证、回归脚本 | Windows PowerShell 5.1 / PowerShell Core 均通过；命令和范围见 [验证摘要](VALIDATION.md) |
| 安装命令隔离测试 | 双 PowerShell 与 Windows Git Bash 各测 Codex / Claude Code 的首次安装、升级和回退，六组通过；未在原生 macOS/Linux 实测 |
| 安装包内容、VERSION、SHA-256 | 41 个技能文件，含 `VERSION=0.4.6` 和 MIT 许可；附件从固定 tag 构建，提供 SHA256SUMS.txt |
| 真人学员试用 | 尚无本次真人反馈，不作通过声明 |

当前证据限于文档、本地验证和 synthetic 示例；不构成 provider-native/runtime 能力证明，不声明 Q25 通过，也不提供厂商能力排名或采购结论。

首次练习使用虚构任务。`data_class` 描述输入材料类别；`PASS / NEEDS_REDACTION / BLOCKED` 描述材料能否公开，两者不是同一个判断。真实客户数据、凭据、租户系统、公开能力声明、合同承诺或采购建议应转 Enterprise 审查。普通脱敏教学材料可采用 Standard 并加强 Gate 4。

Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.

Writeback boundary: user-invoked draft generation to an explicit path is allowed only when explicitly requested. 只生成草稿或写入你明确指定的本地路径，不扫描或批量修改 Vault，不做 GitHub sync、provider workspace 写入或企业系统更新。本包不提供完整课程、生产级 AI Gateway、托管工作流或一键部署平台。

## 维护者验证

学员无需先运行验证脚本。以下命令在**固定 tag 的完整源码仓库根目录**运行；安装 ZIP 只含 skill，不等同于完整源码仓库。

依赖 PowerShell 和 `rg`。macOS/Linux 可用 PowerShell Core；macOS 安装命令为 `brew install powershell ripgrep`，Linux 使用发行版对应的软件包。Windows 可用 PowerShell Core 或 Windows PowerShell 5.1。

```powershell
pwsh -NoProfile -File ./ands-nexus/scripts/validate_templates.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/test_writeback_mvp.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/validate_release.ps1
```

Windows PowerShell 5.1 可将 `pwsh` 换成 `powershell.exe`。`quick_validate.py is external`：它不在本仓库；未传入 `-QuickValidatePath` 时，发布验证会明确输出 `SKIP quick_validate (no -QuickValidatePath; external Codex skill-creator tool not in repo)`，不应记作已执行。GitHub Actions 只做发布验证，不自动发布。

Windows 读取中文异常时，使用 `Get-Content -Raw -Encoding UTF8 ./ands-nexus/SKILL.md`。

## 版本与许可

- [v0.4.5](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.5)：上一正式版，可作为固定回退版本。
- [完整发布记录](RELEASE_NOTES.md) · [发布检查表](PUBLISHING_CHECKLIST.md) · [反馈模板](examples/post-release-feedback-intake-v0.3.1.md)。
- [MIT License](LICENSE)。
