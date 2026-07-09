from abc import ABC, abstractmethod
import re


class BaseEngine(ABC):
    NAME_ALIASES = {
        "endpoint": "endpoints",
        "form": "forms",
        "comment": "comments",
        "email": "emails",
        "fingerprint": "fingerprints",
        "js": "javascript",
    }

    @property
    def name(self):
        raw = self.__class__.__name__.replace("Engine", "")
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", raw).lower()
        return self.NAME_ALIASES.get(name, name)

    @abstractmethod
    def run(self, target):
        raise NotImplementedError
