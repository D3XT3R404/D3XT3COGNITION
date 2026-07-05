from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    Base class untuk seluruh engine DEXTER.
    """

    # wajib dioverride
    name = "base"

    @abstractmethod
    def run(self, context):
        """
        Jalankan engine.
        """
        raise NotImplementedError