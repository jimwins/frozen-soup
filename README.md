# frozen-soup

[![PyPI](https://img.shields.io/pypi/v/frozen-soup.svg)](https://pypi.org/project/frozen-soup/)
[![Tests](https://github.com/jimwins/frozen-soup/actions/workflows/test.yml/badge.svg)](https://github.com/jimwins/frozen-soup/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/jimwins/frozen-soup?include_prereleases&label=changelog)](https://github.com/jimwins/frozen-soup/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jimwins/frozen-soup/blob/main/LICENSE)

Frozen Soup is a Python library for creating a single-file version of an HTML
file by pulling in required external resources and in-lining them.

Built with Python using:
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [Request](https://github.com/psf/requests)
* [tinycss2](https://github.com/Kozea/tinycss2)

Inspired by (but not based on) [SingleFile](https://github.com/gildas-lormeau/SingleFile).

Created by [Jim Winstead](https://trainedmonkey.com/) in March 2024.

## Installation

Install this library using `pip`:
```bash
pip install frozen-soup
```
## Usage

```base
python -mfrozen_soup https://www.example.com
```

```python
import frozen_soup

output = freeze_to_string("https://www.example.com")
```

###

This will serve up a single-file HTML version of the URL supplied. (This is
not even vaguely appropriate for production use, but handy for testing.)

```bash
$ python -mfrozen_soup.server
Server started http://localhost:8080
$ curl -s http://localhost:8080/https://www.example.com
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd frozen-soup
python -m venv .venv
source .venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
