from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from supabase import AsyncClient

import config
from db.core import get_supabase_client

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from supabase import AsyncClient

import config
from db.core import get_supabase_client
from db.books import (
    BookCreate,
    BookUpdate,
    add_book_to_db,
    update_book_in_db,
    get_book_from_db,
    delete_book_from_db,
)

supabase_dependancy = get_supabase_client(config.SUPABASE_URL, config.SUPABASE_KEY)

router = APIRouter(prefix="/books")


@router.post("/")
async def add_book(
    book: BookCreate,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await add_book_to_db(book, supabase_client)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": f"Book successfully added to db.",
            "data": response.data,
        },
    )


@router.patch("/{book_id}")
async def update_book(
    book_id: UUID,
    book: BookUpdate,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await update_book_in_db(book_id, book, supabase_client)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Book successfully updated in db.",
            "data": response.data,
        },
    )


@router.get("/{book_id}")
async def get_book(
    book_id: UUID,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await get_book_from_db(book_id, supabase_client)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Obtained book successfully.",
            "data": response.data,
        },
    )


@router.delete("/{book_id}")
async def delete_book(
    book_id: UUID,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await delete_book_from_db(book_id, supabase_client)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Book with id={book_id} deleted successfully.",
            "data": response.data,
        },
    )
