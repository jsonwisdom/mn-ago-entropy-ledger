import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path("ledger/ledger.jsonl")
DIFF_PATH = Path("site/diff.json")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def load_ledger():
    if not LEDGER_PATH.exists():
        return []
    return [json.loads(line) for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]

def load_diff():
    obj = json.loads(DIFF_PATH.read_text(encoding="utf-8"))
    return obj.get("data", [])

def make_receipt_id(ts: str, n: int) -> str:
    return f"REC-{ts.replace('-', '').replace(':', '').replace('T', '-').replace('Z', '')}-{n:04d}"

def title_from_url(url: str) -> str:
    path = url.rstrip("/").split("/")[-1]
    return path or "root"

def main():
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    entries = load_ledger()
    rows = load_diff()

    last_by_url = {}
    for entry in entries:
        last_by_url[entry["source_url"]] = entry

    prev_chain = entries[-1]["chain_hash"] if entries else None
    ts = now_utc()
    counter = 1
    appended = []

    for row in rows:
        url = row["source_url"]
        src_hash = row["source_hash_sha256"]
        last = last_by_url.get(url)

        if last and last["source_hash_sha256"] == src_hash:
            continue

        chain_hash = sha256_text(src_hash if prev_chain is None else prev_chain + src_hash)

        entry = {
            "receipt_id": make_receipt_id(ts, counter),
            "type": "PUBLIC_PAGE_OBSERVATION",
            "source_url": url,
            "title": title_from_url(url),
            "first_seen_utc": ts,
            "source_hash_sha256": src_hash,
            "previous_hash": prev_chain,
            "chain_hash": chain_hash,
            "state": row["state"],
            "notes": f"auto-appended from diff state={row['state']}"
        }

        appended.append(entry)
        prev_chain = chain_hash
        counter += 1

    if appended:
        with LEDGER_PATH.open("a", encoding="utf-8") as f:
            for entry in appended:
                f.write(json.dumps(entry, separators=(",", ":")) + "\n")

if __name__ == "__main__":
    main()
