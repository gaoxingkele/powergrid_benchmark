"""Regenerate all four manuscript figures from packaged, rights-safe sources.

The generator is clean-unpack portable: it resolves every input relative to the
manuscript directory and never reads the parent workspace.  Scientific counts
and plotted values are parsed from packaged JSON/CSV files rather than embedded
in drawing code.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TRANSFER = ROOT / "supplementary" / "transferable"
INPUTS = {
    "formal_config": TRANSFER / "formal_protocol" / "formal_config_v0_3_1.json",
    "rights_inventory": TRANSFER / "rights_safe_metadata" / "rights_safe_report_metadata.json",
    "aggregate_metrics": TRANSFER / "audits" / "aggregate_metrics.json",
    "paired_differences": TRANSFER / "figure_inputs" / "paired_rougel_differences_nonverbatim.csv",
    "manuscript": ROOT / "paper_applsci.tex",
}
EXPECTED_IMMUTABLE = {
    "formal_config": "C924035295F837B4F94D18D06DED12EC36135628A44345F1F568F9D5582AF14C",
    "rights_inventory": "3E6286D04F95CE99B9E258138E1C40CBF9C9A97D03C42315AA6F6014D6CB12D6",
    "aggregate_metrics": "DF9D9E4EF21BE0BDEC401C27D732D6A2692980FA8C018B119E41D85EE22149AA",
    "paired_differences": "AAE5F9E565AFB0FE98830673BC62A1A714227B86FCE5AF46DFA0723784FA1303",
}
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIXED_TIME = datetime(2026, 8, 8, tzinfo=timezone.utc)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


for name, expected in EXPECTED_IMMUTABLE.items():
    got = digest(INPUTS[name])
    if got != expected:
        raise RuntimeError(f"input hash mismatch for {name}: {got}")

CONFIG = json.loads(INPUTS["formal_config"].read_text(encoding="utf-8"))
INVENTORY = json.loads(INPUTS["rights_inventory"].read_text(encoding="utf-8"))
AGGREGATE = json.loads(INPUTS["aggregate_metrics"].read_text(encoding="utf-8"))
with INPUTS["paired_differences"].open(encoding="utf-8", newline="") as stream:
    PAIRED = list(csv.DictReader(stream))
MANUSCRIPT_TEXT = INPUTS["manuscript"].read_text(encoding="utf-8")

if CONFIG["selection_budgets"] != [5, 10] or len(CONFIG["c2ges_full_weights"]) != 5:
    raise RuntimeError("formal configuration invariant failed")
if len(PAIRED) != 90:
    raise RuntimeError("paired rights-safe input must contain 90 rows")
if "\\label{fig:algorithm}" not in MANUSCRIPT_TEXT or "\\label{fig:data-flow}" not in MANUSCRIPT_TEXT:
    raise RuntimeError("manuscript figure anchors missing")

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)
COLORS = ["#0077BB", "#EE7733", "#009988", "#CC3311", "#33BBEE", "#BBBBBB", "#000000"]


def save(fig, stem: str) -> None:
    fig.savefig(
        OUT / f"{stem}.pdf",
        metadata={"Creator": "C2GES code-native figure generator", "CreationDate": FIXED_TIME, "ModDate": FIXED_TIME},
    )
    fig.savefig(OUT / f"{stem}.png", dpi=300, metadata={"Software": "C2GES code-native figure generator"})
    plt.close(fig)


def architecture() -> None:
    weights = CONFIG["c2ges_full_weights"]
    labels = {
        "relevance": f"Centroid Q\nweight {weights['relevance']:.2f}",
        "role": f"Role R\nweight {weights['role']:.2f}",
        "graph": f"Degree G\nweight {weights['graph']:.2f}",
        "counterfactual": f"Deletion C\nweight {weights['counterfactual']:.2f}\nno-CF: 0",
        "position": f"Position P\nweight {weights['position']:.2f}",
    }
    fig, ax = plt.subplots(figsize=(7.0, 3.55))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    boxes = [
        (0.15, 4.15, 1.55, 0.78, "Full-PDF body\n(summary excluded)"),
        (2.05, 4.15, 1.55, 0.78, "Role evidence\n(lexical proxies)"),
        (3.95, 4.15, 1.55, 0.78, "Typed directed\nproxy graph"),
        (5.85, 4.15, 1.70, 0.78, f"{CONFIG['path_min_edges']}--{CONFIG['path_max_edges']}-edge path\nutility"),
        (7.90, 4.15, 1.85, 0.78, "Node-deletion\nscore C"),
        (0.25, 2.05, 1.40, 0.72, labels["relevance"]),
        (2.00, 2.05, 1.40, 0.72, labels["role"]),
        (3.75, 2.05, 1.40, 0.72, labels["graph"]),
        (5.50, 2.05, 1.40, 0.72, labels["counterfactual"]),
        (7.25, 2.05, 1.40, 0.72, labels["position"]),
        (4.20, 0.78, 2.10, 0.72, "Weighted combination\nEq. (3)"),
        (7.45, 0.78, 2.25, 0.72, f"Redundancy-aware greedy\nselection; K={','.join(map(str, CONFIG['selection_budgets']))}"),
    ]
    for index, (x, y, width, height, label) in enumerate(boxes):
        color = "#E8F1F8" if index < 5 else "#F4F4F4"
        ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=.03", fc=color, ec="#2F4858", lw=1.1))
        ax.text(x + width / 2, y + height / 2, label, ha="center", va="center", fontsize=7.7)
    for start, end in [
        ((1.70, 4.54), (2.05, 4.54)), ((3.60, 4.54), (3.95, 4.54)),
        ((5.50, 4.54), (5.85, 4.54)), ((7.55, 4.54), (7.90, 4.54)),
        ((0.95, 4.15), (0.95, 2.77)), ((2.78, 4.15), (2.70, 2.77)),
        ((4.72, 4.15), (4.45, 2.77)), ((8.82, 4.15), (6.20, 2.77)),
        ((1.0, 2.05), (4.55, 1.50)), ((2.7, 2.05), (4.75, 1.50)),
        ((4.45, 2.05), (5.00, 1.50)), ((6.20, 2.05), (5.45, 1.50)),
        ((7.95, 2.05), (5.85, 1.50)), ((6.30, 1.14), (7.45, 1.14)),
    ]:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10, lw=1, color="#555555"))
    ax.text(5, 0.20, "Five channels enter in parallel. Roles, edges, and deletion are textual proxies; no physical causal effect is identified.", ha="center", fontsize=7.7, style="italic")
    save(fig, "fig01_algorithm")


def dataset_flow() -> None:
    inventory_count = len(INVENTORY)
    page_count = sum(int(row["page_count"]) for row in INVENTORY)
    included = [row for row in INVENTORY if row["inclusion_status"] == "included"]
    excluded_count = sum(row["inclusion_status"] == "excluded" for row in INVENTORY)
    candidate_count = sum(int(row["candidate_count"]) for row in included)
    dev_count = sum(row["analysis_split"] == "dev" for row in INVENTORY)
    test_count = sum(row["analysis_split"] == "test" for row in INVENTORY)
    assert (inventory_count, page_count, len(included), excluded_count, candidate_count, dev_count, test_count) == (40, 3200, 27, 13, 12924, 12, 15)
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.2, 4.2)
    labels = [
        (f"{inventory_count}-report inventory\n{page_count:,} declared pages", 0.25),
        (f"{excluded_count} excluded\nreasons in Table S1", 3.0),
        (f"{len(included)} retained\n{candidate_count:,} candidates", 3.0),
        (f"{dev_count} development\n144-config selection", 6.5),
        (f"{test_count} test reports\none corrective run", 6.5),
    ]
    ys = [1.90, 2.80, 1.10, 1.85, 0.40]
    for (label, x), y in zip(labels, ys):
        ax.add_patch(FancyBboxPatch((x, y), 2.0, 0.72, boxstyle="round,pad=.03", fc="#E8F1F8", ec="#2F4858"))
        ax.text(x + 1, y + 0.36, label, ha="center", va="center", fontsize=8)
    # The 40-report inventory branches in parallel into 13 exclusions and 27
    # retained reports; only the retained branch then splits into dev and test.
    for start, end in [
        ((2.25, 2.26), (3.0, 3.16)),
        ((2.25, 2.26), (3.0, 1.46)),
        ((5.0, 1.46), (6.5, 2.21)),
        ((5.0, 1.46), (6.5, 0.76)),
    ]:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10, color="#555555"))
    ax.text(5, -0.05, "Rights-safe Table S1 records genre, pages, reference words, candidates, split, exclusion reason, and permission status.", ha="center", fontsize=7.8)
    save(fig, "fig02_dataset_flow")


def aggregate() -> None:
    order = CONFIG["conditions"]
    names = ["Lead", "Centroid", "TextRank", "Semantic-MMR", "Role", "Graph no-CF", "Full C2GES"]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), sharey=True)
    x = np.arange(len(order))
    for ax, budget in zip(axes, map(str, CONFIG["selection_budgets"])):
        values = [AGGREGATE[budget][method]["rougeL_f1"] for method in order]
        ax.bar(x, values, 0.72, color=COLORS, edgecolor="black", linewidth=0.35)
        ax.set_xticks(x, names, rotation=45, ha="right")
        ax.set_title(f"K = {budget}")
        ax.set_ylim(0, 0.15)
        ax.set_ylabel("Mean ROUGE-L F1")
        ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    save(fig, "fig03_aggregate_rougel")


def paired() -> None:
    labels = {"graph_no_cf_strict": "Graph no-CF", "semantic_mmr": "Semantic-MMR", "textrank": "TextRank"}
    fig, axes = plt.subplots(2, 3, figsize=(7.0, 4.6), sharey=True)
    for row_index, budget in enumerate(CONFIG["selection_budgets"]):
        for column_index, baseline in enumerate(CONFIG["primary_contrasts"]):
            ax = axes[row_index, column_index]
            subset = sorted(
                (row for row in PAIRED if int(row["budget"]) == budget and row["baseline"] == baseline),
                key=lambda row: int(row["rights_safe_report_index"]),
            )
            values = np.array([float(row["full_minus_baseline_rougeL_f1"]) for row in subset])
            if len(values) != 15:
                raise RuntimeError(f"paired cell {budget}/{baseline} has {len(values)} rows")
            ax.axhline(0, color="black", lw=0.8)
            ax.scatter(np.arange(1, 16), values, color=COLORS[column_index], s=15, alpha=0.85)
            ax.plot([0.5, 15.5], [values.mean(), values.mean()], color=COLORS[column_index], lw=1.8)
            signs = (int((values > 0).sum()), int((values < 0).sum()), int((values == 0).sum()))
            ax.set_title(f"K={budget}: Full - {labels[baseline]}\n+/-/0 = {signs[0]}/{signs[1]}/{signs[2]}", fontsize=8)
            ax.set_xlim(0.5, 15.5)
            ax.set_xticks([1, 5, 10, 15])
            ax.set_xlabel("Rights-safe report index")
            if column_index == 0:
                ax.set_ylabel("Paired ROUGE-L difference")
    fig.tight_layout()
    save(fig, "fig04_paired_differences")


architecture()
dataset_flow()
aggregate()
paired()

script_hash = digest(Path(__file__))
input_hashes = {name: digest(path) for name, path in INPUTS.items()}
specifications = {
    "fig01_algorithm": {
        "manuscript_id": "Figure 2 / label fig:algorithm",
        "caption_claim_anchor": "Materials and Methods, Typed Path Counterfactual Sensitivity and Scoring and Selection",
        "input_names": ["formal_config", "manuscript"],
        "function": "architecture",
        "supported_claim": "parallel Q/R/G/C/P score channels, registered weights, 2--4-edge paths and strict no-CF switch",
        "limitation": "conceptual rendering of deterministic text-processing code; not a physical causal graph",
    },
    "fig02_dataset_flow": {
        "manuscript_id": "Figure 1 / label fig:data-flow",
        "caption_claim_anchor": "Materials and Methods, Source PDFs, Inclusion, and Leakage Gates",
        "input_names": ["rights_inventory"],
        "function": "dataset_flow",
        "supported_claim": "40 to 27 to 12/15 sampling flow, 3,200 pages and 12,924 candidates",
        "limitation": "rights-safe metadata only; source prose and PDFs are excluded",
    },
    "fig03_aggregate_rougel": {
        "manuscript_id": "Figure 3 / label fig:aggregate",
        "caption_claim_anchor": "Results, Aggregate Test Results",
        "input_names": ["formal_config", "aggregate_metrics"],
        "function": "aggregate",
        "supported_claim": "descriptive macro-mean ROUGE-L for seven conditions at K=5 and K=10",
        "limitation": "equal-sentence, not equal-word, budgets; bars omit paired uncertainty",
    },
    "fig04_paired_differences": {
        "manuscript_id": "Figure 4 / label fig:paired",
        "caption_claim_anchor": "Results, Paired Directions and Exact Post-Run Sensitivity",
        "input_names": ["formal_config", "paired_differences"],
        "function": "paired",
        "supported_claim": "all 90 rights-safe paired differences and six sign-count labels",
        "limitation": "non-verbatim report indices replace titles; inferential assumptions remain as stated in the manuscript",
    },
}
artifacts = {}
for stem, spec in specifications.items():
    outputs = {}
    for suffix in ("pdf", "png"):
        path = OUT / f"{stem}.{suffix}"
        outputs[suffix] = {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)}
    artifacts[stem] = {
        **spec,
        "inputs": [
            {"name": name, "path": INPUTS[name].relative_to(ROOT).as_posix(), "sha256": input_hashes[name]}
            for name in spec["input_names"]
        ],
        "script": {"path": Path(__file__).relative_to(ROOT).as_posix(), "function": spec["function"], "sha256": script_hash},
        "outputs": outputs,
    }
lineage = {
    "schema": "c2ges-figure-lineage-v2",
    "status": "PASS",
    "clean_unpack_portable": True,
    "workspace_parent_access": False,
    "artifacts": artifacts,
}
(OUT / "FIGURE_LINEAGE.json").write_text(json.dumps(lineage, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "figures": len(artifacts), "script_sha256": script_hash}, indent=2))
