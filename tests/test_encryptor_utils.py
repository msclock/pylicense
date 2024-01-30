from __future__ import annotations

import base64
import json
from unittest.mock import Mock

import pytest

from pyauthorizer.encryptor.utils import decrypt_with_cipher


@pytest.mark.parametrize(
    ("token_value"),
    [
        "value 1",
        "value 2",
        "value 3",
    ],
)
def test_decrypt_with_cipher(token_value):
    # Create a mock token object
    token = Mock()
    token.token = token_value

    # Create a mock cipher object
    cipher = Mock()
    cipher.decrypt.return_value = base64.urlsafe_b64encode(
        json.dumps(token_value).encode("utf-8")
    )

    decrypted_data = decrypt_with_cipher(token, cipher)

    assert decrypted_data == token_value
