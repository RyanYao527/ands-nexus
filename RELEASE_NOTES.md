# Release Notes

## v0.4.6 - 2026-10-30

面向学员的正式补丁：补全新会话交接信息，并提供下载、安装、升级、首跑、反馈和回退的短路径。

Release: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.6>

### Changed

- Next Prompt 携带已确认任务事实、Acceptance、当前所需产物和未知项；保留六段输出和 13 个 State 字段。
- 明确当前 Owner 回复、示例/模拟回复、草稿推进及 Gate 2 / Gate 3 的区别；新会话可继续生成当前请求的草稿。
- 中文学员入口、Codex / Claude Code 安装说明及其他工具的手动加载路径。
- 安装到明确的新目录；升级备份移出技能扫描目录，提供恢复旧版和固定 v0.4.5 的路径。
- 提供独立技能 ZIP、SHA256 校验文件、安装包 VERSION 和 GitHub Issues 反馈入口。

### Validation And Known Limits

验证范围与本次结果见 [VALIDATION.md](VALIDATION.md)。交接行为采用已验证 H 快照的四份文件；历史 24 项核心行为判定（其中含 8 次留出试跑）及两条四步链通过。本次安装和首跑检查另列，不能把历史结果表述为所有客户端均已验证。

H 的 7 项篇幅比例性下降和后续简洁性评审未决继续保留；本版不声称输出质量收尾完成，也不声称 Q25 完整矩阵通过。输出可能偏长，用户仍需检查事实、缺失证据和待决事项。

本版保持 documentation-first：不新增 helper、API integration、credential setup、tenant connectors、unattended or automated writeback 或 benchmark ranking。客户端中的合成首跑不证明供应商能力、生产集成或团队长期收益；暂无真人使用反馈。

## v0.4.5 - 2026-08-19

`v0.4.5` 已完成公开 patch release execution。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.5>

### Summary

`v0.4.5` is a bounded release-engineering patch that improves release validation maintainability and cross-runtime script compatibility after `v0.4.4`. It does not change the public evidence boundary.

### Added

- `release-manifest.json` as the source of truth for release asset groups, expected counts, and required files.
- `.github/workflows/release-validation.yml` as a minimal GitHub Actions validation gate.
- `ands-nexus/references/one-page-glossary-card.md` as a short first-run terminology card with Chinese aliases.
- `examples/source-provenance-bundle-v0.4.md` as a public-safe source provenance bundle example.

### Changed

- `validate_release.ps1` now reads release asset requirements from `release-manifest.json` instead of hardcoding asset counts.
- Release validation is expected to pass under both PowerShell Core and Windows PowerShell 5.1.
- The GitHub Actions regression guard now rejects write permissions and common release-publishing actions.
- README and publishing checklist document the `v0.4.5` release-engineering patch scope.

### Validation Evidence

- `pwsh -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1`: PASS.
- `powershell.exe -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1`: PASS.
- `pwsh -NoProfile -File ./ands-nexus/scripts/validate_release.ps1`: PASS.
- `powershell.exe -NoProfile -File ./ands-nexus/scripts/validate_release.ps1`: PASS.
- `pwsh -NoProfile -File ./ands-nexus/scripts/validate_templates.ps1`: PASS.
- `git diff --check`: PASS.
- Public package scan: PASS via `validate_release.ps1`.
- Independent reviewer: PASS; no Critical or Important findings after minor consistency fixes.
- Final release execution validation: PASS.

### Non-Scope

- No first-user wording patch beyond the glossary/provenance hardening assets in this release-engineering patch.
- No provider-native validation.
- No API integration.
- No credential setup.
- No tenant connectors.
- No unattended or automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.

## v0.4.4 - 2026-08-19

`v0.4.4` 已完成公开 patch release execution。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.4>

### Summary

v0.4.4 is a bounded governance-boundary wording patch opened from v0.4.3 retest feedback. It keeps the v0.4 documentation-first guided workflow scope and improves first-run clarity for desensitization outcomes, Track gray zones, plain-language boundary terms, and explicit-path writeback limits.

### Changed

- Add a one-page boundary card to `START-HERE.md` covering `data_class`, `PASS / NEEDS_REDACTION / BLOCKED`, external-visible delivery, public claims, explicit paths, Vault scans, no provider-native validation, and no tenant connectors.
- Clarify that `data_class` is input/context classification, while `PASS / NEEDS_REDACTION / BLOCKED` is publication-readiness judgment for examples or feedback.
- Add first-run glossary entries for `PASS`, `NEEDS_REDACTION`, `BLOCKED`, explicit path, Vault scan, no provider-native validation, no tenant connectors, external-visible low-risk delivery, and public claim.
- Align Track and Gate wording so low-risk external-visible desensitized examples/templates can remain Standard with stronger Gate 4 only when they make no public capability claim, customer commitment, contract/compliance statement, provider comparison, or procurement advice.
- Clarify that public claims, provider comparisons, procurement advice, customer commitments, contract/compliance statements, real customer impact, sensitive data, hard rollback, or connector work require Enterprise review.
- Tighten Obsidian writeback wording so `-OutputPath` parent directory creation is limited to the human-specified local draft path and does not authorize Vault scans, GitHub sync, provider workspace writes, or enterprise-system updates.
- Route seed-user and post-release feedback triage through `references/glossary.md` so desensitization outcome definitions are available during classification.

### Validation Evidence

- V04-POST12 release readiness: `CONDITIONAL_GO_FOR_V0_4_4_PUBLIC_PATCH_RELEASE_EXECUTION_AFTER_REQUIRED_WORDING_FIXES`.
- V04-POST12A required wording fixes: complete and revalidated.
- `pwsh -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1`: PASS.
- `pwsh -NoProfile -File ./ands-nexus/scripts/validate_release.ps1`: PASS.
- `pwsh -NoProfile -File ./ands-nexus/scripts/validate_templates.ps1`: PASS.
- `git diff --check`: PASS.
- Public package scan: PASS.
- Asset counts unchanged: root examples 20, installable routed examples 6.
- Final release execution validation: PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup.
- No tenant connectors.
- No unattended or automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.
- No A3/A5 script or validator hardening.
- No GitHub Actions.
- No manifest-driven asset-count refactor.
- No desensitized Obsidian/canvas source-file bundle.
- No v0.5 automation discovery.

## v0.4.3 - 2026-08-19

`v0.4.3` 已完成公开 patch release execution。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.3>

### Summary

v0.4.3 is a bounded governance consistency and guided workflow polish patch. It keeps the v0.4 documentation-first guided workflow scope and clarifies writeback boundaries, external-visible Track gray zones, runtime workflow roles, desensitization outcomes, glossary wording, and guided first-run state continuity.

### Changed

- Align writeback wording across multi-agent adaptation, adapter card, forward-test, guided workflow, and public docs: candidate Lessons remain the default; explicit-path local draft generation is allowed only when explicitly requested; unattended persistence, Vault scans, GitHub sync, provider workspace writes, and enterprise-system updates remain out of scope.
- Clarify Track treatment for external-visible work: Quick has no external delivery or contractual/customer impact; low-risk external-visible delivery can stay Standard only when it has no sensitive data, customer commitment, or real customer impact; contractual/customer/real customer impact triggers Enterprise review.
- Add runtime workflow role versus ANDS-A L1/L2/L3 clarification.
- Add PASS / NEEDS_REDACTION / BLOCKED desensitization criteria.
- Add `stop:` to the `owner_response` glossary entry.
- Fix guided first-run state-chain continuity around Step 2 missing evidence and Gate 1 status.
- Add plain-language boundary explanations for first-run users.

### Validation Evidence

- Release readiness decision: `GO_FOR_V0_4_3_PUBLIC_PATCH_RELEASE_EXECUTION_WITH_CONSTRAINTS`.
- Independent read-only reviewer: 0 Critical; Important findings resolved before release execution.
- `pwsh -NoProfile -File ./ands-nexus/scripts/test_validate_release.ps1`: PASS.
- `pwsh -NoProfile -File ./ands-nexus/scripts/validate_release.ps1`: PASS.
- `pwsh -NoProfile -File ./ands-nexus/scripts/validate_templates.ps1`: PASS.
- `git diff --check`: PASS.
- Root/installable guided first-run example comparison: PASS, no differences.
- Final release execution validation: PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup.
- No tenant connectors.
- No unattended or automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.
- Windows PowerShell 5.1 validator parser compatibility remains a separate A3/A5 hardening backlog item; this release uses PowerShell Core validation evidence.

## v0.4.2 - 2026-08-18

`v0.4.2` 已完成公开 patch release execution。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.2>

### Summary

v0.4.2 is a bounded owner response boundary micro patch opened from v0.4.1 post-release verification and first-user retest evidence. It keeps the v0.4 documentation-first scope and prevents copyable first-run prompts from pre-filling sample human owner decisions.

### Changed

- Replace prefilled copyable prompt-block `owner_response: confirm: ...` examples with placeholders.
- Add explicit instruction to replace `owner_response` with the human owner's actual reply before sending each Step Prompt.
- Clarify that example owner response values are format demonstrations only.
- Include `stop:` consistently in owner response examples.
- Add validator assertions that reject the old prefilled prompt-block pattern.

### Validation Evidence

- `test_validate_release.ps1`: PASS.
- `validate_release.ps1`: PASS.
- `validate_templates.ps1`: PASS.
- `git diff --check`: PASS.
- Release readiness Go / No-Go: `GO_FOR_V0_4_2_RELEASE_EXECUTION_AFTER_FINAL_VALIDATION`.
- Final release execution validation: PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup.
- No tenant connectors.
- No unattended or automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.

## v0.4.1 - 2026-08-18

`v0.4.1` 已完成公开 patch release execution。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.1>

### Summary

v0.4.1 is a bounded stabilization patch for the v0.4 guided workflow first-run path, opened from U1-U5 real/desensitized first-user feedback. It keeps the v0.4 documentation-first scope and improves package availability, onboarding clarity, owner decision carry-forward, writeback boundary wording, template mapping, validation transparency, and Track/Gate ownership language.

### Changed

- Improve non-Codex and macOS/Linux onboarding.
- Add first-run glossary coverage.
- Make SKILL-routed examples available inside the installable skill folder.
- Add `owner_response` carry-forward to the guided workflow.
- Unify writeback wording: no unattended or automated writeback; user-invoked draft generation to an explicit path is allowed only when explicitly requested.
- Add guided lite to formal template mapping.
- Make `quick_validate.py` status explicit as external / skipped when no path is supplied.
- Clarify Track gray zones and Gate 1 human owner responsibility.

### Validation Evidence

- `test_validate_release.ps1`: PASS.
- `validate_release.ps1`: PASS, including `SKIP quick_validate` when no external `-QuickValidatePath` is supplied.
- `validate_templates.ps1`: PASS.
- `git diff --check`: PASS.
- Release readiness Go / No-Go: `GO_FOR_V0_4_1_RELEASE_EXECUTION_AFTER_FINAL_VALIDATION`.
- Final release execution validation: PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup.
- No tenant connectors.
- No unattended or automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.

## v0.4.0 - 2026-08-18

`v0.4.0` 已完成公开发布执行。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.0>

### Summary

v0.4.0 adds a documentation-first guided workflow MVP. It helps a first-time user move through Intake Snapshot, ANDS-T Task Card, Track + Gate Checklist, and Lessons Draft with visible state, owner decisions, and copy-ready next prompts.

Scope remains bounded to references, templates, examples, routing, and validation. Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.

### Added

- `ands-nexus/references/guided-workflow-mvp.md`: four-step workflow, state model, role boundaries, Enterprise triggers, and Non-Scope boundary.
- `ands-nexus/assets/templates/guided-workflow-state-packet.md`: reusable state packet with stable field names.
- `examples/guided-workflow-first-run-v0.4.md`: synthetic four-step first run.
- `examples/guided-workflow-regression-v0.4.md`: role, Gate, owner-decision, writeback, and Enterprise escalation regression prompts.

### Changed

- `SKILL.md`, `START-HERE.md`, `README.md`, and `examples/INDEX.md`: routing and reader entry updates.
- `validate_templates.ps1`: template manifest checks.
- `validate_release.ps1` and `test_validate_release.ps1`: v0.4 asset manifest and content assertions.

### Validation Evidence

Candidate package validation on 2026-08-18:

- `test_validate_release.ps1`: PASS.
- `validate_release.ps1 -QuickValidatePath ...`: PASS.
- `quick_validate.py`: PASS during release execution; external Codex skill-creator tool, not included in this repository.
- `git diff --check`: PASS.
- Public package scan: PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup, no tenant connectors, and no unattended or automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.

## v0.3.1 - 2026-08-18

`v0.3.1` 已完成公开 patch release 执行。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.3.1>

### Summary

v0.3.1 is a post-release adoption hardening patch for v0.3.0. It improves the public first-run path, feedback intake, examples discoverability, and role-routing regression coverage. Scope remains unchanged: no provider-native validation, no API integration, no tenant connectors, no automated writeback, and no benchmark ranking.

### Added

- `START-HERE.md`: a short first-run guide for new users.
- `examples/INDEX.md`: an examples index grouped by first-run, adoption, feedback, regression, and provider adaptation use.
- `examples/post-release-feedback-intake-v0.3.1.md`: a v0.3+ feedback template with evidence-level and boundary fields.
- `examples/first-run-prompt-packet-v0.3.1.md`: a 10-minute ANDS-T + Gate + Lessons prompt packet.
- `examples/role-routing-regression-scenarios-v0.3.1.md`: synthetic scenarios for AI PM, Execution, Validation, Governance, and Writeback role separation.

### Changed

- README now points new users to the v0.3.1 first-run path.
- `SKILL.md` routes first-run, post-release feedback, and role-routing regression tasks to the new v0.3.1 assets.
- Release validation now treats `START-HERE.md` and the new v0.3.1 examples as required public package assets.

### Validation Evidence

- `test_validate_release.ps1`: PASS.
- `validate_release.ps1 -QuickValidatePath ...`: PASS.
- `quick_validate.py`: PASS.
- `git diff --check`: PASS.
- Public package scan: PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup, no tenant connectors, and no automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.

## v0.3.0 - 2026-08-17

`v0.3.0` 已完成公开发布执行。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.3.0>

### Summary

v0.3.0 publishes the v0.3 offline/provider-adaptation documentation package. The scope is limited to offline/proxy provider adaptation references, prompt/profile/template-level guidance, provider labels, role-routing matrix patterns, synthetic/proxy forward-test methodology, and governance boundaries for future Enterprise work.

### Added

- Offline provider adaptation references and handoff patterns.
- Prompt/profile/template-level guidance for multi-runtime ANDS usage.
- Provider label and role-routing matrix patterns.
- Synthetic/proxy forward-test methodology.
- Governance boundaries for future provider-native/API/tenant/connector/writeback work.

### Validation Evidence

- AD46 release readiness intake and evidence map completed.
- AD47 v0.3 release-readiness review spec completed.
- AD48 readiness decision: `READY_FOR_RELEASE_CANDIDATE_PREP_AUTHORIZATION_REVIEW`.
- AD49 bounded candidate documentation prep authorization completed.
- AD50 bounded documentation edit validation completed.
- AD56 release candidate prep chain closeout completed.
- AD57A Project Owner explicit release Go confirmed: `确认 v0.3.0 public release Go`.
- Final release execution validation PASS.

### Non-Scope

- No provider-native validation.
- No API integration.
- No credential setup, no tenant connectors, and no automated writeback.
- No benchmark ranking, best-provider result, procurement guidance, or public provider capability claim.

## v0.2.2 - 2026-08-13

`v0.2.2` 已完成公开发布执行。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.2.2>

### Summary

v0.2.2 adds a limited, provider-neutral multi-agent/model adapter pack for prompt/profile/template-level ANDS adaptation. It helps teams run comparable desensitized trials across Codex/OpenAI baseline, KIMI, GLM, MiniMax, Claude, DeepSeek, and WorkBuddy labels. Non-Scope: no provider-native validation, no API integration, no automated writeback, and no benchmark ranking.

### Added

- `multi-agent-model-adaptation.md`：provider-neutral guidance for adapting ANDS workflows to another agent/model runtime.
- `capability-matrix-template.md`：shared matrix for comparing runtime observations.
- `agent-model-adapter-card.md`：profile template for runtime-specific prompt packets.
- `provider-profile-cards-v0.2.2.md`：initial profile labels for Codex/OpenAI baseline, KIMI, GLM, MiniMax, Claude, DeepSeek, and WorkBuddy.
- `agent-model-adaptation-forward-test-v0.2.2.md`：shared five-role forward-test suite.

### Changed

- `SKILL.md` adds a route for adapting ANDS to another agent/model runtime.
- `governance-and-metrics.md` and `adoption-playbook.md` add multi-runtime Standard / Enterprise boundaries.
- README documents v0.2.2 development scope and non-scope.
- Prompt packets now strengthen execution, validation, and writeback boundaries after T09 proxy-trial findings.

### Validation Evidence

- Template validation requires the adapter card and capability matrix templates.
- Release validation checks updated reference/template/example counts.
- Aggregator regression checks provider labels and unsupported integration-claim boundaries.
- T09 provider-profile proxy trial completed with `PASS_WITH_FIXES_FOR_T10_INPUT`.
- T10 release readiness decision is `READY_FOR_PUBLIC_V0.2.2_RELEASE_EXECUTION` for the limited prompt/profile/template adapter pack.
- final release execution validation PASS.

### Non-Scope

- No live provider API integration.
- No credential setup, no tenant connectors, and no automated writeback.
- No public benchmark ranking or current vendor capability claims.

## v0.2.1 - 2026-08-13

`v0.2.1` 已完成 patch release 审批、最终验证、tag 和 GitHub release。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.2.1>

### Summary

v0.2.1 聚焦 v0.2.0 公开发布后的稳定化：新增反馈入口、30-day pilot template、release validation aggregator 和保守 line-ending policy，帮助后续 patch release 与试点扩围更稳。

### Added

- `30-day-pilot-template.md`：用于管理者把 ANDS 试点压缩成 30 天可执行计划。
- `post-release-feedback-intake-v0.2.1.md`：用于公开发布后的脱敏反馈入口。
- `validate_release.ps1`：聚合 template validation、writeback MVP test、optional skill quick validation、asset counts 和公开包扫描。
- `test_validate_release.ps1`：覆盖 release validation aggregator 的 happy path、quick validation failure 和 public scan blocking 行为。
- `.gitattributes`：为 Markdown、YAML、PowerShell 等文本文件声明 LF 行尾策略。

### Changed

- `SKILL.md` adoption route 增加 30-day pilot template。
- `SKILL.md` feedback route 增加 post-release feedback intake。
- README 更新为 v0.2.1 public patch release 状态和 release validation commands。

### Validation Evidence

- `test_validate_release.ps1` PASS：覆盖 aggregator happy path、quick validation failure 和 public scan blocking。
- `validate_release.ps1 -QuickValidatePath ...` PASS：template validation、writeback MVP、skill quick validation、asset counts、public package scan。
- `quick_validate.py` PASS：`Skill is valid!`。
- v0.2.1 release readiness check：`READY_FOR_OWNER_GO_NO_GO`。
- Governance & Security：`PASS_WITH_NOTE`，无 Critical / Important blocker。
- Project Owner Go 已确认。
- final patch release execution validation PASS。

### Security And Desensitization

- 未发现真实组织/公司、人员、仓库、域名、IP、凭据、本地绝对路径或业务敏感数据进入发布包。
- public package scan 会阻断通用 user home path、URL、IP 和 secret-like patterns；公开 GitHub release URL 与 checklist 中的说明性扫描命令文本为允许项。
- 发布后反馈 intake 要求先脱敏，再转成修订任务、regression prompt 或 Lessons。

### Compatibility

- 保持 Codex skill 结构：`ands-nexus/SKILL.md`、`agents/openai.yaml`、`references/`、`assets/templates/`、`scripts/`。
- 不引入外部运行时依赖；新增验证脚本为可选 PowerShell helper。
- 不改变 LICENSE；当前仍为 MIT。

### Known Limits

- 不是完整课程仓库。
- 不提供生产级 AI Gateway、Dashboard、GitHub Actions 或完整 Obsidian 自动化。
- 真实反馈进入 examples 或 validation 前仍需脱敏。

## v0.2.0 - 2026-08-13

`v0.2.0` 已完成公开发布审批、最终验证、tag 和 GitHub release。

Release URL: <https://github.com/RyanYao527/ands-nexus/releases/tag/v0.2.0>

### Summary

v0.2.0 聚焦内部反馈后的可用性补强：Windows UTF-8 读取、forward-test 场景、种子反馈 intake、Track/Gate 反模式、Acceptance / Gate 2 / Gate 3 拆分，以及 Obsidian writeback MVP。

### Added

- Windows PowerShell UTF-8 读取提示，帮助用户用 `Get-Content -Raw -Encoding UTF8` 恢复中文 Markdown 阅读。
- Windows UTF-8 诊断命令，帮助 seed user 检查 `ContainsExpectedChinese` 与 `ContainsCommonMojibake`。
- v0.2 forward-test scenario corpus，覆盖 UTF-8、反馈归类、反模式和 Obsidian writeback MVP。
- 种子用户反馈 intake 模板，用于把脱敏后的真实反馈转成可分派任务和 regression prompt。
- Obsidian writeback MVP：`new_writeback_note.ps1`、`test_writeback_mvp.ps1` 和 `writeback-note-template.md`。

### Changed

- 增强 management-facing overview/adoption guidance，强调结论先行、风险、投入、验收责任和度量。
- 将常见反模式并入 `governance-and-metrics.md` 与 `adoption-playbook.md`。
- 扩展 Track Decision Card 和 Gate Checklist，要求声明风险、可回滚性、敏感数据、验收人和失败动作。
- 根据 5-Agent seed-user trial 小修 Gate FAQ、Acceptance / Gate 2 / Gate 3 拆分例和 writeback `type / domain / pipeline` 变体说明。

### Validation Evidence

- `test_writeback_mvp.ps1` 已按 TDD 流程先失败后通过。
- `validate_templates.ps1` 已扩展到检查 writeback note template。
- `quick_validate.py` PASS：`Skill is valid!`。
- 5-Agent seed-user read-only trial PASS；FT-SU04 为 PASS_WITH_NOTE，已通过 seed-user feedback polish 修正。
- T09/T10 Enterprise review：`CONDITIONAL_GO`，无 Critical blocker。
- Project Owner Go 已确认。
- final release execution validation PASS。

### Security And Desensitization

- 未发现真实公司、人员、仓库、域名、IP、凭据、本地绝对路径或业务敏感数据进入发布包。
- secret/token 扫描的 `token` 命中位于“禁止凭据”的脱敏说明中，不代表真实泄露。
- Obsidian writeback MVP 只生成草稿或写入用户显式提供的 `-OutputPath`；不扫描或批量改写 Vault。
- 当显式 `-OutputPath` 的父目录不存在时，脚本可能创建该父目录；该行为只发生在用户明确给出的路径内。

### Compatibility

- 保持 Codex skill 结构：`ands-nexus/SKILL.md`、`agents/openai.yaml`、`references/`、`assets/templates/`、`scripts/`。
- 不引入外部运行时依赖；PowerShell 脚本面向 Windows PowerShell / PowerShell Core 常规环境。
- 不改变 LICENSE；当前仍为 MIT。

### Known Limits

- 不是完整课程仓库。
- 不提供生产级 AI Gateway、Dashboard、GitHub Actions 或完整 Obsidian 自动化。
- 不承诺所有团队都适合一次性全量引入五道 Gate。
- 真实反馈进入 examples 或 validation 前仍需脱敏。

## v0.1.0 - 2026-08-12

`ands-nexus` v0.1.0 将 ANDS 方法论整理为一个可安装的 Codex skill，优先支持管理落地与最小实践模板。

### 新增内容

- 新增 `ands-nexus/SKILL.md`，包含任务路由、输出层级、ANDS 原则检查和 Gate 5 回写提醒。
- 新增 `agents/openai.yaml`，用于 Codex skill 展示元信息。
- 新增 7 个 references：overview、五标准、十模型、五平台组件、采用路线、治理与度量、demo trace。
- 新增 6 个 templates：ANDS-T、ADR、Gate Checklist、Track Decision Card、Agent Matrix、Lessons。
- 新增 7 个 examples，覆盖管理落地、ANDS-T、Gate、Lessons、demo trace、脱敏说明和种子用户 prompt。
- 新增模板校验脚本 `ands-nexus/scripts/validate_templates.ps1`。
- 更新 GitHub 读者文档：README、release notes、publishing checklist。

### 验证状态

- `quick_validate.py`：PASS。
- `validate_templates.ps1`：PASS。
- 5 条验收 prompt 材料回归：PASS。
- Governance & Security 审查结论：PASS_WITH_NOTES，无 Critical / Important 阻断。
- Project Owner 已确认公开发布。
- Project Owner 已确认正式采用当前 MIT License。

### 已知限制

- v0.1 不是完整课程仓库。
- v0.1 不提供生产级 AI Gateway、Dashboard、GitHub Actions 或 Obsidian 自动化。
- 当前 LICENSE 已确认为 MIT。
- v0.1.0 发布前脱敏复核已完成。
- 真实运行和 forward-test 可作为 v0.2 前的补充验证。

### 下一步

- 将公开发布完成结果回写到 Gate 5 状态快照和 ADR。
- 收集种子用户试用反馈，形成 v0.2 改进项。
