# r1b__qwen3.5-4b__P1b

```
{
 "model": "mlx-community/Qwen3.5-4B-4bit",
 "revision": "0e7ffd5c629ef7719d4cbc04069232580bfa9d9c",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1b__qwen3.5-4b__P1b",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.05,
 "load_peak_gb": 3.035,
 "finished_at": "2026-11-14 11:42:57"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.911 |       5 |        0 |       0 |    nan     |       0.768 |            1 |         12.6 |
| invoice        |    865 |     8845 |       0.98  |     146 |       35 |     516 |      0.074 |       0.777 |            1 |         17.5 |
| receipt        |    699 |     4372 |       0.962 |     163 |        2 |     681 |      0.862 |       0.774 |            1 |          6.5 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.911 |       5 |        0 |       0 |    nan     |       0.768 |            1 |         12.6 |
| invoice        |    861 |     8814 |       0.98  |     144 |       35 |     516 |      0.074 |       0.777 |            1 |         17.5 |
| receipt        |    696 |     4358 |       0.963 |     158 |        2 |     678 |      0.861 |       0.774 |            1 |          6.5 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.994 |       5 |        0 |      56 |      0     |       0.741 |            1 |         17.4 |
| de     | invoice        | real      |     72 |      692 |       0.975 |      14 |        3 |      51 |      0.157 |       0.736 |            1 |         22.8 |
| de     | receipt        | generated |    160 |     1198 |       0.947 |      63 |        0 |     190 |      0.911 |       0.761 |            1 |          6.3 |
| en     | bank_statement | generated |      8 |       56 |       0.911 |       5 |        0 |       0 |    nan     |       0.768 |            1 |         12.6 |
| en     | invoice        | generated |    194 |     1691 |       0.988 |      15 |        6 |      99 |      0.162 |       0.909 |            1 |         15   |
| en     | invoice        | real      |      2 |       22 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         15.2 |
| en     | receipt        | generated |     40 |      314 |       1     |       0 |        0 |      40 |      0.525 |       1     |            1 |          6.3 |
| en     | receipt        | real      |     95 |      294 |       0.949 |      14 |        1 |      38 |      0.316 |       0.99  |            1 |          7.9 |
| es     | invoice        | generated |     80 |      900 |       0.989 |       7 |        3 |      53 |      0.019 |       0.744 |            1 |         17.6 |
| fr     | invoice        | generated |     65 |      709 |       0.973 |      19 |        0 |      47 |      0     |       0.756 |            1 |         17.6 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       0.864 |            1 |         15.5 |
| fr     | receipt        | generated |    160 |     1212 |       0.979 |      26 |        0 |     178 |      0.961 |       0.749 |            1 |          6.5 |
| id     | receipt        | real      |     54 |      111 |       0.928 |       8 |        0 |      41 |      0.39  |       0.26  |            1 |          8.4 |
| it     | invoice        | generated |     80 |      908 |       0.991 |       7 |        1 |      42 |      0.024 |       0.736 |            1 |         17.8 |
| it     | receipt        | generated |    160 |     1180 |       0.958 |      49 |        0 |     194 |      1     |       0.754 |            1 |          6.3 |
| ko     | receipt        | real      |     30 |       63 |       0.937 |       3 |        1 |       0 |    nan     |       0.871 |            1 |          9.5 |
| nl     | invoice        | generated |     80 |      899 |       0.99  |       7 |        2 |      46 |      0     |       0.726 |            1 |         17.5 |
| pl     | invoice        | generated |     80 |      883 |       0.995 |       4 |        0 |      64 |      0.141 |       0.749 |            1 |         18.1 |
| pt     | invoice        | generated |     80 |      903 |       0.989 |       7 |        3 |      55 |      0.036 |       0.732 |            1 |         18   |
| pt     | invoice        | real      |     50 |      327 |       0.765 |      60 |       17 |       3 |      0.333 |       0.862 |            1 |         15.1 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       0.875 |       1 |        0 |       0 |    nan     |       1     |            1 |         12.6 |
| bank_statement | account_number  |      8 |        8 |       0.75  |       2 |        0 |       0 |    nan     |       1     |            1 |         12.6 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.6 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.167 |            1 |         12.6 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.6 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         12.7 |
| bank_statement | period_end      |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0.833 |            1 |         12.6 |
| bank_statement | period_start    |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0.833 |            1 |         12.6 |
| invoice        | buyer_name      |    774 |      769 |       0.964 |      28 |        0 |       5 |      0     |       0.999 |            1 |         17.6 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.949 |       5 |       17 |     277 |      0.047 |       1     |            1 |         17.6 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         17.6 |
| invoice        | due_date        |    703 |      609 |       1     |       0 |        0 |      94 |      0     |       0.984 |            1 |         17.6 |
| invoice        | invoice_number  |    860 |      849 |       0.98  |      17 |        0 |      11 |      0.273 |       1     |            1 |         17.5 |
| invoice        | issue_date      |    860 |      854 |       0.998 |       2 |        0 |       6 |      0     |       0.988 |            1 |         17.5 |
| invoice        | purchase_order  |     41 |       21 |       0.952 |       1 |        0 |      20 |      0.05  |       1     |            1 |         22.8 |
| invoice        | seller_iban     |    709 |      632 |       0.962 |       6 |       18 |      77 |      0.091 |       1     |            1 |         17.6 |
| invoice        | seller_name     |    827 |      807 |       0.965 |      28 |        0 |      20 |      0.55  |       0.99  |            1 |         17.6 |
| invoice        | seller_vat_id   |    769 |      766 |       0.965 |      27 |        0 |       3 |      0     |       1     |            1 |         17.6 |
| invoice        | total_gross     |    845 |      842 |       0.983 |      14 |        0 |       3 |      1     |       0.205 |            1 |         17.5 |
| invoice        | total_net       |    789 |      789 |       0.98  |      16 |        0 |       0 |    nan     |       0.172 |            1 |         17.6 |
| invoice        | total_tax       |    749 |      749 |       0.997 |       2 |        0 |       0 |    nan     |       0.178 |            1 |         17.6 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          6.3 |
| receipt        | date            |    608 |      598 |       0.983 |      10 |        0 |      10 |      0.1   |       0.995 |            1 |          6.4 |
| receipt        | merchant_name   |    599 |      598 |       0.943 |      34 |        0 |       1 |      1     |       0.998 |            1 |          6.4 |
| receipt        | merchant_tax_id |    490 |      376 |       0.995 |       2 |        0 |     114 |      0.623 |       1     |            1 |          6.4 |
| receipt        | payment_method  |    520 |      520 |       0.888 |      58 |        0 |       0 |    nan     |       1     |            1 |          6.3 |
| receipt        | subtotal        |    617 |      103 |       0.971 |       3 |        0 |     514 |      0.99  |       0.33  |            1 |          6.4 |
| receipt        | tax_amount      |    471 |      438 |       0.986 |       4 |        2 |      33 |      0.121 |       0.341 |            1 |          6.3 |
| receipt        | time            |    565 |      556 |       1     |       0 |        0 |       9 |      0.111 |       1     |            1 |          6.4 |
| receipt        | total           |    663 |      663 |       0.922 |      52 |        0 |       0 |    nan     |       0.376 |            1 |          6.4 |
