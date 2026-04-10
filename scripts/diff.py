import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

TARGETS = [
    {"id": "consumer", "url": "https://www.ag.state.mn.us/consumer/"},
    {"id": "data_requests", "url": "https://www.ag.state.mn.us/Data-Requests/"},
    {"id": "scams", "url": "https://www.ag.state.mn.us/Consumer/Scams/"},
    {"id": "communications", "url": "https://www.ag.state.mn.us/Office/Communications.asp"},
]

DIFF_PATH = Path("site/diff.json")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def fetch(url: str) -> str:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def load_previous():
    if not DIFF_PATH.exists():
        return {}
    obj = json.loads(DIFF_PATH.read_text())
    return {row["source_url"]: row for row in obj.get("data", [])}

def main():
    prev = load_previous()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rows = []

    for t in TARGETS:
        body = fetch(t["url"])
        h = sha256_text(body)
        prev_row = prev.get(t["url"])
        prev_hash = prev_row["source_hash_sha256"] if prev_row else None

        if prev_hash is None:
            state = "seeded"
        elif prev_hash == h:
            state = "unchanged"
        else:
            state = "changed"

        rows.append({
            "receipt_id": f"BASELINE-{t['id']}",
            "source_url": t["url"],
            "prev_source_hash": prev_hash,
            "source_hash_sha256": h,
            "state": state,
            "time": now
        })

    DIFF_PATH.parent.mkdir(parents=True, exist_ok=True)
    DIFF_PATH.write_text(json.dumps({"data": rows}, indent=2))

if __name__ == "__main__":
    main()
