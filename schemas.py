from pydantic import BaseModel, Field
from typing import Optional

# ✅ INPUT schema for creating an author (no id)
class AuthorCreate(BaseModel):
    name: str
    birth_year: Optional[int] = None

# ✅ OUTPUT schema with id
class Author(BaseModel):
    id: int
    name: str
    birth_year: Optional[int] = None

# ✅ INPUT
class BookCreate(BaseModel):
    title: str
    author_id: int
    publication_year: Optional[int] = None

# ✅ OUTPUT
class Book(BaseModel):
    id: int
    title: str
    author_id: int
    publication_year: Optional[int] = None
