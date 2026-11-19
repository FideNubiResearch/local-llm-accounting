# s2__qwen3vl-8b__q8

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-8bit",
 "revision": "a0093b9b5fda6f76ddd4a462c6830ae7c4fe47ec",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__qwen3vl-8b__q8",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.78,
 "load_peak_gb": 9.856,
 "finished_at": "2026-11-16 07:12:21"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| invoice        |     16 |      157 |       0.981 |       2 |        1 |       9 |          0 |       0.885 |            1 |         35.1 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |          1 |       0.793 |            1 |         14.2 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| invoice        |     16 |      157 |       0.981 |       2 |        1 |       9 |          0 |       0.885 |            1 |         35.1 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |          1 |       0.793 |            1 |         14.2 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       0.909 |       1 |        0 |       1 |          0 |       0.727 |            1 |         36.7 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |        nan |       0.7   |            1 |         60.9 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       0.667 |            1 |         12.8 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| en     | invoice        | generated |      5 |       41 |       0.976 |       0 |        1 |       4 |          0 |       1     |            1 |         30.8 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         31.3 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |         12.9 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |          1 |       1     |            1 |         20.6 |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         35.6 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         34.6 |
| fr     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       0.727 |            1 |         32.8 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       0.667 |            1 |         14.6 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         17.9 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         39.3 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       0.625 |            1 |         13.1 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         19.4 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         37.5 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         39.3 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         38   |
| pt     | invoice        | real      |      1 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         29.7 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.3 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25.3 |
| invoice        | buyer_name      |     14 |       14 |       0.929 |       1 |        0 |       0 |        nan |       1     |            1 |         36.1 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         36.7 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         36.7 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         36.1 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         35.1 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         35.1 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         32.8 |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         36.7 |
| invoice        | seller_name     |     15 |       14 |       0.929 |       0 |        1 |       1 |          0 |       1     |            1 |         35.6 |
| invoice        | seller_vat_id   |     13 |       13 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         36.6 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       0.6   |            1 |         35.1 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.6   |            1 |         35.6 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.6   |            1 |         35.6 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.1 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.5 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.1 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.6 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.1 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       0.5   |            1 |         13.5 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       0.455 |            1 |         13.8 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.1 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.5   |            1 |         13.5 |
