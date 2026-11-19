# r2__gemma4-12b__P0b

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P0b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__gemma4-12b__P0b",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.3,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-17 01:30:04"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.885 |       3 |        0 |       0 |    nan     |       0.769 |            1 |         24.2 |
| invoice        |    216 |     2145 |       0.949 |      85 |       25 |     129 |      0     |       0.837 |            1 |         31.8 |
| receipt        |    180 |     1051 |       0.973 |      14 |       14 |     159 |      0.006 |       0.986 |            1 |         22.5 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.885 |       3 |        0 |       0 |    nan     |       0.769 |            1 |         24.2 |
| invoice        |    215 |     2133 |       0.949 |      84 |       25 |     129 |      0     |       0.838 |            1 |         31.8 |
| receipt        |    178 |     1041 |       0.975 |      12 |       14 |     158 |      0.006 |       0.985 |            1 |         22.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.98  |       4 |        0 |      10 |      0     |       0.764 |            1 |         31.5 |
| de     | invoice        | real      |     16 |      158 |       0.968 |       0 |        5 |      10 |      0     |       0.922 |            1 |         45   |
| de     | receipt        | generated |     36 |      268 |       0.985 |       2 |        2 |      44 |      0     |       1     |            1 |         22.6 |
| en     | bank_statement | generated |      4 |       26 |       0.885 |       3 |        0 |       0 |    nan     |       0.769 |            1 |         24.2 |
| en     | invoice        | generated |     61 |      477 |       0.935 |      16 |       15 |      46 |      0     |       0.852 |            1 |         29.7 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.909 |            1 |         31.8 |
| en     | receipt        | generated |     11 |       87 |       0.908 |       0 |        8 |      11 |      0     |       1     |            1 |         22.1 |
| en     | receipt        | real      |     36 |      101 |       0.98  |       2 |        0 |      15 |      0     |       1     |            1 |         22.4 |
| es     | invoice        | generated |     18 |      203 |       0.941 |      12 |        0 |      11 |      0     |       0.749 |            1 |         32.1 |
| fr     | invoice        | generated |     15 |      169 |       0.953 |       8 |        0 |       6 |      0     |       0.964 |            1 |         32.8 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         32.6 |
| fr     | receipt        | generated |     36 |      270 |       1     |       0 |        0 |      42 |      0     |       1     |            1 |         22.8 |
| id     | receipt        | real      |     17 |       39 |       0.872 |       5 |        0 |       5 |      0     |       0.641 |            1 |         20.3 |
| it     | invoice        | generated |     18 |      208 |       0.966 |       7 |        0 |       7 |      0     |       0.74  |            1 |         33.3 |
| it     | receipt        | generated |     36 |      270 |       0.974 |       3 |        4 |      42 |      0.024 |       1     |            1 |         22.6 |
| ko     | receipt        | real      |      8 |       16 |       0.875 |       2 |        0 |       0 |    nan     |       0.938 |            1 |         23.9 |
| nl     | invoice        | generated |     18 |      204 |       0.961 |       8 |        0 |       9 |      0     |       0.745 |            1 |         32.3 |
| pl     | invoice        | generated |     18 |      197 |       0.964 |       7 |        0 |      16 |      0     |       0.832 |            1 |         33   |
| pt     | invoice        | generated |     18 |      205 |       0.956 |       9 |        0 |      11 |      0     |       0.912 |            1 |         32.2 |
| pt     | invoice        | real      |     12 |       77 |       0.792 |      11 |        5 |       3 |      0     |       0.986 |            1 |         29.8 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.2 |
| bank_statement | account_number  |      4 |        4 |       0.75  |       1 |        0 |       0 |    nan     |       1     |            1 |         24.2 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.2 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         24.1 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24.2 |
| bank_statement | opening_balance |      3 |        3 |       0.667 |       1 |        0 |       0 |    nan     |       0     |            1 |         24.2 |
| bank_statement | period_end      |      2 |        2 |       0.5   |       1 |        0 |       0 |    nan     |       1     |            1 |         33.7 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.7 |
| invoice        | buyer_name      |    190 |      189 |       0.958 |       8 |        0 |       1 |      0     |       1     |            1 |         32.1 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.952 |       2 |        3 |      59 |      0     |       1     |            1 |         32.1 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.2 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0     |       1     |            1 |         32   |
| invoice        | invoice_number  |    215 |      209 |       0.986 |       3 |        0 |       6 |      0     |       1     |            1 |         31.8 |
| invoice        | issue_date      |    216 |      211 |       0.981 |       4 |        0 |       5 |      0     |       1     |            1 |         31.8 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         41.5 |
| invoice        | seller_iban     |    165 |      154 |       0.747 |      27 |       12 |      11 |      0     |       1     |            1 |         32.2 |
| invoice        | seller_name     |    203 |      190 |       0.889 |      20 |        1 |      13 |      0     |       0.989 |            1 |         32   |
| invoice        | seller_vat_id   |    178 |      176 |       0.909 |      15 |        1 |       2 |      0     |       1     |            1 |         32.2 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      0     |       0.429 |            1 |         32   |
| invoice        | total_net       |    196 |      196 |       0.954 |       3 |        6 |       0 |    nan     |       0.392 |            1 |         32   |
| invoice        | total_tax       |    188 |      188 |       0.984 |       1 |        2 |       0 |    nan     |       0.403 |            1 |         32   |
| receipt        | currency        |    119 |      119 |       0.933 |       0 |        8 |       0 |    nan     |       1     |            1 |         22.6 |
| receipt        | date            |    148 |      143 |       1     |       0 |        0 |       5 |      0     |       1     |            1 |         22.6 |
| receipt        | merchant_name   |    146 |      145 |       0.979 |       3 |        0 |       1 |      0     |       1     |            1 |         22.6 |
| receipt        | merchant_tax_id |    114 |       84 |       0.952 |       4 |        0 |      30 |      0.033 |       1     |            1 |         22.6 |
| receipt        | payment_method  |    119 |      119 |       0.95  |       0 |        6 |       0 |    nan     |       1     |            1 |         22.6 |
| receipt        | subtotal        |    151 |       37 |       0.946 |       2 |        0 |     114 |      0     |       0.865 |            1 |         22.4 |
| receipt        | tax_amount      |    119 |      113 |       0.973 |       3 |        0 |       6 |      0     |       0.956 |            1 |         22.4 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         22.6 |
| receipt        | total           |    160 |      160 |       0.988 |       2 |        0 |       0 |    nan     |       0.969 |            1 |         22.5 |
