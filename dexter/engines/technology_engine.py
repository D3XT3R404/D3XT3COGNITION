import requests

from dexter.core.base_engine import BaseEngine


class TechnologyEngine(BaseEngine):

    SERVER_MAP = {
        "apache": "Apache",
        "nginx": "Nginx",
        "iis": "Microsoft IIS",
        "openresty": "OpenResty",
        "cloudflare": "Cloudflare",
    }

    def run(self, target):
        technologies = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            headers = response.headers
            server = headers.get("Server", "").lower()
            powered = headers.get("X-Powered-By", "").lower()
            html = response.text.lower()

            for key, value in self.SERVER_MAP.items():
                if key in server:
                    technologies.append(value)

            if "php" in powered:
                technologies.append("PHP")
            if "asp.net" in powered:
                technologies.append("ASP.NET")
            if "express" in powered:
                technologies.append("Express")

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
        except Exception:
            pass

        return sorted(set(technologies))