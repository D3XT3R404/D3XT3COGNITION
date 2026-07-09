import re
import requests
from bs4 import BeautifulSoup

from dexter.core.base_engine import BaseEngine


class WordpressEngine(BaseEngine):
    def run(self, target):
        results = getattr(target, "results", {}) if not isinstance(target, dict) else target
        url = str(getattr(target, "target", target)).rstrip("/")

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
            "generator": None,
        }

        session = requests.Session()
        session.headers.update({"User-Agent": "DEXTER/0.1"})

        try:
            response = session.get(url, timeout=15, allow_redirects=True)
            html = response.text
            html_lower = html.lower()
            headers = response.headers

            soup = BeautifulSoup(html, "html.parser")

            if any(x in html_lower for x in ["/wp-content/", "/wp-includes/", "wp-json", "wordpress"]):
                result["detected"] = True

            link_header = str(headers.get("Link", "")).lower()
            if "/wp-json/" in link_header:
                result["detected"] = True

            generator = soup.find("meta", attrs={"name": "generator"})
            if generator and generator.get("content"):
                content = generator.get("content").strip()
                if "wordpress" in content.lower():
                    result["generator"] = content
                    m = re.search(r"wordpress\s*([0-9]+(?:\.[0-9]+)*)", content, re.I)
                    if m:
                        result["version"] = m.group(1)

            theme = re.search(r"/wp-content/themes/([^/]+)/", html, re.I)
            if theme:
                result["theme"] = theme.group(1)

            plugins = re.findall(r"/wp-content/plugins/([^/]+)/", html, re.I)
            result["plugins"] = sorted(set(plugins))

            try:
                r = session.get(url + "/wp-json/", timeout=10, allow_redirects=True)
                result["rest_api"] = r.status_code == 200
            except Exception:
                pass

            try:
                r = session.get(url + "/xmlrpc.php", timeout=10, allow_redirects=True)
                result["xmlrpc"] = r.status_code in (200, 405)
            except Exception:
                pass

            try:
                r = session.get(url + "/readme.html", timeout=10, allow_redirects=True)
                result["readme"] = r.status_code == 200
            except Exception:
                pass

            try:
                r = session.get(url + "/license.txt", timeout=10, allow_redirects=True)
                result["license"] = r.status_code == 200
            except Exception:
                pass

            try:
                r = session.get(url + "/wp-cron.php", timeout=10, allow_redirects=True)
                result["wp_cron"] = r.status_code == 200
            except Exception:
                pass

            wpscan = results.get("wpscan", {})
            if isinstance(wpscan, dict):
                wp = wpscan.get("wordpress", {})
                if isinstance(wp, dict):
                    if wp.get("version") and not result["version"]:
                        result["version"] = wp.get("version")
                    if wp.get("theme") and not result["theme"]:
                        result["theme"] = wp.get("theme")
                    if wp.get("plugins"):
                        result["plugins"] = sorted(set(result["plugins"]) | set(wp.get("plugins", [])))
                    if wp.get("themes") and not result["theme"]:
                        result["theme"] = wp.get("themes", [None])[0]

            httpx = results.get("httpx", {})
            if isinstance(httpx, dict):
                for item in httpx.get("items", []):
                    if not isinstance(item, dict):
                        continue
                    if any("wordpress" in str(t).lower() for t in item.get("tech", [])):
                        result["detected"] = True

            whatweb = results.get("whatweb", {})
            if isinstance(whatweb, dict):
                for item in whatweb.get("detected", []):
                    if isinstance(item, dict) and str(item.get("name", "")).lower() == "wordpress":
                        result["detected"] = True

        except Exception:
            pass

        result["plugins"] = sorted(set(result["plugins"]))
        result["detected"] = bool(
            result["detected"]
            or result["version"]
            or result["theme"]
            or result["plugins"]
            or result["xmlrpc"]
            or result["rest_api"]
        )

        results["wordpress"] = result
        return result