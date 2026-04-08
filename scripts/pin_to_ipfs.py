import os
import requests

JWT = os.environ["PINATA_JWT"]

url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

headers = {
    "Authorization": f"Bearer {JWT}"
}

with open("ledger/ledger.jsonl", "rb") as f:
    files = {
        "file": ("ledger.jsonl", f)
    }

    r = requests.post(url, headers=headers, files=files)
    r.raise_for_status()

    data = r.json()
    print("CID:", data["IpfsHash"])
