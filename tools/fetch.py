"""Download pinned datasets listed in data/sources.yaml.

- github: zip archive of a pinned commit (no git needed)
- hf:     snapshot of a pinned revision, filtered by allow patterns
- urls:   plain files

Every downloaded file gets a sha256 in data/manifest.json. Nothing downloaded is executed.
Archives are extracted with a path-traversal check.

Usage: uv run python -I tools/fetch.py [id ...]   (no ids = all)
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = ROOT / "data" / "manifest.json"
UA = {"User-Agent": "research-fetch/0.1"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    tmp.rename(dest)


def safe_extract(zpath: Path, target: Path) -> None:
    target = target.resolve()
    with zipfile.ZipFile(zpath) as z:
        for m in z.infolist():
            out = (target / m.filename).resolve()
            if not str(out).startswith(str(target)):
                raise RuntimeError(f"unsafe path in archive: {m.filename}")
        z.extractall(target)


def fetch_github(src: dict, d: Path) -> list[Path]:
    url = f"https://codeload.github.com/{src['repo']}/zip/{src['commit']}"
    z = d / f"{src['id']}-{src['commit'][:10]}.zip"
    if not z.exists():
        download(url, z)
    safe_extract(z, d / "src")
    return [z]


def fetch_hf(src: dict, d: Path) -> list[Path]:
    from huggingface_hub import snapshot_download

    p = snapshot_download(
        repo_id=src["repo"], repo_type="dataset", revision=src["revision"],
        allow_patterns=src.get("allow"), local_dir=d / "src",
    )
    return sorted(x for x in Path(p).rglob("*") if x.is_file() and ".cache" not in x.parts)


def fetch_urls(src: dict, d: Path) -> list[Path]:
    out = []
    for u in src["urls"]:
        url, name = (u["url"], u["name"]) if isinstance(u, dict) else (u, u.rsplit("/", 1)[1])
        f = d / "src" / name
        if not f.exists():
            download(url, f)
        if f.suffix == ".zip":
            safe_extract(f, f.with_suffix(""))
        elif f.suffix == ".tar":
            import tarfile
            target = f.with_suffix("").resolve()
            with tarfile.open(f) as t:
                t.extractall(target, filter="data")  # 'data' filter blocks traversal, links, devices
        out.append(f)
    return out


def main(ids: list[str]) -> None:
    cfg = yaml.safe_load((ROOT / "data" / "sources.yaml").read_text())
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for src in cfg["sources"]:
        if ids and src["id"] not in ids:
            continue
        d = RAW / src["id"]
        d.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        try:
            files = {"github": fetch_github, "hf": fetch_hf, "urls": fetch_urls}[src["kind"]](src, d)
        except Exception as e:  # keep going; record the failure
            print(f"[FAIL] {src['id']}: {type(e).__name__}: {e}", flush=True)
            manifest[src["id"]] = {"status": "failed", "error": f"{type(e).__name__}: {e}"}
            MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
            continue
        entry = {k: src[k] for k in ("kind", "repo", "commit", "revision", "license", "langs", "doc_types") if k in src}
        entry["status"] = "ok"
        entry["fetched_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        entry["files"] = {str(f.relative_to(d)): {"bytes": f.stat().st_size, "sha256": sha256(f)} for f in files}
        manifest[src["id"]] = entry
        MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
        size = sum(v["bytes"] for v in entry["files"].values()) / 1e6
        print(f"[OK] {src['id']}: {len(files)} files, {size:.1f} MB, {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
