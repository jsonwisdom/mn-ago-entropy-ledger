# Minnesota Senate — Intentionally Empty Evidence Lane

**Status:** `GAP_RECEIPT`  
**Research authority:** `FALSE`  
**Governmental authority:** `NOT_COMPUTED`

This directory exists to record verified Minnesota Senate artifacts without inventing hearings, committee actions, votes, dockets, or authority.

The previously named fixture `MN-SENATE-COMMITTEE-HEARING-20260311` is retired from active fixtures because no official Minnesota Senate source was bound to it.

## Admission requirements

A Senate artifact may enter this lane only after recording:

1. official source URI or citation;
2. exact action identifier and date;
3. source bytes or an explicit byte-acquisition gap;
4. source hashes when bytes are possessed;
5. exact claim location;
6. provenance and authentication method;
7. action-specific `J/L/S/D/R/P` evaluation;
8. research boundary with `authority: false`.

## Source-state sequence

```text
FIXTURE_INITIALIZED
→ SOURCE_DISCOVERED
→ SOURCE_PARSED
→ SOURCE_BYTES_ACQUIRED
→ SOURCE_HASHED
→ CLAIM_REVERIFIED
→ J/L/S/D/R/P_EVALUATED
→ PRIMARY_BOUND | BINDING_UNRESOLVED | SOURCE_CONTRADICTION
```

## Discovery queue

Search official Minnesota Senate journals, committee schedules, hearing pages, minutes, audio/video records, and legislative publications. A search result alone does not establish binding.

## Locked doctrine

> Empty Senate is more honest than fake Senate.

> A plan is not a commit. A path is not a file. A source is not a binding. A binding is not authority.
