from brownie import interface, accounts
from ape_safe import ApeSafe
import requests


CHAIN = 288
OPTIMISM = 10
DEPLOYER = accounts.load("p7m")
USDC_ADDRESS = "0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc"
BOBA_SPOKE_POOL_ADDRESS = "0xBbc6009fEfFc27ce705322832Cb2068F8C1e0A58"

OPTIMISM_TREASURY_SAFE_ADDRESS = "0x027F41F041Ed3d484296b9eF7B965d23aBf04200"

USDC_BAL = 11519

ACROSS_USDC_FEES_BASE = f"https://across.to/api/suggested-fees?token={USDC_ADDRESS}&destinationChainId={OPTIMISM}&originChainId={CHAIN}"


def main():
    treasury = ApeSafe("0x559dBda9Eb1E02c0235E245D9B175eb8DcC08398")

    boba_spoke_pool = interface.Boba_SpokePool(BOBA_SPOKE_POOL_ADDRESS, owner=treasury.account)
    usdc = interface.ERC20(USDC_ADDRESS, owner=treasury.account)
    usdc_scale = 10 ** usdc.decimals()

    USDC_BAL_SCALED = USDC_BAL * usdc_scale

    usdc_bal_across_fees = requests\
        .get(f"{ACROSS_USDC_FEES_BASE}&amount={USDC_BAL_SCALED}")\
        .json()

    usdc.approve(BOBA_SPOKE_POOL_ADDRESS, USDC_BAL_SCALED)

    boba_spoke_pool.deposit(
        OPTIMISM_TREASURY_SAFE_ADDRESS,
        USDC_ADDRESS,
        USDC_BAL_SCALED,
        OPTIMISM,
        usdc_bal_across_fees["relayFeePct"],
        usdc_bal_across_fees["timestamp"],
    )

    safe_tx = treasury.multisend_from_receipts()
    safe_tx.sign(DEPLOYER.private_key)
    treasury.post_transaction(safe_tx)
