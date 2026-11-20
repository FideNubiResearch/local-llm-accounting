# Round 2 — rules fixed before the runs

Written 2026-11-15, before the first round-2 run. Changes after the start only as a separate dated entry at the
bottom ("Amendments"), with the reason; results already obtained in round 2 are not used as an argument.

Basis: final v5 (1572 documents, answers sha256 cfac4f69…), the scorer at the commit that added this file
(normalize.RULES, including pay_class and the document-type code before a series), prompt P1b.

## 1. Finalists

By the rule of 00-plan.md, section 8.1 (top 3 by F1 of the main fields on P1b with JSON valid ≥ 90 %; on equal F1 to
3 digits, fewer invented values), applied to r1b (reports/r1_vs_r1b/compare.md). The selection was approved by the
owner on 2026-11-15.

| Model | 4-bit (base, r1b) | 6-bit | 8-bit |
|---|---|---|---|
| qwen3.5-9b | mlx-community/Qwen3.5-9B-4bit @ 8b2b98c0 | mlx-community/Qwen3.5-9B-6bit @ 76fe4065 | mlx-community/Qwen3.5-9B-8bit @ 16daa481 |
| gemma4-12b | mlx-community/gemma-4-12B-it-4bit @ 73bcf090 | mlx-community/gemma-4-12B-it-6bit @ 2fe53aeb | mlx-community/gemma-4-12B-it-8bit @ 200bb6db |
| qwen3vl-8b | mlx-community/Qwen3-VL-8B-Instruct-4bit @ defcdea7 | mlx-community/Qwen3-VL-8B-Instruct-6bit @ 0b6a7d52 | mlx-community/Qwen3-VL-8B-Instruct-8bit @ a0093b9b |

Settings as in r1/r1b: temperature 0, max_tokens 1024, Gemma max_soft_tokens 1120, Qwen with the checkpoint's
default image budget. GPU memory limit raised by the owner: `iogpu.wired_limit_mb = 14848` (valid until reboot;
checked before every queue start).

## 2. Sample

`protocol/samples/round2.txt` — 400 documents, sha256 `33a41f7b135c0e8d1faeea78d865b97e8035ae8a264a22f30d3da6788c48846f`,
`tools/make_sample.py --n 400 --seed 0`: all 41 masked documents + the rest stratified by
source × language × type × variant (proportional, at least 2 per group). Check before the runs: on r1b the F1 ranking
of the six models on the sample matches the full set (difference ≤ 0.5 points).

The base is the same 400 documents from the existing r1b runs (P1b, 4-bit); they are not re-run.

## 3. Modes (one factor at a time against the same model's base)

| Mode | What changes | Runs |
|---|---|---|
| P0b | prompt = P1b without the general rule "no field → null, do not guess" | 3 |
| P2b | prompt = P1b + a quote from the document for every value | 3 |
| constrained | P1b + strict JSON-schema decoding | 3 |
| q6 | P1b, 6-bit weights | 3 |
| q8 | P1b, 8-bit weights | 3 |
| Qwen3.8 27B | P1b, own quantisation from bf16 (`mlx-community/Qwen3.8-27B-bf16` @ 379e7084, Apache-2.0): 3-bit affine g64; if 3-bit does not fit without swap — mixed_2_6 | 1 (+1) |
| extractors | NuExtract3 4B, lift 9B (after a prompt adapter; a separate amendment with their settings before the runs) | 2 |

Every new configuration first passes a smoke run on `protocol/samples/smoke.txt` (33 documents).

## 4. Metrics

As in harness/prompt_compare.py. Main fields = all except payment_method (reported separately).
- Primary: F1 of the main fields (precision = TP/(TP+WV+FF), recall = TP/(TP+WV+FN)).
- Secondary: invented rate FF/(FF+TN), also excluding receipt subtotal; share of documents with all main fields
  right; JSON valid; seconds per document (median); peak memory; swap (runs/system.jsonl).

## 5. Comparison and decision

- Each mode is compared with the base of **the same model on the same keys** (doc, field): better = wrong in the
  base and right in the mode, worse = the reverse; exact sign test (McNemar).
- Multiplicity: Holm over all round-2 comparisons (mode × model), α = 0.05.
- A mode is "better than the base" for a model if better − worse > 0 and Holm p < 0.05. "Worse" symmetrically.
  Otherwise "no difference".
- Invented values are assessed separately with the same paired test over keys whose answer is null.
- Quantisation and 27B are also judged on cost: seconds per document and peak memory next to F1; "does not fit" is
  a result too (section 6).

**Best configuration** = the (model, mode) with the highest F1 on the sample among those not worse than their base;
with an F1 difference < 0.3 points — fewer invented values, then faster. It and qwen3.5-4b in the same mode (the
question "how much worse is a model twice as fast") are run on the whole final/ set — these are the study's final
numbers.

## 6. Stopping and skipping

- Smoke: JSON valid < 50 % or accuracy ≈ 0 on the first 20 documents → the configuration does not go to the main
  run; the reason is recorded (as in 00-plan.md 8.1).
- Memory: swap grows by more than 2 GB during the smoke run, or seconds per document > 4× the 4-bit version of the
  same model → the configuration is skipped and recorded as "not suitable for a 16 GB Mac mini".
- The model does not load / OOM → skipped with the reason.

## 7. Order

1. While Qwen3.8 27B downloads: smoke runs of the finalists' new configurations (`protocol/round2_smoke.json`, P0b,
   P2b, constrained, q6, q8 × 3; 6/8-bit weights are downloaded as the queue goes).
2. Qwen3.8 27B: quantise to 3 bits, smoke run. Depending on the result — decision on 27B in the main run (section 6).
3. Main runs on the sample, in the order of `protocol/round2.json`.
4. Round-2 report, best configuration → full set (+ qwen3.5-4b).

## Amendments

- 2026-11-16: `gemma4-12b q8` removed from the main run. Smoke `s2__gemma4-12b__q8`: all 33 documents failed with `Insufficient Memory` (Metal); the 12.1 GB of weights equal the GPU memory limit of a 16 GB Mac mini (section 6: "The model does not load / OOM → skipped with the reason"; verdict "not suitable for a 16 GB Mac mini"). The first run on 2026-11-15 ended in a kernel panic (watchdog, 20:39). The other 14 configurations passed smoke; the `hold` from the first run was removed.
- 2026-11-18: final run (section 5) — `protocol/round_final.json`. The best configuration by the rule of section 5 is
  gemma4-12b q6 (reports/round2/compare.md). "qwen3.5-4b in the same mode" = P1b, 6-bit:
  `mlx-community/Qwen3.5-4B-6bit` @ fbb1092a (qwen3_5, affine g64, 4.1 GB); a smoke run on 33 documents before the
  full run. GPU limit: `iogpu.wired_limit_mb = 0` (default) — the whole main r2 run used the same (the raised limit
  was reset by the reboot on 2026-11-15 20:39); the "before every start" check was done.
- 2026-11-19: Qwen3.8 27B (3-bit g64, 12.0 GB, own quantisation, `protocol/round2_27b.json`), smoke with the default GPU limit: the `harness.memguard` guard stopped the run, swap grew from 0.43 to 2.49 GB (> 2 GB, section 6), verdict "not suitable for a 16 GB Mac mini". Weights 12.0 GB against a 12.1 GB limit. The mixed_2_6 variant and a raised `iogpu.wired_limit_mb` (needs the owner's sudo) were not tested; the time estimate of ≈ 1 min/doc is a calculation.
- 2026-11-19: Qwen3.8 27B 3-bit again with `iogpu.wired_limit_mb=14000` (`s2__qwen3.8-27b__q3w14`): peak memory 14.7–14.8 GB, Metal OOM (`Insufficient Memory`) on each of the first 4 documents, run stopped manually. Verdict: not suitable for a 16 GB Mac mini (section 6). The mixed_2_6 variant was not tested (below 3 bits in precision, weights of about the same size).
- 2026-11-19: extractors (section 3), settings before the runs. 6-bit weights, as for the best configuration: `numind/NuExtract3-mlx-6bits` @ d0db1bdf (Apache-2.0, qwen3_5, 4B) and `mlx-community/lift-oQ6` @ 8fa369a9 (9B, ≈6-bit mixed oQ, licence AI PUBS OPEN RAIL-M modified: research use). GPU limit: `iogpu.wired_limit_mb=14000` (raised for the 27B test, reset only by reboot); the models peak at ≤ 10.3 GB, so it does not affect the results; the value is recorded here.
  - NuExtract3: prompt adapter `harness/run.py: nuextract_inputs` (`--nuextract`): a template of leaf types (dates `date`, time `time`, currency `currency`, amounts `number`, `payment_method` `string`, everything else `verbatim-string`) + `instructions` = the P1b rules without the schema header and without the line "Return only the JSON object"; structured mode, `enable_thinking=False` (the authors' recommendation: no reasoning), temperature 0, max_tokens 1024, no constrained decoding. List rows (line_items) are not asked, as for all other models.
  - lift 9B: prompt P1b + JSON-schema decoding (`constrained`), as the model card recommends (lift is built for schema-constrained extraction). Comparison base — "one configuration, no modes": compared with gemma4-12b q6 and qwen3.5-4b q6 on the same 400 documents (paired sign test, Holm over the "extractors" family, descriptive; not part of the round-2 family).
  - Order: smoke on 33 documents (`protocol/round2_extractors_smoke.json`, criteria of section 6), then 400 (`protocol/round2_extractors.json`).
- 2026-11-20: energy (section 3, plan 00-plan). `harness/energy.py`: `powermetrics` (cpu_power, gpu_power, ane_power, 1 s step) while running the 33 smoke documents (`protocol/samples/smoke.txt`) for gemma4-12b q6, qwen3.5-4b q6, NuExtract3 4B q6, lift 9B q6 (the same arguments as in the study; run_id `e__…`). Energy = power summed over the document-processing phase (model loading excluded); also "above idle" (60 s idle before the first run). SoC energy (CPU+GPU+ANE) is measured, not wall power. Answers of the energy runs are not scored.
