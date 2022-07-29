from decimal import Decimal
from mimetypes import init
from brownie import interface, accounts
import eth_abi


DEPLOYER = accounts.load("p7m")
DECIMALS = Decimal(10**18)


def _tx_params(gas_limit: int = None):
    return {"from": DEPLOYER, "required_confs": 2, "gas_limit": gas_limit}


def main():
    wETH = interface.ERC20("0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000")
    frax = interface.ERC20("0x7562F525106F5d54E891e005867Bf489B5988CD9")

    vault = interface.Vault("0x2A4409Cc7d2AE7ca1E3D915337D1B6Ba2350D6a3")
    frax_pool = interface.OracleWeightedPool(
        "0x5EC75124616Dc136dEa5560A59512404a133209b"
    )

    frax_pool_id = frax_pool.getPoolId()

    user_data = eth_abi.encode_abi(
        ["uint256", "uint256[]"],
        [int(0), [int(Decimal(106.727) * DECIMALS), int(Decimal(0.1) * DECIMALS)]],
    )

    # wETH.approve(vault, int(Decimal(1) * DECIMALS), _tx_params(5_000_000))
    frax.approve(vault, int(Decimal(106.727) * DECIMALS), _tx_params(5_000_000))

    vault.joinPool(
        frax_pool_id,
        DEPLOYER,
        DEPLOYER,
        (
            [frax, wETH],
            [int(Decimal(106.727) * DECIMALS), int(Decimal(0.1) * DECIMALS)],
            user_data.hex(),
            False,
        ),
        _tx_params(5_000_000),
    )
