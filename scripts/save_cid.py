import json
import os

CID = os.environ.get("CID")

if not CID:
    raise ValueError("CID not provided")

os.makedirs("site", exist_ok=True)

with open("site/latest.json", "w") as f:
    json.dump({"cid": CID}, f)

print(f"Saved CID: {CID}")
