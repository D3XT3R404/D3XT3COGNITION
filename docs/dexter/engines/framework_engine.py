from dexter.core.base_engine import BaseEngine


class FrameworkEngine(BaseEngine):

    def run(self, target):
        framework = None

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
            html = response.text.lower()
            headers = response.headers
            cookies = response.cookies

            cookie_names = {c.name.lower() for c in cookies}

            if "laravel_session" in cookie_names or "xsrf-token" in cookie_names:
                framework = "Laravel"
            elif "__next" in html:
                framework = "Next.js"
            elif "__nuxt" in html:
                framework = "Nuxt"
            elif "django" in headers.get("Server", "").lower():
                framework = "Django"
            elif "express" in headers.get("X-Powered-By", "").lower():
                framework = "Express"
            elif "livewire" in html:
                framework = "Laravel"
        except Exception:
            pass

        return framework
