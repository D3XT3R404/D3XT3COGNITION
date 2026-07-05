import requests

from dexter.core.base_engine import (

    BaseEngine

)


class SecurityHeadersEngine(

    BaseEngine

):

    name = "security_headers"

    def run(

            self,

            target

    ):

        findings = {}

        headers = [

            "Content-Security-Policy",

            "Strict-Transport-Security",

            "X-Frame-Options",

            "X-Content-Type-Options"

        ]

        try:

            r = requests.get(

                f"https://{target}",

                timeout=10

            )

            for h in headers:

                findings[h] = (

                    h in r.headers

                )

        except:

            pass

        return findings