from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models import Movie, MoviesResponse
from data import MOVIES

app = FastAPI(
    title="Movies API",
    description="A simple REST API returning a list of movies.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Movies API is running. Visit /docs for Swagger UI."}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/movies", response_model=MoviesResponse, tags=["Movies"])
def get_movies(
    genre: Optional[str] = Query(None, description="Filter by genre (case-insensitive)"),
    year: Optional[int] = Query(None, description="Filter by release year"),
):
    """
    Returns a hardcoded list of movies.

    Optionally filter by **genre** and/or **year**.
    """
    results = MOVIES

    if genre:
        results = [m for m in results if genre.lower() in [g.lower() for g in m.genres]]

    if year:
        results = [m for m in results if m.year == year]

    return MoviesResponse(total=len(results), movies=results)


@app.get("/movies/{movie_id}", response_model=Movie, tags=["Movies"])
def get_movie(movie_id: int):
    """
    Returns a single movie by its ID.
    """
    from fastapi import HTTPException

    movie = next((m for m in MOVIES if m.id == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found.")
    return movie
