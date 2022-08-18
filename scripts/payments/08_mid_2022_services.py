from brownie import interface, accounts
from ape_safe import ApeSafe
import requests


CHAIN = 288
ETH_MAINNET = 1
DEPLOYER = accounts.load("p7m")
USDC_ADDRESS = "0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc"
BOBA_SPOKE_POOL_ADDRESS = "0xBbc6009fEfFc27ce705322832Cb2068F8C1e0A58"
S_ADDRESS = "0xa31AdEdc1dc31Af8e75750a0E6967fB38a17dc46"
P_N_ADDRESS = "0x6ABAF139796152e23633C007E89888c07E64710b"

B_AMOUNT = 150
SERV_AMOUNT = 500

S_AMOUNT_BRIDGE = B_AMOUNT
P_N_AMOUNT_BRIDGE = SERV_AMOUNT

ACROSS_USDC_FEES_BASE = f"https://across.to/api/suggested-fees?token={USDC_ADDRESS}&destinationChainId={ETH_MAINNET}&originChainId={CHAIN}"


def main():
    treasury = ApeSafe("0x559dBda9Eb1E02c0235E245D9B175eb8DcC08398")

    boba_spoke_pool = interface.Boba_SpokePool(BOBA_SPOKE_POOL_ADDRESS, owner=treasury.account)
    usdc = interface.ERC20(USDC_ADDRESS, owner=treasury.account)
    usdc_scale = 10 ** usdc.decimals()

    S_AMOUNT_SCALED = S_AMOUNT_BRIDGE * usdc_scale
    P_N_AMOUNT_SCALED = P_N_AMOUNT_BRIDGE * usdc_scale

    s_across_fees = requests\
        .get(f"{ACROSS_USDC_FEES_BASE}&amount={S_AMOUNT_SCALED}")\
        .json()
    p_n_across_fees = requests\
        .get(f"{ACROSS_USDC_FEES_BASE}&amount={P_N_AMOUNT_SCALED}")\
        .json()

    usdc.approve(BOBA_SPOKE_POOL_ADDRESS, S_AMOUNT_SCALED + P_N_AMOUNT_SCALED)

    boba_spoke_pool.deposit(
        S_ADDRESS,
        USDC_ADDRESS,
        S_AMOUNT_SCALED,
        ETH_MAINNET,
        s_across_fees["relayFeePct"],
        s_across_fees["timestamp"],
    )
    boba_spoke_pool.deposit(
        P_N_ADDRESS,
        USDC_ADDRESS,
        P_N_AMOUNT_SCALED,
        ETH_MAINNET,
        p_n_across_fees["relayFeePct"],
        p_n_across_fees["timestamp"],
    )

    safe_tx = treasury.multisend_from_receipts()
    safe_tx.sign(DEPLOYER.private_key)
    treasury.post_transaction(safe_tx)
