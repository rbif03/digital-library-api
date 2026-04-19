from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DataBaseModel(BaseModel):
    def to_db_dict(self, action: Literal["create", "update"]) -> dict:
        data = self.model_dump(mode="json")
        if action == "create":
            data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return data


class Author(DataBaseModel):
    id: UUID = Field(default_factory=uuid4)
    full_name: Optional[str] = None
    bio: Optional[str] = None
    country_of_origin: Optional[str] = None


class Book(DataBaseModel):
    id: UUID = Field(default_factory=uuid4)
    author_id: Optional[UUID] = None
    title: str
    isbn: Optional[str] = None
    year_published: Optional[int] = None
    genre: Optional[str] = None
    edition: Optional[int] = None
    total_copies: int
    cover_url: Optional[str] = None
    file_url: str


class Profile(DataBaseModel):
    id: UUID
    full_name: str
    birthdate: date
    role: Literal["admin", "member"]


class BookLoan(DataBaseModel):
    id: UUID = Field(default_factory=uuid4)
    profile_id: Optional[UUID] = None
    loaned_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    book_id: Optional[UUID] = None
