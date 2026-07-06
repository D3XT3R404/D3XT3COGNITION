import requests

from dexter.core.base_engine import BaseEngine


class CmsEngine(BaseEngine):

    def run(self, target):
        cms = None

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            html = response.text.lower()

            if "wp-content" in html or "wp-includes" in html:
                cms = "WordPress"
            elif "joomla" in html:
                cms = "Joomla"
            elif "drupal" in html or "/sites/default/" in html:
                cms = "Drupal"
        except Exception:
            pass

        return cms