$ErrorActionPreference = 'Stop'

$WorkspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

function New-AppliedSciencesManuscript {
    param(
        [Parameter(Mandatory)] [string] $SourceTex,
        [Parameter(Mandatory)] [string] $SourceBib,
        [Parameter(Mandatory)] [string] $SourceDefinitions,
        [Parameter(Mandatory)] [string] $Destination,
        [Parameter(Mandatory)] [string] $Header,
        [Parameter(Mandatory)] [string] $BackMatter,
        [string] $Charts
    )

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $Destination 'Definitions') | Out-Null
    Copy-Item -LiteralPath (Join-Path $SourceDefinitions 'mdpi.cls') -Destination (Join-Path $Destination 'Definitions\mdpi.cls') -Force
    Copy-Item -LiteralPath (Join-Path $SourceDefinitions 'mdpi.bst') -Destination (Join-Path $Destination 'Definitions\mdpi.bst') -Force
    Copy-Item -LiteralPath (Join-Path $SourceDefinitions 'journalnames.tex') -Destination (Join-Path $Destination 'Definitions\journalnames.tex') -Force
    Copy-Item -LiteralPath (Join-Path $SourceDefinitions 'logo-mdpi.eps') -Destination (Join-Path $Destination 'Definitions\logo-mdpi.eps') -Force
    Copy-Item -LiteralPath (Join-Path $SourceDefinitions 'logo-orcid.pdf') -Destination (Join-Path $Destination 'Definitions\logo-orcid.pdf') -Force
    $DestinationBib = Join-Path $Destination 'references_applsci.bib'
    Copy-Item -LiteralPath $SourceBib -Destination $DestinationBib -Force
    $BibText = [System.IO.File]::ReadAllText($DestinationBib, [System.Text.Encoding]::UTF8)
    $BibText = $BibText.Replace('@webpage{', '@misc{')
    [System.IO.File]::WriteAllText($DestinationBib, $BibText, (New-Object System.Text.UTF8Encoding($false)))

    if ($Charts -and (Test-Path -LiteralPath $Charts)) {
        New-Item -ItemType Directory -Force -Path (Join-Path $Destination 'charts') | Out-Null
        Copy-Item -Path (Join-Path $Charts '*') -Destination (Join-Path $Destination 'charts') -Recurse -Force
    }

    $Source = [System.IO.File]::ReadAllText($SourceTex, [System.Text.Encoding]::UTF8)
    $BodyStart = $Source.IndexOf('\section{Introduction}')
    $BodyEnd = $Source.IndexOf('\acknowledgement{')
    if ($BodyStart -lt 0 -or $BodyEnd -le $BodyStart) {
        throw "Could not identify manuscript body in $SourceTex"
    }
    $Body = $Source.Substring($BodyStart, $BodyEnd - $BodyStart).TrimEnd()
    $Body = $Body.Replace('\begin{table*}', '\begin{table}').Replace('\end{table*}', '\end{table}')
    $Body = $Body.Replace('\begin{figure*}', '\begin{figure}').Replace('\end{figure*}', '\end{figure}')
    $Body = $Body.Replace('\tablesize', '\small')
    if ($SourceTex -match 'ma_sqlgrid') {
        $Body = $Body.Replace('\section{Method}', '\section{Materials and Methods}')
        $Body = $Body.Replace('\section{Experimental Setup}', '\section{Experimental Design}')
        $Body = $Body.Replace('\section{Results and Discussion}', '\section{Results}')
        $Body = $Body.Replace('\subsection{Discussion}\label{sect:r6}', '\section{Discussion}\label{sect:r6}')
        $Body = $Body.Replace('\section{Conclusions and Limitations}', '\section{Conclusions}')
        $Body = $Body.Replace(
            'Borov\v{c}ak et al.~\cite{borovcak2026evaluating} evaluated open-source LLM agents for SQL generation and structured analytics on relational databases in this journal,',
            'Borov\v{c}ak et al.~\cite{borovcak2026evaluating} evaluated open-source LLM agents for SQL generation and structured analytics on relational databases in \emph{Computers, Materials \& Continua},'
        )
    }
    if ($SourceTex -match 'c2ges') {
        $Body = $Body.Replace('\section{Task and Benchmark}', '\section{Materials and Data}')
        $Body = $Body.Replace('\section{Method}', '\section{Methods}')
        $Body = $Body.Replace('\section{Experiments and Discussion}', '\section{Results}')
        $Body = $Body.Replace('\subsection{Discussion}', '\section{Discussion}')
        $Body = $Body.Replace('\section{Conclusions, Limitations, and Future Work}', '\section{Conclusions}')
        $Body = $Body.Replace('($400$ resamples)', '($2{,}000$ resamples)')
        $Body = $Body.Replace(
            'the bootstrap difference is significant ($p=0.005$). Gains over TF-IDF, SBERT, query-only, and lexicon cues are also significant ($p<0.001$). The BM25 comparison is not significant.',
            'the 2{,}000-resample bootstrap difference is significant (95\% CI $[0.0020,0.0177]$, $p=0.012$). Gains over TF-IDF, SBERT, query-only, and lexicon cues are also significant. The BM25 comparison is not significant.'
        )
        $Body = $Body.Replace('vs TF-IDF & $+0.0234$ & $[0.0137,0.0336]$ & $<0.001$', 'vs TF-IDF & $+0.0229$ & $[0.0135,0.0327]$ & $<0.001$')
        $Body = $Body.Replace('vs SBERT & $+0.0250$ & $[0.0150,0.0346]$ & $<0.001$', 'vs SBERT & $+0.0247$ & $[0.0156,0.0344]$ & $<0.001$')
        $Body = $Body.Replace('vs query-only & $+0.0133$ & $[0.0055,0.0216]$ & $<0.001$', 'vs query-only & $+0.0130$ & $[0.0051,0.0210]$ & $0.001$')
        $Body = $Body.Replace('vs no-role & $+0.0103$ & $[0.0027,0.0187]$ & $0.005$', 'vs no-role & $+0.0099$ & $[0.0020,0.0177]$ & $0.012$')
        $Body = $Body.Replace('vs LexCue & $+0.0653$ & $[0.0522,0.0790]$ & $<0.001$', 'vs LexCue & $+0.0651$ & $[0.0522,0.0790]$ & $<0.001$')
        $Body = $Body.Replace('vs BM25 & $+0.0041$ & $[-0.0049,0.0128]$ & $0.365$', 'vs BM25 & $+0.0036$ & $[-0.0055,0.0126]$ & $0.451$')
        $Sensitivity = @'
\subsection{Evidence-Budget Sensitivity}
Table~\ref{tab:k-sensitivity} varies the returned-sentence budget without retraining. The role-conditioned gain over the no-role ablation is supported at $K=3$ and $K=5$, but its confidence interval crosses zero at $K=1$ and $K=10$. C2GES remains statistically tied with BM25 throughout; BM25 has the higher point estimate at $K=1$. Thus, the learned role contribution is useful over moderate evidence budgets rather than uniformly dominant.

\begin{table}[!ht]
\centering
\caption{Evidence-budget sensitivity on the frozen FEVER test split}
\label{tab:k-sensitivity}
\begin{tabular}{cccccc}
\toprule
$K$ & C2GES F1 & BM25 F1 & No-role F1 & $\Delta$ vs BM25 & $\Delta$ vs no-role \\
\midrule
1 & 0.7069 & 0.7173 & 0.6957 & $-0.0109$ & $+0.0115$ \\
3 & 0.5066 & 0.5030 & 0.4967 & $+0.0034$ & $+0.0097$ \\
5 & 0.4230 & 0.4222 & 0.4176 & $+0.0007$ & $+0.0053$ \\
10 & 0.3646 & 0.3638 & 0.3642 & $+0.0008$ & $+0.0005$ \\
\bottomrule
\end{tabular}
\end{table}

'@
        $Body = $Body.Replace('\subsection{Ablations and Interpretation}', $Sensitivity + '\subsection{Ablations and Interpretation}')
    }

    $Output = $Header.TrimEnd() + "`r`n`r`n" + $Body + "`r`n`r`n" + $BackMatter.TrimStart()
    [System.IO.File]::WriteAllText((Join-Path $Destination 'paper_applsci.tex'), $Output, (New-Object System.Text.UTF8Encoding($false)))
}

$TemplateDefinitions = Join-Path $WorkspaceRoot 'paper_projects\CMC\MA-SQLGrid\03_Applied_Sciences_Template\extracted_full\Definitions'

$MaHeader = @'
% MDPI Applied Sciences submission version generated from the latest CMC-era source.
\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}
\firstpage{1}
\makeatletter
\setcounter{page}{\@firstpage}
\makeatother
\pubvolume{1}
\issuenum{1}
\articlenumber{0}
\pubyear{2026}
\copyrightyear{2026}
\datereceived{}
\daterevised{}
\dateaccepted{}
\datepublished{}
\usepackage{adjustbox}

\Title{MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL over Power Grid Maintenance Databases}
\Author{Bijing Liu $^{1,2}$, Chenglong Sun $^{1,2}$ and Yong Yang $^{1,2,}$*}
\AuthorNames{Bijing Liu, Chenglong Sun and Yong Yang}
\address{$^{1}$ \quad NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China; author-email-required@example.com\\
$^{2}$ \quad Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China; author-email-required@example.com}
\corres{Correspondence: yangyong1@sgepri.sgcc.com.cn}

\abstract{Maintenance engineers increasingly need natural-language access to structured asset, inspection, work-order, and outage records, but text-to-SQL models remain sensitive to schema scale, domain literals, and answer-format requirements. MA-SQLGrid is a multi-stage context-grounding pipeline that selects schema and value evidence, normalizes power-grid expressions, infers the answer shape, generates SQL, and performs reference-free execution validation. On the held-out 180-question split of the synthetic GridDB-Maintenance-v2 benchmark, the compact contract-aware condition improves strict execution accuracy over full-schema/value prompting from 0.4389 to 0.7000 with one generator and from 0.3389 to 0.7000 with a second generator. Validation increases the corresponding scores to 0.7278 and 0.7667. Compact prompting reduces measured input tokens by 23.4\% and 74.7\% on the two serving stacks. Projection-tolerant rescoring reverses the compact-versus-full ordering, indicating that much of the strict gain arises from projection and ordering conformance rather than row-content retrieval. Three deterministic repeats show at most 1.1 percentage points of spread, and a tenfold row-scale diagnostic preserves the strict compact-context advantage. The results support the complete pipeline as an auditable interface for the tested synthetic maintenance database; cross-database and fully factorial mechanism claims remain outside the current evidence.}
\keyword{Text-to-SQL; power grid maintenance databases; large language models; schema grounding; answer-shape inference; execution validation}
\featuredapplication{MA-SQLGrid provides a reproducible natural-language query layer for maintenance engineers who need auditable access to equipment, inspection, work-order, and outage records in a fixed relational database.}
\begin{document}
'@

$MaBack = @'
\supplementary{The supplementary material contains prompt templates, dataset characterization, paired comparisons, resource-consumption results, error analyses, and the tenfold scale diagnostic.}
\authorcontributions{Conceptualization, L.B. and Y.Y.; methodology, L.B.; software, L.B.; validation, L.B. and C.S.; formal analysis, L.B. and C.S.; investigation, L.B. and C.S.; resources, Y.Y.; data curation, L.B. and C.S.; writing---original draft preparation, L.B.; writing---review and editing, C.S. and Y.Y.; visualization, L.B.; supervision, Y.Y.; project administration, Y.Y.; funding acquisition, Y.Y. All authors have read and agreed to the published version of the manuscript.}
\funding{This research was funded by the Science and Technology Project of NARI Group Corporation (State Grid Electric Power Research Institute), grant number [AUTHOR INPUT REQUIRED].}
\institutionalreview{Not applicable. This study did not involve humans or animals.}
\informedconsent{Not applicable.}
\dataavailability{The frozen benchmark, database, code, prompts, prediction records, raw traces, evaluation outputs, and analysis scripts are available at \url{https://github.com/gaoxingkele/ma-sqlgrid} (release v0.2.0). The manuscript limits its claims to the artifacts available in that release and identifies the unavailable original client package and v0.1 generator script in the repository documentation.}
\acknowledgments{During the preparation of this manuscript, the authors used OpenAI Codex (GPT-5-based) to assist with drafting, editing, code review, and reproducibility checks. The authors reviewed and edited the output and take full responsibility for the content of this publication. The hosted models evaluated in the experiments are research subjects; their outputs are archived in the released traces.}
\conflictsofinterest{The authors declare no conflicts of interest. The funder had no role in the design of the study; in the collection, analyses, or interpretation of data; in the writing of the manuscript; or in the decision to publish the results.}
\begin{adjustwidth}{-\extralength}{0cm}
\reftitle{References}
\bibliography{references_applsci}
\PublishersNote{}
\end{adjustwidth}
\end{document}
'@

$C2Header = @'
% MDPI Applied Sciences submission version generated from the latest learnable C2GES source.
\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}
\firstpage{1}
\makeatletter
\setcounter{page}{\@firstpage}
\makeatother
\pubvolume{1}
\issuenum{1}
\articlenumber{0}
\pubyear{2026}
\copyrightyear{2026}
\datereceived{}
\daterevised{}
\dateaccepted{}
\datepublished{}
\usepackage{algorithmic}
\newcommand{\cges}{C\textsuperscript{2}GES}
\newcommand{\adot}{.}

\Title{Causal-Role-Aware Extractive Evidence Selection for Power Grid Reliability Reports: An Interpretable Learnable Reranker}
\Author{Bijing Liu $^{1,2}$ and Yong Yang $^{1,2,}$*}
\AuthorNames{Bijing Liu and Yong Yang}
\address{$^{1}$ \quad NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China; author-email-required@example.com\\
$^{2}$ \quad Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China; author-email-required@example.com}
\corres{Correspondence: yangyong1@sgepri.sgcc.com.cn}

\abstract{Power-grid engineers reviewing disturbance and lessons-learned reports need the exact sentences supporting a trigger, impact, or mitigation assessment. This study presents \cges{}, an interpretable evidence reranker that combines frozen query relevance, a learnable role-compatibility head, and local-chain consistency. To avoid circular evaluation on domain cue lexicons, the quantitative study uses a filtered FEVER sentence-selection benchmark with human-annotated evidence: 4000 training, 800 development, and 800 test claim--document instances under SUPPORTS/REFUTES conditioning. At budget $K=3$, \cges{} reaches 0.5066 evidence F1, compared with 0.4837 for TF--IDF, 0.4818 for SBERT, 0.4414 for a lexical role baseline, 0.4937 for the query-only ablation, and 0.4967 without the learned role term. A 2000-resample document-cluster bootstrap confirms the gain over the no-role ablation ($+0.0099$, 95\% CI $[0.0020,0.0177]$, $p=0.012$) and over TF--IDF/SBERT, while the difference from BM25 is not significant. Budget sensitivity shows that the role gain is supported at $K=3$ and $K=5$, but not at $K=1$ or $K=10$. Public NERC excerpts are therefore application cases rather than a gold-label leaderboard. The evidence supports a modest, auditable ranking gain on human-gold data; independent domain-expert annotation is still needed for quantitative NERC validation.}
\keyword{Evidence retrieval; fact verification; role-conditioned reranking; power grid reliability reports; FEVER; interpretable ranking}
\featuredapplication{The method supports auditable review of power-grid disturbance and lessons-learned reports by returning sentence identifiers for role-specific engineering questions such as trigger, impact, and mitigation.}
\begin{document}
'@

$C2Back = @'
\supplementary{The supplementary material documents FEVER conversion, hyperparameters, split statistics, robustness settings, and additional NERC application cases.}
\authorcontributions{Conceptualization, L.B. and Y.Y.; methodology, L.B.; software, L.B.; validation, L.B.; formal analysis, L.B.; investigation, L.B.; resources, Y.Y.; data curation, L.B.; writing---original draft preparation, L.B.; writing---review and editing, L.B. and Y.Y.; visualization, L.B.; supervision, Y.Y.; project administration, Y.Y.; funding acquisition, Y.Y. All authors have read and agreed to the published version of the manuscript.}
\funding{This research was funded by the Science and Technology Project of NARI Group Corporation (State Grid Electric Power Research Institute), grant number [AUTHOR INPUT REQUIRED].}
\institutionalreview{Not applicable. This study did not involve humans or animals; it uses a public human-annotated benchmark and public technical reports.}
\informedconsent{Not applicable.}
\dataavailability{The FEVER conversion scripts, trained checkpoint, and evaluation summary are provided in the project artifact under \path{workspace/fever_benchmark/} and \path{workspace/fever_runs/learnable_role/}. FEVER is publicly available at \url{https://fever.ai/dataset/fever.html}. The NERC documents used for qualitative application cases are publicly available from NERC event-analysis pages. A permanent public repository URL must be inserted before submission.}
\acknowledgments{During the preparation of this manuscript, the authors used large-language-model-based tools to assist with drafting and editing. The authors reviewed and edited the output and take full responsibility for the content of this publication. No AI-simulated labels are presented as human or domain-expert ground truth in the main quantitative evaluation.}
\conflictsofinterest{The authors declare no conflicts of interest. The funder had no role in the design of the study; in the collection, analyses, or interpretation of data; in the writing of the manuscript; or in the decision to publish the results.}
\begin{adjustwidth}{-\extralength}{0cm}
\reftitle{References}
\bibliography{references_applsci}
\PublishersNote{}
\end{adjustwidth}
\end{document}
'@

New-AppliedSciencesManuscript `
    -SourceTex (Join-Path $WorkspaceRoot 'paper_projects\2026_ma_sqlgrid_cmc\source\manuscript_cmc\paper_cmc.tex') `
    -SourceBib (Join-Path $WorkspaceRoot 'paper_projects\2026_ma_sqlgrid_cmc\source\manuscript_cmc\references_cmc.bib') `
    -SourceDefinitions $TemplateDefinitions `
    -Destination (Join-Path $WorkspaceRoot 'paper_projects\CMC\MA-SQLGrid\06_Applied_Sciences_Current') `
    -Header $MaHeader `
    -BackMatter $MaBack `
    -Charts (Join-Path $WorkspaceRoot 'paper_projects\2026_ma_sqlgrid_cmc\source\manuscript_cmc\charts')

New-AppliedSciencesManuscript `
    -SourceTex (Join-Path $WorkspaceRoot 'paper_projects\2026_c2ges_engineeringletters\source\manuscript_cmc\paper_cmc.tex') `
    -SourceBib (Join-Path $WorkspaceRoot 'paper_projects\2026_c2ges_engineeringletters\source\manuscript_cmc\references_cmc.bib') `
    -SourceDefinitions $TemplateDefinitions `
    -Destination (Join-Path $WorkspaceRoot 'paper_projects\CMC\C2GES\06_Applied_Sciences_Current') `
    -Header $C2Header `
    -BackMatter $C2Back

Write-Output 'Built Applied Sciences manuscript sources.'
