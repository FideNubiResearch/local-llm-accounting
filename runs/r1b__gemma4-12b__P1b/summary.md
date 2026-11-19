# r1b__gemma4-12b__P1b

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1b__gemma4-12b__P1b",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.21,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-15 14:32:08"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.893 |       6 |        0 |       0 |    nan     |       0.786 |            1 |         24   |
| invoice        |    865 |     8845 |       0.941 |     411 |      108 |     516 |      0.004 |       0.815 |            1 |         31.8 |
| receipt        |    699 |     4372 |       0.979 |      28 |       64 |     681 |      0.019 |       0.987 |            1 |         22.7 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.893 |       6 |        0 |       0 |    nan     |       0.786 |            1 |         24   |
| invoice        |    861 |     8814 |       0.942 |     407 |      108 |     516 |      0.004 |       0.815 |            1 |         31.8 |
| receipt        |    696 |     4358 |       0.979 |      26 |       64 |     678 |      0.019 |       0.987 |            1 |         22.7 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.961 |      34 |        1 |      56 |      0     |       0.757 |            1 |         31.6 |
| de     | invoice        | real      |     72 |      692 |       0.961 |      11 |       16 |      51 |      0     |       0.926 |            1 |         39.5 |
| de     | receipt        | generated |    160 |     1198 |       0.981 |       9 |       14 |     190 |      0.063 |       1     |            1 |         22.7 |
| en     | bank_statement | generated |      8 |       56 |       0.893 |       6 |        0 |       0 |    nan     |       0.786 |            1 |         24   |
| en     | invoice        | generated |    194 |     1691 |       0.939 |      55 |       48 |      99 |      0     |       0.817 |            1 |         30   |
| en     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.909 |            1 |         30.5 |
| en     | receipt        | generated |     40 |      314 |       0.898 |       0 |       32 |      40 |      0     |       1     |            1 |         22.3 |
| en     | receipt        | real      |     95 |      294 |       0.98  |       3 |        3 |      38 |      0     |       0.993 |            1 |         22.6 |
| es     | invoice        | generated |     80 |      900 |       0.944 |      49 |        1 |      53 |      0     |       0.742 |            1 |         32   |
| fr     | invoice        | generated |     65 |      709 |       0.945 |      39 |        0 |      47 |      0     |       0.953 |            1 |         32.6 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         31.4 |
| fr     | receipt        | generated |    160 |     1212 |       0.998 |       1 |        1 |     178 |      0     |       1     |            1 |         23   |
| id     | receipt        | real      |     54 |      111 |       0.946 |       6 |        0 |      41 |      0     |       0.541 |            1 |         20.7 |
| it     | invoice        | generated |     80 |      908 |       0.945 |      50 |        0 |      42 |      0     |       0.738 |            1 |         33   |
| it     | receipt        | generated |    160 |     1180 |       0.985 |       4 |       14 |     194 |      0.005 |       1     |            1 |         22.6 |
| ko     | receipt        | real      |     30 |       63 |       0.921 |       5 |        0 |       0 |    nan     |       0.921 |            1 |         23.2 |
| nl     | invoice        | generated |     80 |      899 |       0.941 |      50 |        3 |      46 |      0.022 |       0.747 |            1 |         31.9 |
| pl     | invoice        | generated |     80 |      883 |       0.943 |      39 |       11 |      64 |      0     |       0.778 |            1 |         33   |
| pt     | invoice        | generated |     80 |      903 |       0.955 |      39 |        2 |      55 |      0.018 |       0.871 |            1 |         32   |
| pt     | invoice        | real      |     50 |      327 |       0.792 |      42 |       26 |       3 |      0     |       0.987 |            1 |         28.5 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24   |
| bank_statement | account_number  |      8 |        8 |       0.75  |       2 |        0 |       0 |    nan     |       1     |            1 |         24   |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24   |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         23.8 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         24   |
| bank_statement | opening_balance |      6 |        6 |       0.667 |       2 |        0 |       0 |    nan     |       0     |            1 |         24.2 |
| bank_statement | period_end      |      6 |        6 |       0.667 |       2 |        0 |       0 |    nan     |       1     |            1 |         23.8 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         23.8 |
| invoice        | buyer_name      |    774 |      769 |       0.926 |      57 |        0 |       5 |      0     |       1     |            1 |         32   |
| invoice        | buyer_vat_id    |    705 |      428 |       0.904 |      23 |       18 |     277 |      0.004 |       1     |            1 |         31.9 |
| invoice        | currency        |    730 |      730 |       0.985 |       0 |       11 |       0 |    nan     |       1     |            1 |         32.1 |
| invoice        | due_date        |    703 |      609 |       0.993 |       4 |        0 |      94 |      0.011 |       1     |            1 |         32   |
| invoice        | invoice_number  |    860 |      849 |       0.973 |      23 |        0 |      11 |      0     |       1     |            1 |         31.8 |
| invoice        | issue_date      |    860 |      854 |       0.985 |      12 |        1 |       6 |      0     |       1     |            1 |         31.8 |
| invoice        | purchase_order  |     41 |       21 |       1     |       0 |        0 |      20 |      0     |       1     |            1 |         39.5 |
| invoice        | seller_iban     |    709 |      632 |       0.728 |     129 |       43 |      77 |      0     |       1     |            1 |         32.1 |
| invoice        | seller_name     |    827 |      807 |       0.923 |      61 |        1 |      20 |      0     |       0.993 |            1 |         31.9 |
| invoice        | seller_vat_id   |    769 |      766 |       0.893 |      76 |        6 |       3 |      0     |       1     |            1 |         32   |
| invoice        | total_gross     |    845 |      842 |       0.983 |      14 |        0 |       3 |      0     |       0.343 |            1 |         31.9 |
| invoice        | total_net       |    789 |      789 |       0.965 |       6 |       22 |       0 |    nan     |       0.284 |            1 |         32   |
| invoice        | total_tax       |    749 |      749 |       0.984 |       6 |        6 |       0 |    nan     |       0.32  |            1 |         31.9 |
| receipt        | currency        |    520 |      520 |       0.938 |       0 |       32 |       0 |    nan     |       1     |            1 |         22.7 |
| receipt        | date            |    608 |      598 |       1     |       0 |        0 |      10 |      0     |       1     |            1 |         22.7 |
| receipt        | merchant_name   |    599 |      598 |       0.988 |       7 |        0 |       1 |      0     |       0.997 |            1 |         22.7 |
| receipt        | merchant_tax_id |    490 |      376 |       0.981 |       7 |        0 |     114 |      0.026 |       1     |            1 |         22.8 |
| receipt        | payment_method  |    520 |      520 |       0.942 |       1 |       29 |       0 |    nan     |       1     |            1 |         22.7 |
| receipt        | subtotal        |    617 |      103 |       0.981 |       2 |        0 |     514 |      0.019 |       0.841 |            1 |         22.7 |
| receipt        | tax_amount      |    471 |      438 |       0.986 |       3 |        3 |      33 |      0     |       0.972 |            1 |         22.7 |
| receipt        | time            |    565 |      556 |       1     |       0 |        0 |       9 |      0     |       1     |            1 |         22.7 |
| receipt        | total           |    663 |      663 |       0.988 |       8 |        0 |       0 |    nan     |       0.961 |            1 |         22.7 |
