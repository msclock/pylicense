# pyauthorizer

<!-- SPHINX-START -->

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/msclock/pyauthorizer/actions/workflows/ci.yml/badge.svg
[actions-link]:             https://github.com/msclock/pyauthorizer/actions/workflows/ci.yml
[pypi-link]:                https://pypi.org/project/pyauthorizer/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/pyauthorizer
[pypi-version]:             https://badge.fury.io/py/pyauthorizer.svg
<!-- prettier-ignore-end -->

A simple authorizer for python project.

In some cases, even for a scripting language like Python, it may be necessary to
generate and validate tokens for specific use cases. The `pyauthorizer` provides
a simple way to generate and validate licenses. Additionally, the built-in
plugins make it easy to customize encryptors and decryptors. There is also a
simple command-line tool available.

## Install

Package-built has uploaded to pypi and just install with the command:

```bash
pip install pyauthorizer
```

## Usage

To generate and validate a license, use the command:

```bash
pyauthorizer create -f simple -C password=1234567890  -O /tmp/license.json
pyauthorizer validate -f simple -C password=1234567890  -I /tmp/license.json
```

More command options can be listed by using `pyauthorizer --help`.

<!-- SPHINX-END -->
