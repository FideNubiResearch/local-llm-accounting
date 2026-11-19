# r2__qwen3vl-8b__q6

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-6bit",
 "revision": "0b6a7d52ff9e393d9560e7b1e0fcd8ac40ba7b60",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3vl-8b__q6",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.97,
 "load_peak_gb": 7.809,
 "finished_at": "2026-11-18 00:47:08"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| invoice        |    216 |     2145 |       0.98  |      28 |       14 |     129 |      0.031 |       0.868 |            1 |         33.4 |
| receipt        |    180 |     1051 |       0.984 |      14 |        3 |     159 |      0.742 |       0.758 |            1 |         13   |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| invoice        |    215 |     2133 |       0.98  |      28 |       14 |     129 |      0.031 |       0.869 |            1 |         33.4 |
| receipt        |    178 |     1041 |       0.986 |      12 |        3 |     158 |      0.741 |       0.758 |            1 |         13   |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.99  |       1 |        1 |      10 |      0     |       0.886 |            1 |         33.8 |
| de     | invoice        | real      |     16 |      158 |       0.975 |       3 |        1 |      10 |      0.2   |       0.698 |            1 |         49.7 |
| de     | receipt        | generated |     36 |      268 |       0.981 |       5 |        0 |      44 |      0.841 |       0.685 |            1 |         12.5 |
| en     | bank_statement | generated |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| en     | invoice        | generated |     61 |      477 |       0.99  |       3 |        2 |      46 |      0.043 |       0.975 |            1 |         28.4 |
| en     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29.5 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         12.7 |
| en     | receipt        | real      |     36 |      101 |       0.95  |       5 |        0 |      15 |      0.333 |       0.981 |            1 |         15.8 |
| es     | invoice        | generated |     18 |      203 |       0.985 |       2 |        1 |      11 |      0     |       0.827 |            1 |         33.5 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.917 |            1 |         34.3 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.727 |            1 |         30.2 |
| fr     | receipt        | generated |     36 |      270 |       0.981 |       3 |        2 |      42 |      0.857 |       0.717 |            1 |         12.6 |
| id     | receipt        | real      |     17 |       39 |       1     |       0 |        0 |       5 |      0.2   |       1     |            1 |         15.9 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.87  |            1 |         34.6 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.905 |       0.682 |            1 |         12.6 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       0 |        1 |       0 |    nan     |       1     |            1 |         17.5 |
| nl     | invoice        | generated |     18 |      204 |       0.995 |       0 |        1 |       9 |      0     |       0.911 |            1 |         33.6 |
| pl     | invoice        | generated |     18 |      197 |       0.985 |       2 |        1 |      16 |      0     |       0.781 |            1 |         34.1 |
| pt     | invoice        | generated |     18 |      205 |       0.98  |       2 |        2 |      11 |      0     |       0.793 |            1 |         33.4 |
| pt     | invoice        | real      |     12 |       77 |       0.766 |      13 |        5 |       3 |      0     |       0.806 |            1 |         28.7 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.4 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.5 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.4 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         38.6 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         38.6 |
| invoice        | buyer_name      |    190 |      189 |       0.989 |       2 |        0 |       1 |      0     |       1     |            1 |         33.6 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.952 |       2 |        3 |      59 |      0     |       1     |            1 |         33.6 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.8 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       1     |            1 |         33.5 |
| invoice        | invoice_number  |    215 |      209 |       0.971 |       5 |        1 |       6 |      0     |       1     |            1 |         33.4 |
| invoice        | issue_date      |    216 |      211 |       0.986 |       3 |        0 |       5 |      0     |       1     |            1 |         33.4 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.667 |       1     |            1 |         43.8 |
| invoice        | seller_iban     |    165 |      154 |       0.942 |       2 |        7 |      11 |      0     |       1     |            1 |         33.8 |
| invoice        | seller_name     |    203 |      190 |       0.958 |       7 |        1 |      13 |      0.077 |       0.989 |            1 |         33.5 |
| invoice        | seller_vat_id   |    178 |      176 |       0.966 |       5 |        1 |       2 |      0     |       1     |            1 |         33.7 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      0     |       0.527 |            1 |         33.5 |
| invoice        | total_net       |    196 |      196 |       0.995 |       0 |        1 |       0 |    nan     |       0.533 |            1 |         33.5 |
| invoice        | total_tax       |    188 |      188 |       1     |       0 |        0 |       0 |    nan     |       0.511 |            1 |         33.5 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.6 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.2   |       1     |            1 |         12.9 |
| receipt        | merchant_name   |    146 |      145 |       0.993 |       1 |        0 |       1 |      1     |       1     |            1 |         12.8 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.1   |       1     |            1 |         12.7 |
| receipt        | payment_method  |    119 |      119 |       0.975 |       1 |        2 |       0 |    nan     |       1     |            1 |         12.6 |
| receipt        | subtotal        |    151 |       37 |       1     |       0 |        0 |     114 |      0.991 |       0.3   |            1 |         12.7 |
| receipt        | tax_amount      |    119 |      113 |       0.973 |       2 |        1 |       6 |      0     |       0.357 |            1 |         12.9 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         12.7 |
| receipt        | total           |    160 |      160 |       0.95  |       8 |        0 |       0 |    nan     |       0.344 |            1 |         12.9 |
