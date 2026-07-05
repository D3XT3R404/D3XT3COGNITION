import requests


class HeaderEngine:

    def run(

            self,

            url

    ):

        try:

            r = requests.get(

                url,

                timeout=10

            )

            return dict(

                r.headers

            )

        except:

            return {}