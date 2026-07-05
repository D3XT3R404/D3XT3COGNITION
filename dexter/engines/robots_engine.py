import requests

from dexter.core.base_engine import (

    BaseEngine

)


class RobotsEngine(

    BaseEngine

):

    name = "robots"

    def run(

            self,

            target

    ):

        result = {}

        try:

            r = requests.get(

                f"https://{target}/robots.txt",

                timeout=10

            )

            result["status"] = (

                r.status_code

            )

            result["found"] = (

                r.status_code == 200

            )

        except:

            pass

        return result