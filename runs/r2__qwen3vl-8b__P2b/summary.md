# r2__qwen3vl-8b__P2b

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P2b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3vl-8b__P2b",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.94,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-17 19:54:04"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| invoice        |    216 |     2145 |       0.973 |      44 |       13 |     129 |      0.078 |       0.938 |            1 |         48.3 |
| receipt        |    180 |     1051 |       0.982 |      19 |        0 |     159 |      0.742 |       0.957 |            1 |         21.4 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| invoice        |    215 |     2133 |       0.973 |      44 |       13 |     129 |      0.078 |       0.939 |            1 |         48.3 |
| receipt        |    178 |     1041 |       0.984 |      17 |        0 |     158 |      0.741 |       0.957 |            1 |         21.4 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.99  |       2 |        0 |      10 |      0     |       0.956 |            1 |         48.5 |
| de     | invoice        | real      |     16 |      158 |       0.949 |       7 |        1 |      10 |      0.2   |       0.849 |            1 |         67.4 |
| de     | receipt        | generated |     36 |      268 |       0.981 |       5 |        0 |      44 |      0.841 |       0.918 |            1 |         21.6 |
| en     | bank_statement | generated |      4 |       26 |       0.923 |       2 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| en     | invoice        | generated |     61 |      477 |       0.985 |       5 |        2 |      46 |      0.152 |       0.981 |            1 |         41.8 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         43.5 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         20.6 |
| en     | receipt        | real      |     36 |      101 |       0.95  |       5 |        0 |      15 |      0.4   |       1     |            1 |         25.4 |
| es     | invoice        | generated |     18 |      203 |       0.97  |       6 |        0 |      11 |      0     |       0.867 |            1 |         48.4 |
| fr     | invoice        | generated |     15 |      169 |       0.988 |       2 |        0 |       6 |      0     |       0.982 |            1 |         49   |
| fr     | invoice        | real      |      2 |       22 |       0.864 |       2 |        1 |       0 |    nan     |       0.714 |            1 |         44.4 |
| fr     | receipt        | generated |     36 |      270 |       0.989 |       3 |        0 |      42 |      0.857 |       0.948 |            1 |         21.2 |
| id     | receipt        | real      |     17 |       39 |       0.974 |       1 |        0 |       5 |      0.4   |       1     |            1 |         23.3 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.899 |            1 |         50.4 |
| it     | receipt        | generated |     36 |      270 |       0.985 |       4 |        0 |      42 |      0.857 |       0.971 |            1 |         20.8 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       1     |            1 |         26.5 |
| nl     | invoice        | generated |     18 |      204 |       0.99  |       2 |        0 |       9 |      0     |       0.926 |            1 |         49.5 |
| pl     | invoice        | generated |     18 |      197 |       0.985 |       2 |        1 |      16 |      0.062 |       1     |            1 |         49.7 |
| pt     | invoice        | generated |     18 |      205 |       0.99  |       2 |        0 |      11 |      0     |       0.956 |            1 |         48.9 |
| pt     | invoice        | real      |     12 |       77 |       0.74  |      12 |        8 |       3 |      0     |       0.855 |            1 |         41   |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| bank_statement | account_number  |      4 |        4 |       0.5   |       2 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.1 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.7 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.4 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         46.6 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         46.6 |
| invoice        | buyer_name      |    190 |      189 |       0.952 |       9 |        0 |       1 |      0     |       1     |            1 |         48.6 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.933 |       2 |        5 |      59 |      0.017 |       1     |            1 |         48.6 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         49   |
| invoice        | due_date        |    172 |      146 |       0.993 |       1 |        0 |      26 |      0     |       1     |            1 |         48.6 |
| invoice        | invoice_number  |    215 |      209 |       0.962 |       4 |        4 |       6 |      0     |       1     |            1 |         48.3 |
| invoice        | issue_date      |    216 |      211 |       0.995 |       1 |        0 |       5 |      0.6   |       1     |            1 |         48.3 |
| invoice        | purchase_order  |     11 |        8 |       0.875 |       1 |        0 |       3 |      0.667 |       1     |            1 |         58.4 |
| invoice        | seller_iban     |    165 |      154 |       0.981 |       1 |        2 |      11 |      0     |       1     |            1 |         49   |
| invoice        | seller_name     |    203 |      190 |       0.953 |       8 |        1 |      13 |      0.077 |       0.989 |            1 |         48.6 |
| invoice        | seller_vat_id   |    178 |      176 |       0.955 |       8 |        0 |       2 |      0     |       1     |            1 |         48.8 |
| invoice        | total_gross     |    208 |      205 |       0.985 |       3 |        0 |       3 |      1     |       0.784 |            1 |         48.5 |
| invoice        | total_net       |    196 |      196 |       0.974 |       4 |        1 |       0 |    nan     |       0.79  |            1 |         48.6 |
| invoice        | total_tax       |    188 |      188 |       0.989 |       2 |        0 |       0 |    nan     |       0.761 |            1 |         48.5 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.2   |       1     |            1 |         21.3 |
| receipt        | merchant_name   |    146 |      145 |       0.986 |       2 |        0 |       1 |      1     |       1     |            1 |         21.3 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.033 |       1     |            1 |         21.2 |
| receipt        | payment_method  |    119 |      119 |       0.992 |       1 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| receipt        | subtotal        |    151 |       37 |       0.973 |       1 |        0 |     114 |      1     |       0.881 |            1 |         21.2 |
| receipt        | tax_amount      |    119 |      113 |       0.991 |       1 |        0 |       6 |      0.167 |       0.877 |            1 |         21.3 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         21.2 |
| receipt        | total           |    160 |      160 |       0.925 |      12 |        0 |       0 |    nan     |       0.888 |            1 |         21.3 |
