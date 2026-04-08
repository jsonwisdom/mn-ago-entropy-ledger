import json, hashlib

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

with open("ledger/ledger.jsonl") as f:
    lines = [json.loads(l) for l in f]

prev = "GENESIS"

for i, r in enumerate(lines):
    expected = sha256(prev + r["source_hash_sha256"])
    
    if r["chain_hash"] != expected:
        print(f"❌ Chain broken at line {i+1}")
        exit(1)
    
    prev = r["chain_hash"]

print("✅ Chain valid")
