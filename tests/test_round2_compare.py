import pandas as pd
import pytest

from harness import round2_compare as R


def test_holm():
    adj = R.holm([0.01, 0.04, 0.03])
    assert adj == pytest.approx([0.03, 0.06, 0.06])
    assert R.holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])


def frame(outcomes, fields=None):
    n = len(outcomes)
    return pd.DataFrame({"doc_id": [f"d{i}" for i in range(n)], "field": fields or ["f"] * n,
                         "outcome": outcomes, "doc_type": ["invoice"] * n, "json_valid": ["True"] * n,
                         "wall_s": [1.0] * n, "peak_gb": [5.0] * n})


def test_paired_counts_and_separate_field():
    a = frame(["WV", "TP", "FF", "TN", "WV"], ["f", "f", "f", "f", "payment_method"])
    b = frame(["TP", "WV", "TN", "FF", "TP"], ["f", "f", "f", "f", "payment_method"])
    p = R.paired(a, b)
    # payment_method is not a main field; row 0 and 2 better, row 1 and 3 worse
    assert (p["better"], p["worse"], p["inv_fixed"], p["inv_new"]) == (2, 2, 1, 1)


def test_paired_rejects_different_keys():
    with pytest.raises(SystemExit):
        R.paired(frame(["TP"]), frame(["TP", "TP"]))


def test_verdicts_and_best():
    base = frame(["WV"] * 30 + ["TP"] * 70)
    good = frame(["TP"] * 100)
    bad = frame(["WV"] * 60 + ["TP"] * 40)
    res = R.compare({"m": base}, [("r__m__good", "m", "good", good), ("r__m__bad", "m", "bad", bad)])
    v = dict(zip(res["tests"]["mode"], res["tests"]["verdict"]))
    assert v == {"good": "better", "bad": "worse"}
    assert res["best"]["mode"].tolist() == ["good", "base"]
