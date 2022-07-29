from brownie import interface, accounts


DEPLOYER = accounts.load("p7m")


def _tx_params(gas_limit: int = None):
    return {"from": DEPLOYER, "required_confs": 2, "gas_limit": gas_limit}


def main():
    authorizer = interface.Authorizer("0xeC9c70b34C4CF4b91cC057D726b114Ef3C7A1749")
    protocol_fees_collector = interface.ProtocolFeesCollector("0xc9453BaBf4705F18e3Bb8790bdc9789Aaf17c2E1")

    set_fee_action_id = protocol_fees_collector.getActionId(protocol_fees_collector.setSwapFeePercentage.signature)
    withdraw_fee_action_id = protocol_fees_collector.getActionId(protocol_fees_collector.withdrawCollectedFees.signature)

    authorizer.grantRoles([set_fee_action_id, withdraw_fee_action_id], DEPLOYER, _tx_params(gas_limit=5_000_000))

    protocol_fees_collector.setSwapFeePercentage(50e16, _tx_params(gas_limit=5_000_000))
