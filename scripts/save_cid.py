import json
import os

cid = os.environ.get("CID")

if not cid:
    raise ValueError("CID not provided")

os.makedirs("site", exist_ok=True)

with open("site/latest.json", "w", encoding="utf-8") as f:
    json.dump({"cid": cid}, f)

print(f"Saved CID: {cid}")
