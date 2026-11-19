# r2__qwen3vl-8b__q8

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-8bit",
 "revision": "a0093b9b5fda6f76ddd4a462c6830ae7c4fe47ec",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3vl-8b__q8",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 5.01,
 "load_peak_gb": 9.856,
 "finished_at": "2026-11-18 03:41:45"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| invoice        |    216 |     2145 |       0.982 |      28 |       10 |     129 |      0.031 |       0.856 |            1 |         36.7 |
| receipt        |    180 |     1051 |       0.985 |      13 |        3 |     159 |      0.742 |       0.75  |            1 |         15   |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| invoice        |    215 |     2133 |       0.982 |      28 |       10 |     129 |      0.031 |       0.855 |            1 |         36.7 |
| receipt        |    178 |     1041 |       0.987 |      11 |        3 |     158 |      0.741 |       0.75  |            1 |         14.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.995 |       0 |        1 |      10 |      0     |       0.842 |            1 |         36.7 |
| de     | invoice        | real      |     16 |      158 |       0.968 |       4 |        1 |      10 |      0.2   |       0.698 |            1 |         52.8 |
| de     | receipt        | generated |     36 |      268 |       0.981 |       5 |        0 |      44 |      0.841 |       0.685 |            1 |         14.4 |
| en     | bank_statement | generated |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| en     | invoice        | generated |     61 |      477 |       0.996 |       1 |        1 |      46 |      0.043 |       0.975 |            1 |         31.5 |
| en     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         14.5 |
| en     | receipt        | real      |     36 |      101 |       0.95  |       4 |        1 |      15 |      0.333 |       0.981 |            1 |         17.6 |
| es     | invoice        | generated |     18 |      203 |       0.985 |       2 |        1 |      11 |      0     |       0.827 |            1 |         36.9 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.876 |            1 |         37.7 |
| fr     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       0.727 |            1 |         33.6 |
| fr     | receipt        | generated |     36 |      270 |       0.989 |       2 |        1 |      42 |      0.857 |       0.689 |            1 |         14.6 |
| id     | receipt        | real      |     17 |       39 |       1     |       0 |        0 |       5 |      0.2   |       1     |            1 |         16.7 |
| it     | invoice        | generated |     18 |      208 |       0.995 |       1 |        0 |       7 |      0     |       0.841 |            1 |         38.2 |
| it     | receipt        | generated |     36 |      270 |       0.993 |       2 |        0 |      42 |      0.905 |       0.682 |            1 |         14.6 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       0 |        1 |       0 |    nan     |       1     |            1 |         19.4 |
| nl     | invoice        | generated |     18 |      204 |       0.995 |       0 |        1 |       9 |      0     |       0.941 |            1 |         37   |
| pl     | invoice        | generated |     18 |      197 |       0.99  |       2 |        0 |      16 |      0     |       0.741 |            1 |         38   |
| pt     | invoice        | generated |     18 |      205 |       0.99  |       2 |        0 |      11 |      0     |       0.78  |            1 |         37.4 |
| pt     | invoice        | real      |     12 |       77 |       0.74  |      15 |        5 |       3 |      0     |       0.806 |            1 |         31.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.6 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.8 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         25.6 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         39.4 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         39.4 |
| invoice        | buyer_name      |    190 |      189 |       0.989 |       2 |        0 |       1 |      0     |       1     |            1 |         36.9 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.952 |       2 |        3 |      59 |      0     |       1     |            1 |         36.9 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         37.1 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       1     |            1 |         36.9 |
| invoice        | invoice_number  |    215 |      209 |       0.962 |       7 |        1 |       6 |      0     |       1     |            1 |         36.7 |
| invoice        | issue_date      |    216 |      211 |       0.991 |       2 |        0 |       5 |      0     |       1     |            1 |         36.7 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.667 |       1     |            1 |         47   |
| invoice        | seller_iban     |    165 |      154 |       0.961 |       2 |        4 |      11 |      0     |       1     |            1 |         37.1 |
| invoice        | seller_name     |    203 |      190 |       0.958 |       7 |        1 |      13 |      0.077 |       0.989 |            1 |         36.8 |
| invoice        | seller_vat_id   |    178 |      176 |       0.972 |       4 |        1 |       2 |      0     |       1     |            1 |         37   |
| invoice        | total_gross     |    208 |      205 |       0.995 |       1 |        0 |       3 |      0     |       0.478 |            1 |         36.7 |
| invoice        | total_net       |    196 |      196 |       0.995 |       1 |        0 |       0 |    nan     |       0.485 |            1 |         36.9 |
| invoice        | total_tax       |    188 |      188 |       1     |       0 |        0 |       0 |    nan     |       0.473 |            1 |         36.7 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.5 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.2   |       1     |            1 |         14.8 |
| receipt        | merchant_name   |    146 |      145 |       0.993 |       1 |        0 |       1 |      1     |       1     |            1 |         14.8 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.1   |       1     |            1 |         14.6 |
| receipt        | payment_method  |    119 |      119 |       0.983 |       1 |        1 |       0 |    nan     |       1     |            1 |         14.5 |
| receipt        | subtotal        |    151 |       37 |       1     |       0 |        0 |     114 |      0.991 |       0.28  |            1 |         14.7 |
| receipt        | tax_amount      |    119 |      113 |       0.973 |       1 |        2 |       6 |      0     |       0.324 |            1 |         14.8 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         14.6 |
| receipt        | total           |    160 |      160 |       0.95  |       8 |        0 |       0 |    nan     |       0.325 |            1 |         14.8 |
