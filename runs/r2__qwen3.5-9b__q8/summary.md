# r2__qwen3.5-9b__q8

```
{
 "model": "mlx-community/Qwen3.5-9B-8bit",
 "revision": "16daa4818c54ce5f5436f929d52542eb65bbed9d",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3.5-9b__q8",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 5.68,
 "load_peak_gb": 10.427,
 "finished_at": "2026-11-16 22:24:58"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         27.6 |
| invoice        |    216 |     2145 |       0.988 |      18 |        7 |     129 |      0.093 |       0.795 |            1 |         38.3 |
| receipt        |    180 |     1051 |       0.99  |       9 |        1 |     159 |      0.736 |       0.927 |            1 |         16.6 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         27.6 |
| invoice        |    215 |     2133 |       0.988 |      18 |        7 |     129 |      0.093 |       0.795 |            1 |         38.3 |
| receipt        |    178 |     1041 |       0.992 |       7 |        1 |     158 |      0.734 |       0.926 |            1 |         16.6 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      10 |      0     |       0.739 |            1 |         38.1 |
| de     | invoice        | real      |     16 |      158 |       0.975 |       4 |        0 |      10 |      0     |       0.753 |            1 |         52.4 |
| de     | receipt        | generated |     36 |      268 |       0.993 |       2 |        0 |      44 |      0.818 |       0.921 |            1 |         16.3 |
| en     | bank_statement | generated |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         27.6 |
| en     | invoice        | generated |     61 |      477 |       0.996 |       1 |        1 |      46 |      0.261 |       0.939 |            1 |         33.1 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         34.6 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         16.5 |
| en     | receipt        | real      |     36 |      101 |       0.98  |       2 |        0 |      15 |      0.333 |       0.972 |            1 |         19.4 |
| es     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      11 |      0     |       0.739 |            1 |         38.5 |
| fr     | invoice        | generated |     15 |      169 |       1     |       0 |        0 |       6 |      0     |       0.763 |            1 |         39.2 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.727 |            1 |         35.5 |
| fr     | receipt        | generated |     36 |      270 |       1     |       0 |        0 |      42 |      0.857 |       0.905 |            1 |         16.5 |
| id     | receipt        | real      |     17 |       39 |       0.897 |       4 |        0 |       5 |      0.4   |       0.927 |            1 |         18.6 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.74  |            1 |         39.7 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.881 |       0.915 |            1 |         16.4 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       0 |        1 |       0 |    nan     |       1     |            1 |         21.3 |
| nl     | invoice        | generated |     18 |      204 |       1     |       0 |        0 |       9 |      0     |       0.74  |            1 |         38.7 |
| pl     | invoice        | generated |     18 |      197 |       1     |       0 |        0 |      16 |      0     |       0.741 |            1 |         39.2 |
| pt     | invoice        | generated |     18 |      205 |       1     |       0 |        0 |      11 |      0     |       0.737 |            1 |         39.5 |
| pt     | invoice        | real      |     12 |       77 |       0.779 |      11 |        6 |       3 |      0     |       0.887 |            1 |         32.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.6 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.6 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.6 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0.667 |            1 |         27.1 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.6 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.1 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         40.2 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         40.2 |
| invoice        | buyer_name      |    190 |      189 |       0.995 |       0 |        1 |       1 |      0     |       1     |            1 |         38.5 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.942 |       0 |        6 |      59 |      0     |       1     |            1 |         38.5 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         38.7 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0     |       1     |            1 |         38.5 |
| invoice        | invoice_number  |    215 |      209 |       0.986 |       3 |        0 |       6 |      0     |       1     |            1 |         38.3 |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0.4   |       1     |            1 |         38.3 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         47.7 |
| invoice        | seller_iban     |    165 |      154 |       0.994 |       1 |        0 |      11 |      0     |       1     |            1 |         38.7 |
| invoice        | seller_name     |    203 |      190 |       0.979 |       4 |        0 |      13 |      0.538 |       0.995 |            1 |         38.5 |
| invoice        | seller_vat_id   |    178 |      176 |       0.955 |       8 |        0 |       2 |      0     |       1     |            1 |         38.6 |
| invoice        | total_gross     |    208 |      205 |       1     |       0 |        0 |       3 |      1     |       0.269 |            1 |         38.4 |
| invoice        | total_net       |    196 |      196 |       0.995 |       1 |        0 |       0 |    nan     |       0.245 |            1 |         38.5 |
| invoice        | total_tax       |    188 |      188 |       0.995 |       1 |        0 |       0 |    nan     |       0.255 |            1 |         38.4 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         16.4 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.2   |       1     |            1 |         16.5 |
| receipt        | merchant_name   |    146 |      145 |       0.986 |       2 |        0 |       1 |      1     |       0.993 |            1 |         16.5 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.033 |       1     |            1 |         16.5 |
| receipt        | payment_method  |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         16.4 |
| receipt        | subtotal        |    151 |       37 |       0.973 |       1 |        0 |     114 |      1     |       0.795 |            1 |         16.5 |
| receipt        | tax_amount      |    119 |      113 |       0.982 |       1 |        1 |       6 |      0     |       0.804 |            1 |         16.5 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         16.5 |
| receipt        | total           |    160 |      160 |       0.981 |       3 |        0 |       0 |    nan     |       0.806 |            1 |         16.5 |
