# r2__nuextract3-4b__q6

```
{
 "model": "numind/NuExtract3-mlx-6bits",
 "revision": "d0db1bdf8eea7e80fe1c08a0be3972f1f17539df",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "nuextract": true,
 "run_id": "r2__nuextract3-4b__q6",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.47,
 "load_peak_gb": 4.086,
 "finished_at": "2026-11-19 21:20:23"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| invoice        |    216 |     2145 |       0.979 |      30 |       14 |     129 |      0.054 |       1     |            1 |         18   |
| receipt        |    180 |     1051 |       0.96  |      41 |        1 |     159 |      0.742 |       0.997 |            1 |          6.8 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| invoice        |    215 |     2133 |       0.979 |      30 |       14 |     129 |      0.054 |       1     |            1 |         18   |
| receipt        |    178 |     1041 |       0.962 |      39 |        1 |     158 |      0.741 |       0.997 |            1 |          6.8 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.995 |       1 |        0 |      10 |      0     |       1     |            1 |         17.9 |
| de     | invoice        | real      |     16 |      158 |       0.994 |       1 |        0 |      10 |      0.1   |       1     |            1 |         27.6 |
| de     | receipt        | generated |     36 |      268 |       0.944 |      15 |        0 |      44 |      0.841 |       1     |            1 |          6.6 |
| en     | bank_statement | generated |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| en     | invoice        | generated |     61 |      477 |       0.973 |      10 |        3 |      46 |      0.13  |       1     |            1 |         15.2 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         16   |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.182 |       1     |            1 |          6.8 |
| en     | receipt        | real      |     36 |      101 |       0.96  |       4 |        0 |      15 |      0.2   |       0.971 |            1 |          8.5 |
| es     | invoice        | generated |     18 |      203 |       1     |       0 |        0 |      11 |      0     |       1     |            1 |         18.1 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       0 |        1 |       6 |      0     |       1     |            1 |         18.4 |
| fr     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         16.3 |
| fr     | receipt        | generated |     36 |      270 |       0.978 |       5 |        1 |      42 |      0.81  |       1     |            1 |          6.6 |
| id     | receipt        | real      |     17 |       39 |       0.795 |       8 |        0 |       5 |      0.2   |       1     |            1 |          8.1 |
| it     | invoice        | generated |     18 |      208 |       0.976 |       5 |        0 |       7 |      0     |       1     |            1 |         18.8 |
| it     | receipt        | generated |     36 |      270 |       0.97  |       8 |        0 |      42 |      0.976 |       1     |            1 |          6.6 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       0.938 |            1 |          9.5 |
| nl     | invoice        | generated |     18 |      204 |       0.99  |       0 |        2 |       9 |      0     |       1     |            1 |         18.4 |
| pl     | invoice        | generated |     18 |      197 |       0.995 |       1 |        0 |      16 |      0     |       1     |            1 |         18.8 |
| pt     | invoice        | generated |     18 |      205 |       0.976 |       4 |        1 |      11 |      0     |       1     |            1 |         18.3 |
| pt     | invoice        | real      |     12 |       77 |       0.818 |       7 |        7 |       3 |      0     |       0.986 |            1 |         15.2 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.6 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.3 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.3 |
| invoice        | buyer_name      |    190 |      189 |       0.974 |       5 |        0 |       1 |      0     |       1     |            1 |         18.1 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.952 |       2 |        3 |      59 |      0     |       1     |            1 |         18.1 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         18.2 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0     |       1     |            1 |         18.1 |
| invoice        | invoice_number  |    215 |      209 |       0.981 |       0 |        4 |       6 |      0     |       1     |            1 |         18   |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0     |       1     |            1 |         18   |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.333 |       1     |            1 |         24.8 |
| invoice        | seller_iban     |    165 |      154 |       0.942 |       2 |        7 |      11 |      0     |       1     |            1 |         18.2 |
| invoice        | seller_name     |    203 |      190 |       0.974 |       5 |        0 |      13 |      0.231 |       0.995 |            1 |         18   |
| invoice        | seller_vat_id   |    178 |      176 |       0.989 |       2 |        0 |       2 |      0     |       1     |            1 |         18.1 |
| invoice        | total_gross     |    208 |      205 |       0.976 |       5 |        0 |       3 |      1     |       1     |            1 |         18   |
| invoice        | total_net       |    196 |      196 |       0.969 |       6 |        0 |       0 |    nan     |       1     |            1 |         18.1 |
| invoice        | total_tax       |    188 |      188 |       0.984 |       3 |        0 |       0 |    nan     |       1     |            1 |         18   |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          6.6 |
| receipt        | date            |    148 |      143 |       0.986 |       2 |        0 |       5 |      0     |       1     |            1 |          6.7 |
| receipt        | merchant_name   |    146 |      145 |       0.945 |       8 |        0 |       1 |      1     |       0.993 |            1 |          6.7 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.267 |       1     |            1 |          6.6 |
| receipt        | payment_method  |    119 |      119 |       0.874 |      14 |        1 |       0 |    nan     |       1     |            1 |          6.6 |
| receipt        | subtotal        |    151 |       37 |       0.919 |       3 |        0 |     114 |      0.956 |       1     |            1 |          6.7 |
| receipt        | tax_amount      |    119 |      113 |       0.982 |       2 |        0 |       6 |      0     |       1     |            1 |          6.7 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       0.977 |            1 |          6.6 |
| receipt        | total           |    160 |      160 |       0.931 |      11 |        0 |       0 |    nan     |       1     |            1 |          6.7 |
