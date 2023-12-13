from __future__ import annotations

import json
from dataclasses import asdict
from json.decoder import JSONDecodeError
from pathlib import Path

import click
from click import option
from loguru import logger

from pyauthorizer.encryptor import interface
from pyauthorizer.encryptor.base import Token, TokenStatus
from pyauthorizer.exceptions import ErrorName, PyAuthorizerError


def convert_user_args_to_dict(user_list: list[str]) -> dict[str, str]:
    """
    Converts a list of user arguments to a dictionary.

    Args:
        user_list (list): A list of user arguments.

    Returns:
        dict: A dictionary containing the converted user arguments. The keys are the names extracted from the user arguments, and the values are the corresponding values.

    Raises:
        PyAuthorizerError: If the user arguments are not in the correct format or if a parameter is repeated.
    """
    user_dict = {}
    for s in user_list:
        try:
            # Some configs may contain '=' in the value
            name, value = s.split("=", 1)
        except ValueError as exc:
            # not enough values to unpack
            msg = (
                "Config options must be a pair and should be "
                "provided as ``-C key=value`` or "
                "``--config key=value``"
            )
            raise PyAuthorizerError(
                msg,
                error_code=ErrorName.invalid_parameter_value,
            ) from exc
        if name in user_dict:
            msg = f"Repeated parameter: '{name}'"
            raise PyAuthorizerError(msg, error_code=ErrorName.invalid_parameter_value)
        user_dict[name] = value
    return user_dict


# load all registered encryptors
installed_flavors = list(interface.encryptor_plugins.registry)
if len(installed_flavors) > 0:
    SUPPORTED_FLAVORS_MSG = f"""Support is currently installed for encryptor to: {", ".join(installed_flavors)}"""
else:
    SUPPORTED_FLAVORS_MSG = (
        "NOTE: you currently do not have support installed for any encryptor flavors."
    )


# mypy: disallow-untyped-decorators=False

# cmd options
parse_output = option(
    "--output-path",
    "-O",
    help="File to output results to as a JSON file. If not provided, prints output to stdout.",
)
parse_input = option(
    "--input-path", "-I", required=True, help="Path to input json file for prediction"
)
parse_custom_arguments = option(
    "--config",
    "-C",
    metavar="NAME=VALUE",
    multiple=True,
    help="Extra target-specific config for the model "
    "encryptor, of the form -C name=value. See "
    "documentation/help for your encryptor target for a "
    "list of supported config options.",
)
encryptor_flavor = option(
    "--flavor",
    "-f",
    required=True,
    help="Which flavor to be used to encrypt. This will be auto inferred if it's not given",
)


commands = click.Group(
    "encrpytor",
    help=f"""
    Using encrpytor to manage tokens.Run `pyauthorizer --help` for
    more details on the supported URI format and config options for a given target.
    {SUPPORTED_FLAVORS_MSG}

    See all supported encryption targets and installation instructions in
    https://github.com/msclock/pyauthorizer/tree/master/pyauthorizer/encrpytor/builtin

    You can also write your own plugin for encryptor to a custom target. For instructions on
    writing and distributing a plugin, related docs are coming soon.""",
)


@commands.command("create")
@parse_output
@parse_custom_arguments
@encryptor_flavor
def generate_license(flavor: str, config: list[str], output_path: str) -> None:
    """
    Generate a token using the given flavor and configuration, and either write it to a file or print it to the console.
    """
    config_dict = convert_user_args_to_dict(config)
    encryptor = interface.get_encryptor(flavor)
    if encryptor is None:
        logger.error(f"Unsupported encryptor: {flavor}")
        return

    token: Token = encryptor.generate_token(config_dict)

    json_license = json.dumps(
        asdict(token),
        indent=4,
        ensure_ascii=False,
        sort_keys=False,
        separators=(",", ":"),
    )
    if len(output_path) != 0:
        with Path(output_path).open("w", encoding="utf-8") as f:
            f.write(json_license)
        logger.info(f"Token written to {output_path}")
    else:
        logger.info(json_license)


@commands.command("validate")
@parse_input
@parse_custom_arguments
@encryptor_flavor
def validate_license(flavor: str, config: list[str], input_path: str) -> None:
    """
    Validates a token using the specified flavor.
    """
    config_dict = convert_user_args_to_dict(config)

    try:
        data = {}
        with Path(input_path).open(encoding="utf-8") as f:
            data = json.load(f)
        token = Token(**data)
    except Exception as err:
        if isinstance(err, FileNotFoundError):
            err_msg = f"open authorized file: {err.args}"
        elif isinstance(err, JSONDecodeError):
            err_msg = f"invalid authorized file: {err.args}"
        else:
            err_msg = str(err.args)
        logger.error(f"Init Token failed with {err_msg}")
        raise SystemExit(1) from err

    encryptor = interface.get_encryptor(flavor)
    if encryptor is None:
        logger.error(f"Target {flavor} is not supported")
        raise SystemExit(1)

    status = encryptor.validate_token(token, config_dict)
    if status == TokenStatus.ACTIVE:
        logger.info("Token is active")
    elif status == TokenStatus.EXPIRED:
        logger.error("Token has expired")
        raise SystemExit(2)
    else:
        logger.error("Token is invalid")
        raise SystemExit(3)


if __name__ == "__main__":
    commands()
