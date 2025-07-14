"""A module with simple (for now) DataFrame functionality."""

from collections import defaultdict
from datetime import datetime


class DataFrame:
    """Column-based data frame."""

    def __init__(self, column_definitions):
        """Validate input structure and initialize the data frame."""
        self._validate_input_type(column_definitions)
        for column in column_definitions.values():
            self.is_valid_column(column)
        self.column_definitions = column_definitions

    @classmethod
    def from_rows(cls, rows):
        """Create a DataFrame object from an iterable consisting of rows."""
        column_definitions = defaultdict(list)
        for row in rows:
            for column, value in row.items():
                column_definitions[column].append(value)
        return cls(column_definitions)

    def is_valid_column(self, column):
        """Verify if a column has members of the same type."""
        item_type = type(column[0])
        for item in column[1:]:
            if not isinstance(item, item_type):
                raise TypeError("Inconsistent column types.")
        return True

    def _validate_input_type(self, column_definitions):
        if not isinstance(column_definitions, dict):
            raise TypeError("Cannot instantiate with anything different then a dictionary.")

    @property
    def shape(self):
        """Size of the DataFrame (rows, cows)."""
        len_rows = max(len(row) for row in self.column_definitions.values())
        len_cols = len(self.column_definitions)
        return len_rows, len_cols

    def __getitem__(self, column_name):
        """Allow for indexing by column name."""
        return self.column_definitions[column_name]

    def __setitem__(self, name, value):
        """Allow for setting of a whole column."""
        self.is_valid_column(value)
        self.column_definitions[name] = value

    def __str__(self):
        """Represent DataFrame as a string with it's size and contents."""
        table = PrettyTable()
        table.field_names = self.column_definitions.keys()
        table.add_rows(row for row in zip(*self.column_definitions.values()))
        return f"DataFrame (2x3)\n{table!s}"

    def __bool__(self):
        """Evaluate truthiness of the DataFrame, depending on whether or not it's empty."""
        return bool(self.column_definitions)


df = DataFrame({"date": [1, 2, 3, 4]})


def validate_column_types(**column_restrictions):
    """Decorate a function to check if columns with a certain name have a specific content type."""

    def decorator(func):
        def decorated(df, **kwargs):
            if not isinstance(df, DataFrame):
                raise TypeError(f"Object {df} is not a DataFrame.")
            for column, column_type in column_restrictions.items():
                if not isinstance(df[column][0], column_type):
                    raise TypeError(f"Type for column {column} must be {column_type}.")
            return func(df, **kwargs)

        return decorated

    return decorator


@validate_column_types(date=datetime)
def extract_time_interval(df):
    """Extract the interval from the earliest to the latest date in a DataFrame."""
    dates = sorted(df["date"])
    return dates[-1] - dates[0]


def require_non_empty(func):
    """Decorate a function to require a DataFrame with size > (0, 0)."""

    def decorated(df, **kwargs):
        if not isinstance(df, DataFrame):
            raise TypeError(f"Object {df} is not a DataFrame.")
        if not df:
            raise TypeError(f"Empty DataFrame not allowed for {func.__name__}.")
        return func(df, **kwargs)

    return decorated


@require_non_empty
def avg(df, /, column_name):
    """Find the average value for a specific column."""
    column = df[column_name]
    return sum(column) / len(column)