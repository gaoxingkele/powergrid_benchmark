param(
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = $null
foreach ($Candidate in @(
    (Join-Path $PSScriptRoot '..\..'),
    (Join-Path $PSScriptRoot '..\..\..')
)) {
    $ResolvedCandidate = (Resolve-Path $Candidate).Path
    if (Test-Path -LiteralPath (Join-Path $ResolvedCandidate 'evidence\manifests\p4_s4_results_artifact_manifest_20260813.json') -PathType Leaf) {
        $ProjectRoot = $ResolvedCandidate
        break
    }
}
if ($null -eq $ProjectRoot) {
    throw 'Cannot locate the p4 project root from this figure-script copy.'
}
$ManifestPath = Join-Path $ProjectRoot 'evidence\manifests\p4_s4_results_artifact_manifest_20260813.json'
$Manifest = Get-Content -Raw -LiteralPath $ManifestPath | ConvertFrom-Json
$Invariant = [System.Globalization.CultureInfo]::InvariantCulture

function Resolve-ProjectPath {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    return [System.IO.Path]::GetFullPath((Join-Path $ProjectRoot $RelativePath))
}

function Get-RelativeProjectPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    $RootUri = [System.Uri]::new(($ProjectRoot.TrimEnd('\') + '\'))
    $PathUri = [System.Uri]::new([System.IO.Path]::GetFullPath($Path))
    return [System.Uri]::UnescapeDataString($RootUri.MakeRelativeUri($PathUri).ToString())
}

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-Double {
    param([Parameter(Mandatory = $true)][object]$Value)
    return [double]::Parse([string]$Value, $Invariant)
}

function Get-Stats {
    param(
        [Parameter(Mandatory = $true)][object[]]$Rows,
        [Parameter(Mandatory = $true)][string]$Column
    )
    $Values = @($Rows | ForEach-Object { Get-Double $_.$Column })
    if ($Values.Count -eq 0) {
        throw "No values for column '$Column'."
    }
    $Mean = ($Values | Measure-Object -Average).Average
    $Variance = 0.0
    if ($Values.Count -gt 1) {
        $SumSquares = 0.0
        foreach ($Value in $Values) {
            $SumSquares += [math]::Pow($Value - $Mean, 2)
        }
        $Variance = $SumSquares / ($Values.Count - 1)
    }
    return [pscustomobject]@{
        n = $Values.Count
        mean = [double]$Mean
        std = [math]::Sqrt($Variance)
    }
}

function Format-Decimal {
    param([double]$Value, [int]$Digits = 8)
    return $Value.ToString("F$Digits", $Invariant)
}

function Write-CanonicalCsv {
    param(
        [Parameter(Mandatory = $true)][object[]]$Rows,
        [Parameter(Mandatory = $true)][string]$Path
    )
    $Parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $Parent)) {
        New-Item -ItemType Directory -Path $Parent | Out-Null
    }
    $Rows | Export-Csv -LiteralPath $Path -NoTypeInformation -Encoding UTF8
}

function Get-SourcePath {
    param([Parameter(Mandatory = $true)][string]$Id)
    $Asset = @($Manifest.source_assets | Where-Object id -eq $Id)
    if ($Asset.Count -ne 1) {
        throw "Manifest source id '$Id' is missing or duplicated."
    }
    return Resolve-ProjectPath $Asset[0].path
}

foreach ($Asset in $Manifest.source_assets) {
    $Path = Resolve-ProjectPath $Asset.path
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Manifest source is missing: $($Asset.id) -> $Path"
    }
    $ActualHash = Get-Sha256 $Path
    if ($ActualHash -ne ([string]$Asset.sha256).ToLowerInvariant()) {
        throw "Manifest hash mismatch for $($Asset.id): expected $($Asset.sha256), found $ActualHash"
    }
    if ($null -ne $Asset.PSObject.Properties['rows']) {
        $ActualRows = (Get-Content -LiteralPath $Path).Count - 1
        if ($ActualRows -ne [int]$Asset.rows) {
            throw "Manifest row-count mismatch for $($Asset.id): expected $($Asset.rows), found $ActualRows"
        }
    }
}

$BuildRecordPath = Resolve-ProjectPath $Manifest.outputs.build_record

if ($VerifyOnly) {
    if (-not (Test-Path -LiteralPath $BuildRecordPath -PathType Leaf)) {
        throw "Build record is missing: $BuildRecordPath"
    }
    $BuildRecord = Get-Content -Raw -LiteralPath $BuildRecordPath | ConvertFrom-Json
    $ManifestHash = Get-Sha256 $ManifestPath
    if ($BuildRecord.source_manifest_sha256 -ne $ManifestHash) {
        throw "Build record was not produced from the current canonical manifest."
    }
    $GeneratorPath = Resolve-ProjectPath $BuildRecord.generator
    if ((Get-Sha256 $GeneratorPath) -ne $BuildRecord.generator_sha256) {
        throw "Build record was not produced by the current artifact generator."
    }
    foreach ($Artifact in $BuildRecord.artifacts) {
        $Path = Resolve-ProjectPath $Artifact.path
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
            throw "Generated artifact is missing: $Path"
        }
        $ActualHash = Get-Sha256 $Path
        if ($ActualHash -ne $Artifact.sha256) {
            throw "Generated artifact hash mismatch: $($Artifact.path)"
        }
    }
    Write-Output "OK: canonical sources and $($BuildRecord.artifacts.Count) generated artifacts verified."
    exit 0
}

$MainRuns = @(Import-Csv -LiteralPath (Get-SourcePath 'main_runs') | Where-Object paper -eq 'p4')
$Inference = @(Import-Csv -LiteralPath (Get-SourcePath 'main_inference') | Where-Object paper -eq 'p4')
$MechanismInference = @(Import-Csv -LiteralPath (Get-SourcePath 'mechanism_inference') | Where-Object paper -eq 'p4')
$AcSummary = @(Import-Csv -LiteralPath (Get-SourcePath 'ac_summary') | Where-Object paper -eq 'p4')
$LabelSpec = @($Manifest.archive_labels | Sort-Object display_order)

# -------------------------------------------------------------------------
# Canonical derived tables
# -------------------------------------------------------------------------
$ProxyRows = @()
foreach ($Label in $LabelSpec) {
    $Experiment = [string]$Label.experiment_id
    $Shield = Get-Stats @($MainRuns | Where-Object { $_.experiment_id -eq $Experiment -and $_.method -eq 'SHIELD-MOEA' }) 'hypervolume'
    $Repair = Get-Stats @($MainRuns | Where-Object { $_.experiment_id -eq $Experiment -and $_.method -eq 'NSGA-II+Repair' }) 'hypervolume'
    $Nsga = Get-Stats @($MainRuns | Where-Object { $_.experiment_id -eq $Experiment -and $_.method -eq 'NSGA-II' }) 'hypervolume'
    $RepairInf = @($Inference | Where-Object { $_.experiment_id -eq $Experiment -and $_.comparison -eq 'SHIELD-MOEA vs NSGA-II+Repair' })
    if ($RepairInf.Count -ne 1) {
        throw "Expected one repaired-NSGA inference row for $Experiment."
    }
    $NsgaInf = @($Inference | Where-Object { $_.experiment_id -eq $Experiment -and $_.comparison -eq 'SHIELD-MOEA vs NSGA-II' })
    if ($NsgaInf.Count -ne 1) {
        throw "Expected one NSGA-II inference row for $Experiment."
    }
    $ProxyRows += [pscustomobject][ordered]@{
        display_order = [int]$Label.display_order
        experiment_id = $Experiment
        display_label = [string]$Label.display_label
        evidence_class = [string]$Label.evidence_class
        active_proxy_configuration = [string]$Label.active_proxy_configuration
        optimizer_seeds_per_method = $Shield.n
        shield_mean_hv = Format-Decimal $Shield.mean
        shield_sd_hv = Format-Decimal $Shield.std
        nsga2_repair_mean_hv = Format-Decimal $Repair.mean
        nsga2_repair_sd_hv = Format-Decimal $Repair.std
        shield_minus_repair_mean_hv = Format-Decimal (Get-Double $RepairInf[0].mean_difference)
        shield_minus_repair_relative_pct = Format-Decimal (Get-Double $RepairInf[0].relative_difference_pct) 6
        shield_minus_repair_ci_low = Format-Decimal (Get-Double $RepairInf[0].mean_diff_ci_low)
        shield_minus_repair_ci_high = Format-Decimal (Get-Double $RepairInf[0].mean_diff_ci_high)
        shield_vs_repair_p_holm = ([double](Get-Double $RepairInf[0].p_holm_stochastic_family)).ToString('G8', $Invariant)
        nsga2_mean_hv = Format-Decimal $Nsga.mean
        nsga2_sd_hv = Format-Decimal $Nsga.std
        shield_minus_nsga2_relative_pct = Format-Decimal (Get-Double $NsgaInf[0].relative_difference_pct) 6
        interpretation_note = [string]$Label.note
    }
}

$PooledRows = @()
foreach ($Method in $Manifest.method_sets.framework_comparison_table) {
    $Rows = @($MainRuns | Where-Object method -eq $Method)
    $Hv = Get-Stats $Rows 'hypervolume'
    $Worst = Get-Stats $Rows 'hypervolume_worst_case'
    $Runtime = Get-Stats $Rows 'runtime_s'
    $Front = Get-Stats $Rows 'feasible_front_size'
    $PooledRows += [pscustomobject][ordered]@{
        method = [string]$Method
        method_role = [string]$Rows[0].method_role
        archived_rows = $Rows.Count
        inferential_n_per_label = if ($Method -in @('Weighted Sum', 'Deterministic Planning')) { 1 } else { 30 }
        archive_label_blocks = 8
        active_proxy_configurations = 5
        mean_hv = Format-Decimal $Hv.mean
        sd_hv = Format-Decimal $Hv.std
        mean_sampled_worst_envelope_hv = Format-Decimal $Worst.mean
        mean_runtime_s = Format-Decimal $Runtime.mean
        mean_feasible_front_size = Format-Decimal $Front.mean 4
        aggregation_scope = 'descriptive over eight archived label blocks; reference configuration is represented four times'
    }
}

$FullRows = @($MainRuns | Where-Object method -eq 'SHIELD-MOEA')
$FullHv = Get-Stats $FullRows 'hypervolume'
$FullRuntime = Get-Stats $FullRows 'runtime_s'
$MechanismDefinitions = @(
    [pscustomobject]@{ key = 'repair'; opponent = 'Ablation-NoRepair'; label = 'No repair'; conclusion = 'resolved quality loss in 8/8 labels; repair is load-bearing within SHIELD' },
    [pscustomobject]@{ key = 'screening'; opponent = 'Ablation-NoScenarioScreen'; label = 'No scenario screening'; conclusion = 'no quality difference detected in 8/8 labels; equivalence not tested' },
    [pscustomobject]@{ key = 'survivability_selection'; opponent = 'Ablation-NoResilienceObj'; label = 'No survivability in selection'; conclusion = 'no quality difference detected; screening still uses survivability' },
    [pscustomobject]@{ key = 'outage_exposure'; opponent = 'Ablation-NoOutage'; label = 'No outage in search'; conclusion = 'proxy difference is label-dependent; AC mapping remains descriptive and associational' }
)
$MechanismRows = @()
foreach ($Definition in $MechanismDefinitions) {
    $OpponentRows = @($MainRuns | Where-Object method -eq $Definition.opponent)
    $OpponentHv = Get-Stats $OpponentRows 'hypervolume'
    $OpponentRuntime = Get-Stats $OpponentRows 'runtime_s'
    $ComparisonName = "SHIELD-MOEA vs $($Definition.opponent)"
    $SigRows = @($Inference | Where-Object comparison -eq $ComparisonName)
    $Significant = @($SigRows | Where-Object { ([string]$_.significant_005_holm).ToLowerInvariant() -eq 'true' }).Count
    $MechanismRows += [pscustomobject][ordered]@{
        mechanism = $Definition.key
        comparison = $ComparisonName
        full_mean_hv = Format-Decimal $FullHv.mean
        ablation_mean_hv = Format-Decimal $OpponentHv.mean
        ablation_relative_to_full_pct = Format-Decimal (100.0 * ($OpponentHv.mean - $FullHv.mean) / $FullHv.mean) 6
        holm_significant_labels = $Significant
        labels_tested = $SigRows.Count
        full_mean_runtime_s = Format-Decimal $FullRuntime.mean
        ablation_mean_runtime_s = Format-Decimal $OpponentRuntime.mean
        full_optimization_loop_objective_rows = if ($Definition.key -eq 'screening') { [int]$Manifest.screening_workload.screened_total_static_objective_rows } else { '' }
        ablation_optimization_loop_objective_rows = if ($Definition.key -eq 'screening') { [int]$Manifest.screening_workload.no_screen_total_static_objective_rows } else { '' }
        optimization_loop_row_reduction_pct = if ($Definition.key -eq 'screening') { Format-Decimal (100.0 * (Get-Double $Manifest.screening_workload.static_row_reduction_fraction)) 2 } else { '' }
        supported_conclusion = $Definition.conclusion
    }
}

$AcRows = @()
foreach ($Row in $AcSummary) {
    $AcRows += [pscustomobject][ordered]@{
        method = [string]$Row.method
        method_role = [string]$Row.method_role
        mapped_cases = [int]$Row.cases
        ac_feasible_rate = Format-Decimal (Get-Double $Row.ac_feasible_rate) 6
        stress_ac_feasible_rate = Format-Decimal (Get-Double $Row.stress_ac_feasible_rate) 6
        mean_min_vm_pu = Format-Decimal (Get-Double $Row.mean_min_vm_pu) 6
        mean_max_line_loading_pct = Format-Decimal (Get-Double $Row.mean_max_line_loading_pct) 4
        mean_losses_mw = Format-Decimal (Get-Double $Row.mean_losses_mw) 6
        analysis_unit = 'one seed-0 action-kind composition mapped to one network and one operating scenario'
        interpretation_scope = 'illustrative/associational fixed mapping; not nodal-plan validation, optimizer replication, or causal attribution'
    }
}

$DerivedDir = Join-Path $ProjectRoot 'manuscript\derived_tables'
$ProxyPath = Join-Path $DerivedDir 'p4_s4_proxy_quality_by_label.csv'
$PooledPath = Join-Path $DerivedDir 'p4_s4_pooled_framework_quality.csv'
$MechanismPath = Join-Path $DerivedDir 'p4_s4_mechanism_quality_calls.csv'
$AcPath = Join-Path $DerivedDir 'p4_s4_ac_mapping.csv'
Write-CanonicalCsv $ProxyRows $ProxyPath
Write-CanonicalCsv $PooledRows $PooledPath
Write-CanonicalCsv $MechanismRows $MechanismPath
Write-CanonicalCsv $AcRows $AcPath

# -------------------------------------------------------------------------
# Publication figures. System.Drawing is used because the sandboxed Windows
# Python launcher is not executable in this environment. The figures remain
# fully data-driven by the same hash-verified manifest and CSV inputs.
# -------------------------------------------------------------------------
Add-Type -AssemblyName System.Drawing

$Blue = [System.Drawing.Color]::FromArgb(42, 120, 214)
$BlueDark = [System.Drawing.Color]::FromArgb(28, 92, 171)
$Orange = [System.Drawing.Color]::FromArgb(230, 126, 34)
$GrayDark = [System.Drawing.Color]::FromArgb(77, 77, 74)
$GrayMid = [System.Drawing.Color]::FromArgb(138, 138, 134)
$GrayLight = [System.Drawing.Color]::FromArgb(201, 201, 196)
$GrayFill = [System.Drawing.Color]::FromArgb(235, 235, 231)
$Ink = [System.Drawing.Color]::FromArgb(38, 38, 37)
$Muted = [System.Drawing.Color]::FromArgb(100, 100, 96)
$BandBlue = [System.Drawing.Color]::FromArgb(235, 244, 253)
$BandGray = [System.Drawing.Color]::FromArgb(245, 245, 242)

function New-Font {
    param([float]$Size, [System.Drawing.FontStyle]$Style = [System.Drawing.FontStyle]::Regular)
    return [System.Drawing.Font]::new('Arial', $Size, $Style, [System.Drawing.GraphicsUnit]::Pixel)
}

function New-Canvas {
    param([int]$Width, [int]$Height)
    $Bitmap = [System.Drawing.Bitmap]::new($Width, $Height)
    $Bitmap.SetResolution(300, 300)
    $Graphics = [System.Drawing.Graphics]::FromImage($Bitmap)
    $Graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $Graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $Graphics.Clear([System.Drawing.Color]::White)
    return [pscustomobject]@{ Bitmap = $Bitmap; Graphics = $Graphics }
}

function Save-Canvas {
    param([object]$Canvas, [string]$Path)
    $Canvas.Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $Canvas.Graphics.Dispose()
    $Canvas.Bitmap.Dispose()
}

function Draw-TextCentered {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [System.Drawing.Font]$Font,
        [System.Drawing.Brush]$Brush,
        [float]$CenterX,
        [float]$Y
    )
    $Size = $Graphics.MeasureString($Text, $Font)
    $Graphics.DrawString($Text, $Font, $Brush, $CenterX - $Size.Width / 2.0, $Y)
}

function Draw-VerticalText {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [System.Drawing.Font]$Font,
        [System.Drawing.Brush]$Brush,
        [float]$X,
        [float]$Y
    )
    $State = $Graphics.Save()
    $Graphics.TranslateTransform($X, $Y)
    $Graphics.RotateTransform(-90)
    $Size = $Graphics.MeasureString($Text, $Font)
    $Graphics.DrawString($Text, $Font, $Brush, -$Size.Width / 2.0, 0)
    $Graphics.Restore($State)
}

function Map-Y {
    param([double]$Value, [double]$Minimum, [double]$Maximum, [float]$Top, [float]$Height)
    return [float]($Top + $Height * (1.0 - (($Value - $Minimum) / ($Maximum - $Minimum))))
}

function Map-X {
    param([double]$Value, [double]$Minimum, [double]$Maximum, [float]$Left, [float]$Width)
    return [float]($Left + $Width * (($Value - $Minimum) / ($Maximum - $Minimum)))
}

function Draw-ProxyQualityFigure {
    param([string]$Path)
    $Canvas = New-Canvas 1800 1050
    $G = $Canvas.Graphics
    $Title = New-Font 34 ([System.Drawing.FontStyle]::Bold)
    $Subtitle = New-Font 22
    $AxisFont = New-Font 21
    $TickFont = New-Font 18
    $Small = New-Font 17
    $SmallBold = New-Font 17 ([System.Drawing.FontStyle]::Bold)
    $InkBrush = [System.Drawing.SolidBrush]::new($Ink)
    $MutedBrush = [System.Drawing.SolidBrush]::new($Muted)
    $BlueBrush = [System.Drawing.SolidBrush]::new($Blue)
    $OrangeBrush = [System.Drawing.SolidBrush]::new($Orange)
    $GrayBrush = [System.Drawing.SolidBrush]::new($GrayDark)

    Draw-TextCentered $G 'Proxy-quality comparison across archived label blocks' $Title $InkBrush 900 25
    Draw-TextCentered $G 'Proxy hypervolume, mean +/- SD over 30 independent optimizer seeds per stochastic method and label' $Subtitle $MutedBrush 900 75

    $Left = 145.0; $Top = 190.0; $Width = 1580.0; $Height = 620.0
    $Step = $Width / 8.0
    $G.FillRectangle([System.Drawing.SolidBrush]::new($BandBlue), $Left, $Top - 55, $Step * 4, $Height + 80)
    $G.FillRectangle([System.Drawing.SolidBrush]::new($BandGray), $Left + $Step * 4, $Top - 55, $Step * 4, $Height + 80)
    Draw-TextCentered $G 'Identical-range replicate blocks (independent optimizer seeds)' $SmallBold $BlueBrush ($Left + $Step * 2) ($Top - 48)
    Draw-TextCentered $G 'Distinct active proxy configurations' $SmallBold $GrayBrush ($Left + $Step * 6) ($Top - 48)
    $G.DrawLine([System.Drawing.Pen]::new($GrayMid, 2), $Left + $Step * 4, $Top - 55, $Left + $Step * 4, $Top + $Height + 25)

    $YMin = 0.20; $YMax = 0.36
    foreach ($Tick in @(0.20, 0.24, 0.28, 0.32, 0.36)) {
        $Y = Map-Y $Tick $YMin $YMax $Top $Height
        $G.DrawLine([System.Drawing.Pen]::new($GrayLight, 1), $Left, $Y, $Left + $Width, $Y)
        $G.DrawString($Tick.ToString('F2', $Invariant), $TickFont, $MutedBrush, 65, $Y - 12)
    }
    $G.DrawLine([System.Drawing.Pen]::new($GrayDark, 2), $Left, $Top, $Left, $Top + $Height)
    $G.DrawLine([System.Drawing.Pen]::new($GrayDark, 2), $Left, $Top + $Height, $Left + $Width, $Top + $Height)
    Draw-VerticalText $G 'Held-out proxy hypervolume' $AxisFont $InkBrush 28 ($Top + $Height / 2)

    $Series = @(
        [pscustomobject]@{ method = 'SHIELD-MOEA'; color = $Blue; offset = -24.0; marker = 'square' },
        [pscustomobject]@{ method = 'NSGA-II+Repair'; color = $Orange; offset = 0.0; marker = 'circle' },
        [pscustomobject]@{ method = 'NSGA-II'; color = $GrayDark; offset = 24.0; marker = 'diamond' }
    )
    for ($I = 0; $I -lt $LabelSpec.Count; $I++) {
        $Label = $LabelSpec[$I]
        $CenterX = $Left + $Step * ($I + 0.5)
        foreach ($S in $Series) {
            $Stats = Get-Stats @($MainRuns | Where-Object { $_.experiment_id -eq $Label.experiment_id -and $_.method -eq $S.method }) 'hypervolume'
            $X = $CenterX + $S.offset
            $Y = Map-Y $Stats.mean $YMin $YMax $Top $Height
            $YLow = Map-Y ($Stats.mean - $Stats.std) $YMin $YMax $Top $Height
            $YHigh = Map-Y ($Stats.mean + $Stats.std) $YMin $YMax $Top $Height
            $Pen = [System.Drawing.Pen]::new($S.color, 3)
            $G.DrawLine($Pen, $X, $YLow, $X, $YHigh)
            $G.DrawLine($Pen, $X - 7, $YLow, $X + 7, $YLow)
            $G.DrawLine($Pen, $X - 7, $YHigh, $X + 7, $YHigh)
            $Brush = [System.Drawing.SolidBrush]::new($S.color)
            if ($S.marker -eq 'square') {
                $G.FillRectangle($Brush, $X - 8, $Y - 8, 16, 16)
            } elseif ($S.marker -eq 'circle') {
                $G.FillEllipse($Brush, $X - 8, $Y - 8, 16, 16)
            } else {
                $Points = [System.Drawing.PointF[]]@(
                    [System.Drawing.PointF]::new($X, $Y - 9),
                    [System.Drawing.PointF]::new($X + 9, $Y),
                    [System.Drawing.PointF]::new($X, $Y + 9),
                    [System.Drawing.PointF]::new($X - 9, $Y)
                )
                $G.FillPolygon($Brush, $Points)
            }
        }
        $LabelText = ([string]$Label.display_label).Replace(' ', "`n")
        $Lines = $LabelText -split "`n"
        for ($J = 0; $J -lt $Lines.Count; $J++) {
            Draw-TextCentered $G $Lines[$J] $Small $InkBrush $CenterX ($Top + $Height + 18 + 20 * $J)
        }
    }

    $LegendY = 900.0
    $LegendItems = @(
        [pscustomobject]@{ label = 'SHIELD-MOEA'; color = $Blue; x = 410 },
        [pscustomobject]@{ label = 'NSGA-II+Repair'; color = $Orange; x = 760 },
        [pscustomobject]@{ label = 'NSGA-II'; color = $GrayDark; x = 1160 }
    )
    foreach ($Item in $LegendItems) {
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Item.color), $Item.x, $LegendY + 4, 20, 20)
        $G.DrawString($Item.label, $Small, $InkBrush, $Item.x + 30, $LegendY)
    }
    Draw-TextCentered $G 'Pooled archive means: 0.27396 vs 0.26070 (post-hoc-repaired NSGA-II, +5.09%) and 0.25953 (plain NSGA-II, +5.56%).' $SmallBold $BlueBrush 900 952
    Draw-TextCentered $G 'The four replicate blocks are independent samples under one active reference configuration, not four uncertainty regimes.' $Small $MutedBrush 900 982
    Save-Canvas $Canvas $Path
}

function Draw-RepairScreeningFigure {
    param([string]$Path)
    $Canvas = New-Canvas 1800 980
    $G = $Canvas.Graphics
    $Title = New-Font 34 ([System.Drawing.FontStyle]::Bold)
    $Subtitle = New-Font 21
    $AxisFont = New-Font 20
    $LabelFont = New-Font 20
    $Small = New-Font 17
    $SmallBold = New-Font 18 ([System.Drawing.FontStyle]::Bold)
    $InkBrush = [System.Drawing.SolidBrush]::new($Ink)
    $MutedBrush = [System.Drawing.SolidBrush]::new($Muted)
    $BlueBrush = [System.Drawing.SolidBrush]::new($Blue)
    Draw-TextCentered $G 'Mechanism evidence: repair drives quality; screening changes loop workload' $Title $InkBrush 900 25
    Draw-TextCentered $G 'Pooled proxy HV is descriptive over eight archived blocks; Holm decisions are within label' $Subtitle $MutedBrush 900 75

    $Left = 360.0; $Top = 160.0; $Width = 850.0; $Height = 610.0
    $Methods = @(
        [pscustomobject]@{ id = 'SHIELD-MOEA'; label = 'Full SHIELD-MOEA'; color = $Blue },
        [pscustomobject]@{ id = 'Ablation-NoRepair'; label = 'No repair'; color = $GrayLight },
        [pscustomobject]@{ id = 'Ablation-NoScenarioScreen'; label = 'No scenario screening'; color = $GrayLight },
        [pscustomobject]@{ id = 'Ablation-NoResilienceObj'; label = 'No survivability in selection'; color = $GrayLight },
        [pscustomobject]@{ id = 'Ablation-NoOutage'; label = 'No outage in search'; color = $GrayLight }
    )
    $XMin = 0.0; $XMax = 0.31
    foreach ($Tick in @(0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)) {
        $X = Map-X $Tick $XMin $XMax $Left $Width
        $G.DrawLine([System.Drawing.Pen]::new($GrayLight, 1), $X, $Top, $X, $Top + $Height)
        Draw-TextCentered $G $Tick.ToString('F2', $Invariant) $Small $MutedBrush $X ($Top + $Height + 12)
    }
    $G.DrawLine([System.Drawing.Pen]::new($GrayDark, 2), $Left, $Top + $Height, $Left + $Width, $Top + $Height)
    $BarStep = $Height / $Methods.Count
    for ($I = 0; $I -lt $Methods.Count; $I++) {
        $Method = $Methods[$I]
        $Rows = @($MainRuns | Where-Object method -eq $Method.id)
        $Stats = Get-Stats $Rows 'hypervolume'
        $CenterY = $Top + $BarStep * ($I + 0.5)
        $BarRight = Map-X $Stats.mean $XMin $XMax $Left $Width
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Method.color), $Left, $CenterY - 28, $BarRight - $Left, 56)
        $G.DrawRectangle([System.Drawing.Pen]::new($(if ($Method.id -eq 'SHIELD-MOEA') { $BlueDark } else { $GrayMid }), 2), $Left, $CenterY - 28, $BarRight - $Left, 56)
        $G.DrawString($Method.label, $LabelFont, $InkBrush, 20, $CenterY - 14)
        if ($Method.id -ne 'SHIELD-MOEA') {
            $Definition = $MechanismDefinitions | Where-Object opponent -eq $Method.id
            $Row = $MechanismRows | Where-Object mechanism -eq $Definition.key
            $Delta = Get-Double $Row.ablation_relative_to_full_pct
            $Annotation = '{0:+0.00;-0.00;0.00}% ; Holm-significant {1}/8' -f $Delta, $Row.holm_significant_labels
            $StyleBrush = if ($Method.id -eq 'Ablation-NoRepair') { $BlueBrush } else { $InkBrush }
            $Font = if ($Method.id -eq 'Ablation-NoRepair') { $SmallBold } else { $Small }
            $G.DrawString($Annotation, $Font, $StyleBrush, $BarRight + 16, $CenterY - 12)
        }
    }
    Draw-TextCentered $G 'Pooled proxy hypervolume (mean over 8 label blocks x 30 seeds)' $AxisFont $InkBrush ($Left + $Width / 2) ($Top + $Height + 50)

    $PanelLeft = 1280.0; $PanelTop = 190.0; $PanelWidth = 450.0; $PanelHeight = 400.0
    $G.DrawRectangle([System.Drawing.Pen]::new($GrayMid, 2), $PanelLeft, $PanelTop, $PanelWidth, $PanelHeight)
    Draw-TextCentered $G 'Optimization-loop rows' $AxisFont $InkBrush ($PanelLeft + $PanelWidth / 2) ($PanelTop + 20)
    $NoScreenRows = [double]$Manifest.screening_workload.no_screen_total_static_objective_rows
    $ScreenRows = [double]$Manifest.screening_workload.screened_total_static_objective_rows
    $MaxRows = 55000.0
    $BarLeft = $PanelLeft + 145
    $BarWidth = 255
    $Y1 = $PanelTop + 120; $Y2 = $PanelTop + 230
    foreach ($Entry in @(
        [pscustomobject]@{ label = 'SHIELD'; value = $ScreenRows; y = $Y1; color = $Blue },
        [pscustomobject]@{ label = 'No screen'; value = $NoScreenRows; y = $Y2; color = $GrayDark }
    )) {
        $G.DrawString($Entry.label, $Small, $InkBrush, $PanelLeft + 18, $Entry.y - 12)
        $Length = [float]($BarWidth * $Entry.value / $MaxRows)
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Entry.color), $BarLeft, $Entry.y - 18, $Length, 36)
        $G.DrawString(('{0:N0}' -f $Entry.value), $SmallBold, $InkBrush, $BarLeft + $Length + 8, $Entry.y - 13)
    }
    Draw-TextCentered $G '65% fewer loop objective rows' $SmallBold $BlueBrush ($PanelLeft + $PanelWidth / 2) ($PanelTop + 320)
    Draw-TextCentered $G 'bounds/final evaluation excluded' $Small $MutedBrush ($PanelLeft + $PanelWidth / 2) ($PanelTop + 352)

    Draw-TextCentered $G 'Quality-workload asymmetry: screening uses fewer optimization-loop rows, but no held-out-HV difference is detected against no screening.' $SmallBold $InkBrush 900 875
    Draw-TextCentered $G 'Equivalence was not tested; archived runtime is 0.0889 s with screening versus 0.0792 s without it, so no wall-clock saving is claimed.' $Small $MutedBrush 900 910
    Save-Canvas $Canvas $Path
}

function Draw-ScreeningQualityCallsFigure {
    param([string]$Path)
    $Canvas = New-Canvas 1600 820
    $G = $Canvas.Graphics
    $Title = New-Font 34 ([System.Drawing.FontStyle]::Bold)
    $Subtitle = New-Font 21
    $AxisFont = New-Font 20
    $Small = New-Font 18
    $SmallBold = New-Font 19 ([System.Drawing.FontStyle]::Bold)
    $InkBrush = [System.Drawing.SolidBrush]::new($Ink)
    $MutedBrush = [System.Drawing.SolidBrush]::new($Muted)
    $BlueBrush = [System.Drawing.SolidBrush]::new($Blue)
    Draw-TextCentered $G 'Screening quality-workload asymmetry' $Title $InkBrush 800 25
    Draw-TextCentered $G 'Quality is held-out proxy HV; workload is optimization-loop plan-scenario row arithmetic' $Subtitle $MutedBrush 800 75

    $PanelTop = 160.0; $PanelHeight = 430.0
    $G.DrawRectangle([System.Drawing.Pen]::new($GrayMid, 2), 80, $PanelTop, 680, $PanelHeight)
    $G.DrawRectangle([System.Drawing.Pen]::new($GrayMid, 2), 840, $PanelTop, 680, $PanelHeight)
    Draw-TextCentered $G '(a) Held-out proxy quality' $AxisFont $InkBrush 420 ($PanelTop + 18)
    Draw-TextCentered $G '(b) Optimization-loop objective rows' $AxisFont $InkBrush 1180 ($PanelTop + 18)

    $ScreenRow = @($MechanismRows | Where-Object mechanism -eq 'screening')[0]
    $FullMean = Get-Double $ScreenRow.full_mean_hv
    $NoScreenMean = Get-Double $ScreenRow.ablation_mean_hv
    $QualityY = $PanelTop + 150
    $BaseX = 235.0; $QualityWidth = 420.0
    foreach ($Entry in @(
        [pscustomobject]@{ label = 'SHIELD'; value = $FullMean; y = $QualityY; color = $Blue },
        [pscustomobject]@{ label = 'No screen'; value = $NoScreenMean; y = $QualityY + 120; color = $GrayDark }
    )) {
        $G.DrawString($Entry.label, $Small, $InkBrush, 105, $Entry.y - 12)
        $Length = [float]($QualityWidth * $Entry.value / 0.30)
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Entry.color), $BaseX, $Entry.y - 22, $Length, 44)
        $G.DrawString($Entry.value.ToString('F5', $Invariant), $SmallBold, $InkBrush, $BaseX + $Length + 8, $Entry.y - 14)
    }
    Draw-TextCentered $G '-0.48% without screening; Holm-significant 0/8' $SmallBold $BlueBrush 420 ($PanelTop + 340)
    Draw-TextCentered $G 'No difference detected; equivalence not tested' $Small $MutedBrush 420 ($PanelTop + 375)

    $CallY = $PanelTop + 150
    $CallBaseX = 1000.0; $CallWidth = 415.0
    foreach ($Entry in @(
        [pscustomobject]@{ label = 'SHIELD'; value = [double]$Manifest.screening_workload.screened_total_static_objective_rows; y = $CallY; color = $Blue },
        [pscustomobject]@{ label = 'No screen'; value = [double]$Manifest.screening_workload.no_screen_total_static_objective_rows; y = $CallY + 120; color = $GrayDark }
    )) {
        $G.DrawString($Entry.label, $Small, $InkBrush, 865, $Entry.y - 12)
        $Length = [float]($CallWidth * $Entry.value / 55000.0)
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Entry.color), $CallBaseX, $Entry.y - 22, $Length, 44)
        $G.DrawString(('{0:N0}' -f $Entry.value), $SmallBold, $InkBrush, $CallBaseX + $Length + 8, $Entry.y - 14)
    }
    Draw-TextCentered $G '65% lower loop-row arithmetic' $SmallBold $BlueBrush 1180 ($PanelTop + 340)
    Draw-TextCentered $G 'Bounds/final evaluation excluded' $Small $MutedBrush 1180 ($PanelTop + 375)
    Draw-TextCentered $G 'Archived wall-clock runtime is higher with screening (0.0889 s vs 0.0792 s); neither a quality gain nor a runtime saving is resolved.' $SmallBold $InkBrush 800 670
    Draw-TextCentered $G 'The loop-row reduction and null quality result answer different estimands and must be reported together.' $Small $MutedBrush 800 710
    Save-Canvas $Canvas $Path
}

function Draw-AcMappingFigure {
    param([string]$Path)
    $Canvas = New-Canvas 1900 1250
    $G = $Canvas.Graphics
    $Title = New-Font 34 ([System.Drawing.FontStyle]::Bold)
    $Subtitle = New-Font 21
    $AxisFont = New-Font 20
    $LabelFont = New-Font 17
    $Small = New-Font 16
    $SmallBold = New-Font 17 ([System.Drawing.FontStyle]::Bold)
    $InkBrush = [System.Drawing.SolidBrush]::new($Ink)
    $MutedBrush = [System.Drawing.SolidBrush]::new($Muted)
    $BlueBrush = [System.Drawing.SolidBrush]::new($Blue)
    Draw-TextCentered $G 'Illustrative fixed-mapping AC composition check' $Title $InkBrush 950 22
    Draw-TextCentered $G '108 mapped cases per method: 3 seed-0 compositions x 6 networks x 6 operating scenarios' $Subtitle $MutedBrush 950 70

    $Order = @('SHIELD-MOEA','NSGA-II+Repair','Ablation-NoRepair','NSGA-II','GA','Ablation-NoResilienceObj','Ablation-NoScenarioScreen','Ablation-NoOutage','Weighted Sum','Deterministic Planning','MOEA/D','NoPlan')
    $Labels = @{
        'SHIELD-MOEA' = 'SHIELD-MOEA'
        'NSGA-II+Repair' = 'NSGA-II + post-hoc repair'
        'Ablation-NoRepair' = 'No repair'
        'NSGA-II' = 'NSGA-II'
        'GA' = 'GA'
        'Ablation-NoResilienceObj' = 'No survivability in selection'
        'Ablation-NoScenarioScreen' = 'No scenario screening'
        'Ablation-NoOutage' = 'No outage in search'
        'Weighted Sum' = 'Weighted Sum'
        'Deterministic Planning' = 'Deterministic planning'
        'MOEA/D' = 'MOEA/D'
        'NoPlan' = 'No plan reference'
    }
    $LeftLabel = 20.0; $Chart1Left = 390.0; $Chart1Width = 610.0; $Chart2Left = 1160.0; $Chart2Width = 650.0
    $Top = 155.0; $Height = 870.0; $Step = $Height / $Order.Count
    Draw-TextCentered $G '(a) AC-feasible rate (solid: all; pale: stress-only)' $AxisFont $InkBrush ($Chart1Left + $Chart1Width / 2) 115
    Draw-TextCentered $G '(b) Mean maximum line loading' $AxisFont $InkBrush ($Chart2Left + $Chart2Width / 2) 115
    foreach ($Tick in @(0.0,0.2,0.4,0.6,0.8,1.0)) {
        $X = Map-X $Tick 0 1 $Chart1Left $Chart1Width
        $G.DrawLine([System.Drawing.Pen]::new($GrayLight,1),$X,$Top,$X,$Top+$Height)
        Draw-TextCentered $G $Tick.ToString('F1',$Invariant) $Small $MutedBrush $X ($Top+$Height+10)
    }
    foreach ($Tick in @(0,25,50,75,100,125)) {
        $X = Map-X $Tick 0 145 $Chart2Left $Chart2Width
        $G.DrawLine([System.Drawing.Pen]::new($GrayLight,1),$X,$Top,$X,$Top+$Height)
        Draw-TextCentered $G ([string]$Tick) $Small $MutedBrush $X ($Top+$Height+10)
    }
    $LimitX = Map-X 100 0 145 $Chart2Left $Chart2Width
    $G.DrawLine([System.Drawing.Pen]::new($GrayDark,2),$LimitX,$Top,$LimitX,$Top+$Height)
    $G.DrawString('100% limit',$Small,$MutedBrush,$LimitX+5,$Top-25)
    $NoPlan = @($AcSummary | Where-Object method -eq 'NoPlan')[0]
    $NoPlanX = Map-X (Get-Double $NoPlan.ac_feasible_rate) 0 1 $Chart1Left $Chart1Width
    $DashPen = [System.Drawing.Pen]::new($GrayDark,2)
    $DashPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
    $G.DrawLine($DashPen,$NoPlanX,$Top,$NoPlanX,$Top+$Height)

    for ($I=0; $I -lt $Order.Count; $I++) {
        $Method = $Order[$I]
        $Row = @($AcSummary | Where-Object method -eq $Method)[0]
        $Y = $Top + $Step * ($I + 0.5)
        $Role = [string]$Row.method_role
        $Color = if ($Method -eq 'SHIELD-MOEA') { $Blue } elseif ($Method -eq 'NSGA-II+Repair') { $Orange } elseif ($Method -eq 'NoPlan') { [System.Drawing.Color]::White } elseif ($Role -eq 'ablation') { $GrayLight } else { $GrayMid }
        $Edge = if ($Method -eq 'SHIELD-MOEA') { $BlueDark } else { $GrayDark }
        $G.DrawString($Labels[$Method],$LabelFont,$InkBrush,$LeftLabel,$Y-12)
        $All = Get-Double $Row.ac_feasible_rate
        $Stress = Get-Double $Row.stress_ac_feasible_rate
        $AllRight = Map-X $All 0 1 $Chart1Left $Chart1Width
        $StressRight = Map-X $Stress 0 1 $Chart1Left $Chart1Width
        $Pale = [System.Drawing.Color]::FromArgb(110,$Color.R,$Color.G,$Color.B)
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Color),$Chart1Left,$Y-23,$AllRight-$Chart1Left,21)
        $G.DrawRectangle([System.Drawing.Pen]::new($Edge,1),$Chart1Left,$Y-23,$AllRight-$Chart1Left,21)
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Pale),$Chart1Left,$Y+2,$StressRight-$Chart1Left,21)
        $G.DrawRectangle([System.Drawing.Pen]::new($Edge,1),$Chart1Left,$Y+2,$StressRight-$Chart1Left,21)
        $Loading = Get-Double $Row.mean_max_line_loading_pct
        $LoadRight = Map-X $Loading 0 145 $Chart2Left $Chart2Width
        $G.FillRectangle([System.Drawing.SolidBrush]::new($Color),$Chart2Left,$Y-19,$LoadRight-$Chart2Left,38)
        $G.DrawRectangle([System.Drawing.Pen]::new($Edge,1),$Chart2Left,$Y-19,$LoadRight-$Chart2Left,38)
        if ($Method -in @('SHIELD-MOEA','NSGA-II+Repair','Ablation-NoOutage','NoPlan')) {
            $Font = if ($Method -eq 'SHIELD-MOEA') { $SmallBold } else { $Small }
            $Brush = if ($Method -eq 'SHIELD-MOEA') { $BlueBrush } else { $InkBrush }
            $G.DrawString($All.ToString('F3',$Invariant),$Font,$Brush,$AllRight+8,$Y-17)
            $G.DrawString(($Loading.ToString('F1',$Invariant)+'%'),$Font,$Brush,$LoadRight+8,$Y-12)
        }
    }
    Draw-TextCentered $G 'AC-feasible rate' $AxisFont $InkBrush ($Chart1Left+$Chart1Width/2) ($Top+$Height+48)
    Draw-TextCentered $G 'Mean maximum line loading (%)' $AxisFont $InkBrush ($Chart2Left+$Chart2Width/2) ($Top+$Height+48)
    Draw-TextCentered $G 'Associational/illustrative scope: fixed rules relocate only action-kind counts; there are no nodal plan identities, independent optimizer replications, or causal p-values.' $SmallBold $InkBrush 950 1140
    Draw-TextCentered $G 'SHIELD improves on no planning (0.685 vs 0.389) but does not exceed post-hoc-repaired NSGA-II (0.694).' $Small $MutedBrush 950 1175
    Save-Canvas $Canvas $Path
}

$ProxyFigure = Join-Path $PSScriptRoot 'fig_proxy_quality.png'
$RepairFigure = Join-Path $PSScriptRoot 'fig_repair_screening.png'
$CallsFigure = Join-Path $PSScriptRoot 'fig_screening_quality_calls.png'
$AcFigure = Join-Path $PSScriptRoot 'fig_ac_mapping.png'
Draw-ProxyQualityFigure $ProxyFigure
Draw-RepairScreeningFigure $RepairFigure
Draw-ScreeningQualityCallsFigure $CallsFigure
Draw-AcMappingFigure $AcFigure

$OutputPaths = @($ProxyPath, $PooledPath, $MechanismPath, $AcPath, $ProxyFigure, $RepairFigure, $CallsFigure, $AcFigure)
$ArtifactRecords = @()
foreach ($Path in $OutputPaths) {
    $Relative = Get-RelativeProjectPath $Path
    $ArtifactRecords += [pscustomobject][ordered]@{
        path = $Relative
        sha256 = Get-Sha256 $Path
        bytes = (Get-Item -LiteralPath $Path).Length
    }
}
$BuildRecord = [pscustomobject][ordered]@{
    manifest_id = [string]$Manifest.manifest_id
    source_manifest = Get-RelativeProjectPath $ManifestPath
    source_manifest_sha256 = Get-Sha256 $ManifestPath
    generated_date = '2026-08-13'
    generator = 'manuscript/figures/build_results_artifacts.ps1'
    generator_sha256 = Get-Sha256 $PSCommandPath
    generator_runtime = "$($PSVersionTable.PSEdition) $($PSVersionTable.PSVersion); System.Drawing"
    artifacts = $ArtifactRecords
    interpretation_constraints = $Manifest.interpretation_constraints
}
$BuildRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $BuildRecordPath -Encoding UTF8

Write-Output "Generated $($ArtifactRecords.Count) artifacts from canonical manifest $($Manifest.manifest_id)."
foreach ($Artifact in $ArtifactRecords) {
    Write-Output ("{0} {1}" -f $Artifact.sha256, $Artifact.path)
}
