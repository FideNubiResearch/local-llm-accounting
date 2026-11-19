"""Run one model with one prompt over documents of final/ and save raw outputs.

  uv run python -m harness.run --model mlx-community/Qwen3-VL-4B-Instruct-4bit --revision <sha> --prompt P1 \
      [--where lang=fr doc_type=invoice] [--docs ids.txt] [--limit N] [--max-pixels N] [--max-soft-tokens N] [--constrained] [--run-id NAME]

Output: runs/<run_id>/config.json and predictions.jsonl (one line per document: raw text, parsed JSON, telemetry).
A run is resumable: documents already in predictions.jsonl are skipped; the config must be identical.
Score with: uv run python -m harness.report runs/<run_id>
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "final"
PROMPTS = ROOT / "protocol" / "prompts"
LIST_FIELDS = {"line_items", "transactions"}   # not in final/ answers -> not asked
# P1 rendered round 1 and is frozen (tests/test_prompts.py). P1b = P1 with the wording fixes from the round-1 GT review
# (journal 2026-11-13): receipt total vs cash tendered, subtotal/tax only if printed, seller name without address,
# total_gross / total_net never copied into each other. Field texts in protocol/fields.yaml do not enter these prompts.
# Round 2 (closeout plan, problem 15): P0b = P1b without the general "null if absent / never guess" rule (the
# field definitions stay); P2b = P1b + a quote for every value. P0 and P2 stay as they were.
PROMPT_IDS = {"P0": "P0_neutral", "P1": "P1_null", "P1b": "P1b_null", "P2": "P2_evidence",
              "P0b": "P0b_neutral", "P2b": "P2b_evidence"}
QUOTE_PROMPTS = {"P2", "P2b"}


def manifest() -> list[dict]:
    with open(FINAL / "manifest.csv") as f:
        return list(csv.DictReader(f))


def select(rows: list[dict], where: list[str], docs: str | None, limit: int | None) -> list[dict]:
    for w in where:
        k, v = w.split("=", 1)
        rows = [r for r in rows if r[k] in v.split(",")]
    if docs:
        want = [l.strip() for l in Path(docs).read_text().splitlines() if l.strip()]
        by_id = {r["doc_id"]: r for r in rows}
        rows = [by_id[d] for d in want if d in by_id]
    return rows[:limit] if limit else rows


def schema_for(doc_type: str, prompt: str) -> dict:
    """Scalar fields of protocol/schemas.json; P2 / P2b wrap each field as {"value", "quote"}."""
    base = json.loads((ROOT / "protocol" / "schemas.json").read_text())[doc_type]
    props = {k: v for k, v in base["properties"].items() if k not in LIST_FIELDS}
    if prompt in QUOTE_PROMPTS:
        props = {k: {"type": "object", "additionalProperties": False, "required": ["value", "quote"],
                     "properties": {"value": v, "quote": {"type": ["string", "null"]}}} for k, v in props.items()}
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


def prompt_text(doc_type: str, prompt: str, schema: dict) -> str:
    import yaml

    human = yaml.safe_load((ROOT / "protocol" / "fields.yaml").read_text())["doc_type_human"][doc_type]
    tpl = (PROMPTS / f"{PROMPT_IDS[prompt]}.txt").read_text()
    return tpl.format(doc_type_human=human, schema=json.dumps(schema, ensure_ascii=False))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--prompt", choices=sorted(PROMPT_IDS), default="P1")
    ap.add_argument("--where", nargs="*", default=[], help="manifest filters, e.g. lang=fr,de doc_type=invoice")
    ap.add_argument("--docs", help="file with doc_ids, one per line")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--max-pixels", type=int, help="Qwen image budget (pixels of area)")
    ap.add_argument("--max-soft-tokens", type=int, help="Gemma 4 image budget (visual tokens per image)")
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--constrained", action="store_true", help="JSON-schema constrained decoding")
    ap.add_argument("--run-id")
    a = ap.parse_args(argv)

    rows = select(manifest(), a.where, a.docs, a.limit)
    config = {k: getattr(a, k) for k in ("model", "revision", "prompt", "max_pixels", "max_soft_tokens", "max_tokens",
                                       "constrained")}
    run_id = a.run_id or f"{a.model.split('/')[-1]}__{a.prompt}__{time.strftime('%Y%m%d-%H%M%S')}"
    out = ROOT / "runs" / run_id
    out.mkdir(parents=True, exist_ok=True)
    cfg_path, pred_path = out / "config.json", out / "predictions.jsonl"
    if cfg_path.exists():
        old = json.loads(cfg_path.read_text())
        if {k: old.get(k) for k in config} != config:
            raise SystemExit(f"{cfg_path} has a different config; use another --run-id")
    done = set()
    if pred_path.exists():
        done = {json.loads(l)["doc_id"] for l in pred_path.read_text().splitlines() if l.strip()}
    todo = [r for r in rows if r["doc_id"] not in done]
    print(f"{run_id}: {len(rows)} selected, {len(done)} already done, {len(todo)} to run", flush=True)
    if not todo:
        if cfg_path.exists() and not json.loads(cfg_path.read_text()).get("finished_at"):   # stopped after the last doc
            cfg = json.loads(cfg_path.read_text())
            cfg_path.write_text(json.dumps({**cfg, "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=1))
        return run_id

    from harness import memguard
    from harness.runner import Runner
    from harness.score import parse_json

    if not cfg_path.exists():
        cfg_path.write_text(json.dumps({**config, "run_id": run_id}, indent=1))   # the guard records its verdict here
    guard = memguard.start(cfg_path)                  # before the model loads: the load itself can exhaust memory
    runner = Runner(a.model, a.revision, max_pixels=a.max_pixels, max_soft_tokens=a.max_soft_tokens)
    import mlx_vlm

    cfg_path.write_text(json.dumps({**config, "run_id": run_id, "n_selected": len(rows), "mlx_vlm": mlx_vlm.__version__,
                                    "image_processor": runner.image_settings,
                                    "load_s": round(runner.load_s, 2), "load_peak_gb": round(runner.load_peak_gb, 3)},
                                   indent=1))
    with open(pred_path, "a") as f:
        for i, r in enumerate(todo, 1):
            ans = json.loads((FINAL / "docs" / r["doc_id"] / "answers.json").read_text())
            schema = schema_for(r["doc_type"], a.prompt)
            text = prompt_text(r["doc_type"], a.prompt, schema)
            images = [str(FINAL / "docs" / r["doc_id"] / p) for p in ans["pages"]]
            res = runner.generate(text, images, schema=schema if a.constrained else None, max_tokens=a.max_tokens)
            parsed, strict = parse_json(res["text"])
            f.write(json.dumps({"doc_id": r["doc_id"], "parsed": parsed, "strict_json": strict, **res},
                               ensure_ascii=False) + "\n")
            f.flush()
            print(f"[{i}/{len(todo)}] {r['doc_id']} {res['wall_s']}s peak {res['peak_gb']} GB"
                  f"{' ERROR ' + res['error'] if res['error'] else ''}", flush=True)
    guard.set()
    runner.close()
    cfg = json.loads(cfg_path.read_text())
    cfg_path.write_text(json.dumps({**cfg, "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=1))
    return run_id


if __name__ == "__main__":
    main()
