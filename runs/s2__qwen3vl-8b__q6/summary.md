# s2__qwen3vl-8b__q6

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-6bit",
 "revision": "0b6a7d52ff9e393d9560e7b1e0fcd8ac40ba7b60",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__qwen3vl-8b__q6",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.99,
 "load_peak_gb": 7.809,
 "finished_at": "2026-11-16 06:49:13"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| invoice        |     16 |      157 |       0.975 |       3 |        1 |       9 |          0 |       0.885 |            1 |         32.1 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |          1 |       0.793 |            1 |         12.3 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| invoice        |     16 |      157 |       0.975 |       3 |        1 |       9 |          0 |       0.885 |            1 |         32.1 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |          1 |       0.793 |            1 |         12.3 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       0.909 |       1 |        0 |       1 |          0 |       0.727 |            1 |         33.4 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |        nan |       0.7   |            1 |         56.8 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       0.667 |            1 |         11.1 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| en     | invoice        | generated |      5 |       41 |       0.976 |       0 |        1 |       4 |          0 |       1     |            1 |         27.8 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         27.9 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |         11.3 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |          1 |       1     |            1 |         18.7 |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         32.5 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         31.7 |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |        nan |       0.727 |            1 |         29.2 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       0.667 |            1 |         12.8 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         16.7 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         35.4 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       0.625 |            1 |         11.3 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         17.6 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         33.9 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         35.4 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         34.3 |
| pt     | invoice        | real      |      1 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         27.5 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.6 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.5 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         23.5 |
| invoice        | buyer_name      |     14 |       14 |       0.929 |       1 |        0 |       0 |        nan |       1     |            1 |         32.9 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         33.3 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.3 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         32.9 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         32.1 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         32.1 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         29.2 |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         33.4 |
| invoice        | seller_name     |     15 |       14 |       0.929 |       0 |        1 |       1 |          0 |       1     |            1 |         32.5 |
| invoice        | seller_vat_id   |     13 |       13 |       0.923 |       1 |        0 |       0 |        nan |       1     |            1 |         33.3 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       0.6   |            1 |         32.1 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.6   |            1 |         32.5 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.6   |            1 |         32.5 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         11.4 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         11.7 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         11.5 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         11.8 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         11.4 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       0.5   |            1 |         11.7 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       0.455 |            1 |         12   |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         11.5 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.5   |            1 |         11.7 |
