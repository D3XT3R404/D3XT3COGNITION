import re

from dexter.core.base_engine import BaseEngine


class CommentEngine(BaseEngine):

    name = "comments"

    def run(self, context):

        if context.response is None:

            return []

        html = context.response.text

        comments = re.findall(

            r"<!--(.*?)-->",

            html,

            re.S

        )

        result = []

        keywords = [

            "todo",

            "fixme",

            "password",

            "admin",

            "secret",

            "debug",

            "staging",

            "internal",

            "api",

            "token"

        ]

        for comment in comments:

            for keyword in keywords:

                if keyword.lower() in comment.lower():

                    result.append({

                        "keyword": keyword,

                        "comment": comment.strip()

                    })

        context.comments = result

        return result