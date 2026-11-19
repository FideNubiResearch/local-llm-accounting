# r2__qwen3.5-9b__q6

```
{
 "model": "mlx-community/Qwen3.5-9B-6bit",
 "revision": "76fe4065e622cf34990d3c13ef80ec8531c9a0f7",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3.5-9b__q6",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 4.53,
 "load_peak_gb": 8.189,
 "finished_at": "2026-11-16 19:19:01"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       0.962 |            1 |         24.7 |
| invoice        |    216 |     2145 |       0.988 |      20 |        6 |     129 |      0.101 |       0.795 |            1 |         34.6 |
| receipt        |    180 |     1051 |       0.99  |      10 |        0 |     159 |      0.742 |       0.929 |            1 |         14.5 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       0.962 |            1 |         24.7 |
| invoice        |    215 |     2133 |       0.988 |      20 |        6 |     129 |      0.101 |       0.795 |            1 |         34.6 |
| receipt        |    178 |     1041 |       0.992 |       8 |        0 |     158 |      0.741 |       0.928 |            1 |         14.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      10 |      0     |       0.739 |            1 |         34.2 |
| de     | invoice        | real      |     16 |      158 |       0.962 |       6 |        0 |      10 |      0     |       0.734 |            1 |         49.5 |
| de     | receipt        | generated |     36 |      268 |       0.993 |       2 |        0 |      44 |      0.818 |       0.905 |            1 |         14.2 |
| en     | bank_statement | generated |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       0.962 |            1 |         24.7 |
| en     | invoice        | generated |     61 |      477 |       0.998 |       1 |        0 |      46 |      0.283 |       0.945 |            1 |         30.4 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         31.6 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         14.5 |
| en     | receipt        | real      |     36 |      101 |       0.98  |       2 |        0 |      15 |      0.4   |       0.972 |            1 |         16.8 |
| es     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      11 |      0     |       0.739 |            1 |         34.7 |
| fr     | invoice        | generated |     15 |      169 |       1     |       0 |        0 |       6 |      0     |       0.763 |            1 |         35.8 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.727 |            1 |         32.3 |
| fr     | receipt        | generated |     36 |      270 |       1     |       0 |        0 |      42 |      0.857 |       0.922 |            1 |         14   |
| id     | receipt        | real      |     17 |       39 |       0.872 |       5 |        0 |       5 |      0.4   |       0.878 |            1 |         16.7 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.74  |            1 |         36.4 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.881 |       0.928 |            1 |         14.1 |
| ko     | receipt        | real      |      8 |       16 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.3 |
| nl     | invoice        | generated |     18 |      204 |       1     |       0 |        0 |       9 |      0     |       0.74  |            1 |         35.6 |
| pl     | invoice        | generated |     18 |      197 |       1     |       0 |        0 |      16 |      0     |       0.741 |            1 |         36.1 |
| pt     | invoice        | generated |     18 |      205 |       1     |       0 |        0 |      11 |      0     |       0.737 |            1 |         35.7 |
| pt     | invoice        | real      |     12 |       77 |       0.779 |      11 |        6 |       3 |      0     |       0.887 |            1 |         30.1 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       0.75  |       1 |        0 |       0 |    nan     |       1     |            1 |         24.7 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.7 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.7 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0.667 |            1 |         24.4 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.7 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.4 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         37.4 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         37.4 |
| invoice        | buyer_name      |    190 |      189 |       0.995 |       1 |        0 |       1 |      0     |       1     |            1 |         34.8 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.942 |       0 |        6 |      59 |      0     |       1     |            1 |         34.8 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         35.1 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0     |       1     |            1 |         34.8 |
| invoice        | invoice_number  |    215 |      209 |       0.986 |       3 |        0 |       6 |      0     |       1     |            1 |         34.6 |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0.4   |       1     |            1 |         34.6 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         44.4 |
| invoice        | seller_iban     |    165 |      154 |       0.987 |       2 |        0 |      11 |      0     |       1     |            1 |         35   |
| invoice        | seller_name     |    203 |      190 |       0.979 |       4 |        0 |      13 |      0.615 |       0.995 |            1 |         34.8 |
| invoice        | seller_vat_id   |    178 |      176 |       0.955 |       8 |        0 |       2 |      0     |       1     |            1 |         34.9 |
| invoice        | total_gross     |    208 |      205 |       1     |       0 |        0 |       3 |      1     |       0.269 |            1 |         34.7 |
| invoice        | total_net       |    196 |      196 |       0.995 |       1 |        0 |       0 |    nan     |       0.245 |            1 |         34.8 |
| invoice        | total_tax       |    188 |      188 |       0.995 |       1 |        0 |       0 |    nan     |       0.255 |            1 |         34.7 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.1 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.4   |       1     |            1 |         14.3 |
| receipt        | merchant_name   |    146 |      145 |       0.986 |       2 |        0 |       1 |      1     |       0.993 |            1 |         14.3 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.033 |       1     |            1 |         14.2 |
| receipt        | payment_method  |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.1 |
| receipt        | subtotal        |    151 |       37 |       0.946 |       2 |        0 |     114 |      1     |       0.795 |            1 |         14.2 |
| receipt        | tax_amount      |    119 |      113 |       0.991 |       1 |        0 |       6 |      0     |       0.814 |            1 |         14.3 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         14.1 |
| receipt        | total           |    160 |      160 |       0.981 |       3 |        0 |       0 |    nan     |       0.812 |            1 |         14.3 |
