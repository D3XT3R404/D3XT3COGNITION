from dexter.core.base_engine import BaseEngine


class CookieEngine(BaseEngine):

    name = "cookies"

    def run(self, context):

        if context.response is None:

            return {}

        cookies = {}

        for cookie in context.response.cookies:

            cookies[cookie.name] = cookie.value

        context.cookies = cookies

        return cookies