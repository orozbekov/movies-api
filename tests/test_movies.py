from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "movies" in data
    assert data["total"] == len(data["movies"])
    assert data["total"] > 0


def test_movie_schema():
    response = client.get("/movies")
    movie = response.json()["movies"][0]
    assert "id" in movie
    assert "title" in movie
    assert "year" in movie
    assert "director" in movie
    assert "genres" in movie
    assert "rating" in movie
    assert "description" in movie


def test_filter_by_genre():
    response = client.get("/movies?genre=Drama")
    assert response.status_code == 200
    data = response.json()
    for movie in data["movies"]:
        genres_lower = [g.lower() for g in movie["genres"]]
        assert "drama" in genres_lower


def test_filter_by_year():
    response = client.get("/movies?year=1994")
    assert response.status_code == 200
    data = response.json()
    for movie in data["movies"]:
        assert movie["year"] == 1994


def test_filter_no_results():
    response = client.get("/movies?year=1800")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["movies"] == []


def test_get_movie_by_id():
    response = client.get("/movies/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_movie_not_found():
    response = client.get("/movies/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
