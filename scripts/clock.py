import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

LEDGER_PATH = Path("ledger/ledger.jsonl")
SITE_PATH = Path("site/clock.json")

def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def business_days(start: datetime, end: datetime) -> int:
    days = 0
    cur = start
    while cur < end:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days

def main():
    SITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER_PATH.exists():
        SITE_PATH.write_text(json.dumps({"tracking_available": False, "reason": "missing ledger"}, indent=2), encoding="utf-8")
        return

    entries = [json.loads(l) for l in LEDGER_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    receipts = [e for e in entries if e.get("type") == "DATA_REQUEST_RECEIPT"]

    if not receipts:
        SITE_PATH.write_text(json.dumps({"tracking_available": False, "reason": "no DATA_REQUEST_RECEIPT entries"}, indent=2), encoding="utf-8")
        return

    target = receipts[-1]
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
        "tracking_available": True,
        "receipt_id": target["receipt_id"],
        "days_open": days_open,
        "deadline_days": deadline,
        "days_remaining": remaining,
        "days_overdue": overdue,
        "status": status,
        "last_updated": now.replace(microsecond=0).isoformat()
    }
    SITE_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
