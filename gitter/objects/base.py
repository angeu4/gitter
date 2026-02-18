from abc import ABC, abstractmethod


class GitterObject(ABC):
    """
    Base class for all immutable repository objects.

    Enforces deterministic serialization contract for hashing and storage.
    """

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Convert object into serializable dictionary form.

        Must be deterministic across identical object instances.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """
        Reconstruct object from serialized dictionary representation.
        """
        pass
