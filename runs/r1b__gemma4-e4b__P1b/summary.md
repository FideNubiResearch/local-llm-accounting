# r1b__gemma4-e4b__P1b

```
{
 "model": "mlx-community/gemma-4-e4b-it-4bit",
 "revision": "475b9088d29754a3379866cf5aeb6b41acd313c2",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1b__gemma4-e4b__P1b",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 3.74,
 "load_peak_gb": 5.149,
 "finished_at": "2026-11-15 02:10:11"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.929 |       3 |        1 |       0 |    nan     |       0.836 |            1 |         10.1 |
| invoice        |    865 |     8845 |       0.882 |     445 |      602 |     516 |      0.025 |       0.961 |            1 |         12.7 |
| receipt        |    699 |     4372 |       0.886 |     186 |      312 |     681 |      0.678 |       0.858 |            1 |          9.5 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.929 |       3 |        1 |       0 |    nan     |       0.836 |            1 |         10.1 |
| invoice        |    861 |     8814 |       0.883 |     443 |      592 |     516 |      0.025 |       0.961 |            1 |         12.7 |
| receipt        |    696 |     4358 |       0.886 |     184 |      311 |     678 |      0.68  |       0.858 |            1 |          9.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.948 |      24 |       22 |      56 |      0     |       0.965 |            1 |         12.8 |
| de     | invoice        | real      |     72 |      692 |       0.724 |      47 |      144 |      51 |      0     |       0.803 |            1 |         16.7 |
| de     | receipt        | generated |    160 |     1198 |       0.891 |      36 |       95 |     190 |      0.816 |       0.754 |            1 |          9.7 |
| en     | bank_statement | generated |      8 |       56 |       0.929 |       3 |        1 |       0 |    nan     |       0.836 |            1 |         10.1 |
| en     | invoice        | generated |    194 |     1691 |       0.918 |      60 |       78 |      99 |      0.071 |       0.97  |            1 |         11.8 |
| en     | invoice        | real      |      2 |       22 |       0.773 |       1 |        4 |       0 |    nan     |       1     |            1 |         11.8 |
| en     | receipt        | generated |     40 |      314 |       0.939 |       4 |       15 |      40 |      0.2   |       1     |            1 |          9.5 |
| en     | receipt        | real      |     95 |      294 |       0.922 |      17 |        6 |      38 |      0.158 |       0.99  |            1 |          9.4 |
| es     | invoice        | generated |     80 |      900 |       0.912 |      41 |       38 |      53 |      0.075 |       0.984 |            1 |         12.8 |
| fr     | invoice        | generated |     65 |      709 |       0.928 |      32 |       19 |      47 |      0     |       1     |            1 |         12.9 |
| fr     | invoice        | real      |      2 |       22 |       0.773 |       3 |        2 |       0 |    nan     |       1     |            1 |         12.1 |
| fr     | receipt        | generated |    160 |     1212 |       0.855 |      36 |      140 |     178 |      0.837 |       0.926 |            1 |          9.5 |
| id     | receipt        | real      |     54 |      111 |       0.757 |      13 |       14 |      41 |      0.049 |       0.374 |            1 |          8.7 |
| it     | invoice        | generated |     80 |      908 |       0.909 |      51 |       32 |      42 |      0.024 |       0.95  |            1 |         13.3 |
| it     | receipt        | generated |    160 |     1180 |       0.911 |      71 |       34 |     194 |      0.732 |       0.869 |            1 |          9.6 |
| ko     | receipt        | real      |     30 |       63 |       0.73  |       9 |        8 |       0 |    nan     |       0.818 |            1 |          9.4 |
| nl     | invoice        | generated |     80 |      899 |       0.909 |      47 |       35 |      46 |      0.022 |       0.946 |            1 |         12.8 |
| pl     | invoice        | generated |     80 |      883 |       0.853 |      61 |       69 |      64 |      0     |       0.973 |            1 |         13   |
| pt     | invoice        | generated |     80 |      903 |       0.918 |      47 |       27 |      55 |      0     |       0.993 |            1 |         12.9 |
| pt     | invoice        | real      |     50 |      327 |       0.502 |      31 |      132 |       3 |      0     |       0.969 |            1 |         10.8 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       0.875 |       0 |        1 |       0 |    nan     |       1     |            1 |         10.1 |
| bank_statement | account_number  |      8 |        8 |       0.875 |       1 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| bank_statement | closing_balance |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0.167 |            1 |         10.1 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| bank_statement | opening_balance |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0.333 |            1 |         10.1 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.1 |
| invoice        | buyer_name      |    774 |      769 |       0.9   |      76 |        1 |       5 |      0     |       1     |            1 |         12.8 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.773 |      15 |       82 |     277 |      0.018 |       1     |            1 |         12.8 |
| invoice        | currency        |    730 |      730 |       0.956 |       2 |       30 |       0 |    nan     |       1     |            1 |         12.9 |
| invoice        | due_date        |    703 |      609 |       0.966 |       8 |       13 |      94 |      0.011 |       1     |            1 |         12.8 |
| invoice        | invoice_number  |    860 |      849 |       0.923 |      38 |       27 |      11 |      0     |       1     |            1 |         12.7 |
| invoice        | issue_date      |    860 |      854 |       0.966 |      29 |        0 |       6 |      0     |       1     |            1 |         12.7 |
| invoice        | purchase_order  |     41 |       21 |       0.429 |       1 |       11 |      20 |      0     |       1     |            1 |         16.7 |
| invoice        | seller_iban     |    709 |      632 |       0.698 |      43 |      148 |      77 |      0     |       1     |            1 |         12.8 |
| invoice        | seller_name     |    827 |      807 |       0.906 |      76 |        0 |      20 |      0.3   |       0.994 |            1 |         12.8 |
| invoice        | seller_vat_id   |    769 |      766 |       0.693 |      43 |      192 |       3 |      0     |       1     |            1 |         12.8 |
| invoice        | total_gross     |    845 |      842 |       0.913 |      54 |       19 |       3 |      0.333 |       0.86  |            1 |         12.8 |
| invoice        | total_net       |    789 |      789 |       0.925 |      41 |       18 |       0 |    nan     |       0.857 |            1 |         12.8 |
| invoice        | total_tax       |    749 |      749 |       0.893 |      19 |       61 |       0 |    nan     |       0.862 |            1 |         12.8 |
| receipt        | currency        |    520 |      520 |       0.975 |       0 |       13 |       0 |    nan     |       1     |            1 |          9.6 |
| receipt        | date            |    608 |      598 |       0.99  |       6 |        0 |      10 |      0     |       1     |            1 |          9.6 |
| receipt        | merchant_name   |    599 |      598 |       0.977 |      13 |        1 |       1 |      1     |       0.993 |            1 |          9.6 |
| receipt        | merchant_tax_id |    490 |      376 |       0.769 |       9 |       78 |     114 |      0     |       1     |            1 |          9.6 |
| receipt        | payment_method  |    520 |      520 |       0.569 |      33 |      191 |       0 |    nan     |       1     |            1 |          9.6 |
| receipt        | subtotal        |    617 |      103 |       0.883 |       6 |        6 |     514 |      0.895 |       0.585 |            1 |          9.5 |
| receipt        | tax_amount      |    471 |      438 |       0.922 |      16 |       18 |      33 |      0.03  |       0.622 |            1 |          9.5 |
| receipt        | time            |    565 |      556 |       0.998 |       0 |        1 |       9 |      0     |       1     |            1 |          9.6 |
| receipt        | total           |    663 |      663 |       0.839 |     103 |        4 |       0 |    nan     |       0.622 |            1 |          9.6 |
