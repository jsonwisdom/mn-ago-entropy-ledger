import json
import sqlite3
from pathlib import Path

from decoder import parse_raw_logs

RAW_LOG_CANDIDATES = [
    "raw_logs.txt",
    "court_fixed.jsonl",
]
DB_PATH = "court.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS proofs (
    contract TEXT NOT NULL,
    blockNumber INTEGER NOT NULL,
    transactionHash TEXT,
    logIndex INTEGER NOT NULL,
    commitmentHash TEXT,
    agentId TEXT,
    tradeId TEXT,
    uri TEXT,
    PRIMARY KEY (transactionHash, logIndex)
);
"""


def load_source_text() -> str:
    for candidate in RAW_LOG_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path.read_text(encoding="utf-8")
    raise FileNotFoundError(
        "Missing source log file. Expected one of: " + ", ".join(RAW_LOG_CANDIDATES)
    )


def normalize_rows(text: str):
    rows = parse_raw_logs(text)
    normalized = []
    for row in rows:
        contract = row.get("contract")
        if not contract:
            continue
        normalized.append(
            {
                "contract": contract,
                "blockNumber": int(row.get("blockNumber", 0) or 0),
                "transactionHash": row.get("transactionHash"),
                "logIndex": int(row.get("logIndex", 0) or 0),
                "commitmentHash": row.get("commitmentHash"),
                "agentId": row.get("agentId"),
                "tradeId": row.get("tradeId"),
                "uri": row.get("uri"),
            }
        )
    return normalized


def ingest(rows, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(SCHEMA)
        conn.executemany(
            """
            INSERT OR REPLACE INTO proofs (
                contract, blockNumber, transactionHash, logIndex,
                commitmentHash, agentId, tradeId, uri
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["contract"],
                    row["blockNumber"],
                    row["transactionHash"],
                    row["logIndex"],
                    row["commitmentHash"],
                    row["agentId"],
                    row["tradeId"],
                    row["uri"],
                )
                for row in rows
            ],
        )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    source_text = load_source_text()
    rows = normalize_rows(source_text)
    ingest(rows)
    print(f"Ingested {len(rows)} records into {DB_PATH}")
