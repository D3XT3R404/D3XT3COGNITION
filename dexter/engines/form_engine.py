from bs4 import BeautifulSoup

from dexter.core.base_engine import BaseEngine


class FormEngine(BaseEngine):

    name = "forms"

    def run(self, context):

        if context.response is None:

            return []

        soup = BeautifulSoup(

            context.response.text,

            "html.parser"

        )

        forms = []

        for form in soup.find_all("form"):

            forms.append({

                "action": form.get("action"),

                "method": form.get("method", "GET").upper(),

                "inputs": len(

                    form.find_all("input")

                )

            })

        context.forms = forms

        return forms