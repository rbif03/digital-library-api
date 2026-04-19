from typing import Any, Optional


class TryResult:
    def __init__(
        self, success: bool, message: Optional[str] = None, data: Optional[Any] = None
    ):
        self.success = success
        self.message = message
        self.data = data
