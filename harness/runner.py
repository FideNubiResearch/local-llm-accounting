"""MLX model runner with per-call telemetry.

One class for all models (VLMs, OCR-VLMs, extractors); text-only calls pass no images.
Telemetry per call: wall seconds, time-to-first-token, prompt/gen tokens, prompt/gen tok/s, MLX peak memory, RSS.
"""
from __future__ import annotations

import gc
import os
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models_cache"
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")


def _complete(local: Path, revision: str) -> bool:
    """All files of this revision already downloaded (huggingface_hub writes one .metadata per file)."""
    meta = list((local / ".cache" / "huggingface" / "download").glob("*.metadata"))
    if not meta or not (local / "config.json").exists():
        return False
    if any(m.read_text().split("\n", 1)[0].strip() != revision for m in meta):
        return False
    return all((local / m.name[: -len(".metadata")]).exists() for m in meta)


def download(repo: str, revision: str) -> Path:
    local = MODELS / repo.replace("/", "__")
    if revision.startswith("local-") and (local / "config.json").exists():     # own quantisation made by mlx_vlm.convert
        return local
    if _complete(local, revision):
        return local
    from huggingface_hub import snapshot_download

    snapshot_download(repo_id=repo, revision=revision, local_dir=local)
    return local


def remove(repo: str) -> None:
    shutil.rmtree(MODELS / repo.replace("/", "__"), ignore_errors=True)


class Runner:
    def __init__(self, repo: str, revision: str, max_pixels: int | None = None, max_soft_tokens: int | None = None):
        import mlx.core as mx
        from mlx_vlm import load

        self.mx = mx
        self.repo, self.revision = repo, revision
        t = time.perf_counter()
        self.path = download(repo, revision)
        self.download_s = time.perf_counter() - t
        mx.reset_peak_memory()
        t = time.perf_counter()
        self.model, self.processor = load(str(self.path))
        mx.eval(self.model.parameters())
        self.load_s = time.perf_counter() - t
        self.load_peak_gb = mx.get_peak_memory() / 1e9
        ip = getattr(self.processor, "image_processor", None)
        if max_soft_tokens:
            # Gemma 4 image budget: mlx-vlm 0.7.10 drops max_soft_tokens passed to stream_generate, and load() may
            # replace the image processor, so it is set on the processor after load (reports/models_setup.md).
            if ip is None or not hasattr(ip, "max_soft_tokens"):
                raise ValueError(f"{repo}: image processor has no max_soft_tokens")
            ip.max_soft_tokens = max_soft_tokens
        # what the image processor actually uses, recorded in the run config
        self.image_settings = {k: getattr(ip, k) for k in ("max_soft_tokens", "min_pixels", "max_pixels")
                               if ip is not None and isinstance(getattr(ip, k, None), (int, float))}
        if max_pixels:
            self.image_settings["max_pixels_call"] = max_pixels
        self.config = self.model.config
        self.max_pixels = max_pixels
        self._schema_cache = {}

    def _prompt(self, text: str, n_images: int) -> str:
        from mlx_vlm.prompt_utils import apply_chat_template

        return apply_chat_template(self.processor, self.config, text, num_images=n_images, enable_thinking=False)

    def nuextract_prompt(self, template: str, instructions: str, n_images: int) -> str:
        tok = self.processor.tokenizer if hasattr(self.processor, "tokenizer") else self.processor
        msgs = [{"role": "user", "content": [{"type": "image"}] * n_images}]
        return tok.apply_chat_template(msgs, template=template, instructions=instructions, enable_thinking=False,
                                       add_generation_prompt=True, tokenize=False)

    def _schema_processor(self, schema: dict):
        import json

        from mlx_vlm.structured import build_json_schema_logits_processor

        key = json.dumps(schema, sort_keys=True)
        tok = self.processor.tokenizer if hasattr(self.processor, "tokenizer") else self.processor
        # processors keep matcher state: build a fresh one per call (tokenizer index is cached inside mlx-vlm)
        return build_json_schema_logits_processor(tok, schema)

    def generate(self, text: str, images: list[str] | None = None, schema: dict | None = None,
                 max_tokens: int = 2048, prompt: str | None = None) -> dict:
        import psutil
        from mlx_vlm import stream_generate

        mx = self.mx
        images = images or []
        prompt = prompt if prompt is not None else self._prompt(text, len(images))
        kw = {"max_tokens": max_tokens, "temperature": 0.0}
        if schema is not None:
            kw["logits_processors"] = [self._schema_processor(schema)]
        if self.max_pixels:
            kw["max_pixels"] = self.max_pixels
        mx.reset_peak_memory()
        out, last, ttft = [], None, None
        t0 = time.perf_counter()
        err = None
        try:
            for chunk in stream_generate(self.model, self.processor, prompt, image=images or None, **kw):
                if ttft is None:
                    ttft = time.perf_counter() - t0
                out.append(chunk.text)
                last = chunk
        except Exception as e:  # OOM / processor errors are recorded, not fatal
            err = f"{type(e).__name__}: {str(e)[:300]}"
        wall = time.perf_counter() - t0
        res = {
            "text": "".join(out), "error": err, "wall_s": round(wall, 3),
            "ttft_s": round(ttft, 3) if ttft is not None else None,
            "prompt_tokens": getattr(last, "prompt_tokens", None), "gen_tokens": getattr(last, "generation_tokens", None),
            "prompt_tps": round(getattr(last, "prompt_tps", 0.0) or 0.0, 2),
            "gen_tps": round(getattr(last, "generation_tps", 0.0) or 0.0, 2),
            "finish": getattr(last, "finish_reason", None),
            "peak_gb": round(mx.get_peak_memory() / 1e9, 3),
            "rss_gb": round(psutil.Process().memory_info().rss / 1e9, 3),
        }
        return res

    def close(self):
        del self.model, self.processor
        gc.collect()
        self.mx.clear_cache()
