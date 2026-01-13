import unittest

from logscope.config import schema


class SchemaValidationTest(unittest.TestCase):
    def test_validate_row_success(self):
        row = {"pattern": "ERROR"}
        schema.validate_row(row)

    def test_validate_row_missing_field_raises(self):
        row = {"owner": "team-a"}
        with self.assertRaises(ValueError):
            schema.validate_row(row)

    def test_validate_row_empty_field_raises(self):
        row = {"pattern": ""}
        with self.assertRaises(ValueError):
            schema.validate_row(row)

    def test_validate_row_whitespace_field_raises(self):
        row = {"pattern": "   "}
        with self.assertRaises(ValueError):
            schema.validate_row(row)


if __name__ == "__main__":
    unittest.main()
