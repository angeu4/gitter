class IndexError(Exception):
    """Base exception for index layer."""


class IndexCorruptedError(IndexError):
    """Raised when index file cannot be parsed."""
