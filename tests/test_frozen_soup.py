import pytest
import requests
from requests_testadapter import TestAdapter, TestSession

from frozen_soup import freeze_to_string

@pytest.fixture
def session() -> requests.Session:
    s = TestSession()
    s.mount('http://test/simple-string', TestAdapter(b'Mock!'))
    return s


def test_freeze_to_string(session):
    out = freeze_to_string('http://test/simple-string', session)

    assert out == "Mock!"
