# Papers Manifest — Systems Thinking Studio knowledge library

Built 2026-08-28. Sources: arXiv API (`export.arxiv.org/api/query`, 3s spacing between
calls) and Semantic Scholar Graph API (`api.semanticscholar.org/graph/v1/paper/search`,
no key, one 10s-backoff retry on 429 per policy, then proceed). Raw fetch JSON cached at
`/tmp/sts_papers/raw/` (fetch script `/tmp/sts_papers/fetch.py`). Selection rule:
combine both APIs per topic, dedupe by title, prefer S2 `citationCount > 50` where
reported, keep only papers whose abstract the API actually returned (notes are written
from abstracts only). 18 paper notes + 8 book canon summaries written.

## Per-query result counts

| Query | arXiv | S2 | Notes |
|---|---|---|---|
| system dynamics modeling | 15 | 20 | 3 notes selected |
| leverage points complex systems intervention | 15 | 0 (429) | 1 note selected (arXiv) |
| organizational learning feedback loops | 15 | 20 | 1 note selected (arXiv) |
| systems thinking decision making | 15 | 0 (429) | 1 note selected (arXiv) |
| complex adaptive systems engineering | 15 | 20 | 3 notes selected (2 arXiv, 1 S2 was picked then swapped — see skips) |
| agent based modeling policy analysis | 15 | 0 (429) | 4 notes selected (3 arXiv, 1 S2 cross-matched from stock-flow query) |
| stock and flow simulation | 15 | 20 | 3 notes selected (S2) |
| **Totals** | **105 fetched** | **80 fetched** | **18 notes** |

## API failures (all recorded, none silently dropped)

1. S2 `leverage points complex systems intervention` — HTTP 429, failed initial call,
   one 10s-backoff retry per policy, still 429. A follow-up retry minutes later: 429 again.
2. S2 `systems thinking decision making` — HTTP 429, same retry policy, still 429; second attempt: 429.
3. S2 `agent based modeling policy analysis` — HTTP 429, same; second attempt: 429.
4. S2 batch endpoint (`/paper/batch`) used to recover abstracts for 4 pre-selected
   papers — HTTP 429 immediately. Consequence: 3 selections swapped to abstract-bearing
   alternates (see skips).
5. arXiv — all 7 queries succeeded, 15 results each, no errors.

Category coverage is intact despite the 429s because arXiv answered every query, and
the S2 queries that did land (SD, org-learning, CASE, stock-and-flow) supplied the
peer-reviewed/applied entries.

## Skips (fetched but not written up)

- **Sterman 2002 "System Dynamics: Systems Thinking and Modeling for a Complex World"**
  (S2, 5,175 cites) — this is the *Business Dynamics* textbook indexed as a paper;
  covered as a book canon summary instead (`../books/sterman-business-dynamics-2000.md`).
- **S2 picks with no abstract returned by the API** (swapped, per abstracts-only rule):
  White 2009 "Complex Adaptive Systems Engineering (CASE)" (30 cites), White 2016
  ten-year update (15), Hall/Paradice/Courtney 2001 HICSS feedback loops (16),
  Simonetti 2014 US blood supply SFD (32). Replacements: Casadei 2024 (CASE-style
  self-organizing engineering, arXiv), Hubbard 2016 (org decision loops, arXiv),
  Pfaff 2018 copper cycle (36 cites, abstract present).
- **arXiv keyword noise** — `stock and flow simulation` and `system dynamics modeling`
  surfaced fluid-dynamics papers (pipe flow, jets, sediment transport) and pure-math
  papers (complex manifolds, dynamical spectra); `organizational learning feedback
  loops` surfaced ML-feedback papers (RLHF, contrastive learning). All skipped as
  off-topic for this library.
- Duplicates across queries (e.g. arXiv 0807.3374 and 2111.04380 appearing twice,
  1003.3767/2307.02422 cross-listed) — deduped by arXiv id/title.
- Mokander 2021 companion "Nature, Scope, and Limitations" (2110.10980) — skipped in
  favor of the intervention-points paper (2111.04380); Burgh/Melo 2024 "Censored
  Beliefs" — skipped in favor of the 2023 version.

## The 18 paper notes

System dynamics: naugle-2023, crielaard-2022, rebs-2019, goodarzi-2025 ·
Leverage points/intervention: moschoyiannis-2016, mokander-2021 ·
Organizational learning/management: hubbard-2016, siebers-2010 ·
Complexity/feedback in engineering systems: abbott-2006, smith-2008, casadei-2024 ·
Agent-based modeling: osoba-2020, montes-2023, shoukat-2020, anderson-2018 ·
Stock-and-flow: kumar-2018, pfaff-2018 ·
Decision making: burgh-2023

Citation counts are as reported by S2 at fetch time (arXiv-only papers have
`citation_count: null`). No papers were invented; every note's Claim/Method derives
from the API-returned abstract stored in the raw cache.

## Source-metadata quirks

- arXiv's own metadata for cs/0603127 (Abbott 2006) truncates the title to
  "...Complex Systems Engineeri"; the note uses the complete title
  "...Complex Systems Engineering". Verified via paper_id, not title string.
- S2's title for the Crielaard 2022 entry ends with a period; the note matches it
  verbatim for exact traceability.
