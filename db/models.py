from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Author(BaseModel):
    full_name: str
    bio: Optional[str] = None
    country_of_origin: Optional[str] = None


class AuthorUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    country_of_origin: Optional[str] = None


class Book(BaseModel):
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


class Profile(BaseModel):
    id: UUID
    full_name: str
    birthdate: date
    role: Literal["admin", "member"]


class BookLoan(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    profile_id: Optional[UUID] = None
    loaned_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    book_id: Optional[UUID] = None
