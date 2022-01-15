import os
from pathlib import Path
import requests
from brownie import config

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
filepath = "./img/English.png"
filename = filepath.split("/")[-1:][0]
headers = {
    "pinata_api_key": config["pinata"]["key"],
    "pinata_secret_api_key": config["pinata"]["secret_key"],
}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
