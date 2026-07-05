import socket

from dexter.core.base_engine import (

    BaseEngine

)


class DNSEngine(

    BaseEngine

):

    name = "dns"

    def run(

            self,

            target

    ):

        data = {}

        try:

            ip = socket.gethostbyname(

                target

            )

            data["ip"] = ip

        except:

            pass

        return data