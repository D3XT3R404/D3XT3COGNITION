import re
import requests

from dexter.core.base_engine import BaseEngine


class TechnologyEngine(BaseEngine):
    SERVER_MAP = {
        "apache": "Apache",
        "nginx": "Nginx",
        "openresty": "OpenResty",
        "iis": "Microsoft IIS",
        "cloudflare": "Cloudflare",
        "openssl": "OpenSSL",
    }

    def _canonical(self, name):
        if not name:
            return None

        n = re.sub(r"[^a-z0-9]+", "", str(name).lower())

        aliases = {
            "apachehttpserver": "Apache",
            "apache": "Apache",
            "nginx": "Nginx",
            "openresty": "OpenResty",
            "microsoftiis": "Microsoft IIS",
            "iis": "Microsoft IIS",
            "php": "PHP",
            "wordpress": "WordPress",
            "jquery": "jQuery",
            "bootstrap": "Bootstrap",
            "elementor": "Elementor",
            "livewire": "Livewire",
            "alpinejs": "Alpine.js",
            "vuejs": "Vue.js",
            "react": "React",
            "cloudflare": "Cloudflare",
            "openssl": "OpenSSL",
            "drupal": "Drupal",
            "joomla": "Joomla",
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
        technologies = []
        versions = {}

        try:
            response = getattr(target, "response", None)
            headers = {}

            if response is not None:
                headers = dict(response.headers)
                html = response.text.lower()
            else:
                headers = results.get("headers", {}) if isinstance(results.get("headers", {}), dict) else {}
                html = ""

            server = str(headers.get("Server", "")).lower()
            powered = str(headers.get("X-Powered-By", "")).lower()

            for key, value in self.SERVER_MAP.items():
                if key in server:
                    technologies.append(value)

            if "php" in powered:
                technologies.append("PHP")
                m = re.search(r"PHP[/ ]([\d\.]+)", str(headers.get("X-Powered-By", "")), re.I)
                if m:
                    versions["PHP"] = m.group(1)

            if "asp.net" in powered:
                technologies.append("ASP.NET")

            if "wp-content" in html or "wp-includes" in html:
                technologies.append("WordPress")

            if "drupal" in html or "/sites/default/" in html:
                technologies.append("Drupal")

            if "joomla" in html:
                technologies.append("Joomla")

            if "bootstrap" in html:
                technologies.append("Bootstrap")

            if "jquery" in html:
                technologies.append("jQuery")

            if "vue" in html:
                technologies.append("Vue.js")

            if "react" in html:
                technologies.append("React")

            if "alpine" in html:
                technologies.append("Alpine.js")

            if "livewire" in html:
                technologies.append("Livewire")

            httpx = results.get("httpx", {})
            if isinstance(httpx, dict):
                for item in httpx.get("items", []):
                    tech_list = item.get("tech", []) if isinstance(item, dict) else []
                    for tech in tech_list:
                        name, version = self._split_tech(tech)
                        canon = self._canonical(name)
                        if canon:
                            technologies.append(canon)
                        if canon and version and canon not in versions:
                            versions[canon] = version

                    webserver = item.get("webserver") if isinstance(item, dict) else None
                    if webserver:
                        name, version = self._split_tech(webserver)
                        canon = self._canonical(name)
                        if canon:
                            technologies.append(canon)
                        if canon and version and canon not in versions:
                            versions[canon] = version

            whatweb = results.get("whatweb", {})
            if isinstance(whatweb, dict):
                for item in whatweb.get("detected", []):
                    if not isinstance(item, dict):
                        continue
                    name = self._canonical(item.get("name"))
                    version = item.get("version")
                    if name:
                        technologies.append(name)
                    if name and version and name not in versions:
                        versions[name] = version

            wordpress = results.get("wordpress", {})
            if isinstance(wordpress, dict) and wordpress.get("detected"):
                technologies.append("WordPress")

        except Exception:
            pass

        technologies = sorted(set(filter(None, technologies)))
        results["technology"] = technologies
        if versions:
            results.setdefault("versions", {}).update(versions)
        return technologies