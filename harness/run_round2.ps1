<#
.SYNOPSIS
  Run one AGENTS.md variant against one round-2 track and score it.
.EXAMPLE
  powershell -File harness\run_round2.ps1 -Track A -Variant none
#>
param(
    [Parameter(Mandatory = $true)][ValidateSet('A', 'B', 'C', 'D')][string]$Track,
    [Parameter(Mandatory = $true)][string]$Variant,
    [string]$Model = "opencode-go/ox-alpha-free",
    [int]$BudgetMin = 25
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot  # repo root (harness/..)
$ws   = Join-Path $repo "round2\workspaces\$Track-$Variant"
$res  = Join-Path $repo "round2\results\$Track-$Variant"
$src  = Join-Path $repo "round2\pristine\track$Track"

if (-not (Test-Path (Join-Path $repo "round2\manifest.json"))) {
    throw "manifest missing - run harness\make_manifest2.py first"
}

# ---- fresh workspace ---------------------------------------------------------
if (Test-Path $ws) { Remove-Item -Recurse -Force $ws }
New-Item -ItemType Directory -Force -Path $ws | Out-Null
Copy-Item -Recurse $src (Join-Path $ws "work")
if (-not (Test-Path (Join-Path $ws "work"))) { throw "workspace copy failed" }

# make the workspace its own git repo so the child's project root is local
$gitAll = "git -C ""$ws\work"" init -q >NUL 2>NUL& git -C ""$ws\work"" add -A >>NUL 2>NUL& git -C ""$ws\work"" -c user.name=harness -c user.email=harness@local commit -q -m baseline >>NUL 2>NUL"
& "$env:ComSpec" /d /c $gitAll

# ---- isolated global config (kept under results/, outside agent view) --------
New-Item -ItemType Directory -Force -Path $res | Out-Null
$cfg = Join-Path $res ".isolated-config"
New-Item -ItemType Directory -Force -Path (Join-Path $cfg "opencode") | Out-Null
$variantFile = Join-Path $repo "variants\$Variant.md"
if ($Variant -ne "none") {
    if (-not (Test-Path $variantFile)) { throw "variant file not found: $variantFile" }
    Copy-Item $variantFile (Join-Path $cfg "opencode\AGENTS.md")
}
# headless runs cannot answer permission prompts -> allow everything
@'
{
  "permission": {
    "edit": "allow",
    "bash": "allow",
    "webfetch": "allow",
    "external_directory": "allow"
  }
}
'@ | Set-Content -Encoding utf8 (Join-Path $cfg "opencode\opencode.jsonc")
if (-not (Test-Path (Join-Path $cfg "opencode\opencode.jsonc"))) {
    throw "isolated config write failed"
}

$promptA = @'
You are working in the work/ directory of this repository. Under work/tasks/<id>/ you will find SPEC.md contracts plus Python stub modules. Implement every spec completely and exactly: grading uses hidden, exhaustive test suites that you cannot see, written directly from these specs. Use only the Python standard library. Keep every public signature unchanged. Write your own quick sanity checks in scratch files if useful (they will not be graded), but your priority is precise conformance to every documented behavior and edge case. Before finishing, re-read each SPEC.md line by line and verify your implementation against every stated rule.
'@

$promptB = @'
You are working in the work/ directory of this repository, which contains legacy applications under work/apps/<app>/. Each app has characterization tests (test_behavior_*.py) that lock in CURRENT observable behavior, plus a REFACTORS.md listing required refactorings. Your job: complete EVERY directive in each REFACTORS.md while keeping ALL characterization tests passing, unmodified. Never edit test files (they are hash-checked afterwards). Do not change any observable behavior: same outputs, same error messages, same public call signatures unless a directive explicitly says otherwise. Do not add features. After each refactoring step, run the app's tests (python -m pytest apps/<app> -q from the work/ directory). At the end run every app suite and report results.
'@

$promptC = @'
You are working in the work/ directory of this repository. It contains db_generator.py which deterministically builds ecommerce.db, and answers.py with stub functions q01(conn) ... q15(conn). Each stub docstring states precisely one analytics question. Implement every function using SQL executed against the sqlite3 connection (you may build query strings freely; fetchall() must be returned). Read each question with extreme care: ordering requirements, tie-breaking rules, NULL semantics, and boundary dates are all graded EXACTLY against hidden expected results. Run python db_generator.py once to create the database. Test your queries by printing their outputs and sanity-checking counts. Grading is exact row matching.
'@

$promptD = @'
You are working in the work/ directory of this repository. It contains mockserver.py, a fully working local HTTP server for a fictional Items & Orders API, API_SPEC.md describing the service contract including its failure modes, and client.py with stub methods you must implement. Hidden scenario tests will boot mockserver.py in-process on a random port (with injected 500s, 429 rate-limit responses with Retry-After headers, and stale auth tokens requiring refresh) and exercise YOUR client against it. Implement list_all(), create_order(), and anything else the spec requires: full pagination via cursor, retries honoring Retry-After and exponential backoff for 5xx, silent single token refresh on 401, and clean exceptions when retry budgets are exhausted. Standard library only. Study mockserver.py source to understand exact server behaviors, then verify your client end-to-end by actually running the server locally before finishing.
'@

switch ($Track) {
    'A' { $prompt = $promptA }
    'B' { $prompt = $promptB }
    'C' { $prompt = $promptC }
    'D' { $prompt = $promptD }
}

$env:XDG_CONFIG_HOME = $cfg
$cmd = Get-Command opencode.cmd -ErrorAction SilentlyContinue
if (-not $cmd) {
    $cmd = Get-Command opencode -CommandType Application -ErrorAction SilentlyContinue |
        Where-Object { $_.Source -match '\.(exe|cmd|bat)$' } | Select-Object -First 1
}
if (-not $cmd) { throw "opencode executable not found on PATH" }
$opencodeExe = $cmd.Source

$sw = [System.Diagnostics.Stopwatch]::StartNew()
Write-Host "[${Track}/${Variant}] starting opencode ($Model), budget ${BudgetMin}min..."
$inner = "/d /s /c `"`"$opencodeExe`" run -m $Model `"$prompt`"`""
$proc = Start-Process -FilePath "$env:ComSpec" `
    -ArgumentList $inner `
    -WorkingDirectory $ws -NoNewWindow -PassThru `
    -RedirectStandardOutput (Join-Path $res "transcript.txt") `
    -RedirectStandardError (Join-Path $res "stderr.txt")
$timedOut = -not $proc.WaitForExit($BudgetMin * 60 * 1000)
if ($timedOut) {
    Write-Host "[${Track}/${Variant}] TIMEOUT - killing process tree"
    & taskkill /PID $proc.Id /T /F 2>$null | Out-Null
}
$sw.Stop()
Remove-Item Env:\XDG_CONFIG_HOME
$txBytes = 0
$txPath = Join-Path $res "transcript.txt"
if (Test-Path $txPath) { $txBytes = (Get-Item $txPath).Length }
if ($txBytes -eq 0) { Write-Host "[${Track}/${Variant}] WARNING: empty transcript" }

# ---- score ---------------------------------------------------------------------
python (Join-Path $PSScriptRoot "score2.py") $Track $ws (Join-Path $res "score.json")
if ($LASTEXITCODE -ne 0) { throw "scoring failed" }

$gitSha = ""
try { $gitSha = (git -C $repo rev-parse HEAD).Trim() } catch {}

@{
    track     = $Track
    variant   = $Variant
    model     = $Model
    budget_min = $BudgetMin
    seconds   = [math]::Round($sw.Elapsed.TotalSeconds, 1)
    timed_out = $timedOut
    exit_code = $proc.ExitCode
    transcript_bytes = $txBytes
    repo_sha  = $gitSha
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $res "meta.json")

Write-Host "[${Track}/${Variant}] done in $([math]::Round($sw.Elapsed.TotalMinutes,1)) min"
