import unittest
from drift import compare


class DriftTests(unittest.TestCase):
    def test_finds_missing_key(self):
        report = compare({"A": "1"}, {})
        self.assertEqual(report["drift"][0]["kind"], "missing")

    def test_hides_sensitive_values(self):
        report = compare({"TOKEN": "one"}, {"TOKEN": "two"}, sensitive=["TOKEN"])
        finding = report["drift"][0]
        self.assertIn("left_fingerprint", finding)
        self.assertNotIn("one", str(finding))

    def test_allows_declared_difference(self):
        report = compare({"REGION": "a"}, {"REGION": "b"}, allowed=["REGION"])
        self.assertTrue(report["healthy"])
        self.assertEqual(report["score"], 100)


if __name__ == "__main__":
    unittest.main()
