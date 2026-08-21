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
    # MiKTeX can write nonfatal maintenance notices to stderr. PowerShell turns
    # those lines into error records when ErrorActionPreference is Stop, even
    # though the native process exits successfully. Judge native tools by their
    # exit code while retaining strict handling for PowerShell filesystem work.
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

Invoke-NativeChecked { python scripts/verify_manuscript.py } 'Manuscript evidence verification failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex } 'First pdflatex pass failed.'
Invoke-NativeChecked { bibtex build/paper_applsci } 'BibTeX pass failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex } 'Second pdflatex pass failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex } 'Final pdflatex pass failed.'

$pdf = Join-Path $manuscriptDir 'build/paper_applsci.pdf'
if (-not (Test-Path -LiteralPath $pdf)) { throw 'PDF was not produced.' }
Write-Output "Built: $pdf"
