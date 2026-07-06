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