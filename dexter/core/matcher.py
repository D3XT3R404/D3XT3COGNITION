class Matcher:

    def match(

            self,

            fp,

            html,

            cookies,

            headers

    ):

        score = 0

        evidence = []

        ################################

        for item in fp.get(

                "html",

                []

        ):

            if item.lower() in html:

                score += 25

                evidence.append(

                    item

                )

        ################################

        for item in fp.get(

                "cookies",

                []

        ):

            if item in cookies:

                score += 25

                evidence.append(

                    item

                )

        ################################

        for item in fp.get(

                "headers",

                []

        ):

            if item in headers:

                score += 25

                evidence.append(

                    item

                )

        ################################

        return {

            "score":

                score,

            "evidence":

                evidence

        }