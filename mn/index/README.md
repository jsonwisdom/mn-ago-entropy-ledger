# Minnesota Artifact Registry

This directory contains the candidate registry for Minnesota research artifacts managed under JQG-50 v0.4.5.

## Governance state

- Registry status: `CANDIDATE`
- Canonical on `main`: `FALSE`
- Pull request: `#6`
- Merge binding: `PENDING_MERGE_SHA`
- Research authority: `FALSE`
- Governmental authority: `NOT IMPLIED`

## Evidence states

- `UNBOUND`: no sufficient evidence pointer or receipt is committed for the claim.
- `PENDING`: a source or migration target is known, but required bytes, hashes, provenance, or review remain incomplete.
- `VERIFIED`: committed evidence supports the exact scoped claim named by the entry.

`VERIFIED` must always declare its scope. Verification of repository existence does not verify repository contents, institutional status, or governmental authority.

## Provenance

The registry is canonical only after merge to the default branch and identification of the actual merge commit. Before merge:

```text
registry_status = CANDIDATE
merge_binding = PENDING_MERGE_SHA
```

A pull-request test merge SHA is not the final merge SHA.

## Boundaries

- A URI establishes discovery, not possession.
- Exact bytes establish possession.
- A hash identifies exact bytes.
- A receipt records an observed event or verification step.
- A merge records repository acceptance.
- None of these independently creates governmental authority.
