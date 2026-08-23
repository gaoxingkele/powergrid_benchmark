import unittest

from ma_sqlgrid_agents import (
    Adjudicator,
    Blackboard,
    CounterfactualCritic,
    MASQLGridCoordinator,
    SQLCandidate,
    SQLSynthesizer,
    Validator,
)


class CoordinationTests(unittest.TestCase):
    def test_validator_rejects_write_and_multiple_statements(self):
        validator = Validator()
        write = SQLCandidate("C000", "DELETE FROM assets;", "test", 0)
        multiple = SQLCandidate("C001", "SELECT * FROM assets; DROP TABLE assets;", "test", 1)
        self.assertFalse(validator.validate(write, lambda _: {"ok": True}).safe)
        self.assertFalse(validator.validate(multiple, lambda _: {"ok": True}).safe)

    def test_synthesizer_deduplicates_without_reordering(self):
        candidates = SQLSynthesizer().package(["", "SELECT 1", " SELECT 1; ", "SELECT 2;"])
        self.assertEqual([c.sql for c in candidates], ["SELECT 1;", "SELECT 2;"])
        self.assertEqual([c.candidate_id for c in candidates], ["C000", "C001"])

    def test_missing_execution_evidence_causes_abstention(self):
        decision, _ = MASQLGridCoordinator().run(
            question_id="Q1",
            question="Count assets",
            schema={"assets": ["asset_id"]},
            candidate_sql=["SELECT COUNT(*) FROM assets;"],
            executor=None,
        )
        self.assertEqual(decision.status, "abstain")
        self.assertIsNone(decision.selected_sql)

    def test_counterfactual_evidence_breaks_validation_tie(self):
        def execute(sql):
            return {"ok": True, "shape_ok": True, "order_ok": True, "value_hits": 1}

        cf = {
            "C000": [
                {"state_id": "s1", "ok": True, "equivalent": True},
                {"state_id": "s2", "ok": True, "equivalent": False},
            ],
            "C001": [
                {"state_id": "s1", "ok": True, "equivalent": True},
                {"state_id": "s2", "ok": True, "equivalent": True},
            ],
        }
        decision, board = MASQLGridCoordinator().run(
            question_id="Q2",
            question="How many assets are active?",
            schema={"assets": ["asset_id", "status"]},
            candidate_sql=[
                "SELECT COUNT(asset_id) FROM assets;",
                "SELECT COUNT(*) FROM assets WHERE status = 'active';",
            ],
            executor=execute,
            counterfactual_results=cf,
            expected_state_ids=["s1", "s2"],
        )
        self.assertEqual(decision.selected_candidate_id, "C001")
        self.assertTrue(board.audit_digest())
        self.assertEqual([m.sequence for m in board.messages], list(range(len(board.messages))))
        with self.assertRaises(RuntimeError):
            board.post("test", "late_write", {})

    def test_unknown_counterfactual_is_not_counted_as_success(self):
        candidate = SQLCandidate("C000", "SELECT 1;", "test", 0)
        evidence = CounterfactualCritic().review(candidate, [], ["s1"])
        self.assertEqual(evidence.evaluated_states, 0)
        self.assertIsNone(evidence.pass_rate)
        self.assertFalse(evidence.coverage_complete)

    def test_tie_break_preserves_candidate_order(self):
        decision, _ = MASQLGridCoordinator().run(
            question_id="Q3",
            question="List assets",
            schema={"assets": ["asset_id"]},
            candidate_sql=["SELECT asset_id FROM assets;", "SELECT * FROM assets;"],
            executor=lambda _: {"ok": True, "shape_ok": True, "order_ok": True},
        )
        self.assertEqual(decision.selected_candidate_id, "C000")

    def test_required_counterfactual_coverage_fails_closed(self):
        candidates = (
            SQLCandidate("C000", "SELECT 1;", "test", 0),
            SQLCandidate("C001", "SELECT 2;", "test", 1),
        )
        validation = {
            candidate.candidate_id: Validator().validate(
                candidate,
                lambda _: {"ok": True, "shape_ok": True, "order_ok": True},
            )
            for candidate in candidates
        }
        critic = CounterfactualCritic()
        counterfactual = {
            "C000": critic.review(candidates[0], [{"state_id": "s1", "ok": True, "equivalent": True}], [f"s{i}" for i in range(1, 12)]),
            "C001": critic.review(candidates[1], [{"state_id": f"s{i}", "ok": True, "equivalent": i <= 10} for i in range(1, 12)], [f"s{i}" for i in range(1, 12)]),
        }
        decision = Adjudicator().decide(
            candidates,
            validation,
            counterfactual,
            require_counterfactual=True,
            expected_state_count=11,
            minimum_counterfactual_passes=10,
        )
        self.assertEqual(decision.selected_candidate_id, "C001")
        self.assertFalse(decision.scores[0].eligible)
        self.assertTrue(decision.scores[1].eligible)

    def test_required_counterfactual_abstains_when_all_coverage_incomplete(self):
        decision, _ = MASQLGridCoordinator().run(
            question_id="Q-CF",
            question="List assets",
            schema={"assets": ["asset_id"]},
            candidate_sql=["SELECT asset_id FROM assets;"],
            executor=lambda _: {"ok": True, "shape_ok": True, "order_ok": True},
            counterfactual_results={"C000": [{"state_id": "s1", "ok": True, "equivalent": True}]},
            expected_state_ids=["s1", "s2"],
            require_counterfactual=True,
            minimum_counterfactual_passes=1,
        )
        self.assertEqual(decision.status, "abstain")

    def test_validation_only_empty_cf_never_uses_counterfactual_tie_break(self):
        candidates = (
            SQLCandidate("C000", "SELECT 1;", "test", 0),
            SQLCandidate("C001", "SELECT 2;", "test", 1),
        )
        validations = {
            candidate.candidate_id: Validator().validate(
                candidate,
                lambda _: {"ok": True, "shape_ok": True, "order_ok": True},
            )
            for candidate in candidates
        }
        decision = Adjudicator().decide(candidates, validations, {})
        self.assertEqual(decision.selected_candidate_id, "C000")
        self.assertTrue(all(score.counterfactual_total == 0 for score in decision.scores))

    def test_blackboard_digest_is_deterministic(self):
        first = Blackboard("Q4")
        second = Blackboard("Q4")
        for board in (first, second):
            board.post("role", "kind", {"b": 2, "a": 1})
            board.seal()
        self.assertEqual(first.audit_digest(), second.audit_digest())


if __name__ == "__main__":
    unittest.main()
