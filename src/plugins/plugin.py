from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, args):
        pass

    def is_valid(self) -> bool:
        return True

    @abstractmethod
    def to_string(self) -> list:
        pass
