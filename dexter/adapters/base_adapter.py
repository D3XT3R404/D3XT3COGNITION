from abc import ABC, abstractmethod
from shutil import which
from urllib.parse import urlparse


class BaseAdapter(ABC):
    binary = None

    @property
    def name(self):
        return self.__class__.__name__.replace("Adapter", "").lower()

    def available(self):
        if not self.binary:
            return True
        return which(self.binary) is not None

    def normalize_target(self, target):
        if hasattr(target, "target"):
            target = getattr(target, "target")
        target = str(target).strip()
        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        return target.rstrip("/")

    def host_only(self, target):
        url = self.normalize_target(target)
        parsed = urlparse(url)
        return parsed.hostname or parsed.netloc

    def run(self, target, results=None):
        return self.execute(target, results=results)

    @abstractmethod
    def execute(self, target, results=None):
        raise NotImplementedError