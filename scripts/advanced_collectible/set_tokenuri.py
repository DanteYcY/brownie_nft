from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_language, get_account, OPENSEA_URL

dog_metadata_dic = {
    "Chinese": "https://ipfs.io/ipfs/QmTUC7cCL8dB1tXQLNn45hUjAAs9AvAEM8HgeD5xxXvr5H?filename=1-Chinese.json",
    "English": "https://ipfs.io/ipfs/QmcwXiniTg77v9BX9Z5VnAjN51LsH7RugcQARYBdsJCfSj?filename=2-English.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        language = get_language(advanced_collectible.tokenIdToLanguage(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[language])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address,token_id)}"
    )
