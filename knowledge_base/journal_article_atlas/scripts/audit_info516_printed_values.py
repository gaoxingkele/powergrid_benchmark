"""Recheck published rounded cells; not a reproduction of forecasting results."""
import calendar
import datetime as dt
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "deconstruction/v1/papers"
ID = "p_654ca5ab287c1e14"


def holm(p_values):
    ordered = sorted(p_values.items(), key=lambda item: item[1])
    adjusted, previous = {}, 0.0
    for rank, (name, value) in enumerate(ordered):
        previous = max(previous, min(1.0, (len(ordered) - rank) * value))
        adjusted[name] = previous
    return adjusted


def audit():
    source = BASE / (ID + ".printed_values.json")
    values = json.loads(source.read_text(encoding="utf8"))
    monthly = values["mape_percent"]
    days = [calendar.monthrange(2010, m)[1] for m in range(1, 13)]
    results = {}
    for model, cells in monthly.items():
        if len(cells) != 12:
            raise ValueError("Exactly twelve monthly cells required")
        mean = statistics.mean(cells)
        reported = values["reported_average"][model]
        results[model] = {"equal_month_mean":mean,
                          "calendar_day_weighted_mean":sum(a*b for a,b in zip(cells,days))/sum(days),
                          "reported_mean":reported,
                          "reported_minus_equal_month_mean":reported-mean,
                          "exceeds_two_stage_2decimal_rounding_allowance":abs(reported-mean)>.010000001}
    split = values["split"]
    start, train_end, test_start, end = [dt.datetime.fromisoformat(split[k]) for k in ("start","train_end","test_start","end")]
    step = dt.timedelta(minutes=split["step_minutes"])
    adj = holm(values["wilcoxon_reported_p"])
    return {"paper_id":ID, "input_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
            "source_sha256":values["source_sha256"], "kind":"post-publication printed-cell arithmetic audit",
            "not_raw_data_replication":True, "monthly_results":results,
            "split_arithmetic":{"assumption":"Contiguous naive local 30-minute timestamps; no DST or missing-row adjustment",
                                "implied_train_rows":int((train_end-start)/step)+1,
                                "implied_test_rows":int((end-test_start)/step)+1,
                                "reported_train_rows":split["reported_train"],
                                "reported_test_rows":split["reported_test"],
                                "end_of_reported_train_count":(start+(split["reported_train"]-1)*step).isoformat()},
            "posthoc_holm_sensitivity":{"family":"Six published paired comparisons, considered together for this audit only",
                                         "adjusted_p":adj,"below_005":[name for name,p in adj.items() if p<.05],
                                         "boundary":"Conditional on original p-values being valid; not evidence the signed-rank pairing or temporal assumptions were correct; not claimed as author-prespecified analysis"}}


if __name__ == "__main__":
    result = audit()
    (BASE/(ID+".numeric_audit.json")).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
