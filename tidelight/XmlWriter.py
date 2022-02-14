from abc import ABC, abstractmethod


class AbstractClassExample(ABC):

    def __init__(self, file: str):
        self.file = file
    
    @abstractmethod
    def write(self) -> None:
        pass
