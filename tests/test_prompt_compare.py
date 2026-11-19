import pandas as pd
import pytest

from harness import prompt_compare as P


def test_sign_test():
    assert P.sign_test(0, 0) == 1.0
    assert P.sign_test(5, 5) == 1.0
    assert P.sign_test(10, 0) == pytest.approx(2 / 1024)


def test_metrics_and_subtotal_split():
    g = pd.DataFrame({"outcome": ["TP", "TP", "WV", "FN", "TN", "FF", "FF"],
                      "doc_type": ["invoice"] * 5 + ["receipt", "receipt"],
                      "field": ["a", "b", "c", "d", "e", "subtotal", "tax_amount"]})
    m = P.metrics(g)
    assert m["value_acc"] == pytest.approx(2 / 4)
    assert m["precision"] == pytest.approx(2 / 5)
    assert m["invented"] == pytest.approx(2 / 3)
    assert m["invented_no_subtotal"] == pytest.approx(1 / 2)


def test_finalists_rule():
    rows = pd.DataFrame({"model": list("abcde"), "prompt": ["P1b"] * 5,
                         "f1": [0.95, 0.96, 0.9601, 0.94, 0.99], "invented": [0.1, 0.3, 0.2, 0.1, 0.0],
                         "json_valid": [1, 1, 1, 1, 0.5]})
    f = P.finalists(rows)
    # e has the best F1 but invalid JSON; b and c tie on F1 (3 decimals) -> c has fewer invented values
    assert f.loc[f["finalist"], "model"].tolist() == ["c", "b", "a"]
    assert not f.loc[f["model"] == "e", "finalist"].item()
