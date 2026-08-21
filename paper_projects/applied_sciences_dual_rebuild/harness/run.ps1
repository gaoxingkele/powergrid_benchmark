param(
    [ValidateSet('check', 'status', 'plan', 'manifest', 'run-stage')]
    [string]$Command = 'check',
    [string]$Stage,
    [switch]$Execute,
    [string]$Write
)

$ErrorActionPreference = 'Stop'
$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../..')).Path
$harness = Join-Path $workspace 'paper_projects/research_paper_harness/harness.py'
$profile = Join-Path $PSScriptRoot 'profile.json'
$cliArgs = @($harness, $Command, '--profile', $profile)
if ($Command -eq 'run-stage') {
    if ([string]::IsNullOrWhiteSpace($Stage)) {
        throw '-Stage is required for run-stage.'
    }
    $cliArgs += @('--stage', $Stage)
    if ($Execute) { $cliArgs += '--execute' }
}
if ($Command -eq 'manifest' -and -not [string]::IsNullOrWhiteSpace($Write)) {
    $cliArgs += @('--write', $Write)
}
& python @cliArgs
exit $LASTEXITCODE

