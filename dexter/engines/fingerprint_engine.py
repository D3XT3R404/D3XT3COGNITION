import os
import yaml
import requests

from dexter.core.base_engine import BaseEngine


class FingerprintEngine(BaseEngine):

    def _load_fingerprints(self):
        base_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "fingerprints",
        )

        fingerprints = []

        for root, _, files in os.walk(base_dir):
            for file in files:
                if not file.endswith(".yaml"):
                    continue

                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        item = yaml.safe_load(f)
                        if item:
                            fingerprints.append(item)
                except Exception:
                    pass

        return fingerprints

    def run(self, target):
        found = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            html = response.text.lower()
            headers = response.headers
            cookie_names = []
            try:
                cookie_names = [c.name.lower() for c in response.cookies]
            except Exception:
                cookie_names = []
        except Exception:
            html = ""
            headers = {}
            cookie_names = []

        fingerprints = self._load_fingerprints()

        for fp in fingerprints:
            name = fp.get("name")
            if not name:
                continue

            keywords = fp.get("keywords", [])
            hints = fp.get("hints", [])

            matched = False
            for kw in keywords + hints:
                if kw and kw.lower() in html:
                    matched = True
                    break

            if not matched:
                for key, value in headers.items():
                    text = f"{key}: {value}".lower()
                    for kw in keywords + hints:
                        if kw and kw.lower() in text:
                            matched = True
                            break
                    if matched:
                        break

            if not matched:
                for ck in cookie_names:
                    for kw in keywords + hints:
                        if kw and kw.lower() in ck:
                            matched = True
                            break
                    if matched:
                        break

            if matched:
                found.append(name)

        return sorted(set(found))