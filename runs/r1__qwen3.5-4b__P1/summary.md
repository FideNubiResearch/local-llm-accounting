# r1__qwen3.5-4b__P1

```
{
 "model": "mlx-community/Qwen3.5-4B-4bit",
 "revision": "0e7ffd5c629ef7719d4cbc04069232580bfa9d9c",
 "prompt": "P1",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1__qwen3.5-4b__P1",
 "n_selected": 1574,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.03,
 "load_peak_gb": 3.035,
 "finished_at": "2026-11-12 06:36:37"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.929 |       4 |        0 |       0 |    nan     |       0.714 |        1     |         11.8 |
| invoice        |    865 |     8845 |       0.952 |     392 |       34 |     578 |      0.138 |       0.797 |        1     |         16.6 |
| receipt        |    701 |     4373 |       0.951 |     194 |       19 |     709 |      0.915 |       0.849 |        0.994 |          5.7 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.965 |      31 |        0 |      56 |      0     |       0.745 |        1     |         16.6 |
| de     | invoice        | real      |     72 |      692 |       0.932 |      43 |        4 |      51 |      0.235 |       0.811 |        1     |         21.8 |
| de     | receipt        | generated |    160 |     1198 |       0.951 |      59 |        0 |     190 |      0.963 |       0.838 |        1     |          5.6 |
| en     | bank_statement | generated |      8 |       56 |       0.929 |       4 |        0 |       0 |    nan     |       0.714 |        1     |         11.8 |
| en     | invoice        | generated |    194 |     1691 |       0.979 |      27 |        8 |     157 |      0.357 |       0.935 |        1     |         14.1 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |        1     |         14.2 |
| en     | receipt        | generated |     40 |      314 |       0.981 |       6 |        0 |      40 |      0.95  |       1     |        1     |          5.6 |
| en     | receipt        | real      |     97 |      296 |       0.875 |      26 |       11 |      59 |      0.508 |       1     |        0.969 |          7.4 |
| es     | invoice        | generated |     80 |      900 |       0.966 |      30 |        1 |      53 |      0.019 |       0.74  |        1     |         16.7 |
| fr     | invoice        | generated |     65 |      709 |       0.956 |      31 |        0 |      47 |      0     |       0.76  |        1     |         16.8 |
| fr     | invoice        | real      |      2 |       22 |       0.864 |       3 |        0 |       0 |    nan     |       0.864 |        1     |         14.7 |
| fr     | receipt        | generated |    160 |     1212 |       0.958 |      43 |        8 |     178 |      0.989 |       0.838 |        0.994 |          5.7 |
| id     | receipt        | real      |     54 |      110 |       0.936 |       7 |        0 |      48 |      0.583 |       0.442 |        1     |          7.5 |
| it     | invoice        | generated |     80 |      908 |       0.96  |      35 |        1 |      42 |      0.024 |       0.738 |        1     |         17.1 |
| it     | receipt        | generated |    160 |     1180 |       0.959 |      48 |        0 |     194 |      1     |       0.835 |        1     |          5.6 |
| ko     | receipt        | real      |     30 |       63 |       0.921 |       5 |        0 |       0 |    nan     |       0.968 |        1     |          8.8 |
| nl     | invoice        | generated |     80 |      899 |       0.983 |      14 |        1 |      46 |      0     |       0.735 |        1     |         16.6 |
| pl     | invoice        | generated |     80 |      883 |       0.956 |      39 |        0 |      64 |      0.109 |       0.803 |        1     |         17.1 |
| pt     | invoice        | generated |     80 |      903 |       0.952 |      40 |        3 |      55 |      0.018 |       0.737 |        1     |         16.8 |
| pt     | invoice        | real      |     50 |      327 |       0.654 |      97 |       16 |       7 |      0.286 |       0.875 |        1     |         14.2 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       0.875 |       1 |        0 |       0 |    nan     |       1     |        1     |         11.8 |
| bank_statement | account_number  |      8 |        8 |       0.625 |       3 |        0 |       0 |    nan     |       1     |        1     |         11.8 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         11.8 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.167 |        1     |         11.8 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         11.8 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.167 |        1     |         11.8 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.5   |        1     |         11.8 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.5   |        1     |         11.8 |
| invoice        | buyer_name      |    774 |      769 |       0.858 |     109 |        0 |       5 |      0     |       1     |        1     |         16.7 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.942 |       9 |       16 |     277 |      0.036 |       1     |        1     |         16.7 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |        1     |         16.7 |
| invoice        | due_date        |    703 |      609 |       0.998 |       1 |        0 |      94 |      0     |       0.997 |        1     |         16.7 |
| invoice        | invoice_number  |    860 |      849 |       0.965 |      30 |        0 |      11 |      0.273 |       1     |        1     |         16.7 |
| invoice        | issue_date      |    860 |      854 |       0.987 |      11 |        0 |       6 |      0     |       0.998 |        1     |         16.7 |
| invoice        | purchase_order  |     41 |       21 |       0.952 |       1 |        0 |      20 |      0.05  |       1     |        1     |         21.7 |
| invoice        | seller_iban     |    709 |      632 |       0.959 |       8 |       18 |      77 |      0.13  |       1     |        1     |         16.7 |
| invoice        | seller_name     |    829 |      807 |       0.841 |     128 |        0 |      22 |      0.682 |       1     |        1     |         16.7 |
| invoice        | seller_vat_id   |    769 |      766 |       0.937 |      48 |        0 |       3 |      0.333 |       1     |        1     |         16.7 |
| invoice        | total_gross     |    855 |      842 |       0.97  |      25 |        0 |      13 |      1     |       0.268 |        1     |         16.7 |
| invoice        | total_net       |    804 |      789 |       0.981 |      15 |        0 |      15 |      1     |       0.248 |        1     |         16.7 |
| invoice        | total_tax       |    784 |      749 |       0.991 |       7 |        0 |      35 |      0.343 |       0.25  |        1     |         16.7 |
| receipt        | currency        |    520 |      520 |       0.998 |       0 |        1 |       0 |    nan     |       1     |        0.998 |          5.6 |
| receipt        | date            |    610 |      598 |       0.955 |      25 |        2 |      12 |      0.083 |       0.99  |        0.997 |          5.7 |
| receipt        | merchant_name   |    599 |      598 |       0.893 |      61 |        3 |       1 |      1     |       1     |        0.995 |          5.6 |
| receipt        | merchant_tax_id |    490 |      376 |       0.992 |       2 |        1 |     114 |      0.912 |       1     |        0.998 |          5.6 |
| receipt        | payment_method  |    520 |      520 |       0.913 |      44 |        1 |       0 |    nan     |       1     |        0.998 |          5.6 |
| receipt        | subtotal        |    620 |      103 |       0.951 |       2 |        3 |     517 |      0.998 |       0.555 |        0.994 |          5.6 |
| receipt        | tax_amount      |    476 |      438 |       0.975 |       8 |        3 |      38 |      0.342 |       0.556 |        0.994 |          5.6 |
| receipt        | time            |    567 |      556 |       0.998 |       0 |        1 |      11 |      0.091 |       1     |        0.998 |          5.6 |
| receipt        | total           |    680 |      664 |       0.916 |      52 |        4 |      16 |      0.812 |       0.593 |        0.994 |          5.7 |
