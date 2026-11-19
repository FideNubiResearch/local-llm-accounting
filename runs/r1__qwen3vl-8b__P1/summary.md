# r1__qwen3vl-8b__P1

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P1",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1__qwen3vl-8b__P1",
 "n_selected": 1574,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 2.93,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-12 01:26:50"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.929 |       4 |        0 |       0 |    nan     |       0.982 |            1 |         19.6 |
| invoice        |    865 |     8845 |       0.946 |     436 |       44 |     578 |      0.093 |       0.824 |            1 |         28   |
| receipt        |    701 |     4373 |       0.96  |     173 |        2 |     709 |      0.8   |       0.76  |            1 |          9.1 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.96  |      34 |        2 |      56 |      0     |       0.788 |            1 |         28   |
| de     | invoice        | real      |     72 |      692 |       0.938 |      42 |        1 |      51 |      0.294 |       0.721 |            1 |         37.5 |
| de     | receipt        | generated |    160 |     1198 |       0.967 |      40 |        0 |     190 |      0.853 |       0.693 |            1 |          8.8 |
| en     | bank_statement | generated |      8 |       56 |       0.929 |       4 |        0 |       0 |    nan     |       0.982 |            1 |         19.6 |
| en     | invoice        | generated |    194 |     1691 |       0.97  |      48 |        2 |     157 |      0.21  |       0.951 |            1 |         23.7 |
| en     | invoice        | real      |      2 |       22 |       0.818 |       4 |        0 |       0 |    nan     |       1     |            1 |         24.1 |
| en     | receipt        | generated |     40 |      314 |       0.971 |       8 |        1 |      40 |      0.225 |       1     |            1 |          8.7 |
| en     | receipt        | real      |     97 |      296 |       0.899 |      30 |        0 |      59 |      0.542 |       0.97  |            1 |         11.9 |
| es     | invoice        | generated |     80 |      900 |       0.954 |      38 |        3 |      53 |      0     |       0.76  |            1 |         28.1 |
| fr     | invoice        | generated |     65 |      709 |       0.958 |      27 |        3 |      47 |      0     |       0.87  |            1 |         28.3 |
| fr     | invoice        | real      |      2 |       22 |       0.773 |       4 |        1 |       0 |    nan     |       0.714 |            1 |         24.3 |
| fr     | receipt        | generated |    160 |     1212 |       0.959 |      49 |        1 |     178 |      0.904 |       0.732 |            1 |          9   |
| id     | receipt        | real      |     54 |      110 |       0.955 |       5 |        0 |      48 |      0.542 |       0.949 |            1 |         12   |
| it     | invoice        | generated |     80 |      908 |       0.948 |      43 |        4 |      42 |      0.048 |       0.774 |            1 |         28.7 |
| it     | receipt        | generated |    160 |     1180 |       0.969 |      36 |        0 |     194 |      0.912 |       0.716 |            1 |          9   |
| ko     | receipt        | real      |     30 |       63 |       0.921 |       5 |        0 |       0 |    nan     |       1     |            1 |         14.1 |
| nl     | invoice        | generated |     80 |      899 |       0.954 |      39 |        2 |      46 |      0.043 |       0.78  |            1 |         28   |
| pl     | invoice        | generated |     80 |      883 |       0.956 |      38 |        1 |      64 |      0     |       0.791 |            1 |         28.7 |
| pt     | invoice        | generated |     80 |      903 |       0.953 |      40 |        2 |      55 |      0.018 |       0.847 |            1 |         28.2 |
| pt     | invoice        | real      |     50 |      327 |       0.688 |      79 |       23 |       7 |      0.143 |       0.839 |            1 |         23.6 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.6 |
| bank_statement | account_number  |      8 |        8 |       0.625 |       3 |        0 |       0 |    nan     |       1     |            1 |         19.6 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.6 |
| bank_statement | closing_balance |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0.833 |            1 |         19.6 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.6 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.7 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.6 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         19.6 |
| invoice        | buyer_name      |    774 |      769 |       0.821 |     138 |        0 |       5 |      0.2   |       1     |            1 |         28.1 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.937 |      10 |       17 |     277 |      0.018 |       1     |            1 |         28   |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         28.2 |
| invoice        | due_date        |    703 |      609 |       0.992 |       5 |        0 |      94 |      0     |       0.995 |            1 |         28.1 |
| invoice        | invoice_number  |    860 |      849 |       0.975 |      16 |        5 |      11 |      0     |       1     |            1 |         28   |
| invoice        | issue_date      |    860 |      854 |       0.978 |      19 |        0 |       6 |      0.167 |       0.984 |            1 |         28   |
| invoice        | purchase_order  |     41 |       21 |       0.952 |       1 |        0 |      20 |      0.6   |       1     |            1 |         37.4 |
| invoice        | seller_iban     |    709 |      632 |       0.96  |       9 |       16 |      77 |      0.039 |       1     |            1 |         28.2 |
| invoice        | seller_name     |    829 |      807 |       0.783 |     174 |        1 |      22 |      0.091 |       1     |            1 |         28   |
| invoice        | seller_vat_id   |    769 |      766 |       0.954 |      30 |        5 |       3 |      0     |       1     |            1 |         28.1 |
| invoice        | total_gross     |    855 |      842 |       0.981 |      16 |        0 |      13 |      0.538 |       0.37  |            1 |         28   |
| invoice        | total_net       |    804 |      789 |       0.989 |       9 |        0 |      15 |      0.8   |       0.363 |            1 |         28.1 |
| invoice        | total_tax       |    784 |      749 |       0.988 |       9 |        0 |      35 |      0.314 |       0.349 |            1 |         28   |
| receipt        | currency        |    520 |      520 |       0.998 |       0 |        1 |       0 |    nan     |       1     |            1 |          8.9 |
| receipt        | date            |    610 |      598 |       0.98  |      12 |        0 |      12 |      0.167 |       0.993 |            1 |          9.1 |
| receipt        | merchant_name   |    599 |      598 |       0.943 |      34 |        0 |       1 |      1     |       1     |            1 |          9   |
| receipt        | merchant_tax_id |    490 |      376 |       0.995 |       2 |        0 |     114 |      0.184 |       1     |            1 |          9   |
| receipt        | payment_method  |    520 |      520 |       0.985 |       7 |        1 |       0 |    nan     |       1     |            1 |          8.9 |
| receipt        | subtotal        |    620 |      103 |       0.951 |       5 |        0 |     517 |      1     |       0.294 |            1 |          9   |
| receipt        | tax_amount      |    476 |      438 |       0.989 |       5 |        0 |      38 |      0.289 |       0.316 |            1 |          8.9 |
| receipt        | time            |    567 |      556 |       0.998 |       1 |        0 |      11 |      0.091 |       1     |            1 |          9   |
| receipt        | total           |    680 |      664 |       0.839 |     107 |        0 |      16 |      0.875 |       0.354 |            1 |          9.1 |
