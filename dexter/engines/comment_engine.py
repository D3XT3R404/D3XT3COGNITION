import re

from dexter.core.base_engine import BaseEngine


class CommentEngine(BaseEngine):

    def run(self, target):
        result = []

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
            html = response.text

            comments = re.findall(r"<!--(.*?)-->", html, re.S)

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
                "token",
            ]

            for comment in comments:
                for keyword in keywords:
                    if keyword.lower() in comment.lower():
                        result.append({
                            "keyword": keyword,
                            "comment": comment.strip(),
                        })
        except Exception:
            pass

        return result
