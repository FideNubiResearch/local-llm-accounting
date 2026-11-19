from decimal import Decimal
from datetime import date

from harness import normalize as N
from harness.score import outcome, parse_json, score_doc, score_rows


# ---------- amounts ----------
def test_amount_formats():
    cases = {
        "1.234,56": "1234.56", "1,234.56": "1234.56", "1 234,56": "1234.56", "1'234.56": "1234.56",
        "€ 12,50": "12.50", "12.50 EUR": "12.50", "1,234": "1234", "0,5": "0.5", "12,5": "12.5",
        "(15.00)": "-15.00", "15.00-": "-15.00", "−3,20": "-3.20", "￥1,200": "1200",
        "1.234.567": "1234567", "100": "100",
    }
    for raw, exp in cases.items():
        assert N.amount(raw) == Decimal(exp), raw


def test_amount_ambiguous_thousands():
    # IDR receipts: "45.000" = 45000; EN: "45.000" = 45
    assert N.equal("total", "45000", "Rp 45.000")
    assert N.equal("total", "45", "45.000")
    assert N.equal("total", "1234", "1,234")
    assert not N.equal("total", "45000", "46.000")


def test_amount_equal_tolerance():
    assert N.equal("total", "12.50", "12,5")
    assert not N.equal("total", "12.50", "12.51")


# ---------- dates ----------
def test_dates():
    assert N.dates("2024-03-05") == {date(2024, 3, 5)}
    assert N.dates("05.03.2024") == {date(2024, 3, 5), date(2024, 5, 3)}
    assert N.dates("2024年3月5日") == {date(2024, 3, 5)}
    assert N.dates("2024년 3월 5일") == {date(2024, 3, 5)}
    assert date(2024, 3, 5) in N.dates("5. März 2024")
    assert date(2024, 3, 5) in N.dates("March 5, 2024")
    assert N.dates("20240305") == {date(2024, 3, 5)}


def test_date_equal():
    assert N.equal("issue_date", "2024-03-05", "05.03.2024")
    assert N.equal("issue_date", "2024-03-05", "2024-03-05")
    assert not N.equal("issue_date", "2024-03-05", "2024-03-06")


# ---------- ids / text / currency ----------
def test_ident():
    assert N.equal("seller_iban", "DE89 3704 0044 0532 0130 00", "DE89370400440532013000")
    assert N.equal("invoice_number", "INV-2024/001", "inv 2024 001")
    assert not N.equal("invoice_number", "INV-001", "INV-002")


def test_currency():
    assert N.equal("currency", "EUR", "€")
    assert N.equal("currency", "JPY", "円")


def test_null_strings():
    for v in [None, "", "null", "N/A", "none", " - "]:
        assert N.is_null(v), v


# ---------- outcomes ----------
def test_outcomes():
    assert outcome("total", "10.00", "10").outcome == "TP"
    assert outcome("total", "10.00", "11").outcome == "WV"
    assert outcome("total", "10.00", None).outcome == "FN"
    assert outcome("total", None, None).outcome == "TN"
    assert outcome("total", None, "10").outcome == "FF"


def test_missing_key_is_null():
    ds = score_doc({"total": None, "date": "2024-01-02"}, {"date": "2024-01-02"})
    assert [r.outcome for r in ds.fields] == ["TN", "TP"]


def test_p2_unwrap():
    ds = score_doc({"total": "5.00"}, {"total": {"value": "5", "quote": "Total 5,00"}})
    assert ds.fields[0].outcome == "TP"


# ---------- rows ----------
def test_rows_order_invariant():
    gt = [{"name": "apple", "price": "1.00"}, {"name": "pear", "price": "2.00"}]
    pr = [{"name": "pear", "price": "2"}, {"name": "apple", "price": "1"}]
    r = score_rows(gt, pr)
    assert r["tp"] == 4 and r["fp"] == 0 and r["fn"] == 0


def test_rows_extra_and_missing():
    gt = [{"name": "apple", "price": "1.00"}, {"name": "pear", "price": "2.00"}]
    pr = [{"name": "apple", "price": "1"}, {"name": "kiwi", "price": "9"}, {"name": "fig", "price": "3"}]
    r = score_rows(gt, pr)
    assert r["tp"] == 2 and r["fn"] == 2 and r["fp"] >= 4


# ---------- json parsing ----------
def test_parse_json():
    assert parse_json('{"a": 1}') == ({"a": 1}, True)
    assert parse_json('```json\n{"a": 1}\n```')[0] == {"a": 1}
    assert parse_json('Sure! {"a": 1} hope it helps')[0] == {"a": 1}
    assert parse_json('<think>hmm</think>{"a": 2}')[0] == {"a": 2}
    assert parse_json("no json here") == (None, False)


def test_text_space_insensitive():
    assert N.equal("merchant_name", "KOREANRESTAURANT", "Korean Restaurant")
    assert not N.equal("merchant_name", "Korean Restaurant", "Thai Restaurant")


def test_rows_skip_cells_not_printed():
    from harness.score import score_rows
    gt = [{"description": "A", "unit_price": "3951.50", "line_total": "7903.00"}]
    pred = [{"description": "A", "unit_price": "4741.80", "line_total": "7903.00"}]
    r = score_rows(gt, pred, skip=[[0, "unit_price"]])
    assert (r["tp"], r["fp"], r["fn"]) == (2, 0, 0)
    r = score_rows(gt, [], skip=[[0, "unit_price"]])
    assert r["fn"] == 2


def test_text_form_leaders_and_checkboxes():
    from harness import normalize as N
    assert N.text("75 ... Rue ..... Coll ...") == N.text("75 Rue Coll")
    assert N.equal("seller_name", "☑开业", "开业")


# ---------- canonical ground truth (final/answers.json) ----------
def test_amount_gt_strict_pred_ambiguous():
    assert N.equal("total", "47000", "47.000")      # model copied KRW grouping: accepted
    assert N.equal("total", "47", "47.000")         # or decimals: accepted
    assert not N.equal("total", "47000", "47")
    assert N.equal("total", "1.234", "1.234")       # canonical with 3 decimals is not read as thousands
    assert not N.equal("total", "1.234", "1234")
    assert N.equal("total_gross", "46834.91", "46 834,91 zł")
    assert N.equal("total", "139.94", 139.94)


def test_date_gt_strict_pred_ambiguous():
    assert N.equal("issue_date", "2026-04-05", "05/04/2026")
    assert N.equal("issue_date", "2026-05-04", "05/04/2026")
    assert not N.equal("issue_date", "2026-04-05", "2026-05-04", N.LEGACY)   # round-1 scorer
    assert not N.equal("issue_date", "2026-04-13", "2026-05-04")
    assert N.equal("issue_date", "2025-12-24", "24 grudnia 2025")


def test_id_label_copied_by_model():
    assert N.equal("seller_vat_id", "DE123456789", "USt-IdNr.: DE123456789")
    assert N.equal("seller_vat_id", "FR50155357030", "N° TVA intracommunautaire: FR 501 553 570 30")
    assert N.equal("seller_iban", "PL52809656401905589817333265", "PL52 8096 5640 1905 5898 1733 3265")
    assert not N.equal("seller_vat_id", "DE123456789", "DE123456780")


def test_is_canonical():
    assert N.is_canonical("total", "47000") and N.is_canonical("total", 12.5)
    assert not N.is_canonical("total", "47.000,00") and not N.is_canonical("total", "€ 5")
    assert N.is_canonical("date", "2026-04-05") and not N.is_canonical("date", "05/04/2026")
    assert N.is_canonical("seller_name", "anything")


def test_score_answers():
    from harness.score import score_answers
    ans = {"fields": {"total": {"answer": "10.5", "printed": "10,50"}, "subtotal": {"answer": None, "printed": None}}}
    ds = score_answers(ans, {"total": "10,50", "subtotal": "10.50", "extra": "x"})
    assert [(r.field, r.outcome, r.canonical) for r in ds.fields] == [("total", "TP", False), ("subtotal", "FF", True)]
    assert not score_answers(ans, None).json_valid


def test_date_pred_formats_seen_in_documents():
    for gt, pred in [("2004-07-31", "31-Jul-2004"), ("2026-08-16", "16 de agosto de 2026"), ("2025-11-08", "2025. 11. 08"),
                     ("2025-11-20", "25-11-20"), ("2018-04-29", "29-APR-2018"), ("2024-03-05", "5. März 2024")]:
        assert N.equal("date", gt, pred), (gt, pred)


# ---------- rules after the round-1 GT review (owner decisions 2026-11-13) ----------
def test_rule_date_swap():
    assert N.equal("date", "2024-04-07", "2024-07-04")                 # day and month <= 12: swap accepted
    assert N.equal("date", "2024-04-07", "07/04/2024")
    assert not N.equal("date", "2024-04-07", "2024-07-04", N.LEGACY)
    assert not N.equal("date", "2024-04-13", "2024-13-04")             # day > 12: no swap
    assert not N.equal("date", "2024-04-07", "2024-07-05")             # a wrong day stays wrong
    assert not N.equal("date", "2024-04-07", "2023-07-04")


def test_rule_amount_sign_ignored():
    assert N.equal("total_tax", "-1.12", "1.12")
    assert N.equal("total", "12.50", "(12,50)")
    assert N.equal("total_gross", "8.79", "-8.79")
    assert not N.equal("total_tax", "-1.12", "1.12", N.LEGACY)
    assert not N.equal("total_tax", "-1.12", "1.13")                   # digits still matter
    assert not N.equal("total", "377859", "377059")


def test_rule_name_diacritics_and_spaces():
    assert N.equal("seller_name", "auto taxis hebepe, unipessoal lda", "AUTO TÁXIS HEBEPE, Unipessoal Lda.")
    assert N.equal("seller_name", "rogerio pais, lda", "ROGÉRIO PAIS, LDA")
    assert N.equal("seller_name", "MVM Musterhafter\nVersicherungsverein", "MVM  Musterhafter Versicherungsverein")
    assert N.equal("merchant_name", "Mcdonald'sHazeldonk-west", "McDonald's Hazeldonk-West")
    assert not N.equal("seller_name", "rogerio pais, lda", "ROGÉRIO PAIS, LDA", N.LEGACY)
    assert not N.equal("seller_name", "elencojasmim lda", "ELENCOJASMIN LDA")   # a different letter stays wrong


def test_rule_name_legal_forms_and_honorifics():
    for gt, pred in [("Au bon moulin", "Au bon moulin SARL"), ("MUSTER-Autovermietung", "MUSTER-Autovermietung GmbH"),
                     ("Pingo Doce", "Pingo Doce, S. A."), ("Matond Consulenza", "Matond Consulenza S.p.A."),
                     ("Toroteark", "Toroteark Sp. z o.o."), ("Riostatorox", "Riostatorox S.r.l."),
                     ("OLIVE9 PHARMACY", "OLIVE9 PHARMACY SDN BHD"), ("Acme", "Acme B.V."), ("Acme", "Acme AG"),
                     ("Acme", "Acme KG"), ("Kaipi", "Kaipi Lda."),
                     ("(주)아성다이소_청주산남2호점", "아성다이소 청주산남2호점"), ("㈜아성다이소", "아성다이소")]:
        assert N.equal("seller_name", gt, pred), (gt, pred)
    assert N.equal("buyer_name", "Herrn\nMax Mustermann", "Max Mustermann")
    assert N.equal("buyer_name", "Max Mustermann", "Frau Max Mustermann")
    assert not N.equal("seller_name", "Au bon moulin", "Au bon moulin SARL", N.LEGACY)
    assert not N.equal("seller_name", "GmbH", "AG")                    # never stripped down to nothing
    # name rules are for names only
    assert not N.equal("payment_method", "Herr Card", "Card")


def test_rule_pay_class():
    for gt, pred in [("CONTANTI", "CASH"), ("BAR", "cash"), ("ESPECES", "CASH"), ("ESPECES", "ESPÈCES"),
                     ("CASH", "Contanti"), ("KONTAKTLOS", "Contactless"), ("SANS CONTACT", "contactless"),
                     ("CARTA CONTACTLESS", "CONTACTLESS"), ("CARTA CONTACTLESS", "CARD CONTACTLESS")]:
        assert N.equal("payment_method", gt, pred), (gt, pred)
        assert not N.equal("payment_method", gt, pred, N.LEGACY) or N.text(gt) == N.text(pred)
    for gt, pred in [("CONTANTI", "CASSA 1"), ("SANS CONTACT", "CASH"), ("BAR", "RUECKGELD"),
                     ("KONTAKTLOS", "KONTAKTLLOS"), ("VISA", "MASTERCARD"), ("MASTERCARD", "CARD"),
                     ("CARTA CONTACTLESS", "CARD"), ("BAR", "CARD")]:
        assert not N.equal("payment_method", gt, pred), (gt, pred)
    assert not N.equal("merchant_name", "BAR", "CASH")                    # pay_class is for payment_method only


def test_rule_name_containment():
    edb = "Mareleriork Doradztwo S.A., al. Peastund 164, 39-586 Poznań"
    assert N.equal("seller_name", "Mareleriork Doradztwo S.A.", edb)    # name + address
    assert N.equal("seller_name", "pingo doce", "Pingo Doce - Distribuição Alimentar, S.A.")
    assert N.equal("merchant_name", "JAWEDHABIB", "JAWED HABIB HAIR & BEAUTY")   # GT written without spaces
    assert not N.equal("seller_name", "Mareleriork Doradztwo S.A.", edb, N.LEGACY)
    assert not N.equal("seller_name", "Mareleriork Doradztwo S.A.", "Mareleriori Doradztwo S.A., al. Peastund 164")
    assert not N.equal("merchant_name", "Mart", "Martin GmbH")          # substring of a token is not a token
    assert not N.equal("merchant_name", "PaneraBread Cafe0994", "Panera Bread")  # only GT inside pred, not reverse
    assert not N.equal("seller_name", "h&m", "H M Logistics")          # too short for containment
    assert not N.equal("buyer_name", "Max Mustermann", "Mustermann")


def test_rule_ids():
    assert N.equal("seller_vat_id", "502607920", "PT502607920")         # country code
    assert N.equal("seller_vat_id", "PT506431134", "506431134")
    assert N.equal("seller_vat_id", "500766681", "500766681/CRC43043-Porto")
    assert N.equal("seller_vat_id", "501419926", "NIF/CRC:501419926")
    assert N.equal("seller_vat_id", "506175502", "NIPC 506175502")
    assert N.equal("invoice_number", "NO.0090302021030000 / 002569", "0090302021030000/002569")   # label in GT
    assert N.equal("invoice_number", "25805", "Nº 25805")
    assert not N.equal("seller_vat_id", "502607920", "PT502607920", N.LEGACY)
    assert not N.equal("seller_vat_id", "500829993", "PT500829983")     # one digit wrong
    assert not N.equal("seller_vat_id", "FR11999999998", "FR119999999998")
    assert not N.equal("seller_iban", "DE02120300000000202051", "02120300000000202051")   # cc rule: tax ids only



def test_rule_invoice_series_prefix():
    for gt, pred in [("1971/1575", "FTS 1971/1575"), ("FT 030101732516200003/00005", "030101732516200003/00005"),
                     ("NFS 2019A12/1930227", "2019A12/1930227"), ("FTR 6/9443", "6/9443"),
                     ("C2 / 1318851", "1318851"), ("FR 12 / 345", "12/345"), ("1318851", "C2/1318851"),
                     ("FR B19/43", "B19/43")]:
        assert N.equal("invoice_number", gt, pred), (gt, pred)
        assert not N.equal("invoice_number", gt, pred, N.LEGACY - {"id_series"} | {"id_label", "id_crc"}), (gt, pred)
    assert not N.equal("invoice_number", "FTS 1971/1575", "1971/1576")      # digits must match exactly
    assert not N.equal("invoice_number", "FT 0300003/00005", "FT 030003/00005")
    assert not N.equal("invoice_number", "C2 / 1318851", "C3 / 1318851")     # different series digit
    assert not N.equal("invoice_number", "1318851", "21318851")
    assert not N.equal("seller_vat_id", "1971/1575", "FTS 1971/1575")      # invoice numbers only


def test_rules_can_be_switched_off_one_by_one():
    cases = {"date_swap": ("date", "2024-04-07", "2024-07-04"), "amount_abs": ("total", "-5", "5"),
             "name_fold": ("seller_name", "rogerio", "ROGÉRIO"), "name_legal": ("seller_name", "Au bon", "Au bon SARL"),
             "name_honorific": ("buyer_name", "Max Muster", "Herrn Max Muster"),
             "name_contain": ("seller_name", "Kaipi Lda.", "Kaipi Lda., Rua Puvux 98"),
             "id_label": ("invoice_number", "25805", "Nº 25805"), "id_crc": ("seller_vat_id", "5007", "5007/CRC43-Porto"),
             "id_cc": ("seller_vat_id", "502607920", "PT502607920"),
             "id_series": ("invoice_number", "1971/1575", "FTS 1971/1575"),
             "pay_class": ("payment_method", "CONTANTI", "CASH")}
    assert set(cases) == N.RULES
    for rule, (f, g, p) in cases.items():
        assert N.equal(f, g, p, frozenset({rule})), rule
        assert not N.equal(f, g, p, N.LEGACY), rule


def test_accepted_variants_and_accept_from():
    from harness.score import score_answers
    ans = {"fields": {
        "seller_name": {"answer": "jumbo", "printed": "jumbo", "accepted": ["AUCHAN RETAIL PORTUGAL, S.A."]},
        "seller_vat_id": {"answer": "DE123456789", "printed": "DE123456789", "accepted": ["201/113/40209"]},
        "total_gross": {"answer": "100.00", "printed": "100.00", "accept_from": ["total_net"]}}}
    ds = score_answers(ans, {"seller_name": "Auchan Retail Portugal SA", "seller_vat_id": "201/113/40209",
                             "total_net": "100", "total_gross": None})
    got = {r.field: (r.outcome, r.matched_by) for r in ds.fields}
    assert got == {"seller_name": ("TP", "accepted"), "seller_vat_id": ("TP", "accepted"),
                   "total_gross": ("TP", "from:total_net")}
    ds = score_answers(ans, {"seller_name": "Continente", "seller_vat_id": "201/113/40208", "total_net": "90",
                             "total_gross": "100"})
    got = {r.field: (r.outcome, r.matched_by) for r in ds.fields}
    assert got == {"seller_name": ("WV", ""), "seller_vat_id": ("WV", ""), "total_gross": ("TP", "")}
    ds = score_answers(ans, {"total_net": "90", "total_gross": "95"})
    assert [r.outcome for r in ds.fields] == ["FN", "FN", "WV"]
    # a field not listed in answers.json (excluded) is not scored even if the model fills it
    assert {r.field for r in score_answers(ans, {"total_tax": "5"}).fields} == set(ans["fields"])


def test_rule_id_label_needs_separator():
    assert N.equal("invoice_number", "25805", "N.º 25805") and N.equal("invoice_number", "25805", "No: 25805")
    assert not N.equal("seller_iban", "123456789", "NO123456789")         # "NO" + digits is not a "No." label


# ---------- format flag for names (owner decision 2026-11-13 (4), closeout 1.9a) ----------
def test_name_canonical_false_when_matched_only_by_containment():
    edb = "Mareleriork Doradztwo S.A., al. Peastund 164, 39-586 Poznań"
    r = outcome("seller_name", "Mareleriork Doradztwo S.A.", edb)
    assert (r.outcome, r.canonical) == ("TP", False)                       # value correct, format wrong
    for pred in ("ROSS DAZZ FOR LESS", "ROSS DRESS FOR LESS"):            # extra tokens after the GT name
        assert (outcome("merchant_name", "ROSS", pred).outcome, outcome("merchant_name", "ROSS", pred).canonical) \
            == ("TP", False)
    r = outcome("buyer_name", "MUSTER-KUNDE GMBH", "GLN 4304171000002 MUSTER-KUNDE")
    assert (r.outcome, r.canonical) == ("TP", False)
    r = outcome("merchant_name", "JAWEDHABIB", "JAWED HABIB HAIR & BEAUTY")
    assert (r.outcome, r.canonical) == ("TP", False)


def test_name_canonical_true_for_clean_matches():
    cases = [("COMPTOIR ARIBELLA", "Comptoir Aribella"),                  # case
             ("Estação Serviço da Cegonha Lda", "ESTACAO SERVICO DA CEGONHA LDA"),   # diacritics
             ("MUSTER-KUNDE GMBH", "MUSTER-KUNDE"),                        # legal form dropped
             ("Max Mustermann", "Herrn Max Mustermann"),                   # honorific
             ("JAWEDHABIB", "JAWED HABIB"),                                # spacing only
             ("Liotoreal Techniek B.V.", "Lioto real Techniek B.V.")]
    for gt, pred in cases:
        r = outcome("seller_name", gt, pred)
        assert (r.outcome, r.canonical) == ("TP", True), (gt, pred)
    # a clean match against an `accepted` variant is canonical too
    r = outcome("seller_name", "galp", "GASNUNOS", accepted=["GASNUNOS"])
    assert (r.outcome, r.matched_by, r.canonical) == ("TP", "accepted", True)
    r = outcome("seller_name", "galp", "GASNUNOS, Rua X 1", accepted=["GASNUNOS"])
    assert (r.outcome, r.canonical) == ("TP", False)


def test_name_canonical_does_not_change_outcomes_or_other_fields():
    assert outcome("seller_name", "Max Mustermann", "Mustermann").outcome == "WV"
    assert outcome("seller_name", "Max Mustermann", "Mustermann").canonical is True   # WV: format not judged
    assert outcome("seller_name", None, "Some Name GmbH, Street 1").canonical is True  # FF: format not judged
    assert outcome("invoice_number", "R18-31", "Nr. R18-31 extra").canonical is True   # ids: unchanged
    assert outcome("total", "10.5", "10,50").canonical is False                      # amounts: unchanged


def test_id_label_nif_iva():
    """Stage 2: 'NIF-IVA' label (es) is stripped like NIF; digits must still match."""
    from harness import normalize as N
    assert N.equal("seller_vat_id", "ESA50742107", "NIF-IVA ES A50 742 107")
    assert N.equal("seller_vat_id", "ESA50742107", "NIF IVA: ESA50742107")
    assert not N.equal("seller_vat_id", "ESA50742107", "NIF-IVA ES A50 742 108")
