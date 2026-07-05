from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    name = "base"

    background = True

    @abstractmethod
    def available(self) -> bool:
        """
        Check whether the external tool exists.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, target: str) -> dict:
        """
        Execute adapter scan.
        """
        raise NotImplementedError