import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─── Home ────────────────────────────────────────────────────────────────────

def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


# ─── Health ──────────────────────────────────────────────────────────────────

def test_health_endpoint_reports_dependencies(client):
    """As an operator, /health returns OK when dependencies are reachable."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_conn):
        response = client.get("/health")
        assert response.status_code == 200


def test_health_returns_error_when_db_down(client):
    with patch("app.get_db_connection", side_effect=Exception("DB unavailable")):
        response = client.get("/health")
        assert response.status_code == 500


# ─── Status ──────────────────────────────────────────────────────────────────

def test_status_shows_connected_when_db_up(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.fetchall.return_value = []
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_conn):
        response = client.get("/status")
        assert response.status_code == 200


def test_status_shows_not_connected_when_db_down(client):
    with patch("app.get_db_connection", side_effect=Exception("DB unavailable")):
        response = client.get("/status")
        assert response.status_code == 200


# ─── Dog view ────────────────────────────────────────────────────────────────

def test_returns_joined_result_when_both_sources_available(client):
    """As a user, I can retrieve a consolidated resource from two sources."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("https://cdn2.thedogapi.com/images/test.jpg", "2026-04-03 10:00:00")
    ]
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_conn):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [{"url": "https://cdn2.thedogapi.com/images/test.jpg"}]
            response = client.get("/dog/view")
            assert response.status_code == 200


def test_graceful_degradation_on_upstream_failure(client):
    """As a user, if the external API is down, I get cached data not a crash."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_conn):
        with patch("requests.get", side_effect=Exception("API down")):
            response = client.get("/dog/view")
            assert response.status_code == 200


# ─── Save dog ────────────────────────────────────────────────────────────────

def test_save_dog_success(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_conn):
        response = client.post("/dog/save", data={
            "image_url": "https://cdn2.thedogapi.com/images/test.jpg"
        })
        assert response.status_code in [200, 302]


def test_save_dog_missing_url_returns_400(client):
    response = client.post("/dog/save", data={})
    assert response.status_code == 400


# ─── Dogs JSON ───────────────────────────────────────────────────────────────

def test_dogs_endpoint_returns_200(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("https://cdn2.thedogapi.com/images/test.jpg", "2026-04-03 10:00:00")
    ]
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_conn):
        response = client.get("/dogs")
        assert response.status_code == 200
