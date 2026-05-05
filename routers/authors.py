from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from supabase import AsyncClient

import config
from db.core import get_supabase_client
from db.authors import (
    AuthorCreate,
    AuthorUpdate,
    add_author_to_db,
    update_author_in_db,
    get_author_from_db,
    delete_author_from_db,
)

supabase_dependancy = get_supabase_client(config.SUPABASE_URL, config.SUPABASE_KEY)

router = APIRouter(prefix="/authors")


@router.post("/")
async def add_author(
    author: AuthorCreate,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await add_author_to_db(author, supabase_client)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": f"Author successfully added to db.",
            "data": response.data,
        },
    )


@router.patch("/{author_id}")
async def update_author(
    author_id: UUID,
    author: AuthorUpdate,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await update_author_in_db(author_id, author, supabase_client)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Author successfully updated in db.",
            "data": response.data,
        },
    )


@router.get("/{author_id}")
async def get_author(
    author_id: UUID,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await get_author_from_db(author_id, supabase_client)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Obtained author successfully.",
            "data": response.data,
        },
    )


@router.delete("/{author_id}")
async def delete_author(
    author_id: UUID,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await delete_author_from_db(author_id, supabase_client)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Author with id={author_id} deleted successfully.",
            "data": response.data,
        },
    )
