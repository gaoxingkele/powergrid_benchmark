"""Index substantive case files without upgrading semantic verification status."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deconstruction/v1"


def validate_inventory(data: dict, name: str, pages: int, digest: str) -> None:
    """An empty inventory needs source-bound absence evidence, not a fake object."""
    if name not in data or data[name] is None:
        raise ValueError(f"Missing substantive inventory {name}")
    if data[name]:
        return
    singular = {"tables": "table", "figures": "figure", "equations": "equation"}.get(name)
    if singular is None or data[name] != []:
        raise ValueError(f"Missing substantive inventory {name}")
    absence = data.get(f"{singular}_inventory_status", {})
    covered = absence.get("pages", [])
    evidence = absence.get("evidence", [])
    if not (absence.get("status") == "source_reviewed_absent"
            and type(absence.get("count")) is int and absence["count"] == 0
            and len(covered) == pages and set(covered) == set(range(1, pages + 1))
            and any(e.get("source_sha256", "").lower() == digest.lower()
                    and set(e.get("locator", {}).get("physical_pages", [])) == set(covered)
                    for e in evidence)):
        raise ValueError(f"Unsubstantiated empty inventory {name}")


def case_record(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    identity = data.get("identity", data.get("source", {}))
    source_value = identity.get("source_path", identity.get("path"))
    if not source_value:
        raise ValueError(f"Missing source: {path.name}")
    source = Path(source_value)
    if not source.is_absolute():
        source = path.parent / source
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    expected = identity.get("source_sha256", identity.get("sha256"))
    if digest.lower() != expected.lower():
        raise ValueError(f"Source mismatch: {path.name}")
    with fitz.open(source) as doc:
        pages = len(doc)
    coverage = data.get("read_coverage", data.get("review", {}))
    read = coverage.get("physical_pages_read", coverage.get("text_pages", coverage.get("text_pages_read", [])))
    if len(set(read)) != len(read) or any(not 1 <= p <= pages for p in read):
        raise ValueError(f"Invalid read coverage: {path.name}")
    human = data.get("human_calibrated", data.get("review", {}).get("human_calibrated"))
    if human is not False:
        raise ValueError(f"Unexpected calibration upgrade: {path.name}")
    for required in ("sections", "equations", "figures", "tables", "experiments", "statistics"):
        validate_inventory(data, required, pages, digest)
    if not path.with_suffix(".md").exists():
        raise ValueError(f"Missing readable case: {path.name}")
    return {"paper_id": data["paper_id"],
            "title": identity.get("title", data.get("title")),
            "venue": identity.get("journal", identity.get("venue", data.get("journal"))),
            "doi": identity.get("doi", data.get("doi")),
            "analyzed_version": identity.get("source_version", identity.get("version", "not_assessed")),
            "formal_layout_metrics_eligible": identity.get("formal_layout_metrics_eligible", None),
            "source_sha256": digest, "source_pages": pages,
            "reported_text_pages_read": len(read), "record_covers_all_text_pages": set(read) == set(range(1, pages + 1)),
            "section_records": len(data["sections"]), "equation_records": len(data["equations"]),
            "figure_records": len(data["figures"]), "table_records": len(data["tables"]),
            "analysis_status": data.get("analysis_status", data.get("status")),
            "human_calibrated": False, "cohort_ready": False,
            "all_fields_verified": False,
            "json": path.relative_to(OUT).as_posix(),
            "markdown": path.with_suffix(".md").relative_to(OUT).as_posix(),
            "independent_review_file": (path.stem + ".independent_review.json") if path.with_name(path.stem + ".independent_review.json").exists() else None,
            "case_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> None:
    cases = [case_record(p) for p in sorted((OUT / "papers").glob("*.json"))
             if re.fullmatch(r"p_[0-9a-f]{16}\.json", p.name)]
    profiles = json.loads((ROOT / "journal_profiles.json").read_text(encoding="utf-8"))
    venues = list(profiles["profiles"]) + ["IEEE PES General Meeting", "IEEE ISGT", "IEEE SmartGridComm"]
    counts = Counter(c["venue"] for c in cases)
    result = {"schema":"atlas_deconstruction_index/1", "cases":cases,
              "venue_progress":[{"venue":v,"substantive_cases":counts[v],"batch_floor":3,
                                  "batch_floor_reached":counts[v]>=3,"all_fields_complete":False} for v in venues],
              "limits":"Counts certify files and source hashes, not semantic correctness. No venue mean, acceptance threshold or human-calibrated profile is released.",
              "original_journal_candidate_target":62,"all_fields_verified_cases":0,
              "goal_complete":False}
    (OUT / "INDEX.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    lines = ["# 全文解构批次索引", "", "本索引是实质分析文件清单，不是全字段验收或期刊校准通过声明。原62篇候选及全部期刊/会议目标保留。", "",
             "| 场所 | 已有实质全文个案 | 首批至少3篇 | 全字段验收 |", "|---|---:|---|---|"]
    lines += [f"| {v} | {counts[v]} | {'数量达到，复核未完成' if counts[v]>=3 else '未达到'} | 未完成 |" for v in venues]
    lines += ["", "## 单篇分析", "", "公式列是对象记录数，含不同计数类别，不能跨论文直接当编号公式总数。会议作者预印本只支持对应版本的方法内容分析，不能代表正式会刊版式；具体版本与版式资格见INDEX.json及单篇文件。", "",
              "| 论文 | 场所 | 原件页数 | 章节对象 | 公式对象 | 图 | 表 |", "|---|---|---:|---:|---:|---:|---:|"]
    lines += [f"| [{c['title']}]({c['markdown']}) | {c['venue']} | {c['source_pages']} | {c['section_records']} | {c['equation_records']} | {c['figure_records']} | {c['table_records']} |" for c in cases]
    lines += ["", "## 尚未完成", "", "逐段语义与词句统计、全对象视觉复核、独立复核、版本/更正检查、统一211字段映射仍有缺项；新增场所样本尚不充分。单助手阅读全文及源文件哈希通过都不等于上述检查全部完成。", ""]
    (OUT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"cases":len(cases),"venues":dict(counts),"pages":sum(c["source_pages"] for c in cases),"source_hashes":"all_match","all_fields_verified":0},ensure_ascii=False))


if __name__ == "__main__":
    main()
