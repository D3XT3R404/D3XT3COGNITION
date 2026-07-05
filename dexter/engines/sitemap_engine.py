import requests

from dexter.core.base_engine import (

    BaseEngine

)


class SitemapEngine(

    BaseEngine

):

    name = "sitemap"

    def run(

            self,

            target

    ):

        data = {}

        try:

            r = requests.get(

                f"https://{target}/sitemap.xml",

                timeout=10

            )

            data["status"] = (

                r.status_code

            )

            data["found"] = (

                r.status_code == 200

            )

        except:

            pass

        return data