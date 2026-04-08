import json

cid = input().strip()

with open("site/latest.json", "w") as f:
    json.dump({"cid": cid}, f)
