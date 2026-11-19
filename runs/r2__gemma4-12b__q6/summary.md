# r2__gemma4-12b__q6

```
{
 "model": "mlx-community/gemma-4-12B-it-6bit",
 "revision": "2fe53aeb9b8686eefa543a60d6aa364c5b219aac",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__gemma4-12b__q6",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 5.85,
 "load_peak_gb": 9.731,
 "finished_at": "2026-11-17 13:39:38"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       0.769 |            1 |         29   |
| invoice        |    216 |     2145 |       0.977 |      36 |       13 |     129 |      0.039 |       0.832 |            1 |         38.4 |
| receipt        |    180 |     1051 |       0.99  |      10 |        0 |     159 |      0.019 |       0.998 |            1 |         26.5 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       0.769 |            1 |         29   |
| invoice        |    215 |     2133 |       0.977 |      35 |       13 |     129 |      0.039 |       0.832 |            1 |         38.4 |
| receipt        |    178 |     1041 |       0.992 |       8 |        0 |     158 |      0.019 |       0.998 |            1 |         26.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      10 |      0     |       0.798 |            1 |         38.1 |
| de     | invoice        | real      |     16 |      158 |       0.975 |       1 |        3 |      10 |      0.1   |       1     |            1 |         52   |
| de     | receipt        | generated |     36 |      268 |       0.996 |       1 |        0 |      44 |      0     |       1     |            1 |         26.6 |
| en     | bank_statement | generated |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       0.769 |            1 |         29   |
| en     | invoice        | generated |     61 |      477 |       0.979 |       4 |        6 |      46 |      0.043 |       0.875 |            1 |         34.7 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         38.2 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0     |       1     |            1 |         26   |
| en     | receipt        | real      |     36 |      101 |       0.97  |       3 |        0 |      15 |      0.133 |       1     |            1 |         26.8 |
| es     | invoice        | generated |     18 |      203 |       0.99  |       2 |        0 |      11 |      0     |       0.754 |            1 |         38.8 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.864 |            1 |         39.6 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         39.5 |
| fr     | receipt        | generated |     36 |      270 |       1     |       0 |        0 |      42 |      0.024 |       1     |            1 |         26.8 |
| id     | receipt        | real      |     17 |       39 |       0.872 |       5 |        0 |       5 |      0     |       0.949 |            1 |         24   |
| it     | invoice        | generated |     18 |      208 |       0.981 |       4 |        0 |       7 |      0     |       0.74  |            1 |         40.4 |
| it     | receipt        | generated |     36 |      270 |       1     |       0 |        0 |      42 |      0     |       1     |            1 |         26.6 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       1     |            1 |         27.3 |
| nl     | invoice        | generated |     18 |      204 |       0.98  |       4 |        0 |       9 |      0     |       0.794 |            1 |         38.9 |
| pl     | invoice        | generated |     18 |      197 |       0.985 |       3 |        0 |      16 |      0     |       0.766 |            1 |         40.3 |
| pt     | invoice        | generated |     18 |      205 |       0.98  |       3 |        1 |      11 |      0     |       0.799 |            1 |         38.8 |
| pt     | invoice        | real      |     12 |       77 |       0.818 |      11 |        3 |       3 |      0.667 |       0.947 |            1 |         34.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29   |
| bank_statement | account_number  |      4 |        4 |       0.75  |       1 |        0 |       0 |    nan     |       1     |            1 |         29   |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29   |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         28.4 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29   |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         28.4 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         39.1 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         39.1 |
| invoice        | buyer_name      |    190 |      189 |       0.974 |       5 |        0 |       1 |      0     |       1     |            1 |         38.8 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.962 |       1 |        3 |      59 |      0     |       1     |            1 |         38.8 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         39.1 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0     |       1     |            1 |         38.7 |
| invoice        | invoice_number  |    215 |      209 |       0.986 |       3 |        0 |       6 |      0.167 |       1     |            1 |         38.4 |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0     |       1     |            1 |         38.4 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.333 |       1     |            1 |         48.7 |
| invoice        | seller_iban     |    165 |      154 |       0.922 |       3 |        9 |      11 |      0     |       1     |            1 |         39   |
| invoice        | seller_name     |    203 |      190 |       0.953 |       8 |        1 |      13 |      0.077 |       0.974 |            1 |         38.7 |
| invoice        | seller_vat_id   |    178 |      176 |       0.938 |      11 |        0 |       2 |      0.5   |       1     |            1 |         38.9 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      0.333 |       0.408 |            1 |         38.6 |
| invoice        | total_net       |    196 |      196 |       0.99  |       2 |        0 |       0 |    nan     |       0.378 |            1 |         38.8 |
| invoice        | total_tax       |    188 |      188 |       0.995 |       1 |        0 |       0 |    nan     |       0.41  |            1 |         38.6 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         26.6 |
| receipt        | date            |    148 |      143 |       1     |       0 |        0 |       5 |      0     |       1     |            1 |         26.6 |
| receipt        | merchant_name   |    146 |      145 |       0.979 |       3 |        0 |       1 |      0     |       1     |            1 |         26.7 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0     |       1     |            1 |         26.6 |
| receipt        | payment_method  |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         26.6 |
| receipt        | subtotal        |    151 |       37 |       0.946 |       2 |        0 |     114 |      0.026 |       0.975 |            1 |         26.5 |
| receipt        | tax_amount      |    119 |      113 |       0.991 |       1 |        0 |       6 |      0     |       1     |            1 |         26.2 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         26.6 |
| receipt        | total           |    160 |      160 |       0.981 |       3 |        0 |       0 |    nan     |       0.994 |            1 |         26.5 |
