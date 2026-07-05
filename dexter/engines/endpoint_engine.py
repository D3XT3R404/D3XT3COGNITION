from bs4 import BeautifulSoup

from urllib.parse import urljoin

from dexter.core.base_engine import BaseEngine


class EndpointEngine(BaseEngine):

    name = "endpoints"

    TAGS = {

        "a": "href",

        "script": "src",

        "link": "href",

        "img": "src",

        "iframe": "src"

    }

    def run(self, context):

        if context.response is None:

            return []

        soup = BeautifulSoup(

            context.response.text,

            "html.parser"

        )

        endpoints = set()

        for tag, attr in self.TAGS.items():

            for node in soup.find_all(tag):

                value = node.get(attr)

                if value:

                    endpoints.add(

                        urljoin(

                            context.target,

                            value

                        )

                    )

        context.endpoints = sorted(endpoints)

        return context.endpoints