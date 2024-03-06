from typing import Optional

import requests

def freeze_to_string(url: str, session: Optional[requests.Session]) -> str:
    if session is None:
        session = requests.Session()

    r = session.get(url)
    return r.text
