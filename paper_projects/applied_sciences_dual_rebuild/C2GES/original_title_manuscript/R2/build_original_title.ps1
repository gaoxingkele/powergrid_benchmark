$ErrorActionPreference = 'Stop'
$env:SOURCE_DATE_EPOCH = '1785888000'
$env:FORCE_SOURCE_DATE = '1'
$manuscriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $manuscriptDir
$outputDir = Join-Path $manuscriptDir 'build_r2'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

function Invoke-NativeChecked {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Command,
        [Parameter(Mandatory = $true)][string]$FailureMessage
    )
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

# Deliberately do not run the narrow-title canonical generator. It regenerates
# FEVER-side tables that are not authoritative for the original-title domain run.
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error "-output-directory=$outputDir" paper_applsci.tex } 'First pdflatex pass failed.'
Invoke-NativeChecked { bibtex (Join-Path $outputDir 'paper_applsci') } 'BibTeX pass failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error "-output-directory=$outputDir" paper_applsci.tex } 'Second pdflatex pass failed.'
Invoke-NativeChecked { pdflatex -interaction=nonstopmode -halt-on-error "-output-directory=$outputDir" paper_applsci.tex } 'Final pdflatex pass failed.'

$pdf = Join-Path $outputDir 'paper_applsci.pdf'
if (-not (Test-Path -LiteralPath $pdf)) { throw 'PDF was not produced.' }
Write-Output "Built original-title manuscript: $pdf"
