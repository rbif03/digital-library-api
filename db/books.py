from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from postgrest.exceptions import APIError
from pydantic import BaseModel
from supabase import AsyncClient

from db.core import DatabaseError, NotFoundError, ForeignKeyError


class Book(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    author_id: UUID
    title: str
    isbn: Optional[str] = None
    year_published: Optional[int] = None
    genre: Optional[str] = None
    edition: Optional[int] = None
    total_copies: int
    cover_url: Optional[str] = None
    file_url: str


class BookCreate(BaseModel):
    author_id: UUID
    title: str
    isbn: Optional[str] = None
    year_published: Optional[int] = None
    genre: Optional[str] = None
    edition: Optional[int] = None
    total_copies: int
    cover_url: Optional[str] = None
    file_url: str


class BookUpdate(BaseModel):
    author_id: Optional[UUID] = None
    title: Optional[str] = None
    isbn: Optional[str] = None
    year_published: Optional[int] = None
    genre: Optional[str] = None
    edition: Optional[int] = None
    total_copies: Optional[int] = None
    cover_url: Optional[str] = None
    file_url: Optional[str] = None


async def add_book_to_db(book: BookCreate, supabase_client: AsyncClient):
    data = book.model_dump(mode="json")
    try:
        response = await supabase_client.table("books").insert(data).execute()

    except APIError as e:
        if e.code == "23503":
            raise ForeignKeyError(e.details)
        else:
            raise DatabaseError(str(e))

    except Exception as e:
        raise DatabaseError(str(e))

    return response


async def update_book_in_db(
    book_id: UUID, book: BookUpdate, supabase_client: AsyncClient
):
    data = book.model_dump(mode="json", exclude_unset=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    try:
        response = await (
            supabase_client.table("books").update(data).eq("id", book_id).execute()
        )

    except APIError as e:
        if e.code == "23503":
            raise ForeignKeyError(e.details)
        else:
            raise DatabaseError(str(e))

    except Exception as e:
        print(type(e))
        print(e)
        raise DatabaseError(str(e))

    if not response.data:
        raise NotFoundError(f"Book with id={book_id} not found.")

    return response


async def get_book_from_db(book_id: UUID, supabase_client: AsyncClient):
    try:
        response = (
            await supabase_client.table("books").select("*").eq("id", book_id).execute()
        )

    except Exception as e:
        raise DatabaseError(str(e))

    if not response.data:
        raise NotFoundError(f"Book with id={book_id} not found.")

    return response


async def delete_book_from_db(book_id: UUID, supabase_client: AsyncClient):
    try:
        response = (
            await supabase_client.table("books").delete().eq("id", book_id).execute()
        )

    except Exception as e:
        raise DatabaseError(str(e))

    if not response.data:
        raise NotFoundError(f"Book with id={book_id} not found.")

    return response
