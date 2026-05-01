# MN AGO Entropy Ledger

> **Status: ACCOUNTABILITY RECEIPTS DATASET**
>
> This repository tracks receipts using a tri-state classification system across three lanes: `LAW`, `JUDICIARY`, and `AUDIT`.
>
> It is not:
>
> - an entropy source or randomness beacon
> - a timestamping service
> - a cryptographic proof system
> - the canonical Anchor 001 source
>
> Byte verification matters: some receipts may be text-verified or source-level verified but not byte-verified.
>
> See `docs/LEDGER_STATUS_BOUNDARY.md` for the distinction between operational status tracking and cryptographic finality.
>
> See `docs/ANCHOR_001_BOUNDARY.md` for the Anchor 001 boundary.

Public control plane for Minnesota accountability receipts.

## Tri-State Auditing System

This repo tracks Minnesota public-system claims through three lanes:

- **LAW** — statute, bill, and enacted-text verification
- **JUDICIARY** — court orders, bail terms, charges, outcomes, docket-backed records
- **AUDIT** — OLA reports, agency claims, findings, and contradictions

## Status Rules

- **GREEN**: receipts match; claim holds
- **YELLOW**: source missing, late, unclear, or not pinned
- **RED**: receipts contradict the claim or show critical system risk

## Current Anchor

- `MN_JUDICIARY_001`
- Status: `RED_REPORTED_NOT_PINNED`
- Truth level: reported signal, pending official court record and source hashes

## Principle

Trust is culture. Verification is infrastructure.

⚙️ jaywisdom.base.eth
