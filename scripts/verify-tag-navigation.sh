#!/usr/bin/env sh
set -eu

rg -q '<a href="search.html"' index.html archives.html
rg -q '<a href="/fungus-field/search.html"' 404.html
rg -q '<a href="../../search.html"' posts/2026-07-04_frege/index.html
test ! -f topics.html
! rg -q 'topics\.html|>Topics<' --glob '*.html' .
test ! -f faq.html
! rg -q 'faq\.html|>FAQ<' --glob '*.html' .
rg -q 'href="search.html\?tag=philosophy-of-language"' index.html search.html
rg -q 'href="../../search.html\?tag=philosophy-of-language"' posts/2026-07-04_frege/index.html
rg -q 'URLSearchParams|searchParams' assets/js/main.js
rg -q 'data-tag-label="philosophy-of-language' search.html
