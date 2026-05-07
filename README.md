# 🎬 Movies API

A minimal **FastAPI** service that exposes a hardcoded list of movies via a REST API.
Built as a clean, production-ready starting point with Docker, Docker Compose, CI/CD, and full test coverage.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI 0.115 |
| Server | Uvicorn (ASGI) |
| Validation | Pydantic v2 |
| Container | Docker (multi-stage build) |
| Orchestration | Docker Compose |
| Linter | Ruff |
| Tests | Pytest + HTTPX |
| CI/CD | GitHub Actions |

---

## Quick Start

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000**.

### Without Docker (local dev)

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check & welcome message |
| `GET` | `/health` | Minimal health probe |
| `GET` | `/movies` | List all movies (supports filters) |
| `GET` | `/movies/{id}` | Get a single movie by ID |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc UI |

### Query Parameters for `GET /movies`

| Parameter | Type | Description |
|-----------|------|-------------|
| `genre` | `string` | Case-insensitive genre filter (e.g. `Drama`) |
| `year` | `integer` | Filter by release year (e.g. `1994`) |

### Example Requests

```bash
# All movies
curl http://localhost:8000/movies

# Filter by genre
curl "http://localhost:8000/movies?genre=Sci-Fi"

# Filter by year
curl "http://localhost:8000/movies?year=2008"

# Combined filters
curl "http://localhost:8000/movies?genre=Drama&year=1994"

# Single movie by ID
curl http://localhost:8000/movies/3
```

### Example Response

```json
{
  "total": 2,
  "movies": [
    {
      "id": 1,
      "title": "The Shawshank Redemption",
      "year": 1994,
      "director": "Frank Darabont",
      "genres": ["Drama"],
      "rating": 9.3,
      "description": "Two imprisoned men bond over a number of years..."
    }
  ]
}
```

---

## Project Structure

```
movies-api/
├── main.py                     # FastAPI app & route definitions
├── models.py                   # Pydantic schemas
├── data.py                     # Hardcoded movie data
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Ruff + Pytest config
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Service orchestration
├── .gitignore
├── tests/
│   └── test_movies.py          # Full test suite
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI pipeline
```

---

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

---

## CI/CD Pipeline

On every push and pull request to `main`:

1. **Lint** – Ruff checks code style and imports
2. **Test** – Pytest runs the full test suite
3. **Docker Build** – Image is built and smoke-tested end-to-end

---

## Docker Details

The Dockerfile uses a **multi-stage build**:
- **Stage 1 (`builder`)** – installs Python dependencies
- **Stage 2 (`runtime`)** – copies only the installed packages; no build tools, minimal image size

The container runs as a **non-root user** for security.
