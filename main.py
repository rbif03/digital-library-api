from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client

import config
from db.models import Author, Book, BookLoan, Profile
from db.utils import try_get_row_by_id, try_insert_dict_to_table

supabase_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

app = FastAPI()


@app.post("/authors")
def add_author(author_model: Author):
    db_dict = author_model.to_db_dict(action="create")
    json_response = try_insert_dict_to_table(supabase_client, "authors", db_dict)
    return json_response


@app.patch("/authors/{author_id}")
def update_author(author_id: str, author_model: dict):
    result = try_get_row_by_id(supabase_client, "authors", author_id)
    if not result.success:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": result.message,
                "data": None,
            },
        )

    return json_response


@app.post("/books")
def add_book(book_model: Book):
    db_dict = book_model.to_db_dict(action="create")
    json_response = try_insert_dict_to_table(supabase_client, "books", db_dict)
    return json_response


@app.post("/loans")
def add_loan(book_loan_model: BookLoan):
    db_dict = book_loan_model.to_db_dict(action="create")
    json_response = try_insert_dict_to_table(supabase_client, "book_loans", db_dict)
    return json_response
