from abc import ABC, abstractmethod


class GitterObject(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        pass
