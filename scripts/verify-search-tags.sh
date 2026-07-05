#!/usr/bin/env bash
set -euo pipefail

python3 scripts/generate-list-pages.py --check

if [ -f topics.html ]; then
  echo "topics.html should be removed after merging Topics into Search." >&2
  exit 1
fi

if rg -q 'topics\.html|>Topics<' --glob '*.html' .; then
  echo "Topics must be merged into Search; no standalone Topics links should remain." >&2
  exit 1
fi

rg -n '<section class="topics-list" aria-label="All tags">' search.html >/dev/null
rg -n 'data-search-tag' search.html >/dev/null
rg -n 'data-tag-label="philosophy-of-language"' search.html >/dev/null
rg -n 'href="search.html\?tag=philosophy-of-language"' search.html >/dev/null

if rg -q 'class="post-entry" data-search-item' search.html; then
  echo "Search page should list tags, not post cards." >&2
  exit 1
fi

rg -n 'data-search-post-results' search.html >/dev/null
rg -n 'data-search-post' search.html >/dev/null
rg -n 'data-title="Frege, On Sense and Nominatum"' search.html >/dev/null
rg -n 'class="search-post-list"' search.html >/dev/null
rg -n 'data-search-empty' search.html >/dev/null

if rg -q 'class="post-entry" data-search-post' search.html; then
  echo "Search post results must be compact list rows, not post cards." >&2
  exit 1
fi

rg -n 'data-search-tags-root|data-search-tag|data-search-post-results|data-search-post|post.hidden|postResults.hidden' assets/js/main.js >/dev/null
