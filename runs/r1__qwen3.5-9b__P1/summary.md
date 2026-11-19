# r1__qwen3.5-9b__P1

```
{
 "model": "mlx-community/Qwen3.5-9B-4bit",
 "revision": "8b2b98c00a6b4d291155e4890773ca8f769aee53",
 "prompt": "P1",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r1__qwen3.5-9b__P1",
 "n_selected": 1574,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.33,
 "load_peak_gb": 5.951,
 "finished_at": "2026-11-12 15:28:25"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      8 |       56 |       1     |       0 |        0 |       0 |    nan     |       0.857 |            1 |         20.2 |
| invoice        |    865 |     8845 |       0.967 |     267 |       24 |     578 |      0.106 |       0.792 |            1 |         28.4 |
| receipt        |    701 |     4373 |       0.969 |     136 |        1 |     709 |      0.817 |       0.781 |            1 |         10.1 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     80 |      889 |       0.98  |      18 |        0 |      56 |      0     |       0.741 |            1 |         28.3 |
| de     | invoice        | real      |     72 |      692 |       0.936 |      40 |        4 |      51 |      0.039 |       0.8   |            1 |         36.8 |
| de     | receipt        | generated |    160 |     1198 |       0.965 |      42 |        0 |     190 |      0.868 |       0.756 |            1 |          9.9 |
| en     | bank_statement | generated |      8 |       56 |       1     |       0 |        0 |       0 |    nan     |       0.857 |            1 |         20.2 |
| en     | invoice        | generated |    194 |     1691 |       0.988 |      20 |        1 |     157 |      0.363 |       0.939 |            1 |         24.4 |
| en     | invoice        | real      |      2 |       22 |       0.818 |       4 |        0 |       0 |    nan     |       1     |            1 |         24.8 |
| en     | receipt        | generated |     40 |      314 |       0.981 |       6 |        0 |      40 |      0.525 |       1     |            1 |          9.8 |
| en     | receipt        | real      |     97 |      296 |       0.916 |      25 |        0 |      59 |      0.508 |       0.966 |            1 |         12.8 |
| es     | invoice        | generated |     80 |      900 |       0.992 |       7 |        0 |      53 |      0     |       0.743 |            1 |         28.6 |
| fr     | invoice        | generated |     65 |      709 |       0.994 |       4 |        0 |      47 |      0     |       0.759 |            1 |         28.7 |
| fr     | invoice        | real      |      2 |       22 |       0.864 |       3 |        0 |       0 |    nan     |       0.727 |            1 |         25.4 |
| fr     | receipt        | generated |    160 |     1212 |       0.977 |      27 |        1 |     178 |      0.904 |       0.748 |            1 |         10   |
| id     | receipt        | real      |     54 |      110 |       0.845 |      17 |        0 |      48 |      0.562 |       0.927 |            1 |         13.1 |
| it     | invoice        | generated |     80 |      908 |       0.976 |      22 |        0 |      42 |      0     |       0.739 |            1 |         29.2 |
| it     | receipt        | generated |    160 |     1180 |       0.986 |      16 |        0 |     194 |      0.902 |       0.715 |            1 |          9.8 |
| ko     | receipt        | real      |     30 |       63 |       0.952 |       3 |        0 |       0 |    nan     |       1     |            1 |         15   |
| nl     | invoice        | generated |     80 |      899 |       0.991 |       8 |        0 |      46 |      0     |       0.74  |            1 |         28.6 |
| pl     | invoice        | generated |     80 |      883 |       0.964 |      32 |        0 |      64 |      0     |       0.744 |            1 |         29.1 |
| pt     | invoice        | generated |     80 |      903 |       0.983 |      15 |        0 |      55 |      0     |       0.751 |            1 |         28.5 |
| pt     | invoice        | real      |     50 |      327 |       0.654 |      94 |       19 |       7 |      0.286 |       0.848 |            1 |         24.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| bank_statement | account_number  |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| bank_statement | bank_name       |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| bank_statement | closing_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.167 |            1 |         20.2 |
| bank_statement | currency        |      8 |        8 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| bank_statement | opening_balance |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       0.5   |            1 |         20.2 |
| bank_statement | period_end      |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| bank_statement | period_start    |      6 |        6 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.2 |
| invoice        | buyer_name      |    774 |      769 |       0.923 |      59 |        0 |       5 |      0     |       1     |            1 |         28.5 |
| invoice        | buyer_vat_id    |    705 |      428 |       0.939 |       7 |       19 |     277 |      0     |       1     |            1 |         28.5 |
| invoice        | currency        |    730 |      730 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         28.6 |
| invoice        | due_date        |    703 |      609 |       0.998 |       1 |        0 |      94 |      0.011 |       0.998 |            1 |         28.5 |
| invoice        | invoice_number  |    860 |      849 |       0.959 |      35 |        0 |      11 |      0.455 |       1     |            1 |         28.4 |
| invoice        | issue_date      |    860 |      854 |       0.993 |       6 |        0 |       6 |      0.333 |       0.999 |            1 |         28.4 |
| invoice        | purchase_order  |     41 |       21 |       0.952 |       1 |        0 |      20 |      0.1   |       1     |            1 |         36.9 |
| invoice        | seller_iban     |    709 |      632 |       0.97  |      18 |        1 |      77 |      0     |       1     |            1 |         28.6 |
| invoice        | seller_name     |    829 |      807 |       0.887 |      91 |        0 |      22 |      0.682 |       1     |            1 |         28.5 |
| invoice        | seller_vat_id   |    769 |      766 |       0.969 |      20 |        4 |       3 |      0     |       1     |            1 |         28.5 |
| invoice        | total_gross     |    855 |      842 |       0.986 |      12 |        0 |      13 |      0.923 |       0.246 |            1 |         28.4 |
| invoice        | total_net       |    804 |      789 |       0.989 |       9 |        0 |      15 |      1     |       0.23  |            1 |         28.5 |
| invoice        | total_tax       |    784 |      749 |       0.989 |       8 |        0 |      35 |      0.257 |       0.227 |            1 |         28.4 |
| receipt        | currency        |    520 |      520 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |          9.9 |
| receipt        | date            |    610 |      598 |       0.983 |      10 |        0 |      12 |      0.083 |       0.987 |            1 |         10   |
| receipt        | merchant_name   |    599 |      598 |       0.945 |      33 |        0 |       1 |      1     |       1     |            1 |         10   |
| receipt        | merchant_tax_id |    490 |      376 |       0.989 |       4 |        0 |     114 |      0.298 |       1     |            1 |          9.9 |
| receipt        | payment_method  |    520 |      520 |       0.952 |      24 |        1 |       0 |    nan     |       1     |            1 |          9.9 |
| receipt        | subtotal        |    620 |      103 |       0.922 |       8 |        0 |     517 |      1     |       0.355 |            1 |          9.9 |
| receipt        | tax_amount      |    476 |      438 |       0.979 |       9 |        0 |      38 |      0.316 |       0.387 |            1 |          9.9 |
| receipt        | time            |    567 |      556 |       1     |       0 |        0 |      11 |      0.182 |       0.996 |            1 |          9.9 |
| receipt        | total           |    680 |      664 |       0.928 |      48 |        0 |      16 |      0.75  |       0.408 |            1 |         10.1 |
