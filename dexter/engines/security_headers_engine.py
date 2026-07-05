from dexter.core.base_engine import BaseEngine


class SecurityHeadersEngine(BaseEngine):

    name = "security_headers"

    SECURITY_HEADERS = [

        "Content-Security-Policy",

        "Strict-Transport-Security",

        "X-Frame-Options",

        "X-Content-Type-Options",

        "Referrer-Policy",

        "Permissions-Policy"

    ]

    def run(self, context):

        if context.response is None:

            return {}

        headers = {}

        for header in self.SECURITY_HEADERS:

            headers[header] = context.response.headers.get(

                header,

                "Missing"

            )

        return headers