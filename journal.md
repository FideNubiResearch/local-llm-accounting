# Журнал исследования

Шаблон записи:

```
## ГГГГ-ММ-ДД — краткий заголовок
Цель:
Действия / команды:
Результат:
Статус: успешно / проблема / отложено
Следующий шаг:
```

---

## 2026-11-10 — Старт, план v1

Цель: определить план исследования локальных LLM для бухгалтерских документов на Mac mini M4 16 ГБ.

Действия:
- Поиск свежих работ 2026 года: ExtractBench, UniKIE-Bench, ReceiptBench, Electricity invoices, Abstention as prompt artifact, lift/NuExtract3.
- Поиск наборов данных: DocILE, CORD, SROIE, FATURA, ZUGFeRD corpus, VAREX.
- Публичных наборов сербских/черногорских счетов не найдено.
- Изучен калькулятор fidenubi.com: оценки памяти и скорости для M4 16 ГБ.

Результат: `00-plan.md` v1. На системе ничего не устанавливалось.

Статус: ждём решений владельца (раздел 10 плана).

Следующий шаг: фаза 0 — дочитать VAREX, RealDocBench, DocAttriBench, подтвердить зазор.

## 2026-11-10 — План v2 по ответам владельца

Решения владельца:
- Документы: любые бухгалтерские, только open-source. Свои документы не даём.
- Языки: английский, любые европейские, азиатские (CJK). Языки — главная ось, по ним будут отдельные публикации.
- Сербский/черногорский синтетический набор — убрать.
- Установка инструментов — разрешена.
- sudo — будет выдан.
- Публикация: только замеры, в fidenubi.com и для бэклинков.

Действия: поиск многоязычных наборов (GitHub/HF): XFUND, SCID, KORIE, CORD, CORU, InvoicesReceiptsPT, synthetic-receipts-ocr, Japanese Mobile Receipt; e-счета ZUGFeRD/XRechnung/FatturaPA/KSeF/Peppol; выписки, финотчёты (Kleister, FinTabNet).

Результат: `00-plan.md` v2.

Статус: ждём ответа по облачному эталону и согласия на старт фаз 0–1.

## 2026-11-10 — План v2.1

Решения владельца:
- облачный эталон не нужен, только локальные модели;
- NC-наборы допустимы: публикуем только замеры;
- прогоны непрерывные, без привязки к ночи;
- отсутствующие поля — прежде всего вопросами о том, чего нет в документе.

Проверено поиском: готовых наборов документов с замаскированными полями нет (есть только UNK-VQA на обычных фото, QASPER/SQuAD2 на тексте). Маскирование остаётся дополнительным тестом и нашим вкладом.

Результат: `00-plan.md` v2.1. Срок ≈7–10 дней: 2–3 дня подготовка, затем прогоны 24/7.

Статус: ждём старта фаз 0–1.

## 2026-11-10 — План v2.2: один запуск

Решение владельца: сначала полностью подготовить всё, потом один непрерывный запуск, в конце — готовые результаты.

Принято:
- очередь экспериментов в `study.yaml`;
- пре-регистрация правил отбора финалистов;
- модели скачиваются и удаляются по очереди;
- автоостановка при явных ошибках, продолжение после сбоя;
- статус прогона в `runs/STATUS.md`;
- каркас многоразовый для следующих исследований.

Статус: ждём старта подготовки (фазы 0–2).

## 2026-11-10 — v2.3: review answers, row-cell hygiene
- Review app: every question now has its own answer set that literally answers it (value: совпадает / другое значение / нет в документе / не могу понять; absence: нет / есть + значение / не могу понять; mask: закрашено / видно / не могу понять). Keys 1–4. Possible print formats of amounts/dates shown. Verdict codes: ok, other, absent, present, mask_bad, unsure (documented in tools/review_app.py).
- Found via review (invbench__INV-2026-0145): invoice_benchmark GT holds net values that are not printed (document prints gross unit prices and "subtotal incl. VAT"). Scalars were already excluded as not_visible; line items were not checked at all.
- New: cell-level hygiene for line_items/transactions (doc.json `row_skip` = [[row, key], ...]); invisible cells are not scored; a row field with >50% invisible cells is excluded (`rows_not_visible`). score_rows(skip=...) / score_doc(row_skip=...).
- Visibility fixes: amounts with trailing zeros after the decimal separator ("9,9000" = 9.90); number boundaries for literal matches ("100" is not visible in "1000"); word coverage ≥85% for text wrapped across table lines.
- Result: 101 GT cells excluded (zugferd 32, invoice_benchmark 47, katanaml 8, bank_statement_intel 14); 3 row fields dropped. Tests: 18 passed.

## 2026-11-10 — v2.4: GT audit by Claude (see 04-gt-audit.md)
- All 88 masked variants checked on crop sheets (tools/audit_masks.py) + OCR of masked page: 32 invalid (value printed twice / handwritten / in words / option label). New mask kinds: label_kept, field_removed (FATURA), still_printed (auto), invalid (review).
- Absence claims: FATURA adapter fixed (BILL_TO, AMOUNT_DUE; SHIP_TO/GST/site-only/total-in-words -> excluded); absence detector prefix matching (German compounds) + tax words in more languages; PT and WildReceipt errors fixed by verdicts.
- Present values: automatic visibility over all values; WildReceipt added to visibility check; visibility uses page text only (OCR + PDF layer), never dataset-provided text; XFUND checkbox pairs dropped, dot leaders ignored.
- harness/review.py applies verdicts after every build (human > claude). Review app: blind audit queue "0. Проверка Claude", mask question reworded; tools/agreement.py.
- Corpus: 710 docs; 3754 present, 387 absent, 1048 foreign probes, 58 clean masks, 329 excluded. Tests: 20 passed.

## 2026-11-10 — v2.5: full-page review (user: crops are not enough)
- tools/page_sheets.py: whole pages at ~0.6 MP (9-pt A4 text still readable), several docs per sheet, masked area outlined.
- All 87 masked docs and all docs with absence claims (fatura, cord, wildreceipt, pt, zugferd, synthetic clean + photo twin) reviewed page by page; verdicts in data/review/verdicts.jsonl (method "full page...").
- New findings: values readable inside e-mails/signatures/second form copy; ROSS date/time printed; Acme ZUGFeRD XML is a different invoice; 7 German invoices with Käufer-/Buchungsreferenz -> PO excluded; ambiguous tax lines excluded.
- Fixes: bare-integer amount variants need >=4 digits; claude "ok" on a mask clears an automatic still_printed flag.
- Result: 375 absence probes and 59 clean masks, all full-page verified; 3754 present values; 342 excluded.

## 2026-11-11 — v3: frozen final set, new sources, cleanup
- final/ is the dataset: one answers.json per document with canonical answers; forms (XFUND) and table fields out; only confirmed nulls; masks kept where both reviews agree (commit 9a26097).
- Added EuroDocBench invoices (8 languages on the same 5 layouts, fr 65 after dropping docs with a missing separator glyph) and 60 more synthetic receipts each de/fr/it (commit eacdd8d). Total 1574 documents.
- Sufficiency rules and their consequences recorded in 00-plan.md section 3 (language comparison on EuroDocBench, real-doc claims only en/de/pt/id/ko, statements out of round 1).
- Cleanup: review/build tools, intermediate corpus, staging and raw downloads removed (reports/cleanup_plan.md). Remaining code: runner, score, normalize, fetch.

## 2026-11-11 — final/: 3 CORD answers fixed
- cord__067 total 950000 -> 9500 (printed 9.500,00); cord__041 subtotal 31601700 -> 316017, total 36500000 -> 365000
  (printed 316017.00 / 365000.00). Cause: build_final's "IDR has no decimals" rule concatenated all digits, including
  the printed ",00"/".00". Found by checking that every `printed` matches its `answer` with the scorer (0 other mismatches).

## 2026-11-11 — pipeline, dashboard, round 1 queued (WHERE WE STOPPED)
Done:
- Pipeline over final/: `harness/run.py` (model x prompt, resumable), `harness/report.py` (scores vs answers.json),
  `harness/dashboard.py` -> runs/dashboard.html (local page: queue, dataset, runs, per-language and per-field scores;
  aggregates only). Open: `uv run python -m harness.dashboard && open runs/dashboard.html`.
- Smoke run (33 docs, one per source x lang x type), Qwen3-VL-4B, old P1: 11 s/doc, peak 4.8 GB, value accuracy 94%,
  JSON valid 100%, format ok 71%; invented values only on receipts (subtotal filled with total 10/10; missing total 3/3).
- P1 fixed (owner approved): "copy exactly" only for names/ids; dates, times, currency, amounts in the requested form.
  Re-check on the same 33 docs: runs/smoke_qwen3vl4b_P1v2.
- Model catalog by helper: reports/models_catalog.md. Round 1 decided (owner approved, no pilot): 6 VLMs x all
  1574 docs x P1, est. ~48 h: Qwen3-VL 4B/8B, Qwen3.5 4B/9B, Gemma 4 E4B/12B. Second round (finalists only):
  P0/P2, constrained decoding, 6/8 bit, extractors NuExtract3 and lift. Not used: GLM-4.1V Thinking (thinking cannot
  be turned off), MiniCPM-V 4.5 and InternVL3.5 (no MLX weights).
- Queue: protocol/round1.json, runner `caffeinate -i uv run python -m harness.study protocol/round1.json`
  (strict order; finished runs skipped; entries with "hold" wait, file re-read every minute).
Next:
1. Compare smoke P1v2 vs P1 (format ok should rise), then start the queue.
2. Helper task pending (asleep until 14:00): reports/models_setup.md - download the 5 models, how to set the image
   budget in mlx-vlm 0.7.10 (Gemma: 1120 visual tokens, default 280 is too low for A4), whether
   enable_thinking=False reaches the chat template (Qwen3.5, Gemma), rendered prompts.
3. After that: add Gemma's image-budget parameter to run.py/runner.py if needed, record it in round1.json,
   remove "hold" from Qwen3.5 / Gemma entries. Rule: every model gets its documented OCR image budget.

## 2026-11-11 — пять моделей готовы, «hold» снят

- Помощник скачал пять моделей и сверил SHA256 всех 8 safetensors с HF API: reports/models_setup.md.
- «Думание» выключается шаблоном у всех пяти. У Qwen3-VL Instruct переключателя нет. Qwen3.5 получает закрытый пустой `<think></think>`. Gemma не получает `<|think|>`, у 12B пустой канал thought. Проверено по шаблону, не инференсом: первые ответы Qwen3.5 и Gemma нужно проверить на остатки рассуждений.
- Бюджет картинки Gemma: mlx-vlm 0.7.10 отбрасывает `max_soft_tokens` в stream_generate, поэтому `Runner` задаёт `processor.image_processor.max_soft_tokens` после load(). Проверено процессором без весов на странице A4 1241×1754: 278 → 1104 токенов у E4B, 282 → 1108 у 12B.
- Qwen работает со штатным max_pixels чекпойнта (65 536–16 777 216). Отдельного значения для OCR в источниках нет.
- В config.json прогона теперь есть `image_processor`: значения, прочитанные у процессора после настройки.
- В round1.json снят «hold», для Gemma добавлено `max_soft_tokens: 1120`. Очередь перезапущена на 780/1574 Qwen3-VL-4B: старый процесс держал прежний код и упал бы на новом параметре.

## 2026-11-13 — проверка входных данных по результатам раунда 1 (gt_check)

Цель: по ошибкам моделей найти ошибки в ответах (answers.json), документах, определениях полей и промпте P1.
Уровень 1 — ошиблись все 6 моделей на паре (doc, field); уровень 2 — больше 50% моделей (4–5 из 6).
Ошибка = WV / FN / FF; TP / TN — верно; canonical=False ошибкой не считается.

- План (Opus 5.5, high): reports/gt_check/PLAN.md. Раунд 1 полный: 6 прогонов × 14561 пар (doc, field), ключи совпадают.
- Код (Opus 5.5, medium): harness/gt_check.py, tests/test_gt_check.py (24 теста, весь набор 47 зелёный).
  Запуск: `uv run python -m harness.gt_check`, вывод в reports/gt_check/ (votes, suspects, by_*, docs, clusters, report.md, review/queue.csv).
- Прогон (Sonnet): все проверки целостности прошли. L1 = 245 (88 со значением, 157 с null), L2 = 638.
  Гистограмма числа ошибшихся моделей: {0:11252, 1:1552, 2:581, 3:293, 4:179, 5:459, 6:245}.
  Подсказки по L1+L2: sibling_copy 539, scorer_strict 124, gt_value_suspect 83, gt_null_suspect 15, value_not_found 15, mask_leak 10, scattered 97.
- Гипотезы (ещё не вердикты): synrec subtotal — модели копируют total (2411 из 2720 FF); PT seller_name — бренд vs юр. лицо;
  PT VAT — префикс «PT» не снимается нормализацией; EuroDocBench имена — модели добавляют адрес; SROIE total=null и FATURA totals — вероятно ошибки GT;
  cord__020 total (GT 377859, модели 377059), cord__031 tax_amount.
- Ревью: очередь 682 позиции (план оценивал ~300). Слепое чтение страницы → вердикт → review/verdicts.jsonl. final/ не меняется;
  исправления — в review/proposed_fixes.csv на одобрение владельца.
  Агент Sonnet упал на ошибке API (403) после 50 вердиктов (2 пачки): scorer_too_strict 18, definition_ambiguity 18,
  model_failure 8, gt_wrong 4, doc_unreadable 1, unsure 1. Продолжение с позиции 51; ход ревью — review/PROGRESS.md.

### 2026-11-13 — ревью gt_check: 200 из 682 (пачки 1–8)
- Пройдены приоритеты 1–2 целиком и начало 3; остановка на cord__020::tax_amount, дальше — пачка 9. Повторный прогон checker: exit 0.
- Вердикты (200): definition_ambiguity 79, scorer_too_strict 60, model_failure 46, gt_wrong 5, ok 4 (контроли), unsure 2, doc_unreadable 2, doc_mismatch 2.
  Скрытые контроли: 7 из 25 попали в просмотренное, все 7 верно. Вердикт «ok» не входит в VERDICTS (harness/gt_check.py:52) — в таблицу кластеров не считается.
- Ошибки GT (review/proposed_fixes.csv, final/ не менялся): zugferd Rechnungskorrektur buyer_name и seller_name (в ответ попал блок GLN/Kunden-Nr.);
  Konik acme invoice-42 total_tax 19 (ставка) → 269.80; zugferd v1 Haftpflicht buyer_name «Herrn\nMax Mustermann» → Max Mustermann;
  pt__20210508_202709 seller_name (низкая уверенность).
- Промпт/определения: receipt total = «total amount paid» (fields.yaml:29) → модели дают «BAR/наличные»; subtotal без строки подытога;
  знак у сумм возвратов; бренд vs юр. лицо в seller_name (PT непоследовательно); имя без адреса (EuroDocBench);
  dd/mm vs mm/dd в synrec (генератор непоследователен); PB1 — налог, сервисный сбор — нет (CORD); tax 0 vs null; префиксы серий в номерах счетов.
- Скорер слишком строгий (предложения для normalize.py): N.text — диакритика, юр. формы, обращения Herr/Frau, пробелы, вложение имени;
  N.ident_value — префикс страны, «No.», хвост «/CRC…»; корейские «(주)/㈜».
- Ждут решения владельца: политика seller_name, subtotal/tax при отсутствии строки, неоднозначные даты, знак отрицательных сумм, продолжать ли ревью (пачки 9–28).

### 2026-11-13 — решения владельца по итогам ревью (200/682)
1. seller_name / merchant_name: засчитываются оба — бренд и юридическое лицо.
2. subtotal / tax_amount, если строка не напечатана: ответ null (GT остаётся null; модели, заполнившие поле, ошибаются; промпт уточнить).
3. Неоднозначные даты (день и месяц ≤ 12): засчитываются оба порядка.
4. Знак суммы игнорируется (возвраты, кредит-ноты, суммы в скобках).
5. Ревью продолжается: пачки 9–28.
Изменения скорера / GT / промпта по этим решениям — после окончания ревью, отдельным шагом; final/ пока не трогаем.

### 2026-11-13 — ревью gt_check завершено: 682/682
- Пачки 9–28 (482): model_failure 252, ok 172, scorer_too_strict 29, definition_ambiguity 28, gt_null_wrong 1.
  Итого 682: model_failure 298, ok 176, definition_ambiguity 107, scorer_too_strict 89, gt_wrong 5, gt_null_wrong 1,
  doc_unreadable 2, doc_mismatch 2, unsure 2. Контроли: 25/25 верно. Повторный прогон checker: exit 0.
- Вывод: из 883 подозрительных пар (L1+L2) ошибок в GT мало — 6 (review/proposed_fixes.csv); основная масса —
  ошибки моделей и неоднозначность определений/строгий скорер. Входные данные в целом подтверждены.
- Новая ошибка GT: cord__009 total null → 36000 (напечатан только «Sub Total 36000», есть наличные и сдача; уверенность средняя).
- Проблемы документов: wild__0426, wild__0428 — стоковые макеты, арифметика не сходится; wild__0352 — ширина 258 px;
  маски, где значение выводится арифметикой (sroie X51007579725, X51005719898, X51008099088; fatura/wild total = SUB_TOTAL+TAX);
  sroie X51007846304 и wild__0298__mask — видна округлённая сумма.
- Новые вопросы к определениям: FATURA с одним только SUB_TOTAL или TOTAL (null или копировать в total_gross/total_net);
  seller_vat_id — Steuernummer/NIPC или только VAT id; seller_name, когда напечатан только дилер/станция (galp, «GAR. RIBAMAR»).
- Скорер: бренд из [P-seller] не проходит (다이소, CU, McDonald's, ROSS DRESS FOR LESS) — GT хранит одно значение, нужен список
  допустимых вариантов; причуды строк GT ('JAWEDHABIB', "Mcdonald'sHazeldonk-west", ' .. ', 'FS A / 42799').

### 2026-11-13 — решения владельца (2): суммы, налоговый номер продавца, имя продавца
1. Суммы счёта (total_gross / total_net / total_tax): отсутствующая сумма = null, копировать нельзя. Если в документе напечатана
   только одна сумма, её верное извлечение засчитывается, в какое бы поле (total_gross или total_net) модель её ни записала.
   Отсутствующие суммы из оценки исключаются (не FF).
   Отличие от решения (1) п.2: для subtotal/tax_amount чеков null остаётся оцениваемым, заполнение — ошибка модели.
2. seller_vat_id: засчитывается любой налоговый идентификатор продавца (VAT id, Steuernummer, NIPC/NIF и т. п.).
3. seller_name / merchant_name: любое опознаваемое имя продавца — бренд, юр. лицо, дилер, станция; все верные варианты принимаются.

### 2026-11-13 — план закрытия проблем: 05-closeout-plan.md
Этапы: 0 — правки GT и скорер (идёт); 1 — данные → final v4 (стоковые макеты, некорректные маски, две величины на странице,
метки качества, префиксы серий); 2 — расширенная проверка GT (пары 3/6, арифметика GT, аудит 200 согласных пар) → final v5;
3 — новый прогон r1b: 6 моделей × весь набор × P1b (~44 ч), потому что ошибки, вызванные формулировками P1, пересчётом не исправить;
4 — раунд 2 на базе r1b, P0/P2 переписать с теми же определениями.

### 2026-11-13 — решения владельца (3)
- wild__0426, wild__0428 (стоковые макеты) исключаются.
- Номер счёта: засчитывается и с префиксом серии (FS, FT, NFS, …), и без него.
- Суммы счёта — итог именно этого счёта, без долгов по прошлым счетам, переплат и зачётов. zugferd Kraftfahrversicherung:
  total_gross = 220 (не 440 «zu zahlender Beitrag» = взнос + долг). GT не меняется; оговорка — в промпт P1b (и для total чека).
- Решения по префиксам серий и P1b переданы агенту этапа 0.
- Полный прогон r1b (6 моделей × весь набор × P1b, ~44 ч) одобрен. Запуск после этапов 0–2 (final v5) и smoke-теста P1b.
  Все решения владельца по 05-closeout-plan.md закрыты.

### 2026-11-13 — правка final/ по итогам ревью GT, новые правила скорера, P1b, пересчёт раунда 1

Владелец разрешил править замороженный final/. Решения: журнал 2026-11-13 (1), (2) и два новых (3):
(3a) total_gross / total_net / total_tax — суммы только этого счёта, без долгов прошлых счетов, кредитов и переплат
(Kraftfahrversicherung: GT 220 остаётся, 440 не добавляется); то же для total чека; (3b) invoice_number засчитывается
с префиксом серии и без него (FS, FT, FTR, NFS, FR, C2 / …), цифры должны совпасть точно.
Скрипт: `tools/apply_gt_review.py` (идемпотентен); машиночитаемый список: reports/gt_check/applied_fixes.csv (117 строк).

**A1. Исправления GT** (все 5 сверены со страницей; пропущенных нет):
- cord__009 total: null → '36000'. receipt has no Total line; 'Sub Total 36000', Discount (0 %), Tunai 50000, Kembalian 14000: the amount due 36000 is printed (as Sub Total) and equals cash - change; verdict gt_null_wrong (med)
- zugferd…v1_correct_Konik_acme_invoice-42_ZUGFeRD.pdf total_tax: '19' → '269.80'. page: 'Umsatzsteuer 19% 269,80' under 'Summe netto 1.420,00'; GT held the VAT rate; verdict gt_wrong (high)
- zugferd…v2_correct_intarsys_BASIC_zugferd_2p0_BASIC_Rechnungskorrektur.pdf buyer_name: 'GLN 4304171000002 \nKunden-Nr. : 009420\nMUSTER-KUNDE GMBH' → 'MUSTER-KUNDE GMBH'. page 1 Käufer block: GLN and Kunden-Nr. lines are not the name; verdict gt_wrong (high)
- zugferd…v2_correct_intarsys_BASIC_zugferd_2p0_BASIC_Rechnungskorrektur.pdf seller_name: 'GLN 4333741000005 \nLief-Nr: 549910\nMUSTERLIEFERANT GMBH' → 'MUSTERLIEFERANT GMBH'. page 1 Verkäufer block: GLN and Lief-Nr lines are not the name; verdict gt_wrong (high)
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Haftpflichtversicherung_Versicherungssteuer.pdf buyer_name: 'Herrn\nMax Mustermann' → 'Max Mustermann'. salutation 'Herrn' is not part of the name; verdict gt_wrong (med)

**A2. Допустимые варианты `accepted`** (33: seller_name 25, merchant_name 7, seller_vat_id 1; старый ответ сохранён; источник — вердикт ревью; варианты, которые новый скорер и так засчитывает, не записывались, кроме pt__20210508_202709 по прямому указанию):
- pt__20210508_202709 seller_name: 'ferragens do combro lda' + 'MTD-FERRAGENS DO COMBRO LDA'. owner rule [seller name]; source: proposed_fixes (low): correct_value; page header reads MTD-FERRAGENS DO COMBRO LDA, first letters partly occluded; old answer kept; verdict gt_wrong
- pt__20210215_172426 seller_name: 'flying tiger' + 'TIGER PORTUGAL, SA'. owner rule [seller name]; source: correct_value / blind_read (legal entity); verdict definition_ambiguity
- pt__20210323_174622 seller_name: 'jumbo' + 'AUCHAN RETAIL PORTUGAL, S.A.'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210508_181909 seller_name: 'botaminuto' + 'Consertos Rapidos Amoreiras, Lda'. owner rule [seller name]; source: correct_value / blind_read (legal); verdict definition_ambiguity
- pt__20210508_202449 seller_name: 'botaminuto' + 'Consertos Rapidos Amoreiras, Lda'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210429_191705 seller_name: 'galp' + 'GASNUNOS - DISTR. COM. GAS LDA'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210429_191705 seller_name: 'galp' + 'GASNUNOS, DISTR. E COM. GAS, LDA'. owner rule [seller name]; source: blind_read (legal entity); verdict definition_ambiguity
- pt__20210429_191705 seller_name: 'galp' + 'GASNUNOS'. owner rule [seller name]; source: prediction confirmed by note '6/6 legal'; verdict definition_ambiguity
- pt__20210507_174441 seller_name: 'galp' + 'SEQUEIRA PINTO - COM. COMB. LDA'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210428_195823 seller_name: 'galp' + 'GAR. RIBAMAR (Campo de Ourique)'. owner rule [seller name]; source: blind_read (station/dealer header); verdict definition_ambiguity
- pt__20210428_195823 seller_name: 'galp' + 'GAR.RIBAMAR-F.CUNHA COSTA'. owner rule [seller name]; source: prediction confirmed by evidence '4 models returned the station/dealer name'; verdict definition_ambiguity
- pt__20210428_201521 seller_name: 'galp' + 'GAR. RIBAMAR (Campo de Ourique)'. owner rule [seller name]; source: blind_read (station header); verdict definition_ambiguity
- pt__20210322_164701 seller_name: 'galp' + 'GALPGESTE, S.A.'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210322_164701 seller_name: 'galp' + 'A.S. LAGOS (FARO/SAGRES)'. owner rule [seller name]; source: blind_read (station); verdict scorer_too_strict
- pt__20210316_215850 seller_name: 'daily mercearia' + 'AZAFAMA CAMPESTRE - Prod. Alim. Unip. Lda'. owner rule [seller name]; source: correct_value (legal); verdict definition_ambiguity
- pt__20210428_232807 seller_name: 'chaviarte' + 'Destreza Aprumada, Lda'. owner rule [seller name]; source: correct_value (legal entity); verdict definition_ambiguity
- pt__20210508_211412 seller_name: 'aki' + 'Dicodis - Distribuição de Bricolage, SA'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210509_002234 seller_name: 'auchan coimbra' + 'AUCHAN RETAIL PORTUGAL, S.A.'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210323_162221 seller_name: 'intermarche' + 'SODIAL PORCHINHOS-SUPERMERCADOS, LDA'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210215_172904 seller_name: 'maria da glória cab.' + 'Maria da Glória Cabeleireiros Lda.'. owner rule [seller name]; source: blind_read (legal entity); verdict scorer_too_strict
- pt__20210320_172744 seller_name: 'requintefinal, lda.' + 'Casa Velha'. owner rule [seller name]; source: blind_read ('Casa Velha is the restaurant brand'); verdict scorer_too_strict
- pt__20210508_204341 seller_name: 'Estação Serviço da Cegonha Lda' + 'ESTAÇÃO SERVIÇO CEGONHA LDA'. owner rule [seller name]; source: blind_read (header form); verdict scorer_too_strict
- sroie__X51006414728 merchant_name: 'FOODELICO SDN. BHD.' + 'KEK SPAN OREE'. owner rule [seller name]; source: correct_value (brand logo); verdict definition_ambiguity
- korie__IMG00339 merchant_name: '(주) 아성다이소 .. 청주산남2호점' + '다이소'. owner rule [seller name]; source: evidence '3 brand-only 다이소', note '[P-seller] brand ok'; verdict scorer_too_strict
- korie__IMG00343 merchant_name: 'CU 청주수곡사랑점' + 'CU'. owner rule [seller name]; source: evidence "2 brand-only 'CU' (ok per [P-seller])"; verdict model_failure
- korie__IMG00013 merchant_name: '이마트 청주점' + '이마트'. owner rule [seller name]; source: note 'brand-only 이마트 would be accepted per [P-seller]'; verdict model_failure
- wild__0332 merchant_name: 'PaneraBread Cafe0994' + 'Panera Bread'. owner rule [seller name]; source: correct_value; verdict scorer_too_strict
- wild__0332__mask merchant_name: 'PaneraBread Cafe0994' + 'Panera Bread'. owner rule [seller name]; source: correct_value; verdict scorer_too_strict
- wild__0377 merchant_name: "Mcdonald'sHazeldonk-west" + "McDonald's". owner rule [seller name]; source: evidence/note: brand-only McDonald's valid per [P-seller]; verdict scorer_too_strict
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_EXTENDED_Kostenrechnung.pdf seller_name: 'MUSTERLIEFERANT GMBH' + 'KOSTENLIEFERANT GMBH'. owner rule [seller name]; source: blind_read: name in the page's Lieferant (supplier) block; verdict doc_mismatch; verdict doc_mismatch
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Haftpflichtversicherung_Versicherungssteuer.pdf seller_name: 'MVM Musterhafter\nVersicherungsverein Musterstadt a.G.' + 'Versicherungsverein Musterstadt a.G.'. owner rule [seller name]; source: blind_read: legal-entity line of the letterhead; verdict scorer_too_strict
- zugferd…v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Kraftfahrversicherung_Bruttopreise.pdf seller_name: 'MVM Musterhafter\nVersicherungsverein Musterstadt a.G.' + 'Versicherungsverein Musterstadt a.G.'. owner rule [seller name]; source: blind_read: legal-entity line of the letterhead; verdict scorer_too_strict
- zugferd…v2_correct_symtrax_Beispiele_BASIC_zugferd_2p1_BASIC_Einfach.pdf seller_vat_id: 'DE123456789' + '201/113/40209'. owner rule [seller tax id]; source: blind_read: 'Steuernummer 201/113/40209 and USt.-Id.-Nr. DE123456789'; verdict definition_ambiguity

**A3. Суммы счёта.** Ответ null и поле не закрашено → поле удалено из answers.json, строка в final/excluded.csv (существующий механизм исключения), null → (не оценивается). 60 полей:
- total_gross (10): fatura__Template26_Instance10, fatura__Template15_Instance100, fatura__Template15_Instance100__mask, fatura__Template19_Instance100, fatura__Template24_Instance0, fatura__Template24_Instance100, fatura__Template24_Instance100__mask, fatura__Template42_Instance1, fatura__Template39_Instance1, fatura__Template39_Instance1__mask
- total_net (15): fatura__Template3_Instance0, fatura__Template34_Instance100, fatura__Template34_Instance100__mask, fatura__Template10_Instance1, fatura__Template10_Instance1__mask, fatura__Template13_Instance1, fatura__Template13_Instance100, fatura__Template26_Instance10, fatura__Template19_Instance100, fatura__Template47_Instance100, fatura__Template47_Instance100__mask, fatura__Template23_Instance10, fatura__Template42_Instance1, fatura__Template22_Instance1, fatura__Template22_Instance1__mask
- total_tax (35): fatura__Template34_Instance100, fatura__Template34_Instance100__mask, fatura__Template10_Instance1, fatura__Template10_Instance1__mask, fatura__Template8_Instance10, fatura__Template8_Instance0, fatura__Template30_Instance10, fatura__Template13_Instance1, fatura__Template13_Instance100, fatura__Template26_Instance10, fatura__Template36_Instance0, fatura__Template15_Instance100, fatura__Template15_Instance100__mask, fatura__Template32_Instance10, fatura__Template32_Instance10__mask, fatura__Template19_Instance100, fatura__Template47_Instance100, fatura__Template47_Instance100__mask, fatura__Template24_Instance0, fatura__Template30_Instance100, fatura__Template30_Instance100__mask, fatura__Template24_Instance100, fatura__Template24_Instance100__mask, fatura__Template23_Instance10, fatura__Template40_Instance1, fatura__Template42_Instance1, fatura__Template49_Instance0, fatura__Template49_Instance0__mask, fatura__Template16_Instance10, fatura__Template30_Instance1, fatura__Template20_Instance100, pt__20210428_144738, pt__20210318_123736, pt__20210318_202746, pt__20210507_203027
`accept_from` (напечатана только одна из total_gross / total_net; сумма засчитывается в любом из двух полей), 19 полей:
- total_gross ← total_net (12): fatura__Template3_Instance0 (1377.77), fatura__Template34_Instance100 (875.45), fatura__Template34_Instance100__mask (875.45), fatura__Template10_Instance1 (796.34), fatura__Template10_Instance1__mask (796.34), fatura__Template13_Instance1 (1149.57), fatura__Template13_Instance100 (213.65), fatura__Template47_Instance100 (303.16), fatura__Template47_Instance100__mask (303.16), fatura__Template23_Instance10 (571.45), fatura__Template22_Instance1 (504.25), fatura__Template22_Instance1__mask (504.25)
- total_net ← total_gross (7): fatura__Template15_Instance100 (241.92), fatura__Template15_Instance100__mask (241.92), fatura__Template24_Instance0 (655.98), fatura__Template24_Instance100 (797.2), fatura__Template24_Instance100__mask (797.2), fatura__Template39_Instance1 (698.43), fatura__Template39_Instance1__mask (698.43)
Закрашенные суммы (3 total_gross masked) остаются в оценке как проверка отсутствия (null — верно). subtotal / tax_amount чеков не менялись.
final/manifest.csv: n_values / n_null пересчитаны у 41 документа; final/README.md: схема accepted / accept_from, итоги (13275 значений, 1226 null).

**B. Скорер** (harness/normalize.py, harness/score.py; у каждого правила тест в tests/test_score.py; правила выключаются по одному через `equal(..., rules=)`, N.LEGACY = скорер раунда 1): date_swap, amount_abs, name_fold, name_legal, name_honorific, name_contain (только имена), id_label, id_crc, id_cc (только налоговые номера), id_series (только invoice_number, префикс может отсутствовать только с одной стороны). score: `accepted`, `accept_from`, колонка `matched_by` в fields.csv.

**C. Промпт.** P1_null.txt и schemas.json не менялись (хэши заморожены в tests/test_prompts.py); тексты полей fields.yaml в промпт не попадают (run.py берёт оттуда только doc_type_human). Новый protocol/prompts/P1b_null.txt (`--prompt P1b`) для раунда 2.

**D. Пересчёт раунда 1** без запуска моделей; runs/ не тронут: `harness.report runs/<run> --out reports/rescore_r1/<run>`, `harness.gt_check --fields-root reports/rescore_r1 --out reports/gt_check_rescored` (exit 0, все проверки зелёные), `harness.rescore_compare` → reports/rescore_r1/compare.md. L1 245 → 195, L2 638 → 516. gt_check на старых runs/*/fields.csv по-прежнему загружается (правки из applied_fixes.csv допускаются), но проверка «скорер воспроизводит outcomes» на них теперь ожидаемо не проходит: они посчитаны старым скорером.

### 2026-11-13 — этап 0 принят
- Проверка: 61 тест зелёный; runs/ не изменён; при пересчёте ни одна верная строка не стала неверной.
  Пересчёт r1 (reports/rescore_r1/compare.md): точность значений +0,7…+2,3 п.п. у всех моделей; L1/L2 245/638 → 195/516.
- Поправка к прежней записи: «total amount paid» из fields.yaml в промпт раунда 1 НЕ попадал (run.py берёт из fields.yaml
  только doc_type_human). В P1 поле total вообще не определено — только ключ схемы. Вывод тот же: нужен P1b с определениями.
- Открыто: засчитывать ли «имя + адрес» (name_contain, 659 строк); GT «Physiotherapeutin» — вероятно ошибка; см. 05-closeout-plan.md п. 1.9.

### 2026-11-13 — решения владельца (4)
- Имя найдено, но с лишним текстом (адрес, юр. форма, вторая строка) — значение верное. Нарушение формата отмечается отдельно (canonical).
- Профессия vs имя: если над именем напечатана профессия, а имя строкой ниже, верным считается имя; если слово служит названием продавца — оно и засчитывается.
  zugferd Physiotherapeut (2 документа): seller_name «Physiotherapeutin» → Tanja Tinder.
- Этап 1 запущен (агент Opus 5.5, medium).

### 2026-11-13 — этап 1 выполнен: final v4 (агент Opus 5.5, medium)
Все правки — скриптом `tools/apply_gt_review.py` (идемпотентен: повторный запуск не меняет ни одного файла, проверено хэшем final/ и applied_fixes.csv); строки этапа 1 — `stage=1` в reports/gt_check/applied_fixes.csv (33 строки; 117 строк этапа 0 не изменились). runs/ не тронут (хэш до/после совпал). Коммита нет — ждёт приёмки.
- 1.1. wild__0426, wild__0428 исключены целиком: строки `*` в final/excluded.csv, убраны из manifest.csv и docs/ (в git остаются).
- 1.2. 19 проб-масок исключены (поле удалено из answers.json `__mask`-документа, строка в excluded.csv с доказательством). Кандидаты: `tools/mask_probe_scan.py` (OCR Apple Vision, правила leak / rounded / a±b(±c) / сумма позиций) → reports/gt_check/stage1/mask_probe_candidates.csv; каждый сверен со страницей. sroie total ×9 (X51007579725, X51005719898, X51008099088, X51007846304, X51005757220, X51006556809, X51006557115, X51006556808, X51009008091), cord total ×4 (014, 070, 020, 072), cord tax_amount ×2 (058, 084), wild__0298 total (видны «Rounding 12.00» и «Adjust 0.02»), wild__0082 total (77.46 + 6.65), wild__0121 subtotal (4.24 − .24), wild__0168 tax_amount (3.05 − 2.50 − 0.20). Оставлены 3 маски FATURA total_gross (Template28_0, 31_0, 43_1): SUB_TOTAL и TAX напечатаны, но TOTAL генератора не равен их сумме — значение не выводится.
- 1.3. BASIC-WL Einfach due_date: accepted 2020-04-04 (страница: «netto bis 04.04.2020» и «Fälligkeit 13.12.2017»). Kostenrechnung v1 seller_name: оба имени уже приняты с этапа 0, страница сверена.
- 1.4. `quality: "low"` (answers.json + колонка manifest `quality`) у 6 документов: wild__0352, sroie__X51006328937, synrec__eval-000608__photo, pt__20210428_141746, pt__20210507_215634, eurodocbench__test-nl-NL-narrow-014. report.py: таблица «All without quality=low documents»; rescore_compare: точность без них.
- 1.5. Вердикты claude-opus (13) в review/verdicts.jsonl, сводка — review/PROGRESS.md. pt__20210428_140713 seller_name: на странице ELENCOJASMIN → accepted (GT jasmim сохранён); pt__20210507_215634 invoice_number: GT FS T1/8072 верен (ok); fatura Template49_Instance0 (+mask) buyer_name: два блока «Bill to» → accepted Joseph Wagner; пограничные name_contain — во всех GT-имя присутствует → TP с canonical=False, ни одного случая «имя не найдено».
- 1.6. final/README.md: дефект генератора synrec (dd/mm и mm/dd), правило date_swap; итоги набора; раздел «Правки этапа 1».
- 1.7. gt_check: `ok` в VERDICTS; `--carry-verdicts` (по умолчанию reports/gt_check/review/verdicts.jsonl) переносит вердикты по review_id (suspects.csv `verdict`/`verdict_source`, queue.csv `prior_verdict`, счётчик в report.md); пересчёт с исключёнными документами (число документов по manifest; exclude_doc допускается при чтении старых runs/). 4 новых теста.
- 1.9a. Для имён canonical=False, если совпадение только через вложение (лишний текст); исход TP не меняется (normalize.name_clean, score.outcome; 3 теста). На r1: 631 строка TP сменила canonical True→False; доля «format ok» по именам 1.000 → 0.905…0.994.
- 1.9b. seller_name обоих Physiotherapeut → Tanja Tinder (page_1 сверены); избыточных accepted не нашлось (единственный — pt__20210508_202709, оставлен по указанию владельца).
- 1.9c. P1b: «a service charge is not tax; local taxes such as PB1 are tax» (P1_null.txt не тронут). FATURA «TAX $0.00» по строкам: ключи total_tax таких счетов исключены ещё на этапе 0; формулировка предложена в отчёте этапа.
- 1.8. Пересчёт: reports/rescore_r1_v2/<run>, gt_check → reports/gt_check_rescored_v2 (exit 0; 232 подозрительных пары помечены перенесёнными вердиктами), сравнение r1 → этап 0 → этап 1 — reports/rescore_r1_v2/compare.md. L1/L2: 245/638 → 195/516 → 186/505. Верно→неверно: 7 строк, все — намеренная правка GT Physiotherapeut (модели ответили «Physiotherapeutin»).
- Итоги final v4: 1572 документа, 13273 значения, 1199 null; 68 тестов зелёные.
- **final v4: sha256 = c14404ba90247a8982f33ec820ebfcdb018c3a123eb70d4c1f5fbe23d8394b58** — от конкатенации всех 1572 final/docs/*/answers.json в порядке путей (`find final/docs -name answers.json | LC_ALL=C sort | xargs cat | shasum -a 256`).

### 2026-11-13 — этап 1 принят; final v4 заморожен
- Поправка при приёмке: zugferd XML-Rechnung_FX_EN16931_Physiotherapeut — на странице поля подписаны
  «Name: Physiotherapeutin», «Ansprechpartner: Tanja Tinder» → это название продавца, по правилу владельца (4) засчитывается.
  Ответ возвращён: Physiotherapeutin. Второй документ (v2 intarsys, без подписей полей: профессия над именем) — Tanja Tinder.
  Вердикт в verdicts.jsonl (reviewer claude-opus, batch stage1-acceptance) отменяет прежний gt_wrong.
- Приёмка: 68 тестов зелёные; tools/apply_gt_review.py идемпотентен (повторный прогон без изменений); runs/ не тронут;
  stage 0 → stage 1 верно→неверно: 1 строка, ожидаемая (qwen3vl-4b, Physiotherapeut v2: «Physiotherapeutin»).
- Пересчёт (reports/rescore_r1_v2/compare.md): L1/L2 245/638 → 195/516 → 185/505; ключей 14472; очередь новых подозрительных — 451.
- final v4: 1572 документа. sha256 (все answers.json в порядке LC_ALL=C sort, cat) =
  4ff069c0af657ea6c9da1ebcb8382a486ec8fc76e690c192e77f6ea7ef7602a7 (заменяет значение из предыдущей записи агента).
- Наблюдение: доля выдуманных значений (FF / (FF + TN)) у qwen 0,49–0,58, у gemma4-12b 0,13 — главный резерв P1b.

### 2026-11-13 — этап 2: код и очередь
- P1b: налог счёта — только строка итога налога; колонка налога по строкам — не итог; нет строки → null.
- harness/gt_arith.py: арифметика самого GT. 56 нарушений, 48 объяснены (скидка/сервисный сбор/округление/генератор FATURA
  напечатаны на странице), 8 не объяснены (invoice_benchmark 5, cord 1, wild 1, zugferd 1). Пример: invbench__INV-2026-0021 —
  сама страница печатает 260 061,20 + 52 010,24 = 312 061,44 (ошибка 10,00 в документе).
- harness/gt_stage2.py: очередь reports/gt_check/stage2/queue.csv — 393 позиции, 16 пачек: arith 7, «3 из 6» 171, аудит
  согласных 200 (стратифицировано по источникам), 15 скрытых контролей. 85 тестов зелёные. Ревью — Sonnet.

### 2026-11-13 — этап 2: ревью 393/393 (Sonnet) и приёмка
- arith 7: все ok — ответы верно копируют страницу; ошибки в самих документах (invbench 0021, 0110, 0115, 0117, 0179;
  zugferd Haftpflicht: срок оплаты 2013-12-06 раньше даты счёта 2014-01-24; wild__0129 — чек на 0,00).
- «3 из 6» (177): model_failure 153, scorer_too_strict 11, definition_ambiguity 6, ok 6, gt_wrong 1.
- Аудит согласных пар: 0 ошибок GT из 200 (без контролей; 95 % Уилсон 0–1,9 %). Расширенный аудит не нужен.
- Контроли: значение GT подтверждено 15/15; 8 контролей в потоке audit_agree помечены ok вместо model_failure
  (ревьюер не сверил предсказания) — на оценку ошибок GT не влияет. Чтение не копирует GT (регистр и формат страницы).
- Ошибка GT: pt__20210323_162221 seller_vat_id <NIF> → <NIF> (страница «CNT: <NIF>»; контрольная цифра NIF
  верна только у 394 — проверено).
- По правилам владельца (к применению): Steuernummer 201/113/40209 в accepted у ~9 документов zugferd XML-Rechnung;
  метка «NIF-IVA» в правиле id_label; имена продавца pt__20210324_200034 (владелец), pt__20210507_214450 (станция/дилер).
- Вопросы владельцу: wild__0016 total 63,92 vs «Amt Due» 63,90 после округления; fatura Template39 seller_name — только
  логотип «LCSR»; zugferd seller_iban, когда напечатан IBAN только другого получателя платежа / налогового представителя.

### 2026-11-13 — решения владельца (5) и final v5
- wild__0016 total: засчитываются 63,92 (Total) и 63,90 (Amt Due после округления).
- fatura Template39_Instance1 (+ __mask) seller_name: исключено (есть только логотип «LCSR»).
- zugferd seller_iban, когда напечатан только IBAN другого получателя платежа / налогового представителя: засчитывается
  этот IBAN (GT AbweichenderZahlungsempf, Innergemeinschaftliche_Lieferungen, intarsys EXTENDED Fremdwaehrung уже его содержит).
- Применено (tools/apply_gt_review.py, stage=2 в applied_fixes.csv): Steuernummer 201/113/40209 в accepted у 18 документов
  zugferd (напечатан на странице — проверено Apple Vision OCR; не только 8 из ревью); имена продавца pt__20210324_200034
  (JOAQUIM ANTÃO TRAVANCA CAPUCHO), pt__20210507_214450 (GAR RIBAMAR F. CUNHA COSTA); метка «NIF-IVA» в id_label (+ тест).
- pt__20210323_162221 seller_vat_id <NIF> → <NIF>. При приёмке: ревьюер ошибся в подсчёте (не «3 из 4 за 394»,
  а 2 модели за 394, 3 за 294); матричная цифра 3/2 размыта (OCR читает 794). Решает контрольная цифра NIF: верна только 394.
  Документ помечен quality=low (как nl-narrow-014). Цена: 3 строки TP→WV (gemma4-12b, qwen3.5-9b, qwen3vl-8b).
- Пересчёт r1 → reports/rescore_r1_v3 (compare.md). L1/L2 185/506. 86 тестов зелёные; скрипт идемпотентен.
- final v5: sha256 (answers.json, LC_ALL=C sort, cat) = cfac4f69e3322783866cd8399a887ed36e021476a7fb6c9ca6f91075d658706b

### 2026-11-13 — Qwen3.8 27B → стресс-трек E
- Владелец спросил про Qwen3.8 27B (VLM, авг. 2026; у владельца работает на другом Mac через ollama). Прогон на другой машине
  не отвечает на вопрос исследования (Mac mini 16 ГБ), поэтому — только трек E на Mac mini (00-plan.md, группа E).
- Оценка до замера: 3 бит ≈ 12,5–13,5 ГБ с картинкой — на грани, нужен поднятый лимит GPU; 2 бит ≈ 9–9,5 ГБ — помещается.
- Порядок: после r1b и раунда 2, чтобы не сдвигать основной прогон.

### 2026-11-13 — smoke P1b и запуск r1b
- Smoke P1b (те же 33 документа, что smoke P1v2), сравнение с r1 на тех же документах тем же скорером:
  qwen3vl-4b точность 95,2 → 94,8 %, выдумано 11/19 → 11/19 (правило про subtotal игнорирует);
  gemma4-12b точность 96,8 → 96,8 %, выдумано 4/19 → 0/19. JSON 100 %, остатков рассуждений и обрезаний нет; скорость прежняя.
  Различия отдельных строк (±4) — шум выборки. fatura Template12 сам противоречив (SUB_TOTAL 826,86 + TAX 26,72 ≠ TOTAL 828,69).
- Панель: «прерван» у r1 был ложным (2 исключённых документа считались недоделанными) — исправлено в harness/dashboard.py/.html.
- Запущен r1b: protocol/round1b.json, `caffeinate -i uv run python -m harness.study protocol/round1b.json`, лог runs/study_round1b.log. ~44 ч.

### 2026-11-15 — r1b завершён; этап 3.3: gt_check на r1b и ревью
- r1b закончен 2026-11-15 14:32 (`study done`): 6 моделей × 1572 документа × P1b, все прогоны полные.
- Выдуманные значения r1b: почти все — subtotal = итог чека (FF subtotal 460–514 у пяти моделей, у gemma4-12b 10).
  Совпадения: 105 полей, где ≥5 моделей дали одно число, — все subtotal, 104 из них = total. Правило P1b
  «Do not copy the total into the subtotal» соблюдает только gemma4-12b. Ловушка — «SUMME» / «TOTAL» без строки subtotal.
- Скорер: правило `pay_class` (решение владельца 2026-11-15: перевод засчитывается) — payment_method: наличные
  CONTANTI = BAR = ESPECES = CASH, бесконтактные KONTAKTLOS = SANS CONTACT = CONTACTLESS, диакритика свёрнута; бренды карт
  не сливаются, «CASSA 1» и опечатки — неверно. SERIES: код типа документа перед серией с буквы («FR B19/43» = «B19/43»,
  решение 2026-11-13 (3)). harness/gt_check.py: `--n-docs` (r1b — 1572), r1b-вердикты в CARRY_DEFAULT. 87 тестов зелёные.
- Пересчёт r1b → reports/rescore_r1b (runs/ не тронут): WV→TP payment_method 137, invoice_number 4; больше ничего.
- gt_check → reports/gt_check_r1b_v2: L1/L2 35/627 (r1 v3: 185/506; падение L1 — gemma4-12b теперь права в subtotal).
  Очередь новых без контролей: 251 → 97 после пересчёта.
- Ревью (reports/gt_check/r1b/verdicts.jsonl, 522 вердикта, поле method):
  - правило, 448: subtotal при GT null → model_failure (генератор synrec subtotal не печатает; реальные чеки — копия TOTAL);
    выборка страниц 10/10 подтвердила: synrec 614c, 012p, 906c, 250c; cord 021, 022, 025, 064; wild 0140, 0298;
  - просмотр страницы, 9: model_failure 8 (cord 021/022/025 subtotal; edb es-000 buyer_vat_id — IBAN продавца;
    edb fr-002 seller_name «Kraipreatraind» верно; korie IMG00241 2481 верно; zugferd Rechnungskorrektur issue_date
    16.09.2013 = Beleg-Datum; fatura Template39 __mask issue_date — маска чистая, скопирован Due Date);
    scorer_too_strict 1 (pt__20210321_120107 invoice_number, исправлено в SERIES);
  - согласие моделей, страница не открывалась, 65: ok (поля документов, поставленных в очередь целиком).
  Ошибок GT не найдено, правок final/ нет — final v5 без изменений. Непросмотренных подозрительных пар: 0 из 662.
- Дальше: 3.4 — отчёт P1 vs P1b (r1 пересчитать текущим скорером), рейтинг, финалисты; payment_method — отдельной
  строкой, не в общем рейтинге (обсуждалось с владельцем).

### 2026-11-15 — этап 3.4: P1 vs P1b, рейтинг, финалисты (предложение)
- r1 пересчитан текущим скорером → reports/rescore_r1_v4; ключи r1 и r1b совпадают (14470 на модель).
- harness/prompt_compare.py (+ tests/test_prompt_compare.py, 90 тестов зелёные) → reports/r1_vs_r1b/compare.md и csv.
  Основная оценка — все поля, кроме payment_method (отдельная колонка). P1 — не «второй хороший промпт», а промпт
  без определений полей (проблема 14); сравнение показывает эффект определений.
- Парное сравнение P1 → P1b (лучше / хуже, знаковый тест): gemma4-12b +175 (p<0,0001), qwen3vl-8b +66, qwen3.5-4b +60
  (p<0,0001), qwen3.5-9b +23 (p=0,056), qwen3vl-4b +15 (p=0,29), gemma4-e4b −239 (p<0,0001).
- gemma4-e4b с P1b перестраховывается: null при напечатанном значении (FN merchant_tax_id 71, seller_iban 76,
  total_tax 34; точность merchant_tax_id 96 → 77 %, seller_iban 82 → 70 %). Правило «не напечатано → null» маленькая
  модель применяет слишком широко.
- Выдумано (FF/(FF+TN)) P1 → P1b: gemma4-12b 13,1 → 1,3 %; у остальных 40–57 % почти целиком subtotal; без subtotal
  qwen3.5-9b 10,4 → 5,1, qwen3vl-8b 8,5 → 6,7, qwen3.5-4b 23,1 → 17,0, qwen3vl-4b 26,1 → 24,9, gemma4-e4b 2,2 → 2,2.
- Рейтинг P1b по F1 (JSON валиден 100 % у всех): qwen3.5-9b 96,1; gemma4-12b 95,9; qwen3vl-8b 95,8; qwen3.5-4b 95,5;
  qwen3vl-4b 93,7; gemma4-e4b 90,5. Правило отбора — пример из 00-plan.md 8.1 (топ-3 по F1, JSON ≥ 90 %), заранее
  не зарегистрировано. По нему финалисты: qwen3.5-9b, gemma4-12b, qwen3vl-8b — ~~ждёт утверждения владельца~~
  **утверждено владельцем 2026-11-15** (protocol/preregistration.md, раздел 1; отметка внесена 2026-11-18).

### 2026-11-15…18 — раунд 2: preregistration, smoke, основной прогон (запись внесена 2026-11-18)
- ☑ Утверждено владельцем: финалисты qwen3.5-9b, gemma4-12b, qwen3vl-8b (2026-11-15); правила раунда 2 —
  protocol/preregistration.md (записаны 2026-11-15 до первого прогона); выборка protocol/samples/round2.txt
  (400 документов, sha256 33a41f7b…, проверено 2026-11-18).
- Smoke (protocol/round2_smoke.json, 33 документа): 14 из 15 конфигураций прошли. gemma4-12b q8 — OOM Metal на всех
  33 документах (веса 12,1 ГБ ≈ предел GPU), первый запуск 2026-11-15 — паника ядра; исключён поправкой 2026-11-16.
- Основной прогон protocol/round2.json: 14 прогонов × 400 документов, 2026-11-16 → 2026-11-18 03:41 (`study done`),
  все полные. Анализ — следующая запись.

### 2026-11-18 — этап 4: анализ раунда 2 (предложение)
- Пересчёт r2 текущим скорером → reports/rescore_r2: 0 изменённых строк из 14 × 3510 против runs/ (прогоны уже
  оценены текущим скорером). final v5 — хэш cfac4f69… совпадает. runs/ не тронут.
- harness/round2_compare.py (+ tests/test_round2_compare.py; 95 тестов зелёные) → reports/round2/compare.md, models.csv,
  tests.csv, best.csv. Правила — preregistration.md разделы 4–5: каждый режим против r1b той же модели на тех же 400
  документах, знаковый тест, Холм по 14 сравнениям; выдумки — отдельным тестом (своё семейство Холма).
- Вердикты (F1 основных полей база → режим; лучше/хуже ключей; p по Холму):
  - q6/q8 — единственное, что помогает: gemma4-12b q6 96,0 → 98,1 (+105/−28, p<0,0001); qwen3.5-9b q6 96,1 → 96,9
    (p=0,010), q8 → 97,0 (p=0,002); qwen3vl-8b q8 95,9 → 96,6 (p=0,008); qwen3vl-8b q6 96,5 — без разницы (p=0,058).
  - P0b, constrained — без разницы у всех трёх. P2b — без разницы у Qwen, хуже у gemma4-12b (−28, p=0,020) и в
    1,6–1,9 раза медленнее.
  - Выдумки: ни одного значимого изменения. Subtotal чеков у Qwen ~44 % остаётся во всех режимах — не лечится ни
    промптом, ни схемой, ни битностью.
- Цена: пик памяти q6 +2,2–3,0 ГБ, q8 +4,0–4,4 ГБ; секунд на документ +10–27 %. Своп за прогон ≤ 1 ГБ (порог 2 ГБ).
  gemma4-12b q6 — пик 12,58 ГБ. iogpu.wired_limit_mb = 0 (по умолчанию) с перезагрузки 2026-11-15 20:39 (паника ядра)
  — весь основной прогон r2 шёл без поднятого лимита, ошибок памяти 0; поднятый лимит не нужен.
- Лучшая конфигурация по правилу раздела 5: **gemma4-12b q6** (F1 98,1; выдумано 2,8 %; 32 с/док; доля документов
  без единой ошибки 86 % против 63 % у следующей). Следующие: qwen3.5-9b q8 97,0; qwen3.5-9b q6 96,9.
- Оговорка (описательно, не по preregistration): выигрыш gemma q6 почти целиком на сгенерированных документах
  (F1 96,4 → 98,9; в основном seller_iban eurodocbench, +27 ключей); на реальных 93 документах 93,6 → 93,2. На реальных
  лучше всех qwen3.5-9b q8 (89,5 → 93,1). Выборка реальных мала — это и проверит полный прогон.
- GT-проверка r2 (gt_check рассчитан на 6 моделей, на 14 конфигурациях не запускается — упрощённый вариант): ключей,
  где ошиблись все 17 конфигураций (14 + 3 базы), — 7, все с прежними вердиктами; большинство ошиблось — 143, из них
  без вердикта 3 → проверены по странице (reports/gt_check_r2/verdicts.jsonl): все model_failure (cord 070 __mask
  subtotal 1,343,000 прочитан как 1343.00; eurodoc pt-007 «Torosetrerk» верно; fatura T18 __mask — текст логотипа
  «SIMPDEHY» не имя, как Template10 «HGH»). Ошибок GT нет, final v5 без изменений.
- Дальше по preregistration (раздел 5, п. 4): gemma4-12b q6 и qwen3.5-4b q6 на всём final/ (оценка ~15 ч + ~6–7 ч;
  веса qwen3.5-4b 6 бит скачать и прогнать smoke). Не запущено — ждёт решения владельца. Также открыто: трек Qwen3.8 27B
  и экстракторы (NuExtract3, lift).

### 2026-11-18 — итоговый прогон: проверка, smoke 4B q6, запуск
- Проверено перед запуском: iogpu.wired_limit_mb = 0 (по умолчанию с перезагрузки 2026-11-15 20:39) — как во всём r2;
  sudo не нужен. Поправка в preregistration.md от 2026-11-18.
- Очередь protocol/round_final.json, `caffeinate -i uv run python -m harness.study protocol/round_final.json`,
  лог runs/study_round_final.log, старт 07:36.
- Smoke s3__qwen3.5-4b__q6 (mlx-community/Qwen3.5-4B-6bit @ fbb1092a, 33 документа): JSON 100 %, ошибок 0, обрезаний 0,
  остатков рассуждений 0; против r1b 4 бит на тех же документах F1 95,3 → 96,3 (+3/−0), выдумано 57,9 → 52,6 %;
  13,7 с/док (4 бит 12,6), пик 6,15 ГБ, своп +0. Критерии раздела 6 выполнены — smoke принят, hold снят.
- Идёт f__gemma4-12b__q6 (1572 док., ~15 ч), затем f__qwen3.5-4b__q6 (~6–7 ч).
