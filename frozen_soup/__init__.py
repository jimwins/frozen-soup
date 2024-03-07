from typing import Optional, Union

import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin
import base64

from .resource import get_ref_as_dataurl
from .css import expand_urls_in_css

def freeze_to_string(
    url: str,
    session: Optional[requests.Session] = None,
    timeout: Union[float, tuple[float, float], None] = 900.0,
    formatter: str = 'html5',
) -> str:
    if session is None:
        session = requests.Session()

    r = session.get(url, timeout= timeout)

    soup = BeautifulSoup(r.text, 'html.parser')

    # Inline images
    for img in soup.find_all('img'):
        img['src'] = get_ref_as_dataurl(url, img['src'], session, timeout)

    # Handle <link> elements
    for link in soup.find_all('link'):
        # Inline rel="icon"
        if 'icon' in link.get_attribute_list('rel'):
            link['href'] = get_ref_as_dataurl(url, link['href'], session, timeout)

        elif 'apple-touch-icon' in link.get_attribute_list('rel'):
            link['href'] = get_ref_as_dataurl(url, link['href'], session, timeout)

        elif 'apple-touch-startup-image' in link.get_attribute_list('rel'):
            link['href'] = get_ref_as_dataurl(url, link['href'], session, timeout)

        # Turn rel="stylesheet" into <style>
        elif 'stylesheet' in link.get_attribute_list('rel'):
            stylesheet_url = urljoin(url, link['href'])
            response = session.get(stylesheet_url, timeout=timeout)
            if response.status_code == 200:
                style = soup.new_tag('style')
                style.string = expand_urls_in_css(response.text, stylesheet_url, session, timeout)
                # Carry over media=""
                if link.get('media'):
                    style['media'] = link['media']
                # TODO anything else?
                link.replace_with(style)
            else:
                raise Exception(f"Unable to replace style {link['href']}")

    # Inline <script src="">
    for script in soup.find_all('script'):
        if script.get('src'):
            response = session.get(urljoin(url, script['src']), timeout=timeout)
            if response.status_code == 200:
                script.string = response.text
                # TODO what other attributes do we care about?
                # TODO parse/rewrite JavaScript to handle `import`?
                del script['src']
            else:
                raise Exception(f"Unable to replace script contents {script['src']}")

    # Should allow the caller to specify the formatter to use, html5 for now
    return soup.decode(formatter=formatter)
