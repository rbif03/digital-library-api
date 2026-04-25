from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from postgrest.exceptions import APIError
from supabase import acreate_client, AsyncClient

import config
from db.models import Author, Book, BookLoan, Profile
from db.models import AuthorUpdate, BookUpdate


app = FastAPI()


async def create_supabase() -> AsyncClient:
    supabase: AsyncClient = await acreate_client(
        config.SUPABASE_URL,
        config.SUPABASE_KEY
    )
    return supabase


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(status_code=500, content={
        "status": "error",
        "message": f"Supabase/postgrest error when performing an action in db. {exc.details}",
        "data": exc.json()
    })


@app.post("/authors")
async def add_author(
    author: Author,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)]
):
    """
    docstring
    """
    data = author.model_dump(mode="json")
    # fields 'id', 'created_at' and 'updated_at' use postgres' default values
    response = await supabase_client.table("authors").insert(data).execute()
    return JSONResponse(status_code=201, content={
        "status": "success",
        "message": f"Author added to db.",
        "data": response.data
    })


@app.patch("/authors/{author_id}")
async def update_author(
    author_id: UUID,
    author: AuthorUpdate,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)]
):
    """
    docstring
    """
    data = author.model_dump(mode="json", exclude_unset=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    response = await (
        supabase_client
        .table("authors")
        .update(data)
        .eq("id", author_id)
        .execute()
    )

    if not response.data:
        return JSONResponse(status_code=404, content={
            "status": "error",
            "message": f"Author with id = {author_id} does not exist."
        })

    return JSONResponse(status_code=200, content={
        "status": "success",
        "message": f"Updated author (id={author_id}).",
        "data": response.data
    })


@app.post("/books")
async def add_book(
    book: Book,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)]
):
    """
    docstring
    """
    data = book.model_dump(mode="json")
    # fields 'id', 'created_at' and 'updated_at' use postgres' default values
    response = await supabase_client.table("books").insert(data).execute()
    return JSONResponse(status_code=201, content={
        "status": "success",
        "message": f"Book added to db.",
        "data": response.data
    })


@app.patch("/books/{book_id}")
async def update_book(
    book_id: UUID,
    book: BookUpdate,
    supabase_client: Annotated[AsyncClient, Depends(create_supabase)]
):
    data = book.model_dump(mode="json", exclude_unset=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    response = await (
        supabase_client
        .table("books")
        .update(data)
        .eq("id", book_id)
        .execute()
    )

    if not response.data:
        return JSONResponse(status_code=404, content={
            "status": "error",
            "message": f"Book with id = {book_id} does not exist."
        })

    return JSONResponse(status_code=200, content={
        "status": "success",
        "message": f"Updated book (id={book_id}).",
        "data": response.data
    })
