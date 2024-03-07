from typing import Optional, Union

import requests
import tinycss2

from ..resource import get_ref_as_dataurl

def expand_urls_in_css(
    css: str,
    base_url: str,
    session: Optional[requests.Session] = None,
    timeout: Union[float, tuple[float, float], None] = 900.0,
) -> str:
    rules = tinycss2.parse_stylesheet(css)

    output = ""

    for rule in rules:
        transformed = expand_urls_in_rule(rule, base_url, session, timeout)
        output += transformed.serialize()

    return output

def expand_urls_in_rule(
    rule,
    base_url: str,
    session: Optional[requests.Session] = None,
    timeout: Union[float, tuple[float, float], None] = 900.0,
):
    if type(rule) == tinycss2.ast.QualifiedRule or type(rule) == tinycss2.ast.AtRule:
        for child_rule in rule.content:
            child_rule = expand_urls_in_rule(child_rule, base_url, session, timeout)
        return rule
    elif type(rule) == tinycss2.ast.URLToken:
        data_url = get_ref_as_dataurl(base_url, rule.value, session, timeout)
        rule.representation = f'url({data_url})'
        return rule
    else:
        return rule
