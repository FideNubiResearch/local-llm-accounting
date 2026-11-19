# r2__qwen3.5-9b__P2b

```
{
 "model": "mlx-community/Qwen3.5-9B-4bit",
 "revision": "8b2b98c00a6b4d291155e4890773ca8f769aee53",
 "prompt": "P2b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "r2__qwen3.5-9b__P2b",
 "n_selected": 400,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.38,
 "load_peak_gb": 5.951,
 "finished_at": "2026-11-16 14:18:25"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| invoice        |    216 |     2145 |       0.984 |      27 |        7 |     129 |      0.085 |       0.878 |            1 |         46.8 |
| receipt        |    180 |     1051 |       0.979 |      22 |        0 |     159 |      0.736 |       0.876 |            1 |         21.8 |

## All without quality=low documents

3 documents tagged quality=low (23 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| invoice        |    215 |     2133 |       0.985 |      26 |        7 |     129 |      0.085 |       0.878 |            1 |         46.8 |
| receipt        |    178 |     1041 |       0.981 |      20 |        0 |     158 |      0.734 |       0.875 |            1 |         21.8 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |     18 |      203 |       0.995 |       1 |        0 |      10 |      0     |       0.823 |            1 |         49.3 |
| de     | invoice        | real      |     16 |      158 |       0.975 |       4 |        0 |      10 |      0.1   |       0.943 |            1 |         62.4 |
| de     | receipt        | generated |     36 |      268 |       0.985 |       4 |        0 |      44 |      0.818 |       0.826 |            1 |         20.9 |
| en     | bank_statement | generated |      4 |       26 |       0.962 |       1 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| en     | invoice        | generated |     61 |      477 |       0.994 |       3 |        0 |      46 |      0.217 |       0.982 |            1 |         38.5 |
| en     | invoice        | real      |      2 |       22 |       0.909 |       2 |        0 |       0 |    nan     |       1     |            1 |         48.3 |
| en     | receipt        | generated |     11 |       87 |       1     |       0 |        0 |      11 |      0.091 |       1     |            1 |         19.6 |
| en     | receipt        | real      |     36 |      101 |       0.96  |       4 |        0 |      15 |      0.333 |       1     |            1 |         24.8 |
| es     | invoice        | generated |     18 |      203 |       0.995 |       1 |        0 |      11 |      0     |       0.837 |            1 |         48.7 |
| fr     | invoice        | generated |     15 |      169 |       0.994 |       1 |        0 |       6 |      0     |       0.888 |            1 |         45.7 |
| fr     | invoice        | real      |      2 |       22 |       0.955 |       1 |        0 |       0 |    nan     |       1     |            1 |         44   |
| fr     | receipt        | generated |     36 |      270 |       0.985 |       4 |        0 |      42 |      0.857 |       0.807 |            1 |         21.3 |
| id     | receipt        | real      |     17 |       39 |       0.821 |       7 |        0 |       5 |      0.4   |       1     |            1 |         24   |
| it     | invoice        | generated |     18 |      208 |       1     |       0 |        0 |       7 |      0     |       0.812 |            1 |         48.5 |
| it     | receipt        | generated |     36 |      270 |       0.996 |       1 |        0 |      42 |      0.881 |       0.893 |            1 |         20.9 |
| ko     | receipt        | real      |      8 |       16 |       0.875 |       2 |        0 |       0 |    nan     |       1     |            1 |         24.8 |
| nl     | invoice        | generated |     18 |      204 |       0.995 |       1 |        0 |       9 |      0     |       0.814 |            1 |         47.9 |
| pl     | invoice        | generated |     18 |      197 |       1     |       0 |        0 |      16 |      0     |       0.797 |            1 |         49.2 |
| pt     | invoice        | generated |     18 |      205 |       1     |       0 |        0 |      11 |      0     |       0.824 |            1 |         45.5 |
| pt     | invoice        | real      |     12 |       77 |       0.74  |      13 |        7 |       3 |      0     |       0.943 |            1 |         42.6 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| bank_statement | account_number  |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| bank_statement | bank_name       |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| bank_statement | closing_balance |      3 |        3 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| bank_statement | currency        |      4 |        4 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| bank_statement | opening_balance |      3 |        3 |       0.667 |       1 |        0 |       0 |    nan     |       1     |            1 |         34.5 |
| bank_statement | period_end      |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         43.8 |
| bank_statement | period_start    |      2 |        2 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         43.8 |
| invoice        | buyer_name      |    190 |      189 |       0.995 |       1 |        0 |       1 |      0     |       1     |            1 |         48   |
| invoice        | buyer_vat_id    |    163 |      104 |       0.933 |       0 |        7 |      59 |      0     |       1     |            1 |         48   |
| invoice        | currency        |    169 |      169 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         48.5 |
| invoice        | due_date        |    172 |      146 |       1     |       0 |        0 |      26 |      0.038 |       1     |            1 |         47.5 |
| invoice        | invoice_number  |    215 |      209 |       0.971 |       6 |        0 |       6 |      0.167 |       1     |            1 |         46.8 |
| invoice        | issue_date      |    216 |      211 |       1     |       0 |        0 |       5 |      0     |       1     |            1 |         46.8 |
| invoice        | purchase_order  |     11 |        8 |       1     |       0 |        0 |       3 |      0.333 |       1     |            1 |         57.2 |
| invoice        | seller_iban     |    165 |      154 |       0.968 |       5 |        0 |      11 |      0     |       1     |            1 |         48.3 |
| invoice        | seller_name     |    203 |      190 |       0.979 |       4 |        0 |      13 |      0.462 |       0.99  |            1 |         47.5 |
| invoice        | seller_vat_id   |    178 |      176 |       0.955 |       8 |        0 |       2 |      0     |       1     |            1 |         48.2 |
| invoice        | total_gross     |    208 |      205 |       0.99  |       2 |        0 |       3 |      0.667 |       0.565 |            1 |         47.2 |
| invoice        | total_net       |    196 |      196 |       0.995 |       1 |        0 |       0 |    nan     |       0.546 |            1 |         47.7 |
| invoice        | total_tax       |    188 |      188 |       1     |       0 |        0 |       0 |    nan     |       0.564 |            1 |         47.6 |
| receipt        | currency        |    119 |      119 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| receipt        | date            |    148 |      143 |       0.993 |       1 |        0 |       5 |      0.2   |       1     |            1 |         21.3 |
| receipt        | merchant_name   |    146 |      145 |       0.972 |       4 |        0 |       1 |      1     |       1     |            1 |         21.3 |
| receipt        | merchant_tax_id |    114 |       84 |       0.988 |       1 |        0 |      30 |      0.033 |       1     |            1 |         20.9 |
| receipt        | payment_method  |    119 |      119 |       0.983 |       2 |        0 |       0 |    nan     |       1     |            1 |         20.9 |
| receipt        | subtotal        |    151 |       37 |       0.919 |       3 |        0 |     114 |      1     |       0.649 |            1 |         21.2 |
| receipt        | tax_amount      |    119 |      113 |       0.956 |       5 |        0 |       6 |      0     |       0.655 |            1 |         21.2 |
| receipt        | time            |    134 |      131 |       1     |       0 |        0 |       3 |      0     |       1     |            1 |         21   |
| receipt        | total           |    160 |      160 |       0.963 |       6 |        0 |       0 |    nan     |       0.669 |            1 |         21.3 |
