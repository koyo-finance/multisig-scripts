from brownie import interface, accounts


DEPLOYER = accounts.load("p7m")


def _tx_params(gas_limit: int = None):
    return {"from": DEPLOYER, "required_confs": 2, "gas_limit": gas_limit}


def main():
    authorizer = interface.Authorizer("0xeC9c70b34C4CF4b91cC057D726b114Ef3C7A1749")
    vault = interface.Vault("0x2A4409Cc7d2AE7ca1E3D915337D1B6Ba2350D6a3")

    manageUserBalance_action_id = vault.getActionId(vault.manageUserBalance.signature)
    batchSwap_action_id = vault.getActionId(vault.batchSwap.signature)

    authorizer.grantRoles([manageUserBalance_action_id, batchSwap_action_id], "0x8bbbD0e8a5A40f761162645E2a4E0f1C090Edf4B", _tx_params(gas_limit=5_000_000))
