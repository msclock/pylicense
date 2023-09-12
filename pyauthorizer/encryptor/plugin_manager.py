import abc

import entrypoints

from pyauthorizer.exceptions import ErrorName, PyAuthorizerError


class PluginManager(abc.ABC):
    """Base class for managing plugins"""

    def __init__(self, group_name) -> None:
        """Initialize the PluginManager"""
        self._registry = {}
        self.group_name = group_name
        self._has_registered = None

    @abc.abstractmethod
    def __getitem__(self, item):
        """Get a plugin from the registry"""

    @property
    def registry(self):
        """Get the plugin registry"""
        return self._registry

    @property
    def has_registered(self):
        """Check if plugins have been registered"""
        return self._has_registered

    def register(self, flavor_name, plugin_module):
        """Register a plugin"""
        self._registry[flavor_name] = entrypoints.EntryPoint(flavor_name, plugin_module, None)
        self._has_registered = True

    def register_entrypoints(self):
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

    def __getitem__(self, item):
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
            raise PyAuthorizerError(msg, error_code=ErrorName.RESOURCE_DOES_NOT_EXIST) from err

        if isinstance(plugin_like, entrypoints.EntryPoint):
            try:
                plugin_obj = plugin_like.load()
            except (AttributeError, ImportError) as exc:
                plugin_load_err_msg = f'Failed to load the plugin "{item}": {exc}'
                raise RuntimeError(plugin_load_err_msg) from exc
            self.registry[item] = plugin_obj
        else:
            plugin_obj = plugin_like

        return plugin_obj
