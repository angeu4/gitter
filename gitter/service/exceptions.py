class ServiceError(Exception):
    """Base service-layer error."""


class NothingToCommitError(ServiceError):
    """Raised when commit is attempted with an empty staging area."""
