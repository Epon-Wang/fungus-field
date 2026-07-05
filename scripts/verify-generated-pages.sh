#!/usr/bin/env bash
set -euo pipefail

python3 scripts/generate-list-pages.py --check

rg -n "posts/2026-07-04_frege/|posts/2026-07-04_russell/|posts/2026-07-04_ayer/|posts/2026-07-04_ryle/|posts/2026-07-04_ambrose/" \
  index.html archives.html >/dev/null

rg -n '<span>\([0-9]+\)</span>' search.html >/dev/null

python3 - <<'PY'
import json
import re
import sys
from pathlib import Path

posts = json.loads(Path("posts.json").read_text(encoding="utf-8"))
archive = Path("archives.html").read_text(encoding="utf-8")
dates = sorted({post["date"] for post in posts})

for post_date in dates:
    count = len(re.findall(rf'<time\b[^>]*datetime="{re.escape(post_date)}"[^>]*>{re.escape(post_date)}</time>', archive))
    if count != 1:
        print(f"archives.html should show {post_date} once, found {count}", file=sys.stderr)
        sys.exit(1)

date_group_count = len(re.findall(r'class="archive-date-group"', archive))
if date_group_count != len(dates):
    print(
        f"archives.html should have one archive-date-group per date, found {date_group_count} for {len(dates)} dates",
        file=sys.stderr,
    )
    sys.exit(1)
PY

if ! awk '
  /^\.archive-date-group \{/ { in_archive_date_group = 1 }
  in_archive_date_group && /border-top: 1px solid var\(--border\);/ { has_date_top_border = 1 }
  in_archive_date_group && /^}/ { in_archive_date_group = 0 }
  END { exit has_date_top_border ? 0 : 1 }
' assets/css/style.css; then
  echo "Archive date groups must draw the separator above each date." >&2
  exit 1
fi

if rg -n '\.archive-date-group \+ \.archive-date-group' assets/css/style.css >/dev/null; then
  echo "Archive date separators should be attached to each date group, not adjacent date groups." >&2
  exit 1
fi

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
