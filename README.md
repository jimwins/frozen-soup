# frozen-soup

[![PyPI](https://img.shields.io/pypi/v/frozen-soup.svg)](https://pypi.org/project/frozen-soup/)
[![Tests](https://github.com/jimwins/frozen-soup/actions/workflows/test.yml/badge.svg)](https://github.com/jimwins/frozen-soup/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/jimwins/frozen-soup?include_prereleases&label=changelog)](https://github.com/jimwins/frozen-soup/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jimwins/frozen-soup/blob/main/LICENSE)

Frozen Soup is a Python library for creating a single-file version of an HTML
file by pulling in required external resources and in-lining them.

Built with Python using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
and [Request](https://github.com/psf/requests).

Inspired by (but not based on) [SingleFile](https://github.com/gildas-lormeau/SingleFile).

Created by [Jim Winstead](https://trainedmonkey.com/) in March 2024.

## Installation

Install this library using `pip`:
```bash
pip install frozen-soup
```
## Usage

Usage instructions go here.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd frozen-soup
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
