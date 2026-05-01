# Anchor 001 — Boundary

## This repo is an independent accountability ledger

`mn-ago-entropy-ledger` tracks receipt status using a tri-state classification system:

```text
GREEN / YELLOW / RED
```

It is not a cryptographic proof system.

## Canonical Anchor 001

| Field | Value |
|---|---|
| Source Repo | `jsonwisdom/Welcome-to-JSONWISDOM` |
| Git Commit | `13004719dd0c34f765ca95dfe8566b6feb2bf6cf` |
| Merkle Root (SHA-256) | `ff55160908ff41d23f7af0df8873ef7a0dcf8163d1a308f58941e87b5a95bad9` |
| Leaf Keccak-256 | `0xb7e55f9e1f4f27cd96f38d74e6510e184a14772ef3f9f628d5acc68531dd185d` |
| EAS Schema UID | `0x3bab210b4da3faff084e146075caf9168efb5c9c87f18509bca2c07d7f2e49c` |
| EAS Attestation UID | `0x18b5b00c62c648df2ccf4a746645493fa2a0b0dcda6697052d8c3a3d1586c142` |
| Chain | Base |
| Canonicalization | RFC 8785 JCS |
| Hash Pipeline | JCS → SHA-256 (Merkle) → Keccak-256 (leaf) → EAS (Base) |
| ENS | `DEFERRED` |

## Relationship

This ledger may reference or track receipts that are anchored elsewhere.

It does not produce Anchor 001 proofs.

Status classifications such as `GREEN`, `YELLOW`, and `RED` are operational indicators, not cryptographic attestations.

## Boundary Rule

Do not treat this repo's status labels, seed claims, or receipt records as Anchor 001 unless a specific cryptographic cross-reference is committed and independently verifiable.

Rule: no ghost anchor.
