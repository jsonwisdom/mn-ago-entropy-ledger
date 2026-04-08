import json
import hashlib
import sys

LEDGER_PATH = "ledger/ledger.jsonl"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def expected_chain_hash(previous_chain_hash: str, source_hash_sha256: str) -> str:
    return sha256_text(previous_chain_hash + source_hash_sha256)

with open(LEDGER_PATH, "r", encoding="utf-8") as f:
    raw_lines = [line.strip() for line in f if line.strip()]

if not raw_lines:
    print("❌ Ledger is empty")
    sys.exit(1)

previous = "GENESIS"

for i, line in enumerate(raw_lines, start=1):
    try:
        entry = json.loads(line)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON at line {i}: {e}")
        sys.exit(1)

    required = [
        "receipt_id",
        "type",
        "source_url",
        "first_seen_utc",
        "source_hash_sha256",
        "previous_chain_hash",
        "chain_hash"
    ]

    missing = [key for key in required if key not in entry]
    if missing:
        print(f"❌ Missing fields at line {i}: {', '.join(missing)}")
        sys.exit(1)

    if entry["previous_chain_hash"] != previous:
        print(f"❌ previous_chain_hash mismatch at line {i}")
        print(f"   expected: {previous}")
        print(f"   found:    {entry['previous_chain_hash']}")
        sys.exit(1)

    expected = expected_chain_hash(previous, entry["source_hash_sha256"])

    if entry["chain_hash"] != expected:
        print(f"❌ chain_hash mismatch at line {i}")
        print(f"   expected: {expected}")
        print(f"   found:    {entry['chain_hash']}")
        sys.exit(1)

    previous = entry["chain_hash"]

print(f"✅ Strict chain valid ({len(raw_lines)} entries)")
