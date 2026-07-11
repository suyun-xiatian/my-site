#!/usr/bin/env python3
"""检查静态站点中的本地链接、资源路径和 HTML 锚点。"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKIP_SCHEMES = {"data", "mailto", "tel", "javascript"}
SKIP_FRAGMENTS = {"__skip"}  # 主题在 404 页面保留的辅助跳转目标


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def resolve_target(site: Path, page: Path, raw_path: str) -> Path:
    decoded = unquote(raw_path)
    if decoded.startswith("/"):
        candidate = site / decoded.lstrip("/")
    else:
        candidate = page.parent / decoded

    if decoded.endswith("/") or candidate.is_dir():
        candidate = candidate / "index.html"
    elif not candidate.suffix:
        html_candidate = candidate.with_suffix(".html")
        index_candidate = candidate / "index.html"
        if html_candidate.exists():
            candidate = html_candidate
        elif index_candidate.exists():
            candidate = index_candidate
    return candidate.resolve()


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("site", type=Path, help="静态站点输出目录，例如 site")
    args = argument_parser.parse_args()

    site = args.site.resolve()
    pages = sorted(site.rglob("*.html"))
    if not pages:
        raise SystemExit(f"没有在 {site} 中找到 HTML 页面，请先构建网站。")

    parsed = {page.resolve(): parse_page(page) for page in pages}
    errors: list[str] = []

    for page, data in parsed.items():
        source = page.relative_to(site)
        for attribute, reference in data.references:
            parts = urlsplit(reference)
            if parts.scheme in SKIP_SCHEMES or parts.scheme in {"http", "https"} or parts.netloc:
                continue
            if not parts.path and not parts.fragment:
                continue

            target = resolve_target(site, page, parts.path) if parts.path else page
            try:
                target.relative_to(site)
            except ValueError:
                errors.append(f"{source}: {attribute}=\"{reference}\" 跳出了站点目录")
                continue

            if not target.exists():
                errors.append(f"{source}: {attribute}=\"{reference}\" 指向不存在的文件")
                continue

            if (
                parts.fragment
                and parts.fragment not in SKIP_FRAGMENTS
                and target.suffix.lower() == ".html"
            ):
                target_data = parsed.get(target)
                if target_data is None:
                    target_data = parse_page(target)
                    parsed[target] = target_data
                fragment = unquote(parts.fragment)
                if fragment not in target_data.ids:
                    errors.append(f"{source}: {attribute}=\"{reference}\" 的锚点不存在")

    if errors:
        print(f"链接检查失败，共发现 {len(errors)} 个问题：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"链接检查通过：{len(pages)} 个 HTML 页面中的本地链接、资源和锚点均有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
