# r2__qwen3vl-8b__constr

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "r2__qwen3vl-8b__constr",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.99,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-17 22:09:18"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       0.962 |            1 |         20.9 |
| invoice        |    216 |     2145 |       0.978 |      38 |       10 |     129 |      0.093 |       0.834 |            1 |         29   |
| receipt        |    180 |     1051 |       0.985 |      16 |        0 |     159 |      0.748 |       0.758 |            1 |         10.5 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       0.962 |            1 |         20.9 |
| invoice        |    215 |     2133 |       0.977 |      38 |       10 |     129 |      0.093 |       0.834 |            1 |         29   |
| receipt        |    178 |     1041 |       0.987 |      14 |        0 |     158 |      0.747 |       0.758 |            1 |         10.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.99  |       2 |        0 |      10 |      0     |       0.768 |            1 |         29.1 |
| de     | invoice        | real      |     16 |      158 |       0.975 |       3 |        1 |      10 |      0.2   |       0.698 |            1 |         46.1 |
| de     | receipt        | generated |     36 |      268 |       0.978 |       6 |        0 |      44 |      0.841 |       0.685 |            1 |         10   |
| en     | bank_statement | generated |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       0.962 |            1 |         20.9 |
| en     | invoice        | generated |     61 |      477 |       0.994 |       3 |        0 |      46 |      0.174 |       0.951 |            1 |         24.3 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         25   |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         10.4 |
| en     | receipt        | real      |     36 |      101 |       0.95  |       5 |        0 |      15 |      0.333 |       0.972 |            1 |         13.1 |
| es     | invoice        | generated |     18 |      203 |       0.98  |       3 |        1 |      11 |      0     |       0.797 |            1 |         29.5 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.87  |            1 |         29.6 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       0.727 |            1 |         25.5 |
| fr     | receipt        | generated |     36 |      270 |       0.993 |       2 |        0 |      42 |      0.857 |       0.709 |            1 |         10.2 |
| id     | receipt        | real      |     17 |       39 |       1     |       0 |        0 |       5 |      0.4   |       1     |            1 |         13.4 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0.143 |       0.813 |            1 |         29.8 |
| it     | receipt        | generated |     36 |      270 |       0.993 |       2 |        0 |      42 |      0.905 |       0.692 |            1 |         10   |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       1     |            1 |         15   |
| nl     | invoice        | generated |     18 |      204 |       0.971 |       6 |        0 |       9 |      0     |       0.868 |            1 |         28.9 |
| pl     | invoice        | generated |     18 |      197 |       0.985 |       2 |        1 |      16 |      0.062 |       0.741 |            1 |         29.5 |
| pt     | invoice        | generated |     18 |      205 |       0.99  |       2 |        0 |      11 |      0     |       0.81  |            1 |         29.4 |
| pt     | invoice        | real      |     12 |       77 |       0.753 |      12 |        7 |       3 |      0     |       0.814 |            1 |         24.4 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| bank_statement | account_number  |      4 |        4 |       0.5   |       2 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0.667 |            1 |         20.9 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.8 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.8 |
| invoice        | buyer_name      |    190 |      189 |       0.958 |       8 |        0 |       1 |      0     |       1     |            1 |         29.2 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.933 |       3 |        4 |      59 |      0.034 |       1     |            1 |         29.2 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29.4 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       1     |            1 |         29.1 |
| invoice        | invoice_number  |    215 |      209 |       0.962 |       5 |        3 |       6 |      0     |       1     |            1 |         29   |
| invoice        | issue_date      |    216 |      211 |       0.991 |       2 |        0 |       5 |      0.4   |       1     |            1 |         29   |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.667 |       1     |            1 |         39.9 |
| invoice        | seller_iban     |    165 |      154 |       0.968 |       2 |        3 |      11 |      0     |       1     |            1 |         29.4 |
| invoice        | seller_name     |    203 |      190 |       0.963 |       7 |        0 |      13 |      0.154 |       0.99  |            1 |         29.1 |
| invoice        | seller_vat_id   |    178 |      176 |       0.955 |       8 |        0 |       2 |      0     |       1     |            1 |         29.2 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      1     |       0.409 |            1 |         29.1 |
| invoice        | total_net       |    196 |      196 |       0.995 |       1 |        0 |       0 |    nan     |       0.403 |            1 |         29.2 |
| invoice        | total_tax       |    188 |      188 |       1     |       0 |        0 |       0 |    nan     |       0.388 |            1 |         29.1 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.2   |       0.993 |            1 |         10.3 |
| receipt        | merchant_name   |    146 |      145 |       0.993 |       1 |        0 |       1 |      1     |       1     |            1 |         10.3 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.1   |       1     |            1 |         10.2 |
| receipt        | payment_method  |    119 |      119 |       0.992 |       1 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| receipt        | subtotal        |    151 |       37 |       1     |       0 |        0 |     114 |      1     |       0.305 |            1 |         10.3 |
| receipt        | tax_amount      |    119 |      113 |       1     |       0 |        0 |       6 |      0     |       0.363 |            1 |         10.4 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         10.2 |
| receipt        | total           |    160 |      160 |       0.925 |      12 |        0 |       0 |    nan     |       0.344 |            1 |         10.3 |
