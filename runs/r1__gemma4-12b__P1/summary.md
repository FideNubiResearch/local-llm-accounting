# r1__gemma4-12b__P1

```
{
 "model": "mlx-community/gemma-4-12B-it-4bit",
 "revision": "73bcf09092aa277861d5a191b989b666f7f32e8f",
 "prompt": "P1",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1__gemma4-12b__P1",
 "n_selected": 1574,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 4.22,
 "load_peak_gb": 6.743,
 "finished_at": "2026-11-13 07:25:08"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.821 |      10 |        0 |       0 |    nan     |       0.786 |            1 |         21.1 |
| invoice        |    865 |     8845 |       0.932 |     478 |      127 |     578 |      0.009 |       0.851 |            1 |         29.1 |
| receipt        |    701 |     4373 |       0.974 |      64 |       51 |     709 |      0.233 |       0.99  |            1 |         20.1 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.962 |      33 |        1 |      56 |      0     |       0.794 |            1 |         28.9 |
| de     | invoice        | real      |     72 |      692 |       0.932 |      30 |       17 |      51 |      0     |       0.97  |            1 |         36.5 |
| de     | receipt        | generated |    160 |     1198 |       0.983 |      18 |        2 |     190 |      0.558 |       1     |            1 |         20.2 |
| en     | bank_statement | generated |      8 |       56 |       0.821 |      10 |        0 |       0 |    nan     |       0.786 |            1 |         21.1 |
| en     | invoice        | generated |    194 |     1691 |       0.94  |      62 |       40 |     157 |      0.019 |       0.856 |            1 |         27.3 |
| en     | invoice        | real      |      2 |       22 |       0.864 |       3 |        0 |       0 |    nan     |       0.909 |            1 |         27.8 |
| en     | receipt        | generated |     40 |      314 |       0.879 |       6 |       32 |      40 |      0     |       1     |            1 |         19.7 |
| en     | receipt        | real      |     97 |      296 |       0.949 |      13 |        2 |      59 |      0.22  |       1     |            1 |         19.8 |
| es     | invoice        | generated |     80 |      900 |       0.948 |      46 |        1 |      53 |      0     |       0.755 |            1 |         29.3 |
| fr     | invoice        | generated |     65 |      709 |       0.942 |      41 |        0 |      47 |      0     |       0.987 |            1 |         30   |
| fr     | invoice        | real      |      2 |       22 |       0.818 |       4 |        0 |       0 |    nan     |       1     |            1 |         28.6 |
| fr     | receipt        | generated |    160 |     1212 |       0.99  |      12 |        0 |     178 |      0.096 |       1     |            1 |         20.3 |
| id     | receipt        | real      |     54 |      110 |       0.9   |       4 |        7 |      48 |      0.125 |       0.624 |            1 |         17.8 |
| it     | invoice        | generated |     80 |      908 |       0.946 |      49 |        0 |      42 |      0     |       0.738 |            1 |         30.3 |
| it     | receipt        | generated |    160 |     1180 |       0.99  |       4 |        8 |     194 |      0.119 |       1     |            1 |         20.1 |
| ko     | receipt        | real      |     30 |       63 |       0.889 |       7 |        0 |       0 |    nan     |       0.968 |            1 |         20.5 |
| nl     | invoice        | generated |     80 |      899 |       0.934 |      55 |        4 |      46 |      0.022 |       0.781 |            1 |         29.2 |
| pl     | invoice        | generated |     80 |      883 |       0.906 |      41 |       42 |      64 |      0     |       0.839 |            1 |         30.2 |
| pt     | invoice        | generated |     80 |      903 |       0.957 |      37 |        2 |      55 |      0.018 |       0.938 |            1 |         29.2 |
| pt     | invoice        | real      |     50 |      327 |       0.703 |      77 |       20 |       7 |      0     |       1     |            1 |         26.1 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | account_number  |      8 |        8 |       0.75  |       2 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0     |            1 |         20.9 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         21.1 |
| bank_statement | opening_balance |      6 |        6 |       0.667 |       2 |        0 |       0 |    nan     |       0     |            1 |         21.3 |
| bank_statement | period_end      |      6 |        6 |       0.667 |       2 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| bank_statement | period_start    |      6 |        6 |       0.333 |       4 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| invoice        | buyer_name      |    774 |      769 |       0.915 |      65 |        0 |       5 |      0     |       1     |            1 |         29.3 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.907 |      24 |       16 |     277 |      0.004 |       1     |            1 |         29.2 |
| invoice        | currency        |    730 |      730 |       0.944 |       0 |       41 |       0 |    nan     |       1     |            1 |         29.4 |
| invoice        | due_date        |    703 |      609 |       0.984 |       9 |        1 |      94 |      0.011 |       1     |            1 |         29.2 |
| invoice        | invoice_number  |    860 |      849 |       0.972 |      23 |        1 |      11 |      0     |       1     |            1 |         29.1 |
| invoice        | issue_date      |    860 |      854 |       0.973 |      22 |        1 |       6 |      0     |       1     |            1 |         29.1 |
| invoice        | purchase_order  |     41 |       21 |       1     |       0 |        0 |      20 |      0     |       1     |            1 |         36.3 |
| invoice        | seller_iban     |    709 |      632 |       0.728 |     127 |       45 |      77 |      0     |       1     |            1 |         29.4 |
| invoice        | seller_name     |    829 |      807 |       0.882 |      94 |        1 |      22 |      0     |       1     |            1 |         29.2 |
| invoice        | seller_vat_id   |    769 |      766 |       0.897 |      73 |        6 |       3 |      0     |       1     |            1 |         29.3 |
| invoice        | total_gross     |    855 |      842 |       0.971 |      24 |        0 |      13 |      0.231 |       0.471 |            1 |         29.1 |
| invoice        | total_net       |    804 |      789 |       0.973 |       8 |       13 |      15 |      0     |       0.433 |            1 |         29.2 |
| invoice        | total_tax       |    784 |      749 |       0.985 |       9 |        2 |      35 |      0     |       0.45  |            1 |         29.1 |
| receipt        | currency        |    520 |      520 |       0.938 |       0 |       32 |       0 |    nan     |       1     |            1 |         20.2 |
| receipt        | date            |    610 |      598 |       0.97  |      18 |        0 |      12 |      0     |       1     |            1 |         20.2 |
| receipt        | merchant_name   |    599 |      598 |       0.978 |      13 |        0 |       1 |      0     |       1     |            1 |         20.2 |
| receipt        | merchant_tax_id |    490 |      376 |       0.979 |       8 |        0 |     114 |      0.026 |       1     |            1 |         20.2 |
| receipt        | payment_method  |    520 |      520 |       0.977 |       2 |       10 |       0 |    nan     |       1     |            1 |         20.2 |
| receipt        | subtotal        |    620 |      103 |       0.961 |       1 |        3 |     517 |      0.292 |       0.944 |            1 |         20.1 |
| receipt        | tax_amount      |    476 |      438 |       0.979 |       5 |        4 |      38 |      0.079 |       0.975 |            1 |         20   |
| receipt        | time            |    567 |      556 |       1     |       0 |        0 |      11 |      0     |       1     |            1 |         20.2 |
| receipt        | total           |    680 |      664 |       0.971 |      17 |        2 |      16 |      0.5   |       0.973 |            1 |         20.1 |
