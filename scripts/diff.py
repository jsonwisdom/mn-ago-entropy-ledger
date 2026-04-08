"""
diff.py — detect changes in AGO public pages
Compares current page content against last known hash in ledger
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
    # strip scripts, styles, nav for stable hashing
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title else url
    body_text = soup.get_text(" ", strip=True)
    # normalize whitespace to avoid false diffs
    body_text = " ".join(body_text.split())
    return title, body_text

def last_receipt_for_url(url):
    if not LEDGER.exists(): return None
    for line in reversed(LEDGER.read_text().strip().splitlines()):
        rec = json.loads(line)
        if rec.get("source_url") == url:
            return rec
    return None

def last_chain():
    if not LEDGER.exists(): return None
    lines = LEDGER.read_text().strip().splitlines()
    if not lines: return None
    return json.loads(lines[-1])["chain_hash"]

def append_receipt(rec):
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")

def main():
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
    prev_chain = last_chain()
    new_diffs = 0
    
    for url, category in WATCH_TARGETS.items():
        try:
            title, body = fetch_and_clean(url)
            content = f"{title}|{url}|{body}"
            src_hash = sha256(content)
            last = last_receipt_for_url(url)
            
            if last and last["source_hash_sha256"] == src_hash:
                print(f"NOCHANGE {url}")
                continue
            
            # content changed or first observation
            chain_hash = sha256(src_hash if prev_chain is None else prev_chain + src_hash)
            
            # save snapshot for before/after
            snap_file = SNAPSHOT_DIR / f"{sha256(url)}.txt"
            if last:
                print(f"DIFF {url}")
                diff_type = "DIFF_RECEIPT"
                prev_snapshot = SNAPSHOT_DIR / f"{last['source_hash_sha256']}.txt"
                notes = f"content changed vs {last['receipt_id']}"
            else:
                print(f"NEW {url}")
                diff_type = "SCAM_ALERT_RECEIPT" if "consumer" in url else "COMPLAINT_PATH_RECEIPT"
                notes = "baseline snapshot"
            
            snap_file.write_text(body, encoding="utf-8")
            
            rec = {
                "receipt_id": f"REC-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "type": diff_type,
                "source_url": url,
                "title": title,
                "first_seen_utc": now,
                "last_checked_utc": now,
                "source_hash_sha256": src_hash,
                "previous_hash": prev_chain,
                "chain_hash": chain_hash,
                "state": "changed" if last else "observed",
                "category": category,
                "prev_receipt_id": last["receipt_id"] if last else None,
                "prev_source_hash": last["source_hash_sha256"] if last else None,
                "notes": notes
            }
            append_receipt(rec)
            prev_chain = chain_hash
            new_diffs += 1
            
        except Exception as e:
            print(f"ERR {url}: {e}")
    
    print(f"diff: {new_diffs} new receipts appended")
    return new_diffs

if __name__ == "__main__":
    main()
