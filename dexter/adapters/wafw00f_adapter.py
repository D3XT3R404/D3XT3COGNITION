import shutil

from dexter.adapters.base_adapter import (

    BaseAdapter

)


class WAFW00FAdapter(

    BaseAdapter

):

    name = "wafw00f"

    background = True

    def available(

            self

    ):

        return (

            shutil.which(

                "wafw00f"

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