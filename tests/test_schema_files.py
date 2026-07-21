import json
import unittest
from pathlib import Path


class SchemaFileTests(unittest.TestCase):
    def test_schema_files_are_valid_json(self):
        for path in Path("schemas").glob("*.json"):
            data = json.loads(path.read_text())
            self.assertIn("$schema", data)
            self.assertEqual(data.get("type"), "object")


if __name__ == "__main__":
    unittest.main()
