import re
import requests

from dexter.core.base_engine import BaseEngine


class CommentEngine(BaseEngine):

    def run(self, target):
        result = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
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