import requests


class ScanContext:
    def __init__(self, target: str, deep: bool = False):
        if not target.startswith(("http://", "https://")):
            target = "https://" + target

        self.target = target
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

    def __getattr__(self, item):
        return getattr(self.target, item)