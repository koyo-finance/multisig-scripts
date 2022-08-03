from ape_safe import ApeSafe
from brownie import interface, accounts
import eth_abi


DEPLOYER = accounts.load("p7m")
USDC_ADDRESS = "0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc"


def main():
    treasury = ApeSafe("0x559dBda9Eb1E02c0235E245D9B175eb8DcC08398")

    vault = interface.Vault(
        "0x2A4409Cc7d2AE7ca1E3D915337D1B6Ba2350D6a3", owner=treasury.account
    )
    stable_pool = interface.StablePool(
        "0xe8a2143598d841972513eea37f632a233e93b2b9", owner=treasury.account
    )
    usdc_dai_gauge = interface.LiquidityGaugeV1("0x7a927d250d4f7e86cc21521BA312E706f0F80bF1", owner=treasury.account)

    dai = interface.ERC20(
        "0xf74195bb8a5cf652411867c5c2c5b8c2a402be35", owner=treasury.account
    )
    usdc = interface.ERC20(USDC_ADDRESS, owner=treasury.account)
    usdc_scale = 10 ** usdc.decimals()

    stable_pool_id = stable_pool.getPoolId()

    user_data = eth_abi.encode_abi(
        ["uint256", "uint256[]", "uint256"],
        [int(1), [10 * usdc_scale, 0], 0],
    )

    usdc.approve(vault, 10 * usdc_scale)

    vault.joinPool(
        stable_pool_id,
        treasury.account,
        treasury.account,
        (
            [usdc, dai],
            [10 * usdc_scale, 0],
            user_data.hex(),
            False,
        ),
    )

    stable_pool_lp_balance = stable_pool.balanceOf(treasury.account)
    stable_pool.approve(usdc_dai_gauge, stable_pool_lp_balance)

    usdc_dai_gauge.deposit(stable_pool_lp_balance)

    safe_tx = treasury.multisend_from_receipts()
    safe_tx.sign(DEPLOYER.private_key)
    treasury.post_transaction(safe_tx)
