# Ledger Status Boundary

## Tri-state classification is operational, not cryptographic

| Status | Meaning |
|---|---|
| GREEN | Receipts match across sources |
| YELLOW | Source missing, late, unclear, or not pinned |
| RED | Receipts contradict or show critical system risk |

These labels are accountability/status indicators.

They are not cryptographic finality by themselves.

## Byte verification gap

Some entries in `truth/receipts.json` have:

```json
"byte_verified": false
```

This means they have not been verified at the byte level against a canonical JCS Merkle tree.

They may be text-level or source-level matches only.

## Not a randomness beacon

Despite the repo name, `mn-ago-entropy-ledger` is an accountability receipts dataset.

It is not:

- an entropy source
- a randomness beacon
- a timestamping service
- the canonical Anchor 001 proof source

## Promotion to cryptographic finality

For a receipt in this ledger to be considered cryptographically anchored:

1. It should have a corresponding canonical artifact in `jsonwisdom/Welcome-to-JSONWISDOM` or another clearly named canonical proof repo.
2. It should pass RFC 8785 JCS canonicalization.
3. It should pass SHA-256 Merkle inclusion.
4. It should have a Keccak-256 leaf or content hash committed through a verifiable on-chain attestation such as EAS on Base.

Until then, it is a tracked observation, not a verified proof.

## Boundary Rule

Operational status is useful.

Cryptographic finality requires bytes, hashes, and an independently verifiable anchor.
