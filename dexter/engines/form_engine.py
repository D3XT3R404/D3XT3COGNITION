from bs4 import BeautifulSoup
import requests

from dexter.core.base_engine import BaseEngine


class FormEngine(BaseEngine):

    def run(self, target):
        forms = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")

            for form in soup.find_all("form"):
                forms.append({
                    "action": form.get("action"),
                    "method": form.get("method", "GET").upper(),
                    "inputs": len(form.find_all("input")),
                })
        except Exception:
            pass

        return forms