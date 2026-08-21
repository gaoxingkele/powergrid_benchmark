$ErrorActionPreference = 'Stop'
$env:SOURCE_DATE_EPOCH = '1785888000'
$env:FORCE_SOURCE_DATE = '1'
$manuscriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $manuscriptDir
New-Item -ItemType Directory -Force -Path (Join-Path $manuscriptDir 'build') | Out-Null

function Invoke-NativeChecked {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Command,
        [Parameter(Mandatory = $true)][string]$FailureMessage
    )
    # MiKTeX writes nonfatal maintenance notices to stderr. Judge native tools
    # by their exit code while retaining strict PowerShell filesystem handling.
    $savedPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & $Command
        $nativeExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $savedPreference
    }
    if ($nativeExitCode -ne 0) { throw $FailureMessage }
}

Invoke-NativeChecked { python scripts/generate_canonical_tex.py } 'Canonical TeX generation failed.'
Invoke-NativeChecked { python scripts/verify_claim_sources.py } 'Claim/source verification failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex } 'First pdflatex pass failed.'
Invoke-NativeChecked { bibtex build/paper_applsci } 'BibTeX pass failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex } 'Second pdflatex pass failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex } 'Final pdflatex pass failed.'

if (-not (Test-Path -LiteralPath "$manuscriptDir\build\paper_applsci.pdf")) { throw "PDF was not produced." }
Write-Output "Built: $manuscriptDir\build\paper_applsci.pdf"
