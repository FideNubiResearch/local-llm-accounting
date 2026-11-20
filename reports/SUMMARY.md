# Summary: local models for extracting fields from accounting documents on a 16 GB Mac mini

As of 2026-11-20. Details and tables: `reports/r1_vs_r1b`, `reports/round2`, `reports/final`, `reports/extractors`,
`reports/energy`, `reports/invented/analysis.md`; rules: `protocol/preregistration.md`.

## Question

Can a small vision-language model running locally on a 16 GB Mac mini (Apple Silicon, MLX) read invoices, receipts
and bank statements and return their fields (seller, buyer, amounts, dates, tax numbers, IBAN, etc.) as JSON? How
accurate is it, how often does the model invent a value for a field that is not in the document, and what does it
cost in time, memory and energy?

## What was done

| Stage | Content |
|---|---|
| Data | 1572 documents (865 invoices, 699 receipts, 8 bank statements), 10 languages, 13 273 values and 1 199 fields whose answer is null. 305 real, 1267 generated. Ground truth checked: blind review and an audit of 200 pairs, no hidden errors found (≤ 1.9 %). |
| Round 1 | 6 models × 2 prompt versions (P1, P1b), all 1572 documents. P1b fixed the field definitions; finalists were chosen on P1b. |
| Round 2 | 3 finalists (qwen3.5-9b, gemma4-12b, qwen3vl-8b) × modes: prompt without the "null" rule, prompt with quotes, JSON-schema constrained decoding, 6- and 8-bit weights; 400 documents; rules and tests fixed before the runs. |
| Final | Best round-2 configuration (gemma4-12b, 6-bit) and qwen3.5-4b (6-bit) on all 1572 documents. |
| Extra tracks | Qwen3.8 27B (3-bit), extractors NuExtract3 4B and lift 9B, energy per document. |

## Main results

1. **Best configuration: gemma4-12b at 6 bits.** On all documents: F1 98.4 %, correct values 98.3 %, invented
   1.4 %, documents without a single error 88.4 % (4-bit: 95.9 %, 95.4 %, 1.3 %, 70.4 %). Cost: 34 s per document,
   peak memory 12.6 GB — right at the GPU limit of a 16 GB machine.
2. **A model twice as fast holds up on values but not on "null".** qwen3.5-4b at 6 bits: 16.8 s/doc, 6.2 GB,
   correct values 98.0 % (gemma 98.3 %), but F1 96.1 % and documents without errors 57.8 % because of invented
   values (see item 4).
3. **What helped and what did not** (round 2, paired tests with Holm correction):
   - 6/8-bit instead of 4-bit weights helps: qwen3.5-9b q6/q8, gemma4-12b q6, qwen3vl-8b q8 beat their base;
   - the prompt with quotes (P2b) does not help: gemma4-12b is worse (−28 keys), the others show no difference, and
     time grows 1.5–2×;
   - removing the general "no field → null" rule (P0b): no difference;
   - strict JSON-schema decoding (constrained): no difference in accuracy, gives 100 % strict JSON;
   - prompt/decoding modes were changed one factor at a time against the same model's base; interactions were not
     studied.
4. **Invented values depend on the model and on one field.** Qwen models invent up to 45–52 % of null fields; 92 %
   of those are a receipt `subtotal` that is not on the page (the model copies or computes it). Without `subtotal`,
   qwen3.5-4b q6 invents 6.0 %, gemma 0.7 %. The apparent "language effect" in invented values (de/fr/it vs
   es/nl/pl/pt) is an artefact: receipts exist only in the former. Details: `reports/invented/analysis.md`.
5. **Does not fit in memory:** gemma4-12b at 8 bits (weights 12.1 GB against a GPU limit of ~12.1 GB): Metal OOM on
   every document. The first run caused a kernel panic (watchdog) on this machine; a guard was added
   (`harness/memguard.py`).
6. **Qwen3.8 27B (3-bit, 12.0 GB) is not suitable for a 16 GB Mac mini.** With the default GPU limit the guard
   stopped the smoke run because of swap (+2.06 GB); with the limit raised to 14 GB the peak was 14.7 GB and every
   document failed with Metal OOM (see the amendments in `protocol/preregistration.md`).
7. **Specialised extractors are not better than general VLMs** (400 documents, 6-bit, `reports/extractors/compare.md`):

   | | F1, % | Correct values, % | Invented excl. subtotal, % | s/doc | Peak, GB |
   |---|---|---|---|---|---|
   | gemma4-12b q6 | 98.1 | 98.1 | 2.9 | 32.4 | 12.6 |
   | qwen3.5-4b q6 | 96.3 | 98.1 | 9.8 | 12.3 | 6.2 |
   | NuExtract3 4B q6 | 96.0 | 97.7 | 9.2 | 11.0 | 6.1 |
   | lift 9B q6 (schema) | 95.4 | 95.7 | 1.7 | 23.2 | 10.3 |

   NuExtract3 ≈ qwen3.5-4b in accuracy and speed (difference not significant, p = 0.2) and worse than gemma
   (−128 keys, p < 10⁻¹⁷). lift 9B is less accurate than both (−163 and −48 keys, especially on real documents:
   87.1 % vs 93 %), but invents almost nothing except receipt `subtotal`. One run per configuration; the extractor
   settings were fixed before the runs; the NuExtract3 prompt adapter is ours, other settings might do better.
8. **Energy** (`reports/energy/energy.md`, powermetrics, CPU+GPU+ANE, 33 documents): the GPU is fully loaded while
   working, power is ≈ 15 W for every model, so energy is proportional to time. Per 1000 documents: gemma4-12b q6
   ≈ 131 Wh, lift 9B ≈ 100, qwen3.5-4b q6 ≈ 59, NuExtract3 ≈ 53 (SoC idle 0.09 W). Wall power (the whole Mac mini)
   was not measured.

## Limitations (important when reading the numbers)

- **Only 305 of 1572 documents are real.** Conclusions are weaker there: the gain of gemma q6 on real documents is
  smaller (92.5 → 94.4 % correct values) and it invents more (0 → 8 keys out of 133 null keys). Numbers on
  generated documents are higher (≈ 98.8 %), so the overall F1 overstates what to expect on real bookkeeping.
- **The data is not independent of the selection.** Finalists were chosen on r1b over the whole set, modes were
  compared on 400 documents, and the best configuration was then run on the same 1572. Final numbers may be
  optimistic.
- **One run per configuration** (temperature 0); run-to-run variation was not measured.
- **Policy for computed fields:** a computed value counts as invented if the prompt explicitly forbade it. P1b
  forbids a `subtotal` without a printed line, so the Qwen `subtotal` values break an instruction. In round 1 (P1)
  there was no such rule.
- **Language is confounded with source and type** (it, es, nl, pl are generated only); language comparisons are
  exploratory.
- One platform and stack (16 GB Mac mini, mlx-vlm 0.7.10); memory and time will differ on other hardware.

## Not covered

- Wall power (the whole Mac mini, not only the SoC); run-to-run variation.

## What it means in practice

For field extraction on a 16 GB Mac mini, gemma4-12b at 6 bits is the sensible choice when accuracy and an honest
null matter; qwen3.5-4b at 6 bits when speed matters and computed fields such as `subtotal` can be handled. For
receipts without a printed `subtotal`, Qwen models need post-processing or an application-side rule.
