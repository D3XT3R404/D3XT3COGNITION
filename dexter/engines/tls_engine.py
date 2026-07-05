import socket

import ssl

from dexter.core.base_engine import (

    BaseEngine

)


class TLSEngine(

    BaseEngine

):

    name = "tls"

    def run(

            self,

            target

    ):

        data = {}

        try:

            context = (

                ssl.create_default_context()

            )

            with socket.create_connection(

                    (

                        target,

                        443

                    ),

                    timeout=10

            ) as sock:

                with context.wrap_socket(

                        sock,

                        server_hostname=target

                ) as ssock:

                    cert = (

                        ssock.getpeercert()

                    )

                    data["version"] = (

                        ssock.version()

                    )

                    data["cipher"] = (

                        ssock.cipher()

                    )

                    data["issuer"] = (

                        cert.get(

                            "issuer",

                            []

                        )

                    )

                    data["subject"] = (

                        cert.get(

                            "subject",

                            []

                        )

                    )

        except:

            pass

        return data