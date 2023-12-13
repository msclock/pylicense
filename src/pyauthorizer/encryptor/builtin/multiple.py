from __future__ import annotations

import base64
import json
from typing import Any

from cryptography.fernet import Fernet, MultiFernet

from pyauthorizer.encryptor.base import BaseEncryptor, Token
from pyauthorizer.encryptor.utils import decrypt_with_cipher, generate_key


class MultiEncryptor(BaseEncryptor):
    def __init__(self) -> None:
        pass

    def encrypt(self, data: dict[str, Any]) -> tuple[str, str]:
        """
        Encrypts the given data using a set of secret keys.

        Args:
            data (dict): The data to be encrypted.

        Returns:
            Tuple[str, str]: A tuple containing the secret key and the encrypted token.
        """

        key_nums = int(data["key_nums"])
        secret_keys = [generate_key() for _ in range(key_nums)]
        base64_data = base64.urlsafe_b64encode(json.dumps(data).encode("utf-8"))
        token = MultiFernet([Fernet(k) for k in secret_keys]).encrypt(base64_data)
        secret_key = " ".join([k.decode("utf-8") for k in secret_keys])
        return secret_key, token.decode("utf-8")

    def decrypt(self, token: Token) -> dict[str, Any]:
        """
        Decrypts a token and returns the token data as a dictionary.

        Parameters:
            token (Token): The token to be decrypted.

        Returns:
            dict: The decrypted token data.
        """

        cipher = MultiFernet([Fernet(k) for k in token.secret_key.split()])
        return decrypt_with_cipher(token, cipher)
