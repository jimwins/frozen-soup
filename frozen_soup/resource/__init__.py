from typing import Optional, Union

import base64
import requests
from urllib.parse import urljoin

def get_ref_as_dataurl(
    base_url: str,
    ref_url: str,
    session: requests.Session,
    timeout: Union[float, tuple[float, float], None] = 900.0,
) -> str:
    url = urljoin(base_url, ref_url)
    response = session.get(url, timeout= timeout)
    if response.status_code == 200:
        # Encode the content to base64 - don't use urlsafe_b64encode because
        # the browser won't be passing this on to a server, and they don't
        # expect the 'URL-safe' substitutions
        encoded_content = base64.b64encode(response.content).decode("utf-8")
        # Grab the content-type from the response headers
        content_type = response.headers.get('Content-Type')
        # TODO: what if we have no content_type?
        # Return the data: URL with appropriate MIME type
        return f"data:{content_type};base64,{encoded_content}"
    else:
        raise Exception(f"Unable to generate base64-encoded value")
