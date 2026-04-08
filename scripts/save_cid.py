import json
import os

CID = os.environ.get("CID", "").strip()

if not CID:
    raise ValueError("Missing CID environment variable")

if CID.lower() == "dummy":
    raise ValueError("Refusing to write dummy CID")

output = {
    "cid": CID
}

with open("site/latest.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Wrote CID: {CID}")
