import requests

from bs4 import BeautifulSoup

from dexter.core.base_engine import (

    BaseEngine

)


class MetadataEngine(

    BaseEngine

):

    name = "metadata"

    def run(

            self,

            target

    ):

        data = {}

        try:

            r = requests.get(

                f"https://{target}",

                timeout=10

            )

            soup = BeautifulSoup(

                r.text,

                "html.parser"

            )

            if soup.title:

                data["title"] = (

                    soup.title.text

                )

            generator = soup.find(

                "meta",

                attrs={

                    "name":

                        "generator"

                }

            )

            if generator:

                data["generator"] = (

                    generator.get(

                        "content"

                    )

                )

        except:

            pass

        return data