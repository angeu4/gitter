class RepositoryError(Exception):
    """Base repository metadata error."""


class HeadError(RepositoryError):
    """HEAD file invalid or inaccessible."""


class RefError(RepositoryError):
    """Branch reference failure."""


class RefNotFoundError(RefError):
    """Branch reference does not exist."""


class ConfigError(RepositoryError):
    """Repository config read/write failure."""
