# s2__qwen3vl-8b__P2b

```
{
 "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit",
 "revision": "defcdea7cc7a4b0858fea563cbbce171d328e457",
 "prompt": "P2b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": false,
 "run_id": "s2__qwen3vl-8b__P2b",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 1.99,
 "load_peak_gb": 5.761,
 "finished_at": "2026-11-16 06:18:32"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.2 |
| invoice        |     16 |      157 |       0.968 |       3 |        2 |       9 |      0.111 |       0.936 |            1 |         45   |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       1     |            1 |         20.7 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |    nan     |       1     |            1 |         33.2 |
| invoice        |     16 |      157 |       0.968 |       3 |        2 |       9 |      0.111 |       0.936 |            1 |         45   |
| receipt        |     15 |       77 |       0.987 |       1 |        0 |      10 |      1     |       1     |            1 |         20.7 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       1     |            1 |         46.5 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |     nan    |       1     |            1 |         76.2 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |         18.6 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         33.2 |
| en     | invoice        | generated |      5 |       41 |       0.951 |       1 |        1 |       4 |       0.25 |       1     |            1 |         40.9 |
| en     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         41.9 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |         18.6 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |       1    |       1     |            1 |         27.3 |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       0.727 |            1 |         46   |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |       0    |       1     |            1 |         43.8 |
| fr     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |     nan    |       0.727 |            1 |         44   |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |         20.8 |
| id     | receipt        | real      |      2 |        5 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         24.7 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         51.1 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |       1    |       1     |            1 |         18.3 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         26.5 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |       0    |       0.727 |            1 |         48.9 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         51.4 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |     nan    |       1     |            1 |         48.3 |
| pt     | invoice        | real      |      1 |        5 |       0.8   |       0 |        1 |       0 |     nan    |       0.75  |            1 |         35.4 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.2 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.2 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.2 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.2 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.2 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.2 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.9 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         33.9 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         46.2 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         47.1 |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         47.1 |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         46.2 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         45   |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         45   |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         44   |
| invoice        | seller_iban     |     11 |       10 |       0.9   |       1 |        0 |       1 |          0 |       1     |            1 |         47.8 |
| invoice        | seller_name     |     15 |       14 |       0.929 |       0 |        1 |       1 |          0 |       0.923 |            1 |         46   |
| invoice        | seller_vat_id   |     13 |       13 |       0.846 |       1 |        1 |       0 |        nan |       1     |            1 |         46.5 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          1 |       0.812 |            1 |         45   |
| invoice        | total_net       |     15 |       15 |       0.933 |       1 |        0 |       0 |        nan |       0.8   |            1 |         46   |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.8   |            1 |         46   |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.7 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.9 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.8 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         19.8 |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.7 |
| receipt        | subtotal        |     12 |        2 |       1     |       0 |        0 |      10 |          1 |       1     |            1 |         18.9 |
| receipt        | tax_amount      |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.9 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         18.8 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       1     |            1 |         18.9 |
