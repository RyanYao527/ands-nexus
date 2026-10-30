# 发布后反馈模板

适用于 v0.4.6 及历史版本；保留原文件名以兼容已有链接。提交到 [GitHub Issues](https://github.com/RyanYao527/ands-nexus/issues/new)。不要粘贴密钥、私人仓库路径、真实客户记录、内部域名或未脱敏的会话。

## 学员最小反馈

```text
版本：v0.4.6 / v0.4.5 / v0.4.4 / v0.4.3 / v0.4.2 / v0.4.1 / v0.4.0 / v0.3.1 / v0.3.0 / 更早版本 / main / unknown
Runtime：Codex / Claude Code / KIMI / GLM / MiniMax / DeepSeek / WorkBuddy / 其他（附工具版本）
操作步骤：从下载、安装、启用或四步练习中的哪一步开始？
预期结果：
实际结果：
脱敏复现：最小虚构输入 + 必要的脱敏输出
```

不知道的字段写 `unknown`，不要为了填表补造信息。以下为维护者分诊字段，学员可以不填。

## 反馈记录

| 字段 | 内容 |
|---|---|
| Feedback ID | `FB-v0.4.6-001`（按实际版本编号） |
| 日期 | `[YYYY-MM-DD]` |
| 反馈者角色 | `[管理者 / PM / 工程师 / 治理审核 / 运营 / 其他]` |
| Data class | `[synthetic / desensitized / unknown]` |
| 任务类型 | `[安装 / 启用 / 试点 / ANDS-T / Gate / 角色路由 / 验证 / 回写 / runtime 适配]` |
| Track | `[Quick / Standard / Enterprise / unclear]` |
| 迷惑表述或缺失资料 | `[脱敏短引文、文件名或 none]` |
| 严重程度 | `[Low / Medium / High]` |

## 边界检查

| 问题 | 回答 |
|---|---|
| 是否请求真实数据？ | `[yes / no / unclear]` |
| 是否请求密钥或凭据？ | `[yes / no / unclear]` |
| 是否请求 live provider 工作？ | `[yes / no / unclear]` |
| 是否请求租户或连接器工作？ | `[yes / no / unclear]` |
| 是否请求自动持久化？ | `[yes / no / unclear]` |
| 是否请求公开 provider 对比或排名？ | `[yes / no / unclear]` |

If any answer is `yes` or `unclear`, route to Enterprise review before changing public guidance.

## 分诊与后续

| 字段 | 内容 |
|---|---|
| 问题分类 | `[安装/启用 / 首跑入口 / Track / 角色路由 / Gate 证据 / 回写边界 / 适配越界 / 文档 / validator]` |
| 脱敏结果 | `[PASS / NEEDS_REDACTION / BLOCKED]`（不等同于 Data class） |
| 建议修复 | `[文档 / 示例 / 模板 / validator / 不修改]` |
| 建议文件 | `[相对文件名或 none；不公开私人绝对路径]` |
| 回归输入 | `[可复现问题的 synthetic prompt]` |
| 验收方法 | `[如何验证修复]` |
| 知识回写候选 | `[项目内 Lessons / 方法规则候选 / 无]` |
| Owner 决定 | `[accept / reject / hold / needs more evidence]` |
| 理由与下一任务 | `[一句理由 + 有限范围任务或 none]` |

只有脱敏结果为 `PASS`、并经人工审核的材料才进入公开 examples 或 validation；`NEEDS_REDACTION` 先改写复核，`BLOCKED` 不进入公开材料。
