from __future__ import annotations

import inspect
import pkgutil
from pathlib import Path

from pyauthorizer.encryptor.base import BaseEncryptor
from pyauthorizer.encryptor.plugin_manager import EncryptorPlugins

# Create a global registry
encryptor_plugins = EncryptorPlugins()

# Register builtin plugins
current_directory = Path(__file__).resolve().parent.joinpath("builtin")
for _, module_name, _ in pkgutil.iter_modules([str(current_directory)]):  # type: ignore[assignment]
    encryptor_plugins.register(
        module_name, f"pyauthorizer.encryptor.builtin.{module_name}"
    )


def get_encryptor(target: str) -> BaseEncryptor | None:
    """
    Get the encryptor corresponding to the target.

    Parameters:
        target (str): The target for which to retrieve the encryptor.

    Returns:
        BaseEncryptor | None: An instance of the encryptor class corresponding to the target, or None if no encryptor is found.
    """
    # Get the plugin corresponding to the target
    plugin = encryptor_plugins[target]
    for _, obj in inspect.getmembers(plugin):
        # Check if the object is a class and a subclass of BaseEncryptor
        if (
            inspect.isclass(obj)
            and issubclass(obj, BaseEncryptor)
            and obj != BaseEncryptor
        ):
            # Return an instance of the class
            return obj()
    return None
