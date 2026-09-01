# BOXD Goblin Courts — SuperSecretSisterSearchSyntax v0.1

**Mode:** SATIRICAL_SEARCH_RECIPE / PUBLIC_SOURCE_ONLY  
**Authority created:** false  
**Secret status:** NOT ACTUALLY SECRET  
**Purpose:** Make public Justice.gov / SDNY / Epstein-library research reproducible, funny, and hard to hand-wave.

## LeahPrime Narrator

> "Welcome to Super Secret Sister Search, where the secret is that the website is public, the documents are public, and the hardest part is remembering which institutional cup the pea is under."
>
> "Blind Justice may wear a blindfold. BoxD does not let the spreadsheet wear one."
>
> "SDNY Three-Card Monte: Court Record, Press Release, Disclosure Set. Pick a card. Wrong answer. You need all three."

## Rule Zero

Search syntax is discovery, **not proof**.

```text
SEARCH RESULT
  -> OFFICIAL SOURCE
  -> EXACT DOCUMENT / DOCKET / DATASET
  -> FREEZE BYTES
  -> HASH
  -> CLAIM BIND
  -> BURDEN CLASS
  -> REPLAY
```

A search miss is not proof that a record does not exist. DOJ itself warns that portions of the Epstein Library may not be reliably electronically searchable because of technical limitations and source formats.

## Public search-engine recipes

These are ordinary public web-search recipes, not privileged DOJ commands.

```text
site:justice.gov/epstein "EFTA"
site:justice.gov/epstein "United States v. Maxwell"
site:justice.gov/epstein "S.D.N.Y."
site:justice.gov/epstein "19-2221"
site:justice.gov/epstein "1:20-cr-00330"
site:justice.gov/epstein "memoranda and correspondence"
site:justice.gov/epstein "letter to Congress"

site:justice.gov/usao-sdny "Jeffrey Epstein"
site:justice.gov/usao-sdny "Ghislaine Maxwell"
site:justice.gov/usao-sdny "victim witness" Epstein
site:justice.gov/usao-sdny "civil frauds"

site:justice.gov/usao-mn fraud Minnesota
site:justice.gov/usao-mn Medicaid fraud Minnesota
site:justice.gov/usao-mn "Feeding Our Future"
```

## Justice.gov path pivots

```text
/epstein
/epstein/search
/epstein/doj-disclosures
/epstein/doj-disclosures/data-set-{N}-files
/epstein/doj-disclosures/court-records-*
/epstein/doj-disclosures/memoranda-and-correspondence
/usao-sdny
/usao-sdny/pr/*
/usao-sdny/programs/victim-witness-services
/usao-mn/pr/*
```

## SDNY Three-Card Monte — evidence version

The joke is institutional routing, not an allegation of misconduct.

```text
CARD_A = PRESS_RELEASE
CARD_B = COURT_RECORD
CARD_C = DISCLOSURE_INDEX

IF only_one_card_found:
    verdict = HOLD
IF cards_disagree:
    verdict = CONFLICT
IF source_is_press_release_only:
    evidence_class = OFFICIAL_SUMMARY_NOT_UNDERLYING_DOCKET
IF court_record_is_bound:
    promote_only_the_claims_the_record_supports
```

## Sister Search pivots

For every named person, event, file, or office:

```text
NAME
 -> exact phrase
 -> alias / initials
 -> docket number
 -> EFTA identifier
 -> office/component
 -> date window
 -> document class
 -> correction / amended / superseding
 -> congressional correspondence
 -> OIG / oversight
```

## Anti-DARVO / anti-hand-wave rule

Do not argue with the institution. Ask the same machine-readable questions every time:

1. What exact claim was made?
2. Who made it?
3. Under what authority?
4. What document supports it?
5. What burden applies?
6. What contradicts it?
7. Was the record corrected, superseded, sealed, redacted, or consolidated?
8. Can the bytes be replayed from 127.0.0.1?

## Search-state labels

```text
DISCOVERED
OFFICIAL_PAGE_OBSERVED
DOCUMENT_LOCATED
BYTES_FROZEN
HASH_BOUND
CLAIM_BOUND
CONFLICT
CORRECTED
NOT_FOUND_YET
```

Never use `NOT_FOUND_YET` as `DOES_NOT_EXIST`.

## BoxD punchline

> "If Justice throws the dice, Goblin Court checks whether the dice, the table, the dealer, the rulebook, and the damn surveillance camera all agree."

**AUTHORITY = FALSE**  
**BASE = OPTIONAL COMMITMENT RAIL**  
**SEARCH != PROOF**
