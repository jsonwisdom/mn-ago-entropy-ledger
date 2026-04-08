"""
validate_chain.py — verifies hash chain integrity
Expects: chain_hash, previous_hash, source_hash_sha256 in each receipt
"""
import json, hashlib, sys
from pathlib import Path

LEDGER = Path(__file__).parent.parent / "ledger" / "ledger.jsonl"

def sha256(s): 
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def verify():
    if not LEDGER.exists():
        print("FAIL: ledger.jsonl not found")
        return False
    
    lines = [l for l in LEDGER.read_text().strip().splitlines() if l]
    if not lines:
        print("OK: empty ledger, nothing to validate")
        return True
    
    prev_chain = None
    for i, line in enumerate(lines, 1):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"FAIL line {i}: invalid JSON: {e}")
            return False
        
        # required fields check
        required = ["receipt_id", "source_hash_sha256", "chain_hash"]
        missing = [f for f in required if f not in rec]
        if missing:
            print(f"FAIL line {i}: missing fields: {', '.join(missing)}")
            return False
        
        src = rec["source_hash_sha256"]
        expected_chain = sha256(src if prev_chain is None else prev_chain + src)
        
        if rec["chain_hash"] != expected_chain:
            print(f"FAIL line {i}: chain broken")
            print(f"  expected: {expected_chain}")
            print(f"  got:      {rec['chain_hash']}")
            return False
        
        # previous_hash must match previous chain_hash, or be null for genesis
        expected_prev = prev_chain
        actual_prev = rec.get("previous_hash")
        if actual_prev != expected_prev:
            print(f"FAIL line {i}: previous_hash mismatch")
            print(f"  expected: {expected_prev}")
            print(f"  got:      {actual_prev}")
            return False
        
        prev_chain = rec["chain_hash"]
    
    print(f"OK: {len(lines)} receipts verified, chain intact")
    print(f"Latest chain_hash: {prev_chain}")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
