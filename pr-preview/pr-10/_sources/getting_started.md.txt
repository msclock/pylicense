# Getting Started

## Installation

The `pyauthorizer` package can be installed with the following command:

```bash
pip install pyauthorizer
```

## Usage

Available commands are:

```bash
Usage: pyauthorizer [OPTIONS] COMMAND [ARGS]...

  Using encrpytor to manage tokens.Run `pyauthorizer --help` for more details
  on the supported URI format and config options for a given target. Support
  is currently installed for encryptor to: multiple, simple

  See all supported encryption targets and installation instructions in https:
  //github.com/msclock/pyauthorizer/tree/master/pyauthorizer/encrpytor/builtin

  You can also write your own plugin for encryptor to a custom target. For
  instructions on writing and distributing a plugin, related docs are coming
  soon.

Options:
  --help  Show this message and exit.

Commands:
  create    Generate a token using the given flavor and configuration,...
  validate  Validates a token using the specified flavor.
```

For more information, run `pyauthorizer --help`
