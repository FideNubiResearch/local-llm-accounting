**Подготовка пяти моделей к первому кругу — 11 ноября 2026.**

Все пять репозиториев скачаны через `harness.runner.download(repo, revision)` в `models_cache/`; SHA256 всех **8** safetensors-файлов совпали с `siblings[].lfs.sha256` HF API закреплённых revision. На диске суммарно **26 828 210 176 байт = 26.828 GB / 24.986 GiB**. Проверка завершена `2026-11-11T12:58:58.046909+00:00`. Инференс и загрузка весов в память/GPU не выполнялись; `Runner()` и `mlx_vlm.load()` не вызывались.

Главный результат проверки конвейера: **Qwen получает `max_pixels`; Gemma с текущим Runner остаётся на 280 visual tokens.** Для требуемого бюджета Gemma 1120 надо при будущем создании процессора установить `processor.image_processor.max_soft_tokens = 1120`. Передача `max_soft_tokens=1120` или `images_kwargs={"max_soft_tokens":1120}` только в `stream_generate()` в версии 0.7.10 не срабатывает: параметр отбрасывается в `process_inputs()`. Подтверждение по строкам и CPU-проверка ниже. Файлы `harness/`, `protocol/`, `final/` не редактировались; скачанные configs/templates сохранены исходными.

Источник revision — [models_catalog.md](./models_catalog.md). Версия `mlx-vlm==0.7.10`: [uv.lock:825](<project>/uv.lock:825) и установленная metadata; проверенные файлы пакета побайтово соответствуют Git blob IDs [тега v0.7.10 / commit 8c061ef516e7f8b584c0d5b64f26b50d5806303b](https://github.com/Neywa-Labs/mlx-vlm/tree/8c061ef516e7f8b584c0d5b64f26b50d5806303b). Путь скачивания реализован в [harness/runner.py:29](<project>/harness/runner.py:29); импорт модуля runner не загружает MLX, это происходит внутри конструктора Runner на строке 45.

| Модель | Локальная папка | Занято на диске (`du -sk × 1024`) | safetensors, байт | SHA256 / revision | Бюджет картинки | Thinking off |
|---|---|---|---|---|---|---|
| Qwen3-VL-8B-Instruct-4bit | [models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit](<project>/models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit) | 5 783 367 680 B (5.783 GB) | 5 760 665 246 | OK, 2 файл(а); metadata SHA OK | `min_pixels=65536`, `max_pixels=16777216`: штатные значения checkpoint; отдельный OCR preset **не найден**. | Подтверждено по template; Instruct не использует переключатель thinking. |
| Qwen3.5-4B-4bit | [models_cache/mlx-community__Qwen3.5-4B-4bit](<project>/models_cache/mlx-community__Qwen3.5-4B-4bit) | 3 069 878 272 B (3.070 GB) | 3 034 300 695 | OK, 1 файл(а); metadata SHA OK | `min_pixels=65536`, `max_pixels=16777216`: штатные значения checkpoint; отдельный OCR preset **не найден**. | Подтверждено: флаг доходит до template. |
| Qwen3.5-9B-4bit | [models_cache/mlx-community__Qwen3.5-9B-4bit](<project>/models_cache/mlx-community__Qwen3.5-9B-4bit) | 5 995 442 176 B (5.995 GB) | 5 950 221 072 | OK, 2 файл(а); metadata SHA OK | `min_pixels=65536`, `max_pixels=16777216`: штатные значения checkpoint; отдельный OCR preset **не найден**. | Подтверждено: флаг доходит до template. |
| gemma-4-e4b-it-4bit | [models_cache/mlx-community__gemma-4-e4b-it-4bit](<project>/models_cache/mlx-community__gemma-4-e4b-it-4bit) | 5 189 746 688 B (5.190 GB) | 5 146 800 534 | OK, 1 файл(а); metadata SHA OK | `processor.image_processor.max_soft_tokens = 1120`; сейчас конфиг/Runner: 280. | Подтверждено: флаг доходит до template. |
| gemma-4-12B-it-4bit | [models_cache/mlx-community__gemma-4-12B-it-4bit](<project>/models_cache/mlx-community__gemma-4-12B-it-4bit) | 6 789 775 360 B (6.790 GB) | 6 741 039 511 | OK, 2 файл(а); metadata SHA OK | `processor.image_processor.max_soft_tokens = 1120`; сейчас конфиг/Runner: 280. | Подтверждено: флаг доходит до template. |

**Как проверены скачивание, SHA256 и размер**

Вызвана только функция `download()` для пяти пар repo/revision из таблицы каталога. Для каждого репозитория проверены наличие всех файлов из `siblings` HF API, размеры safetensors и первая строка всех HF `.metadata` (равна требуемому commit SHA). SHA256 вычислялся потоково через `hashlib.file_digest(file, "sha256")`; файл не читался целиком в RAM. Дополнительно `config.json`, processor configs, `tokenizer_config.json` и `chat_template.jinja` совпали с Git `blobId` API revision. `du -sk` учитывает скачанные файлы и служебную `.cache/huggingface`, а не только веса; logical payload bytes приведены по каждой модели ниже.

Завершающий вывод проверок:

```text
All five downloads complete; mlx/mlx_vlm not imported.
All SHA256 hashes, API files, revision metadata and disk sizes verified; no MLX imports.
```

**Путь бюджета картинки через mlx-vlm 0.7.10**

Наш [harness/runner.py:89](<project>/harness/runner.py:89) добавляет только `max_pixels`, если значение задано и ненулевое; `min_pixels` и `max_soft_tokens` интерфейс Runner не передаёт. Дальше [mlx_vlm/generate/dispatch.py:863](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/generate/dispatch.py:863) вызывает `_prepare_generation_inputs()`, та передаёт `**kwargs` в `prepare_inputs()` ([mlx_vlm/generate/dispatch.py:685](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/generate/dispatch.py:685)), затем в `process_inputs_with_fallback()` ([mlx_vlm/utils.py:2060](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:2060)) и `process_inputs()` ([mlx_vlm/utils.py:1812](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1812)).

В [mlx_vlm/utils.py:1776](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1776) передаются явно именованные параметры сигнатуры processor. Для `**kwargs` разрешены только `min_pixels`, `max_pixels`, `resized_height`, `resized_width` ([mlx_vlm/utils.py:1780](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1780)); затем вызывается processor ([mlx_vlm/utils.py:1798](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:1798)). Поэтому **`max_pixels` для Qwen доходит**, `min_pixels` также дойдёт при прямом вызове `stream_generate(..., min_pixels=...)`; `max_soft_tokens` и `images_kwargs` через эту границу не проходят. Попытка передать Gemma `max_pixels` тоже доходит до processor как kwarg, но **не задаёт бюджет Gemma**: Gemma читает другие параметры.

Qwen3-VL использует `Qwen3VLProcessor`; Qwen3.5 регистрирует тот же класс в [mlx_vlm/models/qwen3_5/__init__.py:6](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_5/__init__.py:6). Он извлекает pixel-параметры ([mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:23](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:23)), передаёт их в image processor ([mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:823](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:823)), а тот применяет `min_pixels/max_pixels` в `_resolved_size()` ([mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:343](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:343)). Поля `size.shortest_edge/longest_edge` из checkpoint конвертируются в min/max pixels на [mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:680](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/qwen3_vl/processing_qwen3_vl.py:680): здесь это 65 536 / 16 777 216. Это количество пикселей площади, не длина стороны. **Рекомендуемое специально для OCR значение min/max в проверенных исходниках и checkpoint configs не найдено**; указанные числа — defaults, а не обещание безопасного расхода RAM на максимальной картинке.

Gemma4Processor умеет принимать `max_soft_tokens` непосредственно в `processor(..., max_soft_tokens=1120)` или `processor(..., images_kwargs={"max_soft_tokens":1120})` ([mlx_vlm/models/gemma4/processing_gemma4.py:594](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:594)). Но обычный `stream_generate()` их отбрасывает раньше. Надёжный путь при будущей загрузке — **настройка атрибута уже созданного image processor**:

```python
# Фрагмент для будущего разрешённого запуска; сейчас не исполнялся.
model, processor = load(path)
processor.image_processor.max_soft_tokens = 1120
# Затем обычный stream_generate(model, processor, prompt, image=[...], ...).
```

Gemma E4B читает этот атрибут в [mlx_vlm/models/gemma4/processing_gemma4.py:227](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:227); Gemma 12B Unified — в [mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:90](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:90), наследуя общий processor ([mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:327](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:327)). `load(path, max_soft_tokens=1120)` не является рабочей настройкой этого бюджета в проверенной реализации: локальные `from_pretrained()` строят image processor из `ip_config`, не применяя такой kwarg ([mlx_vlm/models/gemma4/processing_gemma4.py:929](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:929), [mlx_vlm/models/gemma4/processing_gemma4.py:1029](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:1029), [mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:360](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:360), [mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:428](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:428)). Дополнительно `load()` может заменить image processor на созданный архитектурой ([mlx_vlm/utils.py:838](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:838), [mlx_vlm/utils.py:975](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/utils.py:975)), поэтому устанавливать атрибут следует **после** возврата `load()`.

1120 — бюджет/верхняя граница, а не требование получить ровно 1120 полезных visual tokens из любой A4. Размеры округляются по сетке 48 px: [mlx_vlm/models/gemma4/processing_gemma4.py:119](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:119), число токенов вычисляется по фактическим patches ([mlx_vlm/models/gemma4/processing_gemma4.py:270](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:270)); Unified дополнительно дополняет tensor до бюджета ([mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:147](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4_unified/processing_gemma4_unified.py:147)). Пример вычисления только арифметикой CPU: вход 1241×1754 при бюджете 1120 → 1344×1872 → 1092 полезных токена. [Официальная рекомендация Gemma для OCR](https://huggingface.co/google/gemma-4-12B-it/blob/43c9d014b231474fa7212dbb48a762566c2b255d/README.md#5-variable-image-resolution) — повышенные бюджеты; здесь 1120 выбран согласно задаче.

CPU-проверка **точной функции** `process_inputs` с recorder вместо тела processor и сигнатурами настоящих `__call__` дала:

```text
Qwen: max_pixels/min_pixels forwarded; max_soft_tokens/images_kwargs dropped.
Gemma: max_pixels/min_pixels forwarded; max_soft_tokens/images_kwargs dropped.
No model, image tensor, MLX, torch or transformers package was loaded for this check.
```

**Thinking и способ получения промптов без весов**

Наш вызов — [harness/runner.py:63](<project>/harness/runner.py:63). `apply_chat_template()` строит messages с одной картинкой ([mlx_vlm/prompt_utils.py:1028](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:1028)) и передаёт `enable_thinking=False` в `get_chat_template()` ([mlx_vlm/prompt_utils.py:1137](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:1137)); там флаг сохраняется и передаётся `template_processor.apply_chat_template(..., **template_kwargs)` ([mlx_vlm/prompt_utils.py:934](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:934), [mlx_vlm/prompt_utils.py:952](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/prompt_utils.py:952)). У Qwen используется ProcessorMixin, который передаёт kwargs в Jinja вместе со special tokens ([.venv/lib/python3.12/site-packages/transformers/processing_utils.py:2198](<project>/.venv/lib/python3.12/site-packages/transformers/processing_utils.py:2198)). Gemma в своём wrapper сохраняет флаг ([mlx_vlm/models/gemma4/processing_gemma4.py:835](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:835)) и передаёт его через tokenizer в тот же helper ([mlx_vlm/models/gemma4/processing_gemma4.py:871](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:871)); при `tokenize=False` возвращает текст до подготовки тензоров (строка 887). Это подтверждение управления **шаблоном**, без эмпирической гарантии поведения сгенерированного ответа.

Для примеров выбран один конкретный вход: **P0, invoice, scalar schema**. Текст получен существующими `schema_for("invoice", "P0")` и `prompt_text("invoice", "P0", schema)` из [harness/run.py:41](<project>/harness/run.py:41) / [harness/run.py:51](<project>/harness/run.py:51); шаблон — [protocol/prompts/P0_neutral.txt:1](<project>/protocol/prompts/P0_neutral.txt:1). Использован настоящий код `prompt_utils.py` как отдельный файл (его верхнеуровневые imports только из стандартной библиотеки), downloaded `chat_template.jinja` и special tokens из `tokenizer_config.json`. Текст Jinja отрисован **по шаблону**, без `AutoProcessor` и без загрузки tokenizer/model: из установленного HF файла исполнена только функция компиляции Jinja ([.venv/lib/python3.12/site-packages/transformers/utils/chat_template_utils.py:534](<project>/.venv/lib/python3.12/site-packages/transformers/utils/chat_template_utils.py:534)). Для Gemma также исполнены только три текстовых метода wrapper с зависимостями на helper вместо импортов пакета; подготовка тензоров блокировалась sentinel. Для Qwen эквивалентный текстовый renderer воспроизводит объединение special tokens/kwargs из ProcessorMixin; полный ProcessorMixin не исполнялся.

Для каждой модели recorder подтвердил `enable_thinking=False` на входе в Jinja, одну картинку в messages и `tokenize=False`. Проверка `sys.modules` завершилась пустым списком для `mlx`, `mlx_vlm`, `torch`, `transformers`. Ниже — полный текст выхода **apply_chat_template**, до расширения image placeholder на сетку visual tokens в image processor. Значение 1120 не должно появляться в этом тексте: expansion происходит позднее ([mlx_vlm/models/gemma4/processing_gemma4.py:605](<project>/.venv/lib/python3.12/site-packages/mlx_vlm/models/gemma4/processing_gemma4.py:605)). SHA256 относится к точной UTF-8 строке; для контроля последнего переноса указан `repr` её окончания.

**mlx-community/Qwen3-VL-8B-Instruct-4bit**

Путь: `models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit`. Revision: `defcdea7cc7a4b0858fea563cbbce171d328e457`; [HF API этой revision](https://huggingface.co/api/models/mlx-community/Qwen3-VL-8B-Instruct-4bit/revision/defcdea7cc7a4b0858fea563cbbce171d328e457?blobs=true).

На диске: `5647820 KiB` (`du -sk`), то есть **5 783 367 680 B**; logical payload всех 17 файлов репозитория — 5 776 633 051 B, safetensors — 5 760 665 246 B. Все 17 HF metadata содержат нужную revision. SHA256: **OK**; в каждой строке ниже HF API SHA256 = локальный SHA256.

```text
7c637158b2203e321d83596d3661f33b7b98a72beddfaaaa0eddc512acbdd1fb  model-00001-of-00002.safetensors  OK
77190cd1dcf244522869bf923558340112b26d7db2ef3692f88407dd9b33c25d  model-00002-of-00002.safetensors  OK
```

Бюджет: `max_pixels=16777216`, `min_pixels=65536` по [preprocessor_config.json:1](<project>/models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit/preprocessor_config.json:1); это defaults, отдельный «OCR recommended» — **не найдено**. Наш `Runner(max_pixels=N)` передаёт N до image processor; `min_pixels` остаётся 65536, поскольку Runner не имеет этого аргумента.

Thinking off: **подтверждено для выбранного Instruct**. Флаг до Jinja дошёл, но в [chat_template.jinja:118](<project>/models_cache/mlx-community__Qwen3-VL-8B-Instruct-4bit/chat_template.jinja:118) вообще нет переключателя `enable_thinking` и не открывается `<think>`: Instruct и Thinking здесь разные checkpoints. Префикс заканчивается на assistant + LF.

Итоговый промпт для одной картинки и P0/invoice:

```text
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.
<|im_end|>
<|im_start|>assistant
```

Точная строка: 1230 символов; UTF-8 SHA256 `de8185be879c913c02576a39bbb57456d9dee73292c1af0e9e16c9bd6301be25`. Окончание (`repr`): `'ption": "total including tax"}}}\nReturn only the JSON object.\n<|im_end|>\n<|im_start|>assistant\n'`.

**mlx-community/Qwen3.5-4B-4bit**

Путь: `models_cache/mlx-community__Qwen3.5-4B-4bit`. Revision: `0e7ffd5c629ef7719d4cbc04069232580bfa9d9c`; [HF API этой revision](https://huggingface.co/api/models/mlx-community/Qwen3.5-4B-4bit/revision/0e7ffd5c629ef7719d4cbc04069232580bfa9d9c?blobs=true).

На диске: `2997928 KiB` (`du -sk`), то есть **3 069 878 272 B**; logical payload всех 11 файлов репозитория — 3 061 130 647 B, safetensors — 3 034 300 695 B. Все 11 HF metadata содержат нужную revision. SHA256: **OK**; в каждой строке ниже HF API SHA256 = локальный SHA256.

```text
5fb9acd0246866381cf8c5c354c6db1019f6498eec4ccb4f5edcc71ffeacb2db  model.safetensors  OK
```

Бюджет: `max_pixels=16777216`, `min_pixels=65536` по [processor_config.json:1](<project>/models_cache/mlx-community__Qwen3.5-4B-4bit/processor_config.json:1); это defaults, отдельный «OCR recommended» — **не найдено**. Наш `Runner(max_pixels=N)` передаёт N до image processor; `min_pixels` остаётся 65536, поскольку Runner не имеет этого аргумента.

Thinking off: **подтверждено по [chat_template.jinja:147](<project>/models_cache/mlx-community__Qwen3.5-4B-4bit/chat_template.jinja:147)**: `False` добавляет уже закрытый пустой блок `<think>\n\n</think>\n\n`; `True` оставляет открытый `<think>`. Блок выключения входит во входной prompt, а не является ответом модели.

Итоговый промпт для одной картинки и P0/invoice:

```text
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<|im_end|>
<|im_start|>assistant
<think>

</think>

```

Точная строка: 1248 символов; UTF-8 SHA256 `266d2b64dbff2a7211d132303a68cbd58c645f7dd4584595b72856d611741731`. Окончание (`repr`): `'luding tax"}}}\nReturn only the JSON object.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'`.

**mlx-community/Qwen3.5-9B-4bit**

Путь: `models_cache/mlx-community__Qwen3.5-9B-4bit`. Revision: `8b2b98c00a6b4d291155e4890773ca8f769aee53`; [HF API этой revision](https://huggingface.co/api/models/mlx-community/Qwen3.5-9B-4bit/revision/8b2b98c00a6b4d291155e4890773ca8f769aee53?blobs=true).

На диске: `5854924 KiB` (`du -sk`), то есть **5 995 442 176 B**; logical payload всех 13 файлов репозитория — 5 977 073 303 B, safetensors — 5 950 221 072 B. Все 13 HF metadata содержат нужную revision. SHA256: **OK**; в каждой строке ниже HF API SHA256 = локальный SHA256.

```text
a68b87558c6ef43f74c2bd63ce7e9092ceddc3101f3def0030774bae5f42aadd  model-00001-of-00002.safetensors  OK
b0a770bf8469c7f3f18756a0e0283f1c1174344a83e059a4e483f6af4907352d  model-00002-of-00002.safetensors  OK
```

Бюджет: `max_pixels=16777216`, `min_pixels=65536` по [processor_config.json:1](<project>/models_cache/mlx-community__Qwen3.5-9B-4bit/processor_config.json:1); это defaults, отдельный «OCR recommended» — **не найдено**. Наш `Runner(max_pixels=N)` передаёт N до image processor; `min_pixels` остаётся 65536, поскольку Runner не имеет этого аргумента.

Thinking off: **подтверждено по [chat_template.jinja:147](<project>/models_cache/mlx-community__Qwen3.5-9B-4bit/chat_template.jinja:147)**: `False` добавляет уже закрытый пустой блок `<think>\n\n</think>\n\n`; `True` оставляет открытый `<think>`. Блок выключения входит во входной prompt, а не является ответом модели.

Итоговый промпт для одной картинки и P0/invoice:

```text
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<|im_end|>
<|im_start|>assistant
<think>

</think>

```

Точная строка: 1248 символов; UTF-8 SHA256 `266d2b64dbff2a7211d132303a68cbd58c645f7dd4584595b72856d611741731`. Окончание (`repr`): `'luding tax"}}}\nReturn only the JSON object.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'`.

**mlx-community/gemma-4-e4b-it-4bit**

Путь: `models_cache/mlx-community__gemma-4-e4b-it-4bit`. Revision: `475b9088d29754a3379866cf5aeb6b41acd313c2`; [HF API этой revision](https://huggingface.co/api/models/mlx-community/gemma-4-e4b-it-4bit/revision/475b9088d29754a3379866cf5aeb6b41acd313c2?blobs=true).

На диске: `5068112 KiB` (`du -sk`), то есть **5 189 746 688 B**; logical payload всех 10 файлов репозитория — 5 179 241 512 B, safetensors — 5 146 800 534 B. Все 10 HF metadata содержат нужную revision. SHA256: **OK**; в каждой строке ниже HF API SHA256 = локальный SHA256.

```text
932b8271fc3fe65adcc78b96c10c6268bbfb13e8f67d1358727c0d6ee97e1eff  model.safetensors  OK
```

Бюджет для OCR по задаче: **`processor.image_processor.max_soft_tokens = 1120` после load**. Исходный [processor_config.json:1](<project>/models_cache/mlx-community__gemma-4-e4b-it-4bit/processor_config.json:1) содержит 280; текущий Runner также оставит 280. Это свойство processor в RAM для будущего запуска, а не изменение скачанного config.

Thinking off: **подтверждено по [chat_template.jinja:179](<project>/models_cache/mlx-community__gemma-4-e4b-it-4bit/chat_template.jinja:179) / [chat_template.jinja:356](<project>/models_cache/mlx-community__gemma-4-e4b-it-4bit/chat_template.jinja:356)**: `False` не добавляет `<|think|>` в system, а generation prefix остаётся `<|turn>model\n` без thought-блока.

Итоговый промпт для одной картинки и P0/invoice:

```text
<bos><|turn>user
<|image|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<turn|>
<|turn>model
```

Точная строка: 1183 символов; UTF-8 SHA256 `77582de45a44ec2f44700dbefce1661bf502f27d70225c78f9a03dd65b625a21`. Окончание (`repr`): `'ll"], "description": "total including tax"}}}\nReturn only the JSON object.<turn|>\n<|turn>model\n'`.

**mlx-community/gemma-4-12B-it-4bit**

Путь: `models_cache/mlx-community__gemma-4-12B-it-4bit`. Revision: `73bcf09092aa277861d5a191b989b666f7f32e8f`; [HF API этой revision](https://huggingface.co/api/models/mlx-community/gemma-4-12B-it-4bit/revision/73bcf09092aa277861d5a191b989b666f7f32e8f?blobs=true).

На диске: `6630640 KiB` (`du -sk`), то есть **6 789 775 360 B**; logical payload всех 11 файлов репозитория — 6 773 372 848 B, safetensors — 6 741 039 511 B. Все 11 HF metadata содержат нужную revision. SHA256: **OK**; в каждой строке ниже HF API SHA256 = локальный SHA256.

```text
0d58feed0c98a69c07317b4481aeae5ab2785f12a496ea96ab24c4842808de78  model-00001-of-00002.safetensors  OK
5b00a1bcb596ce6e827b4cdea6ecf2a0f35bb01306eb87c1ea4b3bcde36c7755  model-00002-of-00002.safetensors  OK
```

Бюджет для OCR по задаче: **`processor.image_processor.max_soft_tokens = 1120` после load**. Исходный [processor_config.json:1](<project>/models_cache/mlx-community__gemma-4-12B-it-4bit/processor_config.json:1) содержит 280; текущий Runner также оставит 280. Это свойство processor в RAM для будущего запуска, а не изменение скачанного config.

Thinking off: **подтверждено по [chat_template.jinja:179](<project>/models_cache/mlx-community__gemma-4-12B-it-4bit/chat_template.jinja:179) / [chat_template.jinja:356](<project>/models_cache/mlx-community__gemma-4-12B-it-4bit/chat_template.jinja:356)**: `False` не включает `<|think|>`, а generation prefix заканчивается на закрытый пустой thought channel `<|channel>thought\n<channel|>`.

Итоговый промпт для одной картинки и P0/invoice:

```text
<bos><|turn>user
<|image|>Extract the data from this invoice into JSON that matches this schema:
{"type": "object", "additionalProperties": false, "required": ["invoice_number", "issue_date", "due_date", "currency", "seller_name", "seller_vat_id", "seller_iban", "buyer_name", "buyer_vat_id", "purchase_order", "total_net", "total_tax", "total_gross"], "properties": {"invoice_number": {"type": ["string", "null"]}, "issue_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "due_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"}, "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. EUR"}, "seller_name": {"type": ["string", "null"]}, "seller_vat_id": {"type": ["string", "null"]}, "seller_iban": {"type": ["string", "null"]}, "buyer_name": {"type": ["string", "null"]}, "buyer_vat_id": {"type": ["string", "null"]}, "purchase_order": {"type": ["string", "null"], "description": "buyer order / PO reference"}, "total_net": {"type": ["string", "null"]}, "total_tax": {"type": ["string", "null"]}, "total_gross": {"type": ["string", "null"], "description": "total including tax"}}}
Return only the JSON object.<turn|>
<|turn>model
<|channel>thought
<channel|>
```

Точная строка: 1211 символов; UTF-8 SHA256 `9ba40b787eacdd1d18f5278f355ac1c91083ce8638369b70f19eec5a6d57f6b2`. Окончание (`repr`): `'including tax"}}}\nReturn only the JSON object.<turn|>\n<|turn>model\n<|channel>thought\n<channel|>'`.

**Что требуется перед будущим первым кругом**

Веса готовы у всех пяти моделей. Для Gemma конвейеру нужен post-load атрибут `max_soft_tokens=1120`; передачей текущего `max_pixels` этот бюджет не установить. Для Qwen рабочий путь `Runner(max_pixels=N)` подтверждён, но единое специальное OCR-значение N в исследованных источниках не найдено и должно быть зафиксировано протоколом отдельно. Во всех пяти случаях отключение thinking разобрано по закреплённому template; инференсом это сейчас не проверялось.
