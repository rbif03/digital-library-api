from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Profile(BaseModel):
    id: UUID
    full_name: str
    birthdate: date
    role: Literal["admin", "member"]
