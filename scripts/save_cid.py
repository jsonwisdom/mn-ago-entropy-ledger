import json
import os
from pathlib import Path

CID = os.environ.get("CID", "").strip()
SITE_PATH = Path("site/latest.json")

def main():
    if not CID or CID.lower() == "dummy":
        raise ValueError("Missing or invalid CID")

    SITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SITE_PATH.write_text(json.dumps({"cid": CID}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
