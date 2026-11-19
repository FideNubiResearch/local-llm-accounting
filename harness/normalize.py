"""Comparison of a model answer with a ground-truth answer from final/docs/*/answers.json.

The ground truth is already canonical (final/README.md): ISO date, HH:MM, decimal string with ".", ISO currency,
ids without their printed label. It is parsed strictly. Only the model answer may be ambiguous, and then it counts
as correct if any of its readings equals the ground truth:
  amount  "47.000" / "1,234" (one separator + exactly 3 digits) -> thousands or decimals;
  date    "05/04/2026" -> 5 April or 4 May.
Whether the model used the requested format is recorded separately (is_canonical), not mixed into correctness.
Every rule here has a test in tests/test_score.py.

Rules added after the round-1 GT review (owner decisions, journal 2026-11-13); each can be switched off through
equal(..., rules=...) so that a re-score can tell which rule changed an outcome (RULES; LEGACY = none of them):
  date_swap       GT day and month both <= 12: the day/month swap of the GT date is accepted too;
  amount_abs      the sign is ignored (refunds, credit notes, amounts in brackets);
  name_fold       names: diacritics folded, whitespace / newlines / punctuation ignored;
  name_legal      names: legal-form tokens dropped (GmbH, AG, KG, S.A., S.p.A., S.r.l., SARL, Lda, Sp. z o.o.,
                  Sdn Bhd, B.V., (주), ㈜);
  name_honorific  names: Herr / Herrn / Frau dropped;
  name_contain    names: correct when the GT name's tokens are all in the prediction (name + address), or the GT
                  written without spaces is a run of consecutive prediction tokens;
  id_label        ids: a leading "No." / "Nº" / "N°" / "NIF" / "NIPC" label is dropped (GT and prediction);
  id_crc          ids: a trailing "/CRC ..." (Portuguese registry office) is dropped;
  id_cc           tax ids only: a leading 2-letter country code before a digit is dropped (PT510776914);
  id_series       invoice_number only: a leading series token is dropped (FS, FT, FTR, NFS, FR ... before the
                  number; or letters + one digit before "/", as in "C2 / 1318851"); the remaining characters must
                  match exactly (owner decision 2026-11-13 (3)).
  pay_class       payment_method only: diacritics folded, and a translation counts (owner decision 2026-11-15):
                  answers in the same class are equal -- cash (CONTANTI = BAR = ESPECES = CASH ...) or
                  contactless (KONTAKTLOS = SANS CONTACT = CARTA CONTACTLESS = CONTACTLESS ...). Card brands are
                  not merged (VISA != MASTERCARD != CARD); a register number ("CASSA 1") and typos stay wrong.
Digits are never edited: a wrong digit in an amount or id stays wrong.

Format flag for names (owner decision 2026-11-13 (4)): a name found inside extra text (address, second line,
extra tokens) is a correct value, but its format is wrong; score.outcome sets canonical=False for such a TP
(name_clean). A name equal to the GT or to an `accepted` variant after the name_* normalizations is canonical.
"""
from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation

# field kind per canonical field name (shared across doc types)
FIELD_KIND = {
    # identifiers: compare alphanumerics only, case-insensitive
    "invoice_number": "id", "seller_vat_id": "id", "buyer_vat_id": "id", "seller_iban": "id",
    "purchase_order": "id", "merchant_tax_id": "id", "account_number": "id", "registration_number": "id",
    "address_postcode": "id",
    # dates / time
    "issue_date": "date", "due_date": "date", "date": "date", "period_start": "date", "period_end": "date",
    "period_end_date": "date", "time": "time",
    # amounts
    "total_net": "amount", "total_tax": "amount", "total_gross": "amount", "subtotal": "amount",
    "tax_amount": "amount", "total": "amount", "opening_balance": "amount", "closing_balance": "amount",
    "total_income": "amount", "total_spending": "amount", "quantity": "amount", "unit_price": "amount",
    "line_total": "amount", "price": "amount", "amount": "amount",
    "currency": "currency",
}

NAME_FIELDS = {"seller_name", "buyer_name", "merchant_name", "account_holder", "bank_name"}
TAX_ID_FIELDS = {"seller_vat_id", "buyer_vat_id", "merchant_tax_id"}
RULES = frozenset({"date_swap", "amount_abs", "name_fold", "name_legal", "name_honorific", "name_contain",
                   "id_label", "id_crc", "id_cc", "id_series", "pay_class"})
# rule pay_class: payment methods that are the same thing in another language (text() + fold() applied first)
PAY_CLASS = {
    "cash": {"cash", "contanti", "contante", "bar", "bargeld", "barzahlung", "especes", "espece", "efectivo",
             "dinheiro", "numerario", "contant", "contanten", "gotowka", "현금", "現金", "现金", "tunai"},
    "contactless": {"contactless", "kontaktlos", "sans contact", "carta contactless", "card contactless",
                    "contactless card", "tarjeta contactless", "sin contacto", "sem contacto", "sem contato",
                    "paiement sans contact", "carte sans contact", "contactloos"},
}
_PAY_OF = {w: c for c, ws in PAY_CLASS.items() for w in ws}
LEGACY: frozenset = frozenset()

NULL_STRINGS = {"", "null", "none", "n/a", "na", "-", "--", "nil", "not present", "not available", "unknown"}

CURRENCY_SYMBOLS = {
    "€": "EUR", "eur": "EUR", "euro": "EUR", "$": "USD", "us$": "USD", "usd": "USD", "£": "GBP", "gbp": "GBP",
    "¥": "JPY", "円": "JPY", "jpy": "JPY", "元": "CNY", "rmb": "CNY", "cny": "CNY", "₩": "KRW", "원": "KRW",
    "krw": "KRW", "zł": "PLN", "zl": "PLN", "pln": "PLN", "chf": "CHF", "rp": "IDR", "idr": "IDR",
    "rm": "MYR", "myr": "MYR", "sar": "SAR", "aed": "AED", "egp": "EGP", "r$": "BRL", "brl": "BRL",
}


def is_null(v) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip().lower() in NULL_STRINGS:
        return True
    return False


CHECKBOX = "☐☑☒□■▢✓✔√✗✘"


def text(v) -> str:
    s = unicodedata.normalize("NFKC", str(v)).casefold()
    s = re.sub(f"[{CHECKBOX}]", " ", s)
    s = re.sub(r"(?:\.\s*){3,}|…+", " ", s)  # dot leaders of paper forms ("75 ... Rue ..... Coll ...")
    s = re.sub(r"\s+", " ", s).strip()
    return s.strip(" .,;:")


def ident(v) -> str:
    s = unicodedata.normalize("NFKC", str(v)).upper()
    return "".join(ch for ch in s if ch.isalnum())


ID_LABEL = re.compile(r"^\s*(USt-?IdNr\.?|USt-?ID|SIRET|P\.?\s?IVA|VAT( No\.?| ID)?|NIF[-\s]?IVA|NIF|NIPC|NIP( UE)?|GST( No\.?| ID)?"
                      r"|IBAN|N°\s*TVA( intracommunautaire)?|TVA)\s*[:#.]?\s*", re.I)


def ident_value(v) -> str:
    """Identifier without a printed label the model may have copied ("USt-IdNr.: DE123" -> "DE123")."""
    return ident(ID_LABEL.sub("", unicodedata.normalize("NFKC", str(v))))


# "Nº" becomes "No" under NFKC; a separator must follow, so ids such as "NO123456789MVA" are left alone
NUMBER_LABEL = re.compile(r"^\s*(?:N(?:\.\s?|\s?)[º°o](?:\.|(?=[\s:#]))|(?:NIF|NIPC)(?:\s*/\s*CRC)?)\s*[:#.]?\s*",
                          re.I)
CRC_TAIL = re.compile(r"(?<=\w)\s*/\s*C\.?\s?R\.?\s?C.*$", re.I | re.S)
COUNTRY = re.compile(r"^[A-Z]{2}(?=\d)")
# Portuguese document-type codes may precede a series that starts with a letter ("FR B19/43" = "B19/43")
SERIES = re.compile(r"^\s*(?:[A-Za-z]{1,3}\d(?=\s*/)|[A-Za-z]{1,4}(?=[\s\-./]*\d)"
                    r"|(?:FR|FT|FS|FTR|NFS|NC|ND|VD)\s+(?=[A-Za-z]{1,3}\d))[\s\-./]*")


def id_forms(field: str, v, rules=RULES) -> set[str]:
    """Alphanumeric forms of an identifier under the enabled rules (legacy: as is and without a known label)."""
    s = unicodedata.normalize("NFKC", str(v))
    raw = {s}
    if "id_crc" in rules:
        raw.add(CRC_TAIL.sub("", s))
    if "id_label" in rules:
        raw |= {NUMBER_LABEL.sub("", r) for r in list(raw)}
    out = {f for r in raw for f in (ident(r), ident_value(r))}
    if "id_cc" in rules and field in TAX_ID_FIELDS:
        out |= {COUNTRY.sub("", f) for f in out}
    return {f for f in out if f}


def series_free(v, rules=RULES) -> set[str]:
    """Forms of an invoice number without its leading series token (rule id_series)."""
    s = unicodedata.normalize("NFKC", str(v))
    if "id_label" in rules:
        s = NUMBER_LABEL.sub("", s)
    stripped = SERIES.sub("", s)
    return {ident(stripped)} - {"", ident(s)}


def fold(s: str) -> str:
    """Drop diacritics (NFKD, remove combining marks, NFC again so that Hangul recomposes)."""
    d = unicodedata.normalize("NFKD", s)
    return unicodedata.normalize("NFC", "".join(ch for ch in d if not unicodedata.combining(ch)))


# legal forms as whole tokens; longer forms first so "s.a.r.l." is not read as "s.a." + rest
LEGAL_FORM = re.compile(
    r"(?<!\w)(?:s\.?\s?a\.?\s?r\.?\s?l\.?|s\.?\s?p\.?\s?a\.?|s\.?\s?r\.?\s?l\.?|s\.?\s?a\.?|sp\.?\s?z\s?o\.?\s?o\.?"
    r"|sdn\.?\s?bhd\.?|b\.?\s?v\.?|gmbh|ag|kg|lda\.?)(?!\w)|\(\s*주\s*\)")
HONORIFIC = re.compile(r"(?<!\w)(?:herrn|herr|frau)(?!\w)")


def name_tokens(v, rules=RULES) -> list[str]:
    """Tokens of a name under the enabled rules; '_' and punctuation separate tokens."""
    s = unicodedata.normalize("NFKC", str(v)).casefold()
    if "name_fold" in rules:
        s = fold(s)
    for rule, pat in (("name_legal", LEGAL_FORM), ("name_honorific", HONORIFIC)):
        if rule in rules:
            stripped = pat.sub(" ", s)
            if re.search(r"[^\W_]", stripped):        # never strip a name down to nothing
                s = stripped
    return re.findall(r"[^\W_]+", s)


def name_equal(gt, pred, rules=RULES) -> bool:
    g, p = name_tokens(gt, rules), name_tokens(pred, rules)
    gj, pj = "".join(g), "".join(p)
    if not gj:
        return False
    if gj == pj:
        return True
    if "name_contain" not in rules or len(gj) < 3:
        return False
    if set(g) <= set(p):
        return True
    for i in range(len(p)):                          # GT written without spaces ("JAWEDHABIB", "PaneraBread")
        acc = ""
        for t in p[i:]:
            acc += t
            if len(acc) >= len(gj):
                break
        if acc == gj:
            return True
    return False


def name_clean(gt, pred, rules=RULES) -> bool:
    """Format flag for a correct name (owner decision 2026-11-13 (4)): True when the prediction is the GT name
    itself -- equal after text normalization, or the same token string once diacritics, spacing, punctuation,
    legal forms and honorifics are normalized under `rules`; False when it matched only through containment
    (extra text such as an address, a second line or extra tokens). Correctness is decided by equal(), not here."""
    if text(gt) == text(pred) or (ident(gt) != "" and ident(gt) == ident(pred)):
        return True
    g, p = "".join(name_tokens(gt, rules)), "".join(name_tokens(pred, rules))
    return g != "" and g == p


def amount(v) -> Decimal | None:
    """Parse amounts in EU/US/Swiss/space-grouped formats. Returns None if unparseable."""
    if isinstance(v, (int, float, Decimal)):
        return Decimal(str(v))
    s = unicodedata.normalize("NFKC", str(v)).strip()
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1]
    s = s.replace("−", "-")
    if s.endswith("-"):
        neg, s = True, s[:-1]
    if s.startswith("-"):
        neg, s = True, s[1:]
    s = re.sub(r"[^\d.,' ]", "", s).strip().replace("'", "").replace(" ", "")
    if not s or not any(c.isdigit() for c in s):
        return None
    if "," in s and "." in s:
        dec = "," if s.rfind(",") > s.rfind(".") else "."
        grp = "." if dec == "," else ","
        s = s.replace(grp, "").replace(dec, ".")
    elif "," in s:
        parts = s.split(",")
        # "1,234" or "1,234,567" with 3-digit groups -> thousands; otherwise decimal comma
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3 and len(parts[0]) <= 3 and parts[0] != "0"):
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")
    elif s.count(".") > 1:
        s = s.replace(".", "")
    try:
        d = Decimal(s)
    except InvalidOperation:
        return None
    return -d if neg else d


def amount_candidates(v) -> set[Decimal]:
    """Plausible readings of an amount. A single separator followed by exactly 3 digits
    ("45.000", "1,234") is ambiguous between thousands grouping and decimals; return both."""
    a = amount(v)
    if a is None:
        return set()
    out = {a}
    s = re.sub(r"[^\d.,]", "", unicodedata.normalize("NFKC", str(v)))
    m = re.fullmatch(r"(\d{1,3})([.,])(\d{3})", s)
    if m:
        alt_int = Decimal(m.group(1) + m.group(3))
        alt_dec = Decimal(m.group(1) + "." + m.group(3))
        sign = -1 if a < 0 else 1
        out |= {sign * alt_int, sign * alt_dec}
    return out


_DATE_PATTERNS = [
    (r"^(\d{4})[-/.]\s*(\d{1,2})[-/.]\s*(\d{1,2})", "ymd"),                # 2025-11-08, 2025. 11. 08
    (r"^(\d{4})年(\d{1,2})月(\d{1,2})日", "ymd"),
    (r"^(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일", "ymd"),
    (r"^(\d{4})(\d{2})(\d{2})$", "ymd"),
    (r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", "dmy_or_mdy"),
    (r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2})$", "dmy_or_mdy_2"),
]
_MONTHS = {m: i for i, ms in enumerate([
    [], ["jan", "januar", "janvier", "gennaio", "enero", "janeiro", "januari", "stycznia", "styczeń"],
    ["feb", "februar", "février", "fevrier", "febbraio", "febrero", "fevereiro", "februari", "lutego"],
    ["mar", "märz", "maerz", "mars", "marzo", "março", "maart", "marca", "marzec"],
    ["apr", "april", "avril", "aprile", "abril", "kwietnia"],
    ["may", "mai", "maggio", "mayo", "maio", "mei", "maja"],
    ["jun", "juni", "juin", "giugno", "junio", "junho", "czerwca"],
    ["jul", "juli", "juillet", "luglio", "julio", "julho", "lipca"],
    ["aug", "august", "août", "aout", "agosto", "augustus", "sierpnia"],
    ["sep", "sept", "september", "septembre", "settembre", "septiembre", "setembro", "września"],
    ["oct", "oktober", "octobre", "ottobre", "octubre", "outubro", "października"],
    ["nov", "november", "novembre", "noviembre", "novembro", "listopada"],
    ["dec", "dezember", "décembre", "decembre", "dicembre", "diciembre", "dezembro", "december", "grudnia"],
]) for m in ms}


def dates(v) -> set[date]:
    """All plausible calendar dates for a string (ambiguous d/m vs m/d yields both)."""
    s = unicodedata.normalize("NFKC", str(v)).strip().lower()
    out: set[date] = set()

    def add(y, m, d):
        try:
            out.add(date(int(y), int(m), int(d)))
        except ValueError:
            pass

    for pat, kind in _DATE_PATTERNS:
        m = re.match(pat, s)
        if not m:
            continue
        a, b, c = m.groups()
        if kind == "ymd":
            add(a, b, c)
        elif kind == "dmy_or_mdy":
            add(c, b, a); add(c, a, b)
        else:                                   # two-digit year: d/m/y, m/d/y or y/m/d (KORIE "25-11-20")
            y = 2000 + int(c)
            add(y, b, a); add(y, a, b); add(2000 + int(a), b, c)
        if out:
            return out
    m = re.match(r"^(\d{1,2})\.?[\s/-]*(?:de\s+)?([a-zäöüéèûàçóíáãęśźżłń]+)\.?,?[\s/-]*(?:de\s+)?(\d{4}|\d{2})(?!\d)", s)
    # 5 March 2024 / 5. März 2024 / 31-Jul-2004 / 16 de agosto de 2026
    if m and m.group(2)[:3] in {k[:3] for k in _MONTHS}:
        mon = _MONTHS.get(m.group(2)) or next(v2 for k, v2 in _MONTHS.items() if k[:3] == m.group(2)[:3])
        y = int(m.group(3))
        add(y + 2000 if y < 100 else y, mon, m.group(1))
    m = re.match(r"^([a-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})", s)  # March 5, 2024
    if m and m.group(1)[:3] in {k[:3] for k in _MONTHS}:
        mon = next(v2 for k, v2 in _MONTHS.items() if k[:3] == m.group(1)[:3])
        add(m.group(3), mon, m.group(2))
    return out


def time_hm(v) -> str | None:
    m = re.search(r"(\d{1,2})[:.h](\d{2})", unicodedata.normalize("NFKC", str(v)))
    return f"{int(m.group(1)):02d}:{m.group(2)}" if m else None


def currency(v) -> str:
    s = text(v)
    if s in CURRENCY_SYMBOLS:
        return CURRENCY_SYMBOLS[s]
    for sym, code in CURRENCY_SYMBOLS.items():
        if sym in s and not sym.isalpha():
            return code
    return ident(v)[:3]


def equal(field: str, gt, pred, rules=RULES) -> bool:
    """Compare a non-null ground truth value with a non-null prediction.
    rules: the post-review rules to apply (module docstring); LEGACY reproduces the round-1 scorer."""
    kind = FIELD_KIND.get(field, "text")
    if kind == "amount":
        g = Decimal(str(gt))                      # canonical: strict
        if "amount_abs" in rules:
            return any(abs(abs(g) - abs(b)) < Decimal("0.005") for b in amount_candidates(pred))
        return any(abs(g - b) < Decimal("0.005") for b in amount_candidates(pred))
    if kind == "date":
        g = date.fromisoformat(str(gt))
        ds = dates(pred)
        if g in ds:
            return True
        if "date_swap" in rules and g.day <= 12 and g.month <= 12:
            return date(g.year, g.day, g.month) in ds
        return False
    if kind == "time":
        return time_hm(gt) is not None and time_hm(gt) == time_hm(pred)
    if kind == "id":
        if ident(gt) != "" and ident(gt) in (ident(pred), ident_value(pred)):
            return True
        g, p = id_forms(field, gt, rules), id_forms(field, pred, rules)
        if g & p:
            return True
        if "id_series" in rules and field == "invoice_number":
            # the prefix may be missing on one side only: "C2 / 1318851" = "1318851", but not = "C3 / 1318851"
            return bool(series_free(gt, rules) & p) or bool(g & series_free(pred, rules))
        return False
    if kind == "currency":
        return currency(gt) == currency(pred)
    # text: exact after normalization, or equal ignoring all spaces/punctuation (OCR-style tokens)
    if text(gt) == text(pred) or (ident(gt) != "" and ident(gt) == ident(pred)):
        return True
    if field == "payment_method" and "pay_class" in rules:
        g, p = fold(text(gt)), fold(text(pred))
        return g == p or (g in _PAY_OF and _PAY_OF[g] == _PAY_OF.get(p))
    return field in NAME_FIELDS and bool(rules & {"name_fold", "name_legal", "name_honorific", "name_contain"}) \
        and name_equal(gt, pred, rules)


_CANON = {"amount": r"-?\d+(\.\d+)?", "date": r"\d{4}-\d{2}-\d{2}", "time": r"\d{2}:\d{2}", "currency": r"[A-Z]{3}"}


def is_canonical(field: str, pred) -> bool:
    """Did the model answer in the requested form (plain number, ISO date, HH:MM, ISO code)? Text/ids: always here;
    a correct name with extra text is flagged by score.outcome through name_clean()."""
    pat = _CANON.get(FIELD_KIND.get(field, "text"))
    if pat is None or isinstance(pred, (int, float)) and not isinstance(pred, bool):
        return True
    return re.fullmatch(pat, str(pred).strip()) is not None


def anls(gt, pred, tau: float = 0.5) -> float:
    """Average Normalized Levenshtein Similarity for one pair (DocVQA convention)."""
    from rapidfuzz.distance import Levenshtein

    a, b = text(gt), text(pred)
    if not a and not b:
        return 1.0
    nl = Levenshtein.normalized_distance(a, b)
    return 1.0 - nl if nl < tau else 0.0
