import shutil

from dexter.adapters.base_adapter import (

    BaseAdapter

)


class WhatWebAdapter(

    BaseAdapter

):

    name = "whatweb"

    background = True

    def available(

            self

    ):

        return (

            shutil.which(

                "whatweb"

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