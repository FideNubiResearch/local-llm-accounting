"""GT arithmetic check (harness/gt_arith.py, closeout stage 2.2)."""
import json
from collections import Counter
from decimal import Decimal as D

from harness import gt_arith as A


def doc(doc_type, doc_id="d", **fields):
    return {"doc_id": doc_id, "doc_type": doc_type,
            "fields": {k: (v if isinstance(v, dict) else {"answer": v, "printed": v}) for k, v in fields.items()}}


def checks(rows):
    return {(r["check"], r["status"], r["explanation"]) for r in rows}


def test_tolerance_and_currency():
    assert A.tolerance("EUR") == D("0.01") and A.tolerance("IDR") == A.tolerance("krw") == A.tolerance("JPY") == 1
    assert A.doc_currency("cord_v2", {}) == "IDR" and A.doc_currency("korie", {}) == "KRW"
    assert A.doc_currency("x", {"currency": {"answer": "EUR"}}) == "EUR" and A.doc_currency("x", {}) == ""


def test_invoice_sum_ok_within_tolerance():
    assert A.check_doc(doc("invoice", total_net="100.00", total_tax="19.00", total_gross="119.01"), "s", "") == []
    rows = A.check_doc(doc("invoice", total_net="100.00", total_tax="19.00", total_gross="119.50"), "s", "p")
    assert checks(rows) == {("inv_sum", "unexplained", "")}
    r = rows[0]
    assert r["diff"] == "-0.50" and r["fields"] == "total_net;total_tax;total_gross" and r["page_paths"] == "p"
    assert r["severity"] == "low"


def test_zero_decimal_currency_one_unit():
    d = doc("receipt", subtotal="26818", tax_amount="2681", total="29500")
    assert A.check_doc(d, "cord_v2", "") == []            # IDR: diff -1 is within one unit
    assert A.check_doc(d, "wildreceipt", "")[0]["check"] == "rcpt_sum"  # no currency: 0.01


def test_check_needs_all_fields():
    assert A.check_doc(doc("invoice", total_net="100", total_tax=None, total_gross="90"), "s", "")[0]["check"] == \
        "inv_net_le_gross"
    assert A.check_doc(doc("receipt", subtotal=None, tax_amount="1", total="10"), "s", "") == []


def test_receipt_order_checks_and_negatives():
    rows = A.check_doc(doc("receipt", subtotal="95.50", total="90.00"), "s", "")
    assert checks(rows) == {("rcpt_subtotal_le_total", "unexplained", "")} and rows[0]["severity"] == "high"
    # a refund: everything negative, absolute values compared
    assert A.check_doc(doc("receipt", subtotal="-2.87", tax_amount="-0.26", total="-3.13"), "s", "") == []
    rows = A.check_doc(doc("receipt", tax_amount="0", total="0"), "s", "")
    assert checks(rows) == {("rcpt_tax_lt_total", "unexplained", "")}   # tax == total: never "rounding"


def test_dates():
    assert A.check_doc(doc("invoice", issue_date="2020-01-10", due_date="2020-01-10"), "s", "") == []
    rows = A.check_doc(doc("invoice", issue_date="2014-01-24", due_date="2013-12-06"), "s", "")
    assert rows[0]["check"] == "due_ge_issue" and rows[0]["diff"] == "49d" and rows[0]["severity"] == "med"
    # an ambiguous dd/mm reading that satisfies the rule is no violation
    assert A.check_doc(doc("invoice", issue_date="05/03/2020", due_date="04/04/2020"), "s", "") == []
    rows = A.check_doc(doc("bank_statement", period_start="2025-04-30", period_end="2025-04-01"), "s", "")
    assert rows[0]["check"] == "period_order"


def test_explanations():
    # accepted alternative
    d = doc("invoice", issue_date="2019-11-13",
            due_date={"answer": "2017-12-13", "printed": "x", "accepted": ["2020-04-04"]})
    assert checks(A.check_doc(d, "zugferd_corpus", "")) == {("due_ge_issue", "explained", "accepted_alternative")}
    # FATURA generator
    d = doc("invoice", total_net="502.83", total_tax="23.4", total_gross="505.92")
    assert checks(A.check_doc(d, "fatura", "")) == {("inv_sum", "explained", "fatura_generator")}
    # rounding
    d = doc("receipt", subtotal="10.00", tax_amount="1.00", total="11.03")
    assert checks(A.check_doc(d, "s", "")) == {("rcpt_sum", "explained", "rounding")}
    d = doc("receipt", subtotal="68180", tax_amount="6818", total="75000")
    assert checks(A.check_doc(d, "cord_v2", "")) == {("rcpt_sum", "explained", "rounding")}
    # tax-inclusive subtotal
    d = doc("receipt", subtotal="17.90", tax_amount="1.62", total="17.90")
    assert checks(A.check_doc(d, "s", "")) == {("rcpt_sum", "explained", "tax_inclusive")}


def test_extra_line_from_page_text():
    d = doc("receipt", subtotal="238000", tax_amount="25585", total="281435")
    assert checks(A.check_doc(d, "cord_v2", "", None)) == {("rcpt_sum", "unexplained", "")}
    lines = ["SUBTOTAL", "Service", "PB1", "TOTAL", "238,000", "17,850", "25,585", "281,435"]
    rows = A.check_doc(d, "cord_v2", "", lines)
    assert checks(rows) == {("rcpt_sum", "explained", "extra_line")} and "17,850" in rows[0]["evidence"]
    # a bare small integer (quantity, VAT rate) does not explain a difference
    d = doc("invoice", total_net="260061.20", total_tax="52010.24", total_gross="312061.44")
    assert checks(A.check_doc(d, "s", "", ["Qty", "10", "VAT (20%)"])) == {("inv_sum", "unexplained", "")}
    assert checks(A.check_doc(d, "s", "", ["Discount -10.00"])) == {("inv_sum", "explained", "extra_line")}


def test_printed_numbers():
    nums = A.printed_numbers(["Qty 3 12", "1.764,97", "5.51", "2024"])
    vals = {v for v, _ in nums}
    assert D("1764.97") in vals and D("5.51") in vals and D("2024") in vals and D(3) not in vals and D(12) not in vals


def test_summary_counts():
    rows = [{"source": "a", "check": "inv_sum", "status": "explained"},
            {"source": "a", "check": "inv_sum", "status": "unexplained"},
            {"source": "b", "check": "inv_sum", "status": "unexplained"}]
    s = A.summary(rows, Counter({("a", "inv_sum"): 10, ("b", "inv_sum"): 5, ("b", "rcpt_sum"): 2}))
    by = {(r["source"], r["check"]): r for r in s}
    assert by[("a", "inv_sum")]["n_explained"] == 1 and by[("a", "inv_sum")]["n_unexplained"] == 1
    assert by[("ALL", "inv_sum")] == {"source": "ALL", "check": "inv_sum", "n_checked": 15, "n_violations": 3,
                                      "n_explained": 1, "n_unexplained": 2}
    assert by[("b", "rcpt_sum")]["n_violations"] == 0


def test_run_on_tree(tmp_path):
    final = tmp_path / "final"
    for d, src in (("i1", "s"), ("r1", "s")):
        (final / "docs" / d).mkdir(parents=True)
    (final / "manifest.csv").write_text("doc_id,source\ni1,s\nr1,s\n")
    (final / "docs" / "i1" / "answers.json").write_text(json.dumps(
        {**doc("invoice", "i1", total_net="10", total_tax="2", total_gross="13"), "pages": ["page_1.png"]}))
    (final / "docs" / "r1" / "answers.json").write_text(json.dumps(
        {**doc("receipt", "r1", subtotal="10", tax_amount="2", total="12"), "pages": ["page_1.png"]}))
    out = tmp_path / "out" / "arith.csv"
    rows = A.run(out, use_ocr=False, final=final)
    assert [(r["doc_id"], r["check"]) for r in rows] == [("i1", "inv_sum")]
    assert out.read_text().splitlines()[0] == ",".join(A.COLUMNS)
    summ = (out.parent / "arith_summary.csv").read_text()
    assert "s,inv_sum,1,1,0,1" in summ and "s,rcpt_sum,1,0,0,0" in summ
