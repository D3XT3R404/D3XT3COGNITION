import requests

from dexter.core.base_engine import (

    BaseEngine

)


class FrameworkEngine(

    BaseEngine

):

    name = "framework"

    def run(

            self,

            target

    ):

        findings = []

        try:

            r = requests.get(

                f"https://{target}",

                timeout=10

            )

            html = r.text.lower()

            cookies = str(

                r.cookies

            )

            if "laravel_session" in cookies:

                findings.append(

                    "Laravel"

                )

            if "__next" in html:

                findings.append(

                    "NextJS"

                )

            if "react" in html:

                findings.append(

                    "React"

                )

            if "vue" in html:

                findings.append(

                    "Vue"

                )

        except:

            pass

        return findings