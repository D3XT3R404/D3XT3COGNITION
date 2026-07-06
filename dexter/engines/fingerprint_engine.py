import os
import yaml
import json
import requests

from dexter.core.base_engine import BaseEngine


class FingerprintEngine(BaseEngine):
    def _load_fingerprints(self):
        base_dir = os.path.join(os.path.dirname(__file__), "..", "fingerprints")
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

    def _match_any(self, needles, haystack):
        if not needles or not haystack:
            return False
        haystack = haystack.lower()
        for needle in needles:
            if needle and str(needle).lower() in haystack:
                return True
        return False

    def run(self, target):
        results = getattr(target, "results", {}) if not isinstance(target, dict) else target
        found = []

        try:
            response = getattr(target, "response", None)
            if response is None:
                response = requests.get(str(getattr(target, "target", target)), timeout=15, allow_redirects=True)

            html = response.text.lower()
            headers_blob = "\n".join(f"{k}: {v}" for k, v in response.headers.items()).lower()
            cookie_blob = " ".join([c.name.lower() for c in response.cookies])

        except Exception:
            html = ""
            headers_blob = ""
            cookie_blob = ""

        adapter_blob = json.dumps(
            {
                "httpx": results.get("httpx", {}),
                "whatweb": results.get("whatweb", {}),
                "wordpress": results.get("wordpress", {}),
            },
            default=str,
        ).lower()

        fingerprints = self._load_fingerprints()

        for fp in fingerprints:
            name = fp.get("name")
            if not name:
                continue

            matched = False
            for field in ("keywords", "html", "headers", "cookies", "scripts", "paths", "hints"):
                values = fp.get(field, [])
                if isinstance(values, str):
                    values = [values]

                if field == "html" and self._match_any(values, html):
                    matched = True
                elif field == "headers" and self._match_any(values, headers_blob):
                    matched = True
                elif field == "cookies" and self._match_any(values, cookie_blob):
                    matched = True
                elif field == "paths" and self._match_any(values, adapter_blob):
                    matched = True
                elif field in ("keywords", "scripts", "hints") and self._match_any(values, html + "\n" + headers_blob + "\n" + adapter_blob):
                    matched = True

                if matched:
                    break

            if matched:
                found.append(name)

        found = sorted(set(found))
        results["fingerprints"] = found
        return found