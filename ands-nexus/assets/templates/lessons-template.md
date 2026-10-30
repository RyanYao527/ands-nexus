# Lessons 回写模板

> 使用方式：复制本模板记录一次交付、延期、失败、风险发现或成功经验。复盘要能驱动下一轮标准改进，不只描述经过。
> 脱敏要求：不要填写真实公司、人员、仓库、域名、IP、凭据或业务敏感数据。
> 事实依据：Event、Impact、Root Cause 和 Detection Gate 只填写记录支持的事实；推测标为待验证，缺证写“未记录/未证实”。未解决不等于此前未发现，不得从缺口推断额外轮次、成本或因果。知识或模板缺失结论须限定实际检查范围；未做相关检查时保留为待核实，不必为填表扩大扫描。

## Lesson Meta

- Lesson ID: `[填写脱敏编号]`
- Date: `[YYYY-MM-DD]`
- Related Task: `[[填写 ANDS-T 任务卡]]`
- Related Release / PR: `[[填写脱敏交付记录；无则写“无”]]`
- Track: `[Quick | Standard | Enterprise]`

## Event

`[用 1-3 句话说明发生了什么。只写事实，不写责备。]`

## Impact

- 业务影响：`[例如延期、返工、用户体验偏差、发布暂停；使用脱敏描述]`
- 质量影响：`[例如 Gate 失败、缺陷逃逸、返工次数增加]`
- 成本影响：`[例如人审负载增加、交付周期变长、AI 重试次数增加]`
- 知识影响：`[例如缺少标准、上下文复用失败、Prompt 不可复用]`

## Root Cause

| 根因类别 | 说明 | 证据 |
|---|---|---|
| ANDS-T | `[Goal / Input / Constraint / Acceptance 哪一项不清楚]` | `[引用脱敏记录]` |
| Gate | `[哪个 Gate 未发现或未阻断问题]` | `[引用脱敏记录]` |
| Agent / Workflow | `[分工、交接或执行边界问题]` | `[引用脱敏记录]` |
| Knowledge | `[缺少知识域、标准、模板或历史经验]` | `[引用脱敏记录]` |

## Detection Gate

- First Detected At: `[Gate 1 | Gate 2 | Gate 3 | Gate 4 | Gate 5 | 发布后]`
- Expected Detection Gate: `[Gate 1 | Gate 2 | Gate 3 | Gate 4 | Gate 5]`
- Gap: `[说明为什么没有在期望 Gate 发现]`

## Prevention

- 任务标准改进：`[如何改写 ANDS-T、Acceptance 或 Constraint]`
- Gate 改进：`[新增或调整哪个检查项，区分 Gate 2 机器检查与 Gate 3 人验收]`
- Agent 改进：`[调整角色、上下文、权限或交接物]`
- 度量改进：`[新增或观察效率、质量、成本、知识资产、人的状态中的哪类指标]`

## Knowledge Domain

选择一个或多个：

- [ ] Product
- [ ] Technical
- [ ] Prompt
- [ ] Decision
- [ ] Workflow
- [ ] Governance
- [ ] Metrics
- [ ] Lessons

回写位置：`[[填写 Obsidian 目标笔记或知识域索引]]`

## Standard Update

- 是否需要更新标准：`[是/否]`
- 更新对象：`[ANDS-T / Gate Checklist / Track Decision / Agent Matrix / ADR / 其他]`
- 建议更新内容：`[写成可执行修改建议]`
- 负责人角色：`[填写角色，不写真实姓名]`

## Follow-up Issue

- Issue Title: `[填写改进项标题]`
- Issue Type: `[标准更新 / 模板修订 / 自动化检查 / 培训提醒 / 其他]`
- Priority: `[低 / 中 / 高]`
- Acceptance: `[只写业务或治理上可验证的改进结果]`

## Obsidian Writeback & Backlinks

- 上游链接：`[[填写任务、ADR、Gate 记录或发布记录]]`
- 下游链接：`[[填写标准更新、模板修订或后续 Issue]]`
- 相关链接：`[[填写关联 Lessons 或知识域]]`
- 双链检查：
  - [ ] 本 Lesson 已链接到上游任务或交付记录。
  - [ ] 上游任务或交付记录已反向链接到本 Lesson。
  - [ ] 标准更新或后续 Issue 已链接到本 Lesson。
  - [ ] 本 Lesson 不含真实敏感信息。
