from __future__ import annotations

import base64
import json
from typing import Any

from cryptography.fernet import Fernet

from pyauthorizer.encryptor.base import BaseEncryptor, Token
from pyauthorizer.encryptor.utils import decrypt_with_cipher, generate_key


class SimpleEncryptor(BaseEncryptor):
    def __init__(self) -> None:
        pass

    def encrypt(self, data: dict[str, Any]) -> tuple[str, str]:
        """
        Encrypts the provided data.

        Args:
            data (dict): The data to be encrypted.

        Returns:
            Tuple[str, str]: A tuple containing the secret key and the encrypted token.
        """

        secret_key = generate_key()
        base64_data = base64.urlsafe_b64encode(json.dumps(data).encode("utf-8"))
        token = Fernet(secret_key).encrypt(base64_data)
        return secret_key.decode("utf-8"), token.decode("utf-8")

    def decrypt(self, token: Token) -> dict[str, Any]:
        """
        Decrypts the given token and returns the token data as a dictionary.

        Args:
            token (Token): The token to be decrypted.

        Returns:
            dict: The decrypted token data as a dictionary.
        """
        cipher = Fernet(token.secret_key.encode("utf-8"))
        return decrypt_with_cipher(token, cipher)
