#!/usr/bin/env bash
# Update the public repository (FideNubiResearch/local-llm-accounting) from the current HEAD of this repo.
#
#   tools/publish_public.sh "commit message"          dry run: builds the tree, shows the diff, pushes nothing
#   tools/publish_public.sh "commit message" --push   commit and push
#
# The public repo is English only. Hand-written Russian documents keep their English translation under public_en/<same path>;
# it replaces the Russian file in the public tree. A Russian file without a translation is left out (listed), a translation
# older than its Russian source stops the publication, and any Cyrillic left in the public tree stops it too.
#
# Only an allowlist is published (code, protocols, plans, aggregated reports, per-run config/summary, document list and
# licences). Documents, ground truth and per-document model outputs never leave the private repo
# (00-plan.md section 11). LICENSE, LICENSE-docs and README.md live only in the public repo and are kept as they are.
# Needs `gh auth login` done (PATH: ~/.local/bin). Works from a clean clone, so nothing in the working tree is touched.
set -euo pipefail

MSG="${1:?commit message required}"
PUSH="${2:-}"
REMOTE="https://github.com/FideNubiResearch/local-llm-accounting.git"
ROOT="$(git rev-parse --show-toplevel)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/publish_public.XXXXXX")"
REPO="$WORK/repo"
export PATH="$HOME/.local/bin:$PATH"

[ -z "$(git -C "$ROOT" status --porcelain)" ] || { echo "working tree is not clean; commit first (the public copy is built from HEAD)"; exit 1; }

git clone -q "$REMOTE" "$REPO"
KEEP="$WORK/keep"; mkdir -p "$KEEP"
for f in LICENSE LICENSE-docs README.md; do cp "$REPO/$f" "$KEEP/$f"; done
find "$REPO" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +

# allowlist
git -C "$ROOT" archive HEAD harness tools tests protocol pyproject.toml uv.lock .gitignore \
  00-plan.md 01-literature.md 05-closeout-plan.md journal.md \
  final/README.md final/licenses.csv final/manifest.csv final/excluded.csv \
  reports/SUMMARY.md reports/final reports/round2 reports/r1_vs_r1b reports/invented reports/extractors reports/energy \
  reports/models_catalog.md reports/models_setup.md | tar -x -C "$REPO"
for d in "$ROOT"/runs/*/; do                       # aggregated per-run files only
  n="$(basename "$d")"
  git -C "$ROOT" cat-file -e "HEAD:runs/$n/summary.md" 2>/dev/null || continue
  mkdir -p "$REPO/runs/$n"
  git -C "$ROOT" show "HEAD:runs/$n/summary.md" > "$REPO/runs/$n/summary.md"
  git -C "$ROOT" show "HEAD:runs/$n/config.json" > "$REPO/runs/$n/config.json"
done
cp "$KEEP"/* "$REPO"/

# English translations (public_en/ mirrors the paths it replaces)
if git -C "$ROOT" cat-file -e HEAD:public_en 2>/dev/null; then
  git -C "$ROOT" archive HEAD public_en | tar -x -C "$WORK"
  stale=""
  while IFS= read -r t; do
    rel="${t#public_en/}"
    src_t=$(git -C "$ROOT" log -1 --format=%ct -- "$rel"); tr_t=$(git -C "$ROOT" log -1 --format=%ct -- "$t")
    [ -n "$src_t" ] && [ "$src_t" -gt "$tr_t" ] && stale="$stale $rel"
    mkdir -p "$(dirname "$REPO/$rel")"; cp "$WORK/$t" "$REPO/$rel"
  done < <(git -C "$ROOT" ls-tree -r --name-only HEAD public_en)
  [ -z "$stale" ] || { echo "translation older than its Russian source (update public_en/):$stale"; exit 3; }
fi
# Russian files without a translation are not published yet
untranslated=$(cd "$REPO" && find . -path ./.git -prune -o -type f -print0 \
  | xargs -0 perl -CSD -ne 'if (/\p{Cyrillic}/) { print "$ARGV\n"; close ARGV }' 2>/dev/null | sed 's#^\./##' | sort || true)
if [ -n "$untranslated" ]; then
  echo "left out (Russian, no translation in public_en/ yet):"; echo "$untranslated" | sed 's/^/  /'
  echo "$untranslated" | while IFS= read -r f; do rm -f "$REPO/$f"; done
fi
find "$REPO" -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
find "$REPO" -name .DS_Store -delete

# redaction (patterns are built from pieces so that this script does not contain what it removes)
U="/Use""rs/"
{ grep -rlI --exclude-dir=.git -e "${U}mac""admin" "$REPO" || true; } | while read -r f; do
  perl -pi -e "s#${U}mac\\w+/Documents/[^/]+/local-llm-accounting#<project>#g; s#${U}mac\\w+#~#g" "$f"
done
# tax numbers of companies in the journal (Portuguese NIF of legal entities start with 5)
[ ! -f "$REPO/journal.md" ] || perl -pi -e 's/(?<!\d)5\d{8}(?!\d)/<NIF>/g' "$REPO/journal.md"

cd "$REPO"
git add -A
bad=$(git ls-files | grep -E '(^|/)(docs/|predictions\.jsonl$|gt_check[^/.]*/|rescore_[^/]*/|votes\.csv$)' || true)
[ -z "$bad" ] || { echo "forbidden files in the public tree:"; echo "$bad"; exit 2; }
if git ls-files | grep -E '(^|/)fields\.csv$' | grep -v '^reports/r1_vs_r1b/fields.csv$' | grep -q .; then
  echo "per-document fields.csv in the public tree"; exit 2; fi
PAT="${U}|mac""admin@|gho_[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}|hf_[A-Za-z0-9]{30}"
if git grep -IlE -e "$PAT" -- . ':!tools/publish_public.sh' | grep -q .; then
  echo "personal data or a token pattern in the public tree:"; git grep -IlE -e "$PAT" -- . ':!tools/publish_public.sh'; exit 2; fi
if git grep -IlP '[\x{0400}-\x{04FF}]' -- . | grep -q .; then
  echo "Cyrillic in the public tree:"; git grep -IlP '[\x{0400}-\x{04FF}]' -- .; exit 2; fi
big=$(git ls-files -z | xargs -0 du -k | awk '$1>5120{print $2}')
[ -z "$big" ] || { echo "files over 5 MB:"; echo "$big"; exit 2; }
if git diff --cached --quiet; then echo "no changes to publish"; exit 0; fi
git diff --cached --stat | tail -25
if [ "$PUSH" != "--push" ]; then echo "dry run (add --push to publish). Tree: $REPO"; exit 0; fi
git -c user.name="FideNubi Research" -c user.email="research@localhost" commit -q -m "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin main
echo "published: $(git rev-parse --short HEAD)"
