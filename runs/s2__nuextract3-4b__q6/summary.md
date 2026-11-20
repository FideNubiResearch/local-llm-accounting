# s2__nuextract3-4b__q6

```
{
 "model": "numind/NuExtract3-mlx-6bits",
 "revision": "d0db1bdf8eea7e80fe1c08a0be3972f1f17539df",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "nuextract": true,
 "run_id": "s2__nuextract3-4b__q6",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 0.8,
 "load_peak_gb": 4.086,
 "finished_at": "2026-11-19 19:42:24"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       0.929 |       1 |        0 |       0 |    nan     |       1     |            1 |         12.5 |
| invoice        |     16 |      157 |       0.955 |       7 |        0 |       9 |      0.111 |       0.994 |            1 |         16.9 |
| receipt        |     15 |       77 |       0.935 |       5 |        0 |      10 |      1     |       0.989 |            1 |          6.3 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       0.929 |       1 |        0 |       0 |    nan     |       1     |            1 |         12.5 |
| invoice        |     16 |      157 |       0.955 |       7 |        0 |       9 |      0.111 |       0.994 |            1 |         16.9 |
| receipt        |     15 |       77 |       0.935 |       5 |        0 |      10 |      1     |       0.989 |            1 |          6.3 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       1     |            1 |         17.6 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |     nan    |       1     |            1 |         29.9 |
| de     | receipt        | generated |      2 |       16 |       0.875 |       2 |        0 |       2 |       1    |       1     |            1 |          5.7 |
| en     | bank_statement | generated |      2 |       14 |       0.929 |       1 |        0 |       0 |     nan    |       1     |            1 |         12.5 |
| en     | invoice        | generated |      5 |       41 |       0.902 |       4 |        0 |       4 |       0.25 |       1     |            1 |         14.9 |
| en     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |     nan    |       1     |            1 |         15.2 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |          5.7 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |       1    |       0.917 |            1 |          9.7 |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       1     |            1 |         17.2 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |       0    |       1     |            1 |         16.7 |
| fr     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         15.8 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |          6.6 |
| id     | receipt        | real      |      2 |        5 |       0.8   |       1 |        0 |       0 |     nan    |       1     |            1 |          8.6 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         18.8 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |          5.9 |
| ko     | receipt        | real      |      1 |        2 |       0.5   |       1 |        0 |       0 |     nan    |       1     |            1 |          9.3 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       1     |            1 |         18.1 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         18.9 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         18.3 |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       1 |        0 |       0 |     nan    |       0.8   |            1 |         14.7 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | period_end      |      1 |        1 |       0     |       1 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         12.5 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         17.4 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         17.7 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         17.7 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         17.4 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         16.9 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         16.9 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         15.8 |
| invoice        | seller_iban     |     11 |       10 |       0.8   |       2 |        0 |       1 |          0 |       1     |            1 |         17.7 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       0.929 |            1 |         17.2 |
| invoice        | seller_vat_id   |     13 |       13 |       0.923 |       1 |        0 |       0 |        nan |       1     |            1 |         17.6 |
| invoice        | total_gross     |     16 |       15 |       0.933 |       1 |        0 |       1 |          1 |       1     |            1 |         16.9 |
| invoice        | total_net       |     15 |       15 |       0.867 |       2 |        0 |       0 |        nan |       1     |            1 |         17.2 |
| invoice        | total_tax       |     15 |       15 |       0.933 |       1 |        0 |       0 |        nan |       1     |            1 |         17.2 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          5.9 |
| receipt        | date            |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       1     |            1 |          6   |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          5.9 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          6.1 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          5.9 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       1     |            1 |          6   |
| receipt        | tax_amount      |     11 |       11 |       0.909 |       1 |        0 |       0 |        nan |       1     |            1 |          6.1 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       0.889 |            1 |          5.9 |
| receipt        | total           |     12 |       12 |       0.75  |       3 |        0 |       0 |        nan |       1     |            1 |          6   |
