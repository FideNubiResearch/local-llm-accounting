# r1b__qwen3vl-8b__P1b

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1b__qwen3vl-8b__P1b",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.93,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-14 06:12:20"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.946 |       3 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| invoice        |    865 |     8845 |       0.978 |     157 |       42 |     516 |      0.045 |       0.836 |            1 |         29.6 |
| receipt        |    699 |     4372 |       0.979 |      91 |        1 |     681 |      0.784 |       0.74  |            1 |         10.7 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.946 |       3 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| invoice        |    861 |     8814 |       0.978 |     153 |       42 |     516 |      0.045 |       0.836 |            1 |         29.6 |
| receipt        |    696 |     4358 |       0.98  |      86 |        1 |     678 |      0.783 |       0.739 |            1 |         10.7 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.987 |      10 |        2 |      56 |      0     |       0.809 |            1 |         29.6 |
| de     | invoice        | real      |     72 |      692 |       0.973 |      17 |        2 |      51 |      0.235 |       0.714 |            1 |         40   |
| de     | receipt        | generated |    160 |     1198 |       0.968 |      38 |        0 |     190 |      0.847 |       0.687 |            1 |         10.5 |
| en     | bank_statement | generated |      8 |       56 |       0.946 |       3 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| en     | invoice        | generated |    194 |     1691 |       0.987 |      21 |        1 |      99 |      0.081 |       0.953 |            1 |         25.2 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         26.1 |
| en     | receipt        | generated |     40 |      314 |       1     |       0 |        0 |      40 |      0.2   |       1     |            1 |         10.3 |
| en     | receipt        | real      |     95 |      294 |       0.946 |      16 |        0 |      38 |      0.421 |       0.971 |            1 |         13.7 |
| es     | invoice        | generated |     80 |      900 |       0.984 |      10 |        4 |      53 |      0.019 |       0.816 |            1 |         29.8 |
| fr     | invoice        | generated |     65 |      709 |       0.986 |       7 |        3 |      47 |      0     |       0.847 |            1 |         29.9 |
| fr     | invoice        | real      |      2 |       22 |       0.864 |       2 |        1 |       0 |    nan     |       0.714 |            1 |         26   |
| fr     | receipt        | generated |    160 |     1212 |       0.986 |      16 |        1 |     178 |      0.91  |       0.695 |            1 |         10.7 |
| id     | receipt        | real      |     54 |      111 |       0.982 |       2 |        0 |      41 |      0.39  |       0.945 |            1 |         13.7 |
| it     | invoice        | generated |     80 |      908 |       0.99  |       7 |        2 |      42 |      0     |       0.797 |            1 |         30.3 |
| it     | receipt        | generated |    160 |     1180 |       0.989 |      13 |        0 |     194 |      0.881 |       0.692 |            1 |         10.6 |
| ko     | receipt        | real      |     30 |       63 |       0.905 |       6 |        0 |       0 |    nan     |       1     |            1 |         15.8 |
| nl     | invoice        | generated |     80 |      899 |       0.981 |      17 |        0 |      46 |      0     |       0.861 |            1 |         29.6 |
| pl     | invoice        | generated |     80 |      883 |       0.99  |       8 |        1 |      64 |      0.016 |       0.779 |            1 |         30.4 |
| pt     | invoice        | generated |     80 |      903 |       0.986 |      10 |        3 |      55 |      0.018 |       0.824 |            1 |         29.9 |
| pt     | invoice        | real      |     50 |      327 |       0.789 |      46 |       23 |       3 |      0     |       0.829 |            1 |         25.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | account_number  |      8 |        8 |       0.625 |       3 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.3 |
| invoice        | buyer_name      |    774 |      769 |       0.965 |      27 |        0 |       5 |      0     |       1     |            1 |         29.7 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.939 |       8 |       18 |     277 |      0.011 |       1     |            1 |         29.7 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         29.8 |
| invoice        | due_date        |    703 |      609 |       0.992 |       5 |        0 |      94 |      0.011 |       0.998 |            1 |         29.7 |
| invoice        | invoice_number  |    860 |      849 |       0.979 |      14 |        4 |      11 |      0     |       1     |            1 |         29.6 |
| invoice        | issue_date      |    860 |      854 |       0.991 |       8 |        0 |       6 |      0.333 |       0.996 |            1 |         29.6 |
| invoice        | purchase_order  |     41 |       21 |       1     |       0 |        0 |      20 |      0.6   |       1     |            1 |         39.5 |
| invoice        | seller_iban     |    709 |      632 |       0.957 |       9 |       18 |      77 |      0     |       1     |            1 |         29.8 |
| invoice        | seller_name     |    827 |      807 |       0.959 |      33 |        0 |      20 |      0.1   |       0.991 |            1 |         29.7 |
| invoice        | seller_vat_id   |    769 |      766 |       0.963 |      26 |        2 |       3 |      0     |       1     |            1 |         29.7 |
| invoice        | total_gross     |    845 |      842 |       0.987 |      11 |        0 |       3 |      1     |       0.411 |            1 |         29.6 |
| invoice        | total_net       |    789 |      789 |       0.99  |       8 |        0 |       0 |    nan     |       0.397 |            1 |         29.7 |
| invoice        | total_tax       |    749 |      749 |       0.989 |       8 |        0 |       0 |    nan     |       0.387 |            1 |         29.7 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         10.5 |
| receipt        | date            |    608 |      598 |       0.997 |       2 |        0 |      10 |      0.2   |       0.997 |            1 |         10.7 |
| receipt        | merchant_name   |    599 |      598 |       0.99  |       6 |        0 |       1 |      1     |       0.995 |            1 |         10.6 |
| receipt        | merchant_tax_id |    490 |      376 |       0.995 |       2 |        0 |     114 |      0.123 |       1     |            1 |         10.6 |
| receipt        | payment_method  |    520 |      520 |       0.99  |       4 |        1 |       0 |    nan     |       1     |            1 |         10.5 |
| receipt        | subtotal        |    617 |      103 |       0.971 |       3 |        0 |     514 |      0.994 |       0.231 |            1 |         10.6 |
| receipt        | tax_amount      |    471 |      438 |       0.993 |       3 |        0 |      33 |      0.152 |       0.262 |            1 |         10.5 |
| receipt        | time            |    565 |      556 |       0.998 |       1 |        0 |       9 |      0.111 |       1     |            1 |         10.6 |
| receipt        | total           |    663 |      663 |       0.894 |      70 |        0 |       0 |    nan     |       0.288 |            1 |         10.7 |
