from ape_safe import ApeSafe
from brownie import interface
import eth_abi


SAFE_ADDRESS = ""
KOYO_VAULT_ADDRESS = ""

WETH_ADDRESS = ""
BOBA_ADDRESS = ""
USDC_ADDRESS = ""
DAI_ADDRESS = ""

USDC_DAI_STABLEPOOL_ADDRESS = ""
BOBA_WETH_WEIGHTEDPOOL_ADDRESS = ""

USDC_DAI_STABLEPOOL_USDC_PROVISION = 0
USDC_DAI_STABLEPOOL_DAI_PROVISION = 0


def main():
    # We need a instance of ApeSafe to interact with Gnosis (transactions are submitted via https://safe-transaction.mainnet.boba.network)
    safe = ApeSafe(SAFE_ADDRESS)
    # The vault is the central point for all Koyo pools and their deposits
    vault = interface.Vault(KOYO_VAULT_ADDRESS, owner=safe.account)

    # We need to create contract interfaces for all used tokens to be able to execute approvals and wrappings
    weth = interface.WETH9(WETH_ADDRESS, owner=safe.account)
    boba = interface.ERC20(BOBA_ADDRESS, owner=safe.account)
    usdc = interface.ERC20(USDC_ADDRESS, owner=safe.account)
    dai = interface.ERC20(DAI_ADDRESS, owner=safe.account)

    # Not all tokens have the same decimals so we need to know how to scale them from regular ints and/or floats
    weth_scale = 10 ** weth.decimals()
    boba_scale = 10 ** boba.decimals()
    usdc_scale = 10 ** usdc.decimals()
    dai_scale = 10 ** dai.decimals()

    usdc_dai_stablepool = interface.StablePool(USDC_DAI_STABLEPOOL_ADDRESS, owner=safe.account)
    boba_weth_weightedpool = interface.OracleWeightedPool(BOBA_WETH_WEIGHTEDPOOL_ADDRESS, owner=safe.account)

    usdc_dai_stablepool_id = usdc_dai_stablepool.getPoolId()
    boba_weth_weightedpool_id = boba_weth_weightedpool.getPoolId()

    USDC_DAI_STABLEPOOL_USDC_PROVISION_SCALED = USDC_DAI_STABLEPOOL_USDC_PROVISION * usdc_scale
    USDC_DAI_STABLEPOOL_DAI_PROVISION_SCALED = USDC_DAI_STABLEPOOL_DAI_PROVISION * dai_scale

    # https://dev.balancer.fi/resources/joins-and-exits/pool-joins#joinkinds-explained
    usdc_dai_stablepool_deposit_user_data = eth_abi.encode_abi(
        ["uint256", "uint256[]", "uint256"],
        [
            int(1), # 0 would be INIT but we use 1 since we're performing a EXACT_TOKENS_IN_FOR_BPT_OUT. This is due to the pool already being initialised
            [
                USDC_DAI_STABLEPOOL_USDC_PROVISION_SCALED, # USDC
                USDC_DAI_STABLEPOOL_DAI_PROVISION_SCALED # DAI
            ],
            0 # This is the minimum LP token return. It would matter if slippage while providing liquidity was a concern
        ],
    )

    usdc.approve(vault, USDC_DAI_STABLEPOOL_USDC_PROVISION_SCALED)
    dai.approve(vault, USDC_DAI_STABLEPOOL_DAI_PROVISION_SCALED)

    # https://dev.balancer.fi/resources/joins-and-exits/pool-joins#arguments-explained
    vault.joinPool(
        usdc_dai_stablepool_id,
        safe.account,
        safe.account,
        (
            [usdc, dai],
            [
                USDC_DAI_STABLEPOOL_USDC_PROVISION_SCALED, # USDC
                USDC_DAI_STABLEPOOL_DAI_PROVISION_SCALED # DAI
            ],
            usdc_dai_stablepool_deposit_user_data.hex(),
            False, # The multisig most likely doesn't have an internal balance yet
        ),
    )

    # We gather all transactions done on our fork and create a multisend tx (contract on Boba is at address 0x2Bd65cd56cAAC777f87d7808d13DEAF88e54E0eA)
    tx_safe_multisend = safe.multisend_from_receipts()
    # The tx is signed before being submitted to the Boba multisig API. We use Frame for this as it allows us to support seed phrase and private key based accounts as well as Ledgers and Trezors
    safe.sign_with_frame(tx_safe_multisend)
    # Finally we post the signed tx to the Boba multisig API to be signed by the other signers
    safe.post_transaction(tx_safe_multisend)
