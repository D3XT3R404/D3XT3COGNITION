import requests

from dexter.core.config import (
    TIMEOUT,
    USER_AGENT
)

def create_session():

    session = requests.Session()

    session.headers.update({
        "User-Agent": USER_AGENT
    })

    session.verify = False

    return session