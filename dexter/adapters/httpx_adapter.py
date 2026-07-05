import shutil

from dexter.adapters.base_adapter import (
    BaseAdapter
)

class HTTPXAdapter(
    BaseAdapter
):
    name = "httpx"
    background = True

    def available(
            self
            ):

        return (

            shutil.which(

                "httpx"

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

                True

        }