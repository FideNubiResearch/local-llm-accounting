# Energy per document (powermetrics)

Sample: protocol/samples/smoke.txt (33 documents), CPU+GPU+ANE, 1 s step. Idle: 0.09 W (60 s). Only the document-processing phase is counted (model loading excluded). Whole-system (wall) power was not measured.

| Configuration | Docs | Errors | s/doc | CPU, W | GPU, W | Total, W | Wh/doc | Wh/doc above idle | Peak, GB |
|---|---|---|---|---|---|---|---|---|---|
| e__gemma4-12b__q6 | 33 | 0 | 31.3 | 0.2 | 14.7 | 14.9 | 0.1308 | 0.13 | 12.584 |
| e__qwen3.5-4b__q6 | 33 | 0 | 13.8 | 0.3 | 14.5 | 14.9 | 0.0588 | 0.0584 | 6.154 |
| e__nuextract3-4b__q6 | 33 | 0 | 12.4 | 0.3 | 14.6 | 15.0 | 0.0533 | 0.053 | 6.057 |
| e__lift-9b__q6c | 33 | 0 | 24.3 | 0.2 | 14.5 | 14.8 | 0.1008 | 0.1002 | 10.299 |
