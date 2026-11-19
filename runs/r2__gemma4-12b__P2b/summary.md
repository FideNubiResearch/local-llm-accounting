# r2__gemma4-12b__P2b

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P2b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__gemma4-12b__P2b",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.21,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-17 07:08:40"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.885 |       3 |        0 |       0 |        nan |       0.808 |        1     |         42.5 |
| invoice        |    216 |     2145 |       0.932 |      93 |       52 |     129 |          0 |       0.893 |        0.991 |         60.5 |
| receipt        |    180 |     1051 |       0.976 |      14 |       11 |     159 |          0 |       0.998 |        1     |         39.9 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.885 |       3 |        0 |       0 |        nan |       0.808 |        1     |         42.5 |
| invoice        |    215 |     2133 |       0.932 |      93 |       52 |     129 |          0 |       0.894 |        0.991 |         60.5 |
| receipt        |    178 |     1041 |       0.978 |      12 |       11 |     158 |          0 |       0.998 |        1     |         39.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.975 |       5 |        0 |      10 |          0 |       0.852 |        1     |         60.3 |
| de     | invoice        | real      |     16 |      158 |       0.842 |       0 |       25 |      10 |          0 |       0.947 |        0.875 |         75.9 |
| de     | receipt        | generated |     36 |      268 |       0.993 |       2 |        0 |      44 |          0 |       1     |        1     |         40.2 |
| en     | bank_statement | generated |      4 |       26 |       0.885 |       3 |        0 |       0 |        nan |       0.808 |        1     |         42.5 |
| en     | invoice        | generated |     61 |      477 |       0.925 |      15 |       21 |      46 |          0 |       0.897 |        1     |         55.8 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |        nan |       1     |        1     |         61.3 |
| en     | receipt        | generated |     11 |       87 |       0.943 |       0 |        5 |      11 |          0 |       1     |        1     |         40.7 |
| en     | receipt        | real      |     36 |      101 |       0.95  |       2 |        3 |      15 |          0 |       1     |        1     |         39.5 |
| es     | invoice        | generated |     18 |      203 |       0.946 |      11 |        0 |      11 |          0 |       0.778 |        1     |         60.9 |
| fr     | invoice        | generated |     15 |      169 |       0.953 |       8 |        0 |       6 |          0 |       1     |        1     |         61.5 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |        nan |       1     |        1     |         64.8 |
| fr     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |          0 |       1     |        1     |         40.3 |
| id     | receipt        | real      |     17 |       39 |       0.821 |       5 |        2 |       5 |          0 |       0.973 |        1     |         36   |
| it     | invoice        | generated |     18 |      208 |       0.962 |       8 |        0 |       7 |          0 |       0.755 |        1     |         63   |
| it     | receipt        | generated |     36 |      270 |       0.993 |       2 |        0 |      42 |          0 |       1     |        1     |         40.1 |
| ko     | receipt        | real      |      8 |       16 |       0.812 |       2 |        1 |       0 |        nan |       0.933 |        1     |         40.1 |
| nl     | invoice        | generated |     18 |      204 |       0.961 |       8 |        0 |       9 |          0 |       0.863 |        1     |         60.9 |
| pl     | invoice        | generated |     18 |      197 |       0.949 |      10 |        0 |      16 |          0 |       0.939 |        1     |         62   |
| pt     | invoice        | generated |     18 |      205 |       0.941 |      12 |        0 |      11 |          0 |       0.985 |        1     |         60.9 |
| pt     | invoice        | real      |     12 |       77 |       0.753 |      13 |        6 |       3 |          0 |       0.986 |        1     |         54.8 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |        1     |         42.5 |
| bank_statement | account_number  |      4 |        4 |       0.75  |       1 |        0 |       0 |        nan |       1     |        1     |         42.5 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |        1     |         42.5 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |        nan |       0     |        1     |         42.5 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |        1     |         42.5 |
| bank_statement | opening_balance |      3 |        3 |       0.667 |       1 |        0 |       0 |        nan |       0.333 |        1     |         42.5 |
| bank_statement | period_end      |      2 |        2 |       0.5   |       1 |        0 |       0 |        nan |       1     |        1     |         51.7 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |        1     |         51.7 |
| invoice        | buyer_name      |    190 |      189 |       0.937 |      10 |        2 |       1 |          0 |       1     |        0.989 |         60.8 |
| invoice        | buyer_vat_id    |    163 |      104 |       0.942 |       3 |        3 |      59 |          0 |       1     |        1     |         60.8 |
| invoice        | currency        |    169 |      169 |       0.988 |       0 |        2 |       0 |        nan |       1     |        0.988 |         61   |
| invoice        | due_date        |    172 |      146 |       0.993 |       0 |        1 |      26 |          0 |       1     |        0.994 |         60.7 |
| invoice        | invoice_number  |    215 |      209 |       0.967 |       5 |        2 |       6 |          0 |       1     |        0.991 |         60.5 |
| invoice        | issue_date      |    216 |      211 |       0.976 |       3 |        2 |       5 |          0 |       1     |        0.991 |         60.5 |
| invoice        | purchase_order  |     11 |        8 |       0.875 |       0 |        1 |       3 |          0 |       1     |        0.818 |         78.7 |
| invoice        | seller_iban     |    165 |      154 |       0.74  |      27 |       13 |      11 |          0 |       1     |        0.988 |         61   |
| invoice        | seller_name     |    203 |      190 |       0.9   |      17 |        2 |      13 |          0 |       0.995 |        0.99  |         60.7 |
| invoice        | seller_vat_id   |    178 |      176 |       0.875 |      19 |        3 |       2 |          0 |       1     |        0.989 |         60.9 |
| invoice        | total_gross     |    208 |      205 |       0.985 |       1 |        2 |       3 |          0 |       0.631 |        0.99  |         60.6 |
| invoice        | total_net       |    196 |      196 |       0.908 |       4 |       14 |       0 |        nan |       0.599 |        0.99  |         60.7 |
| invoice        | total_tax       |    188 |      188 |       0.952 |       4 |        5 |       0 |        nan |       0.59  |        0.989 |         60.6 |
| receipt        | currency        |    119 |      119 |       0.958 |       0 |        5 |       0 |        nan |       1     |        1     |         40.2 |
| receipt        | date            |    148 |      143 |       1     |       0 |        0 |       5 |          0 |       1     |        1     |         40.2 |
| receipt        | merchant_name   |    146 |      145 |       0.979 |       3 |        0 |       1 |          0 |       1     |        1     |         40.2 |
| receipt        | merchant_tax_id |    114 |       84 |       0.952 |       4 |        0 |      30 |          0 |       1     |        1     |         40.2 |
| receipt        | payment_method  |    119 |      119 |       1     |       0 |        0 |       0 |        nan |       1     |        1     |         40.2 |
| receipt        | subtotal        |    151 |       37 |       0.919 |       2 |        1 |     114 |          0 |       1     |        1     |         39.9 |
| receipt        | tax_amount      |    119 |      113 |       0.947 |       2 |        4 |       6 |          0 |       0.991 |        1     |         39.9 |
| receipt        | time            |    134 |      131 |       0.992 |       0 |        1 |       3 |          0 |       1     |        1     |         40.1 |
| receipt        | total           |    160 |      160 |       0.981 |       3 |        0 |       0 |        nan |       0.994 |        1     |         40   |
