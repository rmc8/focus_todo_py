class FocusToDoConnectionError(Exception):
    """Raised when communication ended in error."""


class FocusToDoTooManyRequestsError(Exception):
    """Raised when rate limit is exceeded."""


class FocusToDoAuthenticationError(Exception):
    """Raised when authentication is failed."""


class FocusToDoInvalidFileFormatError(Exception):
    """Raised when an invalid file format is passed to upload."""
