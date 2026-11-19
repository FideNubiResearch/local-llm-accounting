# r2__gemma4-12b__constr

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "r2__gemma4-12b__constr",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.24,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-17 09:59:01"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.885 |       3 |        0 |       0 |    nan     |       0.769 |            1 |         22.5 |
| invoice        |    216 |     2145 |       0.946 |      87 |       28 |     129 |      0     |       0.832 |            1 |         29.4 |
| receipt        |    180 |     1051 |       0.973 |      11 |       17 |     159 |      0.013 |       0.985 |            1 |         20.9 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.885 |       3 |        0 |       0 |    nan     |       0.769 |            1 |         22.5 |
| invoice        |    215 |     2133 |       0.947 |      86 |       28 |     129 |      0     |       0.833 |            1 |         29.4 |
| receipt        |    178 |     1041 |       0.975 |       9 |       17 |     158 |      0.013 |       0.984 |            1 |         20.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.975 |       5 |        0 |      10 |      0     |       0.764 |            1 |         29.3 |
| de     | invoice        | real      |     16 |      158 |       0.962 |       1 |        5 |      10 |      0     |       0.922 |            1 |         43   |
| de     | receipt        | generated |     36 |      268 |       0.996 |       1 |        0 |      44 |      0.045 |       1     |            1 |         21   |
| en     | bank_statement | generated |      4 |       26 |       0.885 |       3 |        0 |       0 |    nan     |       0.769 |            1 |         22.5 |
| en     | invoice        | generated |     61 |      477 |       0.937 |      14 |       16 |      46 |      0     |       0.846 |            1 |         26.5 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.909 |            1 |         28.2 |
| en     | receipt        | generated |     11 |       87 |       0.885 |       0 |       10 |      11 |      0     |       1     |            1 |         20.5 |
| en     | receipt        | real      |     36 |      101 |       0.96  |       2 |        2 |      15 |      0     |       1     |            1 |         20.7 |
| es     | invoice        | generated |     18 |      203 |       0.956 |       9 |        0 |      11 |      0     |       0.749 |            1 |         29.8 |
| fr     | invoice        | generated |     15 |      169 |       0.959 |       7 |        0 |       6 |      0     |       0.964 |            1 |         30.2 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         29   |
| fr     | receipt        | generated |     36 |      270 |       1     |       0 |        0 |      42 |      0     |       1     |            1 |         21.1 |
| id     | receipt        | real      |     17 |       39 |       0.872 |       5 |        0 |       5 |      0     |       0.641 |            1 |         19   |
| it     | invoice        | generated |     18 |      208 |       0.966 |       7 |        0 |       7 |      0     |       0.74  |            1 |         31.2 |
| it     | receipt        | generated |     36 |      270 |       0.974 |       2 |        5 |      42 |      0     |       1     |            1 |         21   |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       0.875 |            1 |         21.6 |
| nl     | invoice        | generated |     18 |      204 |       0.936 |      11 |        2 |       9 |      0     |       0.748 |            1 |         29.8 |
| pl     | invoice        | generated |     18 |      197 |       0.964 |       7 |        0 |      16 |      0     |       0.802 |            1 |         30.9 |
| pt     | invoice        | generated |     18 |      205 |       0.941 |      11 |        1 |      11 |      0     |       0.897 |            1 |         29.7 |
| pt     | invoice        | real      |     12 |       77 |       0.792 |      12 |        4 |       3 |      0     |       1     |            1 |         26   |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         22.5 |
| bank_statement | account_number  |      4 |        4 |       0.75  |       1 |        0 |       0 |    nan     |       1     |            1 |         22.5 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         22.5 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         22.4 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         22.5 |
| bank_statement | opening_balance |      3 |        3 |       0.667 |       1 |        0 |       0 |    nan     |       0     |            1 |         22.7 |
| bank_statement | period_end      |      2 |        2 |       0.5   |       1 |        0 |       0 |    nan     |       1     |            1 |         32.2 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         32.2 |
| invoice        | buyer_name      |    190 |      189 |       0.947 |      10 |        0 |       1 |      0     |       1     |            1 |         29.7 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.952 |       2 |        3 |      59 |      0     |       1     |            1 |         29.7 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29.9 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0     |       1     |            1 |         29.6 |
| invoice        | invoice_number  |    215 |      209 |       0.976 |       5 |        0 |       6 |      0     |       1     |            1 |         29.4 |
| invoice        | issue_date      |    216 |      211 |       0.986 |       3 |        0 |       5 |      0     |       1     |            1 |         29.4 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         39.6 |
| invoice        | seller_iban     |    165 |      154 |       0.753 |      24 |       14 |      11 |      0     |       1     |            1 |         29.9 |
| invoice        | seller_name     |    203 |      190 |       0.889 |      20 |        1 |      13 |      0     |       1     |            1 |         29.6 |
| invoice        | seller_vat_id   |    178 |      176 |       0.898 |      16 |        2 |       2 |      0     |       1     |            1 |         29.8 |
| invoice        | total_gross     |    208 |      205 |       0.985 |       3 |        0 |       3 |      0     |       0.41  |            1 |         29.5 |
| invoice        | total_net       |    196 |      196 |       0.949 |       3 |        7 |       0 |    nan     |       0.367 |            1 |         29.6 |
| invoice        | total_tax       |    188 |      188 |       0.989 |       1 |        1 |       0 |    nan     |       0.385 |            1 |         29.5 |
| receipt        | currency        |    119 |      119 |       0.916 |       0 |       10 |       0 |    nan     |       1     |            1 |         21   |
| receipt        | date            |    148 |      143 |       1     |       0 |        0 |       5 |      0     |       1     |            1 |         21   |
| receipt        | merchant_name   |    146 |      145 |       0.979 |       3 |        0 |       1 |      0     |       1     |            1 |         21   |
| receipt        | merchant_tax_id |    114 |       84 |       0.976 |       2 |        0 |      30 |      0     |       1     |            1 |         21   |
| receipt        | payment_method  |    119 |      119 |       0.958 |       0 |        5 |       0 |    nan     |       1     |            1 |         21   |
| receipt        | subtotal        |    151 |       37 |       0.946 |       2 |        0 |     114 |      0.018 |       0.872 |            1 |         20.8 |
| receipt        | tax_amount      |    119 |      113 |       0.965 |       2 |        2 |       6 |      0     |       0.946 |            1 |         20.8 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         21   |
| receipt        | total           |    160 |      160 |       0.988 |       2 |        0 |       0 |    nan     |       0.969 |            1 |         20.9 |
