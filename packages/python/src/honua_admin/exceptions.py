"""Exception classes for Honua Admin client."""

from typing import Optional, Any


class HonuaAdminError(Exception):
    """Base exception for all Honua Admin errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class HonuaAdminApiError(HonuaAdminError):
    """Exception raised when an API request fails with an HTTP error response."""

    def __init__(self, message: str, status_code: int, response: Optional[Any] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        return f"HTTP {self.status_code}: {self.message}"


class HonuaAdminOperationError(HonuaAdminError):
    """Exception raised when an operation fails due to client-side issues."""

    def __init__(self, message: str):
        super().__init__(message)