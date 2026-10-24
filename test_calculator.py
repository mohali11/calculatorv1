import pytest

from calculator import add, divide, multiply, subtract


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (-2, -3, -5),
        (-2, 3, 1),
        (0, 0, 0),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (5, 3, 2),
        (-5, -3, -2),
        (-5, 3, -8),
        (0, 0, 0),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 6),
        (-2, 3, -6),
        (-2, -3, 6),
        (0, 5, 0),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (10, 2, 5),
        (-10, 2, -5),
        (-10, -2, 5),
        (0, 5, 0),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


def test_divide_by_zero_returns_none(capsys):
    result = divide(10, 0)

    assert result is None
    assert "cannot divide by zero" in capsys.readouterr().out.lower()
