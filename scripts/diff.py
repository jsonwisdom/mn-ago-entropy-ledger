import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests

TARGETS = [
    {"id": "consumer", "url": "https://www.ag.state.mn.us/consumer/"},
    {"id": "data_requests", "url": "https://www.ag.state.mn.us/Data-Requests/"},
    {"id": "scams", "url": "https://www.ag.state.mn.us/consumer/scams/"},
    {"id": "press", "url": "https://www.ag.state.mn.us/Office/PressRelease/"},
]

DIFF_PATH = Path("site/diff.json")
USER_AGENT = "mn-ago-entropy-ledger/2.0"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def fetch(url: str) -> str:
    response = requests.get(url, timeout=20, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    return response.text

def load_previous():
    if not DIFF_PATH.exists():
        return {}
    obj = json.loads(DIFF_PATH.read_text(encoding="utf-8"))
    rows = obj.get("data", [])
    return {row["source_url"]: row for row in rows if "source_url" in row}

def main():
    previous = load_previous()
    rows = []
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    for target in TARGETS:
        body = fetch(target["url"])
        current_hash = sha256_text(body)
        prev = previous.get(target["url"])
        prev_hash = prev.get("source_hash_sha256") if prev else None

        if prev_hash is None:
            state = "seeded"
        elif prev_hash == current_hash:
            state = "unchanged"
        else:
            state = "changed"

        rows.append({
            "receipt_id": f"BASELINE-{target['id']}",
            "source_url": target["url"],
            "prev_source_hash": prev_hash,
            "source_hash_sha256": current_hash,
            "state": state,
            "time": now
        })

    payload = {
        "description": "Generated diff state for monitored targets",
        "schema": "array of {receipt_id, source_url, prev_source_hash, source_hash_sha256, state, time}",
        "data": rows
    }
    DIFF_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
