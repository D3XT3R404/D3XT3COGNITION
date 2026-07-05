import shutil

from dexter.adapters.base_adapter import (

    BaseAdapter

)


class SubfinderAdapter(

    BaseAdapter

):

    name = "subfinder"

    background = True

    def available(

            self

    ):

        return (

            shutil.which(

                "subfinder"

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