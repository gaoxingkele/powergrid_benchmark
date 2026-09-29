import copy
import unittest

from index_deconstruction import OUT, case_record, validate_inventory


class InventoryTests(unittest.TestCase):
    def absent(self):
        return {"tables": [], "table_inventory_status": {
            "status": "source_reviewed_absent", "count": 0, "pages": [1, 2],
            "evidence": [{"source_sha256": "abc", "locator": {"physical_pages": [1, 2]}}]}}

    def test_source_bound_zero_is_allowed(self):
        validate_inventory(self.absent(), "tables", 2, "abc")

    def test_missing_or_unreviewed_not_zero(self):
        for data in ({}, {"tables": None}, {"tables": []}):
            with self.assertRaises(ValueError):
                validate_inventory(data, "tables", 2, "abc")

    def test_wrong_hash_partial_pages_and_wrong_count_rejected(self):
        for key, value in (("pages", [1]), ("count", 1), ("count", False),
                           ("status", "not_assessed")):
            data = copy.deepcopy(self.absent())
            data["table_inventory_status"][key] = value
            with self.assertRaises(ValueError):
                validate_inventory(data, "tables", 2, "abc")
        with self.assertRaises(ValueError):
            validate_inventory(self.absent(), "tables", 2, "wrong")

    def test_real_zero_table_case(self):
        case = case_record(OUT / "papers/p_1725337431f8f83f.json")
        self.assertEqual(case["table_records"], 0)
        self.assertEqual(case["source_pages"], 6)
        self.assertFalse(case["all_fields_verified"])


if __name__ == "__main__":
    unittest.main()
