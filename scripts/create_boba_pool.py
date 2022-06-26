from brownie import interface, accounts


DEPLOYER = accounts.load("p7m")


def main():
    oracle_pool_factory = interface.OracleWeightedPoolFactory(
        "0x06f607EC266BB98bcb9Bae402D61Ab5E008ab018"
    )

    oracle_pool_factory.create(
        "Koyo 80 BOBA 20 wETH",
        "K-80BOBA-20wETH",
        [
            "0xa18bF3994C0Cc6E3b63ac420308E5383f53120D7", # BOBA
            "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", # wETH
        ],
        [800000000000000000, 200000000000000000],
        10000000000000000,
        True,
        DEPLOYER,
        {"from": DEPLOYER},
    )
