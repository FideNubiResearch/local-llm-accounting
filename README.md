# local-llm-accounting

Can a small vision-language model, running locally on a 16 GB Mac mini (Apple Silicon, MLX), read accounting
documents — invoices, receipts, bank statements — and return their fields as JSON? We measure how accurate
that is, how often the model invents a value for a field that is not on the page, and what it costs in time,
memory and energy.

Short answer: yes, as a draft for a bookkeeper. The best configuration (`gemma4-12b`, 6-bit) gets 94 % of the
values right on real invoices and receipts (99 % on generated ones), but only 78 % of real documents come out with
every field right, so a person still has to check each document — IBANs and VAT numbers above all.
Full summary: [`reports/SUMMARY.md`](reports/SUMMARY.md).

## Setup

- 1572 documents (865 invoices, 699 receipts, 8 bank statements), 10 languages, 13 273 field values and 1 199 fields
  whose correct answer is `null`. 305 real and 1267 generated documents; sources and licences are in
  [`final/licenses.csv`](final/licenses.csv), the document list in [`final/manifest.csv`](final/manifest.csv).
- Models run through [mlx-vlm](https://github.com/Blaizzy/mlx-vlm), temperature 0, JSON output, 4/6/8-bit weights.
- Scoring: value accuracy, F1 over the main fields, invented-value rate (`FF / (FF + TN)`), documents with every
  field right, seconds per document, peak memory, energy. Paired tests (exact sign test, Holm correction).

## Results

| Stage | What | Where |
|---|---|---|
| Round 1 | 6 models × 2 prompts (P1, P1b), 1572 documents | [`reports/r1_vs_r1b`](reports/r1_vs_r1b/compare.md) |
| Round 2 | 3 finalists × prompt variants, constrained decoding, 6/8-bit weights, 400 documents, rules fixed in advance | [`reports/round2`](reports/round2/compare.md), [`protocol/preregistration.md`](protocol/preregistration.md) |
| Final | best round-2 configuration and `qwen3.5-4b` on all 1572 documents | [`reports/final`](reports/final/compare.md) |
| Extractors | NuExtract3 4B and lift 9B against the best VLMs, 400 documents | [`reports/extractors`](reports/extractors/compare.md) |
| Energy | powermetrics, SoC power per document | [`reports/energy`](reports/energy/energy.md) |
| Invented values | where they come from | [`reports/invented`](reports/invented/analysis.md) |

Final run (all documents):

| | F1, % | Correct values, % | Invented, % | Docs without errors, % | s/doc | Peak GB |
|---|---|---|---|---|---|---|
| gemma4-12b 6-bit | 98.4 | 98.3 | 1.4 | 88.4 | 34.2 | 12.6 |
| qwen3.5-4b 6-bit | 96.1 | 98.0 | 44.9 | 57.8 | 16.8 | 6.2 |

Caveats: on the 305 real documents accuracy is lower (94.4 % correct values for gemma4-12b 6-bit) and its
invented-value rate is higher. 92 % of the values invented by `qwen3.5-4b` are a receipt `subtotal` that is not
printed, which the prompt explicitly forbids. Per-language numbers are exploratory (language is confounded with
source and type). `gemma4-12b` 8-bit and Qwen3.8 27B (3-bit) do not fit in memory on a 16 GB machine
(see the amendments in the pre-registration).

## Layout

- `harness/` — runner, scorer, normalisation, reports (`run.py`, `study.py`, `score.py`, `report.py`, …)
- `protocol/` — prompts, field list, JSON schemas, run queues, sample lists, pre-registration
- `reports/` — comparisons (aggregated results only)
- `runs/<run_id>/` — `config.json` and `summary.md` of every run
- `tools/`, `tests/` — dataset assembly helpers, publication script and unit tests
- `00-plan.md`, `01-literature.md`, `05-closeout-plan.md`, `journal.md` — plan, literature review, close-out plan,
  working log

## What is not here

The documents themselves, the ground-truth answers and per-document model outputs are **not published**: several
source datasets have no confirmed redistribution terms, and some contain real company data. The scorer and all
protocols are included; the sources and their pinned revisions are listed in `final/licenses.csv`.

## Reproducing

```
uv sync
uv run python -m pytest tests
uv run python -m harness.study protocol/round2_smoke.json   # needs the documents (not included)
```

## Licence

Code (`harness/`, `tools/`, `tests/`): [MIT](LICENSE). Reports, protocols and text:
[CC-BY-4.0](LICENSE-docs). Source datasets keep their own licences, see `final/licenses.csv`.
