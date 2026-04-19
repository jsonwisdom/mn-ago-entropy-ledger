import json

def read_dyn(data, idx):
    try:
        off = int(data[idx*64:(idx+1)*64], 16) * 2
        ln = int(data[off:off+64], 16) * 2
        raw = data[off+64:off+64+ln]
        return bytes.fromhex(raw).decode()
    except:
        return None

def parse_raw_logs(text):
    blocks = text.split("- address: ")
    rows = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        lines = b.splitlines()
        # The FIX: Capture the address immediately after the split
        address = lines[0].strip() if lines else None
        row = {"address": address}
        for line in lines[1:]:
            if ":" in line and not line.strip().startswith("topics"):
                k, v = line.split(":", 1)
                row[k.strip()] = v.strip()
        data = row.get("data", "").replace("0x", "")
        if len(data) < 256:
            continue
        try:
            rows.append({
                "contract": row.get("address"),
                "blockNumber": int(row.get("blockNumber", 0)),
                "transactionHash": row.get("transactionHash"),
                "logIndex": int(row.get("logIndex", 0)),
                "commitmentHash": "0x" + data[128:192],
                "agentId": read_dyn(data, 0),
                "tradeId": read_dyn(data, 1),
                "uri": read_dyn(data, 3)
            })
        except:
            continue
    return rows
