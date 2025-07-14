"""Tests for the dataframe module."""

import unittest

from main import DataFrame, require_non_empty


class TestDataframe(unittest.TestCase):
    """Test the DataFrame class."""

    def setUp(self):
        """Create a DataFrame object to be used for testing."""
        self.df = DataFrame({"name": ["Гошо", "Пешо"], "age": [30, 16]})

    def test_initialize_with_anything_other_than_a_dict(self):
        """Initialization of DataFrames with non-dictionaries should raise a ValueError."""
        with self.assertRaises(ValueError):
            DataFrame([("name", "age"), (["Гошо", "Пешо"], [30, 16])])

    def test_shape(self):
        """DataFrame.shape should reflect the size of the data frame."""
        self.assertEqual(self.df.shape, (2, 2))

    def test_getitem(self):
        """DataFrame["column"] should return the whole column with the given name."""
        self.assertEqual(self.df["age"], [30, 16])

    def test_setitem(self):
        """DataFrame["column"] = [...] should replace the whole column with the new one."""
        height = [175, 212]
        self.df["height"] = height
        self.assertEqual(self.df.shape, (2, 3))
        self.assertEqual(self.df["height"], height)

    def test_setitem_invalid(self):
        """Attempting to set an invalid column should result in a TypeError."""
        height = [175, "по-висок от Стан"]
        with self.assertRaises(TypeError) as err:
            self.df["height"] = height
        self.assertEqual(str(err.exception), "Inconsistent column types.")

    def test_print(self):
        """str(DataFrame) should represent the DataFrame with it's size and contents."""
        df = DataFrame({"name": ["Гошо", "Пешо"], "age": [30, 16], "height": [175, 196]})
        expected_string = """DataFrame (2x3)
+------+-----+--------+
| name | age | height |
+------+-----+--------+
| Гошо |  30 |  175   |
| Пешо |  16 |  196   |
+------+-----+--------+"""
        self.assertEqual(str(df), expected_string)

    def test_initialize_inconsistent_column_types(self):
        """Initializing a DataFrame with columns with inconsistent types should result in a TypeError."""
        with self.assertRaises(TypeError):
            DataFrame({"name": [16, "Пешо"], "age": [30, 16]})

    @unittest.skip(reason="Not yet implemented")
    def test_initialize_invalid_column_length(self):
        """Initializing with a column with invalid length should result in a ValueError."""
        with self.assertRaises(ValueError):
            DataFrame({"name": ["Гошо"], "age": [30, 16]})

    def test_from_rows(self):
        """DataFrame.from_rows should create a new DataFrame object from a list of rows."""
        rows = [
            {"name": "Гошо", "age": 30, "height": 175},
            {"name": "Пешо", "age": 16, "height": 196},
        ]
        df = DataFrame.from_rows(rows)
        self.assertIsInstance(df, DataFrame)


class TestValidators(unittest.TestCase):
    """Test the validators (and top-level functions of the dataframe module)."""

    def test_require_non_empty(self):
        """The decorated function's behavior should be preserved when the input is a non-empty DataFrame."""

        def dummy_func(*_, **__):
            return None

        decorated = require_non_empty(dummy_func)
        result = decorated(DataFrame({"number": [1, 2]}), column_name="number")
        self.assertEqual(result, None)

    def test_require_non_empty_empty(self):
        """The decorated function should raise an exception when the input is an empty DataFrame."""

        # TODO: Update with a check if dummy_func was called  # noqa: TD002, TD003, FIX002
        def dummy_func(*_, **__):
            return None

        decorated = require_non_empty(dummy_func)
        with self.assertRaises(TypeError) as err:
            decorated(DataFrame({}), column_name="number")
        self.assertEqual(
            str(err.exception),
            f"Empty DataFrame not allowed for {dummy_func.__name__}.",
        )


if __name__ == "__main__":
    unittest.main()