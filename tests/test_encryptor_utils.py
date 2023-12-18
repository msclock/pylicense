from __future__ import annotations

from unittest.mock import Mock

import pytest

from pyauthorizer.encryptor.utils import decrypt_with_cipher


@pytest.mark.parametrize(
    ("token_value", "cipher_result", "expected_result"),
    [
        (
            "encrypted_token",
            b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
            {"typ": "JWT", "alg": "HS256"},
        )
    ],
)
def test_decrypt_with_cipher_pytest(token_value, cipher_result, expected_result):
    # Create a mock token object
    token = Mock()
    token.token = token_value

    # Create a mock cipher object
    cipher = Mock()
    cipher.decrypt.return_value = cipher_result

    decrypted_data = decrypt_with_cipher(token, cipher)

    assert decrypted_data == expected_result
