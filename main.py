from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import get_db_connection
from schemas import Author, Book, AuthorCreate, BookCreate


app = FastAPI()


@app.post("/authors")
def create_author(author: AuthorCreate):
    conn, cursor = get_db_connection()
    cursor.execute("INSERT INTO authors (name, birth_year) VALUES (%s, %s) RETURNING id", (author.name, author.birth_year))
    author_id = cursor.fetchone()["id"]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": author_id, "name": author.name, "birth_year": author.birth_year}

@app.get("/authors")
def get_authors():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    return authors

@app.post("/books")
def create_book(book: BookCreate):
    conn, cursor = get_db_connection()
    cursor.execute("INSERT INTO books (title, author_id, publication_year) VALUES (%s, %s, %s) RETURNING id",
                   (book.title, book.author_id, book.publication_year))
    book_id = cursor.fetchone()["id"]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": book_id, "title": book.title, "author_id": book.author_id, "publication_year": book.publication_year}


@app.get("/books")
def get_books():
    conn, cursor = get_db_connection()
    cursor.execute("""
    SELECT 
        books.id AS book_id,
        books.title,
        books.publication_year,
        books.author_id,
        books.is_deleted,
        authors.id AS author_id,
        authors.name AS author_name,
        authors.birth_year AS author_birth_year
    FROM books
    JOIN authors ON books.author_id = authors.id
    WHERE books.is_deleted = FALSE
""")

    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id where books.id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()    
    if book is None:
        return {"error": "Book not found"}  
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):  
    conn, cursor = get_db_connection()
    cursor.execute("UPDATE books SET is_deleted = TRUE WHERE id = %s", (book_id,))
    result = cursor.rowcount > 0
    conn.commit()
    cursor.close()
    conn.close()
    if result:
        return {"message": f"Bookd with id {book_id} is moved to recycle bin"}
    else:
        return {"error": "Book not found or already deleted"}



@app.get("/recycle_bin/books")
def get_recycle_bin():
    conn, cursor = get_db_connection()
    cursor.execute("""
        SELECT b.id, b.title, b.publication_year, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.is_deleted = TRUE""")
    recycle_bin_books = cursor.fetchall()
    cursor.close()  
    conn.close()
    return recycle_bin_books

@app.post("/recycle_bin/books/{book_id}/restore")
def restore_book(book_id: int):
    conn, cursor = get_db_connection()
    cursor.execute("UPDATE books SET is_deleted = FALSE WHERE id = %s", (book_id,))
    result = cursor.rowcount > 0
    conn.commit()
    cursor.close()
    conn.close()
    if result:
        return {"message": f"Book with id {book_id} has been restored from recycle bin"}
    else:
        return {"error": "Book not found or not in recycle bin"}
    