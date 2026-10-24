import pytest

from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    ("operation", "a", "b", "expected"),
    [
        ("add", 12, 8, 20),
        ("subtract", 12, 8, 4),
        ("multiply", 12, 8, 96),
        ("divide", 12, 8, 1.5),
        ("add", -12, -8, -20),
        ("multiply", -12, 8, -96),
        ("divide", -12, -8, 1.5),
    ],
)
def test_calculate_uses_calculator_functions(client, operation, a, b, expected):
    response = client.post(
        "/api/calculate",
        json={"operation": operation, "a": a, "b": b},
    )

    assert response.status_code == 200
    assert response.get_json() == {"ok": True, "result": expected}


def test_divide_by_zero_returns_a_helpful_error(client):
    response = client.post(
        "/api/calculate",
        json={"operation": "divide", "a": 12, "b": 0},
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False
    assert "zero" in body["error"].lower()


@pytest.mark.parametrize(
    "payload",
    [
        {"operation": "power", "a": 2, "b": 3},
        {"operation": "add", "a": "two", "b": 3},
        {"operation": "add", "a": 2},
        {"operation": "add", "a": True, "b": 3},
        {"operation": "add", "a": 2, "b": float("inf")},
    ],
)
def test_rejects_invalid_requests(client, payload):
    response = client.post("/api/calculate", json=payload)

    assert response.status_code == 400
    assert response.get_json()["ok"] is False


def test_rejects_a_number_too_large_for_a_float(client):
    response = client.post(
        "/api/calculate",
        json={"operation": "add", "a": 10**400, "b": 1},
    )

    assert response.status_code == 400
    assert response.get_json()["ok"] is False


def test_rejects_a_result_that_overflows(client):
    response = client.post(
        "/api/calculate",
        json={"operation": "multiply", "a": 1e308, "b": 1e308},
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False
    assert "too large" in body["error"].lower()


def test_index_serves_the_calculator_ui(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Apex" in html
    assert 'id="calculator"' in html
