from dexter.core.base_engine import BaseEngine


class TechnologyEngine(BaseEngine):

    name = "technology"

    SERVER_MAP = {
        "apache": "Apache",
        "nginx": "Nginx",
        "iis": "Microsoft IIS",
        "openresty": "OpenResty",
        "cloudflare": "Cloudflare"
    }

    def run(self, context):

        technologies = []

        headers = context.headers

        server = headers.get("Server", "").lower()

        powered = headers.get("X-Powered-By", "").lower()

        for key, value in self.SERVER_MAP.items():

            if key in server:
                technologies.append(value)

        if "php" in powered:
            technologies.append("PHP")

        if "asp.net" in powered:
            technologies.append("ASP.NET")

        if "express" in powered:
            technologies.append("Express")

        html = ""

        if context.response:
            html = context.response.text.lower()

        if "wp-content" in html:
            technologies.append("WordPress")

        if "/sites/default/" in html:
            technologies.append("Drupal")

        if "cdn.jsdelivr.net" in html:
            technologies.append("jsDelivr")

        if "bootstrap" in html:
            technologies.append("Bootstrap")

        if "jquery" in html:
            technologies.append("jQuery")

        if "vue" in html:
            technologies.append("Vue.js")

        if "react" in html:
            technologies.append("React")

        technologies = sorted(set(technologies))

        context.technologies = technologies

        return technologies