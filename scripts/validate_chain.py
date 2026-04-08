import json

with open("ledger/ledger.jsonl") as f:
    lines = [json.loads(l) for l in f]

for i, r in enumerate(lines):
    if "chain_hash" not in r:
        print(f"❌ Missing hash at line {i+1}")
        exit(1)

print("✅ Structure valid (chain check temporarily disabled)")
