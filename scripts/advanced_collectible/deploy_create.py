from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    fund_with_link,
    get_contract,
)
from brownie import AdvancedCollectible, config, network


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
    )
    tx01 = fund_with_link(advanced_collectible.address)
    tx01.wait(1)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created")


def main():
    deploy_and_create()