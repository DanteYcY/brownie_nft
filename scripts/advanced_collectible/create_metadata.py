from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_language
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        # language = advanced_collectible.tokenIdToLanguage(token_id)
        language = get_language(advanced_collectible.tokenIdToLanguage(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{language}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite!")
        else:
            print(f"Creating metadata file {metadata_file_name}!")
            collectible_metadata["name"] = language
            collectible_metadata["description"] = "Most handsome gentleman at Stern"
            image_path = "./img/" + language + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/Chinese.png" -> "Chinese.png"
        filename = filepath.split("/")[-1:][0]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri