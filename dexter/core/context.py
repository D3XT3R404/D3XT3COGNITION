import requests
from urllib.parse import urlparse


class ScanContext:
    def __init__(self, target: str, deep: bool = False):
        self.original_target = target.strip()
        self.target = self._normalize_target(self.original_target)
        parsed = urlparse(self.target)

        self.scheme = parsed.scheme or "https"
        self.host = parsed.netloc
        self.hostname = parsed.hostname or self.host
        self.root_domain = self.hostname
        self.deep = deep

        self.session = requests.Session()
        self.response = None
        self.results = {}

        self.technologies = []
        self.evidence = []
        self.headers = {}
        self.cookies = {}
        self.metadata = {}
        self.framework = None
        self.cms = None
        self.wordpress = {}
        self.confidence = {}
        self.dns = {}
        self.tls = {}
        self.robots = {}
        self.sitemap = []
        self.javascript = []
        self.assets = []
        self.endpoints = []
        self.forms = []
        self.comments = []
        self.emails = []
        self.interesting = []
        self.errors = []

    @staticmethod
    def _normalize_target(target: str) -> str:
        target = target.strip()
        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        return target.rstrip("/")

    def decode(self, encoding="utf-8", errors="strict"):
        return self.target

    def __str__(self):
        return self.target

    def __repr__(self):
        return f"ScanContext(target={self.target!r}, deep={self.deep!r})"

    def __contains__(self, item):
        return item in self.target

    def __iter__(self):
        return iter(self.target)

    def __len__(self):
        return len(self.target)

    def __getitem__(self, item):
        return self.target[item]

    def __bytes__(self):
        return self.target.encode("utf-8")

    def __fspath__(self):
        return self.target

    def __getattr__(self, item):
        return getattr(self.target, item)