import csv
import hashlib
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def read_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def read_csv(name):
    with (HERE / "tables" / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class V2ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((HERE / "V2_REANALYSIS.json").read_text(encoding="utf-8"))
        cls.rows = read_jsonl(HERE / "canonical_rows_v2.jsonl")

    def test_release_passes(self):
        self.assertTrue(self.report["passed"])
        self.assertTrue(all(x["passed"] for x in self.report["checks"]))

    def test_complete_1440_cartesian_rows(self):
        keys={(r["backbone"],r["question_id"],r["condition"]) for r in self.rows}
        self.assertEqual(len(self.rows),1440)
        self.assertEqual(len(keys),1440)
        self.assertEqual(Counter(r["backbone"] for r in self.rows),{"qwen":720,"granite":720})

    def test_one_frozen_target_per_question(self):
        targets=defaultdict(set)
        for r in self.rows: targets[r["question_id"]].add(r["frozen_target_column_count"])
        self.assertEqual(len(targets),180)
        self.assertTrue(all(len(v)==1 for v in targets.values()))

    def test_execution_totals_unchanged(self):
        got=Counter((r["backbone"],r["condition"]) for r in self.rows if r["execution"])
        expected={
            ("qwen","F00_Full_NoShape"):76,("qwen","F01_Full_WithShape"):129,
            ("qwen","F10_Compact_NoShape"):78,("qwen","F11_Compact_WithShape"):108,
            ("granite","F00_Full_NoShape"):77,("granite","F01_Full_WithShape"):100,
            ("granite","F10_Compact_NoShape"):74,("granite","F11_Compact_WithShape"):108}
        self.assertEqual(dict(got),expected)

    def test_corrected_structural_cells(self):
        got=Counter((r["backbone"],r["condition"]) for r in self.rows if r["structural_common"])
        expected={
            ("qwen","F00_Full_NoShape"):94,("qwen","F01_Full_WithShape"):174,
            ("qwen","F10_Compact_NoShape"):106,("qwen","F11_Compact_WithShape"):173,
            ("granite","F00_Full_NoShape"):94,("granite","F01_Full_WithShape"):158,
            ("granite","F10_Compact_NoShape"):102,("granite","F11_Compact_WithShape"):166}
        self.assertEqual(dict(got),expected)

    def test_corrected_shape_main_effects(self):
        rr=self.report["within_backbone_factorial"]
        q=next(x for x in rr if x["backbone"]=="qwen" and x["metric"]=="structural_common" and x["effect"]=="structural_hint_main")
        g=next(x for x in rr if x["backbone"]=="granite" and x["metric"]=="structural_common" and x["effect"]=="structural_hint_main")
        self.assertAlmostEqual(q["estimate"],0.4083333333333333)
        self.assertAlmostEqual(g["estimate"],0.35555555555555557)

    def test_three_disjoint_eight_test_families(self):
        rr=self.report["registered_cluster_randomization"]
        fam=Counter(x["family"] for x in rr)
        self.assertEqual(len(rr),24)
        self.assertEqual(sorted(fam.values()),[8,8,8])

    def test_cluster_randomization_valid(self):
        for r in self.report["registered_cluster_randomization"]:
            self.assertEqual(r["randomization_samples"],100000)
            self.assertGreaterEqual(r["cluster_randomization_p"],0)
            self.assertLessEqual(r["cluster_randomization_p"],1)
            self.assertGreaterEqual(r["cluster_randomization_p_holm"]+1e-15,r["cluster_randomization_p"])

    def test_mcnemar_is_named_descriptive_only(self):
        fields=set(self.report["registered_cluster_randomization"][0])
        self.assertIn("mcnemar_descriptive_p",fields)
        self.assertNotIn("mcnemar_p_holm",fields)

    def test_granite_transcription_fact(self):
        fact=self.report["granite_compact_shape_p_fact"]
        self.assertAlmostEqual(fact["old_question_level_mcnemar_holm"],1.861682221715455e-6)
        self.assertIn("incorrect",fact["manuscript_mistranscription"])

    def test_context_offline_boundary_and_coverage(self):
        c=self.report["context_audit_summary"]
        self.assertIn("offline",c["gold_use"])
        self.assertEqual(c["all_gold_tables_retained"],179)
        self.assertEqual(c["all_gold_columns_retained"],155)
        self.assertEqual(c["multi_table_questions"],116)

    def test_prompt_field_bundle_is_visible(self):
        rr=read_csv("prompt_field_invariance.csv")
        def present(cell,field): return int(next(x for x in rr if x["condition"]==cell and x["field"]==field)["present_questions"])
        self.assertEqual(present("F00_Full_NoShape","global_value_dictionary"),180)
        self.assertEqual(present("F10_Compact_NoShape","normalization_hints"),170)
        self.assertEqual(present("F00_Full_NoShape","normalization_hints"),0)
        self.assertEqual(present("F11_Compact_WithShape","structural_hint"),180)

    def test_figures_have_all_formats(self):
        for stem in ["fig01_v2_cells","fig02_v2_factorial_effects","fig03_context_audit"]:
            for ext in ["pdf","svg","png"]:
                p=HERE/"figures"/f"{stem}.{ext}"
                self.assertTrue(p.is_file())
                self.assertGreater(p.stat().st_size,1000)

    def test_manifest_hashes(self):
        manifest=json.loads((HERE/"release_manifest.json").read_text(encoding="utf-8"))
        for rel,meta in manifest["outputs"].items():
            p=HERE/rel
            self.assertTrue(p.is_file(),rel)
            self.assertEqual(sha(p),meta["sha256"],rel)
            self.assertEqual(p.stat().st_size,meta["bytes"],rel)

    def test_freeze_excludes_quarantined_path(self):
        text=(HERE/"FREEZE_AND_METHOD.json").read_text(encoding="utf-8")
        self.assertNotIn("qwen25coder7b_q4km_seed20260805/",text.replace("\\","/"))
        self.assertIn("clean_rerun1",text)


if __name__ == "__main__":
    unittest.main()
