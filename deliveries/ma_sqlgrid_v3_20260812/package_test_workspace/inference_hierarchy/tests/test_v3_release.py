import csv, hashlib, json, subprocess, sys, unittest
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[3]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def csvrows(name):
    with (HERE/"tables"/name).open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))

class V3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.r=json.loads((HERE/"V3_INFERENCE_HIERARCHY.json").read_text(encoding="utf-8"))
    def test_pass_and_no_model(self):
        self.assertTrue(self.r["passed"]); self.assertTrue(self.r["no_model_execution"]); self.assertFalse(self.r["v2_modified"])
    def test_expected_hash_contract_live(self):
        c=json.loads((HERE/"EXPECTED_INPUT_HASHES.json").read_text(encoding="utf-8"))
        for section in ["v2_accepted_upstream_inputs","v2_products_consumed"]:
            for rel,expected in c[section].items(): self.assertEqual(sha(ROOT/rel),expected,rel)
        p=subprocess.run([sys.executable,str(HERE/"verify_inputs.py")],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr); self.assertIn("PASS: 18",p.stdout)
    def test_two_disjoint_nine_test_families(self):
        rr=csvrows("core_inference_hierarchy.csv"); fam=Counter(x["family"] for x in rr)
        self.assertEqual(len(rr),18); self.assertEqual(sorted(fam.values()),[9,9])
        self.assertEqual({x["metric"] for x in rr if x["family"].startswith("primary")},{"execution"})
    def test_cluster_randomization_and_holm(self):
        for r in csvrows("core_inference_hierarchy.csv"):
            self.assertEqual(int(r["randomization_draws"]),100000); self.assertEqual(int(r["clusters"]),70)
            self.assertGreaterEqual(float(r["p_holm"])+1e-15,float(r["p_raw"])); self.assertGreater(float(r["p_raw"]),0)
    def test_exact_known_effects(self):
        rr=csvrows("core_inference_hierarchy.csv")
        def get(m,s,e): return next(x for x in rr if x["metric"]==m and x["scope"]==s and x["effect"]==e)
        self.assertAlmostEqual(float(get("execution","qwen","structural_hint_main")["estimate"]),.23055555555555557)
        self.assertAlmostEqual(float(get("execution","granite_minus_qwen","backbone_x_interaction")["estimate"]),.18888888888888888)
        self.assertAlmostEqual(float(get("structural_common","granite","structural_hint_main")["estimate"]),.35555555555555557)
    def test_composition_sensitivity_is_not_ci(self):
        rr=csvrows("composition_sensitivity.csv"); self.assertEqual(len(rr),36)
        self.assertEqual(Counter(x["grouping"] for x in rr),{"normalized_sql_70":18,"difficulty_x_feature_39":18})
        self.assertTrue(all("not sampled" in x["interpretation"] for x in rr))
    def test_cluster_and_target_counts(self):
        p=csvrows("dependence_group_profile.csv"); a=next(x for x in p if x["grouping"]=="normalized_sql_70"); b=next(x for x in p if x["grouping"]=="difficulty_x_feature_39")
        self.assertEqual((int(a["groups"]),int(a["singletons"])),(70,58)); self.assertEqual(int(b["groups"]),39); self.assertIn("not authoring",b["rule"])
        targets={int(x["projected_columns"]):int(x["questions"]) for x in csvrows("frozen_target_distribution.csv")}; self.assertEqual(targets,{1:61,2:31,3:57,4:31})
    def test_manual_qa_not_generator_authored(self):
        qa=json.loads((HERE/"MANUAL_VISUAL_QA.json").read_text(encoding="utf-8")); self.assertIn(qa["status"],["pending_manual_inspection","pass","pass_with_minor_accessibility_issue","fail"])
        src=(HERE/"build_v3_inference.py").read_text(encoding="utf-8"); self.assertNotIn('(HERE/"MANUAL_VISUAL_QA.json").write',src)
    def test_manifest_hashes(self):
        m=json.loads((HERE/"release_manifest.json").read_text(encoding="utf-8")); self.assertEqual(m["input_contract_sha256"],sha(HERE/"EXPECTED_INPUT_HASHES.json"))
        for rel,meta in m["outputs"].items(): self.assertEqual(sha(HERE/rel),meta["sha256"],rel)

if __name__=="__main__": unittest.main()
