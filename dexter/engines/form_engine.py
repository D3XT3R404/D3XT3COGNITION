from bs4 import BeautifulSoup

from dexter.core.base_engine import BaseEngine


class FormEngine(BaseEngine):

    def run(self, target):
        forms = []

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
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
