from __future__ import annotations

import abc
from typing import Any

import entrypoints

from pyauthorizer.exceptions import ErrorName, PyAuthorizerError


class PluginManager(abc.ABC):
    """Base class for managing plugins


    Parameters:
        group_name (str): The name of the plugin group.
    """

    def __init__(self, group_name: str) -> None:
        """
        Initialize the PluginManager.
        """
        self._registry: dict[str, entrypoints.EntryPoint] = {}
        self.group_name = group_name
        self._has_registered = False

    @abc.abstractmethod
    def __getitem__(self, item: str) -> Any:
        """Get a plugin from the registry.

        Args:
            item (str): The name of the plugin to get.

        Returns:
            Any: The plugin object.
        """

    @property
    def registry(self) -> dict[str, entrypoints.EntryPoint]:
        """Get the plugin registry"""
        return self._registry

    @property
    def has_registered(self) -> bool:
        """Check if plugins have been registered"""
        return self._has_registered

    def register(self, flavor_name: str, plugin_module: str) -> None:
        """
        Register a plugin.

        Args:
            flavor_name (str): The name of the flavor.
            plugin_module (str): The name of the plugin module.

        Returns:
            None
        """
        entry_point = entrypoints.EntryPoint(flavor_name, plugin_module, "")
        self._registry[flavor_name] = entry_point
        self._has_registered = True

    def register_entrypoints(self) -> None:
        """Register plugins using entrypoints"""
        for entrypoint in entrypoints.get_group_all(self.group_name):
            self._registry[entrypoint.name] = entrypoint

        self._has_registered = True


class EncryptorPlugins(PluginManager):
    """Plugin manager for encryptor plugins"""

    def __init__(self) -> None:
        """Initialize the EncryptorPlugins"""
        super().__init__("pyauthorizer.encryptor")
        self.register_entrypoints()

    def __getitem__(self, item: str) -> Any:
        """Get a plugin from the registry"""
        try:
            flavor_name = item
            plugin_like = self.registry[flavor_name]
        except KeyError as err:
            msg = (
                f'No plugin found for managing tokens from "{item}". '
                "In order to manage tokens, find and install an appropriate "
                "plugin from https://github.com/msclock/pyauthorizer/tree/master/pyauthorizer/encrpytor/builtin "
                "or implement your plugins."
            )
            raise PyAuthorizerError(
                msg, error_code=ErrorName.resource_does_not_exist
            ) from err

        try:
            plugin_obj = plugin_like.load()
        except (AttributeError, ImportError) as exc:
            plugin_load_err_msg = f'Failed to load the plugin "{item}": {exc}'
            raise RuntimeError(plugin_load_err_msg) from exc
        self.registry[item] = plugin_obj

        return plugin_obj
