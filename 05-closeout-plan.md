# Plan for closing the known round-1 issues and the new run

2026-11-13. Basis: the ground-truth check of the round-1 results (reports/gt_check/, 682 verdicts) and the owner's decisions (journal.md, entries of 2026-11-13).

Principle: whatever can be fixed through the data or the scorer is closed without models (rescoring from predictions.jsonl). Models are re-run only where the prompt itself caused the error: neither rescoring nor a ground-truth edit can fix it.

Roles, following the check: plan — Opus 5.5 high, code — Opus 5.5 medium, review and runs — Sonnet.

## Issue map

| # | Issue | Closed by | Stage | Model runs needed |
|---|---|---|---|---|
| 1 | 6 ground-truth errors (proposed_fixes.csv) | edit of final/ | 0 | no |
| 2 | Strict scorer: names, IDs, sign, dates | normalize.py rules | 0 | no |
| 3 | Policy: any seller name, any seller tax ID, both date orders, sign does not matter | `accepted` + scorer | 0 | no |
| 4 | Invoice amounts that are not printed; one amount in either field | `excluded` + scorer | 0 | no |
| 5 | Stock mock-ups wild__0426 and wild__0428 | exclude the documents | 1 | no |
| 6 | Masks where the value can be computed or a rounded amount is visible | exclude these probes | 1 | no |
| 7 | Two different values on a page (Kostenrechnung seller_name, BASIC Einfach due_date) | `accepted` | 1 | no |
| 8 | Poor quality (wild__0352, SROIE OLIVE9, synrec 608 photo, cropped PT series, O/0 in the IBAN of nl-narrow-014) | `quality: low` label, reported separately | 1 | no |
| 9 | Series prefixes in invoice numbers (FS, FT, NFS) | owner's decision → ground truth + scorer | 1 | no |
| 10 | zugferd Kraftfahrversicherung total_gross: 220 or 440; 2 «unsure» verdicts | second review + owner's decision | 1 | no |
| 11 | The synrec generator mixes up dd/mm and mm/dd | record the defect; the scorer accepts both orders | 1 | no |
| 12 | Pairs where 3 models or fewer were wrong were not checked | review of a sample | 2 | no |
| 13 | A ground-truth error the models agree with (voting cannot see it) | ground-truth arithmetic + random audit | 2 | no |
| 14 | Prompt P1 caused errors: total is not defined at all (P1 has only the schema key; fields.yaml does not reach the prompt) → models take the cash tendered, subtotal = copy of total, name with address, gross↔net swap | new prompt P1b | 3 | **yes** |
| 15 | Prompts P0/P2 for round 2 contain the same definitions | P0b/P2b | 4 | yes, in round 2 |
| 16 | gt_check: verdict `ok` is not in the list, no choice of input file | code fix | 0–1 | no |

## Stage 0 — done 2026-11-13 (Opus 5.5 agent, medium; acceptance passed: 61 tests, runs/ untouched, 0 right→wrong transitions)

Content: ground-truth edits, the `accepted` field, excluded amounts, scorer rules, prompt P1b, rescoring r1 into a separate folder, reports/rescore_r1/compare.md.

Acceptance (checked by me before stage 1):
- `uv run pytest -q` green; runs/ unchanged; every edit of final/ recorded in the journal and applied_fixes.csv.
- A sample of 50 rows that changed outcome, per rule: the rule does not accept a digit error in an amount or ID.
- No TP → WV/FN transitions; otherwise analyse each one.

## Stage 1 — close the data (no models) → final v4 — done 2026-11-13, final v4 frozen (sha256 4ff069c0…)

1.1. Exclude documents wild__0426, wild__0428 (stock mock-ups) — approved by the owner.
1.2. Mask probes: find by rule all amount masks whose components are printed (SUB_TOTAL and TAX, line items and discounts), and masks with a visible rounded amount; exclude these probes. Known: SROIE X51007579725, X51005719898, X51008099088, X51007846304; wild__0298__mask; FATURA and wild with total = SUB_TOTAL + TAX. Check the list against the pages (Sonnet).
1.3. `accepted` for pages with two values: Kostenrechnung seller_name (KOSTENLIEFERANT GMBH and MUSTERLIEFERANT GMBH), BASIC Einfach due_date (2017-12-13 and 2020-04-04).
1.4. `quality: low` label for the documents in row 8; reports compute accuracy with and without them.
1.5. Owner's decisions: series prefixes: accept with and without the prefix (decided); total_gross Kraftfahrversicherung = 220, a "no earlier debts" clause in P1b (decided). Two «unsure» — second review (Opus high) and a question to the owner.
1.6. Record the synrec generator defect (date order) in final/README.md.
1.7. gt_check: add `ok` to VERDICTS; an option for the input fields.csv; carry verdicts over by review_id between runs.
1.8. Rescore r1 → rescore_v2; freeze final v4: journal entry, sha256 of answers.json, commit.

1.9. New after stage 0:
- ☑ Name + address / extra text when the name is found — a correct value (owner's decision 2026-11-13). Format label: for names canonical=False if the match is only by containment (there is extra text); currently canonical is always True for text fields — to be refined.
- Ground truth seller_name «Physiotherapeutin» (both zugferd Physiotherapeut documents) → Tanja Tinder: in the Verkäufer block «Physiotherapeutin» is a profession, the name is printed on the line below (owner's rule: profession + name below → the profession does not count; if the word is the name itself, it counts).
- Borderline name_contain matches: «ROSS DAZZ FOR LESS», «Christopher Hayes Andrew Cliff», «GLN … MUSTER-KUNDE» — to be analysed.
- P1b: add «a service charge is not tax; local taxes (PB1) are tax»; FATURA: line-level «TAX $0.00».
- fatura Template49 buyer_name — second review.
- The stage-0 edits of final/ are not committed; commit when freezing v4 (item 1.8). A backup of the original answers is in the session scratchpad.

## Stage 2 — extend the ground-truth check (no models) — done 2026-11-13: 0 hidden errors out of 200 (≤1.9 %), final v5

2.1. Pairs with 3 errors out of 6 (293): the same review procedure (blind reading, controls), Sonnet.
2.2. Arithmetic of the ground truth itself: net + tax = gross, subtotal + tax = total (±0.01), due_date ≥ issue_date, total ≥ any line item. Discrepancies → review.
2.3. Random audit of pairs where all 6 models agree with the ground truth: 200 pairs, stratified by source. Gives an estimate of the share of hidden ground-truth errors with a confidence interval. If ≥ 2 errors are found, extend the audit for that source.
2.4. Fixes → final v5, rescore r1 → rescore_v3.

## Stage 3 — new run r1b with prompt P1b

Why it is needed: the errors in row 14 are caused by the wording of P1. Rescoring cannot fix them. Models make these errors differently (for example gemma4-12b fills empty fields less often), so the ranking and the choice of round-2 finalists may be distorted.

Preliminary check (cheap, before the run): on rescore_v3 compare the ranking of the 6 models on the full set and on the set without the affected clusters (synrec total and subtotal, EuroDocBench names, FATURA amounts). Record the result; it shows how much P1 moved the ranking.

Recommendation: a full r1b run = 6 models × all of final v5 × P1b, about 44 h (r1 actually took 43.7 h: from 4.8 h for gemma4-e4b to 11.1 h for gemma4-12b). Full rather than receipts only (~20 h), because P1b also changes the instructions for invoices (names, gross/net), and mixing prompts breaks comparability. r1 (P1) stays as it is and gives the P1 vs P1b comparison.

3.1. Smoke: P1b on the smoke set (33 documents) for qwen3vl-4b and gemma4-12b: valid JSON, format, no reasoning left-overs, no regressions against P1.
3.2. Queue protocol/round1b.json, the same runner (`caffeinate -i uv run python -m harness.study protocol/round1b.json`), model configuration as in r1 (Gemma image budget 1120).
3.3. gt_check on r1b: a clear drop of L1/L2 in the row-14 clusters is expected. Review only the new suspicious pairs (r1 verdicts carry over by review_id).
3.4. Report: P1 vs P1b by model and field; ranking; choice of finalists.

## Stage 4 — round 2 (as in 00-plan.md, with amendments)

- The base is r1b (P1b), not r1.
- Rewrite P0 and P2 with the same field definitions (P0b, P2b) before the runs, otherwise the prompt comparison repeats the row-14 errors.
- Everything else unchanged: constrained decoding, 6/8 bits, extractors NuExtract3 and lift.

## Order and time estimate

| Stage | What | Time |
|---|---|---|
| 0 | running | hours, agent |
| 1 | data → final v4 | ~half a day, agents + 3 owner decisions |
| 2 | review of 293 pairs + audit of 200 + arithmetic → final v5 | ~a day, agents |
| 3 | smoke P1b → r1b | ~1 h + ~44 h of machine time, then review of new pairs |
| 4 | round 2 | per 00-plan.md |

## Owner's decisions (open)

- ☑ Exclude wild__0426 and wild__0428 — yes (2026-11-13).
- ☑ Series prefixes in invoice numbers — accept with and without the prefix (2026-11-13).
- ☑ total_gross zugferd Kraftfahrversicherung — 220 (the total of this invoice, without the debt); the clause was added to P1b (2026-11-13).
- ☑ Full r1b run (~44 h): 6 models × the whole set × P1b — approved (2026-11-13). Start after stages 0–2 and the P1b smoke test.
- ☑ Round-2 finalists: qwen3.5-9b, gemma4-12b, qwen3vl-8b — approved (2026-11-15; protocol/preregistration.md, section 1).
- ☑ Round-2 rules (protocol/preregistration.md) — fixed before the runs (2026-11-15).
- ☑ gemma4-12b q8 excluded from round 2: OOM in smoke (amendment of 2026-11-16).
