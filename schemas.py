from pydantic import BaseModel, Field
from typing import Optional, List

class Author(BaseModel):
    name: str
    birth_year: Optional[int] = None

class AuthorCreate(Author):
    id: Optional[int] = Field(default=None, description="The unique identifier of the author")


class BookCreate(BaseModel):
    title: str
    author_id: int
    publication_year: Optional[int] = None

class Book(BaseModel):
    id: Optional[int] = Field(default=None, description="The unique identifier of the book") 
    title: str
    author_id: int
    publication_year: Optional[int] = None