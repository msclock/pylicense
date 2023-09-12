from __future__ import annotations

import uuid

from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate a key using the Fernet encryption algorithm.

    Returns:
        bytes: A randomly generated key.

    """
    return Fernet.generate_key()


def get_id_on_mac() -> str:
    """
    Get the MAC address of the machine.
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e : e + 2] for e in range(0, 11, 2)])
