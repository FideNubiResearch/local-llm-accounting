# Research journal

Entry template:

```
## YYYY-MM-DD — short title
Goal:
Actions / commands:
Result:
Status: success / problem / postponed
Next step:
```

---

## 2026-11-10 — Start, plan v1

Goal: define a research plan for local LLMs on accounting documents on a 16 GB Mac mini M4.

Actions:
- Search for recent 2026 work: ExtractBench, UniKIE-Bench, ReceiptBench, Electricity invoices, Abstention as prompt artifact, lift/NuExtract3.
- Search for datasets: DocILE, CORD, SROIE, FATURA, ZUGFeRD corpus, VAREX.
- No public datasets of Serbian/Montenegrin invoices found.
- Studied the fidenubi.com calculator: memory and speed estimates for an M4 with 16 GB.

Result: `00-plan.md` v1. Nothing was installed on the system.

Status: waiting for the owner's decisions (plan section 10).

Next step: phase 0 — finish reading VAREX, RealDocBench, DocAttriBench, confirm the gap.

## 2026-11-10 — Plan v2 after the owner's answers

Owner's decisions:
- Documents: any accounting documents, open-source only. The owner's own documents are not provided.
- Languages: English, any European, Asian (CJK). Languages are the main axis; there will be separate publications on them.
- The Serbian/Montenegrin synthetic set — drop it.
- Installing tools — allowed.
- sudo — will be granted.
- Publication: measurements only, on fidenubi.com and for backlinks.

Actions: search for multilingual datasets (GitHub/HF): XFUND, SCID, KORIE, CORD, CORU, InvoicesReceiptsPT, synthetic-receipts-ocr, Japanese Mobile Receipt; e-invoices ZUGFeRD/XRechnung/FatturaPA/KSeF/Peppol; statements, financial reports (Kleister, FinTabNet).

Result: `00-plan.md` v2.

Status: waiting for an answer on the cloud reference and approval to start phases 0–1.

## 2026-11-10 — Plan v2.1

Owner's decisions:
- no cloud reference needed, local models only;
- NC datasets are acceptable: we publish measurements only;
- runs are continuous, not tied to the night;
- missing fields — primarily through questions about what is not in the document.

Checked by search: no ready document datasets with masked fields exist (only UNK-VQA on ordinary photos, QASPER/SQuAD2 on text). Masking stays an additional test and our contribution.

Result: `00-plan.md` v2.1. Timeline ≈7–10 days: 2–3 days of preparation, then runs 24/7.

Status: waiting for the start of phases 0–1.

## 2026-11-10 — Plan v2.2: one start

Owner's decision: first prepare everything completely, then one continuous start, with finished results at the end.

Adopted:
- experiment queue in `study.yaml`;
- pre-registration of the finalist selection rules;
- models are downloaded and deleted one at a time;
- automatic stop on obvious errors, resume after a failure;
- run status in `runs/STATUS.md`;
- a framework reusable for later studies.

Status: waiting for the start of preparation (phases 0–2).

## 2026-11-10 — v2.3: review answers, row-cell hygiene
- Review app: every question now has its own answer set that literally answers it (value: matches / other value / not in the document / cannot tell; absence: absent / present + value / cannot tell; mask: masked / visible / cannot tell). Keys 1–4. Possible print formats of amounts/dates shown. Verdict codes: ok, other, absent, present, mask_bad, unsure (documented in tools/review_app.py).
- Found via review (invbench__INV-2026-0145): invoice_benchmark GT holds net values that are not printed (document prints gross unit prices and "subtotal incl. VAT"). Scalars were already excluded as not_visible; line items were not checked at all.
- New: cell-level hygiene for line_items/transactions (doc.json `row_skip` = [[row, key], ...]); invisible cells are not scored; a row field with >50% invisible cells is excluded (`rows_not_visible`). score_rows(skip=...) / score_doc(row_skip=...).
- Visibility fixes: amounts with trailing zeros after the decimal separator ("9,9000" = 9.90); number boundaries for literal matches ("100" is not visible in "1000"); word coverage ≥85% for text wrapped across table lines.
- Result: 101 GT cells excluded (zugferd 32, invoice_benchmark 47, katanaml 8, bank_statement_intel 14); 3 row fields dropped. Tests: 18 passed.

## 2026-11-10 — v2.4: GT audit by Claude (see 04-gt-audit.md)
- All 88 masked variants checked on crop sheets (tools/audit_masks.py) + OCR of masked page: 32 invalid (value printed twice / handwritten / in words / option label). New mask kinds: label_kept, field_removed (FATURA), still_printed (auto), invalid (review).
- Absence claims: FATURA adapter fixed (BILL_TO, AMOUNT_DUE; SHIP_TO/GST/site-only/total-in-words -> excluded); absence detector prefix matching (German compounds) + tax words in more languages; PT and WildReceipt errors fixed by verdicts.
- Present values: automatic visibility over all values; WildReceipt added to visibility check; visibility uses page text only (OCR + PDF layer), never dataset-provided text; XFUND checkbox pairs dropped, dot leaders ignored.
- harness/review.py applies verdicts after every build (human > claude). Review app: blind audit queue "0. Claude check", mask question reworded; tools/agreement.py.
- Corpus: 710 docs; 3754 present, 387 absent, 1048 foreign probes, 58 clean masks, 329 excluded. Tests: 20 passed.

## 2026-11-10 — v2.5: full-page review (user: crops are not enough)
- tools/page_sheets.py: whole pages at ~0.6 MP (9-pt A4 text still readable), several docs per sheet, masked area outlined.
- All 87 masked docs and all docs with absence claims (fatura, cord, wildreceipt, pt, zugferd, synthetic clean + photo twin) reviewed page by page; verdicts in data/review/verdicts.jsonl (method "full page...").
- New findings: values readable inside e-mails/signatures/second form copy; ROSS date/time printed; Acme ZUGFeRD XML is a different invoice; 7 German invoices with Käufer-/Buchungsreferenz -> PO excluded; ambiguous tax lines excluded.
- Fixes: bare-integer amount variants need >=4 digits; claude "ok" on a mask clears an automatic still_printed flag.
- Result: 375 absence probes and 59 clean masks, all full-page verified; 3754 present values; 342 excluded.

## 2026-11-11 — v3: frozen final set, new sources, cleanup
- final/ is the dataset: one answers.json per document with canonical answers; forms (XFUND) and table fields out; only confirmed nulls; masks kept where both reviews agree (commit 9a26097).
- Added EuroDocBench invoices (8 languages on the same 5 layouts, fr 65 after dropping docs with a missing separator glyph) and 60 more synthetic receipts each de/fr/it (commit eacdd8d). Total 1574 documents.
- Sufficiency rules and their consequences recorded in 00-plan.md section 3 (language comparison on EuroDocBench, real-doc claims only en/de/pt/id/ko, statements out of round 1).
- Cleanup: review/build tools, intermediate corpus, staging and raw downloads removed (reports/cleanup_plan.md). Remaining code: runner, score, normalize, fetch.

## 2026-11-11 — final/: 3 CORD answers fixed
- cord__067 total 950000 -> 9500 (printed 9.500,00); cord__041 subtotal 31601700 -> 316017, total 36500000 -> 365000
  (printed 316017.00 / 365000.00). Cause: build_final's "IDR has no decimals" rule concatenated all digits, including
  the printed ",00"/".00". Found by checking that every `printed` matches its `answer` with the scorer (0 other mismatches).

## 2026-11-11 — pipeline, dashboard, round 1 queued (WHERE WE STOPPED)
Done:
- Pipeline over final/: `harness/run.py` (model x prompt, resumable), `harness/report.py` (scores vs answers.json),
  `harness/dashboard.py` -> runs/dashboard.html (local page: queue, dataset, runs, per-language and per-field scores;
  aggregates only). Open: `uv run python -m harness.dashboard && open runs/dashboard.html`.
- Smoke run (33 docs, one per source x lang x type), Qwen3-VL-4B, old P1: 11 s/doc, peak 4.8 GB, value accuracy 94%,
  JSON valid 100%, format ok 71%; invented values only on receipts (subtotal filled with total 10/10; missing total 3/3).
- P1 fixed (owner approved): "copy exactly" only for names/ids; dates, times, currency, amounts in the requested form.
  Re-check on the same 33 docs: runs/smoke_qwen3vl4b_P1v2.
- Model catalog by helper: reports/models_catalog.md. Round 1 decided (owner approved, no pilot): 6 VLMs x all
  1574 docs x P1, est. ~48 h: Qwen3-VL 4B/8B, Qwen3.5 4B/9B, Gemma 4 E4B/12B. Second round (finalists only):
  P0/P2, constrained decoding, 6/8 bit, extractors NuExtract3 and lift. Not used: GLM-4.1V Thinking (thinking cannot
  be turned off), MiniCPM-V 4.5 and InternVL3.5 (no MLX weights).
- Queue: protocol/round1.json, runner `caffeinate -i uv run python -m harness.study protocol/round1.json`
  (strict order; finished runs skipped; entries with "hold" wait, file re-read every minute).
Next:
1. Compare smoke P1v2 vs P1 (format ok should rise), then start the queue.
2. Helper task pending (asleep until 14:00): reports/models_setup.md - download the 5 models, how to set the image
   budget in mlx-vlm 0.7.10 (Gemma: 1120 visual tokens, default 280 is too low for A4), whether
   enable_thinking=False reaches the chat template (Qwen3.5, Gemma), rendered prompts.
3. After that: add Gemma's image-budget parameter to run.py/runner.py if needed, record it in round1.json,
   remove "hold" from Qwen3.5 / Gemma entries. Rule: every model gets its documented OCR image budget.

## 2026-11-11 — five models ready, «hold» removed

- The helper downloaded five models and checked the SHA256 of all 8 safetensors against the HF API: reports/models_setup.md.
- «Thinking» is turned off by the template for all five. Qwen3-VL Instruct has no switch. Qwen3.5 gets a closed empty `<think></think>`. Gemma gets no `<|think|>`; the 12B has an empty thought channel. Checked from the template, not by inference: the first answers of Qwen3.5 and Gemma need checking for left-over reasoning.
- Gemma image budget: mlx-vlm 0.7.10 drops `max_soft_tokens` in stream_generate, so `Runner` sets `processor.image_processor.max_soft_tokens` after load(). Checked with the processor without weights on an A4 page of 1241×1754: 278 → 1104 tokens for E4B, 282 → 1108 for 12B.
- Qwen works with the checkpoint's default max_pixels (65 536–16 777 216). The sources give no separate value for OCR.
- A run's config.json now has `image_processor`: the values read from the processor after setup.
- «hold» removed in round1.json, `max_soft_tokens: 1120` added for Gemma. The queue was restarted at 780/1574 of Qwen3-VL-4B: the old process held the previous code and would have failed on the new parameter.

## 2026-11-13 — checking the input data from the round-1 results (gt_check)

Goal: use the models' errors to find errors in the answers (answers.json), documents, field definitions and prompt P1.
Level 1 — all 6 models wrong on a (doc, field) pair; level 2 — more than 50 % of the models (4–5 of 6).
Error = WV / FN / FF; TP / TN — right; canonical=False is not counted as an error.

- Plan (Opus 5.5, high): reports/gt_check/PLAN.md. Round 1 complete: 6 runs × 14561 (doc, field) pairs, keys match.
- Code (Opus 5.5, medium): harness/gt_check.py, tests/test_gt_check.py (24 tests, the whole suite of 47 green).
  Run: `uv run python -m harness.gt_check`, output in reports/gt_check/ (votes, suspects, by_*, docs, clusters, report.md, review/queue.csv).
- Run (Sonnet): all integrity checks passed. L1 = 245 (88 with a value, 157 with null), L2 = 638.
  Histogram of the number of wrong models: {0:11252, 1:1552, 2:581, 3:293, 4:179, 5:459, 6:245}.
  Hints over L1+L2: sibling_copy 539, scorer_strict 124, gt_value_suspect 83, gt_null_suspect 15, value_not_found 15, mask_leak 10, scattered 97.
- Hypotheses (not verdicts yet): synrec subtotal — models copy total (2411 of 2720 FF); PT seller_name — brand vs legal entity;
  PT VAT — the «PT» prefix is not removed by normalisation; EuroDocBench names — models add the address; SROIE total=null and FATURA totals — probably ground-truth errors;
  cord__020 total (GT 377859, models 377059), cord__031 tax_amount.
- Review: a queue of 682 items (the plan estimated ~300). Blind reading of the page → verdict → review/verdicts.jsonl. final/ is not changed;
  fixes go to review/proposed_fixes.csv for the owner's approval.
  The Sonnet agent failed on an API error (403) after 50 verdicts (2 batches): scorer_too_strict 18, definition_ambiguity 18,
  model_failure 8, gt_wrong 4, doc_unreadable 1, unsure 1. Continue from item 51; review progress in review/PROGRESS.md.

### 2026-11-13 — gt_check review: 200 of 682 (batches 1–8)
- Priorities 1–2 done in full and the start of 3; stopped at cord__020::tax_amount, next is batch 9. Checker re-run: exit 0.
- Verdicts (200): definition_ambiguity 79, scorer_too_strict 60, model_failure 46, gt_wrong 5, ok 4 (controls), unsure 2, doc_unreadable 2, doc_mismatch 2.
  Hidden controls: 7 of 25 fell into the reviewed part, all 7 right. The verdict «ok» is not in VERDICTS (harness/gt_check.py:52) — not counted in the cluster table.
- Ground-truth errors (review/proposed_fixes.csv, final/ unchanged): zugferd Rechnungskorrektur buyer_name and seller_name (the GLN/Kunden-Nr. block got into the answer);
  Konik acme invoice-42 total_tax 19 (the rate) → 269.80; zugferd v1 Haftpflicht buyer_name «Herrn\nMax Mustermann» → Max Mustermann;
  pt__20210508_202709 seller_name (low confidence).
- Prompt/definitions: receipt total = «total amount paid» (fields.yaml:29) → models give «BAR»/cash tendered; subtotal without a subtotal line;
  sign of refund amounts; brand vs legal entity in seller_name (PT inconsistent); name without address (EuroDocBench);
  dd/mm vs mm/dd in synrec (the generator is inconsistent); PB1 is tax, a service charge is not (CORD); tax 0 vs null; series prefixes in invoice numbers.
- Scorer too strict (proposals for normalize.py): N.text — diacritics, legal forms, salutations Herr/Frau, spaces, name containment;
  N.ident_value — country prefix, «No.», a «/CRC…» tail; Korean «(주)/㈜».
- Waiting for the owner's decisions: seller_name policy, subtotal/tax when no line is printed, ambiguous dates, sign of negative amounts, whether to continue the review (batches 9–28).

### 2026-11-13 — owner's decisions after the review (200/682)
1. seller_name / merchant_name: both count — the brand and the legal entity.
2. subtotal / tax_amount when the line is not printed: the answer is null (GT stays null; models that fill the field are wrong; clarify the prompt).
3. Ambiguous dates (day and month ≤ 12): both orders count.
4. The sign of an amount is ignored (refunds, credit notes, amounts in brackets).
5. The review continues: batches 9–28.
Changes to the scorer / GT / prompt from these decisions come after the review ends, as a separate step; final/ is not touched yet.

### 2026-11-13 — gt_check review finished: 682/682
- Batches 9–28 (482): model_failure 252, ok 172, scorer_too_strict 29, definition_ambiguity 28, gt_null_wrong 1.
  Total 682: model_failure 298, ok 176, definition_ambiguity 107, scorer_too_strict 89, gt_wrong 5, gt_null_wrong 1,
  doc_unreadable 2, doc_mismatch 2, unsure 2. Controls: 25/25 right. Checker re-run: exit 0.
- Conclusion: of the 883 suspicious pairs (L1+L2) there are few ground-truth errors — 6 (review/proposed_fixes.csv); the bulk is
  model errors and ambiguous definitions/a strict scorer. The input data is confirmed overall.
- New ground-truth error: cord__009 total null → 36000 (only «Sub Total 36000» is printed, with cash and change; medium confidence).
- Document problems: wild__0426, wild__0428 — stock mock-ups, arithmetic does not add up; wild__0352 — 258 px wide;
  masks where the value can be derived arithmetically (sroie X51007579725, X51005719898, X51008099088; fatura/wild total = SUB_TOTAL+TAX);
  sroie X51007846304 and wild__0298__mask — a rounded amount is visible.
- New questions about definitions: FATURA with only SUB_TOTAL or only TOTAL (null, or copy into total_gross/total_net);
  seller_vat_id — Steuernummer/NIPC or VAT id only; seller_name when only the dealer/station is printed (galp, «GAR. RIBAMAR»).
- Scorer: the brand from [P-seller] does not pass (다이소, CU, McDonald's, ROSS DRESS FOR LESS) — GT holds one value, a list of
  acceptable variants is needed; quirks of GT strings ('JAWEDHABIB', "Mcdonald'sHazeldonk-west", ' .. ', 'FS A / 42799').

### 2026-11-13 — owner's decisions (2): amounts, seller tax number, seller name
1. Invoice amounts (total_gross / total_net / total_tax): a missing amount = null, copying is not allowed. If the document prints
   only one amount, its correct extraction counts in whichever field (total_gross or total_net) the model writes it.
   Missing amounts are excluded from scoring (not FF).
   Difference from decision (1) item 2: for receipt subtotal/tax_amount null stays scored, filling it is a model error.
2. seller_vat_id: any tax identifier of the seller counts (VAT id, Steuernummer, NIPC/NIF etc.).
3. seller_name / merchant_name: any recognisable seller name — brand, legal entity, dealer, station; all correct variants are accepted.

### 2026-11-13 — plan for closing the issues: 05-closeout-plan.md
Stages: 0 — ground-truth edits and scorer (running); 1 — data → final v4 (stock mock-ups, invalid masks, two values on a page,
quality labels, series prefixes); 2 — extended ground-truth check (pairs 3/6, GT arithmetic, audit of 200 agreeing pairs) → final v5;
3 — a new r1b run: 6 models × the whole set × P1b (~44 h), because errors caused by the wording of P1 cannot be fixed by rescoring;
4 — round 2 on the r1b base, P0/P2 rewritten with the same definitions.

### 2026-11-13 — owner's decisions (3)
- wild__0426, wild__0428 (stock mock-ups) are excluded.
- Invoice number: counts both with the series prefix (FS, FT, NFS, …) and without it.
- Invoice amounts are the total of this invoice only, without debts from earlier invoices, overpayments or offsets. zugferd Kraftfahrversicherung:
  total_gross = 220 (not 440 «zu zahlender Beitrag» = premium + debt). GT is not changed; the clause goes into prompt P1b (also for the receipt total).
- The decisions on series prefixes and P1b were passed to the stage-0 agent.
- A full r1b run (6 models × the whole set × P1b, ~44 h) is approved. Start after stages 0–2 (final v5) and a P1b smoke test.
  All owner decisions in 05-closeout-plan.md are closed.

### 2026-11-13 — edits of final/ after the ground-truth review, new scorer rules, P1b, rescoring round 1

The owner allowed editing the frozen final/. Decisions: journal 2026-11-13 (1), (2) and two new ones (3):
(3a) total_gross / total_net / total_tax are amounts of this invoice only, without debts from earlier invoices, credits and overpayments
(Kraftfahrversicherung: GT 220 stays, 440 is not added); the same for the receipt total; (3b) invoice_number counts
with and without the series prefix (FS, FT, FTR, NFS, FR, C2 / …), the digits must match exactly.
Script: `tools/apply_gt_review.py` (idempotent); machine-readable list: reports/gt_check/applied_fixes.csv (117 rows).

**A1. Ground-truth fixes** (all 5 checked against the page; none missed):
- cord__009 total: null → '36000'. receipt has no Total line; 'Sub Total 36000', Discount (0 %), Tunai 50000, Kembalian 14000: the amount due 36000 is printed (as Sub Total) and equals cash - change; verdict gt_null_wrong (med)
- zugferd…v1_correct_Konik_acme_invoice-42_ZUGFeRD.pdf total_tax: '19' → '269.80'. page: 'Umsatzsteuer 19% 269,80' under 'Summe netto 1.420,00'; GT held the VAT rate; verdict gt_wrong (high)
- zugferd…v2_correct_intarsys_BASIC_zugferd_2p0_BASIC_Rechnungskorrektur.pdf buyer_name: 'GLN 4304171000002 \nKunden-Nr. : 009420\nMUSTER-KUNDE GMBH' → 'MUSTER-KUNDE GMBH'. page 1 Käufer block: GLN and Kunden-Nr. lines are not the name; verdict gt_wrong (high)
- zugferd…v2_correct_intarsys_BASIC_zugferd_2p0_BASIC_Rechnungskorrektur.pdf seller_name: 'GLN 4333741000005 \nLief-Nr: 549910\nMUSTERLIEFERANT GMBH' → 'MUSTERLIEFERANT GMBH'. page 1 Verkäufer block: GLN and Lief-Nr lines are not the name; verdict gt_wrong (high)
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Haftpflichtversicherung_Versicherungssteuer.pdf buyer_name: 'Herrn\nMax Mustermann' → 'Max Mustermann'. salutation 'Herrn' is not part of the name; verdict gt_wrong (med)

**A2. Acceptable variants `accepted`** (33: seller_name 25, merchant_name 7, seller_vat_id 1; the old answer is kept; source — the review verdict; variants the new scorer already accepts were not recorded, except pt__20210508_202709 on explicit instruction):
- pt__20210508_202709 seller_name: 'ferragens do combro lda' + 'MTD-FERRAGENS DO COMBRO LDA'. owner rule [seller name]; source: proposed_fixes (low): correct_value; page header reads MTD-FERRAGENS DO COMBRO LDA, first letters partly occluded; old answer kept; verdict gt_wrong
- pt__20210215_172426 seller_name: 'flying tiger' + 'TIGER PORTUGAL, SA'. owner rule [seller name]; source: correct_value / blind_read (legal entity); verdict definition_ambiguity
- pt__20210323_174622 seller_name: 'jumbo' + 'AUCHAN RETAIL PORTUGAL, S.A.'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210508_181909 seller_name: 'botaminuto' + 'Consertos Rapidos Amoreiras, Lda'. owner rule [seller name]; source: correct_value / blind_read (legal); verdict definition_ambiguity
- pt__20210508_202449 seller_name: 'botaminuto' + 'Consertos Rapidos Amoreiras, Lda'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210429_191705 seller_name: 'galp' + 'GASNUNOS - DISTR. COM. GAS LDA'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210429_191705 seller_name: 'galp' + 'GASNUNOS, DISTR. E COM. GAS, LDA'. owner rule [seller name]; source: blind_read (legal entity); verdict definition_ambiguity
- pt__20210429_191705 seller_name: 'galp' + 'GASNUNOS'. owner rule [seller name]; source: prediction confirmed by note '6/6 legal'; verdict definition_ambiguity
- pt__20210507_174441 seller_name: 'galp' + 'SEQUEIRA PINTO - COM. COMB. LDA'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210428_195823 seller_name: 'galp' + 'GAR. RIBAMAR (Campo de Ourique)'. owner rule [seller name]; source: blind_read (station/dealer header); verdict definition_ambiguity
- pt__20210428_195823 seller_name: 'galp' + 'GAR.RIBAMAR-F.CUNHA COSTA'. owner rule [seller name]; source: prediction confirmed by evidence '4 models returned the station/dealer name'; verdict definition_ambiguity
- pt__20210428_201521 seller_name: 'galp' + 'GAR. RIBAMAR (Campo de Ourique)'. owner rule [seller name]; source: blind_read (station header); verdict definition_ambiguity
- pt__20210322_164701 seller_name: 'galp' + 'GALPGESTE, S.A.'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210322_164701 seller_name: 'galp' + 'A.S. LAGOS (FARO/SAGRES)'. owner rule [seller name]; source: blind_read (station); verdict scorer_too_strict
- pt__20210316_215850 seller_name: 'daily mercearia' + 'AZAFAMA CAMPESTRE - Prod. Alim. Unip. Lda'. owner rule [seller name]; source: correct_value (legal); verdict definition_ambiguity
- pt__20210428_232807 seller_name: 'chaviarte' + 'Destreza Aprumada, Lda'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210508_211412 seller_name: 'aki' + 'Dicodis - Distribuição de Bricolage, SA'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210509_002234 seller_name: 'auchan coimbra' + 'AUCHAN RETAIL PORTUGAL, S.A.'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210323_162221 seller_name: 'intermarche' + 'SODIAL PORCHINHOS-SUPERMERCADOS, LDA'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210215_172904 seller_name: 'maria da glória cab.' + 'Maria da Glória Cabeleireiros Lda.'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210320_172744 seller_name: 'requintefinal, lda.' + 'Casa Velha'. owner rule [seller name]; source: blind_read ('Casa Velha is the restaurant brand'); verdict scorer_too_strict
- pt__20210508_204341 seller_name: 'Estação Serviço da Cegonha Lda' + 'ESTAÇÃO SERVIÇO CEGONHA LDA'. owner rule [seller name]; source: blind_read (header form); verdict scorer_too_strict
- sroie__X51006414728 merchant_name: 'FOODELICO SDN. BHD.' + 'KEK SPAN OREE'. owner rule [seller name]; source: correct_value (brand logo); verdict definition_ambiguity
- korie__IMG00339 merchant_name: '(주) 아성다이소 .. 청주산남2호점' + '다이소'. owner rule [seller name]; source: evidence '3 brand-only 다이소', note '[P-seller] brand ok'; verdict scorer_too_strict
- korie__IMG00343 merchant_name: 'CU 청주수곡사랑점' + 'CU'. owner rule [seller name]; source: evidence "2 brand-only 'CU' (ok per [P-seller])"; verdict model_failure
- korie__IMG00013 merchant_name: '이마트 청주점' + '이마트'. owner rule [seller name]; source: note 'brand-only 이마트 would be accepted per [P-seller]'; verdict model_failure
- wild__0332 merchant_name: 'PaneraBread Cafe0994' + 'Panera Bread'. owner rule [seller name]; source: correct_value; verdict scorer_too_strict
- wild__0332__mask merchant_name: 'PaneraBread Cafe0994' + 'Panera Bread'. owner rule [seller name]; source: correct_value; verdict scorer_too_strict
- wild__0377 merchant_name: "Mcdonald'sHazeldonk-west" + "McDonald's". owner rule [seller name]; source: evidence/note: brand-only McDonald's valid per [P-seller]; verdict scorer_too_strict
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_EXTENDED_Kostenrechnung.pdf seller_name: 'MUSTERLIEFERANT GMBH' + 'KOSTENLIEFERANT GMBH'. owner rule [seller name]; source: blind_read: name in the page's Lieferant (supplier) block; verdict doc_mismatch; verdict doc_mismatch
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Haftpflichtversicherung_Versicherungssteuer.pdf seller_name: 'MVM Musterhafter\nVersicherungsverein Musterstadt a.G.' + 'Versicherungsverein Musterstadt a.G.'. owner rule [seller name]; source: blind_read: legal-entity line of the letterhead; verdict scorer_too_strict
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Kraftfahrversicherung_Bruttopreise.pdf seller_name: 'MVM Musterhafter\nVersicherungsverein Musterstadt a.G.' + 'Versicherungsverein Musterstadt a.G.'. owner rule [seller name]; source: blind_read: legal-entity line of the letterhead; verdict scorer_too_strict
- zugferd…v2_correct_symtrax_Beispiele_BASIC_zugferd_2p1_BASIC_Einfach.pdf seller_vat_id: 'DE123456789' + '201/113/40209'. owner rule [seller tax id]; source: blind_read: 'Steuernummer 201/113/40209 and USt.-Id.-Nr. DE123456789'; verdict definition_ambiguity

**A3. Invoice amounts.** Answer null and the field not masked → the field was removed from answers.json, with a row in final/excluded.csv (the existing exclusion mechanism), null → (not scored). 60 fields:
- total_gross (10): fatura__Template26_Instance10, fatura__Template15_Instance100, fatura__Template15_Instance100__mask, fatura__Template19_Instance100, fatura__Template24_Instance0, fatura__Template24_Instance100, fatura__Template24_Instance100__mask, fatura__Template42_Instance1, fatura__Template39_Instance1, fatura__Template39_Instance1__mask
- total_net (15): fatura__Template3_Instance0, fatura__Template34_Instance100, fatura__Template34_Instance100__mask, fatura__Template10_Instance1, fatura__Template10_Instance1__mask, fatura__Template13_Instance1, fatura__Template13_Instance100, fatura__Template26_Instance10, fatura__Template19_Instance100, fatura__Template47_Instance100, fatura__Template47_Instance100__mask, fatura__Template23_Instance10, fatura__Template42_Instance1, fatura__Template22_Instance1, fatura__Template22_Instance1__mask
- total_tax (35): fatura__Template34_Instance100, fatura__Template34_Instance100__mask, fatura__Template10_Instance1, fatura__Template10_Instance1__mask, fatura__Template8_Instance10, fatura__Template8_Instance0, fatura__Template30_Instance10, fatura__Template13_Instance1, fatura__Template13_Instance100, fatura__Template26_Instance10, fatura__Template36_Instance0, fatura__Template15_Instance100, fatura__Template15_Instance100__mask, fatura__Template32_Instance10, fatura__Template32_Instance10__mask, fatura__Template19_Instance100, fatura__Template47_Instance100, fatura__Template47_Instance100__mask, fatura__Template24_Instance0, fatura__Template30_Instance100, fatura__Template30_Instance100__mask, fatura__Template24_Instance100, fatura__Template24_Instance100__mask, fatura__Template23_Instance10, fatura__Template40_Instance1, fatura__Template42_Instance1, fatura__Template49_Instance0, fatura__Template49_Instance0__mask, fatura__Template16_Instance10, fatura__Template30_Instance1, fatura__Template20_Instance100, pt__20210428_144738, pt__20210318_123736, pt__20210318_202746, pt__20210507_203027
`accept_from` (only one of total_gross / total_net is printed; the amount counts in either of the two fields), 19 fields:
- total_gross ← total_net (12): fatura__Template3_Instance0 (1377.77), fatura__Template34_Instance100 (875.45), fatura__Template34_Instance100__mask (875.45), fatura__Template10_Instance1 (796.34), fatura__Template10_Instance1__mask (796.34), fatura__Template13_Instance1 (1149.57), fatura__Template13_Instance100 (213.65), fatura__Template47_Instance100 (303.16), fatura__Template47_Instance100__mask (303.16), fatura__Template23_Instance10 (571.45), fatura__Template22_Instance1 (504.25), fatura__Template22_Instance1__mask (504.25)
- total_net ← total_gross (7): fatura__Template15_Instance100 (241.92), fatura__Template15_Instance100__mask (241.92), fatura__Template24_Instance0 (655.98), fatura__Template24_Instance100 (797.2), fatura__Template24_Instance100__mask (797.2), fatura__Template39_Instance1 (698.43), fatura__Template39_Instance1__mask (698.43)
Masked amounts (3 masked total_gross) stay in scoring as an absence check (null is right). Receipt subtotal / tax_amount were not changed.
final/manifest.csv: n_values / n_null recomputed for 41 documents; final/README.md: the accepted / accept_from scheme, totals (13275 values, 1226 nulls).

**B. Scorer** (harness/normalize.py, harness/score.py; every rule has a test in tests/test_score.py; rules can be switched off one by one via `equal(..., rules=)`, N.LEGACY = the round-1 scorer): date_swap, amount_abs, name_fold, name_legal, name_honorific, name_contain (names only), id_label, id_crc, id_cc (tax numbers only), id_series (invoice_number only, the prefix may be missing on one side only). score: `accepted`, `accept_from`, a `matched_by` column in fields.csv.

**C. Prompt.** P1_null.txt and schemas.json were not changed (hashes frozen in tests/test_prompts.py); field texts from fields.yaml do not reach the prompt (run.py takes only doc_type_human from it). New protocol/prompts/P1b_null.txt (`--prompt P1b`) for round 2.

**D. Rescoring round 1** without running models; runs/ untouched: `harness.report runs/<run> --out reports/rescore_r1/<run>`, `harness.gt_check --fields-root reports/rescore_r1 --out reports/gt_check_rescored` (exit 0, all checks green), `harness.rescore_compare` → reports/rescore_r1/compare.md. L1 245 → 195, L2 638 → 516. gt_check still loads the old runs/*/fields.csv (edits from applied_fixes.csv are allowed), but the check «the scorer reproduces the outcomes» now fails on them as expected: they were scored by the old scorer.

### 2026-11-13 — stage 0 accepted
- Check: 61 tests green; runs/ unchanged; on rescoring no right row became wrong.
  Rescoring r1 (reports/rescore_r1/compare.md): value accuracy +0.7…+2.3 points for all models; L1/L2 245/638 → 195/516.
- Correction to an earlier entry: «total amount paid» from fields.yaml did NOT reach the round-1 prompt (run.py takes from fields.yaml
  only doc_type_human). In P1 the total field is not defined at all — only the schema key. Same conclusion: P1b with definitions is needed.
- Open: whether to accept «name + address» (name_contain, 659 rows); GT «Physiotherapeutin» — probably an error; see 05-closeout-plan.md item 1.9.

### 2026-11-13 — owner's decisions (4)
- Name found but with extra text (address, legal form, a second line) — the value is right. The format violation is marked separately (canonical).
- Profession vs name: if a profession is printed above the name and the name on the line below, the name is right; if the word serves as the seller's name, it counts.
  zugferd Physiotherapeut (2 documents): seller_name «Physiotherapeutin» → Tanja Tinder.
- Stage 1 started (Opus 5.5 agent, medium).

### 2026-11-13 — stage 1 done: final v4 (Opus 5.5 agent, medium)
All edits by `tools/apply_gt_review.py` (idempotent: a second run changes no file, checked by the hash of final/ and applied_fixes.csv); stage-1 rows are `stage=1` in reports/gt_check/applied_fixes.csv (33 rows; the 117 stage-0 rows unchanged). runs/ untouched (hash before/after matches). No commit — waiting for acceptance.
- 1.1. wild__0426, wild__0428 excluded entirely: rows `*` in final/excluded.csv, removed from manifest.csv and docs/ (they stay in git).
- 1.2. 19 mask probes excluded (the field removed from answers.json of the `__mask` document, a row in excluded.csv with evidence). Candidates: `tools/mask_probe_scan.py` (Apple Vision OCR, rules leak / rounded / a±b(±c) / sum of line items) → reports/gt_check/stage1/mask_probe_candidates.csv; each checked against the page. sroie total ×9 (X51007579725, X51005719898, X51008099088, X51007846304, X51005757220, X51006556809, X51006557115, X51006556808, X51009008091), cord total ×4 (014, 070, 020, 072), cord tax_amount ×2 (058, 084), wild__0298 total («Rounding 12.00» and «Adjust 0.02» visible), wild__0082 total (77.46 + 6.65), wild__0121 subtotal (4.24 − .24), wild__0168 tax_amount (3.05 − 2.50 − 0.20). Three FATURA total_gross masks kept (Template28_0, 31_0, 43_1): SUB_TOTAL and TAX are printed, but the generator's TOTAL is not their sum — the value cannot be derived.
- 1.3. BASIC-WL Einfach due_date: accepted 2020-04-04 (page: «netto bis 04.04.2020» and «Fälligkeit 13.12.2017»). Kostenrechnung v1 seller_name: both names already accepted since stage 0, page checked.
- 1.4. `quality: "low"` (answers.json + manifest column `quality`) on 6 documents: wild__0352, sroie__X51006328937, synrec__eval-000608__photo, pt__20210428_141746, pt__20210507_215634, eurodocbench__test-nl-NL-narrow-014. report.py: table «All without quality=low documents»; rescore_compare: accuracy without them.
- 1.5. claude-opus verdicts (13) in review/verdicts.jsonl, summary in review/PROGRESS.md. pt__20210428_140713 seller_name: the page says ELENCOJASMIN → accepted (GT jasmim kept); pt__20210507_215634 invoice_number: GT FS T1/8072 is right (ok); fatura Template49_Instance0 (+mask) buyer_name: two «Bill to» blocks → accepted Joseph Wagner; borderline name_contain — the GT name is present in all of them → TP with canonical=False, not a single «name not found» case.
- 1.6. final/README.md: the synrec generator defect (dd/mm and mm/dd), the date_swap rule; set totals; section «Stage-1 edits».
- 1.7. gt_check: `ok` in VERDICTS; `--carry-verdicts` (default reports/gt_check/review/verdicts.jsonl) carries verdicts over by review_id (suspects.csv `verdict`/`verdict_source`, queue.csv `prior_verdict`, a counter in report.md); rescoring with excluded documents (document count from the manifest; exclude_doc allowed when reading old runs/). 4 new tests.
- 1.9a. For names canonical=False if the match is only by containment (extra text); the TP outcome does not change (normalize.name_clean, score.outcome; 3 tests). On r1: 631 TP rows changed canonical True→False; the «format ok» share for names 1.000 → 0.905…0.994.
- 1.9b. seller_name of both Physiotherapeut documents → Tanja Tinder (page_1 checked); no redundant accepted found (the only one — pt__20210508_202709, kept on the owner's instruction).
- 1.9c. P1b: «a service charge is not tax; local taxes such as PB1 are tax» (P1_null.txt untouched). FATURA «TAX $0.00» per line: the total_tax keys of such invoices were already excluded in stage 0; a wording is proposed in the stage report.
- 1.8. Rescoring: reports/rescore_r1_v2/<run>, gt_check → reports/gt_check_rescored_v2 (exit 0; 232 suspicious pairs marked with carried-over verdicts), comparison r1 → stage 0 → stage 1 — reports/rescore_r1_v2/compare.md. L1/L2: 245/638 → 195/516 → 186/505. Right→wrong: 7 rows, all the deliberate GT edit Physiotherapeut (the models answered «Physiotherapeutin»).
- final v4 totals: 1572 documents, 13273 values, 1199 nulls; 68 tests green.
- **final v4: sha256 = c14404ba90247a8982f33ec820ebfcdb018c3a123eb70d4c1f5fbe23d8394b58** — of the concatenation of all 1572 final/docs/*/answers.json in path order (`find final/docs -name answers.json | LC_ALL=C sort | xargs cat | shasum -a 256`).

### 2026-11-13 — stage 1 accepted; final v4 frozen
- Correction at acceptance: zugferd XML-Rechnung_FX_EN16931_Physiotherapeut — on the page the fields are labelled
  «Name: Physiotherapeutin», «Ansprechpartner: Tanja Tinder» → this is the seller's name, and by the owner's rule (4) it counts.
  The answer was restored: Physiotherapeutin. The second document (v2 intarsys, no field labels: profession above the name) — Tanja Tinder.
  The verdict in verdicts.jsonl (reviewer claude-opus, batch stage1-acceptance) overrides the earlier gt_wrong.
- Acceptance: 68 tests green; tools/apply_gt_review.py is idempotent (a second run makes no changes); runs/ untouched;
  stage 0 → stage 1 right→wrong: 1 row, expected (qwen3vl-4b, Physiotherapeut v2: «Physiotherapeutin»).
- Rescoring (reports/rescore_r1_v2/compare.md): L1/L2 245/638 → 195/516 → 185/505; 14472 keys; a queue of 451 new suspicious pairs.
- final v4: 1572 documents. sha256 (all answers.json in LC_ALL=C sort order, cat) =
  4ff069c0af657ea6c9da1ebcb8382a486ec8fc76e690c192e77f6ea7ef7602a7 (replaces the value in the agent's previous entry).
- Observation: the invented-value rate (FF / (FF + TN)) is 0.49–0.58 for qwen and 0.13 for gemma4-12b — the main reserve for P1b.

### 2026-11-13 — stage 2: code and queue
- P1b: invoice tax — only the tax total line; a per-line tax column is not the total; no line → null.
- harness/gt_arith.py: arithmetic of the ground truth itself. 56 violations, 48 explained (discount/service charge/rounding/the FATURA generator
  printed on the page), 8 unexplained (invoice_benchmark 5, cord 1, wild 1, zugferd 1). Example: invbench__INV-2026-0021 —
  the page itself prints 260 061.20 + 52 010.24 = 312 061.44 (an error of 10.00 in the document).
- harness/gt_stage2.py: queue reports/gt_check/stage2/queue.csv — 393 items, 16 batches: arith 7, «3 of 6» 171, audit of
  agreeing pairs 200 (stratified by source), 15 hidden controls. 85 tests green. Review — Sonnet.

### 2026-11-13 — stage 2: review 393/393 (Sonnet) and acceptance
- arith 7: all ok — the answers copy the page correctly; the errors are in the documents themselves (invbench 0021, 0110, 0115, 0117, 0179;
  zugferd Haftpflicht: due date 2013-12-06 earlier than the invoice date 2014-01-24; wild__0129 — a receipt for 0.00).
- «3 of 6» (177): model_failure 153, scorer_too_strict 11, definition_ambiguity 6, ok 6, gt_wrong 1.
- Audit of agreeing pairs: 0 ground-truth errors of 200 (without controls; 95 % Wilson 0–1.9 %). No extended audit needed.
- Controls: the GT value confirmed 15/15; 8 controls in the audit_agree stream marked ok instead of model_failure
  (the reviewer did not compare the predictions) — does not affect the estimate of GT errors. The reading does not copy the GT (case and format of the page).
- Ground-truth error: pt__20210323_162221 seller_vat_id <NIF> → <NIF> (page «CNT: <NIF>»; the NIF check digit
  is valid only for 394 — checked).
- By the owner's rules (to apply): Steuernummer 201/113/40209 in accepted for ~9 zugferd XML-Rechnung documents;
  the «NIF-IVA» label in the id_label rule; seller names pt__20210324_200034 (the owner), pt__20210507_214450 (station/dealer).
- Questions to the owner: wild__0016 total 63.92 vs «Amt Due» 63.90 after rounding; fatura Template39 seller_name — only
  the «LCSR» logo; zugferd seller_iban when only the IBAN of another payee / tax representative is printed.

### 2026-11-13 — owner's decisions (5) and final v5
- wild__0016 total: both 63.92 (Total) and 63.90 (Amt Due after rounding) count.
- fatura Template39_Instance1 (+ __mask) seller_name: excluded (only the «LCSR» logo).
- zugferd seller_iban when only the IBAN of another payee / tax representative is printed: that IBAN
  counts (GT AbweichenderZahlungsempf, Innergemeinschaftliche_Lieferungen, intarsys EXTENDED Fremdwaehrung already holds it).
- Applied (tools/apply_gt_review.py, stage=2 in applied_fixes.csv): Steuernummer 201/113/40209 in accepted for 18 zugferd
  documents (printed on the page — checked with Apple Vision OCR; not only the 8 from the review); seller names pt__20210324_200034
  (the owner's name as printed), pt__20210507_214450 (GAR RIBAMAR F. CUNHA COSTA); the «NIF-IVA» label in id_label (+ a test).
- pt__20210323_162221 seller_vat_id <NIF> → <NIF>. At acceptance: the reviewer miscounted (not «3 of 4 for 394»,
  but 2 models for 394, 3 for 294); the dot-matrix digit 3/2 is blurred (OCR reads 794). The NIF check digit decides: only 394 is valid.
  The document is marked quality=low (like nl-narrow-014). Cost: 3 rows TP→WV (gemma4-12b, qwen3.5-9b, qwen3vl-8b).
- Rescoring r1 → reports/rescore_r1_v3 (compare.md). L1/L2 185/506. 86 tests green; the script is idempotent.
- final v5: sha256 (answers.json, LC_ALL=C sort, cat) = cfac4f69e3322783866cd8399a887ed36e021476a7fb6c9ca6f91075d658706b

### 2026-11-13 — Qwen3.8 27B → stress track E
- The owner asked about Qwen3.8 27B (VLM, Aug 2026; it runs for the owner on another Mac through ollama). A run on another machine
  does not answer the research question (16 GB Mac mini), so — only track E on the Mac mini (00-plan.md, group E).
- Estimate before measuring: 3-bit ≈ 12.5–13.5 GB with an image — at the edge, needs a raised GPU limit; 2-bit ≈ 9–9.5 GB — fits.
- Order: after r1b and round 2, so as not to delay the main run.

### 2026-11-13 — P1b smoke and start of r1b
- P1b smoke (the same 33 documents as the P1v2 smoke), compared with r1 on the same documents with the same scorer:
  qwen3vl-4b accuracy 95.2 → 94.8 %, invented 11/19 → 11/19 (ignores the subtotal rule);
  gemma4-12b accuracy 96.8 → 96.8 %, invented 4/19 → 0/19. JSON 100 %, no reasoning left-overs or truncation; speed unchanged.
  Differences in individual rows (±4) are sample noise. fatura Template12 is self-contradictory (SUB_TOTAL 826.86 + TAX 26.72 ≠ TOTAL 828.69).
- Dashboard: «stopped» for r1 was false (2 excluded documents were counted as unfinished) — fixed in harness/dashboard.py/.html.
- r1b started: protocol/round1b.json, `caffeinate -i uv run python -m harness.study protocol/round1b.json`, log runs/study_round1b.log. ~44 h.

### 2026-11-15 — r1b finished; stage 3.3: gt_check on r1b and review
- r1b finished 2026-11-15 14:32 (`study done`): 6 models × 1572 documents × P1b, all runs complete.
- Invented values in r1b: almost all are subtotal = the receipt total (FF subtotal 460–514 for five models, 10 for gemma4-12b).
  Coincidences: 105 fields where ≥5 models gave the same number — all subtotal, 104 of them = total. The P1b rule
  «Do not copy the total into the subtotal» is followed only by gemma4-12b. The trap: «SUMME» / «TOTAL» with no subtotal line.
- Scorer: the `pay_class` rule (owner's decision 2026-11-15: a translation counts) — payment_method: cash
  CONTANTI = BAR = ESPECES = CASH, contactless KONTAKTLOS = SANS CONTACT = CONTACTLESS, diacritics folded; card brands
  are not merged, «CASSA 1» and typos are wrong. SERIES: a document-type code before a series starting with a letter («FR B19/43» = «B19/43»,
  decision 2026-11-13 (3)). harness/gt_check.py: `--n-docs` (r1b — 1572), r1b verdicts in CARRY_DEFAULT. 87 tests green.
- Rescoring r1b → reports/rescore_r1b (runs/ untouched): WV→TP payment_method 137, invoice_number 4; nothing else.
- gt_check → reports/gt_check_r1b_v2: L1/L2 35/627 (r1 v3: 185/506; L1 dropped because gemma4-12b is now right on subtotal).
  Queue of new pairs without controls: 251 → 97 after rescoring.
- Review (reports/gt_check/r1b/verdicts.jsonl, 522 verdicts, field method):
  - rule, 448: subtotal with GT null → model_failure (the synrec generator does not print subtotal; real receipts — a copy of TOTAL);
    a sample of pages 10/10 confirmed: synrec 614c, 012p, 906c, 250c; cord 021, 022, 025, 064; wild 0140, 0298;
  - page viewed, 9: model_failure 8 (cord 021/022/025 subtotal; edb es-000 buyer_vat_id — the seller's IBAN;
    edb fr-002 seller_name «Kraipreatraind» is right; korie IMG00241 2481 is right; zugferd Rechnungskorrektur issue_date
    16.09.2013 = Beleg-Datum; fatura Template39 __mask issue_date — the mask is clean, the Due Date was copied);
    scorer_too_strict 1 (pt__20210321_120107 invoice_number, fixed in SERIES);
  - models agree, page not opened, 65: ok (fields of documents queued as a whole).
  No ground-truth errors found, no edits of final/ — final v5 unchanged. Unreviewed suspicious pairs: 0 of 662.
- Next: 3.4 — report P1 vs P1b (rescore r1 with the current scorer), ranking, finalists; payment_method as a separate
  row, not in the overall ranking (discussed with the owner).

### 2026-11-15 — stage 3.4: P1 vs P1b, ranking, finalists (proposal)
- r1 rescored with the current scorer → reports/rescore_r1_v4; the keys of r1 and r1b match (14470 per model).
- harness/prompt_compare.py (+ tests/test_prompt_compare.py, 90 tests green) → reports/r1_vs_r1b/compare.md and csv.
  The main score — all fields except payment_method (a separate column). P1 is not «a second good prompt» but a prompt
  without field definitions (issue 14); the comparison shows the effect of the definitions.
- Paired comparison P1 → P1b (better / worse, sign test): gemma4-12b +175 (p<0.0001), qwen3vl-8b +66, qwen3.5-4b +60
  (p<0.0001), qwen3.5-9b +23 (p=0.056), qwen3vl-4b +15 (p=0.29), gemma4-e4b −239 (p<0.0001).
- gemma4-e4b with P1b is over-cautious: null where the value is printed (FN merchant_tax_id 71, seller_iban 76,
  total_tax 34; accuracy merchant_tax_id 96 → 77 %, seller_iban 82 → 70 %). The small model applies the rule «not printed → null»
  too broadly.
- Invented (FF/(FF+TN)) P1 → P1b: gemma4-12b 13.1 → 1.3 %; the others 40–57 %, almost entirely subtotal; without subtotal
  qwen3.5-9b 10.4 → 5.1, qwen3vl-8b 8.5 → 6.7, qwen3.5-4b 23.1 → 17.0, qwen3vl-4b 26.1 → 24.9, gemma4-e4b 2.2 → 2.2.
- P1b ranking by F1 (JSON valid 100 % for all): qwen3.5-9b 96.1; gemma4-12b 95.9; qwen3vl-8b 95.8; qwen3.5-4b 95.5;
  qwen3vl-4b 93.7; gemma4-e4b 90.5. The selection rule is the example from 00-plan.md 8.1 (top 3 by F1, JSON ≥ 90 %), not registered
  in advance. By it the finalists are: qwen3.5-9b, gemma4-12b, qwen3vl-8b — ~~waiting for the owner's approval~~
  **approved by the owner on 2026-11-15** (protocol/preregistration.md, section 1; note added 2026-11-18).

### 2026-11-15…18 — round 2: pre-registration, smoke, main run (entry written 2026-11-18)
- ☑ Approved by the owner: finalists qwen3.5-9b, gemma4-12b, qwen3vl-8b (2026-11-15); round-2 rules —
  protocol/preregistration.md (written 2026-11-15 before the first run); sample protocol/samples/round2.txt
  (400 documents, sha256 33a41f7b…, checked 2026-11-18).
- Smoke (protocol/round2_smoke.json, 33 documents): 14 of 15 configurations passed. gemma4-12b q8 — Metal OOM on all
  33 documents (weights 12.1 GB ≈ the GPU limit); the first run on 2026-11-15 caused a kernel panic; excluded by the amendment of 2026-11-16.
- Main run protocol/round2.json: 14 runs × 400 documents, 2026-11-16 → 2026-11-18 03:41 (`study done`),
  all complete. Analysis in the next entry.

### 2026-11-18 — stage 4: round-2 analysis (proposal)
- Rescoring r2 with the current scorer → reports/rescore_r2: 0 changed rows of 14 × 3510 against runs/ (the runs were already
  scored with the current scorer). final v5 — hash cfac4f69… matches. runs/ untouched.
- harness/round2_compare.py (+ tests/test_round2_compare.py; 95 tests green) → reports/round2/compare.md, models.csv,
  tests.csv, best.csv. Rules — preregistration.md sections 4–5: each mode against r1b of the same model on the same 400
  documents, sign test, Holm over 14 comparisons; invented values — a separate test (its own Holm family).
- Verdicts (F1 of main fields base → mode; better/worse keys; Holm p):
  - q6/q8 are the only thing that helps: gemma4-12b q6 96.0 → 98.1 (+105/−28, p<0.0001); qwen3.5-9b q6 96.1 → 96.9
    (p=0.010), q8 → 97.0 (p=0.002); qwen3vl-8b q8 95.9 → 96.6 (p=0.008); qwen3vl-8b q6 96.5 — no difference (p=0.058).
  - P0b, constrained — no difference for all three. P2b — no difference for Qwen, worse for gemma4-12b (−28, p=0.020) and
    1.6–1.9× slower.
  - Invented values: no significant change at all. Receipt subtotal for Qwen ~44 % remains in all modes — cured neither by
    the prompt, nor the schema, nor the bit width.
- Cost: peak memory q6 +2.2–3.0 GB, q8 +4.0–4.4 GB; seconds per document +10–27 %. Swap per run ≤ 1 GB (threshold 2 GB).
  gemma4-12b q6 — peak 12.58 GB. iogpu.wired_limit_mb = 0 (default) since the reboot of 2026-11-15 20:39 (kernel panic)
  — the whole main r2 run went without a raised limit, 0 memory errors; a raised limit is not needed.
- Best configuration by the rule of section 5: **gemma4-12b q6** (F1 98.1; invented 2.8 %; 32 s/doc; share of documents
  without a single error 86 % against 63 % for the next one). Next: qwen3.5-9b q8 97.0; qwen3.5-9b q6 96.9.
- Caveat (descriptive, not per the pre-registration): the gain of gemma q6 is almost entirely on generated documents
  (F1 96.4 → 98.9; mostly seller_iban eurodocbench, +27 keys); on the 93 real documents 93.6 → 93.2. On real documents
  qwen3.5-9b q8 is best (89.5 → 93.1). The real sample is small — the full run will check this.
- Ground-truth check of r2 (gt_check is built for 6 models and does not run on 14 configurations — a simplified version): keys
  where all 17 configurations were wrong (14 + 3 bases) — 7, all with earlier verdicts; the majority wrong — 143, of them
  3 without a verdict → checked against the page (reports/gt_check_r2/verdicts.jsonl): all model_failure (cord 070 __mask
  subtotal 1,343,000 read as 1343.00; eurodoc pt-007 «Torosetrerk» is right; fatura T18 __mask — the logo text
  «SIMPDEHY» is not a name, like Template10 «HGH»). No ground-truth errors, final v5 unchanged.
- Next per the pre-registration (section 5, item 4): gemma4-12b q6 and qwen3.5-4b q6 on the whole of final/ (estimate ~15 h + ~6–7 h;
  download the 6-bit qwen3.5-4b weights and run a smoke test). Not started — waiting for the owner's decision. Also open: the Qwen3.8 27B track
  and the extractors (NuExtract3, lift).

### 2026-11-18 — final run: checks, 4B q6 smoke, start
- Checked before the start: iogpu.wired_limit_mb = 0 (default since the reboot of 2026-11-15 20:39) — as in all of r2;
  sudo not needed. Amendment in preregistration.md of 2026-11-18.
- Queue protocol/round_final.json, `caffeinate -i uv run python -m harness.study protocol/round_final.json`,
  log runs/study_round_final.log, started 07:36.
- Smoke s3__qwen3.5-4b__q6 (mlx-community/Qwen3.5-4B-6bit @ fbb1092a, 33 documents): JSON 100 %, 0 errors, 0 truncations,
  0 reasoning left-overs; against r1b 4-bit on the same documents F1 95.3 → 96.3 (+3/−0), invented 57.9 → 52.6 %;
  13.7 s/doc (4-bit 12.6), peak 6.15 GB, swap +0. The criteria of section 6 are met — smoke accepted, hold removed.
- Running f__gemma4-12b__q6 (1572 docs, ~15 h), then f__qwen3.5-4b__q6 (~6–7 h).

### 2026-11-19 — final comparison, invented-value analysis, summary document, GitHub
- `harness/final_compare.py` → `reports/final/compare.md`: gemma4-12b q6 vs qwen3.5-4b q6 on 1572 documents,
  paired comparisons, a real/generated breakdown and by language (exploratory). The final runs were rescored into
  `reports/rescore_final/`.
- Invented values (`reports/invented/analysis.md`): for qwen3.5-4b q6, 92 % of invented values (497 of 538) are a receipt `subtotal`; without it
  6.0 % (gemma 0.7 %). The «language effect» in invented values is a document-type artefact (receipts only in de/fr/it/en/id/ko).
  gemma q6 on real documents: 0 → 8 invented values out of 133 null keys (sign test p = 0.0078, descriptive); 66.7 % for
  real pt in final/compare.md — 2 of 3 keys, noise. Open question to the owner: whether a computed subtotal counts as
  an invented value.
- Summary document: `reports/SUMMARY.md`.
- GitHub: organisation FideNubiResearch; a private repository (full history) and the public
  `local-llm-accounting` (clean history, without documents, answers or per-document predictions; list and rules —
  `tools/publish_public.sh`). Licences: MIT (code), CC-BY-4.0 (texts).
- Open: the Qwen3.8 27B track, extractors NuExtract3 and lift, energy (powermetrics), subtotal policy.

## 2026-11-20 — 27B and extractors

- Qwen3.8 27B 3-bit: smoke with the default limit stopped by the guard (swap +2.06 GB); with `iogpu.wired_limit_mb=14000` peak 14.7 GB, Metal OOM on every document, stopped manually. Verdict «not suitable for a 16 GB Mac mini», amendments in the pre-registration. Local revisions (`local-…`) added to `harness/runner.py`.
- Extractors: NuExtract3 4B q6 (prompt adapter `harness/run.py: nuextract_inputs`, `--nuextract`) and lift 9B oQ6 (P1b + constrained); smoke on 33 docs passed (JSON 100 / 97 %), then 400 documents without errors or guard trips. Comparison: `harness/ext_compare.py` → `reports/extractors/compare.md`, rescoring → `reports/rescore_ext/`. Result: the extractors are not better than gemma4-12b q6; NuExtract3 ≈ qwen3.5-4b; lift is less accurate but has almost no invented values outside `subtotal`.
- `iogpu.wired_limit_mb` stays 14000 until reboot (does not affect the extractor results).
- Open: energy (powermetrics, sudo), `subtotal` policy.

## 2026-11-20 — energy and subtotal policy

- A sudoers rule only for `/usr/bin/powermetrics` (NOPASSWD), set up by the owner. `harness/energy.py` → `reports/energy/` (33 smoke documents per configuration, run_id `e__…`). SoC ≈ 15 W for all (GPU saturated); Wh/doc: gemma4-12b q6 0.131, lift 0.100, qwen3.5-4b q6 0.059, NuExtract3 0.053.
- `subtotal` policy (owner): an invented value if the prompt explicitly restricted the computation. P1b restricts it → the current scoring is right, no rescoring needed; P1 (round 1) did not → read with care. Recorded in `reports/invented/analysis.md`, `reports/SUMMARY.md`.
- Open: remove the sudoers rule when measurements are no longer needed; restore `iogpu.wired_limit_mb=0` (or reboot).

## 2026-11-20 — public repository in English only

- Owner's decision: everything published is in English; Russian only in the private repository.
- Code (report generators `final_compare`, `ext_compare`, `energy`, `memguard`) and the queue descriptions in `protocol/*.json` were translated to English in the repository itself; reports rebuilt.
- Hand-written documents stay in Russian; English translations live in `public_en/<same path>` (README, SUMMARY, invented-value analysis, pre-registration, final/README, licences, exclusions, model catalogue and setup, dashboard, plans, literature review, this journal).
- `tools/publish_public.sh`: substitutes the translations, does not publish Russian files without a translation, and stops if a translation is older than its Russian original or Cyrillic is left in the public tree. In the English journal the names of private individuals are replaced by a description.
