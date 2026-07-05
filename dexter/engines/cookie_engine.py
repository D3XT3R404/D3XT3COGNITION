import requests


class CookieEngine:

    def run(

            self,

            url

    ):

        try:

            r = requests.get(

                url,

                timeout=10

            )

            return [

                cookie.name

                for cookie

                in r.cookies

            ]

        except:

            return []