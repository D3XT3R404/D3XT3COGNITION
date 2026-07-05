from dexter.core.base_engine import BaseEngine


class FrameworkEngine(BaseEngine):

    name = "framework"

    def run(self, context):

        framework = None

        cookies = context.cookies

        html = ""

        if context.response:
            html = context.response.text.lower()

        headers = context.headers

        if "laravel_session" in cookies:
            framework = "Laravel"

        elif "xsrf-token" in cookies:
            framework = "Laravel"

        elif "__next" in html:
            framework = "Next.js"

        elif "__nuxt" in html:
            framework = "Nuxt"

        elif "django" in headers.get("Server", "").lower():
            framework = "Django"

        elif "express" in headers.get("X-Powered-By", "").lower():
            framework = "Express"

        context.framework = framework

        return framework