# 从这里开始：ANDS Nexus v0.4.6

下载 → 安装 → 启用 → 4 步练习 → 反馈。先用一个虚构任务，约 10 分钟体验如何写清任务、检查证据和留下复盘草稿。

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

先退出正在使用的 Codex / Claude Code 会话。选择一个 runtime 安装；以下命令默认 Codex，要安装到 Claude Code，把 `runtime` 的值改成 `claude`。

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

Writeback boundary: user-invoked draft generation to an explicit path is allowed only when explicitly requested. 本包只帮助练习流程和准备草稿，不连接真实系统；明确指定一个本地草稿路径，不等于授权扫描 Vault、自动持久化、GitHub sync、provider workspace 写入或企业系统更新。
