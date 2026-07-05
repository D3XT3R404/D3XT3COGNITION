from abc import ABC
from abc import abstractmethod

from typing import Any


class BaseEngine(ABC):

    @abstractmethod
    def run(

            self,

            data: Any

    ) -> Any:

        raise NotImplementedError