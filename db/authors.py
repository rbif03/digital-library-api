from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from supabase import AsyncClient

from db.core import DatabaseError, NotFoundError


class Author(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    full_name: str
    bio: Optional[str]
    country_of_origin: Optional[str]


class AuthorCreate(BaseModel):
    full_name: str
    bio: Optional[str] = None
    country_of_origin: Optional[str] = None


class AuthorUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    country_of_origin: Optional[str] = None


async def add_author_to_db(author: AuthorCreate, supabase_client: AsyncClient):
    data = author.model_dump(mode="json")
    try:
        response = await supabase_client.table("authors").insert(data).execute()

    except Exception as e:
        raise DatabaseError(str(e))

    return response


async def update_author_in_db(
    author_id: UUID, author: AuthorUpdate, supabase_client: AsyncClient
):
    data = author.model_dump(mode="json", exclude_unset=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    try:
        response = await (
            supabase_client.table("authors").update(data).eq("id", author_id).execute()
        )

    except Exception as e:
        raise DatabaseError(str(e))

    if not response.data:
        raise NotFoundError(f"Author with id={author_id} not found.")

    return response


async def get_author_from_db(author_id: UUID, supabase_client: AsyncClient):
    try:
        response = (
            await supabase_client.table("authors")
            .select("*")
            .eq("id", author_id)
            .execute()
        )

    except Exception as e:
        raise DatabaseError(str(e))

    if not response.data:
        raise NotFoundError(f"Author with id={author_id} not found.")

    return response


async def delete_author_from_db(author_id: UUID, supabase_client: AsyncClient):
    try:
        response = (
            await supabase_client.table("authors")
            .delete()
            .eq("id", author_id)
            .execute()
        )

    except Exception as e:
        raise DatabaseError(str(e))

    if not response.data:
        raise NotFoundError(f"Author with id={author_id} not found.")

    return response
