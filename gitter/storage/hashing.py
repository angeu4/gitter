import hashlib


def sha1_hash(data: bytes) -> str:
    """
    SHA1 used for content-addressable storage (Git-compatible behavior).
    Not used for cryptographic security.
    """
    return hashlib.sha1(data, usedforsecurity=False).hexdigest()
