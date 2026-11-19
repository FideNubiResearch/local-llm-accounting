# s2__qwen3.5-9b__constr

```
{
 "model": "mlx-community/Qwen3.5-9B-4bit",
 "revision": "8b2b98c00a6b4d291155e4890773ca8f769aee53",
 "prompt": "P1b",
 "max_pixels": null,
 "max_soft_tokens": null,
 "max_tokens": 1024,
 "constrained": true,
 "run_id": "s2__qwen3.5-9b__constr",
 "n_selected": 33,
 "mlx_vlm": "0.7.10",
 "image_processor": {
  "min_pixels": 65536,
  "max_pixels": 16777216
 },
 "load_s": 3.36,
 "load_peak_gb": 5.951,
 "finished_at": "2026-11-15 17:53:01"
}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| invoice        |     16 |      157 |       0.987 |       2 |        0 |       9 |          0 |       0.822 |            1 |         28.2 |
| receipt        |     15 |       77 |       0.961 |       3 |        0 |      10 |          1 |       1     |            1 |         10.4 |

## All without quality=low documents

0 documents tagged quality=low (0 rows) are left out of this table only.

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| invoice        |     16 |      157 |       0.987 |       2 |        0 |       9 |          0 |       0.822 |            1 |         28.2 |
| receipt        |     15 |       77 |       0.961 |       3 |        0 |      10 |          1 |       1     |            1 |         10.4 |

## Language x type x real/generated

| lang   | doc_type       | kind      |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:-------|:---------------|:----------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| de     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         29.5 |
| de     | invoice        | real      |      1 |       10 |       0.9   |       1 |        0 |       0 |        nan |       1     |            1 |         51.6 |
| de     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |          9.3 |
| en     | bank_statement | generated |      2 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| en     | invoice        | generated |      5 |       41 |       1     |       0 |        0 |       4 |          0 |       0.927 |            1 |         24.8 |
| en     | invoice        | real      |      1 |       11 |       0.909 |       1 |        0 |       0 |        nan |       1     |            1 |         25.4 |
| en     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |          9.6 |
| en     | receipt        | real      |      4 |       10 |       0.9   |       1 |        0 |       2 |          1 |       1     |            1 |         16.6 |
| es     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         28.3 |
| fr     | invoice        | generated |      1 |       10 |       1     |       0 |        0 |       2 |          0 |       0.7   |            1 |         28.2 |
| fr     | invoice        | real      |      1 |       11 |       1     |       0 |        0 |       0 |        nan |       0.727 |            1 |         26.4 |
| fr     | receipt        | generated |      2 |       16 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |         10.8 |
| id     | receipt        | real      |      2 |        5 |       0.6   |       2 |        0 |       0 |        nan |       1     |            1 |         15.1 |
| it     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         30.6 |
| it     | receipt        | generated |      2 |       14 |       1     |       0 |        0 |       2 |          1 |       1     |            1 |          9.2 |
| ko     | receipt        | real      |      1 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         15.6 |
| nl     | invoice        | generated |      1 |       11 |       1     |       0 |        0 |       1 |          0 |       0.727 |            1 |         29.3 |
| pl     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         30.3 |
| pt     | invoice        | generated |      1 |       12 |       1     |       0 |        0 |       0 |        nan |       0.75  |            1 |         29.6 |
| pt     | invoice        | real      |      1 |        5 |       1     |       0 |        0 |       0 |        nan |       0.8   |            1 |         24.7 |

## Field

| doc_type       | field           |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |   format_ok |   json_valid |   sec_median |
|:---------------|:----------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|------------:|-------------:|-------------:|
| bank_statement | account_holder  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| bank_statement | account_number  |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| bank_statement | bank_name       |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| bank_statement | closing_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| bank_statement | currency        |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| bank_statement | opening_balance |      2 |        2 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.2 |
| bank_statement | period_end      |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.3 |
| bank_statement | period_start    |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         21.3 |
| invoice        | buyer_name      |     14 |       14 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.4 |
| invoice        | buyer_vat_id    |     10 |        8 |       1     |       0 |        0 |       2 |          0 |       1     |            1 |         29   |
| invoice        | currency        |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         29   |
| invoice        | due_date        |     12 |        9 |       1     |       0 |        0 |       3 |          0 |       1     |            1 |         28.4 |
| invoice        | invoice_number  |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       1     |            1 |         28.2 |
| invoice        | issue_date      |     16 |       16 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.2 |
| invoice        | purchase_order  |      1 |        1 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         26.4 |
| invoice        | seller_iban     |     11 |       10 |       0.8   |       2 |        0 |       1 |          0 |       1     |            1 |         29.3 |
| invoice        | seller_name     |     15 |       14 |       1     |       0 |        0 |       1 |          0 |       0.929 |            1 |         28.3 |
| invoice        | seller_vat_id   |     13 |       13 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         28.6 |
| invoice        | total_gross     |     16 |       15 |       1     |       0 |        0 |       1 |          0 |       0.4   |            1 |         28.2 |
| invoice        | total_net       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.4   |            1 |         28.3 |
| invoice        | total_tax       |     15 |       15 |       1     |       0 |        0 |       0 |        nan |       0.4   |            1 |         28.3 |
| receipt        | currency        |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.5 |
| receipt        | date            |     12 |       12 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.7 |
| receipt        | merchant_name   |     11 |       11 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.5 |
| receipt        | merchant_tax_id |      4 |        4 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |         10   |
| receipt        | payment_method  |      8 |        8 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.5 |
| receipt        | subtotal        |     12 |        2 |       0.5   |       1 |        0 |      10 |          1 |       1     |            1 |          9.7 |
| receipt        | tax_amount      |     11 |       11 |       0.909 |       1 |        0 |       0 |        nan |       1     |            1 |          9.9 |
| receipt        | time            |      9 |        9 |       1     |       0 |        0 |       0 |        nan |       1     |            1 |          9.5 |
| receipt        | total           |     12 |       12 |       0.917 |       1 |        0 |       0 |        nan |       1     |            1 |          9.7 |
