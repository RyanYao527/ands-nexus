param(
    [string]$SkillRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path,
    [string]$QuickValidatePath = "",
    [switch]$SkipWritebackTest
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][scriptblock]$Block
    )

    & $Block
    Write-Host "PASS $Name"
}

function Get-FileCount {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Missing directory: $Path"
    }

    return @(Get-ChildItem -LiteralPath $Path -File -Filter "*.md").Count
}

function Assert-Count {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Expected
    )

    $actual = Get-FileCount -Path $Path
    if ($actual -ne $Expected) {
        throw "$Name count mismatch: expected $Expected, got $actual. If this was an intentional asset change, update validate_release.ps1 and PUBLISHING_CHECKLIST.md together."
    }
}

function Assert-RequiredFiles {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string[]]$RequiredFiles
    )

    foreach ($requiredFile in $RequiredFiles) {
        $requiredPath = Join-Path $Path $requiredFile
        if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
            throw "Missing required $Name file: $requiredFile"
        }
    }
}

function Get-ReleaseManifest {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing release manifest: $Path"
    }

    $json = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
    try {
        return $json | ConvertFrom-Json
    }
    catch {
        throw "Invalid release manifest JSON: $Path`n$($_.Exception.Message)"
    }
}

function Assert-ReleaseManifest {
    param(
        [Parameter(Mandatory = $true)][string]$ManifestPath,
        [Parameter(Mandatory = $true)][string]$RepoRoot
    )

    $manifest = Get-ReleaseManifest -Path $ManifestPath
    if (-not $manifest.schema_version) {
        throw "release-manifest.json missing schema_version"
    }
    if (-not $manifest.asset_groups) {
        throw "release-manifest.json missing asset_groups"
    }

    foreach ($group in @($manifest.asset_groups)) {
        $groupName = [string]$group.name
        $basePath = [string]$group.base_path
        $fileType = [string]$group.file_type
        $expectedCount = [int]$group.expected_count
        $requiredFiles = @($group.required_files)

        if (-not $groupName) {
            throw "release-manifest.json contains an asset group without name"
        }
        if (-not $basePath) {
            throw "release-manifest.json group '$groupName' missing base_path"
        }
        if (-not $fileType) {
            throw "release-manifest.json group '$groupName' missing file_type"
        }
        if ($expectedCount -lt 0) {
            throw "release-manifest.json group '$groupName' has invalid expected_count"
        }

        $resolvedBasePath = Join-Path $RepoRoot $basePath
        if (-not (Test-Path -LiteralPath $resolvedBasePath -PathType Container)) {
            throw "release-manifest.json group '$groupName' missing directory: $basePath"
        }

        $filter = "*.$fileType"
        $actualCount = @(Get-ChildItem -LiteralPath $resolvedBasePath -File -Filter $filter).Count
        if ($actualCount -ne $expectedCount) {
            throw "release-manifest.json group '$groupName' count mismatch: expected $expectedCount, got $actualCount"
        }

        foreach ($requiredFile in $requiredFiles) {
            $requiredPath = Join-Path $resolvedBasePath $requiredFile
            if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
                throw "release-manifest.json group '$groupName' missing required file: $requiredFile"
            }
        }
    }
}

function Assert-TextContains {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Expected
    )

    if (-not $Text.Contains($Expected)) {
        throw "Expected text to contain: $Expected"
    }
}

function Assert-FileContains {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Expected
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing file for content check: $Path"
    }

    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
    Assert-TextContains -Text $text -Expected $Expected
}

function Assert-FileNotContains {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Unexpected
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing file for content check: $Path"
    }

    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
    if ($text.Contains($Unexpected)) {
        throw "Expected file not to contain '$Unexpected': $Path"
    }
}

function Invoke-Rg {
    param(
        [Parameter(Mandatory = $true)][string]$Pattern,
        [Parameter(Mandatory = $true)][string[]]$Targets
    )

    $rg = Get-Command rg -ErrorAction SilentlyContinue
    if (-not $rg) {
        throw "rg is required for release scans. Install ripgrep and ensure rg is on PATH. Examples: macOS `brew install ripgrep`; Windows `winget install BurntSushi.ripgrep.MSVC`; Linux `apt install ripgrep`."
    }

    $output = & rg -n $Pattern @Targets 2>$null
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 1) {
        return @()
    }
    if ($exitCode -ne 0) {
        throw "rg failed for pattern: $Pattern"
    }
    return @($output)
}

function Invoke-NativeChecked {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & $Command @Arguments 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }

    if ($exitCode -ne 0) {
        $message = "$Name failed with exit code $exitCode"
        if ($output) {
            $message = "$message`n$($output -join "`n")"
        }
        throw $message
    }
    if ($output) {
        $output | Out-Host
    }
}

function Remove-AllowedPublicScanMatches {
    param([Parameter(Mandatory = $true)][string[]]$Matches)

    $filtered = @()
    foreach ($match in $Matches) {
        # Remove only the two verified installation references, then scan the
        # remaining line. A public reference must not hide another private URL.
        $remaining = $match
        $installationReferences = @(
            ('https' + '://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills'),
            ('https' + '://code.claude.com/docs/en/skills')
        )
        foreach ($reference in $installationReferences) {
            $remaining = [regex]::Replace($remaining, [regex]::Escape($reference) + '(?=[\s)\]>]|$)', '')
        }
        if ($remaining -ne $match) {
            if ($remaining -match '([A-Za-z]:\\Users\\|/Users/|/home/|http[s]?://|\b\d{1,3}(\.\d{1,3}){3}\b|Projects[\\/]ands-nexus|04-Implementation[\\/]repo)') {
                $filtered += $match
            }
            continue
        }
        if ($match.Contains("github.com/RyanYao527/ands-nexus")) {
            continue
        }
        if ($match.Contains("rg -n ")) {
            continue
        }
        if ($match.Contains("http[s]?://")) {
            continue
        }
        if ($match.Contains("[A-Za-z]:\\Users\\")) {
            continue
        }
        if ($match.Contains("/Users/|/home/")) {
            continue
        }
        $filtered += $match
    }

    return $filtered
}

function Get-RgMatchPath {
    param([Parameter(Mandatory = $true)][string]$Line)

    $parts = $Line -split ":", 2
    return $parts[0]
}

function Remove-AllowedIntegrationClaimMatches {
    param([Parameter(Mandatory = $true)][string[]]$ScanMatches)

    $filtered = @()
    foreach ($scanMatch in $ScanMatches) {
        $matchPath = Get-RgMatchPath -Line $scanMatch
        $normalizedMatchPath = $matchPath.Replace("\", "/")
        if ($normalizedMatchPath -like "ands-nexus/scripts/*") {
            continue
        }

        if (Test-AllowedIntegrationClaimLine -Line $scanMatch) {
            continue
        }
        $filtered += $scanMatch
    }

    return $filtered
}

function Test-AllowedIntegrationClaimLine {
    param([Parameter(Mandatory = $true)][string]$Line)

    $lower = $Line.ToLowerInvariant()

    if ($lower.Contains("best model") -or $lower.Contains("guaranteed provider capability")) {
        return $false
    }

    $positiveClaimPhrases = @(
        " are available",
        " is available",
        " with no extra work",
        " includes ",
        " provides ",
        " supports ",
        " readiness",
        " validated",
        " validation for"
    )

    if (
        $lower.Contains("enterprise trigger:") -or
        $lower.Contains("enterprise triggers") -or
        $lower.Contains("not fit without enterprise review")
    ) {
        foreach ($positiveClaimPhrase in $positiveClaimPhrases) {
            if ($lower.Contains($positiveClaimPhrase)) {
                return $false
            }
        }
        return $true
    }

    $requirements = @(
        @{
            Patterns = @("provider-native validation")
            Allowed = @("not provider-native validation", "not provider-native capability validation", "no provider-native validation")
        },
        @{
            Patterns = @("native provider validation")
            Allowed = @("not native provider validation", "no native provider validation")
        },
        @{
            Patterns = @("api integration")
            Allowed = @("no live provider api integration", "not an api integration guide", "not api integration", "no api integration")
        },
        @{
            Patterns = @("live provider api integration")
            Allowed = @("no live provider api integration")
        },
        @{
            Patterns = @("credential setup")
            Allowed = @("no credential setup", "no credential or tenant setup")
        },
        @{
            Patterns = @("credential or tenant setup")
            Allowed = @("no credential or tenant setup")
        },
        @{
            Patterns = @("tenant setup")
            Allowed = @("no tenant setup", "no credential or tenant setup")
        },
        @{
            Patterns = @("tenant connectors")
            Allowed = @("no tenant connectors")
        },
        @{
            Patterns = @("tenant connector readiness")
            Allowed = @("no tenant connector readiness", "not tenant connector readiness", "no tenant connectors")
        },
        @{
            Patterns = @("automated writeback")
            Allowed = @("no automated writeback", "no unattended or automated writeback", "no unattended/automatic writeback")
        },
        @{
            Patterns = @("api key setup")
            Allowed = @("no api key setup")
        },
        @{
            Patterns = @("oauth setup")
            Allowed = @("no oauth setup")
        },
        @{
            Patterns = @("benchmark ranking")
            Allowed = @("no benchmark ranking", "no public benchmark ranking", "not benchmark rankings")
        }
    )

    foreach ($requirement in $requirements) {
        $hasPattern = $false
        foreach ($pattern in $requirement.Patterns) {
            if ($lower.Contains($pattern)) {
                $hasPattern = $true
                break
            }
        }

        if (-not $hasPattern) {
            continue
        }

        $hasAllowedPhrase = $false
        foreach ($allowed in $requirement.Allowed) {
            if ($lower.Contains($allowed)) {
                $hasAllowedPhrase = $true
                break
            }
        }

        if (-not $hasAllowedPhrase) {
            return $false
        }
    }

    return $true
}

$templatesValidator = Join-Path $PSScriptRoot "validate_templates.ps1"
$writebackTest = Join-Path $PSScriptRoot "test_writeback_mvp.ps1"

Invoke-Step -Name "validate_templates" -Block {
    & $templatesValidator -SkillRoot $SkillRoot | Out-Host
}

if (-not $SkipWritebackTest) {
    Invoke-Step -Name "test_writeback_mvp" -Block {
        & $writebackTest | Out-Host
    }
}

if ($QuickValidatePath) {
    Invoke-Step -Name "quick_validate" -Block {
        if (-not (Test-Path -LiteralPath $QuickValidatePath -PathType Leaf)) {
            throw "Missing quick_validate.py: $QuickValidatePath"
        }
        Invoke-NativeChecked -Name "quick_validate.py" -Command "python" -Arguments @($QuickValidatePath, $SkillRoot)
    }
}
else {
    Write-Host "SKIP quick_validate (no -QuickValidatePath; external Codex skill-creator tool not in repo)"
}

Invoke-Step -Name "release_manifest" -Block {
    $manifestPath = Join-Path $RepoRoot "release-manifest.json"
    Assert-ReleaseManifest -ManifestPath $manifestPath -RepoRoot $RepoRoot
}

Invoke-Step -Name "guided_workflow_assets" -Block {
    $readme = Join-Path $RepoRoot "README.md"
    $startHere = Join-Path $RepoRoot "START-HERE.md"
    $examplesIndex = Join-Path $RepoRoot "examples/INDEX.md"
    $skillDefinition = Join-Path $SkillRoot "SKILL.md"
    $gateChecklist = Join-Path $SkillRoot "assets/templates/gate-checklist.md"
    $trackDecisionCard = Join-Path $SkillRoot "assets/templates/track-decision-card.md"
    $guidedReference = Join-Path $SkillRoot "references/guided-workflow-mvp.md"
    $glossaryReference = Join-Path $SkillRoot "references/glossary.md"
    $guidedStatePacket = Join-Path $SkillRoot "assets/templates/guided-workflow-state-packet.md"
    $guidedFirstRun = Join-Path $RepoRoot "examples/guided-workflow-first-run-v0.4.md"
    $guidedRegression = Join-Path $RepoRoot "examples/guided-workflow-regression-v0.4.md"

    Assert-FileContains -Path $readme -Expected "If you are not using Codex"
    Assert-FileContains -Path $readme -Expected "macOS/Linux"
    Assert-FileContains -Path $readme -Expected "brew install powershell ripgrep"
    Assert-FileContains -Path $readme -Expected "quick_validate.py is external"
    Assert-FileContains -Path $startHere -Expected "If you are not using Codex"
    Assert-FileContains -Path $startHere -Expected "Core Terms"
    Assert-FileContains -Path $startHere -Expected "If a guided answer misses one of the six sections"
    Assert-FileContains -Path $startHere -Expected "use a fictional task because this package rehearses the process; it does not connect to your systems"
    Assert-FileContains -Path $examplesIndex -Expected 'Installable routed examples are also copied under `ands-nexus/examples/`'
    Assert-FileContains -Path $skillDefinition -Expected "references/glossary.md"
    Assert-FileContains -Path $skillDefinition -Expected "assets/templates/ands-t-template.md"
    Assert-FileContains -Path $skillDefinition -Expected "assets/templates/gate-checklist.md"
    Assert-FileContains -Path $skillDefinition -Expected "assets/templates/lessons-template.md"
    Assert-FileContains -Path $skillDefinition -Expected "examples/management-rollout-plan.md"
    Assert-FileContains -Path $guidedReference -Expected "Intake Snapshot"
    Assert-FileContains -Path $guidedReference -Expected "ANDS-T Task Card"
    Assert-FileContains -Path $guidedReference -Expected "Track + Gate Checklist"
    Assert-FileContains -Path $guidedReference -Expected "Lessons Draft"
    Assert-FileContains -Path $guidedReference -Expected "Role Boundaries"
    Assert-FileContains -Path $guidedReference -Expected "Guided Lite To Formal Template Mapping"
    Assert-FileContains -Path $guidedReference -Expected "Next Prompt embedded state"
    Assert-FileContains -Path $guidedReference -Expected "no unattended or automated writeback"
    Assert-FileContains -Path $guidedReference -Expected "user-invoked draft generation to an explicit path is allowed only when explicitly requested"
    Assert-FileContains -Path $guidedReference -Expected 'such as `confirm: ...`, `revise: ...`, `escalate: ...`, `stop: ...`, or `unfilled`'
    Assert-FileContains -Path $guidedReference -Expected "Owner response values in examples are format demonstrations only"
    Assert-FileContains -Path $glossaryReference -Expected "State Packet"
    Assert-FileContains -Path $glossaryReference -Expected "Gate"
    Assert-FileContains -Path $glossaryReference -Expected "owner_response"

    $guidedStateFields = @(
        "workflow_id",
        "current_step",
        "user_goal",
        "audience",
        "data_class",
        "track",
        "active_role",
        "artifacts_created",
        "missing_evidence",
        "owner_decision",
        "owner_response",
        "next_prompt",
        "boundary_flags"
    )
    foreach ($field in $guidedStateFields) {
        Assert-FileContains -Path $guidedStatePacket -Expected $field
    }

    Assert-FileContains -Path $guidedFirstRun -Expected "Current Artifact"
    Assert-FileContains -Path $guidedFirstRun -Expected "State Packet"
    Assert-FileContains -Path $guidedFirstRun -Expected "Gate / Evidence Check"
    Assert-FileContains -Path $guidedFirstRun -Expected "Owner Decision"
    Assert-FileContains -Path $guidedFirstRun -Expected "Next Prompt"
    Assert-FileContains -Path $guidedFirstRun -Expected "Boundary Reminder"
    Assert-FileContains -Path $guidedFirstRun -Expected "- owner_decision: Confirm Standard Track and provide missing evidence"
    Assert-FileContains -Path $guidedFirstRun -Expected 'Replace `owner_response` with the human owner''s actual reply before sending each Step Prompt.'
    Assert-FileContains -Path $guidedFirstRun -Expected "- owner_response: [confirm/revise/escalate/stop before continuing]"
    Assert-FileContains -Path $guidedFirstRun -Expected "- owner_response: <owner reply: confirm/revise/escalate/stop: ...>"
    Assert-FileNotContains -Path $guidedFirstRun -Unexpected "- owner_response: confirm:"
    Assert-FileContains -Path $guidedFirstRun -Expected "- boundary_flags: Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking"
    Assert-FileContains -Path $guidedFirstRun -Expected "- active_role: Validation + Governance"
    Assert-FileContains -Path $guidedFirstRun -Expected '| `active_role` | Validation + Governance |'
    Assert-FileContains -Path $guidedFirstRun -Expected "Gate 2 test evidence; Gate 3 owner acceptance; human review before reuse"
    Assert-FileContains -Path $guidedFirstRun -Expected "do not authorize broader writeback from this prompt"
    Assert-FileContains -Path $guidedFirstRun -Expected "confirmation that no broader writeback is authorized by this prompt"
    Assert-FileContains -Path $guidedFirstRun -Expected "Status legend"

    Assert-FileContains -Path $guidedRegression -Expected "role drift"
    Assert-FileContains -Path $guidedRegression -Expected "skipped Gate evidence"
    Assert-FileContains -Path $guidedRegression -Expected "missing owner decision"
    Assert-FileContains -Path $guidedRegression -Expected "writeback overreach"
    Assert-FileContains -Path $guidedRegression -Expected "Enterprise escalation"
    Assert-FileContains -Path $gateChecklist -Expected 'Owner: `[人类 Project Owner'
    Assert-FileContains -Path $gateChecklist -Expected "AI PM 仅准备材料与质检，不作准入决策"
    Assert-FileContains -Path $trackDecisionCard -Expected "External delivery or contractual impact"
}

Invoke-Step -Name "public_package_scan" -Block {
    Push-Location $RepoRoot
    try {
        $targets = @("README.md", "START-HERE.md", "RELEASE_NOTES.md", "PUBLISHING_CHECKLIST.md", "release-manifest.json", "examples", "ands-nexus")
        $secretMatches = Invoke-Rg -Pattern 'BEGIN (RSA|OPENSSH|PRIVATE)|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|gh[opsu]_[A-Za-z0-9_]{20,}' -Targets @(".")
        if ($secretMatches.Count -gt 0) {
            throw "Potential secret-like matches found:`n$($secretMatches -join "`n")"
        }

        $pathMatches = Invoke-Rg -Pattern '([A-Za-z]:\\Users\\|/Users/|/home/|http[s]?://|\b\d{1,3}(\.\d{1,3}){3}\b|Projects[\\/]ands-nexus|04-Implementation[\\/]repo)' -Targets $targets
        $pathMatches = Remove-AllowedPublicScanMatches -Matches $pathMatches
        if ($pathMatches.Count -gt 0) {
            throw "Potential local path, URL, or IP matches found:`n$($pathMatches -join "`n")"
        }

        $claimMatches = Invoke-Rg -Pattern '(?i)provider-native validation|native provider validation|API integration|live provider API integration|credential setup|credential or tenant setup|tenant setup|tenant connectors|tenant connector readiness|automated writeback|API key setup|OAuth setup|benchmark ranking|best model|guaranteed provider capability' -Targets $targets
        $claimMatches = Remove-AllowedIntegrationClaimMatches -ScanMatches $claimMatches
        if ($claimMatches.Count -gt 0) {
            throw "Potential unsupported integration or benchmark claims found:`n$($claimMatches -join "`n")"
        }
    }
    finally {
        Pop-Location
    }
}

Write-Host "PASS validate_release"
