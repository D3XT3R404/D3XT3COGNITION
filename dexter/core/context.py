import requests


class ScanContext:

    def __init__(self, target: str):

        if not target.startswith(("http://", "https://")):
            target = "https://" + target

        self.target = target

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

        self.errors = []

        self.evidence = []

        self.endpoints = []

        self.javascript = []

        self.assets = []

        self.emails = []

        self.comments = []

        self.forms = []

        self.interesting = []