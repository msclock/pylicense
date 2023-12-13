from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ErrorName:
    """Definitions for error codes."""

    internal_error: int = 1
    invalid_parameter_value: int = 2
    resource_does_not_exist: int = 3


class PyAuthorizerError(Exception):
    """Generic exception thrown to surface failure information about external-facing operations.

    If the error text is sensitive, raise a generic `Exception` object instead.

    Parameters:
        message (str): The message or exception describing the error that occurred.
            This will be included in the exception's serialized JSON representation.
        error_code (int): An appropriate error code for the error that occurred.
            It will be included in the exception's serialized JSON representation.
        kwargs: Additional key-value pairs to include in the serialized JSON representation
            of the PyAuthorizerError.
    """

    def __init__(
        self,
        message: str,
        error_code: int = ErrorName.internal_error,
        **kwargs: Any,
    ) -> None:
        """Initialize the PyAuthorizerError object."""
        try:
            self.error_code = error_code
        except (ValueError, TypeError):
            self.error_code = ErrorName.internal_error
        message = str(message)
        self.message = message
        self.json_kwargs = kwargs
        super().__init__(message)

    def serialize_as_json(self) -> str:
        """Serialize the PyAuthorizerError object as JSON.

        Returns:
            str: The serialized JSON representation of the PyAuthorizerError object.
        """
        exception_dict = {"error_code": self.error_code, "message": self.message}
        exception_dict.update(self.json_kwargs)
        return json.dumps(exception_dict)

    @classmethod
    def invalid_parameter_value(cls, message: str, **kwargs: Any) -> PyAuthorizerError:
        """Construct an `PyAuthorizerError` object with the `INVALID_PARAMETER_VALUE` error code.

        Args:
            message (str): The message describing the error that occurred.
                This will be included in the exception's serialized JSON representation.
            kwargs: Additional key-value pairs to include in the serialized JSON representation
                of the PyAuthorizerError.

        Returns:
            PyAuthorizerError: An instance of PyAuthorizerError with the specified error code.
        """
        return cls(message, error_code=ErrorName.invalid_parameter_value, **kwargs)
