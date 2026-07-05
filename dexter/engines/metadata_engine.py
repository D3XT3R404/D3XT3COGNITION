from bs4 import BeautifulSoup

from dexter.core.base_engine import BaseEngine


class MetadataEngine(BaseEngine):

    name = "metadata"

    def run(self, context):

        if context.response is None:

            return {}

        soup = BeautifulSoup(

            context.response.text,

            "html.parser"

        )

        title = ""

        if soup.title:

            title = soup.title.text.strip()

        metas = {}

        for meta in soup.find_all("meta"):

            key = meta.get(

                "name"

            ) or meta.get(

                "property"

            )

            value = meta.get(

                "content"

            )

            if key and value:

                metas[key] = value

        result = {

            "title": title,

            "meta": metas

        }

        context.metadata = result

        return result