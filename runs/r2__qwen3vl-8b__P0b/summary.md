# r2__qwen3vl-8b__P0b

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P0b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3vl-8b__P0b",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.03,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-17 15:57:10"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| invoice        |    216 |     2145 |       0.978 |      43 |        4 |     129 |      0.093 |       0.853 |            1 |         29.3 |
| receipt        |    180 |     1051 |       0.984 |      17 |        0 |     159 |      0.755 |       0.758 |            1 |         11   |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| invoice        |    215 |     2133 |       0.978 |      43 |        4 |     129 |      0.093 |       0.853 |            1 |         29.3 |
| receipt        |    178 |     1041 |       0.986 |      15 |        0 |     158 |      0.753 |       0.758 |            1 |         11   |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.99  |       2 |        0 |      10 |      0     |       0.857 |            1 |         29.2 |
| de     | invoice        | real      |     16 |      158 |       0.981 |       3 |        0 |      10 |      0.2   |       0.719 |            1 |         46.2 |
| de     | receipt        | generated |     36 |      268 |       0.978 |       6 |        0 |      44 |      0.841 |       0.685 |            1 |         10.5 |
| en     | bank_statement | generated |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| en     | invoice        | generated |     61 |      477 |       0.994 |       3 |        0 |      46 |      0.196 |       0.957 |            1 |         24.9 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         25.5 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         10.9 |
| en     | receipt        | real      |     36 |      101 |       0.95  |       5 |        0 |      15 |      0.4   |       1     |            1 |         13.5 |
| es     | invoice        | generated |     18 |      203 |       0.966 |       7 |        0 |      11 |      0     |       0.823 |            1 |         29.6 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.888 |            1 |         29.9 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       0.727 |            1 |         26.1 |
| fr     | receipt        | generated |     36 |      270 |       0.989 |       3 |        0 |      42 |      0.857 |       0.699 |            1 |         10.6 |
| id     | receipt        | real      |     17 |       39 |       1     |       0 |        0 |       5 |      0.4   |       1     |            1 |         13.7 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.812 |            1 |         30.3 |
| it     | receipt        | generated |     36 |      270 |       0.993 |       2 |        0 |      42 |      0.905 |       0.692 |            1 |         10.6 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       1     |            1 |         15.4 |
| nl     | invoice        | generated |     18 |      204 |       0.971 |       6 |        0 |       9 |      0     |       0.882 |            1 |         29.5 |
| pl     | invoice        | generated |     18 |      197 |       0.985 |       3 |        0 |      16 |      0.062 |       0.768 |            1 |         30   |
| pt     | invoice        | generated |     18 |      205 |       0.99  |       2 |        0 |      11 |      0     |       0.81  |            1 |         29.7 |
| pt     | invoice        | real      |     12 |       77 |       0.779 |      13 |        4 |       3 |      0     |       0.822 |            1 |         25.1 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | account_number  |      4 |        4 |       0.75  |       1 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.8 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.8 |
| invoice        | buyer_name      |    190 |      189 |       0.952 |       9 |        0 |       1 |      0     |       1     |            1 |         29.5 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.942 |       3 |        3 |      59 |      0.017 |       1     |            1 |         29.5 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29.6 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       1     |            1 |         29.5 |
| invoice        | invoice_number  |    215 |      209 |       0.962 |       7 |        1 |       6 |      0     |       1     |            1 |         29.3 |
| invoice        | issue_date      |    216 |      211 |       0.991 |       2 |        0 |       5 |      0.6   |       1     |            1 |         29.3 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.667 |       1     |            1 |         39.7 |
| invoice        | seller_iban     |    165 |      154 |       0.987 |       2 |        0 |      11 |      0     |       1     |            1 |         29.6 |
| invoice        | seller_name     |    203 |      190 |       0.953 |       9 |        0 |      13 |      0.154 |       0.99  |            1 |         29.4 |
| invoice        | seller_vat_id   |    178 |      176 |       0.966 |       6 |        0 |       2 |      0     |       1     |            1 |         29.5 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      1     |       0.476 |            1 |         29.3 |
| invoice        | total_net       |    196 |      196 |       0.99  |       2 |        0 |       0 |    nan     |       0.474 |            1 |         29.5 |
| invoice        | total_tax       |    188 |      188 |       0.995 |       1 |        0 |       0 |    nan     |       0.452 |            1 |         29.3 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.6 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.4   |       1     |            1 |         10.7 |
| receipt        | merchant_name   |    146 |      145 |       0.993 |       1 |        0 |       1 |      1     |       1     |            1 |         10.7 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.1   |       1     |            1 |         10.6 |
| receipt        | payment_method  |    119 |      119 |       0.983 |       2 |        0 |       0 |    nan     |       1     |            1 |         10.6 |
| receipt        | subtotal        |    151 |       37 |       1     |       0 |        0 |     114 |      1     |       0.305 |            1 |         10.7 |
| receipt        | tax_amount      |    119 |      113 |       1     |       0 |        0 |       6 |      0     |       0.354 |            1 |         10.8 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         10.6 |
| receipt        | total           |    160 |      160 |       0.925 |      12 |        0 |       0 |    nan     |       0.344 |            1 |         10.8 |
