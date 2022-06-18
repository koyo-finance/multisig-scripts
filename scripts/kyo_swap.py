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
    kyo = interface.ERC20("0x618CC6549ddf12de637d46CDDadaFC0C2951131C")

    vault = interface.Vault("0x2A4409Cc7d2AE7ca1E3D915337D1B6Ba2350D6a3")
    kyo_pool = interface.OracleWeightedPool(
        "0xf425eD6a3d48bf765853c8cD3Bf4B697af8D3B04"
    )

    kyo_pool_id = kyo_pool.getPoolId()

    user_data = eth_abi.encode_abi(
        ["uint256"],
        [int(0)],
    )

    wETH_balance = wETH.balanceOf(DEPLOYER)
    # wETH.approve(vault, int(Decimal(1) * DECIMALS), _tx_params(5_000_000))
    # frax.approve(vault, int(Decimal(106.727) * DECIMALS), _tx_params(5_000_000))

    vault.swap(
        (kyo_pool_id, 0, wETH, kyo, wETH_balance / 4, user_data),
        (DEPLOYER, False, DEPLOYER, False),
        0,
        int(1655379114),
        _tx_params(5_000_000),
    )
