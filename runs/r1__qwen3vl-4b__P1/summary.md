# r1__qwen3vl-4b__P1

```
{
 "model": "mlx-community/Qwen3-VL-4B-Instruct-4bit",
 "revision": "2fd8dacbdb8f1e54b8c005f081ec5bf79c56376b",
 "prompt": "P1",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1__qwen3vl-4b__P1",
 "n_selected": 1574,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 1.69,
 "load_peak_gb": 3.095,
 "finished_at": "2026-11-11 16:51:16"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.964 |       2 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| invoice        |    865 |     8845 |       0.936 |     537 |       27 |     578 |      0.168 |       0.79  |            1 |         16.8 |
| receipt        |    701 |     4373 |       0.943 |     242 |        6 |     709 |      0.917 |       0.739 |            1 |          5.2 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.964 |      29 |        3 |      56 |      0.018 |       0.756 |            1 |         16.8 |
| de     | invoice        | real      |     72 |      692 |       0.879 |      84 |        0 |      51 |      0.745 |       0.725 |            1 |         23   |
| de     | receipt        | generated |    160 |     1198 |       0.934 |      79 |        0 |     190 |      0.979 |       0.69  |            1 |          5   |
| en     | bank_statement | generated |      8 |       56 |       0.964 |       2 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| en     | invoice        | generated |    194 |     1691 |       0.961 |      64 |        2 |     157 |      0.331 |       0.957 |            1 |         14.1 |
| en     | invoice        | real      |      2 |       22 |       0.773 |       5 |        0 |       0 |    nan     |       1     |            1 |         14.2 |
| en     | receipt        | generated |     40 |      314 |       0.978 |       7 |        0 |      40 |      0.9   |       0.991 |            1 |          5.1 |
| en     | receipt        | real      |     97 |      296 |       0.868 |      39 |        0 |      59 |      0.593 |       0.967 |            1 |          6.9 |
| es     | invoice        | generated |     80 |      900 |       0.957 |      34 |        5 |      53 |      0     |       0.754 |            1 |         16.8 |
| fr     | invoice        | generated |     65 |      709 |       0.979 |      14 |        1 |      47 |      0     |       0.756 |            1 |         17.2 |
| fr     | invoice        | real      |      2 |       22 |       0.818 |       4 |        0 |       0 |    nan     |       0.727 |            1 |         14.5 |
| fr     | receipt        | generated |    160 |     1212 |       0.959 |      44 |        6 |     178 |      0.966 |       0.684 |            1 |          5.1 |
| id     | receipt        | real      |     54 |      110 |       0.891 |      12 |        0 |      48 |      0.562 |       1     |            1 |          7.1 |
| it     | invoice        | generated |     80 |      908 |       0.941 |      52 |        2 |      42 |      0.048 |       0.754 |            1 |         17.1 |
| it     | receipt        | generated |    160 |     1180 |       0.959 |      48 |        0 |     194 |      1     |       0.688 |            1 |          5.1 |
| ko     | receipt        | real      |     30 |       63 |       0.794 |      13 |        0 |       0 |    nan     |       0.952 |            1 |          8.3 |
| nl     | invoice        | generated |     80 |      899 |       0.944 |      49 |        1 |      46 |      0.022 |       0.754 |            1 |         16.8 |
| pl     | invoice        | generated |     80 |      883 |       0.937 |      52 |        4 |      64 |      0     |       0.728 |            1 |         17.6 |
| pt     | invoice        | generated |     80 |      903 |       0.952 |      41 |        2 |      55 |      0.036 |       0.726 |            1 |         17.1 |
| pt     | invoice        | real      |     50 |      327 |       0.645 |     109 |        7 |       7 |      0.143 |       0.838 |            1 |         14.4 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | account_number  |      8 |        8 |       0.75  |       2 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         11.7 |
| invoice        | buyer_name      |    774 |      769 |       0.804 |     151 |        0 |       5 |      0     |       1     |            1 |         16.9 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.916 |      29 |        7 |     277 |      0.022 |       1     |            1 |         16.9 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       0.981 |            1 |         16.9 |
| invoice        | due_date        |    703 |      609 |       0.997 |       2 |        0 |      94 |      0     |       1     |            1 |         16.9 |
| invoice        | invoice_number  |    860 |      849 |       0.963 |      31 |        0 |      11 |      0     |       1     |            1 |         16.8 |
| invoice        | issue_date      |    860 |      854 |       0.985 |      13 |        0 |       6 |      0     |       0.998 |            1 |         16.8 |
| invoice        | purchase_order  |     41 |       21 |       0.857 |       3 |        0 |      20 |      0.7   |       1     |            1 |         23   |
| invoice        | seller_iban     |    709 |      632 |       0.934 |      22 |       20 |      77 |      0.312 |       1     |            1 |         16.9 |
| invoice        | seller_name     |    829 |      807 |       0.791 |     169 |        0 |      22 |      0.864 |       1     |            1 |         16.8 |
| invoice        | seller_vat_id   |    769 |      766 |       0.923 |      59 |        0 |       3 |      0     |       1     |            1 |         16.9 |
| invoice        | total_gross     |    855 |      842 |       0.967 |      28 |        0 |      13 |      0.923 |       0.244 |            1 |         16.8 |
| invoice        | total_net       |    804 |      789 |       0.977 |      18 |        0 |      15 |      0.6   |       0.223 |            1 |         16.9 |
| invoice        | total_tax       |    784 |      749 |       0.984 |      12 |        0 |      35 |      0.371 |       0.224 |            1 |         16.8 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       0.996 |            1 |          5.1 |
| receipt        | date            |    610 |      598 |       0.97  |      18 |        0 |      12 |      0.25  |       0.962 |            1 |          5.1 |
| receipt        | merchant_name   |    599 |      598 |       0.962 |      23 |        0 |       1 |      1     |       1     |            1 |          5.1 |
| receipt        | merchant_tax_id |    490 |      376 |       0.987 |       5 |        0 |     114 |      0.877 |       1     |            1 |          5.1 |
| receipt        | payment_method  |    520 |      520 |       0.865 |      64 |        6 |       0 |    nan     |       1     |            1 |          5.1 |
| receipt        | subtotal        |    620 |      103 |       0.961 |       4 |        0 |     517 |      1     |       0.235 |            1 |          5.1 |
| receipt        | tax_amount      |    476 |      438 |       0.963 |      16 |        0 |      38 |      0.342 |       0.266 |            1 |          5.1 |
| receipt        | time            |    567 |      556 |       0.998 |       1 |        0 |      11 |      0.091 |       0.989 |            1 |          5.1 |
| receipt        | total           |    680 |      664 |       0.833 |     111 |        0 |      16 |      0.938 |       0.302 |            1 |          5.2 |
