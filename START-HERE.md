# 从这里开始：ANDS Nexus

## Agent 内测入口

**0.5.0-alpha.2 采用 Owner 已批准的 Codex 主持 Loop。** 当前 Codex 会话生成计划、文档和 Lessons，并为审阅请求调用新的独立审阅者；本地程序通过 `next` / `respond` 管理状态及结果。无需新增模型服务，也不启动独立 CLI 探针。旧 `native` 路线的五轮隔离失败保留，不能被称为通过。

开始前查看 [Agent 验证记录](AGENT_VALIDATION.md)，其中分别记录本轮 Hosted Loop、历史隔离失败和尚未完成的实际验收。新路线获准实施不代表真实交付链或 GitHub 操作已经通过。

本分支包含 `0.5.0-alpha.2` Agent 原型，目标环境为 Windows / 当前 Codex。它尚无正式 Release 附件；下面的 v0.4.6 下载段落是稳定版纯提示词流程，不会安装 Agent 程序。

内测从此分支的源码目录安装：先退出旧会话，把旧 `ands-nexus/` 整体移到技能扫描目录之外备份，再将本分支的 `ands-nexus/` 内容复制到新空的 `~/.agents/skills/ands-nexus/`，确认该目录直接包含 `SKILL.md`、`VERSION` 和 `scripts/nexus.py`。不要运行下面要求 `VERSION=0.4.6` 的稳定版安装块来安装 alpha。回退时先移走 alpha，再将备份恢复到不存在的目标目录。

Hosted 模式需要可使用独立审阅者的当前 Codex、Python 3.11；GitHub 操作另需 `gh` 和已有登录。无需安装额外 Python 包。[Agent 使用说明](ands-nexus/references/agent-workflow.md)提供完整 `init → next → respond → 人批准 → next` 操作。运行目录及已批准 GitHub 仓库是操作范围，完整 Vault 和其他仓库不在范围内。

批准、验收、退回或追加预算的命令由人本人在独立终端输入，外层 Codex 不得代执行。终端交互检查不构成人的身份认证，不能把可创建 PTY 误认为可代人批准。

Owner 已指定私有合成联调仓库 `RyanYao527/ands-nexus-sandbox` 及负责人 `RyanYao527`。创建真实 Issues 仍须先展示当前任务计划和动作范围，由 Owner 运行批准命令；尚未收到的批准保持等待。安装本包、启用 skill 或在聊天中展示示例不授予写入权限。

## v0.4.6 稳定版入口

下载 → 安装 → 启用 → 4 步练习 → 反馈。先用一个小型虚构任务，体验如何写清任务、检查证据和留下复盘草稿。

**本版首跑使用 Codex。** Claude Code 安装说明继续保留，但本次 Claude Code 2.1.304 + DeepSeek 配置未通过：新确认可能被旧交接文字覆盖，所请求的 Lessons 未生成。其他 Claude 配置未实测；安装成功不代表四步行为通过。详见[验证摘要](VALIDATION.md)。

## 1. 下载指定版本

打开 [v0.4.6 Release](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.6)，下载 [ands-nexus-v0.4.6.zip](https://github.com/RyanYao527/ands-nexus/releases/download/v0.4.6/ands-nexus-v0.4.6.zip) 和 [SHA256SUMS.txt](https://github.com/RyanYao527/ands-nexus/releases/download/v0.4.6/SHA256SUMS.txt)。校验后解压，顶层应为 `ands-nexus/`，其中有 `SKILL.md` 和内容为 `0.4.6` 的 `VERSION`。安装时不要多套一层同名目录。

可手动下载、校验和解压，也可展开下面对应平台的命令。命令会创建新的下载目录；目录冲突或校验失败会停止。完成后，终端位于含 `ands-nexus/` 的目录。

<details>
<summary>Windows PowerShell：下载与 SHA-256 校验</summary>

```powershell
# download-powershell
$ErrorActionPreference = "Stop"
$release = "v0.4.6"
$asset = "ands-nexus-$release.zip"
$download = Join-Path (Get-Location) "ands-nexus-$release-download"
if (Test-Path -LiteralPath $download) { throw "下载目录已存在，请换一个空目录运行：$download" }
New-Item -ItemType Directory -Path $download | Out-Null
$base = "https://github.com/RyanYao527/ands-nexus/releases/download/$release"
Invoke-WebRequest "$base/$asset" -OutFile (Join-Path $download $asset) -UseBasicParsing
Invoke-WebRequest "$base/SHA256SUMS.txt" -OutFile (Join-Path $download "SHA256SUMS.txt") -UseBasicParsing
$pattern = '^[0-9a-fA-F]{64}\s+\*?' + [regex]::Escape($asset) + '$'
$entries = @(Get-Content -LiteralPath (Join-Path $download "SHA256SUMS.txt") | Where-Object { $_ -match $pattern })
if ($entries.Count -ne 1) { throw "找不到唯一的安装包校验记录" }
$expected = ($entries[0] -split '\s+')[0]
$actual = (Get-FileHash -LiteralPath (Join-Path $download $asset) -Algorithm SHA256).Hash
if ($actual -ne $expected) { throw "SHA-256 校验失败，停止安装" }
Expand-Archive -LiteralPath (Join-Path $download $asset) -DestinationPath $download
Set-Location -LiteralPath $download
Write-Host "校验成功；下一步运行安装代码块。"
```

</details>

<details>
<summary>macOS/Linux（Bash）：下载与 SHA-256 校验</summary>

```bash
# download-shell
set -eu
release=v0.4.6
asset="ands-nexus-$release.zip"
download="$PWD/ands-nexus-$release-download"
mkdir "$download" # 已存在则失败，不覆盖
base="https://github.com/RyanYao527/ands-nexus/releases/download/$release"
curl -fL "$base/$asset" -o "$download/$asset"
curl -fL "$base/SHA256SUMS.txt" -o "$download/SHA256SUMS.txt"
expected="$(awk -v asset="$asset" '$2 == asset { print tolower($1) }' "$download/SHA256SUMS.txt")"
if command -v sha256sum >/dev/null 2>&1; then
  actual="$(sha256sum "$download/$asset" | awk '{print $1}')"
else
  actual="$(shasum -a 256 "$download/$asset" | awk '{print $1}')"
fi
[ -n "$expected" ] && [ "$actual" = "$expected" ] || { echo 'SHA-256 校验失败，停止安装' >&2; exit 1; }
unzip -q "$download/$asset" -d "$download"
cd "$download"
printf '%s\n' '校验成功；下一步运行安装代码块。'
```

</details>

## 2. 安装

先退出正在使用的 Codex / Claude Code 会话。以下命令默认安装本版首发支持的 Codex。若仅参考保留的 Claude Code 安装路径，把 `runtime` 的值改成 `claude`；该配置的行为限制见页首。

| runtime | 安装目录 | 调用 |
|---|---|---|
| `codex` | `~/.agents/skills/ands-nexus/` | `$ands-nexus` |
| `claude` | `~/.claude/skills/ands-nexus/` | `/ands-nexus` |

依据：[Codex 官方 skill 目录](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)、[Claude Code 官方 skills 说明](https://code.claude.com/docs/en/skills)。

命令只处理所选安装目录。Codex 还会精确检查旧目录 `~/.codex/skills/ands-nexus`；若存在，会一并移出扫描目录备份，避免旧、新副本同时加载。不扫描其他用户资料。备份位于 `~/ands-nexus-backups/<timestamp>/<runtime>/ands-nexus`，旧 Codex 目录归入 `codex-legacy`；任何备份路径冲突都会失败，不覆盖备份。

<details>
<summary>Windows PowerShell：安装或升级</summary>

```powershell
# install-powershell
$ErrorActionPreference = "Stop"
if (-not (Get-Variable -Name runtime -ErrorAction SilentlyContinue)) { $runtime = "codex" } # Claude Code 可先设 $runtime = "claude"
if (-not (Get-Variable -Name installHome -ErrorAction SilentlyContinue)) { $installHome = $env:USERPROFILE }
$source = Join-Path (Get-Location) "ands-nexus"
if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md") -PathType Leaf)) { throw "当前目录下缺少 ands-nexus/SKILL.md" }
if ((Get-Content -Raw -LiteralPath (Join-Path $source "VERSION")).Trim() -ne "0.4.6") { throw "安装包版本不是 0.4.6" }
$relative = switch ($runtime) {
    "codex" { ".agents\skills\ands-nexus" }
    "claude" { ".claude\skills\ands-nexus" }
    default { throw "runtime 只能为 codex 或 claude" }
}
$installHome = [IO.Path]::GetFullPath($installHome)
$target = [IO.Path]::GetFullPath((Join-Path $installHome $relative))
$legacy = [IO.Path]::GetFullPath((Join-Path $installHome ".codex\skills\ands-nexus"))
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssfffZ")
$backupRoot = Join-Path $installHome "ands-nexus-backups\$stamp"
if (Test-Path -LiteralPath $backupRoot) { throw "备份路径冲突：$backupRoot" }
$moves = @(@{ Path = $target; Name = $runtime })
if ($runtime -eq "codex") {
    Write-Host "精确检查旧目录：$legacy"
    $moves += @{ Path = $legacy; Name = "codex-legacy" }
}
foreach ($item in $moves) {
    $path = $item.Path
    if (-not $path.StartsWith($installHome.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetFileName($path) -ne "ands-nexus") { throw "目录超出预定安装范围：$path" }
    if (Test-Path -LiteralPath $path) {
        $backup = Join-Path $backupRoot ($item.Name + "\ands-nexus")
        if (Test-Path -LiteralPath $backup) { throw "备份路径冲突：$backup" }
        New-Item -ItemType Directory -Path (Split-Path $backup) -Force | Out-Null
        Move-Item -LiteralPath $path -Destination $backup
        Write-Host "已备份：$path -> $backup"
    }
}
New-Item -ItemType Directory -Path (Split-Path $target) -Force | Out-Null
New-Item -ItemType Directory -Path $target | Out-Null # 目标必须是新空目录
Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $target -Recurse
if (-not (Test-Path -LiteralPath (Join-Path $target "SKILL.md") -PathType Leaf)) { throw "安装不完整，请按下方说明恢复备份" }
Write-Host "已安装 0.4.6：$target"
Write-Host "本次备份位置（有旧目录时才产生）：$backupRoot"
```

</details>

<details>
<summary>macOS/Linux（Bash）：安装或升级</summary>

```bash
# install-shell
set -eu
runtime="${runtime:-codex}" # Claude Code 可先设 runtime=claude
install_home="${install_home:-$HOME}"
source="$PWD/ands-nexus"
[ -f "$source/SKILL.md" ] || { echo '当前目录下缺少 ands-nexus/SKILL.md' >&2; exit 1; }
[ "$(tr -d '\r\n' < "$source/VERSION")" = '0.4.6' ] || { echo '安装包版本不是 0.4.6' >&2; exit 1; }
case "$runtime" in
  codex) target="$install_home/.agents/skills/ands-nexus" ;;
  claude) target="$install_home/.claude/skills/ands-nexus" ;;
  *) echo 'runtime 只能为 codex 或 claude' >&2; exit 1 ;;
esac
legacy="$install_home/.codex/skills/ands-nexus"
stamp="$(date -u +%Y%m%dT%H%M%SZ)-$$"
backup_root="$install_home/ands-nexus-backups/$stamp"
mkdir -p "$install_home/ands-nexus-backups"
mkdir "$backup_root" # 已存在则失败，不覆盖
if [ -e "$target" ] || [ -L "$target" ]; then
  mkdir "$backup_root/$runtime"
  mv "$target" "$backup_root/$runtime/ands-nexus"
  printf '已备份：%s -> %s\n' "$target" "$backup_root/$runtime/ands-nexus"
fi
if [ "$runtime" = codex ]; then
  printf '精确检查旧目录：%s\n' "$legacy"
  if [ -e "$legacy" ] || [ -L "$legacy" ]; then
    mkdir "$backup_root/codex-legacy"
    mv "$legacy" "$backup_root/codex-legacy/ands-nexus"
    printf '已备份：%s -> %s\n' "$legacy" "$backup_root/codex-legacy/ands-nexus"
  fi
fi
mkdir -p "$(dirname "$target")"
mkdir "$target" # 目标必须是新空目录
cp -R "$source/." "$target/"
[ -f "$target/SKILL.md" ] || { echo '安装不完整，请按下方说明恢复备份' >&2; exit 1; }
printf '已安装 0.4.6：%s\n本次备份位置：%s\n' "$target" "$backup_root"
```

</details>

**恢复旧版：** 保留终端打印的备份路径。退出 runtime，把本次新目标整体移到 skills 扫描目录之外，再把备份按打印的映射移回原位置；恢复目的目录必须不存在，不能把备份复制进仍存在的新目录。若同时备份了 `codex` 和 `codex-legacy`，只恢复你要使用的一份，避免双加载。没有备份时，从 [固定 v0.4.5 tag](https://github.com/RyanYao527/ands-nexus/releases/tag/v0.4.5) 下载源码，将其中 `ands-nexus/` 安装到新空目标目录；不要用 `main` 回退，也不要把旧包硬套进要求 `VERSION=0.4.6` 的上方命令。

## 3. 启用

重新打开工具或新建会话，确认目标路径下直接存在 `ands-nexus/SKILL.md`：

- Codex：输入 `$ands-nexus`。
- Claude Code：输入 `/ands-nexus`。
- **其他工具（If you are not using Codex）**：将 `ands-nexus/SKILL.md` 作为主指令，再按其 Task Routing 只附上当前任务所需的资料。首跑使用 `references/guided-workflow-mvp.md`、`references/glossary.md`、`assets/templates/guided-workflow-state-packet.md` 和 `examples/guided-workflow-first-run-v0.4.md`；需要完整任务卡、Gate 或 Lessons 时，再加载对应模板。`$ands-nexus` 不是所有工具通用的语法。

没有识别到 skill 时，检查安装目录、文件名与是否多了一层 `ands-nexus/ands-nexus/`，再开启新会话。

## 4. 完成一次四步练习（Guided Workflow First Run）

打开安装目录里的 [examples/guided-workflow-first-run-v0.4.md](ands-nexus/examples/guided-workflow-first-run-v0.4.md)，按顺序复制 **Step Prompt**。Claude Code 将其中的 `$ands-nexus` 改成 `/ands-nexus`；手动加载时省略这一行。不要把 Expected output 当作你的回答粘贴回去。

练习任务：给虚构的内部报表页加一个“导出上周 CSV”按钮。use a fictional task because this package rehearses the process; it does not connect to your systems.

| 步骤 | 你要得到什么 | 继续前做什么 |
|---|---|---|
| 1. Intake Snapshot | 目标、输入、缺失信息 | 补充字段、文件名和验收人 |
| 2. ANDS-T Task Card | 目标、约束、可检查的业务验收 | 确认或修订任务范围 |
| 3. Track + Gate Checklist | 风险分级、机器检查和人验收 | 检查哪些证据仍缺失 |
| 4. Lessons Draft | 可供审核的复盘草稿 | 人工确认哪些内容值得保留 |

每步应有 Current Artifact、State Packet、Gate / Evidence Check、Owner Decision、Next Prompt、Boundary Reminder 六个部分。将 `owner_response` 填成**你真实的** `confirm / revise / escalate / stop` 回复后再继续；不把示例决定当成你已批准，也不把草稿当成真实执行证据。

If a guided answer misses one of the six sections，回复：“请补齐缺少的 [名称]，重新给出当前步骤。”

**术语（Core Terms）**：ANDS-T 是任务卡，Track 是按风险选择的流程强度，Gate 是检查与决策点，Lessons 是复盘记录。更多见 [一页术语卡](ands-nexus/references/one-page-glossary-card.md)和[术语表](ands-nexus/references/glossary.md)。更短的练习（Compact First Run）见 [examples/first-run-prompt-packet-v0.3.1.md](ands-nexus/examples/first-run-prompt-packet-v0.3.1.md)。

## 5. 通过 GitHub Issues 反馈

打开 [新建 Issue](https://github.com/RyanYao527/ands-nexus/issues/new)，复制以下字段：

```text
版本：v0.4.6（或实际安装版本）
Runtime：Codex / Claude Code / 其他（附工具版本）
操作步骤：卡在哪一步？
预期结果：
实际结果：
脱敏复现：最小虚构输入 + 必要的脱敏输出
```

不要贴密钥、客户数据、内部域名、私人仓库路径或未脱敏的会话。需要细分问题时使用[反馈模板](examples/post-release-feedback-intake-v0.3.1.md)。你可以手动保存任务卡、检查表和 Lessons；可复用经验先留在项目中，审核后再进入团队方法库。

## 首跑边界

Quick 适合低风险、可回滚、无外部交付的任务；Standard 适合普通协作及低风险的外部可见材料，并在外部可见时加强 Gate 4。真实客户影响、敏感数据、生产关键路径、难回滚、公开能力声明、合同承诺或采购建议需 Enterprise 审查。

`data_class` 是输入类别；`PASS / NEEDS_REDACTION / BLOCKED` 是材料可否公开的脱敏结果。首跑选择 synthetic，不把脱敏通过误当成业务验收通过。

Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.

纯提示词模式的 Writeback boundary: user-invoked draft generation to an explicit path is allowed only when explicitly requested. 该流程帮助练习和准备草稿；明确指定一个本地草稿路径，不等于授权扫描 Vault、自动持久化、GitHub sync、provider workspace 写入或企业系统更新。Agent 内测模式另以人批准的计划限定项目文件和单个 GitHub 仓库的操作，见页首入口。
