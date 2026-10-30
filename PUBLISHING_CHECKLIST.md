# Publishing Checklist

本清单用于 `ands-nexus` skill 的内部试用、release candidate 准备和公开发布执行检查。本次版本是 `v0.4.6`；发布状态以 [GitHub Release](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.6) 为准。较早章节保留历史事实。

## v0.4.6 Student Patch

- [x] Owner 已授权独立分支、有限发布检查、PR / CI / 合并及正式 Release。
- [x] Owner 已明确选择 Codex 首发；保留 Claude 安装说明及当前 DeepSeek 配置未通过的事实。
- [x] H 冻结清单 69 文件校验一致，先引入相对主线的四份交接文件，再针对本次首跑失败做定点修正；Q25 工作区和历史结果保留。
- [x] 发布范围固定为交接修复、学员入口、安装升级回退、反馈和版本附件；helper 与完整质量研究后移。
- [x] 安装包、首次安装、升级、回退和本地引用检查完成。
- [x] Windows PowerShell 5.1 / PowerShell Core 包检查完成。
- [x] Codex 四步合成链、最终模板定点复测与四项聚焦行为检查完成；分别保留版本来源，Claude Code 实测失败如实披露。
- [x] Codex 首发范围下独立发布复核无新增阻断项，git diff --check 通过。

发布执行顺序：对应提交的 PR CI 通过后合并，主线 CI 通过后建立 v0.4.6 标签；从标签构建 ZIP / SHA256SUMS.txt，创建非草稿、非预发布 Release；重新下载校验，并同步项目 Hub 与 Lessons。实际 PR、主线 CI、标签提交、附件哈希和回下载结果统一记录在 [Release 正文](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.6)，不将打标签前的清单当作已发生的发布证明。

本版的有限发布检查结果见 [VALIDATION.md](VALIDATION.md)。历史 H 的行为证据、简洁性缺口与本次实际检查分别记录；未完成项不记为通过。

## v0.4.5 Public Patch Release Execution

本节记录 `v0.4.5` release-engineering patch 公开 release execution 状态。

- [x] Windows PowerShell 5.1 validator parser compatibility 已纳入 A3/A5 hardening，并要求 `powershell.exe` 与 `pwsh` 双 runtime 验证。
- [x] 新增 `release-manifest.json` 作为 release asset groups、expected counts、required files 的唯一来源。
- [x] `validate_release.ps1` 的 asset count 检查改为读取 `release-manifest.json`。
- [x] 新增最小 GitHub Actions release validation gate，只运行验证，不自动发布。
- [x] GitHub Actions guard 保持 `contents: read`，并拒绝 release 发布命令/action 或写权限混入。
- [x] 新增 `ands-nexus/references/one-page-glossary-card.md` 作为术语速查卡。
- [x] 新增 `examples/source-provenance-bundle-v0.4.md` 作为脱敏溯源 bundle 示例。
- [x] 独立 reviewer 复核完成：无 Critical / Important；minor Non-Scope 与 CI guard 一致性项已修。
- [x] Non-Scope 保持不变：no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking。
- [x] Release notes 已更新为正式 `v0.4.5 - 2026-08-19` 公开 patch release 口径。
- [x] Release readiness review 结论：`GO_FOR_V0_4_5_RELEASE_ENGINEERING_PATCH_CANDIDATE_OWNER_GO_REQUIRED`。
- [x] Project Owner Go 已确认。
- [x] Release execution final validation PASS：`pwsh test_validate_release.ps1`、`powershell.exe test_validate_release.ps1`、`pwsh validate_release.ps1`、`powershell.exe validate_release.ps1`、`pwsh validate_templates.ps1`、`git diff --check`。
- [x] Commit completed：`docs: release v0.4.5 engineering hardening patch`。
- [x] 创建并推送 `v0.4.5` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.5>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.4.4 Public Patch Release Execution

本节记录 `v0.4.4` governance-boundary wording 公开 patch release execution 状态。

- [x] V04-POST10 v0.4.3 retest round 01 completed：0 Critical / 5 Important / 10 Minor / 8 Observation。
- [x] V04-POST11 bounded governance-boundary patch implementation completed and validated。
- [x] V04-POST12 release readiness review completed：`CONDITIONAL_GO_FOR_V0_4_4_PUBLIC_PATCH_RELEASE_EXECUTION_AFTER_REQUIRED_WORDING_FIXES`。
- [x] Required wording fixes completed：README plain-language boundary includes `procurement advice`; governance Enterprise summary row includes `采购建议`。
- [x] One-page boundary card added to `START-HERE.md` without adding a new release package asset.
- [x] `data_class` versus `PASS / NEEDS_REDACTION / BLOCKED` clarified on the first-run path and in desensitization guidance.
- [x] A4 Track wording aligned for external-visible low-risk delivery, public claims, provider comparisons, procurement advice, customer commitments, contract/compliance statements, and Enterprise review.
- [x] B2 plain-language terms added for explicit path, Vault scan, no provider-native validation, and no tenant connectors.
- [x] B1 writeback `-OutputPath` wording tightened to the human-specified local draft path.
- [x] A3/A5 script or validator hardening, GitHub Actions, manifest-driven asset counts, desensitized source-file bundle, no API integration, no tenant connectors, no unattended or automated writeback, and v0.5 automation discovery were kept out of scope.
- [x] Release notes updated to public `v0.4.4 - 2026-08-19`口径。
- [x] Release execution final validation PASS：`pwsh test_validate_release.ps1`、`pwsh validate_release.ps1`、`pwsh validate_templates.ps1`、`git diff --check`。
- [x] Windows PowerShell 5.1 validator parser compatibility 不作为本 release PASS 证据，继续保留为 A3/A5 hardening backlog。
- [x] 创建并推送 `v0.4.4` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.4>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.4.3 Public Patch Release Execution

本节记录 `v0.4.3` governance consistency + guided polish 公开 patch release execution 状态。

- [x] V04-POST08 release readiness review completed：`GO_FOR_V0_4_3_PUBLIC_PATCH_RELEASE_EXECUTION_WITH_CONSTRAINTS`。
- [x] 独立 reviewer Critical 0；Important findings 已在 release execution 前修复。
- [x] B1 writeback wording 已对齐：candidate-only 默认；显式路径 local draft 仅在用户明确请求时允许；不授权无人值守、Vault scan、GitHub sync、provider workspace 或企业系统写入。
- [x] A4 Track 外部交付灰区已对齐：Quick 无外部交付/合同/客户影响；低风险外部可见可 Standard + Gate 4；合同/客户承诺/真实客户影响升级 Enterprise。
- [x] A6 runtime workflow role 与 ANDS-A L1/L2/L3 已说明；脱敏三值 PASS / NEEDS_REDACTION / BLOCKED 已补。
- [x] B2 first-run 人话边界说明已补。
- [x] BL-03 `owner_response` glossary 已补 `stop:`。
- [x] BL-05 guided first-run state-chain 已小修，且 root / installable copies 保持一致。
- [x] Release notes 已从 candidate wording 改为 public `v0.4.3 - 2026-08-19` 口径。
- [x] Release execution final validation PASS：`pwsh test_validate_release.ps1`、`pwsh validate_release.ps1`、`pwsh validate_templates.ps1`、`git diff --check`、guided example comparison。
- [x] Windows PowerShell 5.1 validator parser compatibility 不作为本 release PASS 证据，已保留为 A3/A5 hardening backlog。
- [x] 创建并推送 `v0.4.3` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.3>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.4.2 Public Patch Release Execution

本节记录 `v0.4.2` owner_response 边界微补丁公开 release execution 状态。

- [x] POST03 A1 High safety / boundary regression 已复核：copyable prompt blocks 不应预填 `owner_response: confirm: ...`。
- [x] 已把 copyable Step Prompt 中的 prefilled owner_response 改为 `<owner reply: confirm/revise/escalate/stop: ...>` 占位符。
- [x] 已新增发送 Step Prompt 前替换 `owner_response` 的显式提示。
- [x] 已在 guided workflow reference 标明示例 owner_response 仅为格式演示。
- [x] 已补齐 `stop:` owner response 枚举一致性。
- [x] 已新增 release validator guard，阻断 `- owner_response: confirm:` 回归。
- [x] Candidate implementation validation PASS：`test_validate_release.ps1`、`validate_release.ps1`、`validate_templates.ps1`、`git diff --check`。
- [x] Release readiness Go / No-Go completed：`GO_FOR_V0_4_2_RELEASE_EXECUTION_AFTER_FINAL_VALIDATION`。
- [x] Release notes 已从 candidate wording 改为 public `v0.4.2 - 2026-08-18` 口径。
- [x] Release execution final validation PASS：`test_validate_release.ps1`、`validate_release.ps1`、`validate_templates.ps1`、`git diff --check`。
- [x] 创建并推送 `v0.4.2` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.2>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.4.1 Public Patch Release Execution

本节记录 `v0.4.1` guided workflow 首用户反馈稳定化补丁公开 release execution 状态。

- [x] 修复 non-Codex 使用路径说明：`$ands-nexus` 是 Codex trigger，其他 runtime 可加载 `ands-nexus/SKILL.md` 并按 Task Routing 附加映射文件。
- [x] 修复 macOS/Linux 验证说明：说明 `pwsh` / PowerShell Core 与 `rg` / ripgrep 依赖。
- [x] 修复包结构可达性：`SKILL.md` 路由引用的 examples 在 `ands-nexus/examples/` 中有 installable copy。
- [x] 新增或验证 `ands-nexus/references/glossary.md`，并从 START-HERE / SKILL / validator 链接。
- [x] guided workflow 增加 `owner_response` slot，支持 `confirm:` / `revise:` / `escalate:` / `stop:` 回填。
- [x] 统一 writeback 边界：no unattended or automated writeback；user-invoked draft generation to an explicit path is allowed only when explicitly requested。
- [x] 明确 guided lite output 到正式 `ands-t-template.md`、`gate-checklist.md`、`lessons-template.md` 的映射。
- [x] validation status 明确 `quick_validate.py` 为 external tool，不传 `-QuickValidatePath` 时输出 SKIP。
- [x] Track/Gate owner 口径：Gate 1 owner 是人类 Project Owner，AI PM 仅准备材料与质检；外部交付/合同影响默认至少 Standard + Gate 4 加强，除非 Enterprise 条件出现。
- [x] Candidate implementation validation PASS：`test_validate_release.ps1`、`validate_release.ps1`、`validate_templates.ps1`、`git diff --check`。
- [x] Release readiness Go / No-Go completed：`GO_FOR_V0_4_1_RELEASE_EXECUTION_AFTER_FINAL_VALIDATION`。
- [x] Release notes 已从 candidate wording 改为 public `v0.4.1 - 2026-08-18` 口径。
- [x] Release execution final validation PASS：`test_validate_release.ps1`、`validate_release.ps1`、`validate_templates.ps1`、`git diff --check`。
- [x] 创建并推送 `v0.4.1` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.1>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.1.0 Released Archive

以下为 `v0.1.0` 的历史发布结论，不代表 `v0.2.0` 已完成公开发布审批。

- [x] Project Owner 已确认公开发布。
- [x] Project Owner 已确认正式采用当前 MIT License。
- [x] Governance & Security 结论：PASS_WITH_NOTES，无 Critical / Important 阻断。
- [x] 发布 tag 前最终脱敏复核已完成。
- [x] GitHub release 已发布：`v0.1.0`。

## v0.2.0 Release Candidate Prep

本节记录公开 `v0.2.0` 候选包准备状态；release execution 已在 Project Owner Go 后完成。

- [x] 仓库结构包含 `README.md`、`LICENSE`、`RELEASE_NOTES.md`、`PUBLISHING_CHECKLIST.md`。
- [x] skill folder 名称为 `ands-nexus`。
- [x] `ands-nexus/SKILL.md` frontmatter 只包含 `name` 与 `description`。
- [x] `ands-nexus/agents/openai.yaml` 与 skill 定位一致。
- [x] 7 个 references 齐备。
- [x] 7 个 templates 齐备。
- [x] 9 个 examples 齐备。
- [x] README 没有把 skill 描述成完整课程或生产级平台。
- [x] README 没有承诺一键部署 Gateway、Dashboard、GitHub Actions 或 Obsidian 自动化。
- [x] README 说明当前 LICENSE 为 MIT，且 v0.1 已由 Project Owner 确认。
- [x] README 说明当前公开版本是 `v0.2.0`。
- [x] Release notes 已改为 public-facing `v0.2.0 - 2026-08-13` 口径。
- [x] Obsidian writeback MVP 边界清楚：只生成草稿或写入显式 `-OutputPath`，不扫描或批量改写 Vault。
- [x] T09/T10 Enterprise review 已完成，结论为 `CONDITIONAL_GO`。
- [x] 发布材料没有真实公司、人员、仓库、域名、IP、凭据、本地绝对路径或业务敏感数据。

## v0.2.0 Public Release Execution

公开 GitHub release 执行状态：

- [x] Project Owner 明确确认可公开发布 `v0.2.0`。
- [x] 完成最终 Enterprise Gate 4 Go/No-Go 记录。
- [x] release execution 前重新运行 `quick_validate.py`、`validate_templates.ps1`、`test_writeback_mvp.ps1`。
- [x] release execution 前重新完成最终脱敏扫描，覆盖 README、release notes、publishing checklist、SKILL.md、references、templates、examples、scripts。
- [x] 确认 tag 名、release notes 版本、GitHub release 标题和仓库可见性一致。
- [x] 创建并推送 `v0.2.0` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.2.0>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.2.1 Patch Release Execution

公开 GitHub patch release 执行状态：

- [x] Project Owner 明确确认可执行 `v0.2.1` patch release。
- [x] 完成 `v0.2.1 release readiness check`，结论为 `READY_FOR_OWNER_GO_NO_GO`。
- [x] release execution 前重新运行 `test_validate_release.ps1`、`validate_release.ps1 -QuickValidatePath ...`、`quick_validate.py`。
- [x] release execution 前重新完成最终脱敏扫描，覆盖 README、release notes、publishing checklist、SKILL.md、references、templates、examples、scripts。
- [x] 确认 tag 名、release notes 版本、GitHub release 标题和仓库可见性一致。
- [x] 创建并推送 `v0.2.1` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.2.1>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.2.2 Public Release Execution

公开 GitHub release 执行状态：

- [x] Project Owner 明确确认可公开发布 `v0.2.2`，范围限定为 prompt/profile/template adapter pack。
- [x] 完成 `v0.2.2 release readiness check`，结论为 `READY_FOR_PUBLIC_V0.2.2_RELEASE_EXECUTION`。
- [x] T09 provider-profile proxy trial 已记录为 `PASS_WITH_FIXES_FOR_T10_INPUT`，且未作为 provider-native / API / benchmark 证据。
- [x] release execution 前修复 execution / validation / writeback prompt 边界。
- [x] release execution 前重新运行 `test_validate_release.ps1`、`validate_release.ps1 -QuickValidatePath ...`、`quick_validate.py`。
- [x] release validation 会阻断 unsupported overreach claims；Non-Scope: no provider-native validation, no API integration, no tenant connector readiness, no automated writeback, and no benchmark ranking。
- [x] 确认 tag 名、release notes 版本、GitHub release 标题和仓库可见性一致。
- [x] 创建并推送 `v0.2.2` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.2.2>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.3.0 Public Release Execution

本节记录 `v0.3.0` 公开 GitHub release 执行状态。

- [x] AD49 已授权 bounded candidate documentation prep。
- [x] AD50 文件范围限定为 `README.md`、`RELEASE_NOTES.md`、`PUBLISHING_CHECKLIST.md`。
- [x] Candidate scope 限定为 offline/proxy provider adaptation、prompt/profile/template guidance、role-routing matrix patterns 和 governance boundaries。
- [x] Candidate Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no automated writeback, no benchmark ranking。
- [x] AD50 bounded documentation edit validation 已完成。
- [x] Project Owner 已确认进入 public `v0.3.0` release execution：`确认 v0.3.0 public release Go`。
- [x] release execution 前重新运行 `test_validate_release.ps1`、`validate_release.ps1 -QuickValidatePath ...`、`quick_validate.py`。
- [x] release execution 前重新完成最终脱敏扫描，覆盖 README、release notes、publishing checklist、SKILL.md、references、templates、examples、scripts。
- [x] 确认 tag 名、release notes 版本、GitHub release 标题和仓库可见性一致。
- [x] 创建并推送 `v0.3.0` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.3.0>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.3.1 Patch Release Execution

本节记录 `v0.3.1` post-release adoption hardening patch 执行状态。

- [x] Project Owner 已确认执行 v0.3.1 patch release chain。
- [x] 新增 `START-HERE.md`，帮助新用户从 10 分钟 first run 开始。
- [x] 新增 `examples/INDEX.md`，按 first-run、adoption、feedback、regression、provider adaptation 分组。
- [x] 新增 `examples/post-release-feedback-intake-v0.3.1.md`，补齐 evidence level 和 boundary fields。
- [x] 新增 `examples/first-run-prompt-packet-v0.3.1.md`，覆盖 ANDS-T + Gate + Lessons。
- [x] 新增 `examples/role-routing-regression-scenarios-v0.3.1.md`，覆盖 AI PM、Execution、Validation、Governance、Writeback 分离。
- [x] `SKILL.md` 已更新 first-run、post-release feedback 和 role-routing regression route。
- [x] release validator 已更新 required public package assets。
- [x] release execution 前重新运行 `test_validate_release.ps1`、`validate_release.ps1 -QuickValidatePath ...`、`quick_validate.py`。
- [x] release execution 前重新完成最终脱敏扫描，覆盖 START-HERE、README、release notes、publishing checklist、SKILL.md、references、templates、examples、scripts。
- [x] 确认 tag 名、release notes 版本、GitHub release 标题和仓库可见性一致。
- [x] 创建并推送 `v0.3.1` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.3.1>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## v0.4.0 Public Release Execution

本节记录 `v0.4.0` guided workflow MVP 公开 GitHub release 执行状态。

- [x] V04-T01 package mapping review 已完成，结论为 `V04_GUIDED_WORKFLOW_PACKAGE_MAPPING_READY_FOR_EDIT_AUTHORIZATION`。
- [x] 候选 scope 限定为 documentation-first guided workflow references、templates、examples、routing 和 validation。
- [x] 新增 `ands-nexus/references/guided-workflow-mvp.md`。
- [x] 新增 `ands-nexus/assets/templates/guided-workflow-state-packet.md`。
- [x] 新增 `examples/guided-workflow-first-run-v0.4.md`。
- [x] 新增 `examples/guided-workflow-regression-v0.4.md`。
- [x] `SKILL.md`、`START-HERE.md`、`README.md` 和 `examples/INDEX.md` 已加入 guided workflow candidate path。
- [x] release validator 已要求 9 个 references、11 个 templates、20 个 examples，并检查 guided workflow 内容。
- [x] Candidate validation PASS：`test_validate_release.ps1`、`validate_release.ps1 -QuickValidatePath ...`、`quick_validate.py`、`git diff --check`。
- [x] Reviewer Important findings 已修复：README candidate/release validation 口径、copy-ready state、Validation + Governance、candidate-only writeback 和 validator assertions。
- [x] Candidate Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no automated writeback, no benchmark ranking。
- [x] Project Owner 已明确确认进入 public `v0.4.0` release execution。
- [x] Current v0.4 candidate package 已先完整 commit：`fbe284e`。
- [x] release execution 前重新运行 `test_validate_release.ps1`、`validate_release.ps1 -QuickValidatePath ...`、`quick_validate.py`、`git diff --check`。
- [x] Release notes 已从 candidate wording 改为 public `v0.4.0 - 2026-08-18` 口径。
- [x] 确认 tag 名、release notes 版本、GitHub release 标题和仓库可见性一致。
- [x] 创建并推送 `v0.4.0` tag。
- [x] 创建 GitHub release，并记录 release URL：<https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.0>。
- [x] 完成 Gate 5 release closeout 与 Knowledge Writeback。

## Validation Commands

在仓库根目录推荐使用 PowerShell Core 运行：

```bash
pwsh -NoProfile -File ./ands-nexus/scripts/validate_templates.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/test_writeback_mvp.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/validate_release.ps1
python <path-to-skill-creator>\scripts\quick_validate.py .\ands-nexus
```

macOS/Linux 可使用 PowerShell Core：

```bash
brew install powershell ripgrep
pwsh -NoProfile -File ./ands-nexus/scripts/validate_templates.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/test_writeback_mvp.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1
pwsh -NoProfile -File ./ands-nexus/scripts/validate_release.ps1
```

`validate_release.ps1` 需要 `rg` / ripgrep 进行 public package scan。公开发布文档可以说明 `quick_validate.py` 来自 Codex skill creator；`quick_validate.py` is external and not included in this repository。release execution 文案不应写入机器特定绝对路径。

Windows PowerShell 5.1 compatibility check:

```powershell
powershell.exe -NoProfile -File .\ands-nexus\scripts\test_validate_release.ps1
powershell.exe -NoProfile -File .\ands-nexus\scripts\validate_release.ps1
```

Release asset counts and required-file checks must be updated in `release-manifest.json`; do not hardcode asset counts directly in `validate_release.ps1`.

## Desensitization Scan

release execution 前至少运行：

```powershell
rg -n "BEGIN (RSA|OPENSSH|PRIVATE)|api[_-]?key|secret|password|token|AKIA|sk-[A-Za-z0-9]" .
rg -n "([A-Za-z]:\\Users\\|/Users/|/home/|http[s]?://|\b\d{1,3}(\.\d{1,3}){3}\b)" README.md RELEASE_NOTES.md PUBLISHING_CHECKLIST.md examples ands-nexus
```

`validate_release.ps1` runs an automated version of the same local path / URL / IP scan with allowlisted public GitHub release links and explanatory checklist command text.

说明性命中可以接受，例如“不要填写 token / 凭据”的脱敏红线；真实凭据、真实仓库、真实域名/IP 或本地绝对路径必须阻断发布。

## Gate 5 Writeback

交给 09 Knowledge Writeback 时应回写：

- v0.2.0 release candidate prep 记录。
- T09/T10 Enterprise review 的 `CONDITIONAL_GO` 结论。
- v0.2.1 post-release stabilization 与 release readiness check 记录。
- v0.2.2 multi-agent/model adapter pack readiness、forward-test、release execution 和 provider-native/API/benchmark 边界。
- v0.3 Enterprise discovery 的 V03-T00 Gate plan。
- v0.3.0 release candidate prep、readiness decision、candidate validation、explicit Owner Go 和 public release execution。
- v0.3.1 post-release adoption hardening、patch readiness、release execution 和 v0.4 next-path decision。
- validation 结果与最终脱敏扫描结果。
- Project Owner 发布决策：Go。
- 公开发布结果：tag、release URL、release notes 快照和后续 Lessons。
