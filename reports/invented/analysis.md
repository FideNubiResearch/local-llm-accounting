# Invented values in the final run: where they come from

2026-11-19. Data: `reports/rescore_final` (gemma4-12b q6, qwen3.5-4b q6, 1572 documents) and `reports/rescore_r1b`
(4-bit, P1b). Invented = the correct answer is null and the model gave a value (outcome FF). Rate = FF / (FF + TN)
over keys whose answer is null, main fields. The analysis is descriptive and not part of the pre-registered family
of tests.

## 1. qwen3.5-4b: invented values are almost entirely one field

| Configuration | Invented, all keys | Excl. receipt `subtotal` | Receipt `subtotal` |
|---|---|---|---|
| qwen3.5-4b q6 | 538 / 1197 = 44.9 % | 41 / 683 = **6.0 %** | 497 / 514 |
| qwen3.5-4b 4-bit | 625 / 1197 = 52.2 % | 116 / 683 = 17.0 % | 509 / 514 |
| gemma4-12b q6 | 17 / 1197 = 1.4 % | 5 / 683 = 0.7 % | 12 / 514 |
| gemma4-12b 4-bit | 15 / 1197 = 1.3 % | 5 / 683 = 0.7 % | 10 / 514 |

- 497 of the 538 values invented by qwen3.5-4b q6 (92 %) are a receipt `subtotal` that is not on the page; 481 of
  them are in synthetic receipts (`synthetic_receipts`). All other fields together give 41.
- **The "language" effect (de/fr/it 66–75 % vs 0 % for es/nl/pl/pt) is a document-type artefact:** receipts exist
  only in de, fr, it, en, id, ko (160 each in de, fr, it), while es, nl, pl, pt contain only invoices, where
  `subtotal` is not asked. Invented-value rates cannot be compared across languages without accounting for
  document type.
- What the model writes instead of null (497 cases): a copy of the total — 165 (33 %); "total minus tax" — 120
  (24 %); another number — 134 (27 %); total/tax not parseable — 78 (16 %). So the model mostly **computes or
  guesses** the missing line, although P1b explicitly says "do not copy the total into the subtotal".
- 6 bits are better than 4: 17.0 % → 6.0 % excluding `subtotal`, but `subtotal` is still invented almost always.

**Policy (owner's decision, 2026-11-20):** a computed value is an invented value if the prompt explicitly
restricted it, and an acceptable inference if the prompt let the model understand that a computation was expected.
P1b (and P0b, P2b) says explicitly: subtotal "only if the receipt prints a subtotal line ... otherwise null. Do not
copy the total into the subtotal", and for invoices "never compute one from the other". So for all runs of round 2,
the final run and the extractors a computed `subtotal` is an invented value, as the scorer counts it; it is a
**violation of an explicit instruction**, not a debatable interpretation. P1 (round 1) had no such rule (only "never
guess, infer or invent"), so round-1 `subtotal` numbers should be read with care; the choice of finalists was made
on P1b and does not depend on this.

## 2. gemma4-12b q6 on real documents: invented values grow from 0 to 8

| | Null keys | Invented |
|---|---|---|
| 4-bit, real documents | 133 | 0 |
| q6, real documents | 133 | 8 (6.0 %) |
| q6, generated | 1064 | 9 (0.8 %); 4-bit: 15 (1.4 %) |

- The eight new invented values: receipt `subtotal` — 5 (en 3, id 2), invoice — 3 (`invoice_number`,
  `purchase_order`, `seller_vat_id`, one each). Paired test on real null keys: 8 worse, 0 better, exact sign test
  p = 0.0078 (no multiplicity correction: descriptive). The effect is real but small in absolute terms on 133 keys.
- The figure "66.7 % invented on real pt" in an earlier report is 2 invented values out of 3 null keys: noise.
- Value accuracy on real documents is higher for q6 than for 4-bit, but unevenly: pt 79.2 → 84.7,
  korie 92.1 → 98.4, zugferd 95.9 → 97.4, wildreceipt 97.5 → 98.7; lower for sroie 98.5 → 95.6 and
  cord 94.6 → 93.7 (63–736 values per source, wide intervals).
- Overall: on real documents q6 gives more correct values and slightly more invented values. Separating this from
  noise needs more real documents with null answers.

## 3. What to do

1. The `subtotal` policy is decided (see above): no rescoring needed.
2. When comparing invented values between models and languages, always show the rate with and without receipt
   `subtotal`.
3. Do not interpret "invented values by language" without a breakdown by document type.
