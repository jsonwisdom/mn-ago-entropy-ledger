import json
import hashlib
import os
import requests
from datetime import datetime

URLS = [
    "https://www.ag.state.mn.us/consumer/",
    "https://www.ag.state.mn.us/Consumer/Publications/",
    "https://www.ag.state.mn.us/Office/DataRequests.asp",
    "https://www.ag.state.mn.us/Office/Complaints.asp"
]

LEDGER_PATH = "ledger/ledger.jsonl"
DIFF_PATH = "site/diff.json"

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def fetch(url):
    try:
        r = requests.get(url, timeout=10)
        return r.text.strip()
    except:
        return ""

def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def append_ledger(entry):
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def write_diff(entries):
    with open(DIFF_PATH, "w") as f:
        json.dump(entries[-20:], f, indent=2)

def main():
    now = datetime.utcnow().isoformat() + "Z"
    ledger = load_ledger()

    last_hash = None
    if ledger:
        last_hash = ledger[-1]["chain_hash"]

    outputs = []

    for url in URLS:
        content = fetch(url)
        source_hash = sha256(content)

        receipt_id = f"REC-{len(ledger)+1:04d}"

        chain_input = (last_hash or "") + source_hash
        chain_hash = sha256(chain_input)

        receipt = {
            "receipt_id": receipt_id,
            "type": "BASELINE_RECEIPT" if not ledger else "DIFF_RECEIPT",
            "source_url": url,
            "timestamp": now,
            "source_hash_sha256": source_hash,
            "previous_hash": last_hash,
            "chain_hash": chain_hash
        }

        append_ledger(receipt)

        outputs.append({
            "time": now,
            "page": url,
            "state": "seeded" if not ledger else "checked",
            "link": url
        })

        last_hash = chain_hash
        ledger.append(receipt)

    write_diff(outputs)

if __name__ == "__main__":
    main()
