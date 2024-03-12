import pytest

import requests
from requests_testadapter import TestAdapter, TestSession

from frozen_soup import freeze_to_string

@pytest.fixture
def session() -> requests.Session:
    s = TestSession()

    s.mount("http://based/content", TestAdapter(
        b'/* WONTON */',
        headers= { 'Content-type' : 'text/plain' }
    ))

    s.mount("http://test/img", TestAdapter(b'<base href="http://based"><img src="/content">'))
    s.mount("http://test/script", TestAdapter(
        b'<base href="http://based"><script src="/content"></script>'
    ))
    s.mount("http://test/stylesheet", TestAdapter(
        b'<base href="http://based"><link rel="stylesheet" href="/content">'
    ))

    s.mount("http://test/extra-base", TestAdapter(
        b'<base target="_blank"><base href="http://based"><script src="/content"></script>'
    ))

    return s

def test_base_img(session):
    out = freeze_to_string('http://test/img', session)
    assert out == '<base href="http://based"><img src="data:text/plain;base64,LyogV09OVE9OICov">'

def test_base_script(session):
    out = freeze_to_string('http://test/script', session)
    assert out == '<base href="http://based"><script>/* WONTON */</script>'

def test_base_stylesheet(session):
    out = freeze_to_string('http://test/stylesheet', session)
    assert out == '<base href="http://based"><style>/* WONTON */</style>'

def test_base_extra_base(session):
    out = freeze_to_string('http://test/extra-base', session)
    assert out == '<base target="_blank"><base href="http://based"><script>/* WONTON */</script>'
