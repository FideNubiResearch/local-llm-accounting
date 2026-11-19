# s2__qwen3vl-8b__P0b

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P0b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__qwen3vl-8b__P0b",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.92,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-16 05:59:51"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| invoice        |     16 |      157 |       0.987 |       2 |        0 |       9 |      0.111 |       0.861 |            1 |         27.7 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       0.828 |            1 |          9.9 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| invoice        |     16 |      157 |       0.987 |       2 |        0 |       9 |      0.111 |       0.861 |            1 |         27.7 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       0.828 |            1 |          9.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       0.727 |            1 |         28.3 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |     nan    |       0.7   |            1 |         51.3 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |       1    |       0.667 |            1 |          8.7 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         20.2 |
| en     | invoice        | generated |      5 |       41 |       1     |       0 |        0 |       4 |       0.25 |       1     |            1 |         23.9 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         24   |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |          9.3 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |       1    |       1     |            1 |         15.9 |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       0.727 |            1 |         27.9 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |       0    |       1     |            1 |         27.5 |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |     nan    |       0.727 |            1 |         25   |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |       1    |       0.833 |            1 |         10.4 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         14.4 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         30.1 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |       1    |       0.625 |            1 |          9.1 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         15   |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       0.727 |            1 |         29.1 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       0.75  |            1 |         30.1 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       0.75  |            1 |         29.5 |
| pt     | invoice        | real      |      1 |        5 |       1     |       0 |        0 |       0 |     nan    |       0.8   |            1 |         23.4 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.2 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.1 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         28.5 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.5 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         28.1 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         27.7 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         27.7 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         25   |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         28.6 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       0.929 |            1 |         27.9 |
| invoice        | seller_vat_id   |     13 |       13 |       0.923 |       1 |        0 |       0 |        nan |       1     |            1 |         28.3 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          1 |       0.562 |            1 |         27.7 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.533 |            1 |         27.9 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.533 |            1 |         27.9 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.1 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.3 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.1 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.4 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.1 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       0.583 |            1 |          9.3 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       0.545 |            1 |          9.5 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.1 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.583 |            1 |          9.3 |
