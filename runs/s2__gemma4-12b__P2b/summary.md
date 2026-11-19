# s2__gemma4-12b__P2b

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P2b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__gemma4-12b__P2b",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.18,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-15 19:34:04"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         42.2 |
| invoice        |     16 |      157 |       0.949 |       5 |        3 |       9 |          0 |       0.922 |            1 |         59.2 |
| receipt        |     15 |       77 |       0.987 |       0 |        1 |      10 |          0 |       1     |            1 |         38.9 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         42.2 |
| invoice        |     16 |      157 |       0.949 |       5 |        3 |       9 |          0 |       0.922 |            1 |         59.2 |
| receipt        |     15 |       77 |       0.987 |       0 |        1 |      10 |          0 |       1     |            1 |         38.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         59.3 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       0 |        1 |       0 |        nan |       1     |            1 |         78.9 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         39.8 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         42.2 |
| en     | invoice        | generated |      5 |       41 |       0.951 |       1 |        1 |       4 |          0 |       1     |            1 |         56.5 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         59.6 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         38.4 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       0 |        1 |       2 |          0 |       1     |            1 |         39.8 |
| es     | invoice        | generated |      1 |       11 |       0.909 |       1 |        0 |       1 |          0 |       0.727 |            1 |         57.7 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         56   |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |        nan |       1     |            1 |         64.9 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         40.4 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         36.2 |
| it     | invoice        | generated |      1 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.75  |            1 |         64.9 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         38.7 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         41.3 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         62   |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         64.6 |
| pt     | invoice        | generated |      1 |       12 |       0.917 |       1 |        0 |       0 |        nan |       1     |            1 |         62.7 |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       0 |        1 |       0 |        nan |       1     |            1 |         51.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         42.2 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         42.2 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         42.2 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0     |            1 |         42.2 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         42.2 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0     |            1 |         42.2 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         41.9 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         41.9 |
| invoice        | buyer_name      |     14 |       14 |       0.929 |       1 |        0 |       0 |        nan |       1     |            1 |         59.4 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         60.7 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         60.8 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         59.2 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         59.2 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         59.2 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         64.9 |
| invoice        | seller_iban     |     11 |       10 |       0.6   |       2 |        2 |       1 |          0 |       1     |            1 |         59.6 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         59.3 |
| invoice        | seller_vat_id   |     13 |       13 |       0.769 |       2 |        1 |       0 |        nan |       1     |            1 |         59.6 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       0.733 |            1 |         59.2 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.733 |            1 |         59.3 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.733 |            1 |         59.3 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         39.3 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         39.8 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         39.7 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         40   |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         39.3 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          0 |       1     |            1 |         38.5 |
| receipt        | tax_amount      |     11 |       11 |       0.909 |       0 |        1 |       0 |        nan |       1     |            1 |         38.6 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         38.9 |
| receipt        | total           |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         39.3 |
