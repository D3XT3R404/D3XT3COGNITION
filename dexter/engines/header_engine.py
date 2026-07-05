import requests

from dexter.core.base_engine import BaseEngine


class HeaderEngine(BaseEngine):

    name = "headers"

    def run(self, context):

        response = requests.get(

            context.target,

            timeout=10,

            allow_redirects=True

        )

        context.response = response

        context.headers = dict(

            response.headers

        )

        return context.headers