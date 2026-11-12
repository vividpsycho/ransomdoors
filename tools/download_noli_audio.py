#!/usr/bin/env python3
"""Download all public audio files linked from the JX1DX1 Noli scrapped-skin page."""
from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

BASE = "https://forsaken2024.fandom.com"
PAGE_URL = BASE + "/wiki/Noli/Skins/Scrapped"
API = BASE + "/api.php"
OUTPUT = Path("Assets/Sounds/Noli")
AUDIO_EXTENSIONS = {".mp3", ".ogg", ".oga", ".wav"}


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ransomdoors-audio-fetcher/1.0)"})
    with urlopen(request, timeout=45) as response:
        return response.read()


def api(params: dict[str, str]) -> dict:
    data = fetch(API + "?" + urlencode(params))
    return json.loads(data)


def discover_files() -> list[str]:
    # The Fandom parse/links endpoint currently returns an empty links array for this page.
    # Parse the public page HTML as a fallback, then resolve each File page through imageinfo.
    page = fetch(PAGE_URL).decode("utf-8", errors="replace")
    found = set()
    for raw in re.findall(r'''href=["']([^"']*?/wiki/File:[^"'#?]+)''', page, flags=re.IGNORECASE):
        path = urlparse(html.unescape(raw)).path
        marker = "/wiki/File:"
        if marker not in path:
            continue
        name = unquote(path.split(marker, 1)[1]).replace("_", " ")
        if Path(name).suffix.lower() in AUDIO_EXTENSIONS:
            found.add(name)
    if found:
        return sorted(found)

    # Use the query links API as a second source. Unlike parse/links, this
    # endpoint supports continuation and returns namespace IDs explicitly.
    found = set()
    continuation: dict[str, str] = {}
    while True:
        params = {
            "action": "query",
            "titles": "Noli/Skins/Scrapped",
            "prop": "links",
            "plnamespace": "6",
            "pllimit": "max",
            "format": "json",
            "formatversion": "2",
            **continuation,
        }
        result = api(params)
        pages = result.get("query", {}).get("pages", [])
        for page_data in pages:
            for item in page_data.get("links", []):
                title = item.get("title", "")
                if title.startswith("File:"):
                    name = title.removeprefix("File:")
                    if Path(name).suffix.lower() in AUDIO_EXTENSIONS:
                        found.add(name)
        continuation = result.get("continue", {})
        if not continuation:
            break
    return sorted(found)


def main() -> int:
    print("Reading audio links from the JX1DX1 scrapped-skin page")
    names = discover_files()
    if not names:
        print("No audio file links found in the public page HTML or API.", file=sys.stderr)
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    downloaded = skipped = failed = 0
    for name in names:
        safe_name = name.replace("/", "_").replace(" ", "_")
        target = OUTPUT / safe_name
        if target.exists() and target.stat().st_size:
            skipped += 1
            continue
        try:
            result = api({
                "action": "query", "titles": "File:" + name,
                "prop": "imageinfo", "iiprop": "url",
                "format": "json", "formatversion": "2",
            })
            pages = result.get("query", {}).get("pages", [])
            info = pages[0].get("imageinfo", []) if pages else []
            if not info or not info[0].get("url"):
                raise RuntimeError("Fandom did not return a file URL")
            data = fetch(info[0]["url"])
            if not data:
                raise RuntimeError("empty response")
            target.write_bytes(data)
            downloaded += 1
            print(f"Downloaded {target.name} ({len(data):,} bytes)")
            time.sleep(0.15)
        except (HTTPError, URLError, KeyError, IndexError, RuntimeError, TimeoutError, ValueError) as exc:
            failed += 1
            print(f"FAILED {name}: {exc}", file=sys.stderr)

    print(f"\nResult: {downloaded} downloaded, {skipped} already present, {failed} failed.")
    print(f"Output: {OUTPUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
