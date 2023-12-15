# Advance

The page is prepared for advanced users. Normally, the built-in plugins are not
enough because security is a concern that encrypt/decrypt operation should be
protected from an exploitation attacker. Here, we will show how to customize the
plugins and work as ports in nuitka to provide more secure operation.

## Encrypt/Decrypt Customize

Thanks to the plugin manager, encryption and decryption operations can be
customized.

The plugin implementation is powered by `entrypoints` module.

### Write your own plugin

You can define a new plugin as a standalone Python package that can be
distributed for installation via PyPI or conda.

See
<https://github.com/msclock/pyauthorizer/tree/master/src/pyauthorizer/encryptor/builtin>
for built-in plugins. You can also write your own plugin as a standalone package
that implements all available plugin types.

What you need to do is to subclass `BaseEncryptor` and implement the `encrypt`
and `decrypt` methods. Then register the plugin through declaring it in the
package configuration with the entrypoint. Such as:

````{tab} pyproject.toml
```toml
# in pyproject.toml
[project.entry-points."pyauthorizer.encryptor"]
subclass_encryptor = "custom_plugins.subclass_encryptor"
```
````

````{tab} setup.py
```python
setup(
    name="custom-plugins",
    # Require pyauthorizer as a dependency of the plugin, so that plugin users can simply install
    # the plugin and then immediately use it with pyauthorizer
    install_requires=["pyauthorizer"],
    ...,
    entry_points={
        # Define a puauthorizer encryptor plugin for target 'subclass_encryptor'
        "pyauthorizer.encryptor": "subclass_encryptor=custom_plugins.subclass_encryptor",
    },
)
```
````

Assuming you’ve structured your plugin similarly to the example plugin, you can
distribute it via PyPI.

Congrats, you’ve now written and distributed your own pyauthorizer plugin!

## Work as ports in nuitka

For secure reasons, sources sometimes need to be converted to executables or
shared modules that prevents them from being tampered with or leaked. This can
be done with nuitka.

More detailed information can be found in
<https://msclock.gitlab.io/pytools/docs/nuitka.html>.
