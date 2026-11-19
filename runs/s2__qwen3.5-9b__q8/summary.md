# s2__qwen3.5-9b__q8

```
{
 "model": "mlx-community/Qwen3.5-9B-8bit",
 "revision": "16daa4818c54ce5f5436f929d52542eb65bbed9d",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__qwen3.5-9b__q8",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 4.65,
 "load_peak_gb": 10.427,
 "finished_at": "2026-11-15 18:51:50"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         26.6 |
| invoice        |     16 |      157 |       0.994 |       1 |        0 |       9 |      0.111 |       0.804 |            1 |         36.5 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       1     |            1 |         15.7 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         26.6 |
| invoice        |     16 |      157 |       0.994 |       1 |        0 |       9 |      0.111 |       0.804 |            1 |         36.5 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       1     |            1 |         15.7 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |         1   |       0 |        0 |       1 |       0    |       0.727 |            1 |         37.9 |
| de     | invoice        | real      |      1 |       10 |         0.9 |       1 |        0 |       0 |     nan    |       1     |            1 |         60.1 |
| de     | receipt        | generated |      2 |       16 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         14.4 |
| en     | bank_statement | generated |      2 |       14 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         26.6 |
| en     | invoice        | generated |      5 |       41 |         1   |       0 |        0 |       4 |       0.25 |       0.857 |            1 |         31.9 |
| en     | invoice        | real      |      1 |       11 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         32.9 |
| en     | receipt        | generated |      2 |       14 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         14.2 |
| en     | receipt        | real      |      4 |       10 |         0.9 |       1 |        0 |       2 |       1    |       1     |            1 |         21.3 |
| es     | invoice        | generated |      1 |       11 |         1   |       0 |        0 |       1 |       0    |       0.727 |            1 |         37.1 |
| fr     | invoice        | generated |      1 |       10 |         1   |       0 |        0 |       2 |       0    |       0.7   |            1 |         35.9 |
| fr     | invoice        | real      |      1 |       11 |         1   |       0 |        0 |       0 |     nan    |       0.727 |            1 |         34.7 |
| fr     | receipt        | generated |      2 |       16 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         16.1 |
| id     | receipt        | real      |      2 |        5 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         19.3 |
| it     | invoice        | generated |      1 |       12 |         1   |       0 |        0 |       0 |     nan    |       0.75  |            1 |         41   |
| it     | receipt        | generated |      2 |       14 |         1   |       0 |        0 |       2 |       1    |       1     |            1 |         14   |
| ko     | receipt        | real      |      1 |        2 |         1   |       0 |        0 |       0 |     nan    |       1     |            1 |         20.6 |
| nl     | invoice        | generated |      1 |       11 |         1   |       0 |        0 |       1 |       0    |       0.727 |            1 |         39.1 |
| pl     | invoice        | generated |      1 |       12 |         1   |       0 |        0 |       0 |     nan    |       0.75  |            1 |         40.6 |
| pt     | invoice        | generated |      1 |       12 |         1   |       0 |        0 |       0 |     nan    |       0.75  |            1 |         39.3 |
| pt     | invoice        | real      |      1 |        5 |         1   |       0 |        0 |       0 |     nan    |       0.8   |            1 |         29.8 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.6 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         37.5 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         37.9 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         37.9 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         37.5 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         36.5 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         36.5 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         34.7 |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         38   |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       0.929 |            1 |         37.1 |
| invoice        | seller_vat_id   |     13 |       13 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         37.9 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          1 |       0.375 |            1 |         36.5 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.333 |            1 |         37.1 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.333 |            1 |         37.1 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         14.4 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         14.6 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         14.6 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         15.2 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         14.4 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       1     |            1 |         14.6 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         14.7 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         14.6 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       1     |            1 |         14.6 |
