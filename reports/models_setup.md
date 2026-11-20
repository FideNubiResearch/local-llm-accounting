**Preparing five models for the first round — 11 November 2026.**

All five repositories were downloaded with `harness.runner.download(repo, revision)` into `models_cache/`; the SHA256 of all **8** safetensors files match `siblings[].lfs.sha256` of the HF API for the pinned revisions. Total on disk **26 828 210 176 bytes = 26.828 GB / 24.986 GiB**. Check finished `2026-11-11T12:58:58.046909+00:00`. No inference and no loading of weights into memory/GPU; `Runner()` and `mlx_vlm.load()` were not called.

Main result of the pipeline check: **Qwen receives `max_pixels`; Gemma with the current Runner stays at 280 visual tokens.** For the required Gemma budget of 1120, `processor.image_processor.max_soft_tokens = 1120` must be set when the processor is created. Passing `max_soft_tokens=1120` or `images_kwargs={\"max_soft_tokens\":1120}` only to `stream_generate()` does not work in 0.7.10: the parameter is dropped in `process_inputs()`. Line references and a CPU check below. Files in `harness/`, `protocol/`, `final/` were not edited; the downloaded configs/templates were kept as they are.

Source of the revisions — [models_catalog.md](./models_catalog.md). Version `mlx-vlm==0.7.10`: [uv.lock:825](../uv.lock:825) and the installed metadata; the checked package files match byte for byte the Git blob IDs of [tag v0.7.10 / commit 8c061ef516e7f8b584c0d5b64f26b50d5806303b](https://github.com/Neywa-Labs/mlx-vlm/tree/8c061ef516e7f8b584c0d5b64f26b50d5806303b). The download path is implemented in [harness/runner.py:29](../harness/runner.py:29); importing the runner module does not load MLX, that happens inside the Runner constructor on line 45.

| Model | Local folder | On disk (`du -sk × 1024`) | safetensors, bytes | SHA256 / revision | Image budget | Thinking off |
|---|---|---|---|---|---|---|
| Qwen3-VL-8B-Instruct-4bit | [models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit](../models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit) | 5 783 367 680 B (5.783 GB) | 5 760 665 246 | OK, 2 file(s); metadata SHA OK | `min_pixels=65536`, `max_pixels=16777216`: the checkpoint's defaults; a separate OCR preset was **not found**. | Confirmed from the template; Instruct does not use a thinking switch. |
| Qwen3.5-4B-4bit | [models_cache/mlx-community__Qwen3.5-4B-4bit](../models_cache/mlx-community__Qwen3.5-4B-4bit) | 3 069 878 272 B (3.070 GB) | 3 034 300 695 | OK, 1 file(s); metadata SHA OK | `min_pixels=65536`, `max_pixels=16777216`: the checkpoint's defaults; a separate OCR preset was **not found**. | Confirmed: the flag reaches the template. |
| Qwen3.5-9B-4bit | [models_cache/mlx-community__Qwen3.5-9B-4bit](../models_cache/mlx-community__Qwen3.5-9B-4bit) | 5 995 442 176 B (5.995 GB) | 5 950 221 072 | OK, 2 file(s); metadata SHA OK | `min_pixels=65536`, `max_pixels=16777216`: the checkpoint's defaults; a separate OCR preset was **not found**. | Confirmed: the flag reaches the template. |
| gemma-4-e4b-it-4bit | [models_cache/mlx-community__gemma-4-e4b-it-4bit](../models_cache/mlx-community__gemma-4-e4b-it-4bit) | 5 189 746 688 B (5.190 GB) | 5 146 800 534 | OK, 1 file(s); metadata SHA OK | `processor.image_processor.max_soft_tokens = 1120`; currently config/Runner: 280. | Confirmed: the flag reaches the template. |
| gemma-4-12B-it-4bit | [models_cache/mlx-community__gemma-4-12B-it-4bit](../models_cache/mlx-community__gemma-4-12B-it-4bit) | 6 789 775 360 B (6.790 GB) | 6 741 039 511 | OK, 2 file(s); metadata SHA OK | `processor.image_processor.max_soft_tokens = 1120`; currently config/Runner: 280. | Confirmed: the flag reaches the template. |

**How download, SHA256 and size were checked**

Only `download()` was called for the five repo/revision pairs from the catalogue table. For each repository we checked that all files from the HF API `siblings` are present, the safetensors sizes, and the first line of every HF `.metadata` (equal to the required commit SHA). SHA256 was computed in streaming mode with `hashlib.file_digest(file, \"sha256\")`; no file was read whole into RAM. In addition `config.json`, processor configs, `tokenizer_config.json` and `chat_template.jinja` match the Git `blobId` of the API revision. `du -sk` counts the downloaded files and the `.cache/huggingface` service folder, not only the weights; logical payload bytes are given per model below.

Final output of the checks:

```text
All five downloads complete; mlx/mlx_vlm not imported.
All SHA256 hashes, API files, revision metadata and disk sizes verified; no MLX imports.
```

**How the image budget travels through mlx-vlm 0.7.10**

Our [harness/runner.py:89](../harness/runner.py:89) adds only `max_pixels`, if set and non-zero; the Runner interface does not pass `min_pixels` or `max_soft_tokens`. Then [mlx_vlm/generate/dispatch.py:863](../.venv/lib/python3.12/site-packages/mlx_vlm/generate/dispatch.py:863) calls `_prepare_generation_inputs()`, which passes `**kwargs` to `prepare_inputs()` ([mlx_vlm/generate/dispatch.py:685](../.venv/lib/python3.12/site-packages/mlx_vlm/generate/dispatch.py:685)), then to `process_inputs_with_fallback()` ([mlx_vlm/utils.py:2060](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:2060)) and `process_inputs()` ([mlx_vlm/utils.py:1812](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1812)).

[mlx_vlm/utils.py:1776](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1776) passes the explicitly named parameters of the processor signature. For `**kwargs` only `min_pixels`, `max_pixels`, `resized_height`, `resized_width` are allowed ([mlx_vlm/utils.py:1780](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1780)); then the processor is called ([mlx_vlm/utils.py:1798](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1798)). So **`max_pixels` reaches Qwen**, and `min_pixels` would too with a direct `stream_generate(..., min_pixels=...)`; `max_soft_tokens` and `images_kwargs` do not cross this boundary. Passing `max_pixels` to Gemma also reaches the processor as a kwarg, but **does not set the Gemma budget**: Gemma reads other parameters.

Qwen3-VL uses `Qwen3VLProcessor`; Qwen3.5 registers the same class in [mlx_vlm/models/qwen3_5/__init__.py:6](../.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_5/__init__.py:6). It extracts the pixel parameters ([mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:23](../.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:23)), passes them to the image processor ([mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:823](../.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:823)), which applies `min_pixels/max_pixels` in `_resolved_size()` ([mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:343](../.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:343)). The checkpoint's `size.shortest_edge/longest_edge` fields are converted to min/max pixels at [mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:680](../.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:680): here 65 536 / 16 777 216. This is a pixel area, not a side length. **No min/max value recommended specifically for OCR was found in the checked sources and checkpoint configs**; these numbers are defaults, not a promise of safe RAM use on the largest image.

Gemma4Processor can take `max_soft_tokens` directly in `processor(..., max_soft_tokens=1120)` or `processor(..., images_kwargs={\"max_soft_tokens\":1120})` ([mlx_vlm/models/gemma4/processing_gemma4.py:594](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:594)). But the usual `stream_generate()` drops them earlier. The reliable way at load time is **setting the attribute of the already created image processor**:

```python
# Snippet for a future authorised run; not executed here.
model, processor = load(path)
processor.image_processor.max_soft_tokens = 1120
# Then the usual stream_generate(model, processor, prompt, image=[...], ...).
```

Gemma E4B reads this attribute in [mlx_vlm/models/gemma4/processing_gemma4.py:227](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:227); Gemma 12B Unified in [mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:90](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:90), inheriting the common processor ([mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:327](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:327)). `load(path, max_soft_tokens=1120)` does not set this budget in the checked implementation: the local `from_pretrained()` build the image processor from `ip_config` without applying such a kwarg ([mlx_vlm/models/gemma4/processing_gemma4.py:929](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:929), [mlx_vlm/models/gemma4/processing_gemma4.py:1029](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:1029), [mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:360](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:360), [mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:428](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:428)). In addition `load()` may replace the image processor with one created by the architecture ([mlx_vlm/utils.py:838](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:838), [mlx_vlm/utils.py:975](../.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:975)), so the attribute must be set **after** `load()` returns.

1120 is a budget/upper bound, not a requirement to get exactly 1120 useful visual tokens from any A4 page. Sizes are rounded to a 48 px grid: [mlx_vlm/models/gemma4/processing_gemma4.py:119](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:119), the token count is computed from the actual patches ([mlx_vlm/models/gemma4/processing_gemma4.py:270](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:270)); Unified also pads the tensor to the budget ([mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:147](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:147)). Example, CPU arithmetic only: input 1241×1754 at budget 1120 → 1344×1872 → 1092 useful tokens. [Gemma's official recommendation for OCR](https://huggingface.co/google/gemma-4-12B-it/blob/43c9d014b231474fa7212dbb48a762566c2b255d/README.md#5-variable-image-resolution) is larger budgets; 1120 was chosen here per the task.

A CPU check of **the exact function** `process_inputs` with a recorder instead of the processor body and the signatures of the real `__call__` gave:

```text
Qwen: max_pixels/min_pixels forwarded; max_soft_tokens/images_kwargs dropped.
Gemma: max_pixels/min_pixels forwarded; max_soft_tokens/images_kwargs dropped.
No model, image tensor, MLX, torch or transformers package was loaded for this check.
```

**Thinking, and how the prompts were obtained without weights**

Our call is [harness/runner.py:63](../harness/runner.py:63). `apply_chat_template()` builds messages with one image ([mlx_vlm/prompt_utils.py:1028](../.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:1028)) and passes `enable_thinking=False` to `get_chat_template()` ([mlx_vlm/prompt_utils.py:1137](../.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:1137)); there the flag is kept and passed to `template_processor.apply_chat_template(..., **template_kwargs)` ([mlx_vlm/prompt_utils.py:934](../.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:934), [mlx_vlm/prompt_utils.py:952](../.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:952)). Qwen uses ProcessorMixin, which passes kwargs to Jinja together with the special tokens ([.venv/lib/python3.12/site-packages/transformers/processing_utils.py:2198](../.venv/lib/python3.12/site-packages/transformers/processing_utils.py:2198)). Gemma keeps the flag in its wrapper ([mlx_vlm/models/gemma4/processing_gemma4.py:835](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:835)) and passes it through the tokenizer to the same helper ([mlx_vlm/models/gemma4/processing_gemma4.py:871](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:871)); with `tokenize=False` it returns the text before tensors are prepared (line 887). This confirms control of the **template**, with no empirical guarantee about the generated answer.

One concrete input was chosen for the examples: **P0, invoice, scalar schema**. The text comes from the existing `schema_for(\"invoice\", \"P0\")` and `prompt_text(\"invoice\", \"P0\", schema)` in [harness/run.py:41](../harness/run.py:41) / [harness/run.py:51](../harness/run.py:51); template — [protocol/prompts/P0_neutral.txt:1](../protocol/prompts/P0_neutral.txt:1). The real `prompt_utils.py` code was used as a separate file (its top-level imports are standard library only), with the downloaded `chat_template.jinja` and the special tokens from `tokenizer_config.json`. The Jinja text was rendered **from the template**, without `AutoProcessor` and without loading a tokenizer/model: only the Jinja compile function from the installed HF file was executed ([.venv/lib/python3.12/site-packages/transformers/utils/chat_template_utils.py:534](../.venv/lib/python3.12/site-packages/transformers/utils/chat_template_utils.py:534)). For Gemma only three text methods of the wrapper were also executed, with helper dependencies instead of package imports; tensor preparation was blocked by a sentinel. For Qwen an equivalent text renderer reproduces the merging of special tokens/kwargs from ProcessorMixin; the full ProcessorMixin was not executed.

For every model the recorder confirmed `enable_thinking=False` at the Jinja input, one image in messages and `tokenize=False`. The `sys.modules` check ended with an empty list for `mlx`, `mlx_vlm`, `torch`, `transformers`. Below is the full output of **apply_chat_template**, before the image placeholder is expanded to the grid of visual tokens in the image processor. The value 1120 must not appear in this text: the expansion happens later ([mlx_vlm/models/gemma4/processing_gemma4.py:605](../.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:605)). The SHA256 is of the exact UTF-8 string; the `repr` of its ending is given to check the final newline.

**mlx-community/Qwen3-VL-8B-Instruct-4bit**

Path: `models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit`. Revision: `defcdea7cc7a4b0858fea563cbbce171d328e457`; [HF API of this revision](https://huggingface.co/api/models/mlx-community/Qwen3-VL-8B-Instruct-4bit/revision/defcdea7cc7a4b0858fea563cbbce171d328e457?blobs=true).

On disk: `5647820 KiB` (`du -sk`), i.e. **5 783 367 680 B**; logical payload of all 17 repository files — 5 776 633 051 B, safetensors — 5 760 665 246 B. All 17 HF metadata files have the right revision. SHA256: **OK**; in each line below HF API SHA256 = local SHA256.

```text
7c637158b2203e321d83596d3661f33b7b98a72beddfaaaa0eddc512acbdd1fb  model-00001-of-00002.safetensors  OK
77190cd1dcf244522869bf923558340112b26d7db2ef3692f88407dd9b33c25d  model-00002-of-00002.safetensors  OK
```

Budget: `max_pixels=16777216`, `min_pixels=65536` from [preprocessor_config.json:1](../models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit/preprocessor_config.json:1); these are defaults, a separate «OCR recommended» value — **not found**. Our `Runner(max_pixels=N)` passes N to the image processor; `min_pixels` stays 65536 because the Runner has no such argument.

Thinking off: **confirmed for the chosen Instruct**. The flag reached Jinja, but [chat_template.jinja:118](../models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit/chat_template.jinja:118) has no `enable_thinking` switch at all and opens no `<think>`: Instruct and Thinking are different checkpoints here. The prefix ends with assistant + LF.

Final prompt for one image and P0/invoice:

```text
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.
<|im_end|>
<|im_start|>assistant
```

Exact string: 1230 characters; UTF-8 SHA256 `de8185be879c913c02576a39bbb57456d9dee73292c1af0e9e16c9bd6301be25`. Ending (`repr`): `'ption": "total including tax"}}}\nReturn only the JSON object.\n<|im_end|>\n<|im_start|>assistant\n'`.

**mlx-community/Qwen3.5-4B-4bit**

Path: `models_cache/mlx-community__Qwen3.5-4B-4bit`. Revision: `0e7ffd5c629ef7719d4cbc04069232580bfa9d9c`; [HF API of this revision](https://huggingface.co/api/models/mlx-community/Qwen3.5-4B-4bit/revision/0e7ffd5c629ef7719d4cbc04069232580bfa9d9c?blobs=true).

On disk: `2997928 KiB` (`du -sk`), i.e. **3 069 878 272 B**; logical payload of all 11 repository files — 3 061 130 647 B, safetensors — 3 034 300 695 B. All 11 HF metadata files have the right revision. SHA256: **OK**; in each line below HF API SHA256 = local SHA256.

```text
5fb9acd0246866381cf8c5c354c6db1019f6498eec4ccb4f5edcc71ffeacb2db  model.safetensors  OK
```

Budget: `max_pixels=16777216`, `min_pixels=65536` from [processor_config.json:1](../models_cache/mlx-community__Qwen3.5-4B-4bit/processor_config.json:1); these are defaults, a separate «OCR recommended» value — **not found**. Our `Runner(max_pixels=N)` passes N to the image processor; `min_pixels` stays 65536 because the Runner has no such argument.

Thinking off: **confirmed from [chat_template.jinja:147](../models_cache/mlx-community__Qwen3.5-4B-4bit/chat_template.jinja:147)**: `False` adds an already closed empty block `<think>\n\n</think>\n\n`; `True` leaves an open `<think>`. The off block is part of the input prompt, not the model's answer.

Final prompt for one image and P0/invoice:

```text
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<|im_end|>
<|im_start|>assistant
<think>

</think>

```

Exact string: 1248 characters; UTF-8 SHA256 `266d2b64dbff2a7211d132303a68cbd58c645f7dd4584595b72856d611741731`. Ending (`repr`): `'luding tax"}}}\nReturn only the JSON object.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'`.

**mlx-community/Qwen3.5-9B-4bit**

Path: `models_cache/mlx-community__Qwen3.5-9B-4bit`. Revision: `8b2b98c00a6b4d291155e4890773ca8f769aee53`; [HF API of this revision](https://huggingface.co/api/models/mlx-community/Qwen3.5-9B-4bit/revision/8b2b98c00a6b4d291155e4890773ca8f769aee53?blobs=true).

On disk: `5854924 KiB` (`du -sk`), i.e. **5 995 442 176 B**; logical payload of all 13 repository files — 5 977 073 303 B, safetensors — 5 950 221 072 B. All 13 HF metadata files have the right revision. SHA256: **OK**; in each line below HF API SHA256 = local SHA256.

```text
a68b87558c6ef43f74c2bd63ce7e9092ceddc3101f3def0030774bae5f42aadd  model-00001-of-00002.safetensors  OK
b0a770bf8469c7f3f18756a0e0283f1c1174344a83e059a4e483f6af4907352d  model-00002-of-00002.safetensors  OK
```

Budget: `max_pixels=16777216`, `min_pixels=65536` from [processor_config.json:1](../models_cache/mlx-community__Qwen3.5-9B-4bit/processor_config.json:1); these are defaults, a separate «OCR recommended» value — **not found**. Our `Runner(max_pixels=N)` passes N to the image processor; `min_pixels` stays 65536 because the Runner has no such argument.

Thinking off: **confirmed from [chat_template.jinja:147](../models_cache/mlx-community__Qwen3.5-9B-4bit/chat_template.jinja:147)**: `False` adds an already closed empty block `<think>\n\n</think>\n\n`; `True` leaves an open `<think>`. The off block is part of the input prompt, not the model's answer.

Final prompt for one image and P0/invoice:

```text
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<|im_end|>
<|im_start|>assistant
<think>

</think>

```

Exact string: 1248 characters; UTF-8 SHA256 `266d2b64dbff2a7211d132303a68cbd58c645f7dd4584595b72856d611741731`. Ending (`repr`): `'luding tax"}}}\nReturn only the JSON object.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'`.

**mlx-community/gemma-4-e4b-it-4bit**

Path: `models_cache/mlx-community__gemma-4-e4b-it-4bit`. Revision: `475b9088d29754a3379866cf5aeb6b41acd313c2`; [HF API of this revision](https://huggingface.co/api/models/mlx-community/gemma-4-e4b-it-4bit/revision/475b9088d29754a3379866cf5aeb6b41acd313c2?blobs=true).

On disk: `5068112 KiB` (`du -sk`), i.e. **5 189 746 688 B**; logical payload of all 10 repository files — 5 179 241 512 B, safetensors — 5 146 800 534 B. All 10 HF metadata files have the right revision. SHA256: **OK**; in each line below HF API SHA256 = local SHA256.

```text
932b8271fc3fe65adcc78b96c10c6268bbfb13e8f67d1358727c0d6ee97e1eff  model.safetensors  OK
```

OCR budget per the task: **`processor.image_processor.max_soft_tokens = 1120` after load**. The original [processor_config.json:1](../models_cache/mlx-community__gemma-4-e4b-it-4bit/processor_config.json:1) has 280; the current Runner would also keep 280. This is an in-memory processor property for a future run, not a change of the downloaded config.

Thinking off: **confirmed from [chat_template.jinja:179](../models_cache/mlx-community__gemma-4-e4b-it-4bit/chat_template.jinja:179) / [chat_template.jinja:356](../models_cache/mlx-community__gemma-4-e4b-it-4bit/chat_template.jinja:356)**: `False` adds no `<|think|>` to system, and the generation prefix stays `<|turn>model\n` without a thought block.

Final prompt for one image and P0/invoice:

```text
<bos><|turn>user
<|image|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<turn|>
<|turn>model
```

Exact string: 1183 characters; UTF-8 SHA256 `77582de45a44ec2f44700dbefce1661bf502f27d70225c78f9a03dd65b625a21`. Ending (`repr`): `'ll"], "description": "total including tax"}}}\nReturn only the JSON object.<turn|>\n<|turn>model\n'`.

**mlx-community/gemma-4-12B-it-4bit**

Path: `models_cache/mlx-community__gemma-4-12B-it-4bit`. Revision: `73bcf09092aa277861d5a191b989b666f7f32e8f`; [HF API of this revision](https://huggingface.co/api/models/mlx-community/gemma-4-12B-it-4bit/revision/73bcf09092aa277861d5a191b989b666f7f32e8f?blobs=true).

On disk: `6630640 KiB` (`du -sk`), i.e. **6 789 775 360 B**; logical payload of all 11 repository files — 6 773 372 848 B, safetensors — 6 741 039 511 B. All 11 HF metadata files have the right revision. SHA256: **OK**; in each line below HF API SHA256 = local SHA256.

```text
0d58feed0c98a69c07317b4481aeae5ab2785f12a496ea96ab24c4842808de78  model-00001-of-00002.safetensors  OK
5b00a1bcb596ce6e827b4cdea6ecf2a0f35bb01306eb87c1ea4b3bcde36c7755  model-00002-of-00002.safetensors  OK
```

OCR budget per the task: **`processor.image_processor.max_soft_tokens = 1120` after load**. The original [processor_config.json:1](../models_cache/mlx-community__gemma-4-12B-it-4bit/processor_config.json:1) has 280; the current Runner would also keep 280. This is an in-memory processor property for a future run, not a change of the downloaded config.

Thinking off: **confirmed from [chat_template.jinja:179](../models_cache/mlx-community__gemma-4-12B-it-4bit/chat_template.jinja:179) / [chat_template.jinja:356](../models_cache/mlx-community__gemma-4-12B-it-4bit/chat_template.jinja:356)**: `False` does not enable `<|think|>`, and the generation prefix ends with a closed empty thought channel `<|channel>thought\n<channel|>`.

Final prompt for one image and P0/invoice:

```text
<bos><|turn>user
<|image|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<turn|>
<|turn>model
<|channel>thought
<channel|>
```

Exact string: 1211 characters; UTF-8 SHA256 `9ba40b787eacdd1d18f5278f355ac1c91083ce8638369b70f19eec5a6d57f6b2`. Ending (`repr`): `'including tax"}}}\nReturn only the JSON object.<turn|>\n<|turn>model\n<|channel>thought\n<channel|>'`.

**What is needed before the first round**

Weights are ready for all five models. For Gemma the pipeline needs a post-load attribute `max_soft_tokens=1120`; this budget cannot be set by passing the current `max_pixels`. For Qwen the working path `Runner(max_pixels=N)` is confirmed, but no single OCR-specific value of N was found in the sources examined; it has to be fixed by the protocol separately. In all five cases disabling thinking was analysed from the pinned template; it has not been checked by inference yet.
