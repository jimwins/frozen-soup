import pytest

import requests
from requests_testadapter import TestAdapter, TestSession

from frozen_soup import freeze_to_string

@pytest.fixture
def session() -> requests.Session:
    s = TestSession()

    s.mount("http://test/content", TestAdapter(
        b'/* WONTON */',
        headers= { 'Content-type' : 'text/plain' }
    ))

    s.mount(
        "http://test/html",
        TestAdapter(b'<i class="ko">pow!</i><img src="/content">')
    )
    s.mount(
        "http://test/multiple",
        TestAdapter(b'<i class="ko">pow!</i><b class="ko">bang!</b><img src="/content">')
    )
    s.mount(
        "http://test/bad-img",
        TestAdapter(b'<i class="ko">pow!</i><img src="/error">')
    )

    return s

def test_knockout(session):
    out = freeze_to_string('http://test/html', session, knockouts=['.ko'])
    assert out == '<img src="data:text/plain;base64,LyogV09OVE9OICov">'

def test_knockout_multiple_elements(session):
    out = freeze_to_string('http://test/multiple', session, knockouts=['.ko'])
    assert out == '<img src="data:text/plain;base64,LyogV09OVE9OICov">'

def test_knockout_multiple_selectors(session):
    out = freeze_to_string('http://test/multiple', session, knockouts=['i', 'b'])
    assert out == '<img src="data:text/plain;base64,LyogV09OVE9OICov">'

# if the knockout doesn't kill the <img> we'll get an exception
def test_knockout_img(session):
    out = freeze_to_string('http://test/bad-img', session, knockouts=['img'])
    assert out == '<i class="ko">pow!</i>'
