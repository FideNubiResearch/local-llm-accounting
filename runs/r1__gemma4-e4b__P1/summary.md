# r1__gemma4-e4b__P1

```
{
 "model": "mlx-community/gemma-4-e4b-it-4bit",
 "revision": "475b9088d29754a3379866cf5aeb6b41acd313c2",
 "prompt": "P1",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1__gemma4-e4b__P1",
 "n_selected": 1574,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 3.7,
 "load_peak_gb": 5.149,
 "finished_at": "2026-11-12 20:17:05"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       0.946 |       3 |        0 |       0 |    nan     |       0.804 |            1 |          9.6 |
| invoice        |    865 |     8845 |       0.897 |     496 |      414 |     578 |      0.029 |       0.895 |            1 |         12.4 |
| receipt        |    701 |     4373 |       0.9   |     238 |      201 |     709 |      0.739 |       0.788 |            1 |          9.1 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.96  |      22 |       14 |      56 |      0     |       0.821 |            1 |         12.2 |
| de     | invoice        | real      |     72 |      692 |       0.786 |      58 |       90 |      51 |      0     |       0.704 |            1 |         16.5 |
| de     | receipt        | generated |    160 |     1198 |       0.901 |      34 |       85 |     190 |      0.837 |       0.715 |            1 |          9.1 |
| en     | bank_statement | generated |      8 |       56 |       0.946 |       3 |        0 |       0 |    nan     |       0.804 |            1 |          9.6 |
| en     | invoice        | generated |    194 |     1691 |       0.927 |      64 |       59 |     157 |      0.064 |       0.929 |            1 |         11.9 |
| en     | invoice        | real      |      2 |       22 |       0.773 |       3 |        2 |       0 |    nan     |       1     |            1 |         11.7 |
| en     | receipt        | generated |     40 |      314 |       0.873 |       7 |       33 |      40 |      0.2   |       1     |            1 |          8.8 |
| en     | receipt        | real      |     97 |      296 |       0.885 |      30 |        4 |      59 |      0.407 |       1     |            1 |          9   |
| es     | invoice        | generated |     80 |      900 |       0.936 |      40 |       18 |      53 |      0.019 |       0.914 |            1 |         12.5 |
| fr     | invoice        | generated |     65 |      709 |       0.937 |      35 |       10 |      47 |      0.021 |       0.991 |            1 |         12.7 |
| fr     | invoice        | real      |      2 |       22 |       0.682 |       5 |        2 |       0 |    nan     |       0.85  |            1 |         11.6 |
| fr     | receipt        | generated |    160 |     1212 |       0.885 |      72 |       67 |     178 |      0.888 |       0.842 |            1 |          9.2 |
| id     | receipt        | real      |     54 |      110 |       0.782 |      15 |        9 |      48 |      0.375 |       0.328 |            1 |          8.3 |
| it     | invoice        | generated |     80 |      908 |       0.932 |      46 |       16 |      42 |      0     |       0.865 |            1 |         13   |
| it     | receipt        | generated |    160 |     1180 |       0.942 |      68 |        0 |     194 |      0.809 |       0.75  |            1 |          9.2 |
| ko     | receipt        | real      |     30 |       63 |       0.762 |      12 |        3 |       0 |    nan     |       0.783 |            1 |          8.9 |
| nl     | invoice        | generated |     80 |      899 |       0.919 |      50 |       23 |      46 |      0.043 |       0.846 |            1 |         12.5 |
| pl     | invoice        | generated |     80 |      883 |       0.858 |      66 |       59 |      64 |      0     |       0.927 |            1 |         12.6 |
| pt     | invoice        | generated |     80 |      903 |       0.931 |      49 |       13 |      55 |      0.036 |       0.99  |            1 |         12.5 |
| pt     | invoice        | real      |     50 |      327 |       0.492 |      58 |      108 |       7 |      0.143 |       0.891 |            1 |         10.4 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          9.6 |
| bank_statement | account_number  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          9.6 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          9.6 |
| bank_statement | closing_balance |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0     |            1 |          9.5 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          9.6 |
| bank_statement | opening_balance |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       0.167 |            1 |          9.6 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          9.5 |
| bank_statement | period_start    |      6 |        6 |       0.833 |       1 |        0 |       0 |    nan     |       1     |            1 |          9.5 |
| invoice        | buyer_name      |    774 |      769 |       0.891 |      83 |        1 |       5 |      0     |       1     |            1 |         12.5 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.806 |      19 |       64 |     277 |      0.011 |       1     |            1 |         12.4 |
| invoice        | currency        |    730 |      730 |       0.934 |       1 |       47 |       0 |    nan     |       1     |            1 |         12.5 |
| invoice        | due_date        |    703 |      609 |       0.959 |      16 |        9 |      94 |      0.032 |       1     |            1 |         12.4 |
| invoice        | invoice_number  |    860 |      849 |       0.922 |      39 |       27 |      11 |      0     |       1     |            1 |         12.4 |
| invoice        | issue_date      |    860 |      854 |       0.931 |      59 |        0 |       6 |      0     |       1     |            1 |         12.4 |
| invoice        | purchase_order  |     41 |       21 |       0.429 |       1 |       11 |      20 |      0     |       1     |            1 |         16.5 |
| invoice        | seller_iban     |    709 |      632 |       0.818 |      49 |       66 |      77 |      0     |       1     |            1 |         12.5 |
| invoice        | seller_name     |    829 |      807 |       0.886 |      92 |        0 |      22 |      0.182 |       1     |            1 |         12.4 |
| invoice        | seller_vat_id   |    769 |      766 |       0.728 |      51 |      157 |       3 |      0     |       1     |            1 |         12.4 |
| invoice        | total_gross     |    855 |      842 |       0.945 |      35 |       11 |      13 |      0     |       0.631 |            1 |         12.4 |
| invoice        | total_net       |    804 |      789 |       0.962 |      28 |        2 |      15 |      0.4   |       0.629 |            1 |         12.4 |
| invoice        | total_tax       |    784 |      749 |       0.944 |      23 |       19 |      35 |      0.029 |       0.611 |            1 |         12.4 |
| receipt        | currency        |    520 |      520 |       0.937 |       0 |       33 |       0 |    nan     |       1     |            1 |          9.2 |
| receipt        | date            |    610 |      598 |       0.931 |      41 |        0 |      12 |      0     |       1     |            1 |          9.2 |
| receipt        | merchant_name   |    599 |      598 |       0.97  |      17 |        1 |       1 |      1     |       1     |            1 |          9.2 |
| receipt        | merchant_tax_id |    490 |      376 |       0.96  |      12 |        3 |     114 |      0     |       1     |            1 |          9.2 |
| receipt        | payment_method  |    520 |      520 |       0.679 |      26 |      141 |       0 |    nan     |       1     |            1 |          9.2 |
| receipt        | subtotal        |    620 |      103 |       0.922 |       4 |        4 |     517 |      0.971 |       0.378 |            1 |          9.1 |
| receipt        | tax_amount      |    476 |      438 |       0.952 |      12 |        9 |      38 |      0.158 |       0.437 |            1 |          9   |
| receipt        | time            |    567 |      556 |       0.996 |       2 |        0 |      11 |      0     |       1     |            1 |          9.1 |
| receipt        | total           |    680 |      664 |       0.798 |     124 |       10 |      16 |      0.938 |       0.436 |            1 |          9.1 |
