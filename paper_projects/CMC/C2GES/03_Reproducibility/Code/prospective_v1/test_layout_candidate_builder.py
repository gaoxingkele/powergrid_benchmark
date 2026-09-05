import unittest

from layout_candidate_builder import (
    bbox_overlap_fraction,
    classify_unit,
    join_lines,
    normalize_match,
    split_block,
)


class LayoutCandidateBuilderTests(unittest.TestCase):
    def test_overlap_fraction_uses_left_area(self):
        self.assertAlmostEqual(bbox_overlap_fraction((0, 0, 10, 10), (5, 0, 15, 10)), 0.5)

    def test_line_join_repairs_lowercase_hyphenation(self):
        self.assertEqual(join_lines(["inter-", "ruption occurred."]), "interruption occurred.")

    def test_unit_types(self):
        self.assertEqual(classify_unit("Figure 2. Event sequence", 10, 10, False, 0.2), "caption")
        self.assertEqual(classify_unit("• Inspect relay settings", 10, 10, False, 0.2), "list_item")
        self.assertEqual(classify_unit("Recommended Actions", 10, 13, True, 0.2), "heading")
        self.assertEqual(classify_unit("ordinary body sentence.", 10, 10, False, 0.2), "body")

    def test_body_split_only(self):
        self.assertEqual(split_block("First event. Second event.", "body"), ["First event.", "Second event."])
        self.assertEqual(split_block("First event. Second event.", "caption"), ["First event. Second event."])

    def test_normalize_match_is_stable(self):
        self.assertEqual(normalize_match("Grid—Event  12"), "grid event 12")


if __name__ == "__main__":
    unittest.main()
