"""Agent identity: load or generate the agent's own EVM keypair.

The key is generated locally, stored mode 600, and never printed or logged.
Only the public address is ever shown. No mnemonic is generated.
"""
import json
import os

from eth_account import Account


def load_or_create_key(path):
    """Returns (account, was_created)."""
    if os.path.exists(path):
        with open(path) as f:
            key = json.load(f)
        return Account.from_key(key["privateKey"]), False
    acct = Account.create()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"address": acct.address, "privateKey": acct.key.hex()}, f)
    os.chmod(path, 0o600)
    return acct, True
