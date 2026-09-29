"""Bounded arithmetic and artifact checks for advisory review; no new experiments."""
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
DATA = PROJECT / "03_Reproducibility" / "Data"
TEX = PROJECT / "01_Manuscript" / "LaTeX"
CCF = Path("D:/aicoding/mylib/Paper_CCF")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def close(a, b):
    return math.isclose(float(a), float(b), abs_tol=1e-12)


def main():
    source = TEX / "paper_information.tex"
    assert sha(source) == "bcee5e325d140dbf949d3012c12644e876b46f8f4a71c7eeb1b7b783735cf95b"
    summary = rows(DATA / "evaluator_audit/run_unified_v1b/unified_evaluator_summary.csv")
    checks = []
    tests = []
    for r in summary:
        n, correct = int(r["n"]), int(r["correct"])
        gain, harm = int(r["rescues"]), int(r["harms"])
        checks.append(close(r["accuracy"], correct / n))
        checks.append(correct - 76 == gain - harm)
        checks.append(close(r["paired_accuracy_difference"], (gain - harm) / n))
        if r["holm_adjusted_p_nine_comparisons"]:
            discordant = gain + harm
            p = min(1.0, 2 * sum(math.comb(discordant, k) for k in range(min(gain, harm) + 1)) / 2**discordant)
            checks.append(close(p, r["exact_discordant_sign_p"]))
            tests.append((p, float(r["holm_adjusted_p_nine_comparisons"])))
    previous = 0.0
    for i, (p, reported) in enumerate(sorted(tests)):
        adjusted = min(1.0, max(previous, (len(tests) - i) * p))
        checks.append(close(adjusted, reported))
        previous = adjusted
    errors = rows(DATA / "error_taxonomy/unified_v1/method_error_counts.csv")
    for r in errors:
        checks.append(sum(int(r[k]) for k in r if k not in ("method", "n")) == int(r["n"]))
    ablations = rows(DATA / "role_ablation/unified_v1/ablation_results.csv")
    parent_counts = {r["variant"]: int(r["correct"]) for r in ablations}
    for r in ablations:
        if r["parent"]:
            delta = int(r["correct"]) - parent_counts[r["parent"]]
            checks.append(delta == int(r["gains_vs_parent"]) - int(r["losses_vs_parent"]))
    # Confirm the export adds Information without silently changing other venues.
    old = json.loads(subprocess.check_output(["git", "-C", str(CCF), "show", "HEAD:Paper_CCF/data/venues.json"]))
    new = json.loads((CCF / "data/venues.json").read_text(encoding="utf-8"))
    old_map = {j["slug"]: j for j in old["journals"]}
    new_map = {j["slug"]: j for j in new["journals"]}
    checks.append(all(new_map[k] == v for k, v in old_map.items()))
    checks.append(old["conferences"] == new["conferences"])
    info = new_map["mdpi-information"]
    checks.append(info["paper_reviews"]["decision_threshold"] is None)
    checks.append(info["acceptance_probability"] is None)
    checks.append("SCIE" not in info["indexing"])
    report = {
        "scope": "Advisory-review arithmetic; no raw SQL/model rerun, confidence-interval reconstruction or independent peer review",
        "manuscript_sha256": sha(source),
        "pdf_sha256": sha(TEX / "paper_information.pdf"),
        "profile_version": info["calibration_version"],
        "profile_sha256": sha(CCF / "journals/mdpi-information/SKILL.md"),
        "calibration_reference_sha256": sha(CCF / "journals/mdpi-information/references/standards-and-evidence.md"),
        "unified_summary_rows": len(summary), "exact_sign_tests": len(tests),
        "checks": len(checks), "all_checks_pass": all(checks),
        "interpretation": "Correct arithmetic does not establish exchangeability, independence, external validity or acceptance readiness",
        "derived_descriptives": {
            "top_tie_fraction": 130 / 180,
            "complete_witness_vs_best_fixed_percentage_points": 100 * (100 - 129) / 180,
            "order_span_percentage_points": 100 * (128 - 95) / 180,
            "complete_vs_validation_percentage_points": 100 / 180,
        },
        "unrelated_export_records_unchanged": all(new_map[k] == v for k, v in old_map.items()) and old["conferences"] == new["conferences"],
    }
    (ROOT / "ASSESSMENT_CHECKS.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert all(checks)


if __name__ == "__main__":
    main()
