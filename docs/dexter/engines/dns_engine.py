import socket

from dexter.core.base_engine import BaseEngine


class DnsEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            host = target.replace("https://", "").replace("http://", "").split("/")[0]
            ip = socket.gethostbyname(host)
            data["ip"] = ip
        except Exception:
            pass

        return data