#!/usr/bin/env bash
set -euo pipefail

python3 scripts/generate-list-pages.py --check

rg -n "posts/2026-07-04_frege/|posts/2026-07-04_russell/|posts/2026-07-04_ayer/|posts/2026-07-04_ryle/|posts/2026-07-04_ambrose/" \
  index.html archives.html search.html >/dev/null

rg -n '<span>\([0-9]+\)</span>' topics.html >/dev/null

while IFS= read -r post_file; do
  rg -n "<!-- generated:post-head:start -->" "$post_file" >/dev/null
  rg -n "<!-- generated:post-header:start -->" "$post_file" >/dev/null
done < <(python3 - <<'PY'
import json
from pathlib import Path

for post in json.loads(Path("posts.json").read_text(encoding="utf-8")):
    path = Path(post["url"])
    if not path.suffix:
        path = path / "index.html"
    print(path.as_posix())
PY
)
