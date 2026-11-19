# s2__gemma4-12b__constr

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "s2__gemma4-12b__constr",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.15,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-15 19:47:44"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         22.1 |
| invoice        |     16 |      157 |       0.955 |       4 |        3 |       9 |          0 |       0.844 |            1 |         28.6 |
| receipt        |     15 |       77 |       0.987 |       0 |        1 |      10 |          0 |       0.987 |            1 |         20.3 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         22.1 |
| invoice        |     16 |      157 |       0.955 |       4 |        3 |       9 |          0 |       0.844 |            1 |         28.6 |
| receipt        |     15 |       77 |       0.987 |       0 |        1 |      10 |          0 |       0.987 |            1 |         20.3 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         29.1 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       0 |        1 |       0 |        nan |       1     |            1 |         47.2 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         20.5 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         22.1 |
| en     | invoice        | generated |      5 |       41 |       0.976 |       0 |        1 |       4 |          0 |       0.85  |            1 |         26.4 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.1 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         20   |
| en     | receipt        | real      |      4 |       10 |       0.9   |       0 |        1 |       2 |          0 |       1     |            1 |         20.4 |
| es     | invoice        | generated |      1 |       11 |       0.909 |       1 |        0 |       1 |          0 |       0.727 |            1 |         28.2 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       0.7   |            1 |         27.4 |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |        nan |       1     |            1 |         29.9 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         20.8 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.6 |
| it     | invoice        | generated |      1 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.75  |            1 |         31.6 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         20.2 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       0.5   |            1 |         21.5 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         30.1 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         31.4 |
| pt     | invoice        | generated |      1 |       12 |       0.917 |       1 |        0 |       0 |        nan |       1     |            1 |         30.1 |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       0 |        1 |       0 |        nan |       1     |            1 |         22.8 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         22.1 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         22.1 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         22.1 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0     |            1 |         22.1 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         22.1 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0     |            1 |         22.1 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.8 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.8 |
| invoice        | buyer_name      |     14 |       14 |       0.929 |       1 |        0 |       0 |        nan |       1     |            1 |         29   |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         29.5 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         29.5 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         28.6 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         28.6 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.6 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         29.9 |
| invoice        | seller_iban     |     11 |       10 |       0.6   |       2 |        2 |       1 |          0 |       1     |            1 |         29.1 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         29   |
| invoice        | seller_vat_id   |     13 |       13 |       0.846 |       1 |        1 |       0 |        nan |       1     |            1 |         29.1 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       0.467 |            1 |         28.6 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.467 |            1 |         29   |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.467 |            1 |         29   |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.4 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.5 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.5 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.7 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.4 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          0 |       1     |            1 |         20   |
| receipt        | tax_amount      |     11 |       11 |       0.909 |       0 |        1 |       0 |        nan |       1     |            1 |         20   |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.3 |
| receipt        | total           |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       0.917 |            1 |         20.4 |
