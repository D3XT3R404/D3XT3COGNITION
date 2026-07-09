from concurrent.futures import (

    ThreadPoolExecutor

)

from concurrent.futures import (

    as_completed

)


class TaskManager:

    def __init__(

            self,

            workers=5

    ):

        self.executor = (

            ThreadPoolExecutor(

                max_workers=workers

            )

        )

    def run(

            self,

            jobs

    ):

        futures = []

        for job in jobs:

            futures.append(

                self.executor.submit(

                    job["func"],

                    *job["args"]

                )

            )

        results = []

        for future in as_completed(

                futures

        ):

            try:

                results.append(

                    future.result()

                )

            except:

                pass

        return results