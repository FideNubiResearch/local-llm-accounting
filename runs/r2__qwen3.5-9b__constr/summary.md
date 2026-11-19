# r2__qwen3.5-9b__constr

```
{
 "model": "mlx-community/Qwen3.5-9B-4bit",
 "revision": "8b2b98c00a6b4d291155e4890773ca8f769aee53",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "r2__qwen3.5-9b__constr",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.46,
 "load_peak_gb": 5.951,
 "finished_at": "2026-11-16 16:31:24"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         20.8 |
| invoice        |    216 |     2145 |       0.979 |      38 |        8 |     129 |      0.093 |       0.803 |            1 |         28.3 |
| receipt        |    180 |     1051 |       0.974 |      25 |        2 |     159 |      0.742 |       0.919 |            1 |         10.6 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         20.8 |
| invoice        |    215 |     2133 |       0.979 |      37 |        8 |     129 |      0.093 |       0.803 |            1 |         28.3 |
| receipt        |    178 |     1041 |       0.976 |      23 |        2 |     158 |      0.741 |       0.919 |            1 |         10.6 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.99  |       2 |        0 |      10 |      0     |       0.739 |            1 |         28.2 |
| de     | invoice        | real      |     16 |      158 |       0.949 |       6 |        2 |      10 |      0     |       0.808 |            1 |         43.4 |
| de     | receipt        | generated |     36 |      268 |       0.978 |       6 |        0 |      44 |      0.818 |       0.878 |            1 |         10.3 |
| en     | bank_statement | generated |      4 |       26 |       1     |       0 |        0 |       0 |    nan     |       0.962 |            1 |         20.8 |
| en     | invoice        | generated |     61 |      477 |       0.987 |       6 |        0 |      46 |      0.239 |       0.949 |            1 |         24   |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         24.8 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.273 |       1     |            1 |         10.7 |
| en     | receipt        | real      |     36 |      101 |       0.96  |       3 |        1 |      15 |      0.267 |       0.971 |            1 |         13.1 |
| es     | invoice        | generated |     18 |      203 |       0.995 |       1 |        0 |      11 |      0     |       0.749 |            1 |         28.6 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.763 |            1 |         28.8 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.727 |            1 |         25.3 |
| fr     | receipt        | generated |     36 |      270 |       0.978 |       5 |        1 |      42 |      0.857 |       0.911 |            1 |         10.3 |
| id     | receipt        | real      |     17 |       39 |       0.769 |       9 |        0 |       5 |      0.4   |       1     |            1 |         13.6 |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.74  |            1 |         29.1 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.881 |       0.909 |            1 |         10.2 |
| ko     | receipt        | real      |      8 |       16 |       0.938 |       1 |        0 |       0 |    nan     |       1     |            1 |         15   |
| nl     | invoice        | generated |     18 |      204 |       0.995 |       1 |        0 |       9 |      0     |       0.74  |            1 |         28.5 |
| pl     | invoice        | generated |     18 |      197 |       1     |       0 |        0 |      16 |      0     |       0.741 |            1 |         28.7 |
| pt     | invoice        | generated |     18 |      205 |       1     |       0 |        0 |      11 |      0     |       0.737 |            1 |         28.6 |
| pt     | invoice        | real      |     12 |       77 |       0.688 |      18 |        6 |       3 |      0.333 |       0.917 |            1 |         24.2 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.8 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.8 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.8 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       0.667 |            1 |         20.5 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.8 |
| bank_statement | opening_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.6 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.6 |
| invoice        | buyer_name      |    190 |      189 |       0.995 |       1 |        0 |       1 |      0     |       1     |            1 |         28.5 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.942 |       0 |        6 |      59 |      0     |       1     |            1 |         28.5 |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         28.6 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       0.993 |            1 |         28.5 |
| invoice        | invoice_number  |    215 |      209 |       0.967 |       7 |        0 |       6 |      0.333 |       1     |            1 |         28.3 |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0.2   |       1     |            1 |         28.3 |
| invoice        | purchase_order  |     11 |        8 |       0.875 |       1 |        0 |       3 |      0     |       1     |            1 |         38   |
| invoice        | seller_iban     |    165 |      154 |       0.961 |       6 |        0 |      11 |      0     |       1     |            1 |         28.6 |
| invoice        | seller_name     |    203 |      190 |       0.974 |       5 |        0 |      13 |      0.615 |       0.99  |            1 |         28.4 |
| invoice        | seller_vat_id   |    178 |      176 |       0.938 |       9 |        2 |       2 |      0     |       1     |            1 |         28.5 |
| invoice        | total_gross     |    208 |      205 |       0.98  |       4 |        0 |       3 |      0     |       0.293 |            1 |         28.3 |
| invoice        | total_net       |    196 |      196 |       0.985 |       3 |        0 |       0 |    nan     |       0.276 |            1 |         28.5 |
| invoice        | total_tax       |    188 |      188 |       0.989 |       2 |        0 |       0 |    nan     |       0.293 |            1 |         28.3 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.3 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0     |       0.986 |            1 |         10.4 |
| receipt        | merchant_name   |    146 |      145 |       0.966 |       5 |        0 |       1 |      1     |       1     |            1 |         10.4 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.1   |       1     |            1 |         10.3 |
| receipt        | payment_method  |    119 |      119 |       0.975 |       2 |        1 |       0 |    nan     |       1     |            1 |         10.3 |
| receipt        | subtotal        |    151 |       37 |       0.892 |       4 |        0 |     114 |      1     |       0.775 |            1 |         10.4 |
| receipt        | tax_amount      |    119 |      113 |       0.956 |       4 |        1 |       6 |      0     |       0.777 |            1 |         10.5 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         10.3 |
| receipt        | total           |    160 |      160 |       0.95  |       8 |        0 |       0 |    nan     |       0.788 |            1 |         10.4 |
