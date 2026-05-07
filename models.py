from pydantic import BaseModel
from typing import List


class Movie(BaseModel):
    id: int
    title: str
    year: int
    director: str
    genres: List[str]
    rating: float
    description: str

    model_config = {"json_schema_extra": {
        "example": {
            "id": 1,
            "title": "The Shawshank Redemption",
            "year": 1994,
            "director": "Frank Darabont",
            "genres": ["Drama"],
            "rating": 9.3,
            "description": "Two imprisoned men bond over years, finding solace and eventual redemption.",
        }
    }}


class MoviesResponse(BaseModel):
    total: int
    movies: List[Movie]
