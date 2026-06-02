from abc import ABC, abstractmethod


class Command(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass
