from typing import Optional

import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin
import base64

def _get_ref_as_dataurl(base_url: str, ref_url: str, session: requests.Session) -> str:
    url = urljoin(base_url, ref_url)
    response = session.get(url)
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

def freeze_to_string(
    url: str,
    session: Optional[requests.Session] = None,
    formatter: str = 'html5'
) -> str:
    if session is None:
        session = requests.Session()

    r = session.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    # Inline images
    for img in soup.find_all('img'):
        img['src'] = _get_ref_as_dataurl(url, img['src'], session)

    # Handle <link> elements
    for link in soup.find_all('link'):
        # Inline rel="icon"
        if 'icon' in link.get_attribute_list('rel'):
            link['href'] = _get_ref_as_dataurl(url, link['href'], session)

        # Turn rel="stylesheet" into <style>
        if 'stylesheet' in link.get_attribute_list('rel'):
            response = session.get(urljoin(url, link['href']))
            if response.status_code == 200:
                style = soup.new_tag('style')
                style.string = response.text
                # Carry over media=""
                if link.get('media'):
                    style['media'] = link['media']
                # TODO anything else?
                # TODO should replace url() in CSS with data URLs
                link.replace_with(style)
            else:
                raise Exception(f"Unable to replace style {link['href']}")

    # Inline <script src="">
    for script in soup.find_all('script'):
        if script.get('src'):
            response = session.get(urljoin(url, script['src']))
            if response.status_code == 200:
                script.string = response.text
                # TODO what other attributes do we care about?
                # TODO parse/rewrite JavaScript to handle `import`?
                del script['src']
            else:
                raise Exception(f"Unable to replace script contents {script['src']}")

    # Should allow the caller to specify the formatter to use, html5 for now
    return soup.decode(formatter=formatter)
