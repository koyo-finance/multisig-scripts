from ape_safe import ApeSafe
from brownie import interface

def main():
    safe = ApeSafe("0x559dBda9Eb1E02c0235E245D9B175eb8DcC08398")

    four_pool_lp = interface.ERC20("0xDAb3Fc342A242AdD09504bea790f9b026Aa1e709", owner=safe.account)
    four_pool_gauge = interface.LiquidityGaugeV1("0x24f47A11AEE5d1bF96C18dDA7bB0c0Ef248A8e71", owner=safe.account)

    amount = four_pool_lp.balanceOf(safe.account)
    four_pool_lp.approve(four_pool_gauge, amount)
    four_pool_gauge.deposit(amount)

    safe_tx = safe.multisend_from_receipts()
    safe.post_transaction(safe_tx)
