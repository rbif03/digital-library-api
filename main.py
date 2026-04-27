from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from postgrest.exceptions import APIError
from supabase import acreate_client, AsyncClient

import config
from db.models import Author, Book, BookLoan, Profile
from db.models import AuthorUpdate, BookUpdate
from schemas.response import OkResp, ErrorResp, get_resp_models


app = FastAPI()


async def create_supabase() -> AsyncClient:
    supabase: AsyncClient = await acreate_client(
        config.SUPABASE_URL,
        config.SUPABASE_KEY
    )
    return supabase


@app.post("/authors", status_code=201, responses=get_resp_models(201, 500))
async def add_author(
    author: Author,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)],
    response: Response
):
    """
    docstring
    """
    data = author.model_dump(mode="json")  # converts request body to dict

    # Inserts data to db, returns status_code=500 if an error occurs
    try:
        supabase_response = await (
            supabase_client
            .table("authors")
            .insert(data)
            .execute()
        )
    except Exception as e:
        response.status_code = 500
        return ErrorResp(
            message="Database error (supabase). {e}"
        )

    response.status_code = 201
    return OkResp(
        message="Author added to database.",
        data=supabase_response.data
    )


@app.patch("/authors/{author_id}", status_code=200, responses=get_resp_models(200, 500, 404))
async def update_author(
    author_id: UUID,
    author: AuthorUpdate,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)],
    response: Response
):
    """
    docstring
    """
    data = author.model_dump(mode="json", exclude_unset=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Updates db data, returns status_code=500 if an error occurs
    try:
        supabase_response = await (
            supabase_client
            .table("authors")
            .update(data)
            .eq("id", author_id)
            .execute()
        )
    except Exception as e:
        response.status_code = 500
        return ErrorResp(
            message="Database error (supabase). {e}"
        )

    # If id is not found, returns 404
    if not supabase_response.data:
        response.status_code = 404
        return ErrorResp(
            message=f"Author with id = {author_id} does not exist."
        )

    response.status_code = 200
    return OkResp(
        message=f"Updated author (id={author_id}).",
        data=supabase_response.data
    )


@app.post("/books", status_code=201, responses=get_resp_models(201, 500))
async def add_book(
    book: Book,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)],
    response: Response
):
    """
    docstring
    """
    data = book.model_dump(mode="json")
    # fields 'id', 'created_at' and 'updated_at' use postgres' default values
    try:
        supabase_response = await (
            supabase_client
            .table("books")
            .insert(data)
            .execute()
        )
    except Exception as e:
        response.status_code = 500
        return ErrorResp(
            message="Database error (supabase). {e}"
        )

    response.status_code = 201
    return OkResp(
        message=f"Book added to db.",
        data=supabase_response.data
    )


@app.patch("/books/{book_id}", status_code=200, responses=get_resp_models(200, 500, 404))
async def update_book(
    book_id: UUID,
    book: BookUpdate,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)],
    response=Response
):
    data = book.model_dump(mode="json", exclude_unset=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    try:
        supabase_response = await (
            supabase_client
            .table("books")
            .update(data)
            .eq("id", book_id)
            .execute()
        )
    except Exception as e:
        response.status_code = 500
        return ErrorResp(
            message="Database error (supabase). {e}"
        )

    if not supabase_response.data:
        response.status_code = 404
        return ErrorResp(
            message=f"Book with id = {book_id} does not exist."
        )

    response.status_code = 200
    return OkResp(
        message=f"Updated book (id={book_id}).",
        data=supabase_response.data
    )
