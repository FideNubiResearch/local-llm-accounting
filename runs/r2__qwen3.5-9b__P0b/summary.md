# r2__qwen3.5-9b__P0b

```
{
 "model": "mlx-community/Qwen3.5-9B-4bit",
 "revision": "8b2b98c00a6b4d291155e4890773ca8f769aee53",
 "prompt": "P0b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3.5-9b__P0b",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.35,
 "load_peak_gb": 5.951,
 "finished_at": "2026-11-16 10:24:20"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         20.7 |
| invoice        |    216 |     2145 |       0.983 |      29 |        7 |     129 |      0.132 |       0.8   |            1 |         29.4 |
| receipt        |    180 |     1051 |       0.979 |      22 |        0 |     159 |      0.748 |       0.826 |            1 |         11.7 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         20.7 |
| invoice        |    215 |     2133 |       0.984 |      28 |        7 |     129 |      0.132 |       0.801 |            1 |         29.4 |
| receipt        |    178 |     1041 |       0.981 |      20 |        0 |     158 |      0.747 |       0.827 |            1 |         11.7 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.995 |       1 |        0 |      10 |      0     |       0.739 |            1 |         29.2 |
| de     | invoice        | real      |     16 |      158 |       0.968 |       4 |        1 |      10 |      0     |       0.771 |            1 |         44.9 |
| de     | receipt        | generated |     36 |      268 |       0.981 |       5 |        0 |      44 |      0.818 |       0.776 |            1 |         11.3 |
| en     | bank_statement | generated |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         20.7 |
| en     | invoice        | generated |     61 |      477 |       0.992 |       3 |        1 |      46 |      0.348 |       0.953 |            1 |         25.2 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         26.2 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.364 |       1     |            1 |         12   |
| en     | receipt        | real      |     36 |      101 |       0.96  |       4 |        0 |      15 |      0.267 |       0.962 |            1 |         14.2 |
| es     | invoice        | generated |     18 |      203 |       0.995 |       1 |        0 |      11 |      0     |       0.739 |            1 |         29.7 |
| fr     | invoice        | generated |     15 |      169 |       1     |       0 |        0 |       6 |      0     |       0.781 |            1 |         29.8 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.727 |            1 |         26.7 |
| fr     | receipt        | generated |     36 |      270 |       0.989 |       3 |        0 |      42 |      0.857 |       0.824 |            1 |         11.4 |
| id     | receipt        | real      |     17 |       39 |       0.769 |       9 |        0 |       5 |      0.4   |       0.854 |            1 |         14.1 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.74  |            1 |         30.3 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.881 |       0.769 |            1 |         11.3 |
| ko     | receipt        | real      |      8 |       16 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         16.3 |
| nl     | invoice        | generated |     18 |      204 |       0.995 |       1 |        0 |       9 |      0     |       0.74  |            1 |         29.7 |
| pl     | invoice        | generated |     18 |      197 |       1     |       0 |        0 |      16 |      0     |       0.741 |            1 |         29.9 |
| pt     | invoice        | generated |     18 |      205 |       1     |       0 |        0 |      11 |      0     |       0.751 |            1 |         29.7 |
| pt     | invoice        | real      |     12 |       77 |       0.727 |      16 |        5 |       3 |      0.333 |       0.822 |            1 |         25.4 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.7 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.7 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.7 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0.667 |            1 |         20.6 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.7 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.6 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.6 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.6 |
| invoice        | buyer_name      |    190 |      189 |       0.995 |       1 |        0 |       1 |      0     |       1     |            1 |         29.5 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.952 |       0 |        5 |      59 |      0     |       1     |            1 |         29.5 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29.6 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       0.993 |            1 |         29.5 |
| invoice        | invoice_number  |    215 |      209 |       0.971 |       6 |        0 |       6 |      0.333 |       1     |            1 |         29.4 |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0.6   |       0.995 |            1 |         29.4 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         39.1 |
| invoice        | seller_iban     |    165 |      154 |       0.961 |       5 |        1 |      11 |      0     |       1     |            1 |         29.6 |
| invoice        | seller_name     |    203 |      190 |       0.979 |       4 |        0 |      13 |      0.692 |       0.99  |            1 |         29.5 |
| invoice        | seller_vat_id   |    178 |      176 |       0.949 |       8 |        1 |       2 |      0     |       1     |            1 |         29.6 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      0.667 |       0.285 |            1 |         29.4 |
| invoice        | total_net       |    196 |      196 |       0.995 |       1 |        0 |       0 |    nan     |       0.276 |            1 |         29.5 |
| invoice        | total_tax       |    188 |      188 |       0.989 |       2 |        0 |       0 |    nan     |       0.277 |            1 |         29.5 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.3 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0     |       0.986 |            1 |         11.5 |
| receipt        | merchant_name   |    146 |      145 |       0.979 |       3 |        0 |       1 |      1     |       0.993 |            1 |         11.5 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.133 |       1     |            1 |         11.3 |
| receipt        | payment_method  |    119 |      119 |       0.983 |       2 |        0 |       0 |    nan     |       1     |            1 |         11.3 |
| receipt        | subtotal        |    151 |       37 |       0.892 |       4 |        0 |     114 |      1     |       0.517 |            1 |         11.4 |
| receipt        | tax_amount      |    119 |      113 |       0.973 |       3 |        0 |       6 |      0     |       0.522 |            1 |         11.6 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         11.4 |
| receipt        | total           |    160 |      160 |       0.95  |       8 |        0 |       0 |    nan     |       0.544 |            1 |         11.5 |
