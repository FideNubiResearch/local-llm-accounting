# r1b__qwen3vl-4b__P1b

```
{
 "model": "mlx-community/Qwen3-VL-4B-Instruct-4bit",
 "revision": "2fd8dacbdb8f1e54b8c005f081ec5bf79c56376b",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1b__qwen3vl-4b__P1b",
 "n_selected": 1572,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 1.7,
 "load_peak_gb": 3.095,
 "finished_at": "2026-11-13 20:55:39"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.964 |       2 |        0 |       0 |    nan     |       0.982 |            1 |         12.7 |
| invoice        |    865 |     8845 |       0.961 |     335 |        7 |     516 |      0.172 |       0.817 |            1 |         17.9 |
| receipt        |    699 |     4372 |       0.948 |     225 |        1 |     681 |      0.874 |       0.737 |            1 |          6.2 |

## All without quality=low documents

7 documents tagged quality=low (48 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.964 |       2 |        0 |       0 |    nan     |       0.982 |            1 |         12.7 |
| invoice        |    861 |     8814 |       0.962 |     329 |        7 |     516 |      0.172 |       0.817 |            1 |         17.9 |
| receipt        |    696 |     4358 |       0.949 |     220 |        1 |     678 |      0.873 |       0.737 |            1 |          6.2 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.982 |      16 |        0 |      56 |      0.036 |       0.853 |            1 |         18   |
| de     | invoice        | real      |     72 |      692 |       0.916 |      58 |        0 |      51 |      0.843 |       0.743 |            1 |         24.1 |
| de     | receipt        | generated |    160 |     1198 |       0.933 |      80 |        0 |     190 |      0.958 |       0.69  |            1 |          6   |
| en     | bank_statement | generated |      8 |       56 |       0.964 |       2 |        0 |       0 |    nan     |       0.982 |            1 |         12.7 |
| en     | invoice        | generated |    194 |     1691 |       0.967 |      55 |        0 |      99 |      0.232 |       0.964 |            1 |         15   |
| en     | invoice        | real      |      2 |       22 |       0.864 |       3 |        0 |       0 |    nan     |       1     |            1 |         15.1 |
| en     | receipt        | generated |     40 |      314 |       0.997 |       1 |        0 |      40 |      0.45  |       0.994 |            1 |          5.8 |
| en     | receipt        | real      |     95 |      294 |       0.912 |      26 |        0 |      38 |      0.447 |       0.965 |            1 |          7.7 |
| es     | invoice        | generated |     80 |      900 |       0.983 |      14 |        1 |      53 |      0.057 |       0.798 |            1 |         18.2 |
| fr     | invoice        | generated |     65 |      709 |       0.983 |      11 |        1 |      47 |      0.021 |       0.77  |            1 |         18.1 |
| fr     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       0.727 |            1 |         15.4 |
| fr     | receipt        | generated |    160 |     1212 |       0.964 |      43 |        1 |     178 |      0.91  |       0.684 |            1 |          6.1 |
| id     | receipt        | real      |     54 |      111 |       0.919 |       9 |        0 |      41 |      0.537 |       1     |            1 |          8.1 |
| it     | invoice        | generated |     80 |      908 |       0.956 |      40 |        0 |      42 |      0.048 |       0.771 |            1 |         18.3 |
| it     | receipt        | generated |    160 |     1180 |       0.955 |      53 |        0 |     194 |      1     |       0.689 |            1 |          6   |
| ko     | receipt        | real      |     30 |       63 |       0.794 |      13 |        0 |       0 |    nan     |       0.968 |            1 |          9.3 |
| nl     | invoice        | generated |     80 |      899 |       0.971 |      26 |        0 |      46 |      0.109 |       0.802 |            1 |         17.8 |
| pl     | invoice        | generated |     80 |      883 |       0.975 |      22 |        0 |      64 |      0.078 |       0.74  |            1 |         18.3 |
| pt     | invoice        | generated |     80 |      903 |       0.983 |      15 |        0 |      55 |      0.073 |       0.735 |            1 |         18   |
| pt     | invoice        | real      |     50 |      327 |       0.761 |      73 |        5 |       3 |      0.333 |       0.873 |            1 |         15.5 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | account_number  |      8 |        8 |       0.75  |       2 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.833 |            1 |         12.7 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         12.7 |
| invoice        | buyer_name      |    774 |      769 |       0.904 |      74 |        0 |       5 |      0.2   |       1     |            1 |         18   |
| invoice        | buyer_vat_id    |    705 |      428 |       0.925 |      27 |        5 |     277 |      0.087 |       1     |            1 |         18   |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       0.992 |            1 |         18.1 |
| invoice        | due_date        |    703 |      609 |       0.995 |       3 |        0 |      94 |      0.011 |       0.998 |            1 |         18   |
| invoice        | invoice_number  |    860 |      849 |       0.972 |      24 |        0 |      11 |      0.091 |       1     |            1 |         17.9 |
| invoice        | issue_date      |    860 |      854 |       0.994 |       5 |        0 |       6 |      0     |       0.998 |            1 |         17.9 |
| invoice        | purchase_order  |     41 |       21 |       0.857 |       3 |        0 |      20 |      0.8   |       1     |            1 |         24   |
| invoice        | seller_iban     |    709 |      632 |       0.965 |      20 |        2 |      77 |      0.299 |       1     |            1 |         18.1 |
| invoice        | seller_name     |    827 |      807 |       0.911 |      72 |        0 |      20 |      0.9   |       0.992 |            1 |         18   |
| invoice        | seller_vat_id   |    769 |      766 |       0.945 |      42 |        0 |       3 |      0.667 |       1     |            1 |         18   |
| invoice        | total_gross     |    845 |      842 |       0.963 |      31 |        0 |       3 |      1     |       0.34  |            1 |         18   |
| invoice        | total_net       |    789 |      789 |       0.972 |      22 |        0 |       0 |    nan     |       0.313 |            1 |         18   |
| invoice        | total_tax       |    749 |      749 |       0.984 |      12 |        0 |       0 |    nan     |       0.312 |            1 |         18   |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       0.996 |            1 |          6   |
| receipt        | date            |    608 |      598 |       0.992 |       5 |        0 |      10 |      0.3   |       0.993 |            1 |          6.1 |
| receipt        | merchant_name   |    599 |      598 |       0.977 |      14 |        0 |       1 |      1     |       0.995 |            1 |          6.1 |
| receipt        | merchant_tax_id |    490 |      376 |       0.989 |       4 |        0 |     114 |      0.596 |       1     |            1 |          6   |
| receipt        | payment_method  |    520 |      520 |       0.844 |      80 |        1 |       0 |    nan     |       1     |            1 |          6   |
| receipt        | subtotal        |    617 |      103 |       0.981 |       2 |        0 |     514 |      1     |       0.224 |            1 |          6   |
| receipt        | tax_amount      |    471 |      438 |       0.97  |      13 |        0 |      33 |      0.242 |       0.251 |            1 |          6   |
| receipt        | time            |    565 |      556 |       0.996 |       2 |        0 |       9 |      0.111 |       0.995 |            1 |          6   |
| receipt        | total           |    663 |      663 |       0.842 |     105 |        0 |       0 |    nan     |       0.278 |            1 |          6.1 |
