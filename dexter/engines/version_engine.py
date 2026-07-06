import re
import requests

from dexter.core.base_engine import BaseEngine


class VersionEngine(BaseEngine):

    def run(self, target):
        versions = {}

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            server = response.headers.get("Server", "")
            powered = response.headers.get("X-Powered-By", "")

            m = re.search(r"(Apache|nginx|OpenResty)[/ ]([\d\.]+)", server, re.I)
            if m:
                versions[m.group(1)] = m.group(2)

            php = re.search(r"PHP[/ ]([\d\.]+)", powered, re.I)
            if php:
                versions["PHP"] = php.group(1)
        except Exception:
            pass

        return versions