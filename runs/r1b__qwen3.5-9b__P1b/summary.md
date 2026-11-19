# r1b__qwen3.5-9b__P1b

```
{
 "model": "mlx-community/Qwen3.5-9B-4bit",
 "revision": "8b2b98c00a6b4d291155e4890773ca8f769aee53",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1b__qwen3.5-9b__P1b",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.34,
 "load_peak_gb": 5.951,
 "finished_at": "2026-11-14 21:11:56"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       1     |       0 |        0 |       0 |    nan     |       0.964 |            1 |         21.6 |
| invoice        |    865 |     8845 |       0.983 |     117 |       35 |     516 |      0.031 |       0.787 |            1 |         29.9 |
| receipt        |    699 |     4372 |       0.959 |     180 |        0 |     681 |      0.783 |       0.792 |            1 |         11.5 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       1     |       0 |        0 |       0 |    nan     |       0.964 |            1 |         21.6 |
| invoice        |    861 |     8814 |       0.983 |     113 |       33 |     516 |      0.031 |       0.787 |            1 |         29.9 |
| receipt        |    696 |     4358 |       0.96  |     176 |        0 |     678 |      0.782 |       0.792 |            1 |         11.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.997 |       3 |        0 |      56 |      0     |       0.741 |            1 |         29.8 |
| de     | invoice        | real      |     72 |      692 |       0.962 |      20 |        6 |      51 |      0.039 |       0.788 |            1 |         38.6 |
| de     | receipt        | generated |    160 |     1198 |       0.952 |      58 |        0 |     190 |      0.842 |       0.752 |            1 |         11.4 |
| en     | bank_statement | generated |      8 |       56 |       1     |       0 |        0 |       0 |    nan     |       0.964 |            1 |         21.6 |
| en     | invoice        | generated |    194 |     1691 |       0.99  |      12 |        5 |      99 |      0.141 |       0.941 |            1 |         25.8 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         26.8 |
| en     | receipt        | generated |     40 |      314 |       1     |       0 |        0 |      40 |      0.35  |       1     |            1 |         11.2 |
| en     | receipt        | real      |     95 |      294 |       0.952 |      14 |        0 |      38 |      0.421 |       0.955 |            1 |         14.3 |
| es     | invoice        | generated |     80 |      900 |       0.996 |       4 |        0 |      53 |      0     |       0.74  |            1 |         30   |
| fr     | invoice        | generated |     65 |      709 |       0.997 |       2 |        0 |      47 |      0     |       0.763 |            1 |         30.2 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.727 |            1 |         27.1 |
| fr     | receipt        | generated |    160 |     1212 |       0.969 |      38 |        0 |     178 |      0.899 |       0.775 |            1 |         11.5 |
| id     | receipt        | real      |     54 |      111 |       0.775 |      25 |        0 |      41 |      0.439 |       0.876 |            1 |         14.7 |
| it     | invoice        | generated |     80 |      908 |       0.993 |       6 |        0 |      42 |      0     |       0.738 |            1 |         30.6 |
| it     | receipt        | generated |    160 |     1180 |       0.964 |      42 |        0 |     194 |      0.851 |       0.743 |            1 |         11.3 |
| ko     | receipt        | real      |     30 |       63 |       0.952 |       3 |        0 |       0 |    nan     |       1     |            1 |         16.5 |
| nl     | invoice        | generated |     80 |      899 |       0.992 |       7 |        0 |      46 |      0     |       0.74  |            1 |         29.9 |
| pl     | invoice        | generated |     80 |      883 |       0.992 |       7 |        0 |      64 |      0     |       0.737 |            1 |         30.5 |
| pt     | invoice        | generated |     80 |      903 |       0.996 |       4 |        0 |      55 |      0     |       0.741 |            1 |         30   |
| pt     | invoice        | real      |     50 |      327 |       0.777 |      49 |       24 |       3 |      0     |       0.812 |            1 |         25.7 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| bank_statement | account_number  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.667 |            1 |         21.6 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.6 |
| invoice        | buyer_name      |    774 |      769 |       0.978 |      17 |        0 |       5 |      0     |       1     |            1 |         30   |
| invoice        | buyer_vat_id    |    705 |      428 |       0.942 |       3 |       22 |     277 |      0     |       1     |            1 |         29.9 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         30   |
| invoice        | due_date        |    703 |      609 |       1     |       0 |        0 |      94 |      0.011 |       0.998 |            1 |         29.9 |
| invoice        | invoice_number  |    860 |      849 |       0.978 |      19 |        0 |      11 |      0.273 |       1     |            1 |         29.9 |
| invoice        | issue_date      |    860 |      854 |       0.998 |       2 |        0 |       6 |      0.167 |       0.999 |            1 |         29.9 |
| invoice        | purchase_order  |     41 |       21 |       0.952 |       1 |        0 |      20 |      0.1   |       1     |            1 |         38.5 |
| invoice        | seller_iban     |    709 |      632 |       0.964 |      16 |        7 |      77 |      0     |       1     |            1 |         30   |
| invoice        | seller_name     |    827 |      807 |       0.975 |      20 |        0 |      20 |      0.4   |       0.994 |            1 |         29.9 |
| invoice        | seller_vat_id   |    769 |      766 |       0.965 |      21 |        6 |       3 |      0     |       1     |            1 |         30   |
| invoice        | total_gross     |    845 |      842 |       0.99  |       8 |        0 |       3 |      0.333 |       0.225 |            1 |         29.9 |
| invoice        | total_net       |    789 |      789 |       0.994 |       5 |        0 |       0 |    nan     |       0.208 |            1 |         30   |
| invoice        | total_tax       |    749 |      749 |       0.993 |       5 |        0 |       0 |    nan     |       0.207 |            1 |         29.9 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.4 |
| receipt        | date            |    608 |      598 |       0.993 |       4 |        0 |      10 |      0.1   |       0.988 |            1 |         11.5 |
| receipt        | merchant_name   |    599 |      598 |       0.968 |      19 |        0 |       1 |      1     |       0.993 |            1 |         11.5 |
| receipt        | merchant_tax_id |    490 |      376 |       0.989 |       4 |        0 |     114 |      0.096 |       1     |            1 |         11.4 |
| receipt        | payment_method  |    520 |      520 |       0.835 |      86 |        0 |       0 |    nan     |       1     |            1 |         11.4 |
| receipt        | subtotal        |    617 |      103 |       0.874 |      13 |        0 |     514 |      1     |       0.394 |            1 |         11.4 |
| receipt        | tax_amount      |    471 |      438 |       0.986 |       6 |        0 |      33 |      0.121 |       0.412 |            1 |         11.3 |
| receipt        | time            |    565 |      556 |       1     |       0 |        0 |       9 |      0.222 |       0.996 |            1 |         11.4 |
| receipt        | total           |    663 |      663 |       0.928 |      48 |        0 |       0 |    nan     |       0.434 |            1 |         11.5 |
