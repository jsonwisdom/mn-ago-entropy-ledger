import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path("ledger/schema.json")
LEDGER_PATH = Path("ledger/ledger.jsonl")

def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    if not LEDGER_PATH.exists():
        print("OK: no ledger file yet")
        return

    lines = [line for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    for i, line in enumerate(lines, 1):
        entry = json.loads(line)
        errors = sorted(validator.iter_errors(entry), key=lambda e: e.path)
        if errors:
            print(f"FAIL line {i}: schema violation")
            for err in errors:
                print(err.message)
            sys.exit(1)

    print(f"OK: schema valid for {len(lines)} entries")

if __name__ == "__main__":
    main()
