#!/usr/bin/env sh
set -eu

rg -q '<a href="topics.html"' index.html archives.html search.html
rg -q '<a href="/fungus-field/topics.html"' 404.html
rg -q '<a href="../../topics.html"' posts/2026-07-04_frege/index.html
test -f topics.html
test ! -f faq.html
! rg -q 'faq\.html|>FAQ<' --glob '*.html' .
rg -q 'href="search.html\?tag=philosophy-of-language"' index.html search.html topics.html
rg -q 'href="../../search.html\?tag=philosophy-of-language"' posts/2026-07-04_frege/index.html
rg -q 'URLSearchParams|searchParams' assets/js/main.js
rg -q 'data-tags="philosophy-of-language' search.html
