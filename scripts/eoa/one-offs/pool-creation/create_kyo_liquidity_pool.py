from brownie import interface, accounts


DEPLOYER = accounts.load("p7m")


def main():
    oracle_pool_factory = interface.OracleWeightedPoolFactory(
        "0x06f607EC266BB98bcb9Bae402D61Ab5E008ab018"
    )

    oracle_pool_factory.create(
        "Koyo 70 KYO 30 wETH",
        "K-70KYO-30wETH",
        [
            "0x618CC6549ddf12de637d46CDDadaFC0C2951131C", # KYO
            "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", # wETH
        ],
        [700000000000000000, 300000000000000000],
        30000000000000000,
        True,
        DEPLOYER,
        {"from": DEPLOYER},
    )
