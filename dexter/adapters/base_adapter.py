from abc import ABC, abstractmethod
from shutil import which


class BaseAdapter(ABC):
    binary = None

    @property
    def name(self):
        return self.__class__.__name__.replace("Adapter", "").lower()

    def available(self):
        if not self.binary:
            return True
        return which(self.binary) is not None

    @abstractmethod
    def execute(self, target, results=None):
        raise NotImplementedError