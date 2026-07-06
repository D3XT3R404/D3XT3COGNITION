import re
import requests

from dexter.core.base_engine import BaseEngine


class VersionEngine(BaseEngine):
    def _canonical(self, name):
        if not name:
            return None

        n = re.sub(r"[^a-z0-9]+", "", str(name).lower())
        aliases = {
            "apachehttpserver": "Apache",
            "apache": "Apache",
            "nginx": "Nginx",
            "openresty": "OpenResty",
            "php": "PHP",
            "wordpress": "WordPress",
            "jquery": "jQuery",
            "bootstrap": "Bootstrap",
            "openssl": "OpenSSL",
            "microsoftiis": "IIS",
            "iis": "IIS",
        }
        return aliases.get(n, str(name).strip())

    def _split_tech(self, value):
        value = str(value).strip()
        if ":" in value and not value.startswith("http"):
            name, version = value.split(":", 1)
            return name.strip(), version.strip() or None
        return value, None

    def run(self, target):
        results = getattr(target, "results", {}) if not isinstance(target, dict) else target
        versions = {}

        try:
            response = getattr(target, "response", None)
            headers = {}

            if response is not None:
                headers = dict(response.headers)
            else:
                headers = results.get("headers", {}) if isinstance(results.get("headers", {}), dict) else {}

            server = str(headers.get("Server", ""))
            powered = str(headers.get("X-Powered-By", ""))

            patterns = [
                (r"(Apache|Nginx|OpenResty)[/ ]([\d\.]+)", server),
                (r"OpenSSL[/ ]([\d\.]+)", server),
                (r"PHP[/ ]([\d\.]+)", powered),
            ]

            for pat, text in patterns:
                m = re.search(pat, text, re.I)
                if m:
                    versions[self._canonical(m.group(1))] = m.group(2)

            httpx = results.get("httpx", {})
            if isinstance(httpx, dict):
                for item in httpx.get("items", []):
                    tech_list = item.get("tech", []) if isinstance(item, dict) else []
                    for tech in tech_list:
                        name, version = self._split_tech(tech)
                        canon = self._canonical(name)
                        if canon and version and canon not in versions:
                            versions[canon] = version

                    webserver = item.get("webserver") if isinstance(item, dict) else None
                    if webserver:
                        m = re.search(r"(Apache|Nginx|OpenResty|OpenSSL)[/ ]([\d\.]+)", webserver, re.I)
                        if m:
                            versions[self._canonical(m.group(1))] = m.group(2)

            whatweb = results.get("whatweb", {})
            if isinstance(whatweb, dict):
                for item in whatweb.get("detected", []):
                    if not isinstance(item, dict):
                        continue
                    name = self._canonical(item.get("name"))
                    version = item.get("version")
                    if name and version and name not in versions:
                        versions[name] = version

            wordpress = results.get("wordpress", {})
            if isinstance(wordpress, dict) and wordpress.get("version"):
                versions["WordPress"] = wordpress["version"]

        except Exception:
            pass

        versions = {k: v for k, v in versions.items() if k and v}
        results["versions"] = versions
        return versions