param(
    [Parameter(Mandatory = $true)]
    [string]$SourceTex,
    [Parameter(Mandatory = $true)]
    [string]$OutputTex
)

$text = Get-Content -LiteralPath $SourceTex -Raw -Encoding UTF8

function Get-SingleLineMacro([string]$name) {
    $pattern = "(?m)^\\" + [regex]::Escape($name) + "\{(.*)\}\s*$"
    $match = [regex]::Match($text, $pattern)
    if (-not $match.Success) {
        throw "Required macro not found: $name"
    }
    return $match.Groups[1].Value
}

$title = Get-SingleLineMacro "Title"
$abstract = Get-SingleLineMacro "abstract"
$keywords = Get-SingleLineMacro "keyword"

$bodyStart = $text.IndexOf("\section{Introduction}")
if ($bodyStart -lt 0) {
    throw "Introduction section not found"
}
$body = $text.Substring($bodyStart)
$body = [regex]::Replace($body, "(?m)^\\reftitle\{References\}\s*$", "")
$body = [regex]::Replace($body, "(?m)^\\end\{document\}\s*$", "")
$body = $body.Replace("\tablesize{\scriptsize}", "")
$body = $body.Replace("\tablesize{\footnotesize}", "")
$body = $body.Replace("\tablesize{\small}", "")
$body = $body.Replace("\begin{adjustbox}{max width=\textwidth}", "")
$body = $body.Replace("\end{adjustbox}", "")
$body = $body.Replace("\begin{enumerate}[label=(\arabic*)]", "\begin{enumerate}")
$body = $body.Replace("\linksupplementary{}", "the journal submission system")
$body = [regex]::Replace(
    $body,
    "\\path\{([^}]*)\}",
    { param($m) "\texttt{" + $m.Groups[1].Value + "}" }
)

$declarations = [ordered]@{
    "acknowledgement" = "Acknowledgement"
    "funding" = "Funding Statement"
    "authorcontributions" = "Author Contributions"
    "availabilityofdataandmaterials" = "Availability of Data and Materials"
    "ethicsapproval" = "Ethics Approval"
    "conflictsofinterest" = "Conflicts of Interest"
    "supplementary" = "Supplementary Materials"
}

foreach ($entry in $declarations.GetEnumerator()) {
    $pattern = "(?m)^\\" + [regex]::Escape($entry.Key) + "\{(.*)\}\s*$"
    $heading = $entry.Value
    $body = [regex]::Replace(
        $body,
        $pattern,
        {
            param($m)
            return "\section*{" + $heading + "}`r`n`r`n" + $m.Groups[1].Value
        }
    )
}

$clean = @"
\documentclass{article}
\usepackage{amsmath,amssymb,booktabs,graphicx,hyperref}
\title{$title}
\author{Bijing Liu, Chenglong Sun, and Yong Yang}
\date{}
\begin{document}
\maketitle

\begin{center}
NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China

Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China

Corresponding author: Yong Yang (yangyong1@sgepri.sgcc.com.cn)
\end{center}

\begin{abstract}
$abstract
\end{abstract}

\textbf{Keywords:} $keywords

$body

\end{document}
"@

[System.IO.File]::WriteAllText($OutputTex, $clean, [System.Text.UTF8Encoding]::new($false))
