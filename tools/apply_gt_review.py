"""Apply the owner-approved results of the round-1 GT review to final/ (journal 2026-11-13, decisions (1) and (2)).

  uv run python tools/apply_gt_review.py [--dry-run]

1. GT fixes from reports/gt_check/review/proposed_fixes.csv (each checked against the page before it was listed here).
2. `accepted` variants (seller_name / merchant_name: any identifiable seller name; seller_vat_id: any tax id of the
   seller). Every value is traced to a verdict in reports/gt_check/review/verdicts.jsonl (correct_value, blind_read,
   evidence, or model predictions the reviewer confirmed). A variant the scorer already accepts against the answer
   (normalize.equal with all rules) is not stored, except where the owner asked for it explicitly.
3. Invoice totals (total_gross / total_net / total_tax): an unmasked null answer is removed from answers.json and
   listed in final/excluded.csv (the existing exclusion mechanism); when exactly one of total_gross / total_net is
   printed, that field gets `accept_from: [<the other one>]`. Masked fields stay (absence probes).
Also updates n_values / n_null in final/manifest.csv. Writes reports/gt_check/applied_fixes.csv.

Stage 1 of 05-closeout-plan.md (journal 2026-11-13, decisions (3) and (4)); rows have stage=1 in applied_fixes.csv:
4. whole documents excluded (wild__0426, wild__0428: stock mock-ups): listed in final/excluded.csv with field "*",
   removed from final/manifest.csv and final/docs/ (they stay in git history);
5. mask probes whose painted amount can still be derived from printed numbers (or whose rounded / pre-rounding
   amount stays visible): the masked field is removed from the __mask document's answers.json and listed in
   final/excluded.csv. Candidates: tools/mask_probe_scan.py; each one verified on the page image (MASK_PROBES);
6. GT fixes (Physiotherapeut seller_name -> the person's name) and `accepted` variants for pages that print two
   values; an `accepted` value the scorer already accepts against the (new) answer is dropped as redundant;
7. doc-level `quality: "low"` in answers.json and a `quality` column in final/manifest.csv (still scored; reports
   give accuracy with and without these documents).
Idempotent: a second run changes nothing.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import normalize as N  # noqa: E402

FINAL = ROOT / "final"
OUT = ROOT / "reports" / "gt_check" / "applied_fixes.csv"
VERDICTS = ROOT / "reports" / "gt_check" / "review" / "verdicts.jsonl"

ZUG = "zugferd__ZUGFeRD"
RK = ZUG + "v2_correct_intarsys_BASIC_zugferd_2p0_BASIC_Rechnungskorrektur.pdf"
HAFT = ZUG + "v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Haftpflichtversicherung_Versicherungssteuer.pdf"
KONIK = ZUG + "v1_correct_Konik_acme_invoice-42_ZUGFeRD.pdf"

# (doc_id, field, old answer, new answer, new printed, reason) -- proposed_fixes.csv, checked on the page 2026-11-13
FIXES = [
    ("cord__009", "total", None, "36000", "36000",
     "receipt has no Total line; 'Sub Total 36000', Discount (0 %), Tunai 50000, Kembalian 14000: the amount due "
     "36000 is printed (as Sub Total) and equals cash - change; verdict gt_null_wrong (med)"),
    (KONIK, "total_tax", "19", "269.80", "269,80",
     "page: 'Umsatzsteuer 19% 269,80' under 'Summe netto 1.420,00'; GT held the VAT rate; verdict gt_wrong (high)"),
    (RK, "buyer_name", "GLN 4304171000002 \nKunden-Nr. : 009420\nMUSTER-KUNDE GMBH", "MUSTER-KUNDE GMBH",
     "MUSTER-KUNDE GMBH",
     "page 1 Käufer block: GLN and Kunden-Nr. lines are not the name; verdict gt_wrong (high)"),
    (RK, "seller_name", "GLN 4333741000005 \nLief-Nr: 549910\nMUSTERLIEFERANT GMBH", "MUSTERLIEFERANT GMBH",
     "MUSTERLIEFERANT GMBH",
     "page 1 Verkäufer block: GLN and Lief-Nr lines are not the name; verdict gt_wrong (high)"),
    (HAFT, "buyer_name", "Herrn\nMax Mustermann", "Max Mustermann", "Max Mustermann",
     "salutation 'Herrn' is not part of the name; verdict gt_wrong (med)"),
]

# (doc_id, field, value, source in the verdict, forced) -- forced: store even if the scorer already accepts it
ACCEPTED = [
    ("pt__20210508_202709", "seller_name", "MTD-FERRAGENS DO COMBRO LDA", "proposed_fixes (low): correct_value; "
     "page header reads MTD-FERRAGENS DO COMBRO LDA, first letters partly occluded; old answer kept", True),
    ("pt__20210215_172426", "seller_name", "TIGER PORTUGAL, SA", "correct_value / blind_read (legal entity)", False),
    ("pt__20210215_172426", "seller_name", "Flying Tiger Copenhagen", "correct_value (brand)", False),
    ("pt__20210323_174622", "seller_name", "AUCHAN RETAIL PORTUGAL, S.A.", "correct_value (legal entity)", False),
    ("pt__20210508_181909", "seller_name", "Consertos Rapidos Amoreiras, Lda", "correct_value / blind_read (legal)",
     False),
    ("pt__20210508_202449", "seller_name", "Consertos Rapidos Amoreiras, Lda", "correct_value (legal entity)", False),
    ("pt__20210429_191705", "seller_name", "GASNUNOS - DISTR. COM. GAS LDA", "correct_value (legal entity)", False),
    ("pt__20210429_191705", "seller_name", "GASNUNOS, DISTR. E COM. GAS, LDA", "blind_read (legal entity)", False),
    ("pt__20210429_191705", "seller_name", "GASNUNOS", "prediction confirmed by note '6/6 legal'", False),
    ("pt__20210507_174441", "seller_name", "SEQUEIRA PINTO - COM. COMB. LDA", "correct_value (legal entity)", False),
    ("pt__20210428_195823", "seller_name", "GAR. RIBAMAR (Campo de Ourique)", "blind_read (station/dealer header)",
     False),
    ("pt__20210428_195823", "seller_name", "GAR.RIBAMAR-F.CUNHA COSTA",
     "prediction confirmed by evidence '4 models returned the station/dealer name'", False),
    ("pt__20210428_201521", "seller_name", "GAR. RIBAMAR (Campo de Ourique)", "blind_read (station header)", False),
    ("pt__20210322_164701", "seller_name", "GALPGESTE, S.A.", "blind_read (legal entity)", False),
    ("pt__20210322_164701", "seller_name", "A.S. LAGOS (FARO/SAGRES)", "blind_read (station)", False),
    ("pt__20210316_215850", "seller_name", "AZAFAMA CAMPESTRE - Prod. Alim. Unip. Lda", "correct_value (legal)",
     False),
    ("pt__20210428_232807", "seller_name", "Destreza Aprumada, Lda", "correct_value (legal entity)", False),
    ("pt__20210508_211412", "seller_name", "Dicodis - Distribuição de Bricolage, SA", "blind_read (legal entity)",
     False),
    ("pt__20210509_002234", "seller_name", "AUCHAN RETAIL PORTUGAL, S.A.", "blind_read (legal entity)", False),
    ("pt__20210323_162221", "seller_name", "SODIAL PORCHINHOS-SUPERMERCADOS, LDA", "blind_read (legal entity)",
     False),
    ("pt__20210215_172904", "seller_name", "Maria da Glória Cabeleireiros Lda.", "blind_read (legal entity)", False),
    ("pt__20210320_172744", "seller_name", "Casa Velha", "blind_read ('Casa Velha is the restaurant brand')", False),
    ("pt__20210508_204341", "seller_name", "ESTAÇÃO SERVIÇO CEGONHA LDA", "blind_read (header form)", False),
    ("pt__20210429_200744", "seller_name", "Pingo Doce - Distribuição Alimentar, S.A.", "blind_read (legal)", False),
    ("pt__20210507_170653", "seller_name", "AUCHAN RETAIL PORTUGAL, S.A.", "blind_read (legal entity)", False),
    ("pt__20210428_144738", "seller_name", "Montepio Geral Assoc. Mutualista", "correct_value / blind_read", False),
    ("sroie__X51006414728", "merchant_name", "KEK SPAN OREE", "correct_value (brand logo)", False),
    ("korie__IMG00339", "merchant_name", "다이소", "evidence '3 brand-only 다이소', note '[P-seller] brand ok'", False),
    ("korie__IMG00343", "merchant_name", "CU", "evidence \"2 brand-only 'CU' (ok per [P-seller])\"", False),
    ("korie__IMG00013", "merchant_name", "이마트", "note 'brand-only 이마트 would be accepted per [P-seller]'", False),
    ("wild__0332", "merchant_name", "Panera Bread", "correct_value", False),
    ("wild__0332__mask", "merchant_name", "Panera Bread", "correct_value", False),
    ("wild__0179", "merchant_name", "JAWED HABIB", "correct_value", False),
    ("wild__0003", "merchant_name", "COSTCO WHOLESALE", "correct_value / blind_read", False),
    ("wild__0377", "merchant_name", "McDonald's", "evidence/note: brand-only McDonald's valid per [P-seller]", False),
    (ZUG + "v1_correct_Intarsys_ZUGFeRD_1p0_EXTENDED_Kostenrechnung.pdf", "seller_name", "KOSTENLIEFERANT GMBH",
     "blind_read: name in the page's Lieferant (supplier) block; verdict doc_mismatch", False),
    (HAFT, "seller_name", "Versicherungsverein Musterstadt a.G.", "blind_read: legal-entity line of the letterhead",
     False),
    (ZUG + "v1_correct_Intarsys_ZUGFeRD_1p0_COMFORT_Kraftfahrversicherung_Bruttopreise.pdf", "seller_name",
     "Versicherungsverein Musterstadt a.G.", "blind_read: legal-entity line of the letterhead", False),
    (ZUG + "v2_correct_symtrax_Beispiele_BASIC_zugferd_2p1_BASIC_Einfach.pdf", "seller_vat_id", "201/113/40209",
     "blind_read: 'Steuernummer 201/113/40209 and USt.-Id.-Nr. DE123456789'", False),
]

# ---------------------------------------------------------------- stage 1 (05-closeout-plan.md, items 1.1-1.5, 1.9)
EXCLUDE_DOCS = [  # 1.1, owner decision (3)
    ("wild__0426", "stock mock-up (template image), its arithmetic does not add up; owner decision 2026-11-13 (3); "
                   "verdicts wild__0426::*"),
    ("wild__0428", "stock mock-up (template image), its arithmetic does not add up; owner decision 2026-11-13 (3); "
                   "verdicts wild__0428::*"),
]
# 1.2: (mask doc, masked field, evidence on the __mask page image). Candidates from tools/mask_probe_scan.py
# (reports/gt_check/stage1/mask_probe_candidates.csv); every one checked on the page by Claude (Opus) 2026-11-13.
MASK_PROBES = [
    ("sroie__X51007579725__mask", "total", "SUBTOTAL 55.90 + SRVC 5% 2.80 = 58.70; also CASH 100.00 - CHANGE 41.30"),
    ("sroie__X51005719898__mask", "total", "GST summary Amt 11.23 + Tax 0.67 = 11.90; also CASH 22.00 - CHANGE 10.10"),
    ("sroie__X51008099088__mask", "total", "items 2.10 + 0.20 = 2.30 (Total QTY 2)"),
    ("sroie__X51007846304__mask", "total", "pre-rounding 'Total Amount: RM7.52' and 'Rounding: -RM0.02' visible "
                                           "(7.52 - 0.02 = 7.50); GST summary 7.52"),
    ("sroie__X51005757220__mask", "total", "items 10.90 + 10.90 + 44.00 + 15.40 = 81.20; GST summary 79.09 + 2.11; "
                                           "CASH 100.00 - Change 18.80"),
    ("sroie__X51006556809__mask", "total", "'Total 6% supplies (Inc. GST) 19.98' + 'Total 0% supplies 23.38' = 43.36 "
                                           "(Total Payable painted)"),
    ("sroie__X51006557115__mask", "total", "'Total 6% supplies (Inc. GST) 21.75' + 'Total 0% supplies 13.83' = 35.58"),
    ("sroie__X51006556808__mask", "total", "'Total 6% supplies (Inc. GST) 60.34' + 'Total 0% supplies 18.92' = 79.26"),
    ("sroie__X51009008091__mask", "total", "item 11.00 - Member Discount 1.10 = 9.90; GST summary 9.34 + 0.56; "
                                           "Cash 20.00 - CHANGE 10.10"),
    ("cord__014__mask", "total", "SUBTOTAL 238,000 + Service 17,850 + PB1 25,585 = 281,435; also Coupon 100,000 + "
                                 "CASH 200,000 - Change 18,565"),
    ("cord__070__mask", "total", "SUBTOTAL 1,343,000 + SERVICE CHARGE 80,580 + Tax 10% 142,358 = 1,565,938"),
    ("cord__020__mask", "total", "SUBTOTAL 325,600 + Service chrg 17,908 + 10% PB1 34,351 = 377,859"),
    ("cord__072__mask", "total", "SubTotal 15,909 + PB1 1,591 = 17,500; also cash 20,000 - Change 2,500"),
    ("cord__058__mask", "tax_amount", "Total 60,500 - Sub Total 55,000 = 5,500 (PB1 painted)"),
    ("cord__084__mask", "tax_amount", "Total Rp 39.600 - Subtotal Rp 36.000 = 3.600 = Tax (10.0%) of 36.000"),
    ("wild__0298__mask", "total", "'Rounding 12.00' and 'Rounding Adjust 0.02' visible: 12.00 - 0.02 = 11.98 "
                                  "(Eat-In Total painted)"),
    ("wild__0082__mask", "total", "SUBTOTAL $77.46 + 9.300% Sales Tax $6.65 = $84.11"),
    ("wild__0121__mask", "subtotal", "TOTAL 4.24 - SALES TAX 6% .24 = 4.00; items .50 + .50 + 1.50 + 1.50 = 4.00"),
    ("wild__0168__mask", "tax_amount", "TOTAL JOD 3.05 - SUB-TOTAL 2.50 - SERVICE 0.20 = 0.35 (TAX 16% value painted)"),
]
# kept on purpose (checked on the page): FATURA total_gross probes Template28_Instance0, Template31_Instance0,
# Template43_Instance1. SUB_TOTAL and TAX are printed, but the generator's TOTAL is not their sum (959.48 vs 988.54,
# 248.12 vs 260.05, 421.93 vs 420.47 with the printed discount), so the masked value cannot be derived.
PHYS1 = ZUG[:-len("ZUGFeRD")] + "XML-Rechnung_FX_EN16931_Physiotherapeut.pdf"
PHYS2 = ZUG + "v2_correct_intarsys_EN16931_zugferd_2p0_EN16931_Physiotherapeut.pdf"
FIXES_1 = [  # 1.9b, owner decision (4); page 1 of each document checked
    # PHYS1 is NOT changed: its page labels the fields 'Name: Physiotherapeutin' / 'Ansprechpartner: Tanja Tinder',
    # so 'Physiotherapeutin' is printed as the seller's name -> owner rule: a word used as the name counts.
    (PHYS2, "seller_name", "Physiotherapeutin", "Tanja Tinder", "Tanja Tinder",
     "page 1 Verkäufer: 'Physiotherapeutin' (profession) printed above 'Tanja Tinder'; owner rule: profession above "
     "the person's name -> the person's name is the seller name"),
]
BASIC_WL = ZUG + "v2_correct_symtrax_Beispiele_BASIC_WL_zugferd_2p1_BASIC-WL_Einfach.pdf"
ACCEPTED_1 = [  # (doc, field, value, evidence on the page); 1.3 and 1.5
    (BASIC_WL, "due_date", "2020-04-04",
     "page 1 prints both: 'Zahlbar innerhalb 30 Tagen netto bis 04.04.2020' and table 'Fälligkeit 13.12.2017'"),
    ("pt__20210428_140713", "seller_name", "ELENCOJASMIN LDA",
     "re-examined 'unsure': zoomed header reads ELENCOJASMIN (last glyph N); GT spelling jasmim kept"),
    ("fatura__Template49_Instance0", "buyer_name", "Joseph Wagner",
     "page 1 prints two buyer blocks: 'Bill to:Jessica Acevedo' and 'BILL_TO: Joseph Wagner'"),
    ("fatura__Template49_Instance0__mask", "buyer_name", "Joseph Wagner",
     "same page as fatura__Template49_Instance0: two 'Bill to' blocks"),
]
# 1.3, already in ACCEPTED (stage 0) and re-checked on page 1 in stage 1: Kostenrechnung v1 EXTENDED seller_name
# MUSTERLIEFERANT GMBH (footer, e-mail) + KOSTENLIEFERANT GMBH (Lieferant block).
QUALITY_LOW = [  # 1.4: still scored; reports show accuracy with and without them
    ("pt__20210323_162221", "stage 2: dot-matrix NIF digit 3 vs 2 ambiguous (models split 2:3); GT 394 by NIF check digit"),
    ("wild__0352", "image 258 px wide: amounts and logo barely legible"),
    ("sroie__X51006328937", "merchant name OLIVE9: first glyph clipped at the edge"),
    ("synrec__eval-000608__photo", "photo variant: blur/perspective makes digits ambiguous"),
    ("pt__20210428_141746", "cropped series (photo of a cropped receipt)"),
    ("pt__20210507_215634", "cropped/faded series: invoice series glyph T1 vs 11"),
    ("eurodocbench__test-nl-NL-narrow-014", "IBAN font: letter O and digit 0 indistinguishable"),
]
EXCLUDE_DOC_REASON = "whole document excluded after round 1 (closeout 1.1): "
PROBE_REASON = ("mask probe excluded (closeout 1.2): the painted amount can be derived from printed numbers or a "
                "rounded/other version stays visible: ")

TOTALS = ("total_gross", "total_net", "total_tax")
EXCLUDE_REASON = ("invoice total not printed (answer null, field not masked): not scored. Owner decision "
                  "2026-11-13 (2) p.1, applied by tools/apply_gt_review.py")

# ---- closeout stage 2 (Sonnet review of reports/gt_check/stage2/, owner decisions (5)) ----
FIXES_2 = [  # (doc, field, old, new, printed, reason)
    ("pt__20210323_162221", "seller_vat_id", "508162294", "508162394", "508162394",
     "header 'CNT: 508162394'; only 394 passes the Portuguese NIF check digit (9..2 weights, mod 11)"),
]
STNR_DOCS = [
    "zugferd__XML-Rechnung_FX_EN16931_1_Teilrechnung.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_AbweichenderZahlungsempf.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_Betriebskostenabrechnung.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_Einfach_DueDate.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_Einfach_negativePaymentDue.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_Rabatte.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_Reisekostenabrechnung.pdf",
    "zugferd__XML-Rechnung_FX_EN16931_SEPA_Prenotification.pdf",
    "zugferd__XML-Rechnung_FX_XRECHNUNG_Einfach.pdf",
    "zugferd__XML-Rechnung_FX_XRECHNUNG_Elektron.pdf",
    "zugferd__XML-Rechnung_FX_XRECHNUNG_Reisekostenabrechnung.pdf",
    "zugferd__ZUGFeRDv2_correct_intarsys_EN16931_zugferd_2p0_EN16931_1_Teilrechnung.pdf",
    "zugferd__ZUGFeRDv2_correct_intarsys_EN16931_zugferd_2p0_EN16931_2_Teilrechnung.pdf",
    "zugferd__ZUGFeRDv2_correct_intarsys_EN16931_zugferd_2p0_EN16931_Einfach.pdf",
    "zugferd__ZUGFeRDv2_correct_intarsys_EN16931_zugferd_2p0_EN16931_SEPA_Prenotification.pdf",
    "zugferd__ZUGFeRDv2_correct_intarsys_MINIMUM_zugferd_2p0_MINIMUM.pdf",
    "zugferd__ZUGFeRDv2_correct_symtrax_Beispiele_EN16931_zugferd_2p1_EN16931_Elektron_XRechnung.pdf",
    "zugferd__ZUGFeRDv2_correct_symtrax_Beispiele_EN16931_zugferd_2p1_EN16931_Reisekostenabrechnung.pdf"
]
ACCEPTED_2 = [  # (doc, field, value, evidence)
    *[(d, "seller_vat_id", "201/113/40209", "page prints the seller's Steuernummer 201/113/40209 next to the USt-IdNr "
       "(Apple Vision OCR); owner rule: any seller tax id counts") for d in STNR_DOCS],
    ("pt__20210324_200034", "seller_name", "JOAQUIM ANTÃO TRAVANCA CAPUCHO",
     "owner name printed in the header; owner rule: any identifiable seller name counts"),
    ("pt__20210507_214450", "seller_name", "GAR RIBAMAR F. CUNHA COSTA",
     "station / dealer name printed; owner rule: dealer or station name counts"),
    ("wild__0016", "total", "63.90",
     "page prints 'Total 63.92' and 'Amt Due 63.90' (0.02 rounding); owner decision (5): both count"),
]
EXCLUDE_FIELDS_2 = [  # (doc, field, reason): owner decision (5)
    ("fatura__Template39_Instance1", "seller_name",
     "no seller name in text, only a logo roundel 'LCSR' (name or emblem unclear); excluded by owner decision (5)"),
    ("fatura__Template39_Instance1__mask", "seller_name", "same page as fatura__Template39_Instance1"),
]
# owner decision (5): zugferd seller_iban when only the divergent payee's / tax representative's IBAN is printed:
# that IBAN counts. The GT of AbweichenderZahlungsempf, Innergemeinschaftliche_Lieferungen and intarsys EXTENDED
# Fremdwaehrung already holds it: no edit.


def dump(a: dict) -> str:
    return json.dumps(a, indent=1, ensure_ascii=False)


def stage1(load, excl: list[dict], man: list[dict], verdicts: dict) -> list[dict]:
    """Closeout stage 1 edits, in place on the loaded answers / excluded rows / manifest rows; returns the log."""
    log = []

    def row(doc, field, action, old, new, rid, reason):
        log.append({"doc_id": doc, "field": field, "action": action, "old": "" if old is None else old,
                    "new": "" if new is None else new, "review_id": rid, "reason": reason, "stage": "1"})
    have = {(x["doc_id"], x["field"]) for x in excl}
    # 1.1 whole documents
    gone = {d for d, _ in EXCLUDE_DOCS}
    for doc, reason in EXCLUDE_DOCS:
        if (doc, "*") not in have:
            excl.append({"doc_id": doc, "field": "*", "printed": "", "reason": EXCLUDE_DOC_REASON + reason})
        row(doc, "*", "exclude_doc", "", "", "", reason)
    man[:] = [r for r in man if r["doc_id"] not in gone]
    # 1.2 mask probes
    mf = {r["doc_id"]: r["masked_field"] for r in man}
    for doc, field, evidence in MASK_PROBES:
        if mf.get(doc) != field:
            raise SystemExit(f"{doc}: masked field is {mf.get(doc)!r}, not {field}")
        fields = load(doc)["fields"]
        if field in fields:
            spec = fields[field]
            if spec["answer"] is not None or not spec.get("masked"):
                raise SystemExit(f"{doc}::{field} is not a masked null probe: {spec}")
            del fields[field]
        if (doc, field) not in have:
            excl.append({"doc_id": doc, "field": field, "printed": "", "reason": PROBE_REASON + evidence})
        row(doc, field, "exclude", "", "", f"{doc}::{field}", "mask probe derivable; page: " + evidence)
    # 1.9b GT fixes
    for doc, field, old, new, printed, reason in FIXES_1:
        f = load(doc)["fields"][field]
        if f["answer"] != new:
            if f["answer"] != old:
                raise SystemExit(f"{doc}::{field}: answer {f['answer']!r}, expected {old!r}")
            f["answer"], f["printed"] = new, printed
        rid = f"{doc}::{field}"
        row(doc, field, "fix", old, new, rid, f"{reason}; verdict {verdicts.get(rid, {}).get('verdict', '')}")
    # 1.3 / 1.5 accepted variants
    for doc, field, value, evidence in ACCEPTED_1:
        f = load(doc)["fields"][field]
        if N.equal(field, f["answer"], value):
            raise SystemExit(f"{doc}::{field}: {value!r} is already accepted by the scorer")
        acc = f.setdefault("accepted", [])
        if value not in acc:
            acc.append(value)
        rid = f"{doc}::{field}"
        row(doc, field, "accepted", f["answer"], value, rid,
            f"page prints both values; {evidence}; verdict {verdicts.get(rid, {}).get('verdict', '')}")
    # redundant accepted entries after the fixes (the scorer accepts them against the answer anyway)
    forced = {(d, f, v) for d, f, v, _, frc in ACCEPTED if frc}
    for doc, *_ in FIXES_1:
        for field, f in load(doc)["fields"].items():
            for v in list(f.get("accepted") or []):
                if (doc, field, v) not in forced and N.equal(field, f["answer"], v):
                    f["accepted"].remove(v)
                    row(doc, field, "accepted_drop", f["answer"], v, f"{doc}::{field}",
                        "redundant after the GT fix: the scorer accepts it against the answer")
            if "accepted" in f and not f["accepted"]:
                del f["accepted"]
    # 1.4 quality tag
    low = dict(QUALITY_LOW)
    for r in man:
        r["quality"] = "low" if r["doc_id"] in low else ""
    for doc, reason in QUALITY_LOW:
        a = load(doc)
        if a.get("quality") != "low":
            a["quality"] = "low"
        row(doc, "*", "quality_low", "", "low", "", reason)
    return log


def stage2(load, excl: list[dict], verdicts: dict) -> list[dict]:
    """Closeout stage 2 edits (after the stage-2 review); returns the log."""
    log = []

    def row(doc, field, action, old, new, rid, reason):
        log.append({"doc_id": doc, "field": field, "action": action, "old": "" if old is None else old,
                    "new": "" if new is None else new, "review_id": rid, "reason": reason, "stage": "2"})
    for doc, field, old, new, printed, reason in FIXES_2:
        f = load(doc)["fields"][field]
        if f["answer"] != new:
            if f["answer"] != old:
                raise SystemExit(f"{doc}::{field}: answer {f['answer']!r}, expected {old!r}")
            f["answer"], f["printed"] = new, printed
        row(doc, field, "fix", old, new, f"{doc}::{field}", reason)
    for doc, field, value, evidence in ACCEPTED_2:
        f = load(doc)["fields"][field]
        if N.equal(field, f["answer"], value):
            raise SystemExit(f"{doc}::{field}: {value!r} is already accepted by the scorer")
        acc = f.setdefault("accepted", [])
        if value not in acc:
            acc.append(value)
        row(doc, field, "accepted", f["answer"], value, f"{doc}::{field}", evidence)
    have = {(x["doc_id"], x["field"]) for x in excl}
    for doc, field, reason in EXCLUDE_FIELDS_2:
        fields = load(doc)["fields"]
        if field in fields:
            if fields[field]["answer"] is not None:
                raise SystemExit(f"{doc}::{field}: expected a null answer, got {fields[field]}")
            del fields[field]
        if (doc, field) not in have:
            excl.append({"doc_id": doc, "field": field, "printed": "", "reason": reason})
        row(doc, field, "exclude", "", "", f"{doc}::{field}", reason)
    return log


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    verdicts = {json.loads(l)["review_id"]: json.loads(l) for l in VERDICTS.read_text().splitlines() if l.strip()}
    docs: dict[str, dict] = {}

    def load(doc):
        if doc not in docs:
            docs[doc] = json.loads((FINAL / "docs" / doc / "answers.json").read_text())
        return docs[doc]

    log = []          # rows of applied_fixes.csv
    # 1. fixes
    for doc, field, old, new, printed, reason in FIXES:
        f = load(doc)["fields"][field]
        if f["answer"] == new:
            print(f"already applied: {doc}::{field}")
        elif f["answer"] != old:
            raise SystemExit(f"{doc}::{field}: answer {f['answer']!r}, expected {old!r}")
        else:
            f["answer"], f["printed"] = new, printed
        log.append({"doc_id": doc, "field": field, "action": "fix", "old": "" if old is None else old,
                    "new": new, "review_id": f"{doc}::{field}", "reason": reason})
    # 2. accepted variants
    for doc, field, value, source, forced in ACCEPTED:
        rid = f"{doc}::{field}"
        if rid not in verdicts:
            raise SystemExit(f"no verdict for {rid}")
        f = load(doc)["fields"][field]
        if not forced and N.equal(field, f["answer"], value):
            continue        # the scorer already accepts it against the answer: nothing to store
        acc = f.setdefault("accepted", [])
        if value not in acc:
            acc.append(value)
        log.append({"doc_id": doc, "field": field, "action": "accepted", "old": f["answer"], "new": value,
                    "review_id": rid, "reason": f"owner rule [{'seller tax id' if 'vat' in field else 'seller name'}]"
                                                f"; source: {source}; verdict {verdicts[rid]['verdict']}"})
    # 3. invoice totals
    excl_path = FINAL / "excluded.csv"
    excl = list(csv.DictReader(open(excl_path, newline="")))
    have = {(r["doc_id"], r["field"]) for r in excl}
    man_path = FINAL / "manifest.csv"
    man = list(csv.DictReader(open(man_path, newline="")))
    for r in man:
        if r["doc_type"] != "invoice":
            continue
        doc = r["doc_id"]
        fields = load(doc)["fields"]
        for t in TOTALS:
            spec = fields.get(t)
            if spec is not None and spec["answer"] is None and not spec.get("masked"):
                del fields[t]
                if (doc, t) not in have:
                    excl.append({"doc_id": doc, "field": t, "printed": "", "reason": EXCLUDE_REASON})
        g, n = fields.get("total_gross"), fields.get("total_net")
        excluded_now = {(x["doc_id"], x["field"]) for x in excl}
        for have_f, other in ((g, "total_net"), (n, "total_gross")):
            if have_f is not None and have_f["answer"] is not None and (doc, other) in excluded_now \
                    and other not in fields:
                if have_f.get("accept_from") != [other]:
                    have_f["accept_from"] = [other]
                me = "total_gross" if other == "total_net" else "total_net"
                log.append({"doc_id": doc, "field": me, "action": "accept_from", "old": have_f["answer"],
                            "new": other, "review_id": "",
                            "reason": f"only {me} printed; the amount counts in {other} too (owner decision (2) p.1)"})
    log += [{"doc_id": x["doc_id"], "field": x["field"], "action": "exclude", "old": "", "new": "", "review_id": "",
             "reason": "answer null, not masked"} for x in excl if x["reason"] == EXCLUDE_REASON]
    for row in log:
        row["stage"] = "0"
    log += stage1(load, excl, man, verdicts)
    log += stage2(load, excl, verdicts)
    # manifest counts
    for r in man:
        if r["doc_id"] in docs:
            fl = docs[r["doc_id"]]["fields"]
            nv = sum(v["answer"] is not None for v in fl.values())
            r["n_values"], r["n_null"] = str(nv), str(len(fl) - nv)

    acts = {}
    for row in log:
        acts[row["action"]] = acts.get(row["action"], 0) + 1
    print(acts)
    if a.dry_run:
        return 0
    for doc, _ in EXCLUDE_DOCS:
        if (FINAL / "docs" / doc).exists():
            shutil.rmtree(FINAL / "docs" / doc)
    for doc, ans in docs.items():
        p = FINAL / "docs" / doc / "answers.json"
        if not p.parent.exists():
            continue
        old = p.read_text()
        new = dump(ans) + ("\n" if old.endswith("\n") else "")   # keep each file's trailing newline
        if old != new:
            p.write_text(new)
    with open(excl_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["doc_id", "field", "printed", "reason"])
        w.writeheader()
        w.writerows(excl)
    with open(man_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(man[0].keys()))
        w.writeheader()
        w.writerows(man)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["doc_id", "field", "action", "old", "new", "review_id", "reason", "stage"])
        w.writeheader()
        w.writerows(log)
    print(f"{len(log)} rows -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
