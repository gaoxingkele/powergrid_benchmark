param(
    [Parameter(Mandatory = $false)]
    [string]$Manifest = "evidence/runs/p3_s4_results_narrative_20260813/manifest.json"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ManifestPath = if ([System.IO.Path]::IsPathRooted($Manifest)) { $Manifest } else { Join-Path $Root $Manifest }
$Spec = Get-Content -Raw -Encoding utf8 $ManifestPath | ConvertFrom-Json
$TableDir = Join-Path $Root "manuscript/derived_tables"
$FigureDir = Join-Path $Root "manuscript/figures"

function C([string]$Hex) { return [System.Drawing.ColorTranslator]::FromHtml($Hex) }
$BLUE = C "#0077BB"; $BLUE_DARK = C "#005A8C"; $ORANGE = C "#EE7733"
$TEAL = C "#009988"; $RED = C "#CC3311"; $GRAY = C "#8A8A86"
$LIGHT = C "#E6E6E2"; $INK = C "#242424"; $WHITE = C "#FFFFFF"

function New-Canvas([int]$Width, [int]$Height) {
    $Bitmap = [System.Drawing.Bitmap]::new($Width, $Height)
    $Bitmap.SetResolution(300, 300)
    $Graphics = [System.Drawing.Graphics]::FromImage($Bitmap)
    $Graphics.Clear($WHITE)
    $Graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $Graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    return [pscustomobject]@{ Bitmap = $Bitmap; Graphics = $Graphics }
}

function Save-Canvas($Canvas, [string]$Name) {
    $Path = Join-Path $FigureDir $Name
    $Canvas.Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $Canvas.Graphics.Dispose(); $Canvas.Bitmap.Dispose()
}

function Draw-Text($G, [string]$Value, [float]$X, [float]$Y, [float]$Size = 26,
                   $Color = $INK, [string]$Align = "Near", [bool]$Bold = $false) {
    $Style = if ($Bold) { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
    $Font = [System.Drawing.Font]::new("Arial", $Size, $Style, [System.Drawing.GraphicsUnit]::Pixel)
    $Brush = [System.Drawing.SolidBrush]::new($Color)
    $Format = [System.Drawing.StringFormat]::new()
    $Format.Alignment = [System.Drawing.StringAlignment]::$Align
    $Format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $G.DrawString($Value, $Font, $Brush, [System.Drawing.PointF]::new($X, $Y), $Format)
    $Format.Dispose(); $Brush.Dispose(); $Font.Dispose()
}

function Draw-Line($G, $Color, [float]$Width, [float]$X1, [float]$Y1, [float]$X2, [float]$Y2) {
    $Pen = [System.Drawing.Pen]::new($Color, $Width)
    $G.DrawLine($Pen, $X1, $Y1, $X2, $Y2); $Pen.Dispose()
}

function Fill-Rect($G, $Color, [float]$X, [float]$Y, [float]$W, [float]$H, $Outline = $INK) {
    $Brush = [System.Drawing.SolidBrush]::new($Color)
    $G.FillRectangle($Brush, $X, $Y, $W, $H); $Brush.Dispose()
    $Pen = [System.Drawing.Pen]::new($Outline, 1.5)
    $G.DrawRectangle($Pen, $X, $Y, $W, $H); $Pen.Dispose()
}

function Draw-Marker($G, [float]$X, [float]$Y, $Color, [string]$Shape) {
    $Brush = [System.Drawing.SolidBrush]::new($Color); $Pen = [System.Drawing.Pen]::new($INK, 2)
    if ($Shape -eq "square") { $G.FillRectangle($Brush, $X-10, $Y-10, 20, 20); $G.DrawRectangle($Pen, $X-10, $Y-10, 20, 20) }
    elseif ($Shape -eq "triangle") {
        $Pts = [System.Drawing.PointF[]]@([System.Drawing.PointF]::new($X,$Y-12),[System.Drawing.PointF]::new($X-12,$Y+10),[System.Drawing.PointF]::new($X+12,$Y+10))
        $G.FillPolygon($Brush,$Pts); $G.DrawPolygon($Pen,$Pts)
    } else { $G.FillEllipse($Brush,$X-10,$Y-10,20,20); $G.DrawEllipse($Pen,$X-10,$Y-10,20,20) }
    $Brush.Dispose(); $Pen.Dispose()
}

function Draw-Axes($G, [float]$X0, [float]$Y0, [float]$X1, [float]$Y1,
                   [double]$Min, [double]$Max, [string]$YLabel, [int]$Ticks = 5) {
    for ($i=0; $i -le $Ticks; $i++) {
        $V = $Min + ($Max-$Min)*$i/$Ticks; $Y = $Y1 - ($Y1-$Y0)*$i/$Ticks
        Draw-Line $G $LIGHT 2 $X0 $Y $X1 $Y
        $TickFormat = if ([Math]::Abs($Max) -le 0.1 -and [Math]::Abs($Min) -le 0.1) { "0.000" } else { "0.0" }
        Draw-Text $G ($V.ToString($TickFormat)) ($X0-15) $Y 23 $INK "Far"
    }
    Draw-Line $G $INK 3 $X0 $Y0 $X0 $Y1; Draw-Line $G $INK 3 $X0 $Y1 $X1 $Y1
    if ($YLabel) { Draw-Text $G $YLabel $X0 ($Y0-25) 23 $INK "Near" }
}

function Draw-HBars($G, [float]$X0, [float]$Y0, [float]$X1, [float]$Y1,
                    [string[]]$Labels, [double[]]$Values, [object[]]$Colors,
                    [double]$Min, [double]$Max, [string]$XLabel, [string]$Format = "0.0") {
    $Zero = $X0 + (0-$Min)/($Max-$Min)*($X1-$X0)
    Draw-Line $G $INK 3 $Zero $Y0 $Zero $Y1
    $Row = ($Y1-$Y0)/$Labels.Count
    for($i=0;$i -lt $Labels.Count;$i++) {
        $YC=$Y0+$Row*($i+0.5); $XV=$X0+($Values[$i]-$Min)/($Max-$Min)*($X1-$X0)
        Fill-Rect $G $Colors[$i] ([Math]::Min($Zero,$XV)) ($YC-$Row*.27) ([Math]::Abs($XV-$Zero)) ($Row*.54)
        Draw-Text $G $Labels[$i] ($X0-18) $YC 22 $INK "Far"
        $A=if($Values[$i]-ge 0){"Near"}else{"Far"};$Off=if($Values[$i]-ge 0){8}else{-8}
        Draw-Text $G ($Values[$i].ToString($Format)) ($XV+$Off) $YC 21 $INK $A
    }
    Draw-Line $G $INK 3 $X0 $Y1 $X1 $Y1; Draw-Text $G $XLabel (($X0+$X1)/2) ($Y1+52) 25 $INK "Center"
}

$Effects = Import-Csv (Join-Path $TableDir "p3_configuration_effects.csv")
$Leaderboard = Import-Csv (Join-Path $TableDir "p3_configuration_weighted_leaderboard.csv")
$ConfigMeans = Import-Csv (Join-Path $TableDir "p3_configuration_metric_means.csv")
$Portfolio = Import-Csv (Join-Path $TableDir "p3_portfolio_composition_config_weighted.csv")
$AcDecision = Import-Csv (Join-Path $TableDir "p3_ac_decision_value.csv")
$AcMargin = Import-Csv (Join-Path $TableDir "p3_ac_margin_diagnostics.csv")
$Sensitivity = Import-Csv (Join-Path $TableDir "p3_sensitivity.csv")
$AcSummary = @($Spec.archived_ac_summary)
$Configs = @($Spec.configuration_contract)

# Figure 2: configuration-specific effects.
$Cv=New-Canvas 2400 1280;$G=$Cv.Graphics
Draw-Text $G "Configuration-specific CARS-MODE relative effects (%)" 1200 55 42 $INK "Center" $true
$Series=@(
    [pscustomobject]@{Suffix="legacy_effect_pct";Label="Sampled/clipped HV";Color=$BLUE;Shape="circle"},
    [pscustomobject]@{Suffix="analytic_ref105_effect_pct";Label="Analytic HV, r=1.05";Color=$ORANGE;Shape="square"},
    [pscustomobject]@{Suffix="igd_plus_effect_pct";Label="Common-reference IGD+";Color=$TEAL;Shape="triangle"}
)
$All=@();foreach($Prefix in @("vs_nsga2_repair","vs_fixedde")){foreach($S in $Series){foreach($R in $Effects){$All += [double]$R.("${Prefix}_$($S.Suffix)")}}}
$Bound=[Math]::Max(5,[Math]::Ceiling((($All|ForEach-Object{[Math]::Abs($_)}|Measure-Object -Maximum).Maximum)/5)*5)
$Panels=@([pscustomobject]@{X0=170;X1=1130;Title="vs NSGA-II+Repair";Prefix="vs_nsga2_repair"},[pscustomobject]@{X0=1370;X1=2330;Title="vs FixedDE joint control";Prefix="vs_fixedde"})
foreach($P in $Panels){$Y0=155;$Y1=1000;Draw-Axes $G $P.X0 $Y0 $P.X1 $Y1 (-$Bound) $Bound "";Draw-Text $G $P.Title (($P.X0+$P.X1)/2) 115 31 $INK "Center" $true
    $Zero=$Y1-(0+$Bound)/(2*$Bound)*($Y1-$Y0);Draw-Line $G $INK 4 $P.X0 $Zero $P.X1 $Zero
    foreach($S in $Series){$Prev=$null;for($i=0;$i-lt$Configs.Count;$i++){$X=$P.X0+($P.X1-$P.X0)*($i+.5)/$Configs.Count;$V=[double]$Effects[$i].("$($P.Prefix)_$($S.Suffix)");$Y=$Y1-($V+$Bound)/(2*$Bound)*($Y1-$Y0);if($null-ne$Prev){Draw-Line $G $S.Color 6 $Prev.X $Prev.Y $X $Y};Draw-Marker $G $X $Y $S.Color $S.Shape;$Prev=[pscustomobject]@{X=$X;Y=$Y}}
    }
    for($i=0;$i-lt$Configs.Count;$i++){$X=$P.X0+($P.X1-$P.X0)*($i+.5)/$Configs.Count;Draw-Text $G $Configs[$i].short_label $X 1045 21 $INK "Center"}
}
$LX=560;foreach($S in $Series){Draw-Marker $G $LX 1135 $S.Color $S.Shape;Draw-Text $G $S.Label ($LX+25) 1135 25 $INK "Near";$LX+=500}
Draw-Text $G "Positive values favor CARS-MODE. Base pools two 30-run seed blocks and remains one configuration." 1200 1225 26 $INK "Center"
Save-Canvas $Cv "fig_configuration_effects.png"

# Figure 3: configuration-equal ablation summary.
$Methods=@("CARS-MODE","Ablation-FixedDE","Ablation-NoDER","Ablation-NoRepair","Ablation-NoDiversity");$Labels=@("CARS-MODE","FixedDE","NoDER (problem variant)","NoRepair","NoDiversity")
$Vals=@();foreach($M in $Methods){$Vals += [double](($Leaderboard|Where-Object method -eq $M).mean_legacy_hv_sampled_clip_ref110)};$Cols=@($BLUE,$ORANGE,$GRAY,$GRAY,$GRAY)
$Cv=New-Canvas 2100 1180;$G=$Cv.Graphics;Draw-Text $G "Configuration-equal sampled/clipped hypervolume" 1050 55 40 $INK "Center" $true
Draw-HBars $G 520 150 1920 920 $Labels $Vals $Cols 0 .05 "Mean hypervolume across six configurations" "0.00000"
$Delta=100*($Vals[1]-$Vals[0])/$Vals[0];Draw-Text $G ("FixedDE is nominally {0:0.00}% above CARS-MODE; the joint adaptation effect remains unresolved." -f $Delta) 1050 1055 28 $INK "Center"
Save-Canvas $Cv "fig_ablation.png"

# Figure 4: archived AC rates.
$AcSorted=@($AcSummary|Sort-Object {[double]$_.ac_feasible_rate} -Descending);$Cv=New-Canvas 2300 1550;$G=$Cv.Graphics;Draw-Text $G "Archived composition-level AC diagnostic" 1150 55 42 $INK "Center" $true
$X0=520;$Y0=140;$X1=2160;$Y1=1310;$Row=($Y1-$Y0)/$AcSorted.Count
for($i=0;$i-lt$AcSorted.Count;$i++){$R=$AcSorted[$i];$YC=$Y0+$Row*($i+.5);$Label=if($R.method-eq"NoPlan"){"No-Plan"}else{$R.method};Draw-Text $G $Label ($X0-20) $YC 22 $INK "Far";$Col=if($R.method-eq"CARS-MODE"){$BLUE}elseif($R.method-eq"Ablation-FixedDE"){$ORANGE}else{$GRAY};$A=[double]$R.ac_feasible_rate;$S=[double]$R.stress_ac_feasible_rate;Fill-Rect $G $Col $X0 ($YC-24) ($A*($X1-$X0)) 20;Fill-Rect $G $LIGHT $X0 ($YC+4) ($S*($X1-$X0)) 20 $Col}
foreach($T in @(0,.2,.4,.6,.8,1.0)){$X=$X0+$T*($X1-$X0);Draw-Line $G $LIGHT 2 $X $Y0 $X $Y1;Draw-Text $G ($T.ToString("0.0")) $X ($Y1+30) 23 $INK "Center"};$XR=$X0+.5*($X1-$X0);Draw-Line $G $INK 4 $XR $Y0 $XR $Y1
Draw-Text $G "AC-feasible fraction of 72 dependent fixed cases" (($X0+$X1)/2) ($Y1+88) 27 $INK "Center";Draw-Text $G "Solid: all cases; outlined: stress-only. Fractions are descriptive, not optimizer-seed feasibility probabilities." 1150 1470 25 $INK "Center";Save-Canvas $Cv "fig_ac_validation.png"

# Figure 5: sensitivity summary.
$Cv=New-Canvas 2200 1160;$G=$Cv.Graphics;Draw-Text $G "Exploratory sampled/clipped HV sensitivity" 1100 55 42 $INK "Center" $true
$Axes=@([pscustomobject]@{Name="population_size";Title="Population size";X0=160},[pscustomobject]@{Name="tau";Title="Resampling probability";X0=1240})
foreach($A in $Axes){$Sub=@($Sensitivity|Where-Object axis -eq $A.Name);$X0=$A.X0;$Y0=160;$X1=$X0+900;$Y1=900;Draw-Axes $G $X0 $Y0 $X1 $Y1 0 .05 "";Draw-Text $G $A.Title ($X0+450) 115 31 $INK "Center" $true;for($i=0;$i-lt$Sub.Count;$i++){$R=$Sub[$i];$XC=$X0+150+$i*280;$CM=[double]$R.cars_mean;$NM=[double]$R.nsga_reference;$SD=[double]$R.cars_std;$YC=$Y1-$CM/.05*($Y1-$Y0);$YN=$Y1-$NM/.05*($Y1-$Y0);Fill-Rect $G $BLUE ($XC-70) $YC 62 ($Y1-$YC);Fill-Rect $G $GRAY ($XC+8) $YN 62 ($Y1-$YN);$E=$SD/.05*($Y1-$Y0);Draw-Line $G $INK 3 ($XC-39) ($YC-$E) ($XC-39) ($YC+$E);Draw-Text $G $R.label $XC ($Y1+30) 22 $INK "Center"}}
Fill-Rect $G $BLUE 700 1020 28 28;Draw-Text $G "CARS-MODE mean +/- SD" 742 1034 25 $INK "Near";Fill-Rect $G $GRAY 1270 1020 28 28;Draw-Text $G "Matched NSGA-II mean" 1312 1034 25 $INK "Near";Save-Canvas $Cv "fig_sensitivity.png"

# Figure 6: all-seed compromise composition, equal configuration weight.
$PM=@("CARS-MODE","Ablation-FixedDE","NSGA-II","Standard DE");$Acts=@([pscustomobject]@{N="reinforcement";L="Reinforcement";C=$BLUE},[pscustomobject]@{N="storage";L="Storage";C=$ORANGE},[pscustomobject]@{N="der";L="DER";C=$TEAL},[pscustomobject]@{N="automation";L="Automation";C=$GRAY})
$Cv=New-Canvas 2200 1180;$G=$Cv.Graphics;Draw-Text $G "Mean action counts in configuration-equal compromise summaries" 1100 55 42 $INK "Center" $true;$X0=180;$Y0=150;$X1=2080;$Y1=920;Draw-Axes $G $X0 $Y0 $X1 $Y1 0 8 "";$BW=52
for($i=0;$i-lt$PM.Count;$i++){$R=$Portfolio|Where-Object method -eq $PM[$i];$XC=$X0+($X1-$X0)*($i+.5)/$PM.Count;for($j=0;$j-lt$Acts.Count;$j++){$V=[double]$R.($Acts[$j].N);$Y=$Y1-$V/8*($Y1-$Y0);Fill-Rect $G $Acts[$j].C ($XC+($j-1.5)*$BW-$BW*.4) $Y ($BW*.8) ($Y1-$Y)};Draw-Text $G ($PM[$i]-replace"Ablation-","") $XC ($Y1+32) 23 $INK "Center"}
$LX=500;foreach($A in $Acts){Fill-Rect $G $A.C $LX 1030 28 28;Draw-Text $G $A.L ($LX+40) 1044 24 $INK "Near";$LX+=350};Draw-Text $G "All rerun seed compromises; these are not the three run-index-0 compositions in the archived AC panel." 1100 1135 24 $INK "Center";Save-Canvas $Cv "fig_portfolio_composition.png"

# Figure 7: paired decision-screening diagnostic.
$AD=@($AcDecision|Sort-Object {[double]$_.net_feasible_case_change} -Descending);$L=@();$V1=@();$V2=@();$Co=@();foreach($R in $AD){$L+=($R.method-replace"Ablation-","");$V1+=[double]$R.net_feasible_case_change;$V2+=[double]$R.median_paired_max_loading_delta_pct_point;$Co+=if($R.method-eq"CARS-MODE"){$BLUE}elseif($R.method-eq"Ablation-FixedDE"){$ORANGE}else{$GRAY}}
$Cv=New-Canvas 2500 1530;$G=$Cv.Graphics;Draw-Text $G "Decision-screening signals relative to the same No-Plan cases" 1250 55 42 $INK "Center" $true;Draw-Text $G "Net AC-feasible case change" 650 120 31 $INK "Center" $true;Draw-HBars $G 430 175 1190 1280 $L $V1 $Co -2 15 "Cases (11 methods x 72 dependent rows)" "0";Draw-Text $G "Median maximum-loading change" 1900 120 31 $INK "Center" $true;Draw-HBars $G 1690 175 2450 1280 $L $V2 $Co -36 5 "Percentage points vs No-Plan" "0.0";Draw-Text $G "Negative loading change is favorable. These summaries diagnose mapped compositions; they do not certify physical feasibility." 1250 1440 25 $INK "Center";Save-Canvas $Cv "fig_decision_value.png"

# Figure 8: AC line-loading summaries.
$AM=@($AcMargin|Sort-Object {[double]$_.median_max_line_loading_pct});$Cv=New-Canvas 2250 1500;$G=$Cv.Graphics;Draw-Text $G "Archived maximum line-loading distribution summaries" 1125 55 42 $INK "Center" $true;$X0=480;$Y0=140;$X1=2100;$Y1=1280;$Row=($Y1-$Y0)/$AM.Count
for($i=0;$i-lt$AM.Count;$i++){$R=$AM[$i];$YC=$Y0+$Row*($i+.5);$Lab=($R.method-replace"Ablation-","")-replace"NoPlan","No-Plan";Draw-Text $G $Lab ($X0-18) $YC 22 $INK "Far";$Med=[double]$R.median_max_line_loading_pct;$P95=[double]$R.p95_max_line_loading_pct;$Col=if($R.method-eq"CARS-MODE"){$BLUE}elseif($R.method-eq"Ablation-FixedDE"){$ORANGE}else{$GRAY};$XM=$X0+$Med/170*($X1-$X0);$XP=$X0+$P95/170*($X1-$X0);Draw-Line $G $Col 7 $XM $YC $XP $YC;Draw-Marker $G $XM $YC $Col "circle";Draw-Marker $G $XP $YC $WHITE "square"}
foreach($T in @(0,50,100,150)){$X=$X0+$T/170*($X1-$X0);Draw-Line $G $LIGHT 2 $X $Y0 $X $Y1;Draw-Text $G ([string]$T) $X ($Y1+28) 23 $INK "Center"};$X100=$X0+100/170*($X1-$X0);Draw-Line $G $RED 4 $X100 $Y0 $X100 $Y1;Draw-Text $G "Maximum line loading (%)" (($X0+$X1)/2) ($Y1+85) 27 $INK "Center";Draw-Text $G "Filled circle: median; open square: 95th percentile; red line: 100% thermal criterion." 1125 1425 25 $INK "Center";Save-Canvas $Cv "fig_ac_margin_distribution.png"

# Figure 9: direct DE controls over six configurations.
$DM=@([pscustomobject]@{N="CARS-MODE";C=$BLUE;S="circle"},[pscustomobject]@{N="GDE3";C=$ORANGE;S="square"},[pscustomobject]@{N="NSDE";C=$TEAL;S="triangle"});$Cv=New-Canvas 2200 1180;$G=$Cv.Graphics;Draw-Text $G "Sampled/clipped HV for direct DE controls by configuration" 1100 55 42 $INK "Center" $true;$X0=180;$Y0=150;$X1=2070;$Y1=900;Draw-Axes $G $X0 $Y0 $X1 $Y1 .03 .052 ""
foreach($M in $DM){$Prev=$null;for($i=0;$i-lt$Configs.Count;$i++){$CID=$Configs[$i].configuration_id;$R=$ConfigMeans|Where-Object{$_.configuration_id-eq$CID-and$_.method-eq$M.N};$V=[double]$R.mean_legacy_hv_sampled_clip_ref110;$X=$X0+($X1-$X0)*($i+.5)/$Configs.Count;$Y=$Y1-($V-.03)/(.052-.03)*($Y1-$Y0);if($null-ne$Prev){Draw-Line $G $M.C 6 $Prev.X $Prev.Y $X $Y};Draw-Marker $G $X $Y $M.C $M.S;$Prev=[pscustomobject]@{X=$X;Y=$Y}}}
for($i=0;$i-lt$Configs.Count;$i++){$X=$X0+($X1-$X0)*($i+.5)/$Configs.Count;Draw-Text $G $Configs[$i].short_label $X ($Y1+32) 23 $INK "Center"};$LX=650;foreach($M in $DM){Draw-Marker $G $LX 1050 $M.C $M.S;Draw-Text $G $M.N ($LX+24) 1050 26 $INK "Near";$LX+=420};Draw-Text $G "The base point pools the primary and replicate seed blocks; the plot contains six configurations." 1100 1135 24 $INK "Center";Save-Canvas $Cv "fig_direct_de_controls.png"

Write-Output "OK: regenerated P3 S4 figures from $ManifestPath"
