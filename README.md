# pyauthorizer

A simple authorizer for python project.

## Install

Package-built has uploaded to pypi and just install with the command:

```bash
pip install pyauthorizer
```
## Usage

### Generate and validate a license

To generate and validate a license, use the command:

```bash
pyauthorizer create -f simple -C password=1234567890  -O /tmp/license.json
pyauthorizer validate -f simple -C password=1234567890  -I /tmp/license.json
```
More command options can be listed by using `pyauthorizer --help`.

## Documentation

The documentation is coming soon.
