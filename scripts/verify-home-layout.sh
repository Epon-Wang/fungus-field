#!/usr/bin/env bash
set -euo pipefail

rg -n '<section class="home-info">' index.html >/dev/null

if rg -n '^\.home-info,?$' assets/css/style.css >/dev/null; then
  echo "Home intro must not share card chrome with post entries." >&2
  exit 1
fi

if ! awk '
  /^\.home-info \{/ { in_home_info = 1 }
  in_home_info && /background:|border:|box-shadow:|border-radius:/ { has_card_chrome = 1 }
  in_home_info && /^}/ { in_home_info = 0 }
  END { exit has_card_chrome ? 1 : 0 }
' assets/css/style.css; then
  echo "Home intro must not define card background, border, radius, or shadow." >&2
  exit 1
fi

