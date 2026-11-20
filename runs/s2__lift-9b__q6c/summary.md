# s2__lift-9b__q6c

```
{
 "model": "mlx-community/lift-oQ6",
 "revision": "8fa369a9f9f3b0eebbf082674d92a2e7c64e5072",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "s2__lift-9b__q6c",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.25,
 "load_peak_gb": 8.258,
 "finished_at": "2026-11-19 19:55:41"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |      nan   |       0.714 |        1     |         22.8 |
| invoice        |     16 |      157 |       0.975 |       4 |        0 |       9 |        0   |       0.764 |        1     |         30.7 |
| receipt        |     15 |       77 |       0.948 |       1 |        3 |      10 |        0.7 |       0.728 |        0.933 |         11.9 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |      nan   |       0.714 |        1     |         22.8 |
| invoice        |     16 |      157 |       0.975 |       4 |        0 |       9 |        0   |       0.764 |        1     |         30.7 |
| receipt        |     15 |       77 |       0.948 |       1 |        3 |      10 |        0.7 |       0.728 |        0.933 |         11.9 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |        0   |       0.727 |            1 |         31.7 |
| de     | invoice        | real      |      1 |       10 |       1     |       0 |        0 |       0 |      nan   |       0.7   |            1 |         53.5 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |        1   |       0.667 |            1 |         10.8 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |      nan   |       0.714 |            1 |         22.8 |
| en     | invoice        | generated |      5 |       41 |       0.976 |       1 |        0 |       4 |        0   |       0.78  |            1 |         27.3 |
| en     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |      nan   |       1     |            1 |         27.5 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |        0.5 |       1     |            1 |         10.7 |
| en     | receipt        | real      |      4 |       10 |       0.8   |       1 |        1 |       2 |        0.5 |       1     |            1 |         18   |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |        0   |       0.727 |            1 |         31.1 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |        0   |       0.7   |            1 |         30.3 |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |      nan   |       0.727 |            1 |         29.2 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |        1   |       0.667 |            1 |         12.3 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |      nan   |       0     |            1 |         16.1 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |      nan   |       0.75  |            1 |         34.1 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |        0.5 |       0.667 |            1 |         10.5 |
| ko     | receipt        | real      |      1 |        2 |       0     |       0 |        2 |       0 |      nan   |     nan     |            0 |         78   |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |        0   |       0.727 |            1 |         32.6 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |      nan   |       0.75  |            1 |         34.1 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |      nan   |       0.75  |            1 |         33.1 |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       1 |        0 |       0 |      nan   |       0.8   |            1 |         25.3 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         22.8 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         22.8 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         22.8 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       0     |        1     |         22.8 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         22.8 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       0     |        1     |         22.8 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         22.7 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         22.7 |
| invoice        | buyer_name      |     14 |       14 |       0.857 |       2 |        0 |       0 |      nan   |       1     |        1     |         31.4 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |        0   |       1     |        1     |         31.9 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         31.9 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |        0   |       1     |        1     |         31.4 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |        0   |       1     |        1     |         30.7 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         30.7 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         29.2 |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |        0   |       1     |        1     |         32   |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |        0   |       0.929 |        1     |         31.1 |
| invoice        | seller_vat_id   |     13 |       13 |       0.923 |       1 |        0 |       0 |      nan   |       1     |        1     |         31.7 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |        0   |       0.2   |        1     |         30.7 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |      nan   |       0.2   |        1     |         31.1 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |      nan   |       0.2   |        1     |         31.1 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         10.8 |
| receipt        | date            |     12 |       12 |       0.917 |       0 |        1 |       0 |      nan   |       1     |        0.917 |         11.1 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         11   |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         11.5 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         10.8 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |        0.7 |       0.222 |        1     |         11.1 |
| receipt        | tax_amount      |     11 |       11 |       0.909 |       0 |        1 |       0 |      nan   |       0.2   |        1     |         11.2 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |      nan   |       1     |        1     |         11   |
| receipt        | total           |     12 |       12 |       0.833 |       1 |        1 |       0 |      nan   |       0.364 |        0.917 |         11.1 |
