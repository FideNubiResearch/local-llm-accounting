"""Stage-2 review queue (harness/gt_stage2.py)."""
import pandas as pd

from harness import gt_stage2 as Q

MODELS = Q.MODELS


def test_allocate_largest_remainder_and_minimum():
    assert Q.allocate({"null": 15, "value": 74}, 5) == {"null": 1, "value": 4}
    assert Q.allocate({"a": 1, "b": 100}, 10, 5) == {"a": 1, "b": 9}
    assert sum(Q.allocate({"a": 7, "b": 13, "c": 2}, 22).values()) == 22
    t = Q.proportional_target({"a": 43, "b": 89, "c": 6377, "d": 3456}, 200, 5)
    assert t["a"] == t["b"] == 5 and sum(t.values()) == 200 and t["c"] > t["d"] > 5
    assert Q.proportional_target({"a": 3, "b": 1000}, 50, 5) == {"a": 3, "b": 47}


def test_pick_arith_field():
    assert Q.pick_arith_field(["total_net", "total_tax", "total_gross"], {"total_gross": 2}, set()) == "total_gross"
    assert Q.pick_arith_field(["total_net", "total_tax", "total_gross"], {}, set()) == "total_tax"
    assert Q.pick_arith_field(["issue_date", "due_date"], {}, {"due_date"}) == "issue_date"
    assert Q.pick_arith_field(["subtotal"], {}, {"subtotal"}) == ""


def _votes():
    rows = []

    def add(doc, field, source, gt, n_wrong, level="L0"):
        rows.append({"review_id": f"{doc}::{field}", "doc_id": doc, "field": field, "source": source,
                     "doc_type": "invoice", "gt": gt, "printed": gt, "consensus_example": "", "n_voting": "6",
                     "n_wrong": str(n_wrong), "n_wrong_raw": str(n_wrong), "level": level, "hint": "scattered",
                     "page_paths": f"/p/{doc}/page_1.png", **{f"pred_{m}": gt for m in MODELS}})

    for f, nw in (("total_net", 0), ("total_tax", 1), ("total_gross", 0)):
        add("ar", f, "src1", "1", nw)
    add("t1", "seller_name", "src1", "x", 3)
    add("t2", "seller_name", "src1", "x", 3)       # already reviewed -> skipped
    add("t3", "seller_name", "src1", "x", 4, "L2")
    for i in range(40):
        add(f"a{i}", "total_net", "src1" if i < 30 else "src2", "" if i % 10 == 0 else "5", 0)
    for i in range(6):
        add(f"c{i}", "total_tax", "src1", "9", 6, "L1")
    return pd.DataFrame(rows)


def test_build_streams_order_controls():
    votes = _votes()
    arith = pd.DataFrame([{"doc_id": "ar", "check": "inv_sum", "fields": "total_net;total_tax;total_gross",
                           "values": "total_net=1;total_tax=1;total_gross=1", "diff": "1", "status": "unexplained"},
                          {"doc_id": "a1", "check": "inv_sum", "fields": "total_net", "values": "", "diff": "",
                           "status": "explained"}])
    verdicts = {"t2::seller_name": {"verdict": "model_failure"}, "c0::total_tax": {"verdict": "model_failure"},
                "c1::total_tax": {"verdict": "ok", "correct_value": "9"},
                "c2::total_tax": {"verdict": "definition_ambiguity"},
                "t3::seller_name": {"verdict": "gt_wrong", "correct_value": "y"}}
    q, ctrl, info = Q.build(votes, arith, verdicts, {"total_net": "net"}, audit_n=12)
    assert list(q.columns) == Q.QUEUE_COLUMNS and q["review_id"].is_unique
    assert set(ctrl["review_id"]) == {"c0::total_tax", "c1::total_tax", "t3::seller_name"}
    assert set(ctrl["prior_verdict"]) == {"model_failure", "ok", "gt_wrong"}
    body = q[~q["review_id"].isin(ctrl["review_id"])]
    assert list(body["stream"]) == ["arith", "three_of_six"] + ["audit_agree"] * 12
    assert body.iloc[0]["review_id"] == "ar::total_tax" and body.iloc[0]["hint"].startswith("arith: inv_sum")
    assert "t2::seller_name" not in set(q["review_id"])       # reviewed 3/6 key skipped
    audit = body[body["stream"] == "audit_agree"]
    src = audit["review_id"].map(dict(zip(votes["review_id"], votes["source"])))
    assert (src == "src2").sum() == Q.AUDIT_MIN and (audit["gt"] == "").sum() >= 1
    # controls are not marked: they carry a stream of the body and the batch they landed in
    assert set(q.loc[q["review_id"].isin(ctrl["review_id"]), "stream"]) <= set(Q.STREAMS)
    assert (ctrl["batch"] == ctrl["review_id"].map(dict(zip(q["review_id"], q["batch"])))).all()
    assert info["three_of_six_total"] == 2 and info["three_of_six_reviewed"] == 1
    # deterministic
    q2, _, _ = Q.build(votes, arith, verdicts, {"total_net": "net"}, audit_n=12)
    assert q.equals(q2)
