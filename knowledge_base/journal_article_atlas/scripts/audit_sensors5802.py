"""Recompute selected printed-cell comparisons; never a raw-data replication."""
import hashlib
import json
import statistics
from pathlib import Path

PAPERS = Path(__file__).resolve().parents[1] / "deconstruction/v1/papers"
CASE = PAPERS / "p_a1adf441aa349153.json"
CELLS = PAPERS / "p_a1adf441aa349153.printed_values.json"


def audit():
    case = json.loads(CASE.read_text(encoding="utf-8"))
    cells = json.loads(CELLS.read_text(encoding="utf-8"))
    source = Path(case["identity"]["source_path"])
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != cells["source_sha256"] or digest != case["identity"]["source_sha256"]:
        raise ValueError("Source hash mismatch")
    t5 = cells["table5"]
    contrasts = []
    for name, row_a, row_b in zip(t5["query_ids"], t5["nearest"], t5["random"], strict=True):
        for fraction, a, b in zip(t5["fractions"], row_a, row_b, strict=True):
            contrasts.append({"query":name,"fraction":fraction,"nearest":a,"random":b,
                              "nearest_better":a < b,"relative_reduction":1-a/b})
    t6, t7 = cells["table6"], cells["table7"]
    return {"paper_id":case["paper_id"],"source_sha256":digest,
            "printed_values_sha256":hashlib.sha256(CELLS.read_bytes()).hexdigest(),
            "not_raw_data_replication":True,"human_calibrated":False,
            "table3_equal_query_mean":statistics.mean(cells["table3"]["values"]),
            "table3_prose_mean":cells["table3"]["prose_mean"],
            "table5_contrasts":contrasts,
            "table5_wins":sum(x["nearest_better"] for x in contrasts),
            "table5_mean_relative_reduction":statistics.mean(x["relative_reduction"] for x in contrasts),
            "table5_ratio_of_means_reduction":1-statistics.mean(x["nearest"] for x in contrasts)/statistics.mean(x["random"] for x in contrasts),
            "table6_all_random_metrics_improve":all(a < b for metric in ("mape","rmse") for a,b in zip(t6[f"random_{metric}_after"],t6[f"random_{metric}_before"],strict=True)),
            "table7_rmse_worsens":t7["nearest_rmse_after"] > t7["nearest_rmse_before"],
            "table7_mape_improves":t7["nearest_mape_after"] < t7["nearest_mape_before"],
            "interpretation":"No p-values or population effects inferred. Unreported weighting or unrounded raw data can differ; source implementation remains unverified."}


if __name__ == "__main__":
    result = audit()
    CASE.with_name(CASE.stem + ".numeric_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "table5_contrasts"},ensure_ascii=False))
