# r2__lift-9b__q6c

```
{
 "model": "mlx-community/lift-oQ6",
 "revision": "8fa369a9f9f3b0eebbf082674d92a2e7c64e5072",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "r2__lift-9b__q6c",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.67,
 "load_peak_gb": 8.258,
 "finished_at": "2026-11-20 00:05:59"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       0.769 |        1     |         23.4 |
| invoice        |    216 |     2145 |       0.952 |      45 |       59 |     129 |      0.016 |       0.774 |        0.977 |         32.4 |
| receipt        |    180 |     1051 |       0.974 |      10 |       17 |     159 |      0.604 |       0.779 |        0.956 |         12.6 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       0.769 |        1     |         23.4 |
| invoice        |    215 |     2133 |       0.951 |      45 |       59 |     129 |      0.016 |       0.774 |        0.977 |         32.4 |
| receipt        |    178 |     1041 |       0.976 |       8 |       17 |     158 |      0.601 |       0.778 |        0.955 |         12.6 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      10 |      0     |       0.739 |        1     |         32.3 |
| de     | invoice        | real      |     16 |      158 |       0.981 |       1 |        2 |      10 |      0     |       0.692 |        1     |         46.6 |
| de     | receipt        | generated |     36 |      268 |       0.993 |       2 |        0 |      44 |      0.682 |       0.758 |        1     |         12.2 |
| en     | bank_statement | generated |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       0.769 |        1     |         23.4 |
| en     | invoice        | generated |     61 |      477 |       0.99  |       4 |        1 |      46 |      0.022 |       0.869 |        1     |         27.6 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.909 |        1     |         28.7 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0     |       1     |        1     |         12.3 |
| en     | receipt        | real      |     36 |      101 |       0.96  |       3 |        1 |      15 |      0.133 |       0.971 |        1     |         15.3 |
| es     | invoice        | generated |     18 |      203 |       0.956 |       9 |        0 |      11 |      0     |       0.739 |        1     |         32.8 |
| fr     | invoice        | generated |     15 |      169 |       0.947 |       8 |        1 |       6 |      0     |       0.768 |        1     |         33.2 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       0.727 |        1     |         29.3 |
| fr     | receipt        | generated |     36 |      270 |       0.989 |       3 |        0 |      42 |      0.81  |       0.75  |        1     |         12.3 |
| id     | receipt        | real      |     17 |       39 |       0.974 |       1 |        0 |       5 |      0.4   |       0.341 |        1     |         14.9 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.74  |        1     |         33.4 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.667 |       0.758 |        1     |         12.1 |
| ko     | receipt        | real      |      8 |       16 |       0     |       0 |       16 |       0 |    nan     |     nan     |        0     |         79.3 |
| nl     | invoice        | generated |     18 |      204 |       0.995 |       1 |        0 |       9 |      0     |       0.74  |        1     |         32.6 |
| pl     | invoice        | generated |     18 |      197 |       0.995 |       1 |        0 |      16 |      0     |       0.741 |        1     |         33.9 |
| pt     | invoice        | generated |     18 |      205 |       0.785 |       9 |       35 |      11 |      0     |       0.735 |        0.833 |         33   |
| pt     | invoice        | real      |     12 |       77 |       0.623 |       9 |       20 |       3 |      0.333 |       0.914 |        0.833 |         27   |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       0.75  |       1 |        0 |       0 |    nan     |       1     |        1     |         23.4 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         23.4 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         23.4 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0     |        1     |         23.3 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         23.4 |
| bank_statement | opening_balance |      3 |        3 |       0.667 |       1 |        0 |       0 |    nan     |       0     |        1     |         23.3 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         36.1 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         36.1 |
| invoice        | buyer_name      |    190 |      189 |       0.894 |      17 |        3 |       1 |      0     |       1     |        0.984 |         32.6 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.923 |       0 |        8 |      59 |      0     |       1     |        0.969 |         32.6 |
| invoice        | currency        |    169 |      169 |       0.982 |       0 |        3 |       0 |    nan     |       1     |        0.982 |         32.8 |
| invoice        | due_date        |    172 |      146 |       0.979 |       0 |        3 |      26 |      0     |       1     |        0.983 |         32.6 |
| invoice        | invoice_number  |    215 |      209 |       0.957 |       2 |        7 |       6 |      0.167 |       1     |        0.977 |         32.4 |
| invoice        | issue_date      |    216 |      211 |       0.976 |       0 |        5 |       5 |      0     |       1     |        0.977 |         32.4 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0     |       1     |        1     |         42   |
| invoice        | seller_iban     |    165 |      154 |       0.968 |       1 |        4 |      11 |      0     |       1     |        0.982 |         32.8 |
| invoice        | seller_name     |    203 |      190 |       0.889 |      15 |        6 |      13 |      0.077 |       1     |        0.975 |         32.5 |
| invoice        | seller_vat_id   |    178 |      176 |       0.932 |       6 |        6 |       2 |      0     |       1     |        0.972 |         32.7 |
| invoice        | total_gross     |    208 |      205 |       0.966 |       1 |        6 |       3 |      0     |       0.178 |        0.976 |         32.5 |
| invoice        | total_net       |    196 |      196 |       0.974 |       2 |        3 |       0 |    nan     |       0.171 |        0.985 |         32.5 |
| invoice        | total_tax       |    188 |      188 |       0.968 |       1 |        5 |       0 |    nan     |       0.186 |        0.979 |         32.5 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         12.3 |
| receipt        | date            |    148 |      143 |       0.986 |       1 |        1 |       5 |      0     |       1     |        0.993 |         12.4 |
| receipt        | merchant_name   |    146 |      145 |       0.952 |       5 |        2 |       1 |      1     |       0.986 |        0.986 |         12.4 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0     |       1     |        1     |         12.3 |
| receipt        | payment_method  |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         12.3 |
| receipt        | subtotal        |    151 |       37 |       1     |       0 |        0 |     114 |      0.833 |       0.364 |        1     |         12.3 |
| receipt        | tax_amount      |    119 |      113 |       0.947 |       1 |        5 |       6 |      0     |       0.389 |        0.966 |         12.5 |
| receipt        | time            |    134 |      131 |       0.962 |       0 |        5 |       3 |      0     |       1     |        0.963 |         12.3 |
| receipt        | total           |    160 |      160 |       0.963 |       2 |        4 |       0 |    nan     |       0.372 |        0.975 |         12.4 |
