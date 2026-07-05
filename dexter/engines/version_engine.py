import re


class VersionEngine:

    name = "version"

    def detect_server(

            self,

            headers

    ):

        server = headers.get(

            "server",

            ""

        )

        m = re.search(

            r'([A-Za-z]+)/([\d\.]+)',

            server

        )

        if m:

            return {

                "name":

                    m.group(1),

                "version":

                    m.group(2)

            }

        return None


    def detect_generator(

            self,

            metadata

    ):

        generator = metadata.get(

            "generator",

            ""

        )

        m = re.search(

            r'([A-Za-z]+)\s([\d\.]+)',

            generator

        )

        if m:

            return {

                "name":

                    m.group(1),

                "version":

                    m.group(2)

            }

        return None


    def run(

            self,

            findings

    ):

        versions = []

        headers = findings.get(

            "headers",

            {}

        )

        metadata = findings.get(

            "metadata",

            {}

        )

        server = self.detect_server(

            headers

        )

        if server:

            versions.append(

                server

            )

        gen = self.detect_generator(

            metadata

        )

        if gen:

            versions.append(

                gen

            )

        return versions