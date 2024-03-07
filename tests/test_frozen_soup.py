import pytest

import requests
from requests_testadapter import TestAdapter, TestSession

from frozen_soup import freeze_to_string

@pytest.fixture
def session() -> requests.Session:
    s = TestSession()
    s.mount('http://test/simple-string', TestAdapter(b'Alive!'))

    s.mount(
        "http://test/1x1.gif",
        TestAdapter(
            stream= open("tests/test_data/1x1.gif", "rb").read(),
            headers= {
                'Content-type': 'image/gif',
            },
        ),
    )
    s.mount("http://test/bad.gif", TestAdapter(b'BAD', status=404))
    s.mount("http://test/html-one-image", TestAdapter(b'<img src="/1x1.gif">'))
    s.mount("http://test/html-bad-image", TestAdapter(b'<img src="/bad.gif">'))

    s.mount(
        "http://test/style.css",
        TestAdapter(b'* { color: white }', headers= { 'Content-type': 'text/css' })
    )
    s.mount(
        "http://test/urls.css",
        TestAdapter(
            b'* { background: url(1x1.gif) } @media screen { background: url(1x1.gif) }',
            headers = { 'Content-type': 'text/css' }
        )
    )

    s.mount("http://test/html-link-icon", TestAdapter(b'<link rel="icon" href="1x1.gif">'))
    s.mount("http://test/html-link-style", TestAdapter(b'<link rel="stylesheet" href="style.css">'))
    s.mount(
        "http://test/html-link-style-urls",
        TestAdapter(b'<link rel="stylesheet" href="urls.css">')
    )

    s.mount(
        "http://test/code.js",
        TestAdapter(b'/* Code! */', headers= { 'Content-type': 'application/javascript' })
    )

    s.mount("http://test/html-script", TestAdapter(b'<script src="code.js"></script>'))

    # Not really data, but we're just testing to see it doesn't get mangled
    s.mount("http://test/already-data-url", TestAdapter(b'<img src="data:foo;bar:baz">'))

    return s


def test_freeze_to_string(session):
    out = freeze_to_string('http://test/simple-string', session)

    assert out == 'Alive!'


@pytest.fixture
def data_url():
    return "data:image/gif;base64,R0lGODlhAQABAIAAAMRUFwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="

def test_single_image(session, data_url):
    out = freeze_to_string('http://test/html-one-image', session)

    assert out == f'<img src="{data_url}">'

def test_single_image_as_xhtml(session, data_url):
    out = freeze_to_string('http://test/html-one-image', session, formatter='html')

    assert out == f'<img src="{data_url}"/>'

def test_bad_image(session):
    with pytest.raises(Exception):
        out = freeze_to_string('http://test/html-bad-image', session)

def test_link_icon(session, data_url):
    out = freeze_to_string('http://test/html-link-icon', session)

    assert out == f'<link href="{data_url}" rel="icon">'

def test_link_style(session):
    out = freeze_to_string('http://test/html-link-style', session)

    assert out == '<style>* { color: white }</style>'

def test_link_style_urls(session, data_url):
    out = freeze_to_string('http://test/html-link-style-urls', session)

    assert out == f'<style>* {{ background: url({data_url}) }} @media screen {{ background: url({data_url}) }}</style>'

def test_script(session):
    out = freeze_to_string('http://test/html-script', session)

    assert out == '<script>/* Code! */</script>';

def test_already_data_url(session):
    out = freeze_to_string('http://test/already-data-url', session)

    assert out == '<img src="data:foo;bar:baz">';
