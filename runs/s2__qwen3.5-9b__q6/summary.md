# s2__qwen3.5-9b__q6

```
{
 "model": "mlx-community/Qwen3.5-9B-6bit",
 "revision": "76fe4065e622cf34990d3c13ef80ec8531c9a0f7",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__qwen3.5-9b__q6",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.87,
 "load_peak_gb": 8.189,
 "finished_at": "2026-11-15 18:26:04"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       0.857 |            1 |         24.3 |
| invoice        |     16 |      157 |       0.994 |       1 |        0 |       9 |      0.111 |       0.804 |            1 |         32.9 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       0.966 |            1 |         13.2 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       0.857 |            1 |         24.3 |
| invoice        |     16 |      157 |       0.994 |       1 |        0 |       9 |      0.111 |       0.804 |            1 |         32.9 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       0.966 |            1 |         13.2 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |         1   |       0 |        0 |       1 |       0    |       0.727 |            1 |         34.1 |
| de     | invoice        | real      |      1 |       10 |         0.9 |       1 |        0 |       0 |     nan    |       1     |            1 |         55.4 |
| de     | receipt        | generated |      2 |       16 |         1   |       0 |        0 |       2 |       1    |       0.833 |            1 |         12.4 |
| en     | bank_statement | generated |      2 |       14 |         1   |       0 |        0 |       0 |     nan    |       0.857 |            1 |         24.3 |
| en     | invoice        | generated |      5 |       41 |         1   |       0 |        0 |       4 |       0.25 |       0.857 |            1 |         28.8 |
| en     | invoice        | real      |      1 |       11 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         29.2 |
| en     | receipt        | generated |      2 |       14 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         12.3 |
| en     | receipt        | real      |      4 |       10 |         0.9 |       1 |        0 |       2 |       1    |       1     |            1 |         19.5 |
| es     | invoice        | generated |      1 |       11 |         1   |       0 |        0 |       1 |       0    |       0.727 |            1 |         33.4 |
| fr     | invoice        | generated |      1 |       10 |         1   |       0 |        0 |       2 |       0    |       0.7   |            1 |         32.5 |
| fr     | invoice        | real      |      1 |       11 |         1   |       0 |        0 |       0 |     nan    |       0.727 |            1 |         30.7 |
| fr     | receipt        | generated |      2 |       16 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         13.8 |
| id     | receipt        | real      |      2 |        5 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         17.6 |
| it     | invoice        | generated |      1 |       12 |         1   |       0 |        0 |       0 |     nan    |       0.75  |            1 |         36.4 |
| it     | receipt        | generated |      2 |       14 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         12.6 |
| ko     | receipt        | real      |      1 |        2 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         18.7 |
| nl     | invoice        | generated |      1 |       11 |         1   |       0 |        0 |       1 |       0    |       0.727 |            1 |         35.4 |
| pl     | invoice        | generated |      1 |       12 |         1   |       0 |        0 |       0 |     nan    |       0.75  |            1 |         36.1 |
| pt     | invoice        | generated |      1 |       12 |         1   |       0 |        0 |       0 |     nan    |       0.75  |            1 |         34.9 |
| pt     | invoice        | real      |      1 |        5 |         1   |       0 |        0 |       0 |     nan    |       0.8   |            1 |         27.2 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.3 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.3 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.3 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0.5   |            1 |         24.3 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.3 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0.5   |            1 |         24.3 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.3 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.3 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.6 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         33.9 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.9 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         33.6 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         32.9 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         32.9 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         30.7 |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         34.1 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       0.929 |            1 |         33.4 |
| invoice        | seller_vat_id   |     13 |       13 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.7 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          1 |       0.375 |            1 |         32.9 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.333 |            1 |         33.4 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.333 |            1 |         33.4 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.6 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.7 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.6 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.9 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.6 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       0.917 |            1 |         12.7 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       0.909 |            1 |         12.7 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.6 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.917 |            1 |         12.7 |
