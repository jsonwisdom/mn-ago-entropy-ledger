# MN_JUDICIARY_001 — Public Audit Summary

## Case

- Case number: `27-CR-23-25929`
- Venue: Hennepin County District Court
- Defendant: Abdirashid Ismail Said
- Judge: Juan Hoyos
- System lane: Judiciary

## Audit Claim

Known flight-risk inputs existed in the court record. A $150,000 bond path was used. The defendant failed to appear before trial. The bond was forfeited. Reporting consistently states the bail structure allowed the defendant to retain his passport.

## Chain State

```text
R0 → claim committed
R1 → evidence slots opened
R2 → irrelevant context source pinned but rejected as proof
R3 → case source URL pinned
R4 → KARE 11 excerpt pinned for bail mechanics
R5 → primary court record links pinned
R6 → primary court text excerpts pinned
R7 → full byte-replay target opened
```

## Primary-Locked Facts

From court-record excerpts pinned in R6:

- $150,000 bond posted on 12/08/2023
- Defendant failed to appear
- Bond was forfeited
- Judge Juan Hoyos signed the forfeiture order dated 4/7/2026
- Investigator filing documented family ties in Nairobi, Kenya and warned of potential flight risk

## Strong Secondary Alignment

Multiple contemporaneous reports state the bail mechanics as:

- $50,000 bond with passport surrender
- $150,000 bond with no conditions
- Defendant chose the higher amount and kept his passport

This remains secondary until the original bail order, conditions document, hearing transcript, or audio transcript is pinned.

## Status

```text
FUNCTIONALLY VERIFIED
PRIMARY + MULTI-SOURCE SECONDARY ALIGNMENT
NOT FULL BYTE-REPLAY LOCKED
```

## Next Hard Lock

R7 requires:

- raw PDF SHA-256 hashes
- `pdftotext -layout -nopgbrk` output hashes
- canonical excerpt match

## Principle

The system does not prove intent. It proves the failure trace:

```text
known flight risk → bond outcome → failure to appear → bond forfeiture
```

⚙️ jaywisdom.base.eth
