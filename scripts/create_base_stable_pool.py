from brownie import interface, accounts


DEPLOYER = accounts.load("p7m")


def main():
    stable_pool_factory = interface.StablePoolFactory(
        "0xb4455B572b4dBF39d76a10de530988803C13d854"
    )

    stable_pool_factory.create(
        "Koyo FRAX<>USDC",
        "K-FraxBP",
        [
            "0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc", # USDC
            "0x7562F525106F5d54E891e005867Bf489B5988CD9", # FRAX
        ],
        200,
        5000000000000000,
        "0xBA1BA1ba1BA1bA1bA1Ba1BA1ba1BA1bA1ba1ba1B",
        {"from": DEPLOYER},
    )
