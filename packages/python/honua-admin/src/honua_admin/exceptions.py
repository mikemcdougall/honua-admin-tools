"""
Custom exceptions for Honua admin operations.
"""


class HonuaAdminError(Exception):
    """Base exception for Honua admin operations."""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(HonuaAdminError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR")


class ServiceNotFoundError(HonuaAdminError):
    """Raised when a service is not found."""

    def __init__(self, message: str):
        super().__init__(message, "SERVICE_NOT_FOUND")


class LayerNotFoundError(HonuaAdminError):
    """Raised when a layer is not found."""

    def __init__(self, message: str):
        super().__init__(message, "LAYER_NOT_FOUND")


class ValidationError(HonuaAdminError):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")


class ImportError(HonuaAdminError):
    """Raised when bulk import operations fail."""

    def __init__(self, message: str, failed_features: list = None):
        self.failed_features = failed_features or []
        super().__init__(message, "IMPORT_ERROR")


class ExportError(HonuaAdminError):
    """Raised when export operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "EXPORT_ERROR")


class PermissionError(HonuaAdminError):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str, required_permission: str = None):
        self.required_permission = required_permission
        super().__init__(message, "PERMISSION_ERROR")