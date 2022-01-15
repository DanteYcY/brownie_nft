from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/QmTUC7cCL8dB1tXQLNn45hUjAAs9AvAEM8HgeD5xxXvr5H?filename=0-Chinese.json"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    print("Contract Deployed!")
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"You can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )
    return simple_collectible


def main():
    deploy_and_create()