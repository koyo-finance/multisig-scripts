from decimal import Decimal
from mimetypes import init
from brownie import interface, accounts
import eth_abi


DEPLOYER = accounts.load("p7m")
DECIMALS = Decimal(10**18)


def _tx_params(gas_limit: int = None):
    return {"from": DEPLOYER, "required_confs": 2, "gas_limit": gas_limit}


def main():
    usdc = interface.ERC20("0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc")
    frax = interface.ERC20("0x7562F525106F5d54E891e005867Bf489B5988CD9")

    vault = interface.Vault("0x2A4409Cc7d2AE7ca1E3D915337D1B6Ba2350D6a3")
    stable_pool = interface.StablePool(
        "0xe529b330017f3ee8b4665b0cae4b9c224e1dab38"
    )

    stable_pool_id = stable_pool.getPoolId()

    usdc_balance = usdc.balanceOf(DEPLOYER)
    frax_balance = frax.balanceOf(DEPLOYER)

    user_data = eth_abi.encode_abi(
        ["uint256", "uint256[]"],
        [int(0), [usdc_balance, frax_balance]],
    )

    usdc.approve(vault, usdc_balance, _tx_params(5_000_000))
    frax.approve(vault, frax_balance, _tx_params(5_000_000))

    vault.joinPool(
        stable_pool_id,
        DEPLOYER,
        DEPLOYER,
        (
            [usdc, frax],
            [usdc_balance, frax_balance],
            user_data.hex(),
            False,
        ),
        _tx_params(5_000_000),
    )
