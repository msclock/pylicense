from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorName:
    INTERNAL_ERROR = 1
    INVALID_PARAMETER_VALUE = 2
    RESOURCE_DOES_NOT_EXIST = 3


class PyAuthorizerError(Exception):
    """Generic exception thrown to surface failure information about external-facing operations.

    If the error text is sensitive, raise a generic `Exception` object instead.
    """

    def __init__(self, message, error_code=ErrorName.INTERNAL_ERROR, **kwargs):
        """Initialize the PyAuthorizerError object.

        Args:
            message (str): The message or exception describing the error that occurred.
                This will be included in the exception's serialized JSON representation.
            error_code (int): An appropriate error code for the error that occurred.
                It will be included in the exception's serialized JSON representation.
                This should be one of the codes listed in the `mlflow.protos.databricks_pb2` proto.
            kwargs: Additional key-value pairs to include in the serialized JSON representation
                of the PyAuthorizerError.
        """
        try:
            self.error_code = error_code
        except (ValueError, TypeError):
            self.error_code = ErrorName.INTERNAL_ERROR
        message = str(message)
        self.message = message
        self.json_kwargs = kwargs
        super().__init__(message)

    def serialize_as_json(self):
        """Serialize the PyAuthorizerError object as JSON.

        Returns:
            str: The serialized JSON representation of the PyAuthorizerError object.
        """
        exception_dict = {"error_code": self.error_code, "message": self.message}
        exception_dict.update(self.json_kwargs)
        return json.dumps(exception_dict)

    @classmethod
    def invalid_parameter_value(cls, message, **kwargs):
        """Construct an `PyAuthorizerError` object with the `INVALID_PARAMETER_VALUE` error code.

        Args:
            message (str): The message describing the error that occurred.
                This will be included in the exception's serialized JSON representation.
            kwargs: Additional key-value pairs to include in the serialized JSON representation
                of the PyAuthorizerError.

        Returns:
            PyAuthorizerError: An instance of PyAuthorizerError with the specified error code.
        """
        return cls(message, error_code=ErrorName.INVALID_PARAMETER_VALUE, **kwargs)
