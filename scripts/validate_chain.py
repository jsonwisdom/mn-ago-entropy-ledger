import json
import hashlib
import sys
from pathlib import Path

LEDGER = Path("ledger/ledger.jsonl")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def verify() -> bool:
    if not LEDGER.exists():
        print("FAIL: ledger.jsonl not found")
        return False

    lines = [line for line in LEDGER.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        print("OK: empty ledger")
        return True

    prev_chain = None
    for i, line in enumerate(lines, 1):
        rec = json.loads(line)
        required = ["receipt_id", "source_hash_sha256", "previous_hash", "chain_hash"]
        missing = [field for field in required if field not in rec]
        if missing:
            print(f"FAIL line {i}: missing fields {missing}")
            return False

        src = rec["source_hash_sha256"]
        expected_chain = sha256_text(src if prev_chain is None else prev_chain + src)

        if rec["previous_hash"] != prev_chain:
            print(f"FAIL line {i}: previous_hash mismatch")
            return False

        if rec["chain_hash"] != expected_chain:
            print(f"FAIL line {i}: chain_hash mismatch")
            return False

        prev_chain = rec["chain_hash"]

    print(f"OK: {len(lines)} receipts verified")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
