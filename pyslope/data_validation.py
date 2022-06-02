"""Module to aid with data validation"""


def assert_integer(n, name):
    """Assert that an input is an integer."""
    if not isinstance(n, int):
        raise ValueError(
            f"The value for '{name}' should be an integer, not a {type(n)}."
        )


def assert_positive_number(n, name):
    """Assert that an input is a positive number."""
    if not isinstance(n, (int, float)):
        raise ValueError(
            f"The value for '{name}' should be an integer or a float, not a {type(n)}."
        )
    if n < 0:
        raise ValueError(f"The value for '{name}' should be >= 0, not {n}")


def assert_strictly_positive_number(n, name):
    """Assert that an input is a strictly positive number."""
    if not isinstance(n, (int, float)):
        raise ValueError(
            f"The value for '{name}' should be an integer or a float, not a {type(n)}."
        )
    if n < 0:
        raise ValueError(f"The value for '{name}' should be > 0, not {n}")


def assert_number(n, name):
    """Assert that an input is a number."""
    if type(n) not in [int, float]:
        raise ValueError(
            f"The value for '{name}' should be an integer or a float, not a {type(n)}."
        )


def assert_range(n, name, low, high, not_low=False, not_high=False):
    """Assert that an input is a number in a specified range."""
    if not isinstance(n, (int, float)):
        raise ValueError(
            f"The value for '{name}' should be an integer or a float, not a {type(n)}."
        )
    if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
        raise ValueError(
            f"The value for the ranges low and high should be an integer or a float"
            f" not a {type(low)} and {type(high)}."
        )
    if n < low:
        raise ValueError(
            f"The value for '{name}' should be greater than {low}, not {n}."
        )
    if n > high:
        raise ValueError(
            f"The value for '{name}' should be greater than {high}, not {n}."
        )
    if not_low and n == low:
        raise ValueError(
            f"The value for '{name}' should not be greater than and not equal to {low}"
        )
    if not_high and n == high:
        raise ValueError(
            f"The value for '{name}' should not be less than and not equal to {high}"
        )


def assert_length(li, num, name):
    """Assert that a tuple or list is of a specific length."""
    if len(li) != num:
        raise ValueError(f"The length of '{name}' should be {num} not {len(li)}.")


def assert_list_contents(li, content, name):
    """Assert that a tuple or list contains only specific items"""
    for a in li:
        if a not in content:
            raise ValueError(
                f"The variable '{name}', must be a tuple or"
                + f" list containing only items in {content} not {a}."
            )


def assert_contents(var, content, name):
    """Assert that a variable is within a specific subset of available values"""

    if var not in content:
        raise ValueError(
            f"The variable '{name}', must only have a"
            + f" value that is specified in {content} not '{var}'."
        )
