"""Round 1 must stay reproducible: P1 and the schemas that rendered it are frozen; P1b is the round-2 wording."""
import hashlib

from harness.run import PROMPTS, ROOT, prompt_text, schema_for

P1_SHA256 = "89e5cc9d47b671cd3e56765869b17925687c3315d88bc1f859219706c89fb50d"
SCHEMAS_SHA256 = "297c403c4e08cddda0a3b5e3712d32152df52253ee96d961fefe6d2376e6a2b3"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_round1_prompt_frozen():
    assert sha(PROMPTS / "P1_null.txt") == P1_SHA256
    assert sha(ROOT / "protocol" / "schemas.json") == SCHEMAS_SHA256


def test_p1b_renders_with_new_rules():
    for dt in ("invoice", "receipt", "bank_statement"):
        schema = schema_for(dt, "P1b")
        assert schema == schema_for(dt, "P1")
        p1, p1b = prompt_text(dt, "P1", schema), prompt_text(dt, "P1b", schema)
        assert p1 != p1b and "{" not in p1b.split("Rules:")[1]
    t = prompt_text("receipt", "P1b", schema_for("receipt", "P1b"))
    for phrase in ("not the cash tendered", "not a prior balance", "otherwise null", "without the address",
                   "Never copy one into the other", "totals of this invoice only", "outstanding balances",
                   "a service charge is not tax", "PB1 are tax",
                   "invoice-level tax total printed in the totals block", "a per-line tax column is not the invoice tax total"):
        assert phrase in t, phrase


def test_round2_prompts_p0b_p2b():
    for dt in ("invoice", "receipt", "bank_statement"):
        s1b, s2b = schema_for(dt, "P1b"), schema_for(dt, "P2b")
        assert schema_for(dt, "P0b") == s1b
        assert set(s2b["properties"]) == set(s1b["properties"])
        assert all(p["required"] == ["value", "quote"] for p in s2b["properties"].values())
        p0b, p1b, p2b = (prompt_text(dt, p, schema_for(dt, p)) for p in ("P0b", "P1b", "P2b"))
        # P0b = P1b without the general null rule; field definitions kept
        assert "Never guess" not in p0b and "Never guess" in p1b
        assert [l for l in p1b.splitlines() if "set it to null" not in l] == p0b.splitlines()
        # P2b = P1b rules + quote for every value
        for phrase in ("not the cash tendered", "Do not copy the total into the subtotal", "totals of this invoice only",
                       '{"value": null, "quote": null}', "exact text from the document"):
            assert phrase in p2b, phrase
