import hashlib


def sha1_hash(data: bytes) -> str:
    """
    Compute SHA1 hash for content-addressable storage.

    SHA1 is intentionally used for Git-compatible object addressing.
    This hash is NOT used for cryptographic security or authentication.

    Args:
        data: Raw object bytes.

    Returns:
        Hexadecimal SHA1 hash string.

    Notes:
        usedforsecurity=False is set to satisfy security linters and indicate
        that SHA1 is used only for content identity.
    """
    return hashlib.sha1(data, usedforsecurity=False).hexdigest()
