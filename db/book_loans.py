from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BookLoan(BaseModel):
    profile_id: Optional[UUID] = None
    loaned_at: datetime
    expires_at: datetime
    book_id: Optional[UUID] = None
