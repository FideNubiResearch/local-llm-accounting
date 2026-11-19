"""Tests for harness/gt_check.py (reports/gt_check/PLAN.md section 7)."""
from collections import Counter
from pathlib import Path

import pandas as pd
import pytest

from harness import gt_check as G

ROOT = Path(__file__).resolve().parents[1]
MODELS = ["qwen3vl-4b", "qwen3vl-8b", "qwen3.5-4b", "qwen3.5-9b", "gemma4-e4b", "gemma4-12b"]


# ---------- levels ----------
def test_levels():
    assert G.level(6, 6) == "L1"
    assert G.level(5, 6) == "L2"
    assert G.level(4, 6) == "L2"
    assert G.level(3, 6) == "L0"
    assert G.level(0, 6) == "L0"


def test_level_with_abstention():
    assert G.level(5, 5) == "L1"          # one model abstains, the other five all wrong
    assert G.level(4, 5) == "L2"
    assert G.level(3, 5) == "L2"          # 0.6 > 0.5
    assert G.level(4, 4) == "L2"          # fewer than 5 voters cannot be L1
    assert G.level(0, 0) == "L0"


def test_only_wrong_outcomes_count():
    assert not G.is_wrong("TP") and not G.is_wrong("TN")
    assert all(G.is_wrong(o) for o in ("WV", "FN", "FF"))


def _wide(outcomes, preds, gt="10.00", field="total", canonical=None, abstain=None, masked=False):
    rec = {"doc_id": "d__clean", "field": field, "source": "s", "kind": "real", "lang": "en", "doc_type": "receipt",
           "variant": "clean", "template": "", "masked": "False", "gt": gt, "printed": gt,
           "field_masked": masked, "page_paths": "", "base_doc": ""}
    for i, m in enumerate(MODELS):
        rec[f"outcome_{m}"] = outcomes[i]
        rec[f"predraw_{m}"] = preds[i]
        rec[f"canonical_{m}"] = (canonical or ["True"] * 6)[i]
        rec[f"abstain_{m}"] = (abstain or [False] * 6)[i]
    return pd.DataFrame([rec])


def test_canonical_false_alone_not_wrong():
    w = _wide(["TP"] * 6, ['"10,00"'] * 6, canonical=["False"] * 6)
    r = G.analyze(w, MODELS).iloc[0]
    assert r["n_wrong"] == 0 and r["level"] == "L0" and r["hint"] == ""


def test_analyze_abstention_l1():
    outs = ["FN", "WV", "WV", "WV", "WV", "WV"]
    preds = ["", '"12.00"', '"12,00"', '"12"', '"12.0"', '"12.00"']
    w = _wide(outs, preds, abstain=[True, False, False, False, False, False])
    r = G.analyze(w, MODELS).iloc[0]
    assert (r["n_voting"], r["n_wrong"], r["n_wrong_raw"]) == (5, 5, 6)
    assert r["level"] == "L1" and r["level_raw"] == "L1"
    assert r["n_agree"] == 5 and r["pattern"] == "consensus_alt" and r["err_type"] == "WV"
    assert r["hint"] == "gt_value_suspect"


def test_analyze_tp_tn_never_wrong():
    w = _wide(["TN"] * 6, [""] * 6, gt="")
    r = G.analyze(w, MODELS).iloc[0]
    assert r["n_wrong"] == 0 and r["level"] == "L0" and r["err_type"] == ""


# ---------- err_type ----------
def test_err_type_ff_probe_vs_mask():
    assert G.err_type("", False, ["FF"]) == "FF_probe"
    assert G.err_type("", True, ["FF", "FF"]) == "FF_mask"
    assert G.err_type("5", False, ["WV", "FN"]) == "WV"
    assert G.err_type("5", False, ["FN", "FN", "WV"]) == "FN"
    assert G.err_type("5", False, []) == ""


# ---------- consensus ----------
def test_consensus_merge_amounts():
    cl = G.cluster_preds("total", [("a", "120,000"), ("b", "120000"), ("c", 120000.0)])
    assert len(cl) == 1 and len(cl[0]["models"]) == 3
    cl = G.cluster_preds("total", [("a", "7,27"), ("b", "7.27")])
    assert len(cl) == 1


def test_consensus_merge_dates():
    cl = G.cluster_preds("date", [("a", "2021-02-15"), ("b", "15/02/2021")])
    assert len(cl) == 1 and cl[0]["key"] == "2021-02-15"
    # ambiguous d/m vs m/d merges with its ISO reading
    cl = G.cluster_preds("date", [("a", "2026-04-05"), ("b", "05/04/2026")])
    assert len(cl) == 1


def test_consensus_nulls_own_cluster():
    cl = G.cluster_preds("total", [("a", None), ("b", "null"), ("c", "5.00")])
    keys = {c["key"]: len(c["models"]) for c in cl}
    assert keys == {G.NULL_KEY: 2, "5.00": 1}


def test_consensus_deterministic_ties():
    a = G.cluster_preds("total", [("a", "1.00"), ("b", "2.00")])
    b = G.cluster_preds("total", [("b", "2.00"), ("a", "1.00")])
    assert [c["key"] for c in a] == [c["key"] for c in b] == ["1.00", "2.00"]
    ex = G.cluster_example({"preds": ["1,00", "1.00"], "models": ["a", "b"], "key": "1.00"})
    assert ex == "1,00"


# ---------- signals ----------
def test_consensus_eq_field():
    gts = {"subtotal": "", "total": "25.50", "tax_amount": "2.10", "merchant_name": "25.50"}
    assert G.consensus_eq_field("subtotal", "25,50", gts) == "total"
    gts = {"seller_vat_id": "DE111", "buyer_vat_id": "DE222"}
    assert G.consensus_eq_field("seller_vat_id", "DE 222", gts) == "buyer_vat_id"
    assert G.consensus_eq_field("subtotal", None, {"total": "1"}) == ""


def test_gt_in_pred():
    assert G.substring_signals("seller_name", "pingo doce", "Pingo Doce Distribuição SA") == (True, False)
    assert G.substring_signals("buyer_name", "ACME GmbH Musterstr. 1", "ACME GmbH") == (False, True)
    assert G.substring_signals("total", "15", "150") == (False, False)


def test_id_prefix_only():
    assert G.id_prefix_only("510776914", "PT510776914")
    assert G.id_prefix_only("DE123456789", "123456789")
    assert not G.id_prefix_only("510776914", "510776914")
    assert not G.id_prefix_only("510776914", "PT510776915")


def test_digit_edit1():
    assert G.digit_edit1("total", "377859", "377059")
    assert G.digit_edit1("total", "377859", "377,059")
    assert not G.digit_edit1("tax_amount", "18126", "10260")
    assert G.digit_edit1("invoice_number", "INV1234", "INV1284")
    assert not G.digit_edit1("seller_name", "abc", "abd")


def test_hint_scorer_strict_and_sibling():
    w = _wide(["FF"] * 6, ['"25.50"'] * 6, gt="", field="subtotal")
    w["doc_id"] = "x"
    tot = w.copy()
    tot["field"] = "total"
    tot["gt"] = "25.50"
    for m in MODELS:
        tot[f"outcome_{m}"] = "TP"
    v = G.analyze(pd.concat([w, tot], ignore_index=True), MODELS).set_index("field")
    assert v.loc["subtotal", "hint"] == "sibling_copy" and v.loc["subtotal", "consensus_eq_field"] == "total"
    assert v.loc["subtotal", "err_type"] == "FF_probe"
    w = _wide(["WV"] * 6, ['"PT510776914"'] * 6, gt="510776914", field="buyer_vat_id")
    r = G.analyze(w, MODELS).iloc[0]
    assert r["id_prefix_only"] and r["hint"] == "scorer_strict"


# ---------- twins ----------
def test_twin_group():
    assert G.twin_group("synrec__eval-000001__clean") == G.twin_group("synrec__eval-000001__photo") \
        == "synrec__eval-000001"
    assert G.twin_group("bsi__classic_grid_00__digital") == G.twin_group("bsi__classic_grid_00__scan")
    assert G.twin_group("fatura__T28_I0__mask", "fatura__T28_I0") == G.twin_group("fatura__T28_I0") \
        == "fatura__T28_I0"
    assert G.twin_group("cord__014__mask") == "cord__014"
    assert G.twin_group("wild__0252") == "wild__0252"


# ---------- summary.md ----------
SUMMARY = """# r1__x__P1

```
{}
```

## All

| doc_type       |   docs |   values |   value_acc |   wrong |   missed |   nulls |   invented |
|:---------------|-------:|---------:|------------:|--------:|---------:|--------:|-----------:|
| invoice        |      1 |        3 |       0.333 |       1 |        1 |       2 |      0.5   |
| receipt        |      1 |        1 |       1     |       0 |        0 |       0 |    nan     |

## Language x type x real/generated

| lang | doc_type | docs |
|:-----|:---------|-----:|
| de   | invoice  |    1 |
"""


def test_parse_summary_all():
    t = G.parse_summary_all(SUMMARY)
    assert list(t["doc_type"]) == ["invoice", "receipt"]
    assert t.set_index("doc_type").loc["invoice", "wrong"] == "1"


def test_reconcile():
    df = pd.DataFrame({"doc_type": ["invoice"] * 5 + ["receipt"],
                       "outcome": ["TP", "WV", "FN", "TN", "FF", "TP"]})
    r = G.reconcile("r", df, SUMMARY)
    assert r["ok"].all()
    df.loc[0, "outcome"] = "WV"
    assert not G.reconcile("r", df, SUMMARY)["ok"].all()


def test_read_verdicts(tmp_path):
    p = tmp_path / "v.jsonl"
    p.write_text('{"review_id": "a::b", "verdict": "unsure"}\n\nnot json\n{"review_id": "a::b", "verdict": "gt_wrong"}\n')
    v, bad = G.read_verdicts(p)
    assert v["a::b"]["verdict"] == "gt_wrong" and bad == 1
    assert G.read_verdicts(tmp_path / "missing.jsonl") == ({}, 0)


# ---------- integration over the real round-1 runs (read-only) ----------
RUNS_PRESENT = all((ROOT / "runs" / f"r1__{m}__P1" / "fields.csv").exists() for m in MODELS)


@pytest.fixture(scope="module")
def real():
    data = G.load(ROOT)
    return data, G.analyze(data["wide"], data["models"])


@pytest.mark.skipif(not RUNS_PRESENT, reason="round-1 runs not present")
def test_integration_counts(real):
    data, v = real
    assert len(v) == 14561 and v["review_id"].is_unique
    assert data["recon"]["ok"].all()
    hist = Counter(v["n_wrong_raw"])
    assert {k: hist[k] for k in range(7)} == {0: 11252, 1: 1552, 2: 581, 3: 293, 4: 179, 5: 459, 6: 245}
    expected = {
        "gemma4-12b": (12544, 552, 178, 1117, 170), "gemma4-e4b": (11922, 737, 615, 746, 541),
        "qwen3.5-4b": (12631, 590, 53, 558, 729), "qwen3.5-9b": (12846, 403, 25, 647, 640),
        "qwen3vl-4b": (12460, 781, 33, 540, 747), "qwen3vl-8b": (12615, 613, 46, 666, 621),
    }
    for m, exp in expected.items():
        c = v[f"outcome_{m}"].value_counts()
        assert tuple(int(c.get(o, 0)) for o in ("TP", "WV", "FN", "TN", "FF")) == exp, m
    raw = v["level_raw"].value_counts()
    assert (raw["L1"], raw["L2"]) == (245, 638)
    l1 = v[v["level_raw"] == "L1"]
    assert ((l1["gt"] != "").sum(), (l1["gt"] == "").sum()) == (88, 157)


@pytest.mark.skipif(not RUNS_PRESENT, reason="round-1 runs not present")
def test_integration_abstaining_docs(real):
    data, v = real
    abst = {(d, m) for m in data["models"]
            for d in data["frames"][m].loc[data["frames"][m]["json_valid"].eq("False"), "doc_id"]}
    assert {d for d, _ in abst} == {"wild__0252", "wild__0049", "wild__0081", "synrec__eval-000253__clean"}
    assert {m for _, m in abst} == {"qwen3.5-4b"}
    assert (v["n_voting"] == 5).sum() == 20 and v["n_voting"].min() == 5


@pytest.mark.skipif(not RUNS_PRESENT, reason="round-1 runs not present")
def test_integration_suspects_consistent(real):
    _, v = real
    s = v[v["level"].isin(["L1", "L2"])]
    assert s["pattern"].isin(G.PATTERNS).all() and s["hint"].isin(G.HINTS).all()
    assert (v.loc[v["n_wrong"] == 0, "hint"] == "").all()


# ---------- end-to-end on a synthetic tree (tmp_path) ----------
def _make_tree(root: Path) -> None:
    import json
    import shutil

    from harness.score import outcome

    (root / "protocol").mkdir(parents=True)
    shutil.copy(ROOT / "protocol" / "fields.yaml", root / "protocol" / "fields.yaml")
    runs = [{"run_id": f"r1__{m}__P1", "model": m, "revision": "x"} for m in MODELS]
    (root / "protocol" / "round1.json").write_text(json.dumps({"runs": runs}))
    docs = {  # doc -> (variant, base_doc, {field: (gt, masked)})
        "s__a__clean": ("clean", "", {"total": ("10.00", False), "subtotal": ("", False), "merchant_name": ("Shop", False)}),
        "s__a__photo": ("photo", "", {"total": ("10.00", False), "subtotal": ("", False), "merchant_name": ("Shop", False)}),
        "s__b": ("digital", "", {"total": ("7.00", False), "tax_amount": ("1.00", False), "merchant_name": ("Mart", False)}),
        "s__b__mask": ("digital+masked", "s__b", {"total": ("", True), "tax_amount": ("1.00", False), "merchant_name": ("Mart", False)}),
    }
    preds = {  # (doc, field) -> 6 predictions (None = null)
        ("s__a__clean", "total"): ["12.00"] * 6,
        ("s__a__clean", "subtotal"): ["10,00"] * 5 + [None],
        ("s__a__photo", "total"): ["10.00"] * 6,
        ("s__a__photo", "subtotal"): [None] * 6,
        ("s__b__mask", "total"): ["7.00"] * 5 + [None],
        # GT is a substring but not a token of the prediction: still wrong after the name-containment rule
        ("s__b", "merchant_name"): ["Martin GmbH"] * 4 + ["Mart", "Mart"],
    }
    man = ["doc_id,source,base_doc"]
    rows = {m: [] for m in MODELS}
    for doc, (variant, base, fields) in docs.items():
        man.append(f"{doc},src,{base}")
        d = root / "final" / "docs" / doc
        d.mkdir(parents=True)
        (d / "page_1.png").write_bytes(b"")
        ans = {"doc_id": doc, "pages": ["page_1.png"], "fields": {}}
        for f, (gt, masked) in sorted(fields.items()):
            ans["fields"][f] = {"answer": gt or None, "printed": gt or None, **({"masked": True} if masked else {})}
            ps = preds.get((doc, f), [gt or None] * 6)
            for m, p in zip(MODELS, ps):
                o = outcome(f, gt or None, p)
                rows[m].append({"doc_id": doc, "source": "src", "kind": "real", "lang": "de", "doc_type": "receipt",
                                "variant": variant, "template": "", "masked": str(bool(base)), "field": f,
                                "outcome": o.outcome, "canonical": "" if o.canonical is None else str(o.canonical),
                                "gt": gt, "pred": "" if p is None else json.dumps(p), "json_valid": "True",
                                "strict_json": "True", "wall_s": "1", "peak_gb": "1", "error": ""})
        (d / "answers.json").write_text(json.dumps(ans))
    (root / "final" / "manifest.csv").write_text("\n".join(man) + "\n")
    for m in MODELS:
        rd = root / "runs" / f"r1__{m}__P1"
        rd.mkdir(parents=True)
        (rd / "config.json").write_text(json.dumps({"run_id": rd.name, "n_selected": 4, "revision": "x"}))
        df = pd.DataFrame(rows[m])
        df.to_csv(rd / "fields.csv", index=False)
        c = Counter(df["outcome"])
        (rd / "summary.md").write_text(
            "# x\n\n## All\n\n| doc_type | docs | values | wrong | missed | nulls |\n|:--|--:|--:|--:|--:|--:|\n"
            f"| receipt | 4 | {c['TP'] + c['WV'] + c['FN']} | {c['WV']} | {c['FN']} | {c['TN'] + c['FF']} |\n")


def _snapshot(root: Path) -> dict:
    return {str(p): p.read_bytes() for d in ("runs", "final") for p in (root / d).rglob("*") if p.is_file()}


def test_run_end_to_end(tmp_path):
    import json

    root = tmp_path / "proj"
    _make_tree(root)
    before = _snapshot(root)
    out = root / "reports" / "gt_check"
    kw = {"n_runs": 6, "n_docs": 4, "n_rows": 12}
    assert G.run(root, root / "protocol" / "round1.json", out, **kw) == 0
    for name in ("votes.csv", "suspects.csv", "by_field.csv", "by_source_field.csv", "by_source.csv", "by_lang.csv",
                 "by_doc_type.csv", "by_variant.csv", "by_kind.csv", "by_template.csv", "by_lang_field_edb.csv",
                 "docs.csv", "clusters.csv", "report.md", "review/queue.csv", "review/verdicts.jsonl"):
        assert (out / name).exists(), name
    v = pd.read_csv(out / "votes.csv", dtype=str, keep_default_na=False).set_index("review_id")
    assert len(v) == 12
    assert v.loc["s__a__clean::total", "level"] == "L1"
    assert v.loc["s__a__clean::total", "hint"] == "gt_value_suspect"
    assert v.loc["s__a__clean::subtotal", "hint"] == "sibling_copy"
    assert v.loc["s__a__clean::subtotal", "twin_levels"] == "s__a__photo:L0"
    assert v.loc["s__b__mask::total", "err_type"] == "FF_mask" and v.loc["s__b__mask::total", "hint"] == "mask_leak"
    assert v.loc["s__b__mask::total", "twin_group"] == "s__b"
    assert v.loc["s__b::merchant_name", "hint"] == "scorer_strict"
    q = pd.read_csv(out / "review/queue.csv", dtype=str, keep_default_na=False)
    assert q["review_id"].is_unique and "s__a__clean::total" in set(q["review_id"])
    assert (out / "review/verdicts.jsonl").read_text() == ""
    report = (out / "report.md").read_text()
    assert "## Sanity checks" in report and "False" not in report.split("## Sanity checks")[1]
    first = {p.name: p.read_bytes() for p in out.rglob("*.csv")}

    # re-run is deterministic and picks up verdicts
    (out / "review/verdicts.jsonl").write_text(json.dumps(
        {"review_id": "s__a__clean::total", "doc_id": "s__a__clean", "field": "total", "verdict": "gt_wrong",
         "correct_value": "12.00", "confidence": "high"}) + "\n")
    assert G.run(root, root / "protocol" / "round1.json", out, **kw) == 0
    s = pd.read_csv(out / "suspects.csv", dtype=str, keep_default_na=False).set_index("review_id")
    assert s.loc["s__a__clean::total", "verdict"] == "gt_wrong"
    fx = pd.read_csv(out / "review/proposed_fixes.csv", dtype=str, keep_default_na=False)
    assert list(fx["proposed_answer"]) == ["12.00"]
    assert "Verdict by cluster" in (out / "report.md").read_text()
    second = {p.name: p.read_bytes() for p in out.rglob("*.csv")}
    for name in ("votes.csv", "docs.csv", "clusters.csv"):
        assert first[name] == second[name], name
    q2 = pd.read_csv(out / "review/queue.csv", dtype=str, keep_default_na=False)
    assert q2.drop(columns="prior_verdict").equals(q.drop(columns="prior_verdict"))   # only the mark changed
    assert dict(zip(q2["review_id"], q2["prior_verdict"]))["s__a__clean::total"] == "gt_wrong"
    assert _snapshot(root) == before            # runs/ and final/ untouched


def test_report_out_dir_leaves_run_untouched(tmp_path):
    import json

    from harness import report

    run = tmp_path / "run"
    run.mkdir()
    (run / "config.json").write_text(json.dumps({"run_id": "t"}))
    (run / "predictions.jsonl").write_text(json.dumps(
        {"doc_id": "cord__009", "parsed": {"subtotal": "36.000", "total": "36000", "tax_amount": None},
         "strict_json": True, "wall_s": 1, "peak_gb": 1, "error": None}) + "\n")
    before = sorted(p.name for p in run.iterdir())
    out = tmp_path / "out"
    report.main(str(run), str(out))
    assert sorted(p.name for p in run.iterdir()) == before
    df = pd.read_csv(out / "fields.csv")
    assert (out / "summary.md").exists() and set(df["outcome"]) <= {"TP", "TN"}


def test_applied_fixes_tolerated(tmp_path):
    (tmp_path / "reports" / "gt_check").mkdir(parents=True)
    (tmp_path / "reports" / "gt_check" / "applied_fixes.csv").write_text(
        "doc_id,field,action,old,new,review_id,reason\nd,total,fix,,36000,,x\nd,total_net,exclude,,,,y\n"
        "d,seller_name,accepted,a,b,,z\n")
    fixes, excl = G.applied_fixes(tmp_path)
    assert fixes == {("d", "total"): ("", "36000")} and excl == {("d", "total_net")}
    assert G.applied_fixes(tmp_path / "none") == ({}, set())


# ---------- closeout 1.7: verdict "ok", verdicts carried over between checks ----------
def test_ok_is_a_verdict():
    assert "ok" in G.VERDICTS and "ok" not in G.FIX_VERDICTS


def test_merge_verdicts_carries_by_review_id(tmp_path):
    import json

    old = tmp_path / "old.jsonl"
    own = tmp_path / "own.jsonl"
    old.write_text("\n".join(json.dumps(r) for r in [
        {"review_id": "a::total", "verdict": "model_failure"}, {"review_id": "b::date", "verdict": "ok"},
        {"review_id": "c::x", "verdict": "unsure"}]) + "\n")
    own.write_text(json.dumps({"review_id": "c::x", "verdict": "gt_wrong"}) + "\nbroken\n")
    v, bad = G.merge_verdicts([old], own)
    assert {k: r["verdict"] for k, r in v.items()} == {"a::total": "model_failure", "b::date": "ok", "c::x": "gt_wrong"}
    assert v["a::total"]["_source"] == str(old) and v["c::x"]["_source"] == str(own) and bad == 1
    # the own file listed as a carried file too is read once; missing files are skipped
    assert G.merge_verdicts([own, tmp_path / "missing.jsonl"], own)[0].keys() == {"c::x"}


def test_run_marks_carried_verdicts(tmp_path):
    import json

    root = tmp_path / "proj"
    _make_tree(root)
    kw = {"n_runs": 6, "n_docs": 4, "n_rows": 12}
    earlier = root / "reports" / "gt_check" / "review" / "verdicts.jsonl"
    earlier.parent.mkdir(parents=True)
    earlier.write_text(json.dumps({"review_id": "s__a__clean::total", "verdict": "ok", "reviewer": "x"}) + "\n")
    out = root / "reports" / "gt_check_new"
    assert G.run(root, root / "protocol" / "round1.json", out, carry_verdicts=[earlier], **kw) == 0
    s = pd.read_csv(out / "suspects.csv", dtype=str, keep_default_na=False).set_index("review_id")
    assert (s.loc["s__a__clean::total", "verdict"], s.loc["s__a__clean::total", "verdict_source"]) == ("ok", "carried")
    assert (s.drop(index="s__a__clean::total")["verdict"] == "").all()
    q = pd.read_csv(out / "review/queue.csv", dtype=str, keep_default_na=False).set_index("review_id")
    assert q.loc["s__a__clean::total", "prior_verdict"] == "ok"
    assert (out / "review/verdicts.jsonl").read_text() == ""          # carried verdicts are not copied
    assert "verdict carried over" in (out / "report.md").read_text()
    # a verdict of the new check overrides the carried one
    (out / "review/verdicts.jsonl").write_text(
        json.dumps({"review_id": "s__a__clean::total", "verdict": "gt_wrong", "correct_value": "12.00"}) + "\n")
    assert G.run(root, root / "protocol" / "round1.json", out, carry_verdicts=[earlier], **kw) == 0
    s = pd.read_csv(out / "suspects.csv", dtype=str, keep_default_na=False).set_index("review_id")
    assert (s.loc["s__a__clean::total", "verdict"], s.loc["s__a__clean::total", "verdict_source"]) == \
        ("gt_wrong", "own")


def test_excluded_document_tolerated(tmp_path):
    import shutil

    root = tmp_path / "proj"
    _make_tree(root)
    (root / "reports" / "gt_check").mkdir(parents=True)
    (root / "reports" / "gt_check" / "applied_fixes.csv").write_text(
        "doc_id,field,action,old,new,review_id,reason\ns__b,*,exclude_doc,,,,stock mock-up\n")
    shutil.rmtree(root / "final" / "docs" / "s__b")
    assert G.applied_fixes(root)[1] == {("s__b", "*")}
    data = G.load(root, n_runs=6, n_docs=4, n_rows=12)      # the round-1 fields.csv still hold s__b rows
    assert data["gt_edits_tolerated"] == 3


# ---------- closeout stage 2: several carried verdict files (round-1 review + stage-2 review) ----------
def test_carry_default_includes_stage2():
    assert G.CARRY_DEFAULT == ("reports/gt_check/review/verdicts.jsonl", "reports/gt_check/stage2/verdicts.jsonl",
                               "reports/gt_check/r1b/verdicts.jsonl")


def test_merge_verdicts_several_carried_files(tmp_path):
    import json

    r1, s2, own = tmp_path / "r1.jsonl", tmp_path / "s2.jsonl", tmp_path / "own.jsonl"
    r1.write_text(json.dumps({"review_id": "a::total", "verdict": "model_failure"}) + "\n"
                  + json.dumps({"review_id": "b::date", "verdict": "unsure"}) + "\n")
    s2.write_text(json.dumps({"review_id": "b::date", "verdict": "gt_wrong", "correct_value": "2020-01-01"}) + "\n"
                  + json.dumps({"review_id": "c::tax", "verdict": "ok"}) + "\n")
    v, bad = G.merge_verdicts([r1, s2], own)
    assert {k: r["verdict"] for k, r in v.items()} == {"a::total": "model_failure", "b::date": "gt_wrong",
                                                        "c::tax": "ok"}
    assert v["b::date"]["_source"] == str(s2) and bad == 0


def test_main_accepts_several_carry_files(tmp_path, monkeypatch):
    seen = {}
    monkeypatch.setattr(G, "run", lambda root, proto, out, carry_verdicts=None, **kw: seen.update(c=carry_verdicts)
                        or 0)
    assert G.main(["--carry-verdicts", "x/a.jsonl", str(tmp_path / "b.jsonl")]) == 0
    assert seen["c"] == [G.ROOT / "x/a.jsonl", tmp_path / "b.jsonl"]
    assert G.main([]) == 0
    assert seen["c"] == [G.ROOT / p for p in G.CARRY_DEFAULT]
