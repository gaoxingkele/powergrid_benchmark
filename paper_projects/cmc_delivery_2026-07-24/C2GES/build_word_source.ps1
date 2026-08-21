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
$abstract = $abstract.Replace("\cges{}", "C\textsuperscript{2}GES")
$abstract = $abstract.Replace("\cges", "C\textsuperscript{2}GES")

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
$body = $body.Replace("\cges{}", "C\textsuperscript{2}GES")
$body = $body.Replace("\cges", "C\textsuperscript{2}GES")
$body = $body.Replace("\linksupplementary{}", "the journal submission system")
$body = [regex]::Replace(
    $body,
    "\\path\{([^}]*)\}",
    { param($m) "\texttt{" + $m.Groups[1].Value + "}" }
)
$body = [regex]::Replace(
    $body,
    "\\begin\{tabularx\}\{\\textwidth\}\{([^}]*)\}",
    {
        param($m)
        $columns = ($m.Groups[1].Value -replace "\s+", "") -replace "L", "l"
        return "\begin{tabular}{" + $columns + "}"
    }
)
$body = $body.Replace("\end{tabularx}", "\end{tabular}")

$algorithmReplacement = @'
\textbf{Algorithm 1: C\textsuperscript{2}GES evidence sentence reranking}

\textbf{Input:} Document sentences $D=\{s_1,\ldots,s_n\}$, question $q$, role $r$, budget $K$, and weights $\theta=(w_q,w_r,w_g)$.

\begin{enumerate}
\item For each sentence $s_j \in D$, compute query relevance $Q_j=Q(s_j,q)$ and role compatibility $R_j=R(s_j,r)$.
\item If $r$ is propagation/response or mitigation, compute chain consistency $G_j=G(s_j,D,r)$; otherwise set $G_j=0$.
\item Compute the combined score $S_j=w_qQ_j+w_rR_j+w_gG_j$.
\item Sort sentence IDs by descending $S_j$, using document order to break ties.
\item Return the top-$K$ sentence IDs.
\end{enumerate}
'@
$body = [regex]::Replace(
    $body,
    "(?s)\\vspace\{4pt\}\s*\\noindent\\rule\{\\textwidth\}\{0\.8pt\}.*?\\noindent\\rule\{\\textwidth\}\{0\.8pt\}\s*\\vspace\{4pt\}",
    [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $algorithmReplacement }
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
\newcommand{\adot}{.}
\title{$title}
\author{Bijing Liu and Yong Yang}
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
