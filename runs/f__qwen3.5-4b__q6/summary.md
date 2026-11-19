# f__qwen3.5-4b__q6

```
{
 "model": "mlx-community/Qwen3.5-4B-6bit",
 "revision": "fbb1092aa9daef007603ea9273cd24c225a409f1",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "f__qwen3.5-4b__q6",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.39,
 "load_peak_gb": 4.086,
 "finished_at": "2026-11-19 04:44:29"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.982 |       1 |        0 |       0 |    nan     |       0.857 |            1 |         14.3 |
| invoice        |    865 |     8845 |       0.982 |     129 |       34 |     516 |      0.027 |       0.823 |            1 |         20   |
| receipt        |    699 |     4372 |       0.976 |      95 |        9 |     681 |      0.769 |       0.832 |            1 |          7.9 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.982 |       1 |        0 |       0 |    nan     |       0.857 |            1 |         14.3 |
| invoice        |    861 |     8814 |       0.982 |     127 |       34 |     516 |      0.027 |       0.823 |            1 |         20   |
| receipt        |    696 |     4358 |       0.977 |      93 |        9 |     678 |      0.771 |       0.831 |            1 |          7.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.993 |       6 |        0 |      56 |      0     |       0.764 |            1 |         20   |
| de     | invoice        | real      |     72 |      692 |       0.978 |      13 |        2 |      51 |      0.02  |       0.89  |            1 |         24.9 |
| de     | receipt        | generated |    160 |     1198 |       0.957 |      48 |        3 |     190 |      0.853 |       0.845 |            1 |          7.8 |
| en     | bank_statement | generated |      8 |       56 |       0.982 |       1 |        0 |       0 |    nan     |       0.857 |            1 |         14.3 |
| en     | invoice        | generated |    194 |     1691 |       0.986 |      20 |        4 |      99 |      0.111 |       0.968 |            1 |         17.4 |
| en     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         17.7 |
| en     | receipt        | generated |     40 |      314 |       1     |       0 |        0 |      40 |      0.225 |       1     |            1 |          7.6 |
| en     | receipt        | real      |     95 |      294 |       0.956 |      12 |        1 |      38 |      0.263 |       0.997 |            1 |          9.6 |
| es     | invoice        | generated |     80 |      900 |       0.991 |       3 |        5 |      53 |      0     |       0.759 |            1 |         20.2 |
| fr     | invoice        | generated |     65 |      709 |       0.994 |       4 |        0 |      47 |      0     |       0.817 |            1 |         20.3 |
| fr     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         18.1 |
| fr     | receipt        | generated |    160 |     1212 |       0.989 |      10 |        3 |     178 |      0.882 |       0.808 |            1 |          7.9 |
| id     | receipt        | real      |     54 |      111 |       0.919 |       9 |        0 |      41 |      0.244 |       0.595 |            1 |          9.5 |
| it     | invoice        | generated |     80 |      908 |       0.987 |       9 |        3 |      42 |      0.024 |       0.745 |            1 |         20.6 |
| it     | receipt        | generated |    160 |     1180 |       0.99  |      12 |        0 |     194 |      0.907 |       0.779 |            1 |          7.8 |
| ko     | receipt        | real      |     30 |       63 |       0.905 |       4 |        2 |       0 |    nan     |       1     |            1 |         11   |
| nl     | invoice        | generated |     80 |      899 |       0.991 |       6 |        2 |      46 |      0     |       0.755 |            1 |         20.1 |
| pl     | invoice        | generated |     80 |      883 |       0.994 |       5 |        0 |      64 |      0     |       0.804 |            1 |         20.6 |
| pt     | invoice        | generated |     80 |      903 |       0.986 |       9 |        4 |      55 |      0     |       0.756 |            1 |         20.1 |
| pt     | invoice        | real      |     50 |      327 |       0.792 |      54 |       14 |       3 |      0.333 |       0.911 |            1 |         17.1 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       0.875 |       1 |        0 |       0 |    nan     |       1     |            1 |         14.3 |
| bank_statement | account_number  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.3 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.3 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.333 |            1 |         14.3 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.3 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.333 |            1 |         14.3 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.3 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         14.3 |
| invoice        | buyer_name      |    774 |      769 |       0.961 |      30 |        0 |       5 |      0     |       1     |            1 |         20.2 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.958 |       4 |       14 |     277 |      0.004 |       1     |            1 |         20.1 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| invoice        | due_date        |    703 |      609 |       0.997 |       1 |        1 |      94 |      0     |       0.979 |            1 |         20.1 |
| invoice        | invoice_number  |    860 |      849 |       0.981 |      16 |        0 |      11 |      0.273 |       1     |            1 |         20   |
| invoice        | issue_date      |    860 |      854 |       0.999 |       1 |        0 |       6 |      0     |       0.984 |            1 |         20   |
| invoice        | purchase_order  |     41 |       21 |       0.952 |       1 |        0 |      20 |      0.05  |       1     |            1 |         25.6 |
| invoice        | seller_iban     |    709 |      632 |       0.959 |       7 |       19 |      77 |      0     |       1     |            1 |         20.2 |
| invoice        | seller_name     |    827 |      807 |       0.964 |      29 |        0 |      20 |      0.35  |       0.993 |            1 |         20.1 |
| invoice        | seller_vat_id   |    769 |      766 |       0.977 |      18 |        0 |       3 |      0     |       1     |            1 |         20.2 |
| invoice        | total_gross     |    845 |      842 |       0.985 |      13 |        0 |       3 |      0.667 |       0.376 |            1 |         20.1 |
| invoice        | total_net       |    789 |      789 |       0.992 |       6 |        0 |       0 |    nan     |       0.349 |            1 |         20.1 |
| invoice        | total_tax       |    749 |      749 |       0.996 |       3 |        0 |       0 |    nan     |       0.354 |            1 |         20.1 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          7.8 |
| receipt        | date            |    608 |      598 |       0.99  |       6 |        0 |      10 |      0     |       0.998 |            1 |          7.9 |
| receipt        | merchant_name   |    599 |      598 |       0.952 |      29 |        0 |       1 |      1     |       0.998 |            1 |          7.9 |
| receipt        | merchant_tax_id |    490 |      376 |       0.997 |       1 |        0 |     114 |      0.202 |       1     |            1 |          7.8 |
| receipt        | payment_method  |    520 |      520 |       0.969 |      10 |        6 |       0 |    nan     |       1     |            1 |          7.8 |
| receipt        | subtotal        |    617 |      103 |       0.99  |       1 |        0 |     514 |      0.967 |       0.513 |            1 |          7.8 |
| receipt        | tax_amount      |    471 |      438 |       0.977 |       7 |        3 |      33 |      0.091 |       0.493 |            1 |          7.8 |
| receipt        | time            |    565 |      556 |       1     |       0 |        0 |       9 |      0     |       1     |            1 |          7.8 |
| receipt        | total           |    663 |      663 |       0.938 |      41 |        0 |       0 |    nan     |       0.538 |            1 |          7.9 |
