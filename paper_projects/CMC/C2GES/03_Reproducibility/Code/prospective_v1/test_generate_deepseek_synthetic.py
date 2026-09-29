from __future__ import annotations

import random
import unittest

from generate_deepseek_synthetic import CORE_ROLES, causal_graph_is_acyclic, contains_real_marker, expand_report, select_reference, validate_core, validate_dataset, words


class DeepSeekSyntheticGeneratorTests(unittest.TestCase):
    def core(self) -> dict:
        units = []
        for role in CORE_ROLES:
            for index in range(4):
                units.append({"text": f"Synthetic station records {role.replace('_', ' ')} evidence number {index} under controlled fictional operating conditions today.",
                              "role": role, "causal_predecessors": [], "summary_priority": 2 if index == 0 else 1})
        distractors = [f"Synthetic auxiliary subsystem background statement {i} remains unrelated to the fictional incident outcome." for i in range(24)]
        return {"reports": [{"title": "Synthetic A", "core_units": units, "distractor_seeds": distractors},
                            {"title": "Synthetic B", "core_units": units, "distractor_seeds": distractors}]}

    def profile(self) -> dict:
        return {"page_count": 20, "candidate_count": 80, "reference_words": 140,
                "units_over_256_tokens": 1, "body": 55, "heading": 5,
                "list_item": 10, "table_unit": 7, "caption": 2, "footnote": 1}

    def test_validates_compact_core_and_builds_reference_locally(self) -> None:
        core = validate_core(self.core(), require_distractor_seeds=True)[0]
        selected = select_reference(core["core_units"])
        self.assertTrue(110 <= words(" ".join(core["core_units"][i]["text"] for i in selected)) <= 180)

    def test_expansion_matches_target_count_and_is_extractive(self) -> None:
        core = validate_core(self.core(), require_distractor_seeds=True)[0]
        row = expand_report(core, self.profile(), "d1", "s1", "explicit", "fictional test", random.Random(7))
        self.assertEqual(len(row["candidate_sentences"]), 80)
        self.assertEqual(validate_dataset([row])["reports"], 1)
        distractors = [unit["text"] for unit in row["candidate_sentences"]
                       if unit["synthetic_ground_truth_role"] == "distractor"]
        self.assertEqual(len(distractors), len(set(distractors)))

    def test_long_report_expansion_keeps_exact_duplicates_below_gate(self) -> None:
        core = validate_core(self.core(), require_distractor_seeds=True)[0]
        profile = {**self.profile(), "page_count": 472, "candidate_count": 11230}
        row = expand_report(core, profile, "long-d1", "long-s1", "ambiguous",
                            "fictional long-document test", random.Random(11))
        texts = [unit["text"].casefold() for unit in row["candidate_sentences"]]
        exact_duplicate_rate = 1 - len(set(texts)) / len(texts)
        self.assertLessEqual(exact_duplicate_rate, .20)

    def test_rejects_real_organization_marker(self) -> None:
        value = self.core()
        value["reports"][0]["core_units"][0]["text"] = "NERC issued this entirely fictional statement with enough additional words for schema validation today."
        with self.assertRaisesRegex(ValueError, "real-entity"):
            validate_core(value)

    def test_denylist_uses_token_boundaries(self) -> None:
        self.assertFalse(contains_real_marker("A misoperation occurred in a fictional controller."))
        self.assertTrue(contains_real_marker("The fictional text improperly names MISO here."))

    def test_causal_graph_allows_future_document_reference_but_rejects_cycle(self) -> None:
        value = self.core()
        value["reports"][0]["core_units"][0]["causal_predecessors"] = [1]
        validated = validate_core(value, require_distractor_seeds=True)
        self.assertTrue(causal_graph_is_acyclic(validated[0]["core_units"]))
        value["reports"][0]["core_units"][1]["causal_predecessors"] = [0]
        with self.assertRaisesRegex(ValueError, "cycle"):
            validate_core(value, require_distractor_seeds=True)


if __name__ == "__main__":
    unittest.main()
