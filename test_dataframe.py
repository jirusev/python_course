# test_dataframe.py

import unittest

from main import DataFrame


class TestDataFrame(unittest.TestCase):
    def test_init_and_shape(self):
        df = DataFrame({
            "name": ["A", "B", "C"],
            "age": [10, 20, 30]
        })
        self.assertEqual(df.shape, (3, 2))

    def test_get_item(self):
        data = {"x": [1, 2], "y": [3, 4]}
        df = DataFrame(data)
        self.assertListEqual(df["x"], [1, 2])
        self.assertListEqual(df["y"], [3, 4])

    def test_set_item_new_column(self):
        df = DataFrame({"a": [0, 1]})
        df["b"] = [5, 6]
        self.assertEqual(df.shape, (2, 2))
        self.assertListEqual(df["b"], [5, 6])

    def test_set_item_overwrite(self):
        df = DataFrame({"a": [1, 2]})
        df["a"] = [9, 8]
        self.assertListEqual(df["a"], [9, 8])
        self.assertEqual(df.shape, (2, 1))

    def test_str_repr(self):
        df = DataFrame({"col": ["x", "y"]})
        s = str(df)
        self.assertIn("DataFrame (2×1)", s)
        self.assertIn("col", s)
        self.assertIn("x", s)
        self.assertIn("y", s)

    def test_mismatched_length_init(self):
        with self.assertRaises(ValueError):
            DataFrame({
                "a": [1, 2, 3],
                "b": [4, 5]
            })

    def test_mismatched_length_setitem(self):
        df = DataFrame({"a": [1, 2]})
        with self.assertRaises(ValueError):
            df["b"] = [7]  # грешна дължина

    def test_key_error_getitem(self):
        df = DataFrame({"foo": [0]})
        with self.assertRaises(KeyError):
            _ = df["bar"]

if __name__ == "__main__":
    unittest.main()
