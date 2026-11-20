# Local LLMs for accounting documents on a 16 GB Mac mini M4 — research plan

Plan version: **2** (2026-11-10). Includes the owner's answers. Changes against v1 are at the end of the file.

**Hardware:** Mac mini M4 (10 CPU / 10 GPU), 16 GB unified memory (≈12 GB available to the GPU by default), 120 GB/s, 256 GB SSD (≈196 GB free), macOS 26.3.1.

**Principles:**
- only **open-source documents** with existing annotations;
- we publish **only measurements and conclusions**, not the documents themselves;
- everything runs **locally** on this Mac.

---

## 1. Goal and research questions

Find the **most accurate** configuration for extracting data from accounting documents on a 16 GB Mac mini and describe its cost: time, memory, energy. Separately: how the result depends on the **document language**.

- **RQ1. Accuracy.** Which model and which pipeline give the best per-field accuracy?
- **RQ2. Hallucinations.** How often does the model invent a value for a missing field? How does this depend on the model, quantisation, prompt and strict JSON?
- **RQ3. Languages.** How much does accuracy drop and hallucination grow in German, French, Italian, Spanish, Portuguese, Polish, Dutch, Chinese, Japanese, Korean and other languages compared with English? Which model is best for each language?
- **RQ4. Document type.** Invoices, receipts, bank statements, financial reports, e-invoices with line items — where are models strong and where do they break?
- **RQ5. Speed and resources.** Seconds, memory and energy per document. Pareto front «accuracy ↔ time».
- **RQ6. Getting the most out of it.** Voting over several runs, a second checking pass, the PDF text layer, arithmetic checks — what accuracy gain and at what time cost?

## 2. What has already been studied (so as not to repeat it)

Checked by search on 2026-11-10. Details are kept in `01-literature.md`.

| Work | What was done | What is missing (our gap) |
|---|---|---|
| **ExtractBench** (arXiv 2607.29677) | 370 business documents, 14 systems, F1 with null handling; Qwen3.6 35B-A3B (FP8), Gemma 4 26B, lift 9B, NuExtract3 | Server GPUs; languages not analysed; quantisation not studied |
| **UniKIE-Bench** (arXiv 2602.07038) | DocILE/SROIE/CORD/SIBR/EPHOIE etc., 15 models, open 2–9B on 2×A100. Chinese clearly worse than English | Missing fields only in the error analysis; EN/ZH only; not edge hardware |
| **ReceiptBench** (arXiv 2605.22413, ACL 2026) | 10.6 k receipts, false positives as a hallucination measure | 98 % English; no degradations; no edge hardware |
| **Electricity invoices** (arXiv 2604.25927) | Spanish invoices; Mistral-small «makes up» fields | Cloud, text only, one language |
| **Abstention as prompt artifact** (EMNLP 2026) | Refusal to answer depends strongly on the prompt | Not on documents, not on local models |
| **lift / NuExtract3** (Datalab, 2026) | Vendor benchmark of 225 documents | Vendor benchmark, no hallucinations or languages |
| **VAREX** (2603.15118), **RealDocBench** (2606.07401), **DocAttriBench** (2609.20574), **CFMME** (2605.29462, Chinese finance) | — | **Read in phase 0** |

**Our gap (re-check in phase 0):**
1. **A multilingual accounting benchmark** of local models: 10+ languages and several document types under one method. The works found cover at most EN + ZH.
2. **Controlled missing fields on real documents:** we mask a field by its coordinates from the annotation and measure whether the model invents a value. Plus the effect of quantisation, prompt and strict JSON on that rate.
3. **Consumer Apple silicon with 16 GB:** accuracy together with time, memory and energy per document.
4. **Three approaches on one machine:** VLM directly · OCR → text LLM (base: the built-in macOS OCR) · specialised extractor.

## 3. Data

The set is frozen in `final/`: pages, correct answers, composition and justification — `final/README.md`.
Below: what it contains and which conclusions it allows (decisions of 2026-11-11).

### 3.1. Composition: independent documents

An independent document is one source document; its variants (clean/photo, masked field) do not add to the count.
«Real» means documents from actual business or software (SROIE, WildReceipt, CORD, KORIE, ZUGFeRD, PT receipts and
invoices); the rest are generated (EuroDocBench, synthetic receipts, FATURA, InvoiceBenchmark, katanaml, statements).

| Language | Invoices, total (real) | Receipts, total (real) |
| --- | ---: | ---: |
| en | 178 (2) | 100 (80) |
| de | 152 (72) | 80 (0) |
| fr | 67 (2) | 80 (0) |
| it | 80 (0) | 80 (0) |
| pt | 130 (50) | — |
| es, nl, pl | 80 each (0) | — |
| id | — | 48 (48) |
| ko | — | 30 (30) |

8 bank statements (en, generated).

### 3.2. Sufficiency rules and what follows from them

1. **A «language × type» cell** is shown from 30 independent documents, target 80. id (48) and ko (30) have wide
   error margins.
2. **Language comparison** uses the EuroDocBench block: 8 languages, the same 5 layouts, type invoice. The rule
   «each language has two document types» was dropped: identical layouts separate language from type better.
3. **Font.** fr in EuroDocBench has no monospaced font (those invoices were excluded because of a glyph defect).
   Languages are compared twice: all 8 languages on documents without the monospaced font, and 7 languages (without
   fr) on all of them. Layout and font are the `template` column in `final/manifest.csv`.
4. **Real documents.** Conclusions «on real documents» only for en (receipts), de and pt (invoices), id and ko
   (receipts). fr, it, es, nl, pl have only generated documents; this is a limitation of the study, we stop searching.
   Results on generated and real documents are shown separately.
5. **Invented answers (correct answer null).** The main measurement is on the whole EuroDocBench block (about 400
   nulls). Per language only as a guide; de and en pass the 150-null threshold. For id (6 nulls) and ko (0) it is not
   computed. In the EU synthetic receipts subtotal is not printed and is always null — show it per field, not as one
   total.
6. **Bank statements** (8 documents) are outside the conclusions of the first round.
7. **Volume.** 1574 documents ≈ 13 hours per model with one prompt at 30 s per document. The first round runs on a
   subsample; which one is decided when the pipeline is built.

### 3.3. Missing fields

- `null` in the answers only if confirmed by viewing the page or proven by the generator code and absence from the
  page text.
- 41 documents with a masked value whose label is kept («IBAN: ____»); the correct answer is `null`.

## 4. Models (candidates — confirm by measurement that they fit)

The starting list comes from the fidenubi.com calculator. Its memory and speed predictions are **checked against real measurements** (also useful for the site).

| Group | Models |
|---|---|
| **A. General VLMs** (image → JSON) | Qwen3-VL 4B/8B · Qwen3.5 4B/9B · Gemma 4 E4B/12B · if they run: MiniCPM-V 4.5 8B, InternVL3.5 8B, GLM-4.1V 9B |
| **B. Extractors** | lift 9B (Datalab) · NuExtract3 4B (NuMind) |
| **C. OCR for the pipeline** | Apple Vision OCR (built into macOS) · GLM-OCR 1.3B · PaddleOCR-VL 0.9B · DeepSeek-OCR small · PDF text layer |
| **D. Text LLMs for the pipeline** | Qwen3.5 9B · Gemma 4 12B · Llama 3.1 8B |
| **E. «Maximum» stress track** | Qwen3.8 27B (VLM, Aug 2026; added 2026-11-13) · Qwen3.6 27B and 35B-A3B at 2–3 bits · Bonsai 2 27B (ternary) · with a raised GPU memory limit |

Memory estimate for Qwen3.8 27B (before measuring): 3-bit ≈ 11.5–12 GB of weights + image encoder and cache ≈ 1–1.5 GB → 12.5–13.5 GB: only with a raised `iogpu.wired_limit_mb`, at the edge, swap possible. 2-bit ≈ 8.5–9.5 GB: fits the default limit (~10.7 GB). First a smoke run (33 documents, P1b) at 3 bits; on swap or crashes — 2 bits. Disable «thinking» via the template and check on the first answers. Ready MLX weights at 2/3 bits may not exist — then quantise ourselves (mlx-vlm convert; bf16 ≈ 54 GB on SSD).

**Quantisation** for 2–3 finalists: 4 / 6 / 8 bits.

**Cloud models are not used** (owner's decision). We study only local models on this Mac.

## 5. How we test (protocol)

**Tasks:**
1. **Schema extraction.** One JSON schema per document type:
   - invoice: seller, buyer, tax IDs, number, dates, currency, net, VAT, total, IBAN, line items;
   - receipt: shop, date, line items, total, tax;
   - statement: account, period, balances, transactions;
   - financial report: given indicators.
2. **Targeted questions**, including about missing fields. The correct answer for them is `null`.

**Factors:**

| Factor | Levels |
|---|---|
| Model | section 4 |
| Language and document type | section 3 |
| Pipeline | VLM directly · OCR → LLM · extractor · hybrid (image + text layer) |
| Quantisation | 4 / 6 / 8 bits (for finalists) |
| Prompt | P0 neutral · P1 «return null if the field is absent» · P2 + a mandatory quote from the document |
| Output | free JSON · schema-constrained decoding |
| Prompt language | English · the document's language (for finalists) |
| Boosters | voting over 3 runs · a second checking pass · arithmetic validator + retry |

A full factorial is impossible. So: pilot → 3–4 finalists → prompt, quantisation and output factors on the finalists only.

**Rules:**
- temperature 0, fixed seed; 3 repeats on 10 % of the sample to estimate variation.
- Normalisation before comparison: dates → ISO, amounts → decimal allowing for local formats (`1.234,56` / `1 234,56` / `1,234.56`), IDs without spaces, Unicode NFKC for CJK.
- The same inputs, schemas and prompts for all models; everything is versioned in `protocol/`.
- Before a series we record the environment: versions, weight revisions, `pmset`, no other load.
- Runs go continuously in the background under `caffeinate`. Every answer is written to JSONL at once, so a run continues after a failure.
- During speed measurements nothing heavy runs on the Mac, otherwise the timings are distorted. If there was load, it is noted in the journal and the run is repeated.

## 6. Metrics

**Accuracy:** field accuracy and F1 after normalisation (null following ExtractBench) · ANLS for strings · share of documents with all fields right · F1 over invoice lines (Hungarian matching).

**Hallucinations:**
- **False-fill rate** — share of missing fields that got a value. The main metric.
- **Over-abstention** — share of present fields the model answered with `null`.
- **Wrong-value rate** — the field exists, the value is wrong.
- **Unsupported value** — the value is not in the document text.
- **Arithmetic violation** — line items, net + VAT, total do not add up.
- For P2: the share of quotes actually found in the document.

**Speed and resources:** seconds per document · image encoding · prefill/decode tok/s · time to first token · documents per hour · peak memory and swap · **energy per document** (`powermetrics`) · throttling on long runs · cold and warm start.

**Reliability:** share of valid JSON · schema conformance · crashes and OOM.

**Statistics:** 95 % bootstrap confidence intervals; models compared with McNemar's paired test. «A is better than B» only with a significant difference.

**Output:**
- tables «best model per language» and «per document type»;
- Pareto plots «accuracy × time» and «accuracy × false fill»;
- a recommended configuration for 16 GB.

## 7. Organisation and reproducibility

```
local-llm-accounting/
├── 00-plan.md            ← this file
├── 01-literature.md      ← works, links, gap
├── journal.md            ← journal: date, what was done, result
├── final/                ← the set: pages, answers, composition, exclusions, licences (README.md)
├── protocol/             ← schemas, prompts P0–P2, field names
├── harness/              ← runner.py (mlx-vlm), run.py (run), score.py + normalize.py (scoring), report.py
├── tools/fetch.py        ← downloading the sources (data/sources.yaml, data/manifest.json)
├── tests/                ← scoring tests
├── runs/<run_id>/        ← config.json, predictions.jsonl, fields.csv, summary.md
├── models_cache/         ← model weights (not in git)
└── reports/              ← dataset checks, model catalogue, reports
```

Run: `uv run python -m harness.run --model <repo> --revision <sha> --prompt P1 [--where lang=fr]`;
scoring: `uv run python -m harness.report runs/<run_id>`. A run resumes where it stopped.

- The folder is a local **git repository**, every series is a commit. Any run can be repeated with the command from its `config.json`.
- Python via `uv` with a lock file, runtime versions pinned.
- Documentation is written as we go; after every step, an entry in `journal.md`.
- **Runtime:** main — MLX / mlx-vlm; control — llama.cpp (GGUF, constrained grammar). Ollama is not used for measurements: an extra layer, less control over parameters.
- **Published package:** code, protocol, manifest (links + sha256 instead of documents), raw model answers (without images) and metrics. With it anyone can repeat the study by downloading the datasets themselves.

## 8. Phases and timeline

### 8.1. Mode of work: «prepare everything → one start → results»

Owner's decision: first prepare everything completely (phases 0–2), then **one start** of the pipeline, which runs phases 3–6 by itself up to finished tables and plots.

- **Experiment queue** — one file `study.yaml`: sets, models, factors, order.
- **Pre-registration of the selection rules** before the start, in `protocol/preregistration.md`. For example: «the 3 best pilot models by F1 with valid JSON ≥ 90 % go to the main runs; on a tie, fewer false fills». The pipeline applies the rules itself, without manual intervention.
- **Models one at a time:** download → check the hash → run → record the result → delete. Peak disk use — 1–2 models.
- **Self-protection:** a model that does not load or fails with OOM is skipped with the reason recorded. A run stops if valid JSON < 50 % or accuracy ≈ 0 on the first 20 documents (a likely configuration error). After a failure or reboot the pipeline continues where it stopped.
- **Status** in `runs/STATUS.md` is updated as it goes: what is done, what is running, estimated time left.
- **A recommended (not mandatory) check** 1–2 hours after the start, once the smoke test has passed.
- **Reusable framework:** the code in `harness/` does not depend on this study. A new study is a new `study.yaml` and, if needed, a new dataset or schema.

### 8.2. Phases and timeline

| Phase | Content | Time |
|---|---|---|
| 0 | More literature, confirm the gap | 0.5 day |
| 1 | Environment setup, smoke test of models, memory measured against the calculator | 0.5–1 day |
| 2 | Loading the datasets, masking, schemas, prompts, scorer with tests | 1.5–2 days |
| 3 | Pilot ≈70 documents × all candidates → finalists | ≈0.5–1 day of machine time |
| 4 | Main runs: finalists × languages × pipelines × prompts × quantisation | ≈3–4 days non-stop |
| 5 | «Maximum» track + stress track of large models | ≈1–2 days |
| 6 | Analysis, report, texts per language | 1–2 days (in parallel with the runs) |

**Total ≈ 7–10 calendar days.** Preparation takes 2–3 days; the rest of the time the Mac computes 24/7.

Where the figure comes from: one pass of one model over 600 documents at 20–40 s per document takes 3–7 hours. 20–30 passes are needed, i.e. ≈4–6 days of machine time.

First results (finalists, first numbers per language) — **on day 3–4**. The timeline can be shortened by reducing the set or the number of factors.

## 9. Compatibility with other uses of the Mac

- Installing the tools (Xcode CLT, Homebrew, Python/uv, mlx-vlm, llama.cpp) **does not affect** SSH, Screen Sharing, network or power settings.
- During runs the Mac is loaded almost 100 %. SSH and Screen Sharing keep working, but slower.
- Reboots, power-loss tests and network changes are coordinated so as not to break a run. A run continues where it stopped, but time is lost.
- **Disk:** models take 80–120 GB of 196 GB. Models that are done are deleted.
- The study has to be finished and its results exported before the Mac is reset for other use.

## 10. sudo access

Needed for two things: `powermetrics` (energy) and `sysctl iogpu.wired_limit_mb` (GPU memory limit for the stress track).

**Do not send the password in the chat.** It is safer to grant a narrow rule: the owner creates a file in `/etc/sudoers.d/` once, allowing **only these two commands** without a password. The rule is removed afterwards. The exact text of the rule will be prepared for approval.

## 11. Licences and publication

We publish only measurements and conclusions; the documents are not published or sold (owner's decision). Datasets marked non-commercial (EPHOIE, FUNSD, possibly XFUND) are used like the others. The report states the source and licence of each dataset, as attribution requires.

---

## Changes against v1

- Our own synthetic set of Serbian/Montenegrin invoices was dropped. Only open-source data is used.
- Languages became the main axis (RQ3): 12+ languages, including ZH/JA/KO.
- Document types extended: statements, financial reports, e-invoices with line items.
- Missing fields are tested on real documents: natural absence and masking by coordinates.
- The owner's real documents are not used.
- Timeline, sudo and compatibility with other uses of the Mac clarified.
- v2.2: «prepare everything → one start → results» mode; pre-registration of the selection rules; an automatic pipeline with self-protection; a reusable framework.
- v2.1: the cloud reference was dropped; XML rendering only as a fallback; the main missing-field test is questions about what is not in the document, masking in addition; runs go continuously, not only at night; NC datasets are allowed.

## Sources (checked 2026-11-10)

**Research:**
- ExtractBench — https://arxiv.org/html/2607.29677
- UniKIE-Bench — https://arxiv.org/html/2602.07038v1
- ReceiptBench — https://arxiv.org/html/2605.22413
- Electricity invoices — https://arxiv.org/html/2604.25927
- Abstention as prompt artifact — https://aclanthology.org/2026.emnlp-main.549/
- VAREX — https://arxiv.org/pdf/2603.15118
- RealDocBench — https://arxiv.org/pdf/2606.07401
- DocAttriBench — https://arxiv.org/pdf/2609.20574
- CFMME — https://arxiv.org/pdf/2605.29462

**Data:**
- DocILE — https://github.com/rossumai/docile
- FATURA — https://arxiv.org/pdf/2311.11856
- CORD — https://github.com/clovaai/cord
- ZUGFeRD corpus — https://github.com/ZUGFeRD/corpus
- FatturaPA examples — https://www.fatturapa.gov.it/en/lafatturapa/esempi/
- FatturaPA format and XSLT — https://www.fatturapa.gov.it/en/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/
- KSeF FA(3) examples — https://mavitconsulting.com/en/ksef-test/factures-exemples
- Peppol test invoices — https://www.efacturatieontcijferd.be/en/test-invoices/
- EU e-invoice examples — https://github.com/peculiar-systems/invoicein-examples
- SCID — https://davar-lab.github.io/dataset/scid.html
- KORIE — https://github.com/MahmoudSalah/KORIE
- XFUND — https://aclanthology.org/2022.findings-acl.253/
- InvoicesReceiptsPT — https://huggingface.co/datasets/Francisco-Cruz/InvoicesReceiptsPT
- synthetic-receipts-ocr — https://huggingface.co/datasets/albertobarnabo/synthetic-receipts-ocr
- CORU — https://github.com/Update-For-Integrated-Business-AI/CORU
- Japanese Mobile Receipt OCR 1.3K — https://www.techrxiv.org/doi/full/10.36227/techrxiv.175616889.90325672/v1
- Kleister-Charity — https://arxiv.org/abs/2105.05796
- FinTabNet — https://huggingface.co/datasets/bsmock/FinTabNet.c
- Bank-Statement-Intelligence — https://github.com/praneeth-hari/Bank-Statement-Intelligence
- stmtflow — https://github.com/tiwaker9404/stmtflow
- Invoice-to-Json — https://huggingface.co/datasets/shubh303/Invoice-to-Json
- parsee-ai invoices — https://huggingface.co/datasets/parsee-ai/invoices-example

**Models and tools:**
- lift — https://github.com/datalab-to/lift
- NuExtract — https://github.com/numindai/nuextract
- Gemma 4 — https://ai.google.dev/gemma/docs/core/model_card_4
- Qwen3.6 — https://huggingface.co/Qwen/Qwen3.6-27B
- mlx-vlm — https://pypi.org/project/mlx-vlm/
- FideNubi calculator — https://fidenubi.com/blog/what-llm-can-mac-mini-run/
