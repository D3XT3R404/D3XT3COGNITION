import requests

from dexter.core.base_engine import BaseEngine


class WafEngine(BaseEngine):
    def run(self, target):
        results = getattr(target, "results", {}) if not isinstance(target, dict) else target
        waf = None
        source = None
        confidence = 0

        try:
            wafw00f = results.get("wafw00f", {})
            if isinstance(wafw00f, dict) and wafw00f.get("waf"):
                waf = wafw00f.get("waf")
                source = "wafw00f"
                confidence = 95

            if not waf:
                httpx = results.get("httpx", {})
                if isinstance(httpx, dict):
                    for item in httpx.get("items", []):
                        techs = [str(t).lower() for t in item.get("tech", [])] if isinstance(item, dict) else []
                        webserver = str(item.get("webserver", "")).lower() if isinstance(item, dict) else ""
                        cdn = str(item.get("cdn", "")).lower() if isinstance(item, dict) else ""

                        if any("cloudflare" in t for t in techs) or "cloudflare" in webserver or "cloudflare" in cdn:
                            waf = "Cloudflare"
                            source = "httpx"
                            confidence = 80
                            break
                        if "akamai" in webserver:
                            waf = "Akamai"
                            source = "httpx"
                            confidence = 75
                            break
                        if "sucuri" in webserver:
                            waf = "Sucuri"
                            source = "httpx"
                            confidence = 75
                            break

            if not waf:
                headers = results.get("headers", {})
                if isinstance(headers, dict):
                    header_blob = " ".join(f"{k}:{v}" for k, v in headers.items()).lower()
                    if "cf-ray" in header_blob or "cloudflare" in header_blob:
                        waf = "Cloudflare"
                        source = "headers"
                        confidence = 70

            if not waf:
                response = getattr(target, "response", None)
                if response is None:
                    response = requests.get(str(getattr(target, "target", target)), timeout=15, allow_redirects=True)

                headers = {k.lower(): str(v).lower() for k, v in response.headers.items()}
                if "cf-ray" in headers or "cloudflare" in headers.get("server", ""):
                    waf = "Cloudflare"
                    source = "headers"
                    confidence = 70
                elif "akamai" in headers.get("server", ""):
                    waf = "Akamai"
                    source = "headers"
                    confidence = 65
                elif "sucuri" in headers.get("server", ""):
                    waf = "Sucuri"
                    source = "headers"
                    confidence = 65

        except Exception:
            pass

        result = {
            "detected": bool(waf),
            "name": waf,
            "source": source,
            "confidence": confidence,
        }

        results["waf"] = result
        return result