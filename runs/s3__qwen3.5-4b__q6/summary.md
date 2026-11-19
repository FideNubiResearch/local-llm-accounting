# s3__qwen3.5-4b__q6

```
{
 "model": "mlx-community/Qwen3.5-4B-6bit",
 "revision": "fbb1092aa9daef007603ea9273cd24c225a409f1",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s3__qwen3.5-4b__q6",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 0.84,
 "load_peak_gb": 4.086,
 "finished_at": "2026-11-18 07:48:23"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         13.7 |
| invoice        |     16 |      157 |       0.981 |       3 |        0 |       9 |          0 |       0.879 |            1 |         18.8 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |          1 |       0.862 |            1 |          7.6 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         13.7 |
| invoice        |     16 |      157 |       0.981 |       3 |        0 |       9 |          0 |       0.879 |            1 |         18.8 |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |          1 |       0.862 |            1 |          7.6 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         19.4 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |        nan |       1     |            1 |         32.3 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |          6.9 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         13.7 |
| en     | invoice        | generated |      5 |       41 |       0.976 |       1 |        0 |       4 |          0 |       0.927 |            1 |         16.6 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         16.9 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |          7   |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |          1 |       1     |            1 |         11   |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         19.1 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         18.5 |
| fr     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         17.3 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       0.667 |            1 |          7.8 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.9 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         20.8 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       0.625 |            1 |          7   |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         10.5 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         20   |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         20.7 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         20.2 |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       1 |        0 |       0 |        nan |       0.8   |            1 |         16.1 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.7 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.7 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.7 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0     |            1 |         13.7 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.7 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       0     |            1 |         13.7 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.7 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         13.7 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         19.2 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         19.5 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         19.5 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         19.2 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         18.8 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.8 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         17.3 |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         19.6 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       0.929 |            1 |         19.1 |
| invoice        | seller_vat_id   |     13 |       13 |       0.923 |       1 |        0 |       0 |        nan |       1     |            1 |         19.4 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       0.6   |            1 |         18.8 |
| invoice        | total_net       |     15 |       15 |       0.933 |       1 |        0 |       0 |        nan |       0.6   |            1 |         19.1 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.6   |            1 |         19.1 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          7   |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          7.2 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          7.1 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          7.3 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          7   |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       0.667 |            1 |          7.2 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       0.636 |            1 |          7.4 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          7.1 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.667 |            1 |          7.2 |
