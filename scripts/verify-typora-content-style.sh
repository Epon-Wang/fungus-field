#!/usr/bin/env bash
set -euo pipefail

while IFS= read -r post_file; do
  rg -n 'class="main main--post"' "$post_file" >/dev/null
  rg -n 'class="post-single post-single--typora"' "$post_file" >/dev/null
  rg -n 'class="post-content typora-content"' "$post_file" >/dev/null
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

rg -n '\.typora-content \{|\.typora-content h1|\.typora-content blockquote|\.typora-content table|\.typora-content code|\.typora-content \.mathjax-block' \
  assets/css/style.css >/dev/null

rg -n '\.main--post \{' assets/css/style.css >/dev/null

for css_pattern in '\.post-toc \{' 'position: fixed' '\.post-toc__link--level-' '@media \(min-width: 1500px\)'; do
  rg -n "$css_pattern" assets/css/style.css >/dev/null
done

for js_pattern in 'document\.querySelector\("\.main--post \.typora-content"\)' 'querySelectorAll\("h1, h2, h3, h4"\)' 'slugifyHeading' 'post-toc__link--level-' 'document\.body\.appendChild\(toc\)'; do
  rg -n "$js_pattern" assets/js/main.js >/dev/null
done

if ! awk '
  /\.typora-content p,/ { in_text_spacing = 1 }
  in_text_spacing && /white-space: normal;/ { has_normal = 1 }
  in_text_spacing && /white-space: pre-wrap;/ { has_pre_wrap = 1 }
  in_text_spacing && /^}/ { in_text_spacing = 0 }
  END { exit has_normal && !has_pre_wrap ? 0 : 1 }
' assets/css/style.css; then
  echo "Typora paragraph/list spacing must collapse formatted HTML source whitespace." >&2
  exit 1
fi

if ! awk '
  /\.typora-content mjx-container\[jax="SVG"\]\[display="true"\]/ { in_display_math = 1 }
  in_display_math && /display: block;/ { has_display_block = 1 }
  in_display_math && /text-align: center;/ { has_center = 1 }
  in_display_math && /margin: 1em 0;/ { has_margin = 1 }
  in_display_math && /^}/ { in_display_math = 0 }
  END { exit has_display_block && has_center && has_margin ? 0 : 1 }
' assets/css/style.css; then
  echo "Typora display MathJax SVG blocks must be centered." >&2
  exit 1
fi

if rg -n '^#write|^body\.typora-export|^body \{[^}]+"Open Sans"' assets/css/style.css >/dev/null; then
  echo "Typora styles must stay scoped to .typora-content." >&2
  exit 1
fi
