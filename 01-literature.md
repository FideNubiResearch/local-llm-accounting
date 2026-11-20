# Literature review (phase 0)

Checked: 2026-11-10. Goal: avoid repeating what has been done and confirm the gap.

## Closest work

| Work | Data | Models / hardware | What is measured | What is missing |
|---|---|---|---|---|
| **ExtractBench** — arXiv 2607.29677 | 370 business documents, 67 types, 8 domains | 14 systems: APIs, agents, open-weight (Qwen3.6 35B-A3B FP8, Gemma 4 26B, lift 9B, NuExtract3) on server GPUs | value-F1, null = missing key, a value for a null ground truth = hallucination; grounding | No breakdown by language; no quantisation; no consumer hardware |
| **UniKIE-Bench** — arXiv 2602.07038 | DocILE, SROIE, CORD, SIBR, EPHOIE, FUNSD etc. + synthetic | 15 LMMs; open 2–9B on 2×A100 (vLLM) | Field F1 exact match; faithfulness against OCR | Missing fields only in the error analysis; EN/ZH; not edge |
| **ReceiptBench** — arXiv 2605.22413 (ACL 2026) | 10 656 receipts, 98 % EN | GPT-5, Gemini-3-Pro, Qwen3-VL 4/8/32B, InternVL3, OCR models; SFT+GRPO | F1 with true negatives; FP as hallucinations | Almost English only; no degradations; no edge |
| **Electricity invoices** — arXiv 2604.25927 | IDSEM, Spanish invoices, 2400 | Gemini 1.5 Pro, Mistral-small (API) | P/R/F1; effect of temperature/top-p (≈0.6 points) | Cloud, text only, one language. Notes that Mistral "makes up" missing fields |
| **VAREX** — arXiv 2603.15118 | 1777 government forms, synthetic values, 4 input modalities | 20 models, focus ≤4B | Accuracy | Forms, not accounting; no hallucinations on empty fields. **Useful:** "schema echo" in models <4B (−45…65 points); layout-preserving text +3…18 points |
| **RealDocBench** — arXiv 2606.07401 | 581 real regulated documents, 1356 questions + layout | 18 systems | Per-field accuracy, cost, latency | No unanswerable questions; no languages; no edge |
| **DocAttriBench** — arXiv 2609.20574 | 237k documents, 296k QA | Grounding MLLMs | Answer and attribution accuracy | No abstention |
| **CFMME** — arXiv 2605.29462 | 6052 Chinese financial examples | LVLMs | QA accuracy, IE score | ZH only; no local hardware |
| **Abstention as prompt artifact** — EMNLP 2026 | — | LLMs | Refusal to answer depends strongly on the prompt | Not documents, not local models |
| **UNK-VQA** — arXiv 2310.10942 | VQA v2 + perturbations | MLLMs | Abstention | Ordinary photos, not documents |
| **lift / NuExtract3** (Datalab, 2026) | 225 documents, vendor benchmark | lift 9B, NuExtract3 4B and others | Field accuracy, latency | Vendor benchmark; no languages or hallucinations |

## Confirmed gap

1. **Multilinguality.** No work compares models on accounting documents in more than 2 languages (EN/ZH).
2. **Controlled missing fields.** A protocol of "asking about what is not in the document" and masking a value while
   keeping its label is not found for documents. No ready masked sets exist.
3. **Consumer Apple silicon with 16 GB.** Nowhere is accuracy measured together with time, memory and energy per
   document.
4. **Quantisation × hallucinations.** The effect of 4/6/8 bits on false fills has not been studied.
5. **Prompt × abstention on documents.** The EMNLP 2026 finding has not been tested on document extraction.

## What we take into the method

- Null following ExtractBench: a missing key = null; a value where the annotation is null = hallucination.
- F1 with true negatives (ReceiptBench), so that a correct `null` counts.
- The **schema echo** metric (VAREX): the model returns the schema or field labels instead of values.
- A **layout-preserving text** pipeline (VAREX) as a separate input variant.
- Temperature barely affects the result (Electricity invoices): we fix it at 0 and do not spend runs on sweeping it.
