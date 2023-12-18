from __future__ import annotations

import base64
import json
import uuid
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet, InvalidToken

from pyauthorizer.encryptor.base import Token


def generate_key() -> bytes:
    """
    Generate a key using the Fernet encryption algorithm.

    Returns:
        bytes: A randomly generated key.

    """
    return bytes(Fernet.generate_key())


def get_id_on_mac() -> str:
    """
    Get the MAC address of the machine.
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e : e + 2] for e in range(0, 11, 2)])


def decrypt_with_cipher(token: Token, cipher: Any) -> dict[str, Any]:
    """
    Decrypts a token using the provided cipher and returns the decrypted token data.

    Parameters:
        token (Token): The token to be decrypted.
        cipher (Any): The cipher object used for decryption.

    Returns:
        dict[str, Any]: The decrypted token data as a dictionary.
    """
    token_data: dict[str, Any] = {}
    try:
        decrypted_token = cipher.decrypt(token.token.encode("utf-8"))
        decoded_data = base64.urlsafe_b64decode(decrypted_token)
        token_data = json.loads(decoded_data)
    except (InvalidToken, InvalidSignature):
        pass

    return token_data
