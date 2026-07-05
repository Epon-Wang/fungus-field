#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections import OrderedDict
from datetime import date
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
POSTS_FILE = ROOT / "posts.json"
SITE_TITLE = "Fungus Field"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def tag_href(tag: str) -> str:
    return "search.html?tag=" + quote(tag.lower())


def relative_url(from_path: Path, target: str) -> str:
    return Path(os.path.relpath(ROOT / target, start=from_path.parent)).as_posix()


def post_tag_href(page_path: Path, tag: str) -> str:
    return relative_url(page_path, "search.html") + "?tag=" + quote(tag.lower())


def read_posts() -> list[dict[str, object]]:
    posts = json.loads(POSTS_FILE.read_text(encoding="utf-8"))
    if not isinstance(posts, list):
        raise ValueError("posts.json must contain a list of posts")

    normalized = []
    for index, post in enumerate(posts):
        if not isinstance(post, dict):
            raise ValueError("each post must be an object")
        title = str(post["title"]).strip()
        post_date = str(post["date"]).strip()
        url = str(post["url"]).strip()
        summary = str(post["summary"]).strip()
        tags = post["tags"]
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError(f"{title}: tags must be a list of strings")
        date.fromisoformat(post_date)
        if not url or url.startswith("/") or "://" in url:
            raise ValueError(f"{title}: url must be a relative site path")
        normalized.append(
            {
                "title": title,
                "date": post_date,
                "url": url,
                "summary": summary,
                "tags": [tag.strip().lower() for tag in tags if tag.strip()],
                "index": index,
            }
        )

    return sorted(normalized, key=lambda item: (str(item["date"]), -int(item["index"])), reverse=True)


def render_tags(post: dict[str, object], prefix: str = "", href_for_tag=tag_href) -> list[str]:
    tags = post["tags"]
    assert isinstance(tags, list)
    return [
        f'{prefix}<a class="tag" href="{href_for_tag(str(tag))}">{esc(str(tag))}</a>'
        for tag in tags
    ]


def render_home(posts: list[dict[str, object]]) -> str:
    lines = [
        "      <!-- generated:home:start -->",
        '      <section class="post-list" aria-label="Recent posts">',
    ]
    for post in posts:
        lines.extend(
            [
                '        <article class="post-entry">',
                '          <header class="entry-header">',
                f'            <h2><a href="{esc(str(post["url"]))}">{esc(str(post["title"]))}</a></h2>',
                "          </header>",
                '          <div class="entry-content">',
                f'            <p>{esc(str(post["summary"]))}</p>',
                "          </div>",
                '          <footer class="entry-footer">',
                f'            <time datetime="{esc(str(post["date"]))}">{esc(str(post["date"]))}</time>',
                '            <span class="entry-tags" aria-label="Tags">',
                *render_tags(post, "              "),
                "            </span>",
                "          </footer>",
                f'          <a class="entry-link" aria-label="Read {esc(str(post["title"]))}" href="{esc(str(post["url"]))}"></a>',
                "        </article>",
            ]
        )
    lines.extend(["      </section>", "      <!-- generated:home:end -->"])
    return "\n".join(lines)


def render_archive(posts: list[dict[str, object]]) -> str:
    grouped: OrderedDict[str, OrderedDict[str, list[dict[str, object]]]] = OrderedDict()
    for post in posts:
        year = str(post["date"])[:4]
        post_date = str(post["date"])
        grouped.setdefault(year, OrderedDict()).setdefault(post_date, []).append(post)

    lines = ["      <!-- generated:archive:start -->"]
    for year, date_groups in grouped.items():
        lines.extend(
            [
                f'      <section class="archive-year" aria-labelledby="archive-{esc(year)}">',
                f'        <h2 id="archive-{esc(year)}">{esc(year)}</h2>',
            ]
        )
        for post_date, date_posts in date_groups.items():
            lines.extend(
                [
                    '        <div class="archive-date-group">',
                    f'          <time class="archive-date" datetime="{esc(post_date)}">{esc(post_date)}</time>',
                    '          <ul class="archive-list">',
                ]
            )
            for post in date_posts:
                lines.extend(
                    [
                        "            <li>",
                        f'              <a href="{esc(str(post["url"]))}">{esc(str(post["title"]))}</a>',
                        "            </li>",
                    ]
                )
            lines.extend(["          </ul>", "        </div>"])
        lines.append("      </section>")
    lines.append("      <!-- generated:archive:end -->")
    return "\n".join(lines)


def render_search(posts: list[dict[str, object]]) -> str:
    counts = tag_counts(posts)
    lines = [
        "      <!-- generated:search:start -->",
        '      <section class="topics-list" aria-label="All tags">',
    ]
    for tag in sorted(counts):
        lines.append(
            f'        <a class="tag tag--large" href="{tag_href(tag)}" data-search-tag data-tag-label="{esc(tag)}">{esc(tag)} <span>({counts[tag]})</span></a>'
        )
    lines.extend(
        [
            "      </section>",
            '      <section class="search-post-results" data-search-post-results hidden aria-label="Matching posts">',
            '        <ul class="search-post-list">',
        ]
    )
    for post in posts:
        tags = post["tags"]
        assert isinstance(tags, list)
        tag_text = " ".join(str(tag) for tag in tags)
        lines.extend(
            [
                f'          <li data-search-post data-title="{esc(str(post["title"]))}" data-summary="{esc(str(post["summary"]))}" data-tags="{esc(tag_text)}">',
                f'            <a href="{esc(str(post["url"]))}">{esc(str(post["title"]))}</a>',
                '            <div class="search-post-meta">',
                f'              <time datetime="{esc(str(post["date"]))}">{esc(str(post["date"]))}</time>',
                f'              <span>{esc(tag_text)}</span>',
                "            </div>",
                "          </li>",
            ]
        )
    lines.extend(
        [
            "        </ul>",
            '        <p class="search-empty" data-search-empty hidden>No matches</p>',
            "      </section>",
            "      <!-- generated:search:end -->",
        ]
    )
    return "\n".join(lines)


def tag_counts(posts: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for post in posts:
        tags = post["tags"]
        assert isinstance(tags, list)
        for tag in tags:
            counts[str(tag)] = counts.get(str(tag), 0) + 1
    return counts


def render_post_head(post: dict[str, object]) -> str:
    return "\n".join(
        [
            "    <!-- generated:post-head:start -->",
            f'    <meta name="description" content="{esc(str(post["summary"]))}">',
            f'    <title>{esc(str(post["title"]))} | {SITE_TITLE}</title>',
            "    <!-- generated:post-head:end -->",
        ]
    )


def render_post_header(post: dict[str, object], page_path: Path) -> str:
    tag_lines = render_tags(
        post,
        "              ",
        href_for_tag=lambda tag: post_tag_href(page_path, tag),
    )
    return "\n".join(
        [
            "          <!-- generated:post-header:start -->",
            f'          <h1>{esc(str(post["title"]))}</h1>',
            '          <div class="post-meta">',
            f'            <time datetime="{esc(str(post["date"]))}">{esc(str(post["date"]))}</time>',
            '            <span class="entry-tags" aria-label="Tags">',
            *tag_lines,
            "            </span>",
            "          </div>",
            "          <!-- generated:post-header:end -->",
        ]
    )


def post_page_path(post: dict[str, object]) -> Path:
    path = ROOT / str(post["url"])
    if not path.suffix:
        path = path / "index.html"
    try:
        path.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f'{post["title"]}: url points outside the site root') from exc
    if not path.is_file():
        raise FileNotFoundError(f'{post["title"]}: post page not found at {path.relative_to(ROOT)}')
    return path


def replace_generated(
    content: str,
    name: str,
    rendered: str,
    fallback_pattern: str,
    marker_indent: str = "      ",
) -> str:
    start = f"{marker_indent}<!-- generated:{name}:start -->"
    end = f"{marker_indent}<!-- generated:{name}:end -->"
    marker_pattern = re.compile(
        rf"{re.escape(marker_indent)}<!-- generated:{re.escape(name)}:start -->.*?{re.escape(marker_indent)}<!-- generated:{re.escape(name)}:end -->\n?",
        re.DOTALL,
    )
    if start in content and end in content:
        return marker_pattern.sub(rendered + "\n", content)

    updated, count = re.subn(fallback_pattern, rendered + "\n", content, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"could not find {name} region")
    return updated


def build_post_page(post: dict[str, object]) -> tuple[Path, str]:
    path = post_page_path(post)
    content = path.read_text(encoding="utf-8")
    content = replace_generated(
        content,
        "post-head",
        render_post_head(post),
        r'    <meta name="description" content="[^"]*">\n    <title>.*?</title>\n',
        marker_indent="    ",
    )
    content = replace_generated(
        content,
        "post-header",
        render_post_header(post, path),
        r'          <h1>.*?</h1>\n          <div class="post-meta">.*?          </div>\n',
        marker_indent="          ",
    )
    return path, content


def build_pages(posts: list[dict[str, object]]) -> dict[Path, str]:
    specs = {
        ROOT / "index.html": (
            "home",
            render_home(posts),
            r'      <section class="post-list" aria-label="Recent posts">.*?      </section>\n?',
        ),
        ROOT / "archives.html": (
            "archive",
            render_archive(posts),
            r'      <section class="archive-year".*?      </section>\n(?=    </main>)',
        ),
        ROOT / "search.html": (
            "search",
            render_search(posts),
            r'      <section class="(?:search-results|topics-list)"[^>]*>.*?      </section>\n?',
        ),
    }

    pages: dict[Path, str] = {}
    for path, (name, rendered, fallback_pattern) in specs.items():
        content = path.read_text(encoding="utf-8")
        pages[path] = replace_generated(content, name, rendered, fallback_pattern)
    for post in posts:
        path, rendered = build_post_page(post)
        pages[path] = rendered
    return pages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated pages are out of date")
    args = parser.parse_args()

    pages = build_pages(read_posts())
    changed = []
    for path, rendered in pages.items():
        current = path.read_text(encoding="utf-8")
        if current != rendered:
            changed.append(path)
            if not args.check:
                path.write_text(rendered, encoding="utf-8")

    if changed and args.check:
        for path in changed:
            print(f"{path.relative_to(ROOT)} is not generated from posts.json", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
