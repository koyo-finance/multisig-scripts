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

    helpers = interface.KoyoHelpers("0x535daCfF059e44F3933188BD5124B1dAA2D23e4a")
    vault = interface.Vault("0x2A4409Cc7d2AE7ca1E3D915337D1B6Ba2350D6a3")
    kyo_pool = interface.OracleWeightedPool(
        "0xf425eD6a3d48bf765853c8cD3Bf4B697af8D3B04"
    )

    kyo_pool_id = kyo_pool.getPoolId()
    print(kyo_pool_id)
    print(kyo_pool.getScalingFactors())

    user_data = eth_abi.encode_abi(
        ["uint256", "uint256[]"],
        [int(0), [int(Decimal(300_000) * DECIMALS), int(Decimal(0.01) * DECIMALS)]],
    )
    # print(
    #     helpers.queryJoin(
    #         kyo_pool_id,
    #         DEPLOYER.address,
    #         DEPLOYER.address,
    #         (
    #             [kyo.address, wETH.address],
    #             [int(Decimal(300_000) * DECIMALS), int(Decimal(0.01) * DECIMALS)],
    #             user_data.hex(),
    #             False,
    #         ),
    #     )
    # )

    # wETH.approve(vault, int(Decimal(1) * DECIMALS), _tx_params(5_000_000))
    # kyo.approve(vault, int(Decimal(10_000_000) * DECIMALS), _tx_params(5_000_000))

    vault.joinPool(
        kyo_pool_id,
        DEPLOYER,
        DEPLOYER,
        (
            [kyo, wETH],
            [int(Decimal(300_000) * DECIMALS), int(Decimal(0.01) * DECIMALS)],
            user_data.hex(),
            False,
        ),
        _tx_params(5_000_000),
    )

    # user_data = eth_abi.encode_abi(
    #     ["uint256", "uint256"],
    #     [int(1), int(kyo_pool.balanceOf(DEPLOYER))],
    # )
    # vault.exitPool(
    #     kyo_pool_id,
    #     DEPLOYER,
    #     DEPLOYER,
    #     (
    #         [kyo, wETH],
    #         [int(0), int(0)],
    #         user_data.hex(),
    #         False,
    #     ),
    #     _tx_params(5_000_000),
    # )
