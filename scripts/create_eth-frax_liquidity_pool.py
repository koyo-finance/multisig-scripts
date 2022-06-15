from brownie import interface, accounts


DEPLOYER = accounts.load("p7m")


def main():
    oracle_pool_factory = interface.OracleWeightedPoolFactory(
        "0x06f607EC266BB98bcb9Bae402D61Ab5E008ab018"
    )

    oracle_pool_factory.create(
        "Koyo 50 FRAX 50 wETH",
        "K-50FRAX-50wETH",
        [
            "0x7562F525106F5d54E891e005867Bf489B5988CD9", # FRAX
            "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", # wETH
        ],
        [500000000000000000, 500000000000000000],
        5000000000000000,
        True,
        DEPLOYER,
        {"from": DEPLOYER},
    )
