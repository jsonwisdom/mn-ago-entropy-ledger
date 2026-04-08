"""
diff.py — detect changes in AGO public pages
Auto-seeds baseline on first run so UI shows data immediately
Emits DIFF_RECEIPT when content changes, links to previous state
"""
import json, hashlib, datetime, requests
from pathlib import Path
from bs4 import BeautifulSoup

LEDGER = Path(__file__).parent.parent / "ledger" / "ledger.jsonl"
SNAPSHOT_DIR = Path(__file__).parent.parent / "ledger" / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "MN-AGO-Entropy-Ledger/1.0 (+public accountability)"}

WATCH_TARGETS = {
    "https://www.ag.state.mn.us/consumer/Publications/Scams.asp": "scam_alert_index",
    "https://www.ag.state.mn.us/consumer/": "consumer_hub",
    "https://www.ag.state.mn.us/Data-Requests/": "mgdpa_page",
    "https://www.ag.state.mn.us/Office/Communications/": "press_releases"
}

def sha256(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def fetch_and_clean(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title else url
    body_text = soup.get_text(" ", strip=True)
    body_text = " ".join(body_text.split())
    return title, body_text

def last_receipt_for_url(url):
    if not LEDGER.exists(): return None
    for line in reversed(LEDGER.read_text().strip().splitlines()):
        try:
            rec = json.loads(line)
            if rec.get("source_url") == url:
                return rec
        except: continue
    return None

def last_chain():
    if not LEDGER.exists(): return None
    lines = LEDGER.read_text().strip().splitlines()
    if not lines: return None
    return json.loads(lines[-1])["chain_hash"]

def append_receipt(rec):
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")

def is_first_run():
    if not LEDGER.exists(): return True
    lines = [l for l in LEDGER.read_text().strip().splitlines() if l]
    # consider first run if no DIFF_RECEIPT or BASELINE_RECEIPT exists yet
    for line in lines:
        try:
            rec = json.loads(line)
            if rec["type"] in ("DIFF_RECEIPT", "BASELINE_RECEIPT"):
                return False
        except: continue
    return True

def main():
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
    prev_chain = last_chain()
    new_count = 0
    first_run = is_first_run()
    
    for url, category in WATCH_TARGETS.items():
        try:
            title, body = fetch_and_clean(url)
            content = f"{title}|{url}|{body}"
            src_hash = sha256(content)
            last = last_receipt_for_url(url)
            
            if last and last["source_hash_sha256"] == src_hash:
                print(f"NOCHANGE {url}")
                continue
            
            chain_hash = sha256(src_hash if prev_chain is None else prev_chain + src_hash)
            
            snap_file = SNAPSHOT_DIR / f"{src_hash}.txt"
            snap_file.write_text(body, encoding="utf-8")
            
            if first_run:
                rec_type = "BASELINE_RECEIPT"
                state = "seeded"
                notes = "initial baseline for diff engine"
                print(f"SEED {url}")
            elif last:
                rec_type = "DIFF_RECEIPT"
                state = "changed"
                notes = f"content changed vs {last['receipt_id']}"
                print(f"DIFF {url}")
            else:
                rec_type = "SCAM_ALERT_RECEIPT" if "consumer" in url else "COMPLAINT_PATH_RECEIPT"
                state = "observed"
                notes = "new target discovered"
                print(f"NEW {url}")
            
            rec = {
                "receipt_id": f"REC-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]}",
                "type": rec_type,
                "source_url": url,
                "title": title,
                "first_seen_utc": now,
                "last_checked_utc": now,
                "source_hash_sha256": src_hash,
                "previous_hash": prev_chain,
                "chain_hash": chain_hash,
                "state": state,
                "category": category,
                "prev_receipt_id": last["receipt_id"] if last else None,
                "prev_source_hash": last["source_hash_sha256"] if last else None,
                "notes": notes
            }
            append_receipt(rec)
            prev_chain = chain_hash
            new_count += 1
            
        except Exception as e:
            print(f"ERR {url}: {e}")
    
    print(f"diff: {new_count} receipts appended")
    if first_run and new_count > 0:
        print("baseline seeded: UI will populate on next deploy")
    return new_count

if __name__ == "__main__":
    main()
