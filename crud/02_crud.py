from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="Registro de películas", version="1.0.0")

# creando un registro
movies = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "overview": "Película sobre la esperanza y la amistad en una prisión.",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama"
    },
    {
        "id": 2,
        "title": "The Godfather",
        "overview": "Historia de una familia mafiosa en Nueva York.",
        "year": 1972,
        "rating": 9.2,
        "category": "Crime"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "overview": "Batman enfrenta al Joker en Gotham City.",
        "year": 2008,
        "rating": 9.0,
        "category": "Action"
    }
]

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Registro de películas</h1>")

@app.get("/movies/", tags=["movies"])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=["movies"])
def get_movies(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []

@app.get("/movies/", tags=["movies"])
def get_movies_by_categories(category: str, year: int):
    movies_found = []
    for item in movies:
        if item["category"] == category and item["year"] == year:
            movies_found.append(item)
    return movies_found

@app.post("/movies/", tags=["movies"])
def create_movie(id: int = Body(), title: str = Body(),
                 overview: str = Body(), year: int = Body(),
                 rating: float = Body(), category: str = Body()):
    movie = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    movies.append(movie)
    return movies

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi película", max_length=5, min_length=15)
    overview: str
    year: int
    rating: float
    category: str

@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return movies
    return []

@app.post("/movies/", tags=["movies"])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies