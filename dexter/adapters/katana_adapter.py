import shutil

from dexter.adapters.base_adapter import (BaseAdapter)
from dexter.adapters.base_adapter import BaseAdapter

class KatanaAdapter(BaseAdapter):

    name = "katana"

    background = True

    def available(

            self

    ):

        return (

            shutil.which(

                "katana"

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