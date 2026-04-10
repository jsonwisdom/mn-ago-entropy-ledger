import json
import os
import requests

PINATA_JWT = os.environ.get("PINATA_JWT")
PINATA_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

def main():
    if not PINATA_JWT:
        raise ValueError("Missing PINATA_JWT")

    path = "ledger/ledger.jsonl"
    with open(path, "rb") as f:
        response = requests.post(
            PINATA_URL,
            files={"file": (os.path.basename(path), f)},
            headers={"Authorization": f"Bearer {PINATA_JWT}"},
            timeout=60,
        )

    response.raise_for_status()
    data = response.json()
    cid = data.get("IpfsHash")
    if not cid:
        raise ValueError(f"Pinata response missing IpfsHash: {json.dumps(data)}")

    print(cid)

if __name__ == "__main__":
    main()
