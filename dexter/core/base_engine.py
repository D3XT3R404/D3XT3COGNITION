from abc import ABC, abstractmethod


class BaseEngine(ABC):
    @property
    def name(self):
        return self.__class__.__name__.replace("Engine", "").lower()

    @abstractmethod
    def run(self, target):
        raise NotImplementedError