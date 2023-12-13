from __future__ import annotations

import importlib.metadata

import pyauthorizer as m


def test_version():
    assert importlib.metadata.version("pyauthorizer") == m.__version__
