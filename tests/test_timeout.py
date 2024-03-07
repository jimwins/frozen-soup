import pytest

import requests
from requests_testadapter import TestAdapter, TestSession

from urllib3.exceptions import ConnectTimeoutError, ReadTimeoutError

from frozen_soup import freeze_to_string

class TimeoutTestAdapter(TestAdapter):
    def __init__(self, stream, timeout=None, status=200, headers=None):
        self.stream = stream
        self.status = status
        self.headers = headers or {}
        self.timeout = timeout
        super().__init__(stream, status, headers)

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        if type(timeout) == int:
            if (timeout < self.timeout):
                raise ConnectTimeoutError
        elif type(timeout) == tuple:
            if (timeout[0] < self.timeout):
                raise ConnectTimeoutError
            elif (timeout[1] < self.timeout):
                raise ReadTimeoutError("(dummy)", request.url, "Read timeout!")

        return super().send(request, stream, timeout, verify, cert, proxies)

@pytest.fixture
def session() -> requests.Session:
    s = TestSession()

    s.mount("http://test/long-timeout",  TimeoutTestAdapter(b'DATA', timeout= 1200))
    s.mount("http://test/short-timeout", TimeoutTestAdapter(b'DATA', timeout= 3))

    s.mount("http://test/img-contains-long-timeout", TestAdapter(b'<img src="long-timeout">'))
    s.mount("http://test/img-contains-short-timeout", TestAdapter(b'<img src="short-timeout">'))

    return s

def test_timeout_okay(session):
    out = freeze_to_string('http://test/short-timeout', session, timeout= 100)
    assert out == 'DATA'

def test_timeout_raised(session):
    with pytest.raises(ConnectTimeoutError):
        out = freeze_to_string('http://test/long-timeout', session, timeout= 100)

def test_timeout_okay_on_img(session):
    out = freeze_to_string('http://test/img-contains-short-timeout', session, timeout= 100)
    assert out == '<img src="data:None;base64,REFUQQ==">'

def test_timeout_raised_on_img(session):
    with pytest.raises(ConnectTimeoutError):
        out = freeze_to_string('http://test/img-contains-long-timeout', session, timeout= 100)

def test_timeout_tuple_okay(session):
    out = freeze_to_string('http://test/short-timeout', session, timeout= (100,100))
    assert out == 'DATA'

def test_timeout_tuple_connect_raised(session):
    with pytest.raises(ConnectTimeoutError):
        out = freeze_to_string('http://test/long-timeout', session, timeout= (100, 1200))

def test_timeout_tuple_read_raised(session):
    with pytest.raises(ReadTimeoutError):
        out = freeze_to_string('http://test/long-timeout', session, timeout= (1200, 100))
