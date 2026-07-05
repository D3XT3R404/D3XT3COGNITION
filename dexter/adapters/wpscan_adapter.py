import shutil

import subprocess

from dexter.adapters.base_adapter import (

    BaseAdapter

)


class WPScanAdapter(

    BaseAdapter

):

    name = "wpscan"

    background = True

    def available(

            self

    ):

        return (

            shutil.which(

                "wpscan"

            )

            is not None

        )

    def run(

            self,

            target

    ):

        if not self.available():

            return {

                "installed":

                    False

            }

        return {

            "installed":

                True,

            "status":

                "stub"

        }