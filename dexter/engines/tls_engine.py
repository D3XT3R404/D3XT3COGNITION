import socket
import ssl

from dexter.core.base_engine import BaseEngine


class TlsEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            host = target.replace("https://", "").replace("http://", "").split("/")[0]
            ctx = ssl.create_default_context()

            with socket.create_connection((host, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert() or {}

                    data["version"] = ssock.version()
                    data["cipher"] = ssock.cipher()
                    data["issuer"] = cert.get("issuer", [])
                    data["subject"] = cert.get("subject", [])
        except Exception:
            pass

        return data