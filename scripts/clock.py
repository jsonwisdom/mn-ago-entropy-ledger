import json
from datetime import datetime, timezone, timedelta

LEDGER_PATH = "ledger/ledger.jsonl"
SITE_PATH = "site/clock.json"

def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def business_days(start, end):
    days = 0
    cur = start
    while cur < end:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days

def main():
    with open(LEDGER_PATH, "r") as f:
        entries = [json.loads(l) for l in f if l.strip()]

    # target receipt #002
    target = None
    for e in entries:
        if e["receipt_id"] == "REC-2026-0002":
            target = e
            break

    if not target:
        print("No receipt #002 found")
        return

    start = parse_dt(target["first_seen_utc"])
    now = datetime.now(timezone.utc)

    days_open = business_days(start, now)
    deadline = 10
    remaining = max(0, deadline - days_open)
    overdue = max(0, days_open - deadline)

    status = "on_time"
    if overdue > 0:
        status = "overdue"
    elif remaining <= 2:
        status = "due_soon"

    out = {
        "receipt_id": "REC-2026-0002",
        "days_open": days_open,
        "deadline_days": deadline,
        "days_remaining": remaining,
        "days_overdue": overdue,
        "status": status,
        "last_updated": now.isoformat()
    }

    with open(SITE_PATH, "w") as f:
        json.dump(out, f)

    print("Clock updated:", out)

if __name__ == "__main__":
    main()
