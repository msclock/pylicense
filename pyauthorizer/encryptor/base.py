from __future__ import annotations

import abc
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TokenStatus(Enum):
    """
    Enum representing the status of a token.
    """

    ACTIVE = 1
    EXPIRED = 2
    INVALID = 3


@dataclass
class Token:
    """
    Class representing a token.
    """

    secret_key: str
    token: str
    expiry: str


class BaseEncryptor(abc.ABC):
    """
    Abstract base class for encryptors.
    """

    @abc.abstractmethod
    def encrypt(self, token_data: dict) -> tuple[str, str]:
        """
        Encrypts the provided data.

        Args:
            token_data (dict): The data to be encrypted.

        Returns:
            Tuple[str, str]: A tuple containing the secret key and the encrypted token.
        """

    def generate_token(self, data: dict) -> Token:
        """
        Generates a token based on the provided data.

        Args:
            data (dict): The data to be used for generating the token.

        Returns:
            Token: The generated token.

        Raises:
            None
        """
        token_data = deepcopy(data)
        expiry = token_data.pop("expiry", "")
        secret_key, token = self.encrypt(token_data)
        return Token(
            secret_key=secret_key,
            token=token,
            expiry=expiry,
        )

    @abc.abstractmethod
    def decrypt(self, token: Token) -> dict:
        """
        Decrypts the provided token.

        Args:
            token (Token): The token to decrypt.

        Returns:
            dict: A dictionary containing the decrypted data.
        """

    def validate_token(self, token: Token, data: dict) -> TokenStatus:
        """
        Validates a token by comparing its decrypted data with the provided data dictionary.

        Args:
            token (Token): The token object to be validated.
            data (dict): The dictionary containing the data to be matched with the token's decrypted data.

        Returns:
            TokenStatus: The status of the token after validation. Possible values are:
                - TokenStatus.INVALID: If the token data does not match the provided data dictionary.
                - TokenStatus.ACTIVE: If the token is valid and active.
                - TokenStatus.EXPIRED: If the token is valid but has expired.
        """
        token_data = self.decrypt(token)
        for key, value in token_data.items():
            if key not in data or value != data[key]:
                return TokenStatus.INVALID

        if token.expiry == "":
            return TokenStatus.ACTIVE

        expiry_date = datetime.fromisoformat(token.expiry)
        current_date = datetime.now()
        if expiry_date > current_date:
            return TokenStatus.ACTIVE
        return TokenStatus.EXPIRED
