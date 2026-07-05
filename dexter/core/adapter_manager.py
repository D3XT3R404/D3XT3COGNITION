from dexter.adapters.wpscan_adapter import (

    WPScanAdapter

)

from dexter.adapters.whatweb_adapter import (

    WhatWebAdapter

)

from dexter.adapters.httpx_adapter import (

    HTTPXAdapter

)
from dexter.adapters.katana_adapter import (

    KatanaAdapter

)

from dexter.adapters.wafw00f_adapter import (

    WAFW00FAdapter

)

from dexter.adapters.subfinder_adapter import (

    SubfinderAdapter

)


class AdapterManager:

    def __init__(

            self

    ):
    
        self.adapters = [

    WPScanAdapter(),

    WhatWebAdapter(),

    HTTPXAdapter(),

    KatanaAdapter(),

    WAFW00FAdapter(),

    SubfinderAdapter()

]

    def run(

            self,

            target

    ):

        data = {}

        for adapter in self.adapters:

            data[

                adapter.name

            ] = adapter.run(

                target

            )

        return data