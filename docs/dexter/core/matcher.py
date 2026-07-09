import re


class Matcher:

    @staticmethod
    def regex(pattern, text):

        try:
            return re.search(
                pattern,
                text,
                re.I
            )

        except Exception:
            return None

    @staticmethod
    def contains(keyword, text):

        return keyword.lower() in text.lower()