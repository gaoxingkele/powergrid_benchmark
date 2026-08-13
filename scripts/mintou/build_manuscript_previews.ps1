param(
    [string]$RepositoryRoot = "D:\aicoding\powergrid_benchmark"
)

$ErrorActionPreference = "Stop"

$pandoc = Join-Path $RepositoryRoot ".tools\pandoc-3.6.4\pandoc.exe"
$xelatex = (Get-Command xelatex -ErrorAction Stop).Source
$filter = Join-Path $RepositoryRoot "scripts\mintou\drop_first_title.lua"
$figureFilter = Join-Path $RepositoryRoot "scripts\mintou\unwrap_standalone_figures.lua"

if (-not (Test-Path -LiteralPath $pandoc)) {
    throw "Pinned pandoc executable not found: $pandoc"
}

$projects = @(
    "mintou_p1_dstar_gru_dispatch",
    "mintou_p2_hygraph_load_forecasting",
    "mintou_p3_samode_distribution_planning",
    "mintou_p4_shield_resilience_planning",
    "mintou_p5_trace_moea_feasibility_review",
    "mintou_p6_bilonsga_project_review"
)

$summary = @()
foreach ($project in $projects) {
    $manuscriptDir = Join-Path $RepositoryRoot "paper_projects\$project\manuscript"
    $markdown = Join-Path $manuscriptDir "MANUSCRIPT.md"
    $previewDir = Join-Path $manuscriptDir "submission_preview"
    New-Item -ItemType Directory -Path $previewDir -Force | Out-Null
    $previewFigures = Join-Path $previewDir "figures"
    New-Item -ItemType Directory -Path $previewFigures -Force | Out-Null
    Copy-Item -Path (Join-Path $manuscriptDir "figures\*") -Destination $previewFigures -Force

    $titleLine = Get-Content -LiteralPath $markdown -Encoding UTF8 |
        Where-Object { $_ -match '^#\s+' } |
        Select-Object -First 1
    if (-not $titleLine) {
        throw "No level-one title found in $markdown"
    }
    $title = $titleLine -replace '^#\s+', ''
    $tex = Join-Path $previewDir "paper.tex"

    & $pandoc $markdown `
        --from "markdown+tex_math_dollars+tex_math_single_backslash+raw_tex+pipe_tables" `
        --to latex `
        --standalone `
        --shift-heading-level-by=-1 `
        --toc `
        --lua-filter $filter `
        --lua-filter $figureFilter `
        --pdf-engine xelatex `
        --metadata "title=$title" `
        --variable "documentclass=article" `
        --variable "papersize=a4" `
        --variable "fontsize=10pt" `
        --variable "geometry:margin=18mm" `
        --variable "mainfont=Times New Roman" `
        --variable "sansfont=Arial" `
        --variable "monofont=Consolas" `
        --variable "CJKmainfont=Microsoft YaHei" `
        --variable "colorlinks=true" `
        --variable "linkcolor=blue" `
        --variable "urlcolor=blue" `
        --output $tex

    if ($LASTEXITCODE -ne 0) {
        throw "Pandoc failed for $project"
    }

    # Compile from the source folder that will be packaged.  This is a
    # portability check: paper.tex must not depend on the caller's cwd.
    Push-Location $previewDir
    try {
        & $xelatex -interaction=nonstopmode -halt-on-error "paper.tex" | Out-Null
        $firstExit = $LASTEXITCODE
        $pdf = Join-Path $previewDir "paper.pdf"
        $log = Join-Path $previewDir "paper.log"
        $firstFatal = (Test-Path -LiteralPath $log) -and (Select-String -LiteralPath $log -Pattern '^!' -Quiet)
        if (($firstExit -ne 0) -and ((-not (Test-Path -LiteralPath $pdf)) -or $firstFatal)) {
            throw "First XeLaTeX pass failed for $project"
        }
        & $xelatex -interaction=nonstopmode -halt-on-error "paper.tex" | Out-Null
        $secondExit = $LASTEXITCODE
        $secondFatal = (Test-Path -LiteralPath $log) -and (Select-String -LiteralPath $log -Pattern '^!' -Quiet)
        if (($secondExit -ne 0) -and ((-not (Test-Path -LiteralPath $pdf)) -or $secondFatal)) {
            throw "Second XeLaTeX pass failed for $project"
        }
    }
    finally {
        Pop-Location
    }

    $pdf = Join-Path $previewDir "paper.pdf"
    $summary += [pscustomobject]@{
        Project = $project
        TeX = $tex
        PDF = $pdf
        PDFBytes = (Get-Item -LiteralPath $pdf).Length
    }
}

$summary | Format-Table -AutoSize
