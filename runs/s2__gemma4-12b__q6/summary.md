# s2__gemma4-12b__q6

```
{
 "model": "mlx-community/gemma-4-12B-it-6bit",
 "revision": "2fe53aeb9b8686eefa543a60d6aa364c5b219aac",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": 1120,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__gemma4-12b__q6",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "max_soft_tokens": 1120
 },
 "load_s": 5.29,
 "load_peak_gb": 9.731,
 "finished_at": "2026-11-15 20:17:33"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |      nan   |       0.714 |            1 |         28.2 |
| invoice        |     16 |      157 |       0.962 |       3 |        3 |       9 |        0   |       0.857 |            1 |         37.7 |
| receipt        |     15 |       77 |       1     |       0 |        0 |      10 |        0.2 |       1     |            1 |         26.1 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |      nan   |       0.714 |            1 |         28.2 |
| invoice        |     16 |      157 |       0.962 |       3 |        3 |       9 |        0   |       0.857 |            1 |         37.7 |
| receipt        |     15 |       77 |       1     |       0 |        0 |      10 |        0.2 |       1     |            1 |         26.1 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         37.9 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       0 |        1 |       0 |        nan |       1     |            1 |         61.4 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         26.2 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       0.714 |            1 |         28.2 |
| en     | invoice        | generated |      5 |       41 |       0.976 |       0 |        1 |       4 |          0 |       0.925 |            1 |         33.4 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         35.7 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         25.1 |
| en     | receipt        | real      |      4 |       10 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |         26.7 |
| es     | invoice        | generated |      1 |       11 |       0.909 |       1 |        0 |       1 |          0 |       0.727 |            1 |         37.4 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       0.7   |            1 |         36.1 |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |        nan |       1     |            1 |         38.1 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         26.4 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         24.2 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         42   |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         25.5 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         27.4 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         39.8 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         41.9 |
| pt     | invoice        | generated |      1 |       12 |       0.917 |       1 |        0 |       0 |        nan |       0.75  |            1 |         41   |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       0 |        1 |       0 |        nan |       0.75  |            1 |         31.8 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         28.2 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         28.2 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         28.2 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       0     |            1 |         28.2 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         28.2 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |      nan   |       0     |            1 |         28.2 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         27.9 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         27.9 |
| invoice        | buyer_name      |     14 |       14 |       0.929 |       1 |        0 |       0 |      nan   |       1     |            1 |         38   |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |        0   |       1     |            1 |         38.6 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         38.6 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |        0   |       1     |            1 |         37.7 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |        0   |       1     |            1 |         37.7 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         37.7 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         38.1 |
| invoice        | seller_iban     |     11 |       10 |       0.8   |       0 |        2 |       1 |        0   |       1     |            1 |         39.2 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |        0   |       0.929 |            1 |         37.9 |
| invoice        | seller_vat_id   |     13 |       13 |       0.769 |       2 |        1 |       0 |      nan   |       1     |            1 |         38.1 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |        0   |       0.533 |            1 |         37.7 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |      nan   |       0.533 |            1 |         37.9 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |      nan   |       0.533 |            1 |         37.9 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         25.9 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         26.2 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         26.1 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         26.3 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         25.9 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |        0.2 |       1     |            1 |         25.7 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         25.6 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         26.1 |
| receipt        | total           |     12 |       12 |       1     |       0 |        0 |       0 |      nan   |       1     |            1 |         26   |
