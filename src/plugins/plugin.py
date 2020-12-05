from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, args):
        pass

    def validate(self) -> bool:
        return True

    def apply_plugin(self, probe):
        pass

    @abstractmethod
    def to_string(self) -> list:
        pass
