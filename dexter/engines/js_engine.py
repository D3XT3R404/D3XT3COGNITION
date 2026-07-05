import requests

from bs4 import BeautifulSoup

from dexter.core.base_engine import (

    BaseEngine

)


class JSEngine(

    BaseEngine

):

    name = "javascript"

    def run(

            self,

            target

    ):

        libraries = []

        try:

            r = requests.get(

                f"https://{target}",

                timeout=10

            )

            soup = BeautifulSoup(

                r.text,

                "html.parser"

            )

            scripts = soup.find_all(

                "script"

            )

            for script in scripts:

                src = script.get(

                    "src",

                    ""

                ).lower()

                if "jquery" in src:

                    libraries.append(

                        "jQuery"

                    )

                if "bootstrap" in src:

                    libraries.append(

                        "Bootstrap"

                    )

        except:

            pass

        return list(

            set(

                libraries

            )

        )