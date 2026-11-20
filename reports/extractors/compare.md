# Extractors vs. VLMs on the same 400 documents

Metrics as in harness/prompt_compare.py (main fields, payment_method excluded). Paired tests are descriptive: a separate "extractors" family, Holm correction over the pairs on this page; not part of the round-2 family.

## 1. Overview

| Configuration | F1, % | Correct values, % | Invented, % | Invented excl. receipt subtotal, % | Error-free docs, % | JSON, % | s/doc (median) | Hours per 400 | Peak, GB |
|---|---|---|---|---|---|---|---|---|---|
| gemma4-12b q6 | 98.1 | 98.1 | 2.8 | 2.9 | 86.0 | 100.0 | 32.4 | 3.7 | 12.6 |
| qwen3.5-9b q6 | 96.9 | 98.8 | 45.5 | 9.8 | 61.8 | 100.0 | 21.5 | 2.8 | 10.2 |
| qwen3.5-4b q6 | 96.3 | 98.1 | 43.4 | 9.8 | 62.3 | 100.0 | 12.3 | 1.6 | 6.2 |
| NuExtract3 4B q6 | 96.0 | 97.7 | 43.4 | 9.2 | 60.2 | 100.0 | 11.0 | 1.4 | 6.1 |
| lift 9B q6 (schema) | 95.4 | 95.7 | 34.0 | 1.7 | 59.5 | 96.8 | 23.2 | 2.8 | 10.3 |

## 2. Paired comparison over all main keys

Better = wrong in the configuration right of "vs" and right in the extractor on the left.

| Comparison | Keys | Better | Worse | Net | p | p (Holm) |
|---|---|---|---|---|---|---|
| NuExtract3 4B q6 vs gemma4-12b q6 | 3391 | 50 | 178 | -128 | 4.98e-18 | 1.49e-17 |
| NuExtract3 4B q6 vs qwen3.5-4b q6 | 3391 | 37 | 50 | -13 | 0.198 | 0.198 |
| lift 9B q6 (schema) vs gemma4-12b q6 | 3391 | 43 | 206 | -163 | 1.06e-26 | 4.26e-26 |
| lift 9B q6 (schema) vs qwen3.5-4b q6 | 3391 | 69 | 117 | -48 | 0.000533 | 0.00107 |

## 3. Paired comparison over keys whose answer is null (invented values)

Better = wrong in the configuration right of "vs" and right in the extractor on the left.

| Comparison | Keys | Better | Worse | Net | p | p (Holm) |
|---|---|---|---|---|---|---|
| NuExtract3 4B q6 vs gemma4-12b q6 | 288 | 2 | 119 | -117 | 5.55e-33 | 2.22e-32 |
| NuExtract3 4B q6 vs qwen3.5-4b q6 | 288 | 11 | 11 | 0 | 1 | 1 |
| lift 9B q6 (schema) vs gemma4-12b q6 | 288 | 4 | 94 | -90 | 2.38e-23 | 7.14e-23 |
| lift 9B q6 (schema) vs qwen3.5-4b q6 | 288 | 32 | 5 | 27 | 7.43e-06 | 1.49e-05 |

## 4. Real and generated documents

**gemma4-12b q6**

| Kind | Docs | Values | Correct, % | 95 % interval | F1, % | Invented, % |
|---|---|---|---|---|---|---|
| generated | 307 | 2668 | 98.9 | 98.4–99.2 | 98.9 | 1.2 |
| real | 93 | 435 | 93.1 | 90.3–95.1 | 93.2 | 15.2 |

**qwen3.5-9b q6**

| Kind | Docs | Values | Correct, % | 95 % interval | F1, % | Invented, % |
|---|---|---|---|---|---|---|
| generated | 307 | 2668 | 99.8 | 99.6–99.9 | 97.6 | 48.2 |
| real | 93 | 435 | 92.6 | 89.8–94.7 | 92.4 | 24.2 |

**qwen3.5-4b q6**

| Kind | Docs | Values | Correct, % | 95 % interval | F1, % | Invented, % |
|---|---|---|---|---|---|---|
| generated | 307 | 2668 | 98.9 | 98.4–99.2 | 96.8 | 46.7 |
| real | 93 | 435 | 93.3 | 90.6–95.3 | 93.3 | 18.2 |

**NuExtract3 4B q6**

| Kind | Docs | Values | Correct, % | 95 % interval | F1, % | Invented, % |
|---|---|---|---|---|---|---|
| generated | 307 | 2668 | 98.4 | 97.9–98.8 | 96.4 | 47.1 |
| real | 93 | 435 | 93.3 | 90.6–95.3 | 93.5 | 15.2 |

**lift 9B q6 (schema)**

| Kind | Docs | Values | Correct, % | 95 % interval | F1, % | Invented, % |
|---|---|---|---|---|---|---|
| generated | 307 | 2668 | 97.1 | 96.4–97.7 | 96.1 | 36.5 |
| real | 93 | 435 | 87.1 | 83.7–90.0 | 90.7 | 15.2 |

## 5. By document type

**gemma4-12b q6**

| Type | Docs | Values | Correct, % | F1, % | Invented, % |
|---|---|---|---|---|---|
| bank_statement | 4 | 26 | 96.2 | 96.2 | — |
| invoice | 216 | 2145 | 97.7 | 97.9 | 3.9 |
| receipt | 180 | 932 | 98.9 | 98.8 | 1.9 |

**qwen3.5-9b q6**

| Type | Docs | Values | Correct, % | F1, % | Invented, % |
|---|---|---|---|---|---|
| bank_statement | 4 | 26 | 96.2 | 96.2 | — |
| invoice | 216 | 2145 | 98.8 | 98.6 | 10.1 |
| receipt | 180 | 932 | 98.9 | 93.0 | 74.2 |

**qwen3.5-4b q6**

| Type | Docs | Values | Correct, % | F1, % | Invented, % |
|---|---|---|---|---|---|
| bank_statement | 4 | 26 | 100.0 | 100.0 | — |
| invoice | 216 | 2145 | 98.4 | 98.3 | 8.5 |
| receipt | 180 | 932 | 97.4 | 91.9 | 71.7 |

**NuExtract3 4B q6**

| Type | Docs | Values | Correct, % | F1, % | Invented, % |
|---|---|---|---|---|---|
| bank_statement | 4 | 26 | 100.0 | 100.0 | — |
| invoice | 216 | 2145 | 97.9 | 98.1 | 5.4 |
| receipt | 180 | 932 | 97.1 | 91.3 | 74.2 |

**lift 9B q6 (schema)**

| Type | Docs | Values | Correct, % | F1, % | Invented, % |
|---|---|---|---|---|---|
| bank_statement | 4 | 26 | 92.3 | 92.3 | — |
| invoice | 216 | 2145 | 95.2 | 96.4 | 1.6 |
| receipt | 180 | 932 | 97.1 | 93.2 | 60.4 |
