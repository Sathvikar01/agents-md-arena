<#
.SYNOPSIS
  Run one AGENTS.md variant against the benchmark and score it.
.EXAMPLE
  powershell -File harness\run.ps1 -Variant none
#>
param(
    [Parameter(Mandatory = $true)][string]$Variant,
    [string]$Model = "opencode-go/ox-alpha-free",
    [int]$BudgetMin = 25
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$ws   = Join-Path $repo "workspaces\$Variant"
$res  = Join-Path $repo "results\$Variant"

if (-not (Test-Path (Join-Path $repo "benchmark\manifest.json"))) {
    throw "manifest missing - run harness\make_manifest.py first"
}

# ---- fresh workspace -------------------------------------------------------
if (Test-Path $ws) { Remove-Item -Recurse -Force $ws }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ws) | Out-Null
Copy-Item -Recurse (Join-Path $repo "benchmark\pristine\tasks") $ws

# ---- isolated global config -------------------------------------------------
$cfg = Join-Path $ws ".isolated-config"
New-Item -ItemType Directory -Force -Path (Join-Path $cfg "opencode") | Out-Null
$variantFile = Join-Path $repo "variants\$Variant.md"
if ($Variant -ne "none") {
    if (-not (Test-Path $variantFile)) { throw "variant file not found: $variantFile" }
    Copy-Item $variantFile (Join-Path $cfg "opencode\AGENTS.md")
}

New-Item -ItemType Directory -Force -Path $res | Out-Null

$prompt = @'
You are working in this repository. Under the tasks/ directory there are multiple Python task folders. Each folder contains implementation module(s) with bugs or missing behavior, plus a test suite that defines exactly what correct behavior looks like. Your job: fix the implementations so that ALL tests pass for ALL tasks. Hard rules: never modify, delete, or weaken any test file (every test file is hash-checked afterwards); use only the Python standard library; keep all public function and class signatures unchanged. Run each task suite as you go, for example: python -m pytest tasks/t01-slugify -q. At the end run the complete suite (python -m pytest tasks -q) from the repository root and report the final totals.
'@

$env:XDG_CONFIG_HOME = $cfg
$cmd = Get-Command opencode.cmd -ErrorAction SilentlyContinue
if (-not $cmd) {
    $cmd = Get-Command opencode -CommandType Application -ErrorAction SilentlyContinue |
        Where-Object { $_.Source -match '\.(exe|cmd|bat)$' } | Select-Object -First 1
}
if (-not $cmd) { throw "opencode executable not found on PATH" }
$opencodeExe = $cmd.Source
$sw = [System.Diagnostics.Stopwatch]::StartNew()
Write-Host "[$Variant] starting opencode ($Model), budget ${BudgetMin}min..."
$proc = Start-Process -FilePath $opencodeExe `
    -ArgumentList @("run", "-m", $Model, "`"$prompt`"") `
    -WorkingDirectory $ws -NoNewWindow -PassThru `
    -RedirectStandardOutput (Join-Path $res "transcript.txt") `
    -RedirectStandardError (Join-Path $res "stderr.txt")
$timedOut = -not $proc.WaitForExit($BudgetMin * 60 * 1000)
if ($timedOut) {
    Write-Host "[$Variant] TIMEOUT - killing process tree"
    & taskkill /PID $proc.Id /T /F 2>$null | Out-Null
}
$sw.Stop()
Remove-Item Env:\XDG_CONFIG_HOME

# ---- score -------------------------------------------------------------------
python (Join-Path $repo "harness\score.py") $ws (Join-Path $res "score.json")
if ($LASTEXITCODE -ne 0) { throw "scoring failed" }

$gitSha = ""
try { $gitSha = (git -C $repo rev-parse HEAD).Trim() } catch {}

@{
    variant   = $Variant
    model     = $Model
    budget_min = $BudgetMin
    seconds   = [math]::Round($sw.Elapsed.TotalSeconds, 1)
    timed_out = $timedOut
    exit_code = $proc.ExitCode
    repo_sha  = $gitSha
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $res "meta.json")

Write-Host "[$Variant] done in $([math]::Round($sw.Elapsed.TotalMinutes,1)) min"
