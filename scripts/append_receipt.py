import json
import hashlib
from datetime import datetime, timezone

LEDGER_PATH = "ledger/ledger.jsonl"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def load_entries():
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

entries = load_entries()
last_chain_hash = entries[-1]["chain_hash"] if entries else "GENESIS"

receipt_id = input("receipt_id: ").strip()
entry_type = input("type: ").strip()
source_url = input("source_url: ").strip()
title = input("title: ").strip()
source_hash_sha256 = input("source_hash_sha256: ").strip()
notes = input("notes: ").strip()

entry = {
    "receipt_id": receipt_id,
    "type": entry_type,
    "source_url": source_url,
    "title": title,
    "first_seen_utc": now_utc(),
    "source_hash_sha256": source_hash_sha256,
    "previous_chain_hash": last_chain_hash,
    "chain_hash": sha256_text(last_chain_hash + source_hash_sha256),
    "notes": notes
}

with open(LEDGER_PATH, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, separators=(",", ":")) + "\n")

print("✅ Appended entry")
print(json.dumps(entry, indent=2))
