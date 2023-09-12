from __future__ import annotations

import base64
import json

from cryptography.fernet import Fernet, InvalidSignature, InvalidToken, MultiFernet

from pyauthorizer.encryptor.base import BaseEncryptor, Token
from pyauthorizer.encryptor.utils import generate_key


class MultiEncryptor(BaseEncryptor):
    def __init__(self):
        super().__init__()

    def encrypt(self, data: dict) -> tuple[str, str]:
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

    def decrypt(self, token: Token) -> dict:
        """
        Decrypts a token and returns the token data as a dictionary.

        Parameters:
            token (Token): The token to be decrypted.

        Returns:
            dict: The decrypted token data.

        Raises:
            InvalidToken: If the token is invalid or cannot be decrypted.
            InvalidSignature: If the token has an invalid signature.
        """
        token_data = {}
        try:
            cipher = MultiFernet([Fernet(k) for k in token.secret_key.split()])
            decrypted_token = cipher.decrypt(token.token.encode("utf-8"))
            decoded_data = base64.urlsafe_b64decode(decrypted_token)
            token_data: dict = json.loads(decoded_data)
        except (InvalidToken, InvalidSignature):
            pass

        return token_data
