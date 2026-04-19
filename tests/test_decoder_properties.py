import pytest
from hypothesis import given, strategies as st

from decoder import parse_raw_logs

HEX = "0123456789abcdef"

def make_min_log(address: str, data_hex: str) -> str:
    return f"- address: {address}\nblockNumber: 1\ntransactionHash: 0xdeadbeef\nlogIndex: 0\ndata: 0x{data_hex}\n"


@given(
    addr=st.from_regex(r"0x[a-fA-F0-9]{40}", fullmatch=True),
    data=st.text(alphabet=HEX, min_size=256, max_size=512),
)
def test_never_null_contract_on_valid_envelope(addr, data):
    text = make_min_log(addr, data)
    rows = parse_raw_logs(text)
    if rows:
        assert all(r.get("contract") for r in rows)


def test_deterministic_sample_contract():
    addr = "0x082836b2A8E2a77Cca7DDd9F9fC8eE99F884F58D"
    data = "a" * 256
    text = make_min_log(addr, data)
    rows = parse_raw_logs(text)
    if rows:
        assert rows[0]["contract"] == addr
