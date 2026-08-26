# Install agents-md-arena agents + commands into the user's global
# opencode config (~/.config/opencode). Re-run after editing sources.

$ErrorActionPreference = "Stop"
$src = $PSScriptRoot
$dst = Join-Path $env:USERPROFILE ".config\opencode"

New-Item -ItemType Directory -Force -Path (Join-Path $dst "agent") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $dst "command") | Out-Null

foreach ($a in Get-ChildItem (Join-Path $src "agents") -Filter *.md) {
    Copy-Item $a.FullName (Join-Path $dst "agent\$($a.Name)") -Force
    Write-Output "agent   -> $($a.Name)"
}
foreach ($c in Get-ChildItem (Join-Path $src "commands") -Filter *.md) {
    Copy-Item $c.FullName (Join-Path $dst "command\$($c.Name)") -Force
    Write-Output "command -> $($c.Name)"
}
Write-Output "Installed. Restart any running opencode session to load them."
