from __future__ import annotations

import base64
import json

from cryptography.fernet import Fernet, InvalidSignature, InvalidToken

from pyauthorizer.encryptor.base import BaseEncryptor, Token
from pyauthorizer.encryptor.utils import generate_key


class SimpleEncryptor(BaseEncryptor):
    def __init__(self):
        super().__init__()

    def encrypt(self, data: dict) -> tuple[str, str]:
        """
        Encrypts the provided data.

        Args:
            token_data (dict): The data to be encrypted.

        Returns:
            Tuple[str, str]: A tuple containing the secret key and the encrypted token.
        """

        secret_key = generate_key()
        base64_data = base64.urlsafe_b64encode(json.dumps(data).encode("utf-8"))
        token = Fernet(secret_key).encrypt(base64_data)
        return secret_key.decode("utf-8"), token.decode("utf-8")

    def decrypt(self, token: Token) -> dict:
        """
        Decrypts the given token and returns the token data as a dictionary.

        Args:
            token (Token): The token to be decrypted.

        Returns:
            dict: The decrypted token data as a dictionary.

        Raises:
            InvalidToken: If the token is invalid.
            InvalidSignature: If the token signature is invalid.
        """
        token_data = {}
        try:
            cipher = Fernet(token.secret_key.encode("utf-8"))
            decrypted_token = cipher.decrypt(token.token.encode("utf-8"))
            decoded_data = base64.urlsafe_b64decode(decrypted_token)
            token_data: dict = json.loads(decoded_data)
        except (InvalidToken, InvalidSignature):
            pass

        return token_data
