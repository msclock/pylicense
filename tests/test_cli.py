from __future__ import annotations

import pytest

from pyauthorizer.cli import convert_user_args_to_dict
from pyauthorizer.exceptions import PyAuthorizerError


def test_convert_user_args_to_dict():
    # Test case 1: Valid input with single argument
    user_list = ["key=value"]
    expected_output = {"key": "value"}
    assert convert_user_args_to_dict(user_list) == expected_output

    # Test case 2: Valid input with multiple arguments
    user_list = ["key1=value1", "key2=value2", "key3=value3"]
    expected_output = {"key1": "value1", "key2": "value2", "key3": "value3"}
    assert convert_user_args_to_dict(user_list) == expected_output

    # Test case 3: Invalid input with missing value
    user_list = ["key"]
    with pytest.raises(PyAuthorizerError):
        convert_user_args_to_dict(user_list)

    # Test case 4: Invalid input with repeated parameter
    user_list = ["key1=value1", "key1=value2"]
    with pytest.raises(PyAuthorizerError):
        convert_user_args_to_dict(user_list)
