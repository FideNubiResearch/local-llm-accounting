"""Extractors (NuExtract3 4B q6, lift 9B q6) against the best VLM configurations on the same 400 documents.

  uv run python -m harness.ext_compare [--out reports/extractors]

Protocol: protocol/preregistration.md, amendment 2026-11-19. Descriptive: paired exact sign tests per pair with Holm over
the pairs shown here (a separate "extractors" family, not part of round 2). Metrics as harness/prompt_compare.py.
Read-only over its inputs; writes only --out.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from harness.final_compare import by_group, pct, read, table
from harness.prompt_compare import RIGHT, SEPARATE, side_row, sign_test
from harness.round2_compare import holm

ROOT = Path(__file__).resolve().parents[1]
EXT = ["NuExtract3 4B q6", "lift 9B q6 (схема)"]


def keys_paired(a: pd.DataFrame, b: pd.DataFrame, only_null: bool) -> dict:
    k = ["doc_id", "field"]
    a = a[~a["field"].isin(SEPARATE)].set_index(k)["outcome"]
    b = b[~b["field"].isin(SEPARATE)].set_index(k)["outcome"]
    if set(a.index) != set(b.index):
        raise SystemExit(f"keys differ: {len(set(a.index) ^ set(b.index))}")
    b = b.reindex(a.index)
    if only_null:
        m = a.isin(["TN", "FF"]) & b.isin(["TN", "FF"])
        a, b = a[m], b[m]
    ra, rb = a.isin(RIGHT), b.isin(RIGHT)
    better, worse = int((~ra & rb).sum()), int((ra & ~rb).sum())
    return {"keys": len(a), "better": better, "worse": worse, "net": better - worse, "p": sign_test(better, worse)}


def inv_no_sub(df: pd.DataFrame) -> float:
    d = df[~df["field"].isin(SEPARATE) & ~((df["doc_type"] == "receipt") & (df["field"] == "subtotal"))]
    n = d["outcome"].isin(["TN", "FF"]).sum()
    return float((d["outcome"] == "FF").sum() / n) if n else float("nan")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/extractors")
    a = ap.parse_args(argv)
    r2, fin, ext = ROOT / "reports/rescore_r2", ROOT / "reports/rescore_final", ROOT / "reports/rescore_ext"
    sample = set(l.strip() for l in (ROOT / "protocol/samples/round2.txt").read_text().splitlines() if l.strip())
    q4 = read(fin / "f__qwen3.5-4b__q6/fields.csv")
    cfg = {
        "gemma4-12b q6": read(r2 / "r2__gemma4-12b__q6/fields.csv"),
        "qwen3.5-9b q6": read(r2 / "r2__qwen3.5-9b__q6/fields.csv"),
        "qwen3.5-4b q6": q4[q4["doc_id"].isin(sample)],
        EXT[0]: read(ext / "r2__nuextract3-4b__q6/fields.csv"),
        EXT[1]: read(ext / "r2__lift-9b__q6c/fields.csv"),
    }
    for k, v in cfg.items():
        assert v["doc_id"].nunique() == len(sample), (k, v["doc_id"].nunique())
    L = ["# Экстракторы против VLM на тех же 400 документах", "",
         "Метрики как в harness/prompt_compare.py (основные поля без payment_method). Парные тесты описательные: "
         "отдельное семейство «экстракторы», поправка Холма по парам этой страницы; не часть семейства раунда 2.", ""]
    rows = []
    for name, df in cfg.items():
        r = side_row(df)
        rows.append({"cfg": name, "f1": pct(r["f1"]), "acc": pct(r["value_acc"]), "inv": pct(r["invented"]),
                     "inv2": pct(inv_no_sub(df)), "docs_ok": pct(r["docs_ok"]), "json": pct(r["json_valid"]),
                     "sec": f"{r['sec_median']:.1f}", "hours": f"{r['hours']:.1f}", "peak": f"{r['peak_gb']:.1f}"})
    L += ["## 1. Общая таблица", "", table(rows, [("Конфигурация", "cfg"), ("F1, %", "f1"), ("Верных значений, %", "acc"),
          ("Выдумано, %", "inv"), ("Выдумано без subtotal чеков, %", "inv2"), ("Док. без ошибок, %", "docs_ok"),
          ("JSON, %", "json"), ("с/док (медиана)", "sec"), ("Часов на 400", "hours"), ("Пик, ГБ", "peak")]), ""]
    for title, only_null in (("2. Парное сравнение по всем основным ключам", False),
                             ("3. Парное сравнение только по ключам с ответом null (выдумки)", True)):
        pr = []
        for e in EXT:
            for ref in ("gemma4-12b q6", "qwen3.5-4b q6"):
                pr.append({"cmp": f"{e} против {ref}", **keys_paired(cfg[ref], cfg[e], only_null)})
        for r, h in zip(pr, holm([r["p"] for r in pr])):
            r["p"], r["ph"] = f"{r['p']:.3g}", f"{h:.3g}"
        L += [f"## {title}", "", "«Лучше» = неверно у конфигурации справа от «против» и верно у экстрактора слева.", "",
              table(pr, [("Сравнение", "cmp"), ("Ключей", "keys"), ("Лучше", "better"), ("Хуже", "worse"),
                         ("Итого", "net"), ("p", "p"), ("p по Холму", "ph")]), ""]
    L += ["## 4. Реальные и сгенерированные документы", ""]
    for name, df in cfg.items():
        L += [f"**{name}**", "", table(by_group(df, ["kind"]), [("Тип", "kind"), ("Док.", "docs"), ("Значений", "values"),
              ("Верных, %", "acc"), ("95 % интервал", "ci"), ("F1, %", "f1"), ("Выдумано, %", "inv")]), ""]
    L += ["## 5. По типу документа", ""]
    for name, df in cfg.items():
        L += [f"**{name}**", "", table(by_group(df, ["doc_type"]), [("Тип", "doc_type"), ("Док.", "docs"),
              ("Значений", "values"), ("Верных, %", "acc"), ("F1, %", "f1"), ("Выдумано, %", "inv")]), ""]
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "compare.md").write_text("\n".join(L))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
