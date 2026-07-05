import re

from dexter.core.base_engine import BaseEngine


class EmailEngine(BaseEngine):

    name = "emails"

    def run(self, context):

        if context.response is None:

            return []

        emails = list(

            set(

                re.findall(

                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

                    context.response.text

                )

            )

        )

        context.emails = emails

        return emails