import os
import json
import requests

PINATA_JWT = os.environ.get("PINATA_JWT")

if not PINATA_JWT:
    raise ValueError("Missing PINATA_JWT")

PINATA_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

def pin_file(path: str) -> str:
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
    return cid

def main():
    target = "ledger/ledger.jsonl"
    if not os.path.exists(target):
        raise FileNotFoundError(f"Missing file to pin: {target}")

    cid = pin_file(target)
    print(f"CID: {cid}")

if __name__ == "__main__":
    main()
