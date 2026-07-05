import requests

from dexter.core.base_engine import (

    BaseEngine

)


class WAFEngine(

    BaseEngine

):

    name = "waf"

    def run(

            self,

            target

    ):

        waf = []

        try:

            r = requests.get(

                f"https://{target}",

                timeout=10

            )

            server = (

                r.headers.get(

                    "server",

                    ""

                )

            ).lower()

            if "cloudflare" in server:

                waf.append(

                    "Cloudflare"

                )

            if "sucuri" in server:

                waf.append(

                    "Sucuri"

                )

        except:

            pass

        return waf