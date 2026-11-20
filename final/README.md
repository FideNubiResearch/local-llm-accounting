# Final document set

The documents the models are tested on, and their correct answers. The experiment uses only this folder.
The set is frozen: it is not rebuilt, and changes only through a deliberate edit recorded in the journal.

The documents and answers themselves (`docs/`) are not published in the public repository; only the manifest,
the exclusions and the licences are.

## Contents

1572 documents: 865 invoices, 699 receipts, 8 bank statements; 10 languages (en 339, de 312, it 240, fr 227,
pt 130, es 80, nl 80, pl 80, id 54, ko 30); 41 documents with a masked field (for 19 of them the masked amount
is excluded from scoring, see below). 13273 values, 1199 fields whose answer is null. (Before the stage-1 edits of
2026-11-13: 1574 documents, 13275 values, 1226 nulls.) The number of documents is larger than the number of
independent ones: a receipt has `clean` and `photo` variants, a masked document has its original (`base_doc`). How
many independent documents there are in each cell and which of them are real: `../00-plan.md`, section 3.

Added 2026-11-11 (generated, answers from the generator, found in the page text):
- **EuroDocBench** — 625 invoices: 80 each in de, en (en-IE), es, it, nl, pl, pt and 65 in fr. Five layouts and
  three fonts, the same for all languages, to compare languages with everything else equal. The `template` column
  in `manifest.csv` is the layout/font. French invoices whose font lacks the thousands-separator glyph (an empty box
  in the image) are excluded entirely; hence fr has 65 invoices and no monospaced font.
- **Synthetic receipts** — another 60 independent receipts each in de, fr, it (now 80 each), each in a clean and a
  photo variant.

- `docs/<doc_id>/page_N.png` — the pages as the model receives them.
- `docs/<doc_id>/answers.json` — correct answers per field:
  - `answer` — the answer in a single canonical form; `null` — the field is not in the document, the model's correct
    answer is null;
  - `printed` — how the value is printed (for checking), `masked: true` — the value is masked.
  - `accepted` (optional) — other correct values of the field: the seller's brand and legal entity, dealer/station,
    another seller tax number (Steuernummer, NIPC). The model's answer is right if it matches `answer` or any of them;
  - `accept_from` (optional) — the invoice prints only one of the amounts total_gross / total_net: that amount is
    accepted in whichever of the two fields the model writes it.
  - `quality: "low"` (optional, document level) — the page is hard to read (low resolution, cropping,
    indistinguishable O/0). The document is scored as usual; reports give accuracy both with and without such
    documents.
- `manifest.csv` — one row per document: source, where it was actually downloaded from (`upstream`: the id in
  `data/sources.yaml` and the path inside the archive), language, type, variant, masked field, number of values and
  nulls, page sha256, the basis for trusting the answers, `quality` (`low` or empty).
- `excluded.csv` — what was left out and why. It also lists 60 invoice amounts (total_gross / total_net /
  total_tax) that are not in the document (the answer was null, the field not masked): they were removed from
  answers.json and are not scored.
- `licenses.csv` — the licence of every source with a verbatim quote. Five sources (ZUGFeRD, SROIE, WildReceipt,
  KORIE, Bank-Statement-Intelligence) have no explicitly established licence; they were kept deliberately: the
  documents are used only for local measurements and are not published.

## Canonical answer forms

| Kind | Format | Example |
| --- | --- | --- |
| Date | `YYYY-MM-DD` | `2015-09-18` |
| Time | `HH:MM`, 24-hour | `13:48` |
| Amount | decimal number with a point, no thousands separators or currency; compared as a number | `889.2`, `27640` |
| Currency | ISO code | `EUR` |
| Number (invoice, tax, IBAN) | without the printed label («SIRET», «USt-IdNr.») | `20149268321989` |
| Text (names) | as printed | `COMPTOIR ARIBELLA` |

## Why the answers can be trusted

A value is taken only if one of these holds:

1. it comes from the document's XML or generator and is found in the text of the page itself;
2. Claude viewed the whole page and confirmed the value.

In addition, it was not disputed by an independent review (`../reports/review_2026-11-11.md`): if the review
corrected a value, its correction is taken.

`null` is taken only if the absence of the field was confirmed by viewing the page. Masked documents are taken only
if both checks agree that the value cannot be read anywhere else.

## How it was checked

- **Every value** was first searched for in the page text (PDF text layer and Apple Vision OCR), allowing for number
  and date formats and line breaks.
- **Every "field absent" and every mask** was checked by viewing the whole page, scaled down to about 0.6 megapixels
  (at that size the small text of an A4 invoice is still readable). Crops around the field turned out to be
  insufficient: they missed repeats of the value elsewhere on the page (the total in words, a handwritten amount, a
  name in an e-mail address).
- **Values on photos and scans** that were not found automatically were checked on the full page.
- **Independent review** by another agent: 159 whole documents, including all corrected values.

Errors found in the datasets themselves (excluded from scoring or corrected):

| Dataset | Error |
| --- | --- |
| InvoiceBenchmark | Amounts labelled without VAT, but printed with VAT |
| ZUGFeRD | The embedded XML sometimes differs from the printed PDF; in one invoice the XML describes another invoice |
| FATURA | Buyer and total under non-standard labels are not annotated; the total is sometimes only in words |
| WildReceipt | Manual transcription with typos; the total is not annotated although printed |
| Portuguese receipts | Seller not annotated; a credit note carries the number of the original invoice |
| KORIE, SROIE, synthetic receipts | Extra characters in the date, recognition errors in the name, tax number together with its label |

## What is not here (deliberately)

- XFUND forms — not accounting, ambiguous annotation;
- tables (invoice lines, statement transactions) — the cells were not checked one by one;
- fields that could not be brought to one canonical form unambiguously (for example WildReceipt dates where it is
  unclear whether day or month comes first) — see `excluded.csv`.

## Known defect: day and month order in synthetic receipts

The synthetic receipt generator (`synrec__*`, source `synthetic_receipts`) prints the date sometimes as dd/mm,
sometimes as mm/dd, with no format hint on the page; the answer (`answer`) comes from the generator and is right,
but from the page an ambiguous date (day and month ≤ 12, e.g. «07/04/2024») cannot be told from a swap. So the scorer
accepts both orders for ambiguous dates (the `date_swap` rule in `../harness/normalize.py`, owner's decision of
2026-11-13 (1) item 3). Unambiguous dates (day > 12) are compared strictly. The answers were not changed; the defect
can only be fixed by regenerating the set.

## How it was built

The set was built from an intermediate corpus by `tools/build_final.py`. Both the corpus and the script were removed
after the freeze; their code is kept in git, in a snapshot commit whose hash is given below. A byte-for-byte rebuild
from the sources is not guaranteed: downloading the sources again may give different files.

Snapshot commit: see `git log --grep "Freeze final dataset"`.

The 2026-11-11 addition was built separately by `staging/eurodocbench/build.py` and
`staging/synthetic_receipts/build.py` and copied here unchanged (page hashes verified). Checks and exclusions:
`../reports/staging_check.md`. After the transfer `staging/` was removed; the scripts, selection and evidence are kept
in git, in the commit `git log --grep "Add EuroDocBench"`.

## Edits after round 1 (2026-11-13)

The set was edited deliberately, with the owner's permission, after the ground-truth check (`../reports/gt_check/`):
5 corrected answers, 33 acceptable alternatives (`accepted`), 19 fields with `accept_from`, 60 excluded invoice
amounts. Every edit is in `../journal.md` and `../reports/gt_check/applied_fixes.csv`; applied by
`../tools/apply_gt_review.py`. Masked amounts (`masked: true`) stayed in scoring as an absence check. Round-1 results
with the old answers: `../runs/r1__*/fields.csv`; rescored with the new ones: `../reports/rescore_r1/`.

## Stage-1 edits (2026-11-13, final v4)

With the same `../tools/apply_gt_review.py` (rows `stage=1` in `applied_fixes.csv`), with the owner's permission:
- 2 documents excluded entirely: wild__0426, wild__0428 — stock mock-ups whose arithmetic does not add up (rows with
  field `*` in `excluded.csv`; removed from `manifest.csv` and `docs/`, kept in git history);
- 19 mask probes excluded: the masked amount can be computed from printed numbers (subtotal + tax, subtotal +
  service + tax, line items, total − subtotal), or a rounded / unrounded amount is visible. Candidates were found by a
  rule (`../tools/mask_probe_scan.py`, Apple Vision OCR) and each checked against the page; evidence in
  `excluded.csv`. Three FATURA total_gross masks were kept: SUB_TOTAL and TAX are printed, but the generator's TOTAL
  is not their sum;
- the seller_name answer of two zugferd Physiotherapeut invoices corrected: «Physiotherapeutin» (a profession) →
  «Tanja Tinder»;
- `accepted` added for pages that print two values: BASIC-WL Einfach due_date 2020-04-04 (and 2017-12-13),
  fatura Template49_Instance0 (+ __mask) buyer_name Joseph Wagner (and Jessica Acevedo), pt__20210428_140713
  seller_name ELENCOJASMIN LDA (and elencojasmim lda); Kostenrechnung v1 seller_name — both names, since stage 0;
- `quality: low` label on 6 documents: wild__0352, sroie__X51006328937, synrec__eval-000608__photo,
  pt__20210428_141746, pt__20210507_215634, eurodocbench__test-nl-NL-narrow-014.
