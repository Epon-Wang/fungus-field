#!/usr/bin/env sh
set -eu

tagged_post=$(python3 - <<'PY'
import json
from pathlib import Path

posts = json.loads(Path("posts.json").read_text(encoding="utf-8"))
post = next(post for post in posts if "philosophy-of-language" in post["tags"])
path = Path(post["url"])
print(path if path.suffix else path / "index.html")
PY
)

rg -q '<a href="search.html"' index.html archives.html
rg -q '<a href="/fungus-field/search.html"' 404.html
rg -q '<a href="../../search.html"' "$tagged_post"
test ! -f topics.html
! rg -q 'topics\.html|>Topics<' --glob '*.html' .
test ! -f faq.html
! rg -q 'faq\.html|>FAQ<' --glob '*.html' .
rg -q 'href="search.html\?tag=philosophy-of-language"' index.html search.html
rg -q 'href="../../search.html\?tag=philosophy-of-language"' "$tagged_post"
rg -q 'URLSearchParams|searchParams' assets/js/main.js
rg -q 'data-tag-label="philosophy-of-language' search.html
