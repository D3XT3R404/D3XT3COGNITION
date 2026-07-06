import re
import requests

from dexter.core.base_engine import BaseEngine


class WordpressEngine(BaseEngine):

    def run(self, target):

        result = {
            "detected": False,
            "version": None,
            "theme": None,
            "plugins": [],
            "xmlrpc": False,
            "rest_api": False,
            "readme": False,
            "license": False,
            "wp_cron": False,
            "generator": None
        }

        if not target.startswith("http://") and not target.startswith("https://"):
            url = "https://" + target
        else:
            url = target

        session = requests.Session()
        session.headers.update({
            "User-Agent": "DEXTER/0.1"
        })

        try:

            response = session.get(
                url,
                timeout=10,
                verify=False
            )

            html = response.text

        except Exception:

            return result

        ##########################
        # WordPress Detection
        ##########################

        indicators = [
            "/wp-content/",
            "/wp-includes/",
            "wp-json",
            "wordpress"
        ]

        if any(i.lower() in html.lower() for i in indicators):
            result["detected"] = True

        ##########################
        # Generator Version
        ##########################

        m = re.search(
            r'content="WordPress\s*([0-9.]+)',
            html,
            re.I
        )

        if m:
            result["version"] = m.group(1)
            result["generator"] = m.group(0)

        ##########################
        # Theme
        ##########################

        theme = re.search(
            r"/wp-content/themes/([^/]+)/",
            html
        )

        if theme:
            result["theme"] = theme.group(1)

        ##########################
        # Plugins
        ##########################

        plugins = re.findall(
            r"/wp-content/plugins/([^/]+)/",
            html
        )

        result["plugins"] = sorted(set(plugins))

        ##########################
        # REST API
        ##########################

        try:

            r = session.get(
                url.rstrip("/") + "/wp-json/",
                timeout=5,
                verify=False
            )

            result["rest_api"] = (
                r.status_code == 200
            )

        except Exception:
            pass

        ##########################
        # XMLRPC
        ##########################

        try:

            r = session.get(
                url.rstrip("/") + "/xmlrpc.php",
                timeout=5,
                verify=False
            )

            result["xmlrpc"] = (
                r.status_code in [200, 405]
            )

        except Exception:
            pass

        ##########################
        # readme.html
        ##########################

        try:

            r = session.get(
                url.rstrip("/") + "/readme.html",
                timeout=5,
                verify=False
            )

            result["readme"] = (
                r.status_code == 200
            )

        except Exception:
            pass

        ##########################
        # license.txt
        ##########################

        try:

            r = session.get(
                url.rstrip("/") + "/license.txt",
                timeout=5,
                verify=False
            )

            result["license"] = (
                r.status_code == 200
            )

        except Exception:
            pass

        ##########################
        # wp-cron
        ##########################

        try:

            r = session.get(
                url.rstrip("/") + "/wp-cron.php",
                timeout=5,
                verify=False
            )

            result["wp_cron"] = (
                r.status_code == 200
            )

        except Exception:
            pass

        return result