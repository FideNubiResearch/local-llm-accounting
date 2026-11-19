# f__gemma4-12b__q6

```
{
 "model": "mlx-community/gemma-4-12B-it-6bit",
 "revision": "2fe53aeb9b8686eefa543a60d6aa364c5b219aac",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "f__gemma4-12b__q6",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 5.73,
 "load_peak_gb": 9.731,
 "finished_at": "2026-11-18 22:22:14"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.982 |       1 |        0 |       0 |    nan     |       0.786 |            1 |         28.1 |
| invoice        |    865 |     8845 |       0.978 |     155 |       44 |     516 |      0.01  |       0.821 |            1 |         38.7 |
| receipt        |    699 |     4372 |       0.996 |      17 |        1 |     681 |      0.018 |       0.996 |            1 |         26.6 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.982 |       1 |        0 |       0 |    nan     |       0.786 |            1 |         28.1 |
| invoice        |    861 |     8814 |       0.978 |     152 |       44 |     516 |      0.01  |       0.821 |            1 |         38.7 |
| receipt        |    696 |     4358 |       0.996 |      15 |        1 |     678 |      0.018 |       0.996 |            1 |         26.6 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.987 |      11 |        1 |      56 |      0     |       0.816 |            1 |         38.4 |
| de     | invoice        | real      |     72 |      692 |       0.977 |       8 |        8 |      51 |      0.02  |       0.999 |            1 |         47   |
| de     | receipt        | generated |    160 |     1198 |       0.998 |       1 |        1 |     190 |      0.011 |       1     |            1 |         26.6 |
| en     | bank_statement | generated |      8 |       56 |       0.982 |       1 |        0 |       0 |    nan     |       0.786 |            1 |         28.1 |
| en     | invoice        | generated |    194 |     1691 |       0.986 |       8 |       16 |      99 |      0.02  |       0.85  |            1 |         36.4 |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         38.3 |
| en     | receipt        | generated |     40 |      314 |       1     |       0 |        0 |      40 |      0     |       1     |            1 |         26.1 |
| en     | receipt        | real      |     95 |      294 |       0.973 |       8 |        0 |      38 |      0.079 |       0.993 |            1 |         26.8 |
| es     | invoice        | generated |     80 |      900 |       0.979 |      18 |        1 |      53 |      0     |       0.763 |            1 |         39.7 |
| fr     | invoice        | generated |     65 |      709 |       0.992 |       6 |        0 |      47 |      0     |       0.865 |            1 |         39.2 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         39.6 |
| fr     | receipt        | generated |    160 |     1212 |       1     |       0 |        0 |     178 |      0.022 |       1     |            1 |         26.9 |
| id     | receipt        | real      |     54 |      111 |       0.937 |       7 |        0 |      41 |      0.049 |       0.876 |            1 |         23.9 |
| it     | invoice        | generated |     80 |      908 |       0.967 |      28 |        2 |      42 |      0     |       0.742 |            1 |         40.8 |
| it     | receipt        | generated |    160 |     1180 |       1     |       0 |        0 |     194 |      0.005 |       1     |            1 |         26.6 |
| ko     | receipt        | real      |     30 |       63 |       0.984 |       1 |        0 |       0 |    nan     |       1     |            1 |         27.3 |
| nl     | invoice        | generated |     80 |      899 |       0.986 |      12 |        1 |      46 |      0     |       0.778 |            1 |         38.8 |
| pl     | invoice        | generated |     80 |      883 |       0.99  |       9 |        0 |      64 |      0     |       0.775 |            1 |         40.4 |
| pt     | invoice        | generated |     80 |      903 |       0.981 |      14 |        3 |      55 |      0     |       0.771 |            1 |         38.9 |
| pt     | invoice        | real      |     50 |      327 |       0.847 |      38 |       12 |       3 |      0.667 |       0.965 |            1 |         34.2 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         28.1 |
| bank_statement | account_number  |      8 |        8 |       0.875 |       1 |        0 |       0 |    nan     |       1     |            1 |         28.1 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         28.1 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         27.9 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         28.1 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         28.4 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.9 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         27.9 |
| invoice        | buyer_name      |    774 |      769 |       0.97  |      23 |        0 |       5 |      0     |       0.999 |            1 |         39   |
| invoice        | buyer_vat_id    |    705 |      428 |       0.958 |       8 |       10 |     277 |      0     |       1     |            1 |         38.9 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         39.2 |
| invoice        | due_date        |    703 |      609 |       0.998 |       1 |        0 |      94 |      0     |       1     |            1 |         38.9 |
| invoice        | invoice_number  |    860 |      849 |       0.987 |      11 |        0 |      11 |      0.091 |       1     |            1 |         38.7 |
| invoice        | issue_date      |    860 |      854 |       0.995 |       4 |        0 |       6 |      0     |       1     |            1 |         38.7 |
| invoice        | purchase_order  |     41 |       21 |       1     |       0 |        0 |      20 |      0.05  |       1     |            1 |         46.6 |
| invoice        | seller_iban     |    709 |      632 |       0.919 |      21 |       30 |      77 |      0     |       1     |            1 |         39.1 |
| invoice        | seller_name     |    827 |      807 |       0.962 |      29 |        2 |      20 |      0.05  |       0.983 |            1 |         38.9 |
| invoice        | seller_vat_id   |    769 |      766 |       0.958 |      30 |        2 |       3 |      0.333 |       1     |            1 |         39   |
| invoice        | total_gross     |    845 |      842 |       0.987 |      11 |        0 |       3 |      0.333 |       0.358 |            1 |         38.8 |
| invoice        | total_net       |    789 |      789 |       0.986 |      11 |        0 |       0 |    nan     |       0.318 |            1 |         39   |
| invoice        | total_tax       |    749 |      749 |       0.992 |       6 |        0 |       0 |    nan     |       0.36  |            1 |         38.9 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         26.6 |
| receipt        | date            |    608 |      598 |       0.998 |       1 |        0 |      10 |      0     |       1     |            1 |         26.7 |
| receipt        | merchant_name   |    599 |      598 |       0.988 |       7 |        0 |       1 |      0     |       0.997 |            1 |         26.7 |
| receipt        | merchant_tax_id |    490 |      376 |       0.997 |       1 |        0 |     114 |      0     |       1     |            1 |         26.7 |
| receipt        | payment_method  |    520 |      520 |       0.998 |       0 |        1 |       0 |    nan     |       1     |            1 |         26.6 |
| receipt        | subtotal        |    617 |      103 |       0.981 |       2 |        0 |     514 |      0.023 |       0.957 |            1 |         26.6 |
| receipt        | tax_amount      |    471 |      438 |       0.995 |       2 |        0 |      33 |      0     |       0.998 |            1 |         26.5 |
| receipt        | time            |    565 |      556 |       1     |       0 |        0 |       9 |      0     |       1     |            1 |         26.6 |
| receipt        | total           |    663 |      663 |       0.994 |       4 |        0 |       0 |    nan     |       0.988 |            1 |         26.6 |
